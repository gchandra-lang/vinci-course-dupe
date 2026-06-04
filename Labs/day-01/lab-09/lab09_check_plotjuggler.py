#!/usr/bin/env python3
"""
Lab 9 — Verify PlotJuggler ROS 2 integration (no GUI required for PASS).

Usage (from repo root):
  python3 course/day-01/New-lab/lab-09/lab09_check_plotjuggler.py
  python3 course/day-01/New-lab/lab-09/lab09_check_plotjuggler.py --try-demo-topic
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
INSTALL_EXTRAS = SCRIPTS / "install_ros2_gui_extras.sh"
DEMO_PUB = _LAB / "plot_demo_publisher.py"


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
    return False


def check_plotjuggler_installed(ws) -> bool:
    proc = run_in_ros_env(ws, "ros2 pkg list 2>/dev/null | grep -i plotjuggler || true")
    lines = [ln.strip() for ln in (proc.stdout or "").splitlines() if ln.strip()]
    if lines:
        _ok(f"ROS packages: {', '.join(lines)}")
        return True

    proc_ex = run_in_ros_env(ws, "ros2 pkg executables plotjuggler 2>/dev/null || true")
    text = (proc_ex.stdout or "").strip()
    if "plotjuggler" in text:
        _ok(f"plotjuggler executables: {text.replace(chr(10), ', ')}")
        return True

    proc_run = run_in_ros_env(
        ws,
        "ros2 run plotjuggler plotjuggler --help 2>&1 | head -3",
        timeout_s=20.0,
    )
    combined = (proc_run.stdout or "") + (proc_run.stderr or "")
    if proc_run.returncode == 0 or "plotjuggler" in combined.lower():
        _ok("ros2 run plotjuggler plotjuggler available")
        return True

    _fail("plotjuggler ROS package not installed")
    print(f"        Run: {INSTALL_EXTRAS}")
    print("        or: sudo apt install -y ros-humble-plotjuggler-ros")
    return False


def check_demo_publisher(ws) -> bool:
    if not DEMO_PUB.is_file():
        _fail(f"missing {DEMO_PUB.name}")
        return False
    ros_py = resolve_ros_python()
    cmd = (
        "set +u; "
        f"{ros_py} {DEMO_PUB} & "
        "TPID=$!; sleep 2; "
        "ros2 topic echo /plot_demo/angle --once; "
        "RC=$?; kill $TPID 2>/dev/null; wait $TPID 2>/dev/null; "
        "set -u; exit $RC"
    )
    proc = run_in_ros_env(ws, cmd, timeout_s=25.0)
    if proc.returncode != 0:
        _warn("demo publisher or ros2 topic echo failed")
        if proc.stderr:
            print(proc.stderr[:400])
        return False
    if "data:" in proc.stdout:
        _ok("demo topic /plot_demo/angle publishes Float32 (ros2 topic echo --once)")
        return True
    _warn("echo succeeded but no data: line in output")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--try-demo-topic",
        action="store_true",
        help="Briefly run plot_demo_publisher and echo one message",
    )
    args = parser.parse_args()

    print("Lab 9 — PlotJuggler readiness\n")
    ws = resolve_unitree_ros2(prefer_built=False)

    ok = True
    ok &= check_humble()
    ok &= check_plotjuggler_installed(ws)

    if args.try_demo_topic:
        check_demo_publisher(ws)  # optional; WARN only

    print()
    if ok:
        print("RESULT: PASS — launch PlotJuggler (see README):")
        print("  ./course/day-01/New-lab/lab-09/run_demo_plot.sh      # terminal A")
        print("  ros2 run plotjuggler plotjuggler                      # terminal B")
        return 0
    print("RESULT: FAIL — install PlotJuggler first:")
    print(f"  {INSTALL_EXTRAS}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
