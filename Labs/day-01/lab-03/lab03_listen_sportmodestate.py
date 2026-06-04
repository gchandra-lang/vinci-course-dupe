#!/usr/bin/env python3
"""
Lab 3 — Subscribe to Go2 rt/sportmodestate (and optional rt/lowstate). No motion commands.

Usage:
  conda activate unitree_env
  export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
  unset CYCLONEDDS_URI
  python course/day-01/New-lab/lab-03/lab03_listen_sportmodestate.py enx207bd22b611a
  python course/day-01/New-lab/lab-03/lab03_listen_sportmodestate.py enx207bd22b611a --duration 15 --rate 1
  python course/day-01/New-lab/lab-03/lab03_listen_sportmodestate.py enx207bd22b611a --once
  python course/day-01/New-lab/lab-03/lab03_listen_sportmodestate.py enx207bd22b611a --lowstate --log sportmodestate_log.jsonl

  # Or set once per shell: export GO2_INTERFACE=enx207bd22b611a
  # Doc placeholders (enp0s31f6, ens33) only if that is YOUR link — see ip -br addr
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

_LAB_DIR = Path(__file__).resolve().parent
_NEW_LAB = _LAB_DIR.parent
if str(_NEW_LAB) not in sys.path:
    sys.path.insert(0, str(_NEW_LAB))

from go2_network_helpers import dds_failure_hint, prepare_go2_interface  # noqa: E402

from unitree_sdk2py.core.channel import ChannelFactoryInitialize, ChannelSubscriber
from unitree_sdk2py.idl.unitree_go.msg.dds_ import LowState_, SportModeState_


def _init_dds(iface: str) -> None:
    if os.environ.get("CYCLONEDDS_URI"):
        print("Warning: CYCLONEDDS_URI is set; unset it for interface-only init.")
        ChannelFactoryInitialize(0)
    else:
        ChannelFactoryInitialize(0, iface)


def _vec3(label: str, v: Any) -> str:
    try:
        return f"{label}=({float(v[0]):.3f},{float(v[1]):.3f},{float(v[2]):.3f})"
    except (TypeError, IndexError, ValueError):
        return f"{label}=?"


def _format_sport(msg: SportModeState_, count: int) -> str:
    vel = msg.velocity
    pos = msg.position
    return (
        f"[{count:4d}] mode={msg.mode} gait_type={msg.gait_type} "
        f"progress={msg.progress} error_code={msg.error_code} "
        f"body_height={msg.body_height:.3f} "
        f"{_vec3('vel', vel)} {_vec3('pos', pos)} "
        f"yaw_speed={msg.yaw_speed:.3f}"
    )


def _format_lowstate(msg: LowState_, count: int, *, inspect: bool = False) -> str:
    imu = msg.imu_state
    n_motors = len(msg.motor_state) if msg.motor_state else 0
    base = (
        f"[{count:4d}] tick={msg.tick} "
        f"{_vec3('imu_rpy', imu.rpy)} "
        f"motors={n_motors} bandwidth={msg.bandwidth}"
    )
    if not inspect:
        return base
    bms = msg.bms_state
    soc = getattr(bms, "soc", None)
    extra = (
        f" power_v={msg.power_v:.2f} power_a={msg.power_a:.2f}"
        f" bms_soc={soc}"
    )
    wr = msg.wireless_remote
    if wr is not None and len(wr) >= 4:
        extra += f" wireless_remote[0:4]={list(wr[:4])}"
    return base + extra


def _sport_record(msg: SportModeState_, count: int, t: float) -> dict[str, Any]:
    return {
        "t": round(t, 3),
        "n": count,
        "topic": "rt/sportmodestate",
        "mode": int(msg.mode),
        "gait_type": int(msg.gait_type),
        "progress": float(msg.progress),
        "error_code": int(msg.error_code),
        "body_height": float(msg.body_height),
        "yaw_speed": float(msg.yaw_speed),
        "velocity": [float(msg.velocity[i]) for i in range(3)],
        "position": [float(msg.position[i]) for i in range(3)],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "interface",
        nargs="?",
        default=None,
        help="PC NIC wired to Go2 (omit to auto-detect 192.168.123.x). Not the robot IP.",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=10.0,
        help="Seconds to listen after first sport message (default: 10)",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Print first sportmodestate message and exit",
    )
    parser.add_argument(
        "--rate",
        type=float,
        default=2.0,
        help="Max print rate in Hz for sportmodestate (default: 2)",
    )
    parser.add_argument(
        "--lowstate",
        action="store_true",
        help="Also subscribe to rt/lowstate and print first sample",
    )
    parser.add_argument(
        "--log",
        metavar="PATH",
        default=None,
        help="Append JSON lines (sportmodestate) at print rate",
    )
    parser.add_argument(
        "--inspect",
        action="store_true",
        help="With --lowstate: print BMS/power/wireless_remote on first sample",
    )
    args = parser.parse_args()
    if args.inspect:
        args.lowstate = True

    if not os.environ.get("CYCLONEDDS_HOME"):
        print("ERROR: CYCLONEDDS_HOME is not set. See Lab 0 / scripts/setup_unitree_sdk.sh")
        return 1

    iface, code = prepare_go2_interface(args.interface)
    if code != 0:
        return code
    args.interface = iface

    print(f"Interface: {args.interface}")
    try:
        _init_dds(args.interface)
    except Exception as e:
        print(f"ERROR: ChannelFactoryInitialize failed: {e}\n")
        print(dds_failure_hint(args.interface))
        return 1

    sport_count = 0
    low_count = 0
    sport_done = False
    first_at: float | None = None
    last_print = 0.0
    min_interval = 1.0 / args.rate if args.rate > 0 else 0.0
    log_path: Path | None = Path(args.log) if args.log else None
    log_fp = None

    if log_path:
        log_fp = log_path.open("a", encoding="utf-8")
        print(f"Logging sportmodestate to {log_path}")

    topics = '"rt/sportmodestate" (SportModeState_, unitree_go)'
    if args.lowstate:
        topics += ' and "rt/lowstate" (LowState_, unitree_go)'
    print(f"Subscribing to {topics}...")

    def on_sport(msg: SportModeState_) -> None:
        nonlocal sport_count, first_at, last_print, sport_done
        if args.once and sport_done:
            return
        sport_count += 1
        now = time.time()
        if first_at is None:
            first_at = now
            last_print = now
            print("First rt/sportmodestate received:")
            print("  " + _format_sport(msg, sport_count))
            if log_fp:
                log_fp.write(json.dumps(_sport_record(msg, sport_count, now)) + "\n")
            if args.once:
                sport_done = True
                return
        if args.once:
            return
        if now - last_print >= min_interval:
            last_print = now
            print("  " + _format_sport(msg, sport_count))
            if log_fp:
                log_fp.write(json.dumps(_sport_record(msg, sport_count, now)) + "\n")

    def on_lowstate(msg: LowState_) -> None:
        nonlocal low_count
        low_count += 1
        if low_count == 1:
            print("First rt/lowstate received:")
            print(
                "  "
                + _format_lowstate(msg, low_count, inspect=args.inspect)
            )

    sport_sub = ChannelSubscriber("rt/sportmodestate", SportModeState_)
    sport_sub.Init(on_sport, 10)

    if args.lowstate:
        low_sub = ChannelSubscriber("rt/lowstate", LowState_)
        low_sub.Init(on_lowstate, 10)

    deadline = time.time() + 8.0
    while time.time() < deadline and sport_count == 0:
        time.sleep(0.05)

    if sport_count == 0:
        print("FAIL: no sportmodestate in 8s.\n")
        print(dds_failure_hint(args.interface))
        if log_fp:
            log_fp.close()
        return 1

    if args.once:
        if args.lowstate and low_count == 0:
            deadline = time.time() + 2.0
            while time.time() < deadline and low_count == 0:
                time.sleep(0.05)
        if log_fp:
            log_fp.close()
        low_note = f", lowstate={'OK' if low_count else 'none'}" if args.lowstate else ""
        print(f"Done. sportmodestate=1{low_note}")
        return 0

    end = time.time() + args.duration
    while time.time() < end:
        time.sleep(0.05)

    elapsed = time.time() - (first_at or time.time())
    hz = sport_count / elapsed if elapsed > 0 else 0.0
    print(
        f"Done. sportmodestate: {sport_count} messages in {elapsed:.1f}s (~{hz:.0f} Hz)"
    )
    if args.lowstate:
        print(f"      lowstate: {low_count} messages in {elapsed:.1f}s")
    if log_fp:
        log_fp.close()
        print(f"Log appended: {log_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
