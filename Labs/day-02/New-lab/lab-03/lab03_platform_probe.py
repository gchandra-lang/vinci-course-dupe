#!/usr/bin/env python3
"""
Lab 3b — Platform probe (read-only RPC + optional UT lidar DDS publish).

Exercises more of the Go2 Python SDK without sport motion:
  RobotStateClient.ServiceList
  VuiClient GetVolume / GetBrightness
  ChannelPublisher rt/utlidar/switch (optional ON/OFF)

Usage:
  python course/day-02/New-lab/lab-03/lab03_platform_probe.py en6
  python course/day-02/New-lab/lab-03/lab03_platform_probe.py en6 --lidar on
  python course/day-02/New-lab/lab-03/lab03_platform_probe.py en6 --json-out probe.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from unitree_sdk2py.core.channel import ChannelFactoryInitialize, ChannelPublisher
from unitree_sdk2py.go2.robot_state.robot_state_client import RobotStateClient
from unitree_sdk2py.go2.vui.vui_client import VuiClient
from unitree_sdk2py.idl.default import std_msgs_msg_dds__String_
from unitree_sdk2py.idl.std_msgs.msg.dds_ import String_


def _init_dds(iface: str) -> None:
    if os.environ.get("CYCLONEDDS_URI"):
        print("Warning: CYCLONEDDS_URI is set; unset it for interface-only init.")
        ChannelFactoryInitialize(0)
    else:
        ChannelFactoryInitialize(0, iface)


def _probe_robot_state() -> dict[str, Any]:
    client = RobotStateClient()
    client.SetTimeout(5.0)
    client.Init()
    code, services = client.ServiceList()
    rows: list[dict[str, Any]] = []
    if code == 0 and services:
        for s in services:
            rows.append(
                {
                    "name": s.name,
                    "status": s.status,
                    "protect": s.protect,
                }
            )
    return {"code": code, "services": rows}


def _probe_vui() -> dict[str, Any]:
    vui = VuiClient()
    vui.SetTimeout(3.0)
    vui.Init()
    vol_code, volume = vui.GetVolume()
    bri_code, brightness = vui.GetBrightness()
    sw_code, switch = vui.GetSwitch()
    return {
        "volume": {"code": vol_code, "value": volume},
        "brightness": {"code": bri_code, "value": brightness},
        "switch": {"code": sw_code, "value": switch},
    }


def _utlidar_switch(state: str) -> int:
    pub = ChannelPublisher("rt/utlidar/switch", String_)
    pub.Init()
    msg = std_msgs_msg_dds__String_()
    msg.data = state.upper()
    pub.Write(msg)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("interface", nargs="?", default=os.environ.get("GO2_INTERFACE", "enp0s31f6"))
    parser.add_argument(
        "--lidar",
        choices=("on", "off"),
        default=None,
        help="Publish rt/utlidar/switch ON or OFF (clear space; instructor)",
    )
    parser.add_argument("--json-out", type=Path, default=None, help="Save probe results as JSON")
    args = parser.parse_args()

    if not os.environ.get("CYCLONEDDS_HOME"):
        print("ERROR: CYCLONEDDS_HOME is not set.")
        return 1

    print(f"Interface: {args.interface}")
    _init_dds(args.interface)

    report: dict[str, Any] = {"interface": args.interface}

    print("\n[RobotStateClient] ServiceList()")
    rs = _probe_robot_state()
    report["robot_state"] = rs
    if rs["code"] != 0:
        print(f"  FAIL code={rs['code']}")
    else:
        for row in rs["services"]:
            print(
                f"  {row['name']!r}: status={row['status']} protect={row['protect']}"
            )

    print("\n[VuiClient] volume / brightness / switch")
    vui = _probe_vui()
    report["vui"] = vui
    print(f"  volume:     code={vui['volume']['code']} value={vui['volume']['value']}")
    print(f"  brightness: code={vui['brightness']['code']} value={vui['brightness']['value']}")
    print(f"  switch:     code={vui['switch']['code']} value={vui['switch']['value']}")

    if args.lidar:
        state = args.lidar.upper()
        print(f"\n[DDS publish] rt/utlidar/switch → {state!r}")
        _utlidar_switch(state)
        report["utlidar_switch"] = state
        print("  Published (confirm on robot / instructor demo)")

    if args.json_out:
        args.json_out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"\nSaved {args.json_out.resolve()}")

    ok = rs["code"] == 0 and vui["volume"]["code"] == 0
    print()
    print("Summary:", "PASS" if ok else "PARTIAL", "— platform probe complete")
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
