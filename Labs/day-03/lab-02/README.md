# Lab 2 — Interactive B2 motion menu (supervised movement)

**Duration:** ~20–30 min  
**Robot motion:** Yes — this lab sends motion commands; instructor supervision required  
**Prerequisites:** `unitree_sdk2py` installed, robot on and reachable on the same network interface

---

## Learning objectives

1. Use the `SportClient` API to send basic locomotion commands to the B2 robot.
2. Observe command sequencing (stand before MoveToPos) and gait switching.
3. Practice safe supervised motion: issuing BalanceStand, Move, RecoveryStand, and emergency StopMove.

---

## 1. Concepts

This lab demonstrates the difference between telemetry (read-only) and control (motion) labs.
The script provides a simple numbered menu to execute common commands via the `SportClient`:

- `BalanceStand()` — bring robot to standing balance
- `StandDown()` — sit down / relax stance
- `StopMove()` — immediate motion stop (emergency)
- `Move(x, y, yaw)` — short relative translation
- `RecoveryStand()` — recovery from damp or fallen state
- `MoveToPos(x, y, yaw)` — higher-level move-to command (the script ensures the robot stands first)
- `SwitchGait(type)` — switch gait mode (example uses `2`)

Why this lab matters

Issuing motion commands requires strict safety checks. This lab keeps commands simple and supervised so you can observe effects and learn command semantics.

---

## 2. Safety (required)

- Motion is ENABLED. Clear the floor area (minimum 3 m × 3 m recommended).
- No people or obstacles in front of the robot while it moves.
- Instructor must supervise all movements.
- Keep hands and tools away from the legs during motion.
- Be ready to press **Ctrl+C** to exit the script or use the StopMove menu option for emergencies.

---

## 3. Hands-on

### Step 0 — Prepare environment

```bash
conda activate unitree_env
cd /path/to/vinci-unitree
```

### Step 1 — Run the motion menu

```bash
python course/student/B2-day1/lab-02/lab02_b2_motion_menu.py <networkInterface>
```

Example:

```bash
python course/student/B2-day1/lab-02/lab02_b2_motion_menu.py eth0
```

### Step 2 — Use the menu

- Press `Enter` to continue at the safety prompt.
- Type the menu number and press Enter to send the command to the robot.
- Observe robot behaviour after each command and note return codes printed by the script (`0` = success for typical calls).

Suggested sequence (supervised):

1. `1` — BalanceStand (verify the robot stands)
2. `4` — Move forward 0.5 m (verify controlled translation)
3. `5` — RecoveryStand (try if robot is damp)
4. `6` — MoveToPos (script will call `BalanceStand()` then `MoveToPos`)
5. `3` — StopMove (test emergency stop while moving only under instructor direction)

---

## 4. Exercises

### Exercise A — Validate MoveToPos sequencing

Run option `6` and confirm the script explicitly issues `BalanceStand()` before `MoveToPos`.

### Exercise B — Observe return codes

Record the printed return codes for each command and map them to expected outcomes.

### Exercise C — Gait switch

Try option `7` to call `SwitchGait(2)` and observe changes in locomotion behaviour when issuing `Move` or `MoveToPos` afterwards.

---

## 5. Troubleshooting

| Symptom | Action |
|---------|--------|
| Script fails to import `unitree_sdk2py` | Activate `unitree_env` and ensure the package is installed |
| No connection / timeouts | Verify `ChannelFactoryInitialize` interface name and network connectivity |
| Robot does not stand or move | Confirm robot safety switch is enabled and power state; retry `BalanceStand()` |
| Unexpected motion or instability | Stop immediately with `StopMove()` and call instructor |

---

## 6. Deliverable

- A short log or video demonstrating: successful `BalanceStand`, one `Move` or `MoveToPos`, and a successful `StopMove` (if tested).  
- One sentence describing what `BalanceStand`, `Move`, and `StopMove` do.

---

## 7. Next lab

**[Lab 3 — Stand sequence and compound motions](../lab-03/lab03_b2_stand_sequence.py)**
