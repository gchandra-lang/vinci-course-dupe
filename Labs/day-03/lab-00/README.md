# B2 Day 1 — Labs 1–3 Summary

This summary (`README.md`) collects the essentials for Day 1 B2 labs (Lab 1–3).
It mirrors the structure used in the per-lab README files and provides quick links and commands to run each lab.

**Audience:** students preparing to run the B2 Day 1 exercises under instructor supervision.

---

## Quick facts

- Platform: Unitree B2 (quadruped)  
- Day: 1 — Intro telemetry, supervised motion, low-level stand sequence  
- Safety: Labs 2–3 command motion; instructor supervision required; clear working area

---

## Prerequisites

1. `conda activate unitree_env` with `unitree_sdk2py` installed.  
2. Laptop on the same subnet as the B2 (verify interface name, e.g. `eth0`).  
3. Instructor present for any motion commands (Labs 2–3).

---

## Lab 1 — Subscribe to `rt/sportmodestate` (read-only)

- Purpose: Verify DDS connectivity and read robot telemetry without commanding motion.  
- Duration: ~20–30 min  
- Safety: No motion commanded.  
- Run:

```bash
python course/student/B2-day1/lab-01/lab01_b2_subscribe_sport_mode_state.py <networkInterface>
```

- What you observe: `mode`, `gait_type`, `position`, `velocity`, `yaw_speed`, `body_height`.  
- Deliverable: Screenshot/log of received `rt/sportmodestate` messages and one-sentence description of key fields.

---

## Lab 2 — Interactive motion menu (supervised movement)

- Purpose: Use `SportClient` to issue simple supervised motions via a menu.  
- Duration: ~15–30 min  
- Safety: MOTION ENABLED. Clear at least 3 m × 3 m area; instructor present.  
- Run:

```bash
python course/student/B2-day1/lab-02/lab02_b2_motion_menu.py <networkInterface>
```

- Menu commands include `BalanceStand()`, `StandDown()`, `StopMove()`, `Move()`, `RecoveryStand()`, `MoveToPos()`, and gait switch.  
- Suggested supervised sequence: BalanceStand → Move (short) → RecoveryStand → MoveToPos.  
- Deliverable: Short log/video showing BalanceStand and one Move/MoveToPos (and StopMove if tested).

---

## Lab 3 — Advanced stand sequence (low-level joint control)

- Purpose: Demonstrate a multi-stage low-level stand sequence by publishing `rt/lowcmd` motor targets.  
- Duration: ~30–45 min  
- Safety: HIGH MOTION RISK — legs move significantly. Clear space, spotter required.  
- Run:

```bash
python course/student/B2-day1/lab-03/lab03_b2_stand_sequence.py <networkInterface>
```

- Key points: Releases high-level modes first, publishes joint position PD targets at 500 Hz, and uses CRC on `LowCmd_`.  
- Deliverable: Video/log of the multi-stage stand sequence and confirmation you can switch back to remote (`SelectMode("ai")`).

---

## Common notes & troubleshooting

- If `ChannelFactoryInitialize` fails: verify the interface name and that the laptop is on the B2 subnet.  
- If telemetry not received in Lab 1: confirm the robot is powered and DDS topics are publishing.  
- For motion failures: verify FSM/readiness (use Lab 1 outputs), ensure no obstacles, and have an instructor present.  
- Package/import issues: ensure `conda activate unitree_env` and `unitree_sdk2py` are installed.

---

## Safety checklist (before running any motion lab)

1. Spotter present (first run).  
2. Clear area ≥ 3 m × 3 m for motion labs (2 m may be sufficient for arm labs).  
3. Confirm `rt/sportmodestate` is publishing and FSM ≠ damp.  
4. Have an emergency stop procedure and power-off plan accessible.

---

## Deliverables (summary)

- Lab 1: Telemetry log.  
- Lab 2: Motion log/video showing BalanceStand and Move/MoveToPos.  
- Lab 3: Stand sequence log/video and confirmation of `ai` mode recovery.

---

## Links

- Lab 1 script: [lab01_b2_subscribe_sport_mode_state.py](lab-01/lab01_b2_subscribe_sport_mode_state.py)  
- Lab 2 script: [lab02_b2_motion_menu.py](lab-02/lab02_b2_motion_menu.py)  
- Lab 3 script: [lab03_b2_stand_sequence.py](lab-03/lab03_b2_stand_sequence.py)


