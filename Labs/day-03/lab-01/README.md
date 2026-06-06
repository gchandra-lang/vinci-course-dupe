# Lab 1 — Subscribe to B2 `SportModeState`

**Duration:** ~15–25 min  
**Robot motion:** No — read-only status subscription only  
**Prerequisites:** `unitree_sdk2py` installed and network interface connected to the B2 robot

---

## Learning objectives

1. Subscribe to DDS topic **`rt/sportmodestate`** and receive `SportModeState_` messages.
2. Read the robot’s current mode, gait, body position, velocity, yaw speed, and height.
3. Understand the difference between status telemetry and motion commands.
4. Verify the network interface and DDS setup before attempting any control lab.

---

## 1. Concepts

### `rt/sportmodestate` status stream

The B2 publishes its current locomotion state on the DDS topic **`rt/sportmodestate`**.
This lab does not send any motion commands; it only listens for telemetry.

Key fields in `SportModeState_`:

- `mode` — current control mode
- `gait_type` — active gait
- `position` — robot body position `[x, y, z]`
- `velocity` — body velocity `[vx, vy, vz]`
- `yaw_speed` — rotational speed around the vertical axis
- `body_height` — body height above the floor

### Why this lab matters

Reading `rt/sportmodestate` is a safe first step before commanding the robot.
It confirms DDS is working, the robot is publishing state, and your interface is correct.

---

## 2. Hands-on

### Step 0 — Safety

- Clear the area around the robot even though no motion is commanded.
- Confirm the robot is on a stable surface.
- Use the correct network interface for your B2 robot.

### Step 1 — Activate the environment

```bash
conda activate unitree_env
cd /path/to/vinci-unitree
```

### Step 2 — Run the subscriber

```bash
python course/student/B2-day1/lab01_b2_subscribe_sport_mode_state.py <networkInterface>
```

Example:

```bash
python course/student/B2-day1/lab01_b2_subscribe_sport_mode_state.py eth0
```

### Step 3 — Observe robot status

The script prints each received message as a single line with:

- `mode`
- `gait`
- `pos` `[x, y]`
- `vel` `[vx, vy]`
- `yaw`
- `height`

If no messages arrive within 5 seconds, the script warns you to check the connection.

### Step 4 — Stop cleanly

Press **Ctrl+C** to exit the subscriber.

---

## 3. Exercises

### Exercise A — Verify connection

Run the script and confirm it prints live state lines. If it does not, check the interface and whether the robot is on the same DDS network.

### Exercise B — Inspect the payload

Open `lab01_b2_subscribe_sport_mode_state.py` and identify where each printed field comes from in the callback.

### Exercise C — Compare to motion labs

Explain why this lab is safe to run before any arm or locomotion control lab.

---

## 4. Troubleshooting

| Symptom | Action |
|---------|--------|
| No output, script starts normally | Verify the network interface and the robot’s DDS network connection |
| Warning after 5 seconds | Confirm the B2 robot is powered on and on the same subnet |
| Import error for `unitree_sdk2py` | Activate the correct conda environment and ensure `unitree_sdk2py` is installed |
| `ChannelFactoryInitialize` fails | Check the interface name and local network configuration |

---

## 5. Deliverable

- Screenshot or log showing the script successfully receiving `rt/sportmodestate` updates
- One sentence describing the meaning of `mode`, `gait_type`, `position`, and `body_height`
- Confirmation that no motion was commanded during this lab

---

## 6. Next lab

**[Lab 2 — B2 motion menu and command sequencing](../B2-day-1/lab02_b2_motion_menu.py)**
