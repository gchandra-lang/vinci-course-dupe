# Lab 3 — Advanced B2 stand sequence (low-level joint control)

**Duration:** ~30–45 min  
**Robot motion:** Yes — low-level joint commands move legs significantly; instructor supervision required  
**Prerequisites:** `unitree_sdk2py` installed, familiarity with `SportClient` and `lowcmd` concepts, robot powered and on the same network

---

## Learning objectives

1. Understand and run a multi-stage low-level stand sequence using direct joint commands.
2. Learn how to publish `rt/lowcmd` and subscribe to `rt/lowstate` for closed-loop low-level control.
3. Practice releasing high-level motion modes and returning the robot to a remote controller (AI) mode.

---

## 1. Concepts

This lab implements a staged stand routine that transitions joint angles through several target poses using position control:

- Low-level command stream: `rt/lowcmd` (`LowCmd_`) — published at 500 Hz.
- Low-level state stream: `rt/lowstate` (`LowState_`) — used to capture current joint positions.
- MotionSwitcherClient & `SportClient` — used to release high-level controllers before running low-level commands and to switch back to `ai` mode afterwards.

Key parameters in the script:

- Joint `q` targets for each stage (12 joint values)
- `Kp` / `Kd` gains for joint PD control
- Control loop interval: 2 ms (500 Hz)

Why this lab matters

Low-level control exposes how high-level behaviours map to joint commands and demonstrates the importance of safe sequencing and mode management when bypassing high-level controllers.

---

## 2. Safety (required)

- This script WILL move the legs significantly. Clear a large area around the robot (minimum 3 m × 3 m recommended).
- Instructor must supervise at all times.
- Keep hands away from legs and mechanical linkages.
- Ensure the robot is on a stable surface and the power/safety switches are correctly set before starting.
- Be prepared to stop the program (Ctrl+C) — the robot may not be in a stable posture if interrupted.

---

## 3. Hands-on

### Step 0 — Prepare environment

```bash
conda activate unitree_env
cd /path/to/vinci-unitree
```

### Step 1 — Run the stand sequence script

```bash
python course/student/B2-day1/lab-03/lab03_b2_stand_sequence.py <networkInterface>
```

Example:

```bash
python course/student/B2-day1/lab-03/lab03_b2_stand_sequence.py eth0
```

### Step 2 — Use the menu

- Choose `0` to start the low-level stand sequence (robot will move).
- Choose `1` to switch the robot to `ai` mode and regain remote controller control.
- Choose `2` to exit without action.

The stand sequence will:

1. Release any active high-level motion modes (call `StandDown()` and `MotionSwitcherClient.ReleaseMode()` as needed).
2. Initialise `LowCmd_` with safe defaults and PD gains.
3. Publish joint position targets at 500 Hz and step through the defined stages until complete.

---

## 4. Exercises

### Exercise A — Inspect stage targets

Open `lab03_b2_stand_sequence.py` and identify the three primary target joint vectors (`targetPos_1`, `targetPos_2`, `targetPos_3`) and describe in one sentence how each stage changes posture.

### Exercise B — Adjust gains

Experiment with smaller `Kp` / `Kd` values in a simulation or under strict supervision and observe effects on motion smoothness.

### Exercise C — Mode recovery

After running the low-level sequence, choose menu option `1` and confirm the robot responds to the remote controller.

---

## 5. Troubleshooting

| Symptom | Action |
|---------|--------|
| No imports for `unitree_sdk2py` | Activate `unitree_env` and install the package |
| `ChannelPublisher` or `ChannelSubscriber` fails | Verify `ChannelFactoryInitialize` interface argument and network connectivity |
| Unexpected joint behaviour | Stop immediately (Ctrl+C). Check `Kp`/`Kd` and target positions before retrying |
| Cannot regain remote control | Use menu option `1` to call `SelectMode("ai")` and verify return code |

---

## 6. Deliverable

- showing the stand sequence start and final stance.  
- One paragraph describing what each target stage accomplishes and how the PD gains affect behaviour.  
- Confirmation that the robot was returned to `ai` mode or the remote controller after the exercise.

---

## 7. Next lab

**[Lab 4 — Trajectory Following](../lab-0/lab04_b2_trajectory.py)**

