#!/usr/bin/env python3
"""
Lab 2 (Day 2) — Go2 obstacle avoidance intro (visible stand + short forward move).

Sequence:
  StandUp → BalanceStand → avoid on → UseRemoteCommandFromApi(True)
  → periodic Move → stop → switch off

Usage:
  python course/student/day-02/lab-02/lab02_obstacle_avoid_intro.py en6 --dry-run
  python course/student/day-02/lab-02/lab02_obstacle_avoid_intro.py en6
  python course/student/day-02/lab-02/lab02_obstacle_avoid_intro.py en6 --vx 0.3 --move-sec 3
  python course/student/day-02/lab-02/lab02_obstacle_avoid_intro.py en6 --increment-move
  python course/student/day-02/lab-02/lab02_obstacle_avoid_intro.py en6 --compare-free-avoid
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

_DAY02 = Path(__file__).resolve().parents[1]
_DAY01 = _DAY02.parent / "day-01"
for _p in (_DAY01, _DAY02):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from go2_motion_helpers import (  # noqa: E402
    periodic_avoid_move,
    visible_stand_prep,
)
from go2_network_helpers import prepare_go2_interface  # noqa: E402

from unitree_sdk2py.core.channel import ChannelFactoryInitialize, ChannelSubscriber
from unitree_sdk2py.go2.obstacles_avoid.obstacles_avoid_client import (
    ObstaclesAvoidClient,
)
from unitree_sdk2py.go2.sport.sport_client import SportClient
from unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_


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


def _confirm_motion() -> bool:
    print()
    print("WARNING: Robot will STAND UP, then move forward under obstacle avoidance.")
    print("  - Clear ~2 m in front; use cones not people.")
    print("  - Spotter required; know estop / power switch.")
    try:
        ans = input("Type yes to continue: ").strip().lower()
    except EOFError:
        print("No TTY — use a real terminal or --dry-run")
        return False
    return ans in ("yes", "y")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "interface",
        nargs="?",
        default=None,
        help="Robot LAN NIC (or export GO2_INTERFACE)",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--vx", type=float, default=0.3, help="Forward m/s (default 0.3)")
    parser.add_argument("--move-sec", type=float, default=3.0, help="Move duration (default 3 s)")
    parser.add_argument("--move-hz", type=float, default=20.0)
    parser.add_argument(
        "--skip-stand",
        action="store_true",
        help="Skip StandUp/BalanceStand (only if already standing)",
    )
    parser.add_argument("--stand-up-wait", type=float, default=5.0)
    parser.add_argument(
        "--increment-move",
        action="store_true",
        help="After velocity Move, try MoveToIncrementPosition(dx,0,0) (SDK path goal)",
    )
    parser.add_argument(
        "--increment-dx",
        type=float,
        default=0.4,
        help="Forward metres for increment move (default 0.4)",
    )
    parser.add_argument(
        "--compare-free-avoid",
        action="store_true",
        help="Briefly toggle SportClient.FreeAvoid vs ObstaclesAvoidClient",
    )
    parser.add_argument("-y", "--yes", action="store_true")
    args = parser.parse_args()

    if not os.environ.get("CYCLONEDDS_HOME"):
        print("ERROR: CYCLONEDDS_HOME is not set. See Day 1 Lab 0.")
        return 1

    iface, err = prepare_go2_interface(args.interface, ping_robot=not args.dry_run)
    if err:
        return err
    assert iface is not None

    if abs(args.vx) > 0.4 and not args.dry_run:
        print(f"WARN: |vx|={args.vx} is high for training; prefer <= 0.35")

    print(f"Interface: {iface}")
    extras = []
    if args.increment_move:
        extras.append(f"MoveToIncrementPosition({args.increment_dx},0,0)")
    if args.compare_free_avoid:
        extras.append("FreeAvoid compare")
    extra_txt = (" + " + " + ".join(extras)) if extras else ""
    print(f"Plan: stand prep → avoid Move vx={args.vx} for {args.move_sec}s{extra_txt}")

    if args.dry_run:
        print("[dry-run] StandUp → BalanceStand → avoid on → Move → stop → off")
        if args.increment_move:
            print(f"         → MoveToIncrementPosition({args.increment_dx},0,0)")
        if args.compare_free_avoid:
            print("         → SportClient.FreeAvoid demo")
        return 0

    if not args.yes and not _confirm_motion():
        print("Aborted.")
        return 1

    _init_dds(iface)
    if not _wait_sportmodestate():
        print("FAIL: no rt/sportmodestate — complete Day 1 Labs 0 and 3 first")
        return 1

    sport = SportClient()
    sport.SetTimeout(10.0)
    sport.Init()

    avoid = ObstaclesAvoidClient()
    avoid.SetTimeout(3.0)
    avoid.Init()

    step = 1

    def nxt(label: str) -> None:
        nonlocal step
        print(f"[{step}/7] {label}")
        step += 1

    try:
        nxt("Visible stand prep")
        visible_stand_prep(
            sport,
            skip=args.skip_stand,
            stand_up_wait_s=args.stand_up_wait,
        )

        nxt("ObstaclesAvoidClient.SwitchSet(True)")
        for _ in range(30):
            if avoid.SwitchSet(True) == 0:
                _, on = avoid.SwitchGet()
                if on:
                    break
            time.sleep(0.1)
        code, enabled = avoid.SwitchGet()
        print(f"      SwitchGet: code={code} enable={enabled}")
        if code != 0 or not enabled:
            print("FAIL: could not enable obstacle avoidance")
            return 1

        nxt("UseRemoteCommandFromApi(True)")
        print(f"      code={avoid.UseRemoteCommandFromApi(True)}")
        time.sleep(0.5)

        nxt(f"Move({args.vx}, 0, 0) for {args.move_sec}s")
        periodic_avoid_move(avoid, args.vx, 0.0, 0.0, args.move_sec, args.move_hz)

        if args.increment_move:
            nxt(f"MoveToIncrementPosition({args.increment_dx}, 0, 0)")
            for _ in range(int(args.move_hz * max(args.move_sec, 2.0))):
                avoid.MoveToIncrementPosition(args.increment_dx, 0.0, 0.0)
                time.sleep(1.0 / args.move_hz)
            print("      (sent increment goal — watch robot; firmware may blend with avoid)")

        if args.compare_free_avoid:
            nxt("SportClient.FreeAvoid(True) — sport-layer avoid toggle")
            print(f"      code={sport.FreeAvoid(True)}")
            time.sleep(1.0)
            print(f"      FreeAvoid(False) code={sport.FreeAvoid(False)}")

        nxt("Stop — Move(0,0,0), remote API off")
        for _ in range(15):
            avoid.Move(0.0, 0.0, 0.0)
            time.sleep(0.05)
        avoid.UseRemoteCommandFromApi(False)
        time.sleep(0.5)
        sport.StopMove()

        nxt("SwitchSet(False)")
        avoid.SwitchSet(False)
        print(f"      enable={avoid.SwitchGet()[1]}")

    except KeyboardInterrupt:
        print("\nInterrupt — stopping...")
        avoid.Move(0.0, 0.0, 0.0)
        avoid.UseRemoteCommandFromApi(False)
        avoid.SwitchSet(False)
        sport.StopMove()
        return 130

    print()
    print("Summary: PASS — Lab 4 avoid intro complete")
    print("  If no forward motion: confirm avoid enabled + sport mode in app.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
