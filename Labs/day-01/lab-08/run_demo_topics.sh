#!/usr/bin/env bash
# Lab 8 — run Lab 2 talker so rqt Graph / Topic Monitor have data.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
LAB02="${REPO_ROOT}/course/day-01/New-lab/lab-02"
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
echo "==> Publishing on /ros_basic_topic (Ctrl+C to stop)"
echo "    Open rqt in another terminal: Plugins → Graph or Topic Monitor"
exec "$ROS_PY" "${LAB02}/talker.py"
