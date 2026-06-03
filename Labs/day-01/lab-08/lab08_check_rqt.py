#!/usr/bin/env python3
"""
Lab 8 — Verify rqt is installed and usable (no GUI required for PASS).

Usage (from repo root):
  python3 course/day-01/New-lab/lab-08/lab08_check_rqt.py
  python3 course/day-01/New-lab/lab-08/lab08_check_rqt.py --try-graph-hz
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_LAB = Path(__file__).resolve().parent
_NEW_LAB = _LAB.parent
if str(_NEW_LAB) not in sys.path:
    sys.path.insert(0, str(_NEW_LAB))

from ros_basic_helpers import (  # noqa: E402
    REPO_ROOT,
    humble_available,
    resolve_ros_python,
    resolve_unitree_ros2,
    run_in_ros_env,
)

SCRIPTS = REPO_ROOT / "scripts"
INSTALL_HUMBLE = SCRIPTS / "install_ros2_humble.sh"
INSTALL_EXTRAS = SCRIPTS / "install_ros2_gui_extras.sh"


def _ok(msg: str) -> None:
    print(f"  PASS  {msg}")


def _fail(msg: str) -> None:
    print(f"  FAIL  {msg}")


def _warn(msg: str) -> None:
    print(f"  WARN  {msg}")


def check_humble() -> bool:
    if humble_available():
        _ok("ROS 2 Humble at /opt/ros/humble")
        return True
    _fail("ROS 2 Humble not found")
    print(f"        Run: {INSTALL_HUMBLE}")
    return False


def check_rqt_binary(ws) -> bool:
    proc = run_in_ros_env(ws, "command -v rqt")
    if proc.returncode != 0 or not proc.stdout.strip():
        _fail("rqt not in PATH after sourcing Humble")
        print(f"        Reinstall desktop: {INSTALL_HUMBLE}")
        return False
    _ok(f"rqt binary: {proc.stdout.strip()}")
    return True


def check_rqt_packages(ws) -> bool:
    proc = run_in_ros_env(
        ws,
        "ros2 pkg list | grep -E '^rqt(_|$)' | head -20",
        timeout_s=30.0,
    )
    if proc.returncode != 0:
        _fail("ros2 pkg list failed")
        if proc.stderr:
            print(proc.stderr[:400])
        return False
    pkgs = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
    if not pkgs:
        _fail("no rqt_* ROS packages found")
        print(f"        Run: {INSTALL_HUMBLE}")
        return False
    _ok(f"rqt ROS packages ({len(pkgs)}): {', '.join(pkgs[:5])}{'…' if len(pkgs) > 5 else ''}")
    return True


def check_demo_talker_topic(ws) -> bool:
    """Optional: talker publishes; ros2 topic info works (no rqt GUI)."""
    lab02 = _NEW_LAB / "lab-02"
    talker = lab02 / "talker.py"
    if not talker.is_file():
        _warn("Lab 2 talker.py missing — skip live topic check")
        return True

    ros_py = resolve_ros_python()
    cmd = (
        "set +u; "
        f"{ros_py} {talker} & "
        "TPID=$!; sleep 2; "
        "ros2 topic info /ros_basic_topic; "
        "RC=$?; kill $TPID 2>/dev/null; wait $TPID 2>/dev/null; "
        "set -u; exit $RC"
    )
    proc = run_in_ros_env(ws, cmd, timeout_s=25.0)
    if proc.returncode != 0:
        _warn("ros2 topic info /ros_basic_topic failed (demo talker)")
        if proc.stderr:
            print(proc.stderr[:400])
        return False
    if "ros_basic_talker" in proc.stdout or "Publisher count" in proc.stdout:
        _ok("demo talker visible on /ros_basic_topic (ros2 topic info)")
        return True
    _warn("topic info returned but talker not obvious in output")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--try-graph-hz",
        action="store_true",
        help="Start Lab 2 talker briefly and run ros2 topic info",
    )
    args = parser.parse_args()

    print("Lab 8 — rqt readiness\n")
    ws = resolve_unitree_ros2(prefer_built=False)

    ok = True
    ok &= check_humble()
    ok &= check_rqt_binary(ws)
    ok &= check_rqt_packages(ws)

    if args.try_graph_hz:
        check_demo_talker_topic(ws)

    print()
    if ok:
        print("RESULT: PASS — open rqt (see README):")
        print("  source /opt/ros/humble/setup.bash")
        print("  ./course/day-01/New-lab/lab-08/run_demo_topics.sh   # terminal A")
        print("  rqt                                                # terminal B")
        return 0
    print("RESULT: FAIL — fix items above.")
    print(f"  PlotJuggler extras (not required for rqt): {INSTALL_EXTRAS}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
