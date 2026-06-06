# Lab 3 — Arm SDK streaming (`rt/arm_sdk`)

**Duration:** ~60–75 min (concepts + supervised run + debrief)  
**Robot motion:** Yes — moves **both arms** and waist joints in a fixed 4-stage trajectory (~21 s)  
**Prerequisites:** [Lab 2](../lab-02/) complete; [Day 5 Lab 2](../../day-05/lab-02/) **Readiness: PASS**

---

## Learning objectives

1. Publish **`LowCmd_`** on DDS topic **`rt/arm_sdk`** (not the `"arm"` RPC from Labs 1–2).
2. Explain the **arm_sdk enable** flag on motor index **29** and the **four stages** of the upstream demo.
3. Relate streamed **`kp` / `kd` / `q`** commands to feedback from **`rt/lowstate`**.
4. Choose **arm5 vs arm7** variant for your robot’s DOF configuration.

---

## 1. Concepts

### Lab 2 RPC vs Lab 3 streaming

| | Labs 1–2 — `G1ArmActionClient` | Lab 3 — arm SDK stream |
|--|-------------------------------|-------------------------|
| **Mechanism** | RPC service **`"arm"`** | DDS publish **`rt/arm_sdk`** |
| **You send** | Discrete action id | `LowCmd_` every **20 ms** (`control_dt_ = 0.02`) |
| **Who plans motion** | Onboard action player | Script interpolates toward `target_pos` |
| **Typical duration** | Seconds per gesture | ~**21 s** (4 × `duration_` = 4 × 3 s) |
| **Stop / release** | `release arm` RPC | Stage 4 ramps arm_sdk **disable** on index 29 |

### Topic wiring

```
subscribe  rt/lowstate   →  current motor_state[joint].q
publish    rt/arm_sdk    →  LowCmd_ with CRC each tick
```

Each arm joint in `arm_joints` gets `q`, `dq=0`, `tau=0`, `kp`, `kd`. The example **blends** from measured `q` toward targets over time.

### Four stages (upstream defaults, `duration_ = 3.0` s)

| Stage | Time window | What happens |
|-------|-------------|--------------|
| **1** | 0 … 3 s | Enable arm_sdk (`motor_cmd[29].q = 1`); blend arms toward **zero** pose |
| **2** | 3 … 9 s | Interpolate to **`target_pos`** (arms-up posture) |
| **3** | 9 … 18 s | Blend back toward measured pose |
| **4** | 18 … 21 s | Ramp arm_sdk **disable** (`motor_cmd[29].q → 0`) |

Script prints **`Done!`** and exits when complete.

### arm5 vs arm7 (this lab uses arm7)

| Script | Arm joints | When to use |
|--------|------------|-------------|
| **`g1_arm5_sdk_dds_example.py`** | 5 DOF per arm + wrist roll + waist | **23 DOF** G1 |
| **`g1_arm7_sdk_dds_example.py`** | Adds wrist pitch/yaw per side | **29 DOF** G1 |

This student script is the **arm7** variant. Confirm with your instructor that the classroom robot is **29 DOF**. On **23 DOF** hardware, use the upstream **arm5** example instead — wrist pitch/yaw indices are marked **INVALID** in the source.

### Do not confuse with `rt/lowcmd`

Full-body low-level control uses **`rt/lowcmd`**. This lab uses **`rt/arm_sdk`** only — the locomotion stack stays responsible for balance while arm_sdk is active.

---

## 2. Safety (required)

- Clear **≥ 2 m**; **ceiling clearance** for raised arms.
- **Spotter** mandatory for first run.
- Complete Lab 2 successfully before trying arm_sdk.
- Do **not** run Lab 2 arm RPC and this lab **back-to-back** without instructor approval — finish one pipeline cleanly first.

---

## 3. Hands-on

### Step 0 — Confirm readiness

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI

python day-05/lab-02/fsm_readonly.py en6
```

### Step 1 — Read the source (before motion)

Open [`g1_arm7_sdk_dds_example.py`](g1_arm7_sdk_dds_example.py) and locate:

- `G1JointIndex` — leg, waist, arm indices
- `arm_joints` — which joints are commanded
- `target_pos` — nominal “arms up” pose (radians)
- `LowCmdWrite()` — four-stage logic and CRC write

### Step 2 — Supervised arm_sdk run

```bash
python day-06/lab-03/g1_arm7_sdk_dds_example.py en6
```

1. Press **Enter** at the safety prompt.
2. Script waits for first `rt/lowstate`, then starts the 50 Hz control thread.
3. Watch all **four stages** (~21 s).
4. Expect **`Done!`** and clean exit.

### Step 3 — Recovery check

```bash
python day-06/lab-02/arm_action_sequence.py en6 --sequence "release arm"
```

If arms look odd after the demo, one RPC `release arm` often helps. Re-run Day 5 Lab 2 to confirm FSM ≠ 1.

---

## 4. Exercises

### Exercise A — Stage map

During a second supervised run (or from video), note **start/end time** for each of the four stages. Does stage 2 match “arms lifting” visually?

### Exercise B — Enable flag

What value does `motor_cmd[29].q` have during stage 1 vs stage 4? What happens if you skip stage 4?

### Exercise C — RPC vs stream (written)

One sentence each: when would you use **`G1ArmActionClient`** vs **`rt/arm_sdk`**?

---

## 5. Troubleshooting

| Symptom | Action |
|---------|--------|
| Hangs before motion | Waiting for first `lowstate` — check Day 5 network/DDS |
| No motion, no errors | Confirm stage 1 sets `motor_cmd[29].q = 1`; verify arm7 vs arm5 DOF |
| Jerky or fighting motion | Stop (Ctrl+C); ensure no other arm SDK client publishing |
| Robot tips or stumbles | Abort; only run when standing stable (FSM not damp) |
| After run, arms odd | Try Lab 2 `--sequence "release arm"` once |
| Wrong DOF variant | 23 DOF robot needs arm5 upstream example, not arm7 |

---

## 6. Deliverable

- Short video note or log: one successful run through **`Done!`**
- Exercise A: four-stage rough timestamps
- One sentence: difference between **`rt/arm_sdk`** and **`"arm"`** RPC

---

## 7. Next lab

**[Lab 4 — Custom arm action](../lab-04/)**  
Build your own multi-pose timeline on `rt/arm_sdk` (A-pose + waist yaw).

---

## References

- [Lab 2](../lab-02/) · [Lab 1](../lab-01/) · [Day 5 Lab 2](../../day-05/lab-02/)
- [`g1_arm7_sdk_dds_example.py`](g1_arm7_sdk_dds_example.py)
- Upstream: [g1_arm7_sdk_dds_example.py](https://github.com/unitreerobotics/unitree_sdk2_python/blob/master/example/g1/high_level/g1_arm7_sdk_dds_example.py) · [g1_arm5_sdk_dds_example.py](https://github.com/unitreerobotics/unitree_sdk2_python/blob/master/example/g1/high_level/g1_arm5_sdk_dds_example.py)
