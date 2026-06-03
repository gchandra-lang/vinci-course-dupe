#!/usr/bin/env python3
"""
Lab 2 — Short forward move in Go2 Gazebo (CHAMP /cmd_vel).

Mirrors the *intent* of hardware SportClient.Move (see go2_motion_helpers.periodic_sport_move)
and day-02 lab02_obstacle_avoid_intro (--vx / --move-sec).

Usage (Gazebo must be running, unpause with space if needed):
  source scripts/setup_gazebo_go2.sh
  python3 course/student/day-02/gazebo/lab-02/lab02_sim_move_forward.py
  python3 course/student/day-02/gazebo/lab-02/lab02_sim_move_forward.py --vx 0.25 --duration 3.0
  python3 course/student/day-02/gazebo/lab-02/lab02_sim_move_forward.py --dry-run
"""

from __future__ import annotations

import argparse
import sys
import time


def _normalize_topic(topic: str) -> str:
    topic = topic.strip()
    if not topic:
        return "/cmd_vel"
    return topic if topic.startswith("/") else f"/{topic}"


def _wait_for_subscribers(
    node: object,
    pub: object,
    *,
    timeout_s: float,
    spin,
) -> int:
    """Return subscriber count once > 0, or final count after timeout."""
    deadline = time.time() + timeout_s
    count = 0
    while time.time() < deadline:
        spin(node, timeout_sec=0.2)
        count = int(pub.get_subscription_count())
        if count > 0:
            return count
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish /cmd_vel forward then stop")
    parser.add_argument("--vx", type=float, default=0.25, help="Forward m/s (linear.x)")
    parser.add_argument("--vy", type=float, default=0.0, help="Lateral m/s (linear.y)")
    parser.add_argument("--vyaw", type=float, default=0.0, help="Yaw rad/s (angular.z)")
    parser.add_argument("--duration", type=float, default=3.0, help="Move duration (seconds)")
    parser.add_argument("--hz", type=float, default=20.0, help="Publish rate")
    parser.add_argument(
        "--topic",
        default="/cmd_vel",
        help="Twist topic (default /cmd_vel — CHAMP quadruped_controller listens here)",
    )
    parser.add_argument(
        "--wait",
        type=float,
        default=30.0,
        metavar="SEC",
        help="Seconds to wait for a /cmd_vel subscriber before moving (default: 30)",
    )
    parser.add_argument(
        "--skip-wait",
        action="store_true",
        help="Publish immediately (no wait for CHAMP controller)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print plan only",
    )
    args = parser.parse_args()
    topic = _normalize_topic(args.topic)

    if args.duration <= 0:
        print("error: --duration must be positive")
        return 1
    if args.hz <= 0:
        print("error: --hz must be positive")
        return 1

    if args.dry_run:
        print(
            f"[dry-run] Would publish Twist on {topic}: "
            f"vx={args.vx} vy={args.vy} vyaw={args.vyaw} for {args.duration}s @ {args.hz} Hz, then zero."
        )
        if not args.skip_wait:
            print(f"[dry-run] Would wait up to {args.wait}s for a subscriber on {topic}.")
        return 0

    try:
        import rclpy
        from geometry_msgs.msg import Twist
        from rclpy.node import Node
    except ImportError as exc:
        print(f"error: rclpy not available ({exc}). Source setup_gazebo_go2.sh first.")
        return 1

    class _Publisher(Node):
        def __init__(self, twist_topic: str) -> None:
            super().__init__("lab02_sim_move_forward")
            self._pub = self.create_publisher(Twist, twist_topic, 10)
            self._topic = twist_topic

        def publish_twist(self, vx: float, vy: float, vyaw: float) -> None:
            msg = Twist()
            msg.linear.x = float(vx)
            msg.linear.y = float(vy)
            msg.angular.z = float(vyaw)
            self._pub.publish(msg)

    rclpy.init()
    node = _Publisher(topic)
    interval = 1.0 / args.hz

    print(f"[lab02] Publishing geometry_msgs/Twist on {topic}")
    print("        Prerequisite: ./scripts/run_gazebo_go2.sh running, Gazebo unpaused (space).")

    if not args.skip_wait:
        print(f"[wait] Up to {args.wait:.0f}s for CHAMP to subscribe to {topic}...")
        subs = _wait_for_subscribers(
            node,
            node._pub,
            timeout_s=args.wait,
            spin=rclpy.spin_once,
        )
        if subs == 0:
            print(
                f"FAIL: no subscriber on {topic} after {args.wait:.0f}s.\n"
                "  - Is ./scripts/run_gazebo_go2.sh still running?\n"
                "  - Wait ~20s after spawn; check launch terminal for controller errors.\n"
                "  - In another terminal: ros2 topic info /cmd_vel -v\n"
                "  - Gazebo paused? Click Gazebo window → press space.\n"
                "  - Retry with --skip-wait only for debugging (motion likely still fails)."
            )
            node.destroy_node()
            rclpy.shutdown()
            return 1
        print(f"[wait] OK — {subs} subscriber(s) on {topic}.")

    print(
        f"[move] vx={args.vx} vy={args.vy} vyaw={args.vyaw} "
        f"for {args.duration}s @ ~{args.hz:.0f} Hz"
    )
    print("       Watch Gazebo — dog should walk forward, then stop.")

    n = 0
    end = time.time() + args.duration
    try:
        while time.time() < end:
            node.publish_twist(args.vx, args.vy, args.vyaw)
            rclpy.spin_once(node, timeout_sec=0.0)
            n += 1
            time.sleep(interval)

        print(f"[stop] Publishing zero velocity ({n} move commands sent)")
        for _ in range(max(3, int(args.hz))):
            node.publish_twist(0.0, 0.0, 0.0)
            rclpy.spin_once(node, timeout_sec=0.0)
            time.sleep(interval)
    finally:
        node.destroy_node()
        rclpy.shutdown()

    print(
        "\nLab 2 done. Deliverable: one sentence comparing sim vx/duration to "
        "SportClient.Move on hardware (day-02 lab-02)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
