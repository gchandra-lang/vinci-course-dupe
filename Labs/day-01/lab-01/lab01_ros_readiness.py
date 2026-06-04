#!/usr/bin/env python3
"""
Lab 0 — ROS 2 Humble + unitree_ros2 readiness (machine only; robot optional).

Checks standard install and both common unitree_ros2 locations:
  - <repo>/unitree_ros2
  - ~/unitree_ros2
  - UNITREE_ROS2 environment override

Usage (from repo root):
  python3 course/day-01/New-lab/lab-01/lab01_ros_readiness.py
  python3 course/day-01/New-lab/lab-01/lab01_ros_readiness.py --try-demo
  python3 course/day-01/New-lab/lab-01/lab01_ros_readiness.py enp0s31f6
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

_LAB00 = Path(__file__).resolve().parent
_ROS_BASIC = _LAB00.parent
if str(_ROS_BASIC) not in sys.path:
    sys.path.insert(0, str(_ROS_BASIC))

from ros_basic_helpers import (  # noqa: E402
    REPO_ROOT,
    humble_available,
    missing_unitree_packages,
    resolve_unitree_ros2,
    unitree_ros2_candidates,
)

SCRIPTS = REPO_ROOT / "scripts"
DOCS_ROS = REPO_ROOT / "docs" / "ROS2-INSTALL.md"


def _ok(msg: str) -> None:
    print(f"  PASS  {msg}")


def _fail(msg: str) -> None:
    print(f"  FAIL  {msg}")


def _warn(msg: str) -> None:
    print(f"  WARN  {msg}")


def _print_howto() -> None:
    print("\n==> How to install (first time)")
    print(f"    Guide: {DOCS_ROS}")
    print("    1) ROS 2 Humble (sudo):")
    print(f"       {SCRIPTS}/install_ros2_humble.sh")
    print("    2) unitree_ros2 workspace (pick one location):")
    print(f"       {SCRIPTS}/build_unitree_ros2.sh")
    print("       # default clone/build: ~/unitree_ros2")
    print("       # OR clone into repo:")
    print(f"       git clone https://github.com/unitreerobotics/unitree_ros2.git {REPO_ROOT}/unitree_ros2")
    print(f"       UNITREE_ROS2={REPO_ROOT}/unitree_ros2 {SCRIPTS}/build_unitree_ros2.sh")
    print("    3) Each new terminal (robot Ethernet NIC):")
    print(f"       source {SCRIPTS}/setup_unitree_ros2.sh enp0s31f6")
    print("    Keep Python SDK (conda) in a separate terminal from ROS 2 + Unitree DDS.\n")


def check_humble() -> bool:
    if humble_available():
        _ok("ROS 2 Humble at /opt/ros/humble")
        return True
    _fail("ROS 2 Humble not found")
    print(f"        Run: {SCRIPTS}/install_ros2_humble.sh")
    return False


def check_candidates() -> tuple[bool, Path | None]:
    print("\n==> unitree_ros2 locations")
    any_exists = False
    any_built = False
    for c in unitree_ros2_candidates():
        status = "built" if c.built else ("present, not built" if c.exists else "missing")
        print(f"    [{c.label}] {c.path} — {status}")
        any_exists = any_exists or c.exists
        any_built = any_built or c.built

    resolved = resolve_unitree_ros2(prefer_built=True)
    if resolved and (resolved / "cyclonedds_ws/install/setup.bash").is_file():
        _ok(f"Using built workspace: {resolved}")
        print(f"        export UNITREE_ROS2={resolved}")
        return True, resolved

    if any_exists and not any_built:
        _fail("unitree_ros2 directory found but not built (no cyclonedds_ws/install/setup.bash)")
        print(f"        UNITREE_ROS2=<path> {SCRIPTS}/build_unitree_ros2.sh")
        return False, resolve_unitree_ros2(prefer_built=False)

    _fail("No unitree_ros2 workspace found")
    print(f"        {SCRIPTS}/build_unitree_ros2.sh")
    print(f"        or clone into {REPO_ROOT}/unitree_ros2")
    return False, None


def check_unitree_packages(ws: Path | None) -> bool:
    if ws is None:
        return False
    missing = missing_unitree_packages(ws)
    if not missing:
        _ok("unitree_ros2 packages: unitree_api, unitree_go, unitree_ros2_example")
        return True
    _fail(f"Missing ROS packages after sourcing workspace: {', '.join(missing)}")
    print(f"        Rebuild: UNITREE_ROS2={ws} {SCRIPTS}/build_unitree_ros2.sh")
    return False


def check_setup_script(iface: str | None) -> bool:
    setup = SCRIPTS / "setup_unitree_ros2.sh"
    if not setup.is_file():
        _fail(f"Missing {setup}")
        return False
    _ok(f"setup script present: {setup}")
    if iface:
        print(f"        source {setup} {iface}")
    else:
        print(f"        source {setup} <ethernet_iface>")
    return True


def try_demo_talker() -> bool:
    ws = resolve_unitree_ros2(prefer_built=True)
    if not humble_available():
        return False
    from ros_basic_helpers import run_in_ros_env

    _warn("Running ros2 run demo_nodes_cpp talker (3s) — Ctrl+C not needed, will timeout")
    proc = run_in_ros_env(
        ws,
        "timeout 3 ros2 run demo_nodes_cpp talker || test $? -eq 124",
        timeout_s=15.0,
    )
    if proc.returncode == 0:
        _ok("demo_nodes_cpp talker ran (ROS graph OK)")
        return True
    _fail("demo_nodes_cpp talker failed")
    if proc.stderr:
        print(proc.stderr[:500])
    return False


def try_robot_topics(iface: str, ws: Path | None) -> bool:
    from ros_basic_helpers import run_in_ros_env

    if not humble_available() or ws is None:
        return False
    nic = iface
    cmd = (
        f'export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp; '
        f'export CYCLONEDDS_URI=\'<CycloneDDS><Domain><General><Interfaces>'
        f'<NetworkInterface name="{nic}" priority="default" multicast="default" />'
        f"</Interfaces></General></Domain></CycloneDDS>'; "
        "timeout 5 ros2 topic list"
    )
    proc = run_in_ros_env(ws, cmd, timeout_s=20.0)
    if proc.returncode != 0:
        _warn(f"ros2 topic list on {nic} failed (robot off or wrong NIC?)")
        if proc.stderr:
            print(proc.stderr[:400])
        return False
    topics = proc.stdout.strip().splitlines()
    if any("sportmodestate" in t for t in topics):
        _ok(f"Robot topics visible on {nic} (e.g. sportmodestate)")
        return True
    _warn(f"No sportmodestate in topic list on {nic} ({len(topics)} topics)")
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "interface",
        nargs="?",
        default=os.environ.get("UNITREE_ROS2_NIC", ""),
        help="Optional Ethernet NIC for robot topic check (e.g. enp0s31f6)",
    )
    parser.add_argument(
        "--try-demo",
        action="store_true",
        help="Run demo_nodes_cpp talker for 3 seconds",
    )
    parser.add_argument(
        "--robot-topics",
        action="store_true",
        help="With interface arg, try ros2 topic list on robot LAN",
    )
    args = parser.parse_args()

    print("Lab 0 — ROS 2 + unitree_ros2 readiness\n")
    _print_howto()

    ok = True
    ok &= check_humble()
    built_ok, ws = check_candidates()
    ok &= built_ok
    if ws:
        ok &= check_unitree_packages(ws)
    ok &= check_setup_script(args.interface or None)

    if args.try_demo:
        ok &= try_demo_talker()

    if args.robot_topics and args.interface:
        try_robot_topics(args.interface, ws)
    elif args.interface:
        print(f"\n  Tip: add --robot-topics to probe Go2 on {args.interface}")

    print()
    if ok:
        print("RESULT: PASS — proceed to Lab 2 (ROS pub/sub).")
        return 0
    print("RESULT: FAIL — fix items above, then re-run this script.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
