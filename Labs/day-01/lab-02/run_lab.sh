#!/usr/bin/env bash
# Lab 2 — run talker or listener (ROS 2 Humble only; no robot).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cmd="${1:-}"

if [[ ! -f /opt/ros/humble/setup.bash ]]; then
  echo "ROS 2 Humble not found. Run: $REPO_ROOT/scripts/install_ros2_humble.sh"
  exit 1
fi

set +u
# shellcheck source=/dev/null
source /opt/ros/humble/setup.bash
set -u

LAB_DIR="$(cd "$(dirname "$0")" && pwd)"

if [[ -x /usr/bin/python3.10 ]]; then
  ROS_PY=/usr/bin/python3.10
elif [[ -x /usr/bin/python3 ]]; then
  ROS_PY=/usr/bin/python3
else
  ROS_PY=python3
fi

case "$cmd" in
  talker) exec "$ROS_PY" "$LAB_DIR/talker.py" ;;
  listener) exec "$ROS_PY" "$LAB_DIR/listener.py" ;;
  *)
    echo "Usage: $0 {talker|listener}"
    echo "  Prerequisite: source /opt/ros/humble/setup.bash (done by this script)"
    exit 1
    ;;
esac
