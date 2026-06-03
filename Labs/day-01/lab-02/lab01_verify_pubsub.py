#!/usr/bin/env python3
"""
Lab 2 — Automated check: talker publishes, listener receives (no robot).

Run from repo root after Lab 1 PASS:
  python3 course/day-01/New-lab/lab-02/lab01_verify_pubsub.py

Uses system Python 3.10 for rclpy (not conda python3).
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

_LAB_DIR = Path(__file__).resolve().parent
_NEW_LAB = _LAB_DIR.parent
if str(_NEW_LAB) not in sys.path:
    sys.path.insert(0, str(_NEW_LAB))

from ros_basic_helpers import resolve_ros_python  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify ROS-Basic pub/sub")
    parser.add_argument("--timeout", type=float, default=12.0, help="Seconds to wait for messages")
    args = parser.parse_args()

    lab_dir = _LAB_DIR
    listener_log = lab_dir / ".lab01_listener.log"
    ros_py = resolve_ros_python()

    if not Path("/opt/ros/humble/setup.bash").is_file():
        print("FAIL: ROS 2 Humble not installed")
        return 1

    listener_log.unlink(missing_ok=True)
    proc_l = subprocess.Popen(
        [
            "bash",
            "-lc",
            f"set +u; source /opt/ros/humble/setup.bash; set -u; "
            f"{ros_py} {lab_dir}/listener.py",
        ],
        stdout=listener_log.open("w"),
        stderr=subprocess.STDOUT,
    )
    time.sleep(1.5)
    proc_t = subprocess.Popen(
        [
            "bash",
            "-lc",
            f"set +u; source /opt/ros/humble/setup.bash; set -u; "
            f"timeout 5 {ros_py} {lab_dir}/talker.py",
        ],
    )
    proc_t.wait(timeout=10)
    deadline = time.time() + args.timeout
    heard = False
    while time.time() < deadline:
        if listener_log.exists():
            text = listener_log.read_text()
            if "hello_from_unitree_camp" in text:
                heard = True
                break
        time.sleep(0.3)

    proc_l.terminate()
    try:
        proc_l.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc_l.kill()

    if heard:
        print("PASS: listener received talker messages on ros_basic_topic")
        listener_log.unlink(missing_ok=True)
        return 0

    log_tail = listener_log.read_text()[:500] if listener_log.exists() else ""
    print("FAIL: no messages received. Run manually:")
    print(f"  Terminal A: {lab_dir}/run_lab.sh listener")
    print(f"  Terminal B: {lab_dir}/run_lab.sh talker")
    if "rclpy" in log_tail or "cpython-31" in log_tail:
        print(
            "\nHint: ROS 2 needs system Python 3.10, not conda. "
            f"This script uses {ros_py}. "
            "Deactivate conda (conda deactivate) before ROS labs, or use run_lab.sh."
        )
    if listener_log.exists():
        print("--- listener log ---")
        print(listener_log.read_text()[:800])
    return 1


if __name__ == "__main__":
    sys.exit(main())
