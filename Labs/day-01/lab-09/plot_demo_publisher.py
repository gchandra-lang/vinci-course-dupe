#!/usr/bin/env python3
"""Lab 9 — publish a simple Float32 sine for PlotJuggler exercises."""

from __future__ import annotations

import math

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class PlotDemo(Node):
    def __init__(self) -> None:
        super().__init__("plot_demo_publisher")
        self._pub = self.create_publisher(Float32, "plot_demo/angle", 10)
        self._t0 = self.get_clock().now()
        self._timer = self.create_timer(0.1, self._on_timer)

    def _on_timer(self) -> None:
        t = (self.get_clock().now() - self._t0).nanoseconds * 1e-9
        msg = Float32()
        msg.data = float(0.5 * math.sin(2.0 * math.pi * 0.5 * t))
        self._pub.publish(msg)


def main() -> None:
    rclpy.init()
    node = PlotDemo()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
