# Gazebo Lab 1 — Turn simulation on (Go2 sandbox)

**TtT Day 2 · 13:30–15:00 (extension)**  
**Robot required:** No  
**Motion:** None

## Objectives

- Install and launch **Gazebo Classic** with a **Unitree Go2** model (CHAMP).
- Confirm the ROS 2 graph is alive before afternoon field work on hardware.
- Understand **sim (`/cmd_vel`)** vs **hardware (`SportClient`)** — see [`docs/GAZEBO-GO2.md`](../../../../docs/GAZEBO-GO2.md).

## Prerequisites

- Ubuntu 22.04, ROS 2 Humble — [`docs/ROS2-INSTALL.md`](../../../../docs/ROS2-INSTALL.md)
- Display available: `echo $DISPLAY`
- One-time: `./scripts/install_gazebo_go2.sh` from repo root

## Steps

1. **Terminal A** — start sim:

```bash
cd /path/to/vinci-unitree
source scripts/setup_gazebo_go2.sh
./scripts/run_gazebo_go2.sh
```

Wait until the Go2 model is visible and the launch terminal shows no errors (~10–20 s).

2. **Terminal B** — verify:

```bash
source scripts/setup_gazebo_go2.sh
ros2 topic list
python3 course/day-02/New-lab/gazebo/lab-01/lab01_check_sim.py
```

3. *(Optional)* keyboard teleop — see [Optional teleop](#optional-keyboard-teleop-instructor-demo) below. **Not required** for the Lab 1 deliverable.

## Success criteria

- Gazebo window stays open ≥ 60 s without crash.
- Go2 quadruped visible in the world.
- `lab01_check_sim.py` exits **0** (topics `/joint_states`, `/odom` present).

## Deliverable

Short note plus `ros2 topic list` output (or screenshot) showing sim is running.

**Next:** [Lab 2 — forward move](../lab-02/)

## Optional: keyboard teleop (instructor demo)

### Is it normal that teleop “does nothing”?

**Yes, very common.** The program starts and prints key help, but the Go2 stays still unless several conditions are met. That does **not** mean Gazebo failed — Lab 1 success is only: sim running + `lab01_check_sim.py` passes.

Motion in sim is taught properly in [Lab 2](../lab-02/) (`lab02_sim_move_forward.py`).

### How CHAMP expects commands

```text
Terminal B: teleop_twist_keyboard  --publishes-->  /cmd_vel  --subscribed by-->  quadruped_controller (CHAMP)
                                                                                              |
                                                                                              v
                                                                                    Gazebo leg controllers
```

This is **not** the physical Go2 SDK. No `SportClient`, no Ethernet.

### Before you press keys

1. **Terminal A** still running `./scripts/run_gazebo_go2.sh` (no errors).
2. **Terminal B** ran `source scripts/setup_gazebo_go2.sh` (same as step 2).
3. Wait **~20 s** after spawn so `joint_states` / controllers are up.
4. Gazebo is **not paused** — click the Gazebo window once, press **space** (unpause) if sim time is frozen.
5. Click the **teleop terminal** so it has keyboard focus (keys do **not** go to the Gazebo window).

### Run teleop

```bash
source scripts/setup_gazebo_go2.sh
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Use **`i` / `j` / `l` / `k`** (and `u` / `o` / `m` / `,`) — **not arrow keys**. Layout is US QWERTY (see the node’s printed help). Hold **`i`** for forward.

### Verify commands are actually published

**Terminal C** (while teleop is running):

```bash
source scripts/setup_gazebo_go2.sh
ros2 topic echo /cmd_vel
```

Hold **`i`** in the teleop terminal. You should see `linear.x` change (e.g. ~0.5). If echo stays empty → focus/wrong terminal or teleop not running.

Check something is listening:

```bash
ros2 topic info /cmd_vel -v
```

Expect at least one **subscription** (CHAMP `quadruped_controller_node`).

### If `/cmd_vel` updates but the dog still does not walk

| Check | Action |
|-------|--------|
| Sim paused | Gazebo window → **space** to unpause |
| Controllers | Launch terminal should show `joint_group_effort_controller` / CHAMP without errors |
| Too soon | Wait longer after spawn, try again |
| Speed | Press **`q`** a few times in teleop to raise max speed |

### CHAMP-native teleop (alternative)

Upstream CHAMP ships a matching teleop node (after `install_gazebo_go2.sh`):

```bash
source scripts/setup_gazebo_go2.sh
ros2 launch champ_teleop teleop.launch.py use_sim_time:=true
```

Opens a separate xterm; same **`i` / `j` / `k` / `l`** keys, publishes to `/cmd_vel`.

### Recommended teaching flow

| Lab | Motion proof |
|-----|----------------|
| **Lab 1** | Gazebo on + topics OK — **no teleop required** |
| **Lab 2** | Scripted forward move — reliable for all students |

## Troubleshooting

See [`docs/GAZEBO-GO2.md`](../../../../docs/GAZEBO-GO2.md). If Gazebo cannot run on your machine, use the fallback in [`../README.md`](../README.md).
