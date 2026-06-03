#!/usr/bin/env python3
"""
Lab 4 — Go2 sport RPC readiness (read-only). No stand, move, or damp commands.

Usage:
  conda activate unitree_env
  export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
  unset CYCLONEDDS_URI
  python course/day-01/New-lab/lab-04/lab04_sport_readonly.py enx207bd22b611a
  python course/day-01/New-lab/lab-04/lab04_sport_readonly.py enx207bd22b611a --watch 10

  export GO2_INTERFACE=enx207bd22b611a   # optional default instead of enp0s31f6
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

_LAB_DIR = Path(__file__).resolve().parent
_NEW_LAB = _LAB_DIR.parent
if str(_NEW_LAB) not in sys.path:
    sys.path.insert(0, str(_NEW_LAB))

from go2_network_helpers import dds_failure_hint, prepare_go2_interface  # noqa: E402

from unitree_sdk2py.comm.motion_switcher.motion_switcher_client import (
    MotionSwitcherClient,
)
from unitree_sdk2py.core.channel import ChannelFactoryInitialize, ChannelSubscriber
from unitree_sdk2py.go2.sport.sport_client import SportClient
from unitree_sdk2py.idl.unitree_go.msg.dds_ import LowState_, SportModeState_

# Same set as scripts/go2_connection_check.py
GO2_CHECKMODE_OK = frozenset({"mcf", "ai", "normal", "sport"})


def _init_dds(iface: str) -> None:
    if os.environ.get("CYCLONEDDS_URI"):
        print("Warning: CYCLONEDDS_URI is set; unset it for interface-only init.")
        ChannelFactoryInitialize(0)
    else:
        ChannelFactoryInitialize(0, iface)


def _wait_topic(
    topic: str,
    msg_type: type,
    timeout_s: float,
) -> tuple[bool, str]:
    sample: list[object] = []

    def handler(msg) -> None:
        sample.append(msg)

    sub = ChannelSubscriber(topic, msg_type)
    sub.Init(handler, 10)
    deadline = time.time() + timeout_s
    while time.time() < deadline and not sample:
        time.sleep(0.05)

    if not sample:
        return False, "no messages"

    msg = sample[0]
    if topic == "rt/sportmodestate":
        return True, f"mode={int(msg.mode)} gait_type={int(msg.gait_type)} error_code={int(msg.error_code)}"
    if topic == "rt/lowstate":
        return True, f"tick={int(msg.tick)} motors={len(msg.motor_state) if msg.motor_state else 0}"
    return True, "ok"


def _read_rpc() -> dict[str, object]:
    msc = MotionSwitcherClient()
    msc.SetTimeout(10.0)
    msc.Init()
    mode_code, check_mode = msc.CheckMode()

    sport = SportClient()
    sport.SetTimeout(10.0)
    sport.Init()

    ar_code, ar_enabled = sport.AutoRecoveryGet()

    return {
        "mode_code": mode_code,
        "check_mode": check_mode,
        "mode_name": str(check_mode.get("name", "")).lower() if isinstance(check_mode, dict) else "",
        "sport_init": True,
        "auto_recovery_code": ar_code,
        "auto_recovery_enabled": ar_enabled,
    }


def _print_report(iface: str, rpc: dict[str, object], sport_ok: bool, sport_detail: str, low_ok: bool, low_detail: str) -> int:
    print(f"Interface: {iface}")
    print()

    print("[DDS topics]")
    print(f"  rt/sportmodestate: {'OK' if sport_ok else 'FAIL'} ({sport_detail})")
    print(f"  rt/lowstate:       {'OK' if low_ok else 'FAIL'} ({low_detail})")

    print()
    print("[Motion switcher RPC]")
    mode_code = rpc["mode_code"]
    check_mode = rpc["check_mode"]
    mode_name = rpc["mode_name"]
    if mode_code != 0:
        print(f"  CheckMode: FAIL (code={mode_code}, result={check_mode})")
        mode_ok = False
    else:
        mode_ok = mode_name in GO2_CHECKMODE_OK or bool(mode_name)
        mark = "OK" if mode_ok else "WARN"
        print(f"  CheckMode: {mark}  name={mode_name!r}  full={check_mode}")
        if mode_name == "mcf":
            print("        (mcf is normal on Go2 — not G1's 'ai')")

    print()
    print('[SportClient RPC — service "sport"]')
    print("  Init: OK")
    ar_code = rpc["auto_recovery_code"]
    ar_val = rpc["auto_recovery_enabled"]
    if ar_code == 0:
        print(f"  AutoRecoveryGet: OK  enabled={ar_val!r}")
    else:
        print(f"  AutoRecoveryGet: optional read failed (code={ar_code})")

    print()
    dds_ok = sport_ok and low_ok
    rpc_ok = rpc["sport_init"] and mode_code == 0

    if dds_ok and rpc_ok and mode_ok:
        print("Readiness: PASS — OK for supervised sport menu (Lab 2 Step 2) and Lab 3+")
        print("  Next: ./scripts/run_go2_highlevel.sh", iface)
        print("        Try: list → balanced stand (9). Avoid damp (0) and flips.")
        return 0

    if dds_ok and rpc_ok and not mode_ok:
        print("Readiness: PARTIAL — DDS + SportClient OK; CheckMode name unusual.")
        print("  Sport menu may still work. See docs/GO2-FIELD-GUIDE.md")
        return 2

    if dds_ok and not rpc_ok:
        print("Readiness: PARTIAL — DDS OK; sport RPC issue.")
        return 2

    print("Readiness: FAIL — fix Lab 0 (network / DDS / SDK)")
    if not sport_ok:
        print()
        print(dds_failure_hint(iface))
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "interface",
        nargs="?",
        default=None,
        help="PC NIC wired to Go2 (omit to auto-detect 192.168.123.x). Not the robot IP.",
    )
    parser.add_argument(
        "--watch",
        type=float,
        metavar="SEC",
        help="Re-print report every 2s for SEC seconds (read-only)",
    )
    args = parser.parse_args()

    if not os.environ.get("CYCLONEDDS_HOME"):
        print("ERROR: CYCLONEDDS_HOME is not set. See Lab 0.")
        return 1

    iface, code = prepare_go2_interface(args.interface)
    if code != 0:
        return code
    args.interface = iface

    def once() -> int:
        try:
            _init_dds(args.interface)
        except Exception as e:
            print(f"ERROR: ChannelFactoryInitialize failed: {e}\n")
            print(dds_failure_hint(args.interface))
            return 1
        sport_ok, sport_detail = _wait_topic("rt/sportmodestate", SportModeState_, 5.0)
        low_ok, low_detail = _wait_topic("rt/lowstate", LowState_, 5.0)
        rpc = _read_rpc()
        return _print_report(args.interface, rpc, sport_ok, sport_detail, low_ok, low_detail)

    if not args.watch:
        return once()

    end = time.time() + args.watch
    last = 0
    while time.time() < end:
        print("=" * 60)
        last = once()
        print()
        time.sleep(2.0)
    return last


if __name__ == "__main__":
    sys.exit(main())
