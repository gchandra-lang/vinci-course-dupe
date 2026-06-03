#!/usr/bin/env bash
# Lab 9 — Float32 sine on /plot_demo/angle for PlotJuggler.
set -euo pipefail
LAB_DIR="$(cd "$(dirname "$0")" && pwd)"
set +u
source /opt/ros/humble/setup.bash
set -u
if [[ -x /usr/bin/python3.10 ]]; then
  ROS_PY=/usr/bin/python3.10
elif [[ -x /usr/bin/python3 ]]; then
  ROS_PY=/usr/bin/python3
else
  ROS_PY=python3
fi
echo "==> Publishing /plot_demo/angle (std_msgs/Float32, ~0.5 Hz sine)"
echo "    PlotJuggler: Streaming → ROS2 Topic Subscriber → /plot_demo/angle → drag 'data'"
exec "$ROS_PY" "${LAB_DIR}/plot_demo_publisher.py"
