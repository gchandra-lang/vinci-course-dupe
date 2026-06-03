#!/usr/bin/env python3
"""
Lab 2 — First visible SportClient motion: StandUp → BalanceStand → forward walk.

Default includes a short walk (most visible). Use --posture-only to skip translation.

Usage:
  python course/day-01/New-lab/lab-03/lab02_safe_posture.py en6 --dry-run
  python course/day-01/New-lab/lab-03/lab02_safe_posture.py en6
  python course/day-01/New-lab/lab-03/lab02_safe_posture.py en6 --posture-only
  python course/day-01/New-lab/lab-03/lab02_safe_posture.py en6 --vx 0.3 --move-sec 3
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

# Import shared helper from course/day-01/
_DAY01 = Path(__file__).resolve().parents[2]
_NEW_LAB = Path(__file__).resolve().parent.parent
for _p in (_NEW_LAB, _DAY01):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from go2_network_helpers import dds_failure_hint, prepare_go2_interface  # noqa: E402
from go2_motion_helpers import (  # noqa: E402
    periodic_sport_move,
    set_gait_classic_walk,
    visible_stand_prep,
)

from unitree_sdk2py.core.channel import ChannelFactoryInitialize, ChannelSubscriber
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
        got.append(1)

    sub = ChannelSubscriber("rt/sportmodestate", SportModeState_)
    sub.Init(handler, 10)
    deadline = time.time() + timeout_s
    while time.time() < deadline and not got:
        time.sleep(0.05)
    return bool(got)


def _confirm(walk: bool) -> bool:
    print()
    if walk:
        print("WARNING: Robot will STAND UP, balance, then walk forward ~3 s.")
    else:
        print("WARNING: Robot will STAND UP and balance (no forward walk).")
    print("  Clear ~2 m; spotter required.")
    try:
        return input("Type yes to continue: ").strip().lower() in ("yes", "y")
    except EOFError:
        print("No TTY — use a real terminal or --dry-run")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "interface",
        nargs="?",
        default=None,
        help="PC NIC to Go2 (omit to auto-detect 192.168.123.x)",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--posture-only",
        action="store_true",
        help="StandUp + BalanceStand only (no forward walk)",
    )
    parser.add_argument("--skip-stand", action="store_true", help="Skip StandUp/BalanceStand prep")
    parser.add_argument("--vx", type=float, default=0.3, help="Forward m/s (default 0.3)")
    parser.add_argument("--move-sec", type=float, default=3.0, help="Walk duration (default 3 s)")
    parser.add_argument("--move-hz", type=float, default=20.0)
    parser.add_argument("--stand-up-wait", type=float, default=5.0, help="Seconds after StandUp")
    parser.add_argument("-y", action="store_true", help="Skip confirmation")
    parser.add_argument(
        "--classic-walk",
        action="store_true",
        help="Call ClassicWalk(True) after BalanceStand (sport gait RPC)",
    )
    args = parser.parse_args()

    walk = not args.posture_only

    if not os.environ.get("CYCLONEDDS_HOME"):
        print("ERROR: CYCLONEDDS_HOME is not set.")
        return 1

    iface, code = prepare_go2_interface(args.interface)
    if code != 0:
        return code
    args.interface = iface

    print(f"Interface: {args.interface}")
    plan = []
    if not args.skip_stand:
        plan += ["StandUp()", "BalanceStand()"]
    if walk:
        plan.append(f"Move({args.vx},0,0) ~{args.move_sec}s @ {args.move_hz}Hz")
        plan.append("StopMove()")

    if args.dry_run:
        print("[dry-run]", " → ".join(plan) if plan else "(nothing)")
        return 0

    if not args.y and not _confirm(walk):
        print("Aborted.")
        return 1

    try:
        _init_dds(args.interface)
    except Exception as e:
        print(f"ERROR: ChannelFactoryInitialize failed: {e}\n")
        print(dds_failure_hint(args.interface))
        return 1
    if not _wait_sportmodestate():
        print("FAIL: no sportmodestate — complete Lab 3 first\n")
        print(dds_failure_hint(args.interface))
        return 1

    sport = SportClient()
    sport.SetTimeout(10.0)
    sport.Init()

    try:
        visible_stand_prep(
            sport,
            skip=args.skip_stand,
            stand_up_wait_s=args.stand_up_wait,
        )

        if args.classic_walk:
            set_gait_classic_walk(sport, True)

        if walk:
            print(f"[walk] Move({args.vx}, 0, 0) for {args.move_sec}s")
            err = periodic_sport_move(
                sport, args.vx, 0.0, 0.0, args.move_sec, args.move_hz
            )
            if err != 0:
                print(f"    Move returned code={err}")
            print("[walk] StopMove()")
            print(f"        code={sport.StopMove()}")
        else:
            print("[walk] skipped (--posture-only)")

    except KeyboardInterrupt:
        sport.StopMove()
        return 130

    print()
    print("Summary: PASS — visible SportClient motion complete")
    print("  If you saw no movement: Unitree app sport mode, estop, or use menu stand_up (1).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
