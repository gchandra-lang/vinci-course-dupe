#!/usr/bin/env python3
"""Lab 2 — subscribe to ros_basic_topic."""

from __future__ import annotations

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String


class Listener(Node):
    def __init__(self) -> None:
        super().__init__("ros_basic_listener")
        self._count = 0
        self.create_subscription(String, "ros_basic_topic", self._on_msg, 10)
        self.get_logger().info("Listening on ros_basic_topic ...")

    def _on_msg(self, msg: String) -> None:
        self._count += 1
        self.get_logger().info(f"[{self._count}] {msg.data}")


def main() -> None:
    rclpy.init()
    node = Listener()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    if rclpy.ok():
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
