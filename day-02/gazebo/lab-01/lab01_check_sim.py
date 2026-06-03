#!/usr/bin/env python3
"""
Lab 1 — Verify Go2 Gazebo sandbox is running (topics publishing).

Run in a second terminal while ./scripts/run_gazebo_go2.sh is active:
  source scripts/setup_gazebo_go2.sh
  python3 course/student/day-02/gazebo/lab-01/lab01_check_sim.py

Exit 0 if required topics exist and /joint_states publishes at least once.
"""

from __future__ import annotations

import argparse
import sys
import time

REQUIRED_TOPICS = ("/joint_states", "/odom")
OPTIONAL_TOPICS = ("/cmd_vel",)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Go2 Gazebo ROS graph")
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Seconds to wait for topics (default: 30)",
    )
    parser.add_argument(
        "--skip-joint-sample",
        action="store_true",
        help="Only check topic names, not a JointState message",
    )
    args = parser.parse_args()

    try:
        import rclpy
        from rclpy.node import Node
        from sensor_msgs.msg import JointState
    except ImportError as exc:
        print(f"error: rclpy not available ({exc}). Source ROS 2 Humble first.")
        return 1

    class _Checker(Node):
        def __init__(self) -> None:
            super().__init__("lab01_check_sim")
            self.joint_got = False
            self.create_subscription(JointState, "/joint_states", self._on_joint, 10)

        def _on_joint(self, _msg: JointState) -> None:
            self.joint_got = True

    print("Checking ROS 2 topics (is run_gazebo_go2.sh running?)...")
    rclpy.init()
    node = _Checker()
    names: list[str] = []
    deadline = time.time() + args.timeout

    joint_got = False
    try:
        while time.time() < deadline:
            rclpy.spin_once(node, timeout_sec=0.2)
            names = sorted({n for n, _ in node.get_topic_names_and_types()})
            joint_got = node.joint_got
            if all(t in names for t in REQUIRED_TOPICS):
                if args.skip_joint_sample or joint_got:
                    break
    finally:
        node.destroy_node()
        rclpy.shutdown()

    if not names:
        print("FAIL: could not list topics. Source setup_gazebo_go2.sh and start Gazebo.")
        return 1

    missing = [t for t in REQUIRED_TOPICS if t not in names]
    if missing:
        print(f"FAIL: missing topics: {missing}")
        print("Available topics:")
        for n in names:
            print(f"  {n}")
        return 1

    print("OK: required topics present:", ", ".join(REQUIRED_TOPICS))
    for t in OPTIONAL_TOPICS:
        if t in names:
            print(f"  also found {t}")

    if not args.skip_joint_sample and not joint_got:
        print("FAIL: /joint_states did not publish in time.")
        return 1
    if not args.skip_joint_sample:
        print("OK: /joint_states publishing.")

    print("\nLab 1 sim check passed. Deliverable: note + ros2 topic list (or screenshot).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
