#!/usr/bin/env bash
# Lab 6 — launch RViz2 for Go2 (wraps repo scripts/run_rviz2.sh).
#
# Usage (from repo root):
#   chmod +x course/day-01/New-lab/lab-06/run_rviz.sh
#   ./course/day-01/New-lab/lab-06/run_rviz.sh
#   ./course/day-01/New-lab/lab-06/run_rviz.sh enx207bd22b611a
#   ./course/day-01/New-lab/lab-06/run_rviz.sh --ros-only
#
# Uses GO2_INTERFACE when set; otherwise pass your robot-LAN NIC (see ip -br addr).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
RUN_RVIZ="$REPO_ROOT/scripts/run_rviz2.sh"
NIC="${GO2_INTERFACE:-${UNITREE_ROS2_NIC:-}}"

usage() {
  cat <<EOF
Lab 6 — RViz2 launcher

Usage: $0 [interface] [--ros-only] [--config FILE] [-- RVIZ_ARGS...]

  interface     PC NIC wired to Go2 (not 192.168.123.161). Example: enx207bd22b611a
  --ros-only    Humble only — no robot DDS (empty RViz for UI practice)
  --config FILE Custom .rviz file (passed to rviz2 -d)

Environment:
  export GO2_INTERFACE=enx207bd22b611a   # optional default NIC

Default config (with robot): config/rviz/unitree_go2_lidar.rviz
  Fixed frame: odom · LiDAR: /utlidar/cloud_deskewed · odom: /utlidar/robot_odom

See README.md in this folder for click-by-click tasks.
EOF
}

if [[ ! -x "$RUN_RVIZ" ]]; then
  echo "error: missing $RUN_RVIZ" >&2
  exit 1
fi

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ -n "$NIC" && $# -eq 0 ]]; then
  echo "Lab 6 — using GO2_INTERFACE=${NIC}"
  exec "$RUN_RVIZ" "$NIC"
fi

if [[ $# -eq 0 ]]; then
  echo "Lab 6 — RViz2 (auto-detect NIC or pass interface name)"
  echo "  tip: export GO2_INTERFACE=\$(ip -br addr | awk '/192\\.168\\.123/{print \$1}')"
  echo "  tip: $0 --ros-only   # practice RViz UI without robot"
  exec "$RUN_RVIZ"
fi

exec "$RUN_RVIZ" "$@"
