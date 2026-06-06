# Lab 4 — Custom arm action (`rt/arm_sdk`)

**Duration:** ~45–60 min  
**Robot motion:** Yes — custom A-pose, waist yaw, and return-to-stand (~20 s total)  
**Prerequisites:** [Lab 3](../lab-03/) complete; [Day 5 Lab 2](../../day-05/lab-02/) **Readiness: PASS**

---

## Learning objectives

1. Build a **custom joint trajectory** using measured standing pose as reference.
2. Blend between poses with linear interpolation (`blend_pose`) instead of fixed `target_pos` arrays.
3. Command **waist yaw** and **shoulder roll** offsets for an A-pose demonstration.
4. Release arm_sdk control cleanly at the end of a multi-stage timeline.

---

## 1. Concepts

### Extension of Lab 3

Lab 3 runs the upstream **four-stage** demo with a fixed `target_pos`. This lab implements an **11-stage timeline** in `LowCmdWrite()`:

| Stage | Time (s) | Action |
|-------|----------|--------|
| 1 | 0 → 2 | Blend from current pose → **standing** reference |
| 2 | 2 → 4 | Hold standing |
| 3 | 4 → 6 | Blend standing → **A-pose** (shoulder roll ±30°) |
| 4 | 6 → 10 | Hold A-pose |
| 5 | 10 → 11 | Waist yaw **left +30°** |
| 6 | 11 → 12 | Hold left yaw |
| 7 | 12 → 14 | Waist yaw **right −60°** (from left target) |
| 8 | 14 → 15 | Hold right yaw |
| 9 | 15 → 17 | Return to **standing** |
| 10 | 17 → 19 | Hold standing |
| 11 | 19 → 20 | Ramp **arm_sdk disable** while holding stand |

Total runtime ~**20 s**; script prints **`Done!`** and exits.

### Pose definitions

On first tick, the script captures **`_stand_q`** from live `motor_state`. Derived poses:

- **A-pose:** left shoulder roll +30°, right shoulder roll −30° from stand
- **Yaw left:** waist yaw +30° from A-pose
- **Yaw right:** waist yaw −60° from yaw-left target

Gains: `kp = 40`, `kd = 1.0` (softer than Lab 3’s 60 / 1.5).

### Same arm_sdk mechanics as Lab 3

```
motor_cmd[29].q = 1.0   # enable arm_sdk (held until stage 11 ramp-down)
publish rt/arm_sdk      # LowCmd_ + CRC @ 50 Hz
subscribe rt/lowstate   # feedback for initial capture and blending
```

---

## 2. Safety (required)

- Clear **≥ 2 m**; ceiling clearance; spotter mandatory.
- Robot must be **standing stable** (Day 5 Lab 2 PASS).
- Complete Lab 3 successfully before this lab.
- **Do not modify joint offsets or gains** without instructor approval.
- If motion looks unstable, **Ctrl+C** and run Lab 2 `release arm`.

---

## 3. Hands-on

### Step 0 — Session setup

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI

python day-05/lab-02/fsm_readonly.py en6
```

### Step 1 — Study the timeline

Open [`custom_arm_action.py`](custom_arm_action.py) and find:

- `_stand_q`, `_a_pose_q`, `_yaw_left_q`, `_yaw_right_q` initialization
- `blend_pose()` and `write_pose()` helpers
- Time breakpoints `t1` … `t11`

### Step 2 — Supervised run

```bash
python day-06/lab-04/custom_arm_action.py en6
```

1. Press **Enter** at the safety prompt.
2. Watch the full ~20 s sequence.
3. Confirm **`Done!`** and neutral-ish arm posture.

### Step 3 — Recovery

```bash
python day-06/lab-02/arm_action_sequence.py en6 --sequence "release arm"
python day-05/lab-02/fsm_readonly.py en6
```

---

## 4. Exercises

### Exercise A — Timeline sketch

Draw a simple timeline (0–20 s) labeling when A-pose starts and when waist yaw peaks.

### Exercise B — Compare to Lab 3

What is one advantage of capturing `_stand_q` from live state vs using a fixed `target_pos` array?

### Exercise C — Design extension (written only)

Propose **one additional stage** (e.g. single-arm point) that still ends with arm_sdk release. Describe which joints you would change — do **not** run without instructor approval.

---

## 5. Troubleshooting

| Symptom | Action |
|---------|--------|
| Hangs at start | Waiting for `lowstate` — fix Day 5 network first |
| Asymmetric A-pose | Check left/right shoulder roll signs (+30° / −30°) |
| Excessive waist twist | Stop run; confirm ±30° / −60° limits with instructor |
| Arms drift after Done | Run `release arm` via Lab 2 |
| Invalid joint on 23 DOF | Waist roll/pitch may be INVALID — confirm hardware with instructor |

---

## 6. Deliverable

- Log or short video of one successful run through **`Done!`**
- Exercise A timeline sketch
- One sentence comparing this lab’s approach to Lab 3’s four-stage demo

---

## 7. Next day

**[Day 7 — Audio & peripherals](../../day-07/)**  
LED, audio, TTS — capstone glue for multi-modal demos.

---

## References

- [Lab 3](../lab-03/) · [Lab 2](../lab-02/) · [Day 5 Lab 2](../../day-05/lab-02/)
- [`custom_arm_action.py`](custom_arm_action.py)
