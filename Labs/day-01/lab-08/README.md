# Lab 8 — rqt (ROS 2 GUI toolbox)

**TtT Day 1 · ROS visualization**  
**Robot required:** No for the checker; optional with NIC for live Unitree topics  
**Motion:** None

## Objectives

- Open **rqt** and use plugins to inspect the ROS 2 graph.
- Relate **nodes**, **topics**, and **message types** to [Lab 2](../lab-02/) talker/listener.
- Optional: view robot topics after `source scripts/setup_unitree_ros2.sh <nic>`.

## Prerequisites

- [Lab 1](../lab-01/) **PASS** (ROS 2 Humble + `unitree_ros2` readiness).
- [Lab 2](../lab-02/) pub/sub completed or demo script below.
- **Display:** `echo $DISPLAY` set (native desktop or WSLg).

`rqt` is included with `ros-humble-desktop` from [`install_ros2_humble.sh`](../../../scripts/install_ros2_humble.sh). No extra apt step.

## Steps

### A — Automated check (no GUI window required)

```bash
cd /path/to/vinci-unitree
python3 course/day-01/New-lab/lab-08/lab08_check_rqt.py
```

### B — Demo graph (talker running)

**Terminal A** — sample publisher:

```bash
# Do NOT use sudo with source (see Troubleshooting)
source /opt/ros/humble/setup.bash
chmod +x course/day-01/New-lab/lab-08/run_demo_topics.sh   # once
./course/day-01/New-lab/lab-08/run_demo_topics.sh
# or without +x:
bash course/day-01/New-lab/lab-08/run_demo_topics.sh
```

**Terminal B** — rqt:

```bash
source /opt/ros/humble/setup.bash
rqt
```

In rqt: **Plugins → Visualization → Graph** (or **Plugins → Topics → Topic Monitor**).

Confirm you see:

| Item | Expected |
|------|----------|
| Node | `/ros_basic_talker` |
| Topic | `/ros_basic_topic` |
| Type | `std_msgs/msg/String` |

Other useful plugins:

| Plugin | Use |
|--------|-----|
| **Graph** | Node/topic topology |
| **Topic Monitor** | Hz and publishers |
| **Console** | Log level (when nodes use `rclpy` logging) |

Stop the demo with **Ctrl+C** in Terminal A.

### C — Optional: Unitree robot LAN

```bash
source /path/to/vinci-unitree/scripts/setup_unitree_ros2.sh enp0s31f6
rqt
```

Use **Topic Monitor** or **Graph** to find topics containing `sportmodestate` or `lowstate` (exact names depend on firmware).

## Troubleshooting

| Error | Why | Fix |
|-------|-----|-----|
| `sudo: source: command not found` | `source` is a **bash builtin**, not a program. `sudo` only runs external commands. | Run `source /opt/ros/humble/setup.bash` **without** `sudo`. ROS install does not need root in your user shell. |
| `Permission denied` on `run_demo_topics.sh` | The file was not marked executable (`chmod +x`). | `chmod +x course/day-01/New-lab/lab-08/run_demo_topics.sh` or run `bash course/day-01/New-lab/lab-08/run_demo_topics.sh` |
| `rclpy` / wrong Python with conda active | Conda’s `python3` is not ROS Humble’s 3.10. | For ROS labs use a terminal **without** `conda activate`, or let `run_demo_topics.sh` use `/usr/bin/python3.10` (as Lab 2 does). |

## Files

| File | Purpose |
|------|---------|
| `lab08_check_rqt.py` | Verifies `rqt` CLI and ROS packages (no window) |
| `run_demo_topics.sh` | Starts Lab 2 talker for graph exercises |
| `README.md` | This guide |

## Deliverable

- Log: `lab08_check_rqt.py` → **RESULT: PASS**
- Screenshot: rqt **Graph** with `/ros_basic_talker` and `/ros_basic_topic`

**Next:** [Lab 9 — PlotJuggler](../lab-09/)
