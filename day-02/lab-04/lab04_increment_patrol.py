#!/usr/bin/env python3
"""
Lab 4 (Day 2) — Multi-leg patrol using ObstaclesAvoidClient increment goals.

Sequence:
  StandUp → BalanceStand → avoid on → for each leg in patrol_plan.json
  → MoveToIncrementPosition → dwell → stop → avoid off

Usage:
  python course/student/day-02/lab-04/lab04_increment_patrol.py en6 --dry-run
  python course/student/day-02/lab-04/lab04_increment_patrol.py en6
  python course/student/day-02/lab-04/lab04_increment_patrol.py en6 --plan patrol_plan.cone_course.json
  python course/student/day-02/lab-04/lab04_increment_patrol.py en6 --plan ../lab-01/../run_dry/patrol_plan.json \\
      --scenario ../lab-00/my_team_scenario.json -y
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

_DAY02 = Path(__file__).resolve().parents[1]
_DAY01 = _DAY02.parent / "day-01"
for _p in (_DAY01, _DAY02):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from go2_motion_helpers import visible_stand_prep  # noqa: E402
from go2_network_helpers import prepare_go2_interface  # noqa: E402
from go2_patrol_helpers import (  # noqa: E402
    checkpoint_dwell,
    clamp_plan_to_limits,
    enable_avoid,
    load_patrol_plan,
    load_scenario_limits,
    release_avoid,
    run_increment_leg,
    run_velocity_leg,
)

from unitree_sdk2py.core.channel import ChannelFactoryInitialize, ChannelSubscriber
from unitree_sdk2py.go2.obstacles_avoid.obstacles_avoid_client import (
    ObstaclesAvoidClient,
)
from unitree_sdk2py.go2.sport.sport_client import SportClient
from unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_

LAB02 = Path(__file__).resolve().parent
DEFAULT_PLAN = LAB02 / "patrol_plan.cone_course.json"


def _init_dds(iface: str) -> None:
    if os.environ.get("CYCLONEDDS_URI"):
        print("Warning: CYCLONEDDS_URI is set; unset it for interface-only init.")
        ChannelFactoryInitialize(0)
    else:
        ChannelFactoryInitialize(0, iface)


def _wait_sportmodestate(timeout_s: float = 8.0) -> bool:
    got: list[int] = []

    def handler(msg: SportModeState_) -> None:
        got.append(int(msg.mode))

    sub = ChannelSubscriber("rt/sportmodestate", SportModeState_)
    sub.Init(handler, 10)
    deadline = time.time() + timeout_s
    while time.time() < deadline and not got:
        time.sleep(0.05)
    return bool(got)


def _confirm(n_legs: int) -> bool:
    print()
    print(f"WARNING: Robot will STAND UP and run {n_legs} avoid increment leg(s).")
    print("  - Cleared cone course; spotter required; max forward increment ≤ 0.5 m per leg.")
    print("  - Remote / app can override — keep estop ready.")
    try:
        return input("Type yes to continue: ").strip().lower() in ("yes", "y")
    except EOFError:
        print("No TTY — use a real terminal or --dry-run")
        return False


def _print_plan_summary(plan: dict[str, Any]) -> None:
    cps = plan.get("checkpoints") or []
    legs = plan.get("legs") or []
    print(f"Plan: {len(cps)} checkpoints, {len(legs)} legs")
    for i, leg in enumerate(legs, start=1):
        if not isinstance(leg, dict):
            continue
        ltype = leg.get("type", "?")
        to_cp = leg.get("to_checkpoint", "?")
        if ltype == "increment":
            print(
                f"  leg {i}: increment → {to_cp} "
                f"dx={leg.get('dx', 0)} dy={leg.get('dy', 0)} dyaw={leg.get('dyaw', 0)}"
            )
        elif ltype == "velocity":
            print(
                f"  leg {i}: velocity → {to_cp} "
                f"vx={leg.get('vx', 0)} for {leg.get('duration_s', '?')}s"
            )
        else:
            print(f"  leg {i}: {ltype} → {to_cp}")


def _dry_run_steps(
    plan: dict[str, Any],
    *,
    leg_pulses: int,
    leg_settle_s: float,
    stream: bool,
) -> None:
    cps = plan.get("checkpoints") or []
    print("[dry-run] StandUp → BalanceStand → avoid on → UseRemoteCommandFromApi(True)")
    for i, leg in enumerate(plan.get("legs") or [], start=1):
        if not isinstance(leg, dict):
            continue
        to_cp = leg.get("to_checkpoint", "?")
        if leg.get("type") == "increment":
            mode = (
                f"stream ~{leg_settle_s}s"
                if stream
                else f"{leg_pulses} pulse(s) + settle {leg_settle_s}s"
            )
            print(
                f"[dry-run] leg {i}: MoveToIncrementPosition("
                f"{leg.get('dx', 0)}, {leg.get('dy', 0)}, {leg.get('dyaw', 0)}) "
                f"— {mode}"
            )
        elif leg.get("type") == "velocity":
            print(
                f"[dry-run] leg {i}: Move({leg.get('vx', 0)}, ...) "
                f"for {leg.get('duration_s', leg_settle_s)}s"
            )
        dwell = checkpoint_dwell(cps, str(to_cp), 2.0)
        print(f"[dry-run] dwell at {to_cp}: {dwell}s")
    print("[dry-run] stop → avoid off")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "interface",
        nargs="?",
        default=None,
        help="Robot LAN NIC (or export GO2_INTERFACE)",
    )
    parser.add_argument(
        "--plan",
        type=Path,
        default=DEFAULT_PLAN,
        help="patrol_plan.json (default: lab cone course)",
    )
    parser.add_argument(
        "--scenario",
        type=Path,
        default=None,
        help="Lab 0 scenario JSON — clamp legs to motion_limits",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-stand", action="store_true")
    parser.add_argument("--stand-up-wait", type=float, default=5.0)
    parser.add_argument(
        "--leg-wait",
        type=float,
        default=5.0,
        help="Settle seconds after increment pulses (default 5)",
    )
    parser.add_argument(
        "--leg-pulses",
        type=int,
        default=3,
        help="How many times to send each increment goal (default 3)",
    )
    parser.add_argument(
        "--leg-hz",
        type=float,
        default=2.0,
        help="Pulse rate when sending increment goals (default 2)",
    )
    parser.add_argument(
        "--stream-increment",
        action="store_true",
        help="Legacy: repeat increment for whole --leg-wait window",
    )
    parser.add_argument(
        "--default-dwell",
        type=float,
        default=2.0,
        help="Dwell at checkpoint if plan omits dwell_s",
    )
    parser.add_argument("-y", "--yes", action="store_true")
    args = parser.parse_args()

    if not os.environ.get("CYCLONEDDS_HOME"):
        print("ERROR: CYCLONEDDS_HOME is not set. See Lab 0.")
        return 1

    plan_path = args.plan.resolve()
    if not plan_path.is_file():
        print(f"ERROR: plan not found: {plan_path}")
        return 1

    try:
        plan = load_patrol_plan(plan_path)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"ERROR: {e}")
        return 1

    limits = load_scenario_limits(args.scenario.resolve() if args.scenario else None)
    for msg in clamp_plan_to_limits(plan, limits):
        print(f"WARN: {msg}")

    legs = [lg for lg in (plan.get("legs") or []) if isinstance(lg, dict)]
    if not legs:
        print("ERROR: patrol plan has no legs")
        return 1

    iface, err = prepare_go2_interface(args.interface, ping_robot=not args.dry_run)
    if err:
        return err
    assert iface is not None

    print(f"Interface: {iface}")
    print(f"Plan file: {plan_path}")
    _print_plan_summary(plan)

    if args.dry_run:
        _dry_run_steps(
            plan,
            leg_pulses=args.leg_pulses,
            leg_settle_s=args.leg_wait,
            stream=args.stream_increment,
        )
        return 0

    if not args.yes and not _confirm(len(legs)):
        print("Aborted.")
        return 1

    _init_dds(iface)
    if not _wait_sportmodestate():
        print("FAIL: no rt/sportmodestate")
        return 1

    sport = SportClient()
    sport.SetTimeout(10.0)
    sport.Init()

    avoid = ObstaclesAvoidClient()
    avoid.SetTimeout(3.0)
    avoid.Init()

    checkpoints: list[dict[str, Any]] = list(plan.get("checkpoints") or [])
    step = 1
    total = 3 + len(legs) * 2

    def nxt(label: str) -> None:
        nonlocal step
        print(f"[{step}/{total}] {label}")
        step += 1

    try:
        nxt("Visible stand prep")
        visible_stand_prep(
            sport,
            skip=args.skip_stand,
            stand_up_wait_s=args.stand_up_wait,
        )

        nxt("Enable obstacle avoidance")
        if not enable_avoid(avoid):
            print("FAIL: SwitchSet(True) did not stick")
            return 1
        print(f"      SwitchGet enable={avoid.SwitchGet()[1]}")

        nxt("UseRemoteCommandFromApi(True)")
        print(f"      code={avoid.UseRemoteCommandFromApi(True)}")
        time.sleep(0.5)

        for i, leg in enumerate(legs, start=1):
            ltype = str(leg.get("type", "increment"))
            to_cp = str(leg.get("to_checkpoint", f"leg{i}"))

            if ltype == "increment":
                dx = float(leg.get("dx", 0.0))
                dy = float(leg.get("dy", 0.0))
                dyaw = float(leg.get("dyaw", 0.0))
                nxt(f"Leg {i}: increment → {to_cp} (dx={dx})")
                run_increment_leg(
                    avoid,
                    dx,
                    dy,
                    dyaw,
                    pulses=args.leg_pulses,
                    pulse_hz=args.leg_hz,
                    settle_s=args.leg_wait,
                    stream=args.stream_increment,
                    stream_duration_s=args.leg_wait,
                    stream_hz=args.leg_hz,
                )
            elif ltype == "velocity":
                vx = float(leg.get("vx", 0.0))
                vy = float(leg.get("vy", 0.0))
                vyaw = float(leg.get("vyaw", 0.0))
                dur = float(leg.get("duration_s", args.leg_wait))
                nxt(f"Leg {i}: velocity → {to_cp} (vx={vx}, {dur}s)")
                run_velocity_leg(avoid, vx, vy, vyaw, dur, args.leg_hz)
            else:
                print(f"WARN: skip unknown leg type {ltype!r}")
                continue

            dwell = checkpoint_dwell(checkpoints, to_cp, args.default_dwell)
            nxt(f"Dwell at {to_cp} ({dwell}s)")
            time.sleep(dwell)

        nxt("Stop and release avoid API")
        release_avoid(avoid, sport)

    except KeyboardInterrupt:
        print("\nInterrupt — stopping...")
        release_avoid(avoid, sport)
        return 130

    print()
    print("Summary: PASS — Lab 2 increment patrol complete")
    print("  If a leg fell short: reduce dx or increase --leg-wait.")
    print("  Next: Lab 3 integrated runner + checkpoint capture.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
