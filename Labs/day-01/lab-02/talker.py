#!/usr/bin/env python3
"""Lab 2 — publish std_msgs/String on ros_basic_topic."""

from __future__ import annotations

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String


class Talker(Node):
    def __init__(self) -> None:
        super().__init__("ros_basic_talker")
        self._pub = self.create_publisher(String, "ros_basic_topic", 10)
        self._timer = self.create_timer(1.0, self._on_timer)
        self._count = 0

    def _on_timer(self) -> None:
        msg = String()
        msg.data = f"hello_from_unitree_camp {self._count}"
        self._pub.publish(msg)
        self.get_logger().info(f"Published: {msg.data}")
        self._count += 1


def main() -> None:
    rclpy.init()
    node = Talker()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        # ExternalShutdownException: normal when verify script uses `timeout` or SIGTERM
        pass
    if rclpy.ok():
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
