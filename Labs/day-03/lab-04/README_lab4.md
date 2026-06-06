# Lab 4 — B2 trajectory following (autonomous path with turns)

**Duration:** ~30–45 min
**Robot motion:** Yes — high-level autonomous path execution; instructor supervision required
**Prerequisites:** `unitree_sdk2py` installed, familiarity with `SportClient`, `PathPoint`, and trajectory commands, robot powered and on the same network

---

## Learning objectives

1. Understand how to execute a pre-defined autonomous trajectory using `SportClient` and `TrajectoryFollow`.
2. Learn how to read robot state from `rt/sportmodestate` and verify mode/gait information.
3. Practice safe transition between standing, classic walk mode, and return-to-menu behavior.

---

## 1. Concepts

This lab runs a high-level trajectory sequence using the B2 sport mode API:

- High-level command stream: `TrajectoryFollow` with a padded list of `PathPoint` objects.
- State monitoring: subscribe once to `rt/sportmodestate` to print robot mode, gait, position, velocity, yaw speed, and body height.
- Motion flow: stand up, enable classic walk, execute a sequence of forward, turn, sideways, and turn-back movements, then disable classic walk.

Key parameters in the script:

- `PathPoint(timeFromStart, x, y, yaw, vx, vy, vyaw)` for each waypoint.
- Trajectory length requirement: exactly 30 points in the SDK, padded by repeating the final point.
- Safety flow: explicit prompt before starting, and a menu for discrete actions.

Why this lab matters

Trajectory following demonstrates how to command complex path motion at a high level, while still needing careful supervision and space around the robot.

---

## 2. Safety (required)

- This script WILL move the robot forward, turn, and move sideways. Clear a large area around the robot.
- Instructor must supervise at all times.
- Keep hands away from legs and any moving parts.
- Ensure the robot is on a stable surface and the power/safety switches are correctly set before starting.
- Be prepared to stop the program (Ctrl+C) if the robot behaves unexpectedly.

---

## 3. Hands-on

### Step 0 — Prepare environment

```bash
conda activate unitree_env
cd /path/to/vinci-unitree
```

### Step 1 — Run the trajectory script

```bash
python course/student/B2-day1/lab-04/lab04_b2_trajectory.py <networkInterface>
```

Example:

```bash
python course/student/B2-day1/lab-04/lab04_b2_trajectory.py eth0
```

### Step 2 — Use the menu

- Choose `0` to display sport mode state once.
- Choose `1` to run the predefined trajectory (forward, turn, sideways, turn back).
- Choose `2` to exit.

The trajectory will:

1. Call `RecoveryStand()` to stand the robot up.
2. Enable `ClassicWalk(True)`.
3. Send a 30-point trajectory containing forward move, yaw turn, sideways move, and return turn.
4. Wait about 23 seconds while the trajectory executes.
5. Disable `ClassicWalk(False)` and return to menu.

---

## 4. Exercises

### Exercise A — Inspect the trajectory

Open `lab04_b2_trajectory.py` and identify the five defined `PathPoint` waypoints. Describe how each segment changes the robot's motion.

### Exercise B — Adjust the path

Change one path point to modify the forward travel distance or the turn angle, then run the script under supervision and observe the effect.

### Exercise C — Verify state output

Use menu option `0` and confirm the robot state prints mode, gait, position, velocity, yaw speed, and body height.

---

## 5. Troubleshooting

| Symptom | Action |
|---------|--------|
| No `unitree_sdk2py` imports | Activate `unitree_env` and install the package |
| `ChannelSubscriber` fails | Verify `ChannelFactoryInitialize` interface argument and network connectivity |
| Trajectory does not execute | Confirm `TrajectoryFollow` return value and robot mode; ensure `ClassicWalk(True)` completed |
| Robot does not stop | Use menu option `2` to exit, and verify `ClassicWalk(False)` is called |

---

## 6. Deliverable

- a short video or screenshots showing the robot executing the autonomous trajectory and the final stance.
- one paragraph describing each path segment and how the trajectory commands affect motion.
- confirmation that the robot returned to normal mode or the remote controller after the exercise.

---

## 7. Next / related labs

- **Previous:** [Lab 3 — Advanced B2 stand sequence (low-level joint control)](../lab-03/README.md)
