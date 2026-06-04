# Gazebo Lab 2 — Small move forward

**TtT Day 2 · 13:30–15:00 (extension)**  
**Robot required:** No (simulation only)  
**Motion:** Sim — `/cmd_vel` forward

## Objectives

- Send a **short forward velocity** in Gazebo (scripted, no keyboard).
- Relate sim parameters to hardware **SportClient.Move** used in [`../../../lab-02/lab04_obstacle_avoid_intro.py`](../../../lab-02/lab04_obstacle_avoid_intro.py).

## Prerequisites

- [Lab 1](../lab-01/) complete — `./scripts/run_gazebo_go2.sh` running
- Same session: `source scripts/setup_gazebo_go2.sh`

## Sim vs hardware

| | Gazebo (this lab) | Physical Go2 ([`lab-02`](../../../lab-02/)) |
|--|-------------------|------------------------------------------|
| API | `geometry_msgs/Twist` → `/cmd_vel` | `SportClient.Move(vx, vy, vyaw)` |
| Typical forward | `--vx 0.25` | `--vx 0.3` (avoid intro) |
| Rate | `--hz 20` (default) | ~20 Hz in [`go2_motion_helpers`](../../../day-01/go2_motion_helpers.py) |

## Steps

1. Start sim (Lab 1) and wait until the robot is settled in the world.

2. **Unpause Gazebo** if needed (Gazebo window → **space**).

3. Run the forward move (~3 s default). The script **waits for CHAMP** to subscribe to `/cmd_vel` before moving:

```bash
source scripts/setup_gazebo_go2.sh
python3 course/day-02/New-lab/gazebo/lab-02/lab02_sim_move_forward.py --vx 0.25 --duration 3.0
```

4. Confirm the Go2 walks forward, then stops when the script finishes (zero velocity at end).

5. Dry-run (no ROS):

```bash
python3 course/day-02/New-lab/gazebo/lab-02/lab02_sim_move_forward.py --dry-run
```

## Options

| Flag | Default | Meaning |
|------|---------|---------|
| `--vx` | `0.25` | Forward speed (m/s), `linear.x` |
| `--duration` | `3.0` | Move time (seconds) |
| `--hz` | `20` | Publish rate |
| `--topic` | `/cmd_vel` | Twist topic (CHAMP listens here after launch remap) |
| `--wait` | `30` | Seconds to wait for a `/cmd_vel` subscriber |
| `--skip-wait` | off | Publish immediately (debug only) |
| `--dry-run` | off | Print plan only |

## Success criteria

- Visible forward displacement in Gazebo.
- No sustained spin after the script exits.

## Deliverable

One sentence, for example:

> Sim moved forward with vx=0.25 for 3 s via `/cmd_vel`; on hardware I will use SportClient / avoid client in day-02 lab-02.

## Troubleshooting

| Issue | Try |
|-------|-----|
| `FAIL: no subscriber on /cmd_vel` | Launch still running? Wait after spawn; unpause Gazebo (**space**); `ros2 topic info /cmd_vel -v` |
| Script runs but dog still still | Same as teleop: controllers / pause / try `--vx 0.35`; echo `/cmd_vel` during run |
| Dog drifts/spins after stop | Re-run script (sends zero twist); reset Gazebo (Ctrl+C launch, relaunch) |
| `rclpy` import error | `source scripts/setup_gazebo_go2.sh` |
| `python` not found | Use **`python3`** (see commands above) |

**Back:** [Extension index](../README.md) · **Hardware next:** [`../../../lab-04/`](../../../lab-04/) field patrol
