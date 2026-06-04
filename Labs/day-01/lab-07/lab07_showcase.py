#!/usr/bin/env python3
"""
Lab 2b — SportClient showcase (gestures + optional handstand).

Runs after lab02_safe_posture.py when the dog is already standing.
Default: Hello → Stretch → Heart. Handstand is opt-in only (--wow-handstand).

Usage:
  python course/day-01/New-lab/lab-03/lab02_showcase.py en6 --dry-run
  python course/day-01/New-lab/lab-03/lab02_showcase.py en6 --skip-stand
  python course/day-01/New-lab/lab-03/lab02_showcase.py en6 --gestures hello,heart
  python course/day-01/New-lab/lab-03/lab02_showcase.py en6 --wow-handstand
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

_DAY01 = Path(__file__).resolve().parents[2]
_NEW_LAB = Path(__file__).resolve().parent.parent
for _p in (_NEW_LAB, _DAY01):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from go2_network_helpers import dds_failure_hint, prepare_go2_interface  # noqa: E402
from go2_motion_helpers import (  # noqa: E402
    SHOWCASE_GESTURES,
    run_showcase,
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


def _confirm(handstand: bool) -> bool:
    print()
    print("WARNING: Robot will run sport showcase gestures (Hello / Stretch / Heart).")
    if handstand:
        print("  HANDSTAND enabled — acrobatic; instructor + spotter; ~3 m clear.")
    print("  Flat floor; know estop / power switch.")
    try:
        ans = input("Type yes to continue: ").strip().lower()
    except EOFError:
        print("No TTY — use a real terminal or --dry-run")
        return False
    if ans not in ("yes", "y"):
        return False
    if not handstand:
        return True
    try:
        ans2 = input('Type handstand to confirm acrobatic trick: ').strip().lower()
    except EOFError:
        return False
    return ans2 == "handstand"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "interface",
        nargs="?",
        default=None,
        help="PC NIC to Go2 (omit to auto-detect 192.168.123.x)",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-stand", action="store_true", help="Skip StandUp/BalanceStand if already up")
    parser.add_argument(
        "--gestures",
        default=",".join(SHOWCASE_GESTURES),
        help="Comma-separated: hello,stretch,heart",
    )
    parser.add_argument(
        "--wow-handstand",
        action="store_true",
        help="After gestures, HandStand(True) then HandStand(False) — instructor only",
    )
    parser.add_argument("--handstand-hold", type=float, default=4.0)
    parser.add_argument("--pause", type=float, default=3.0, help="Seconds between gestures")
    parser.add_argument("-y", action="store_true", help="Skip confirmation (not for handstand)")
    args = parser.parse_args()

    gestures = tuple(g.strip().lower() for g in args.gestures.split(",") if g.strip())
    handstand = args.wow_handstand

    if not os.environ.get("CYCLONEDDS_HOME"):
        print("ERROR: CYCLONEDDS_HOME is not set.")
        return 1

    iface, code = prepare_go2_interface(args.interface)
    if code != 0:
        return code
    args.interface = iface

    plan = []
    if not args.skip_stand:
        plan += ["StandUp()", "BalanceStand()"]
    plan.append(f"showcase: {', '.join(gestures)}")
    if handstand:
        plan.append("HandStand(True/False)")

    print(f"Interface: {args.interface}")
    if args.dry_run:
        print("[dry-run]", " → ".join(plan))
        return 0

    if handstand and not _confirm(True):
        print("Aborted.")
        return 1
    if not handstand and not args.y and not _confirm(False):
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
        visible_stand_prep(sport, skip=args.skip_stand)
        run_showcase(
            sport,
            gestures=gestures,
            handstand=handstand,
            handstand_hold_s=args.handstand_hold,
            pause_s=args.pause,
        )
    except KeyboardInterrupt:
        sport.StopMove()
        sport.BalanceStand()
        return 130

    print()
    print("Summary: PASS — Lab 2b showcase complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
