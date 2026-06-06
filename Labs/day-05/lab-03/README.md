# Lab 3 — Interactive FSM & LocoClient actions

**Duration:** ~20–30 min  
**Robot motion:** Yes — this lab sends motion commands; supervision required  
**Prerequisites:** [Lab 2](../lab-02/) **Readiness: PASS** (`FSM ≠ 1`, `CheckMode → ai`)

---

## Learning objectives

1. Use the `LocoClient` API to read and set FSM id on the G1 robot.
2. Run a supervised gesture (`ShakeHand`) and observe FSM state before and after.
3. Practice safe mode management: understand `Damp()`, `ZeroTorque()`, and recovery via `SetFsmId`.
4. Relate interactive RPC commands to the read-only checks from Labs 0–2.

---

## 1. Concepts

This lab demonstrates the difference between telemetry/read-only labs (Labs 1–2) and control (motion) labs.
The script provides an interactive menu to execute common `LocoClient` commands:

| Menu id | Action | Effect |
|---------|--------|--------|
| **0** | `ZeroTorque()` | **CAUTION** — all joints relax; robot may fall instantly |
| **1** | `Damp()` | Enter damp mode (FSM = 1); blocks high-level wave/walk |
| **2** | `ShakeHand()` | Supervised gesture — robot moves arm |
| **3** | `GetFsmId()` | Read current FSM id (same as Lab 2 RPC 7001) |
| **4** | `SetFsmId(id)` | Set FSM directly (prompts for id: 0, 1, 4, 802, …) |

Why this lab matters

Issuing motion commands requires strict safety checks. This lab keeps commands simple and supervised so you can observe effects and learn FSM semantics before Day 6 locomotion sequences.

---

## 2. Safety (required)

- Motion is **ENABLED**. Clear the floor area (minimum 2 m around the robot).
- Robot **feet on the ground** — do not run while hanging.
- Supervision required for all movements.
- Keep hands away from the robot during gestures.
- **Never choose option 0 (Zero Torque)** unless instructed — the robot will collapse.
- Avoid option 1 (`Damp()`) unless you know how to recover (stand + remote or `SetFsmId(500)`).
- Be ready to press **Ctrl+C** to exit the script.

Official example warning:

> *Please ensure there are no obstacles around the robot while running this example.*

---

## 3. Hands-on

### Step 0 — Prepare environment

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/repo
```

### Step 1 — Confirm readiness

```bash
python day-05/lab-02/fsm_readonly.py en6
```

Expect `Readiness: PASS`. Do **not** proceed if FSM = 1 or CheckMode ≠ `ai`.

### Step 2 — Run the interactive menu

```bash
python day-05/lab-03/setmode_action_fsm.py en6
```

- Press **Enter** at the safety prompt.
- Type `list` to see all menu options.
- Enter a menu **id** (0–4) or option name to execute.

Suggested sequence (supervised):

1. `3` — GetFsmId (record starting FSM)
2. `2` — ShakeHand (observe gesture; clear space in front)
3. `3` — GetFsmId again (note any change)
4. `4` then enter `500` — SetFsmId to Start (if needed after recovery practice)

**Do not** run options 0 or 1 unless your instructor directs a damp/recovery exercise.

### Step 3 — Verify state after session

In a second terminal:

```bash
python day-05/lab-02/fsm_readonly.py en6
```

Confirm the robot is still in a safe, recoverable state before leaving the lab.

---

## 4. Exercises

### Exercise A — FSM before and after

Record FSM id before and after `ShakeHand`. Did the gesture require a specific FSM state?

### Exercise B — Damp recovery (supervised, instructor only)

If allowed: run option `1` (Damp), confirm Lab 2 shows `FSM=1`, then recover using remote stand or `SetFsmId(500)` via option `4`. Document steps.

### Exercise C — Compare to Lab 2

Explain in 2–3 sentences why Lab 2 could read FSM without moving the robot, but Lab 3 needs extra safety rules.

---

## 5. Troubleshooting

| Symptom | Action |
|---------|--------|
| Script fails to import `unitree_sdk2py` | Activate `unitree_env` and ensure the package is installed |
| No connection / timeouts | Verify interface name and `unset CYCLONEDDS_URI` |
| Robot does not move on ShakeHand | Re-run Lab 2 — FSM may be 1 (damp); stand robot first |
| Robot collapsed after Zero Torque | **Emergency** — power off if needed; do not retry without instructor |
| Stuck in damp after option 1 | Stand via remote L1+UP or `SetFsmId(500)`; re-run Lab 2 until PASS |

---

## 6. Deliverable

- A short log or video demonstrating: successful `GetFsmId`, one supervised `ShakeHand`, and post-lab `Readiness: PASS`
- One sentence each: what `Damp()`, `ShakeHand()`, and `SetFsmId` do
- Confirmation that option 0 (Zero Torque) was **not** used unless instructor-directed

---

## 7. Next lab

**Next camp day:** [Day 6 — Locomotion & arm](../../day-06/)  
Scripted stand, wave, walk, and arm actions — requires **Readiness: PASS** from Lab 2.

---

## References

- [Lab 2](../lab-02/) · [Lab 1](../lab-01/) · [Lab 0](../lab-00/)
- [`setmode_action_fsm.py`](setmode_action_fsm.py)
- [Unitree sports services](https://support.unitree.com/home/en/developer/sports_services)
