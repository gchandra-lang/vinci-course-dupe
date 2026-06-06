# Day 6 — G1 Arm Control

**Platform:** Unitree **G1** (EDU Plus / Ultimate-D)  
**Stack:** [`unitree_sdk2_python`](https://github.com/unitreerobotics/unitree_sdk2_python) + CycloneDDS

**Prerequisite:** [Day 5](../day-05/) complete — especially Lab 2 **Readiness: PASS** (`FSM ≠ 1`, `CheckMode → ai`).

---

## What this day is for

G1 **high-level arm actions** (RPC) and **arm SDK streaming** (`rt/arm_sdk`) — from interactive menus to scripted sequences and custom joint trajectories.

**By the end of Day 6** you should be able to:

- Run discrete arm gestures via **`G1ArmActionClient`** (`ExecuteAction`).
- Build **multi-step arm sequences** with pauses and `release arm`.
- Publish **`LowCmd_`** on **`rt/arm_sdk`** and explain the arm_sdk enable flag.
- Design a simple **custom arm trajectory** using measured joint positions and blended poses.

---

## Lab sequence

| Lab | Folder | Motion? | Script | Focus |
|-----|--------|---------|--------|--------|
| **1** | [`lab-01/`](lab-01/) | **Yes** | [`g1_arm_action_example.py`](lab-01/g1_arm_action_example.py) | Interactive arm action menu (RPC `"arm"`) |
| **2** | [`lab-02/`](lab-02/) | **Yes** | [`arm_action_sequence.py`](lab-02/arm_action_sequence.py) | Scripted `ExecuteAction` sequence + readiness gate |
| **3** | [`lab-03/`](lab-03/) | **Yes** | [`g1_arm7_sdk_dds_example.py`](lab-03/g1_arm7_sdk_dds_example.py) | Arm SDK stream — upstream 4-stage demo (29 DOF) |
| **4** | [`lab-04/`](lab-04/) | **Yes** | [`custom_arm_action.py`](lab-04/custom_arm_action.py) | Custom A-pose + waist yaw via `rt/arm_sdk` |

Work through labs **in order**. Every motion lab requires Day 5 Lab 2 **Readiness: PASS** before running.

**If time is short:** complete Labs 1–2 (RPC arm actions); treat Labs 3–4 as optional depth on `rt/arm_sdk`.

---

## Session setup (every lab)

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/repo
```

Set your NIC once per session:

```bash
export G1_INTERFACE=en6   # macOS example; use enp0s31f6 on Linux
```

Re-check readiness before first motion:

```bash
python day-05/lab-02/fsm_readonly.py en6
```

---

## Quick start

```bash
# Lab 1 — interactive arm menu
python day-06/lab-01/g1_arm_action_example.py en6

# Lab 2 — show action map (no robot)
python day-06/lab-02/arm_action_sequence.py --show-map

# Lab 2 — default sequence (face wave + release)
python day-06/lab-02/arm_action_sequence.py en6

# Lab 3 — arm SDK 4-stage demo (~21 s)
python day-06/lab-03/g1_arm7_sdk_dds_example.py en6

# Lab 4 — custom A-pose + waist yaw (~20 s)
python day-06/lab-04/custom_arm_action.py en6
```

---

## Key concepts (Day 6)

| Topic | G1 detail |
|-------|-----------|
| High-level arm RPC | `G1ArmActionClient` → service **`"arm"`** · `ExecuteAction(id)` |
| Action names | Static **`action_map`** in SDK (`"face wave"`, `"release arm"`, …) |
| Arm SDK stream | Publish **`LowCmd_`** on **`rt/arm_sdk`** at ~50 Hz |
| Enable flag | `motor_cmd[29].q = 1` enables arm_sdk; ramp to 0 to release |
| vs full low-level | **`rt/lowcmd`** controls whole body — not used in these labs |
| Readiness gate | `rt/lowstate` OK + `CheckMode → ai` + **FSM ≠ 1** |

### Lab 1 RPC vs Lab 3–4 streaming

| | Lab 1–2 — `G1ArmActionClient` | Lab 3–4 — `rt/arm_sdk` |
|--|-------------------------------|-------------------------|
| **Mechanism** | RPC service `"arm"` | DDS publish `LowCmd_` |
| **You send** | Discrete action id | Joint targets every 20 ms |
| **Who plans motion** | Onboard action player | Your script interpolates poses |
| **Stop / release** | `release arm` RPC | Ramp arm_sdk disable on index 29 |

---

## Deliverables (day summary)

| Lab | Submit |
|-----|--------|
| 1 | Log of two supervised gestures + `release arm`; list output from `list` command |
| 2 | `--show-map` output; `--dry-run` PASS; log of default or approved `--sequence` |
| 3 | Note of four stages with rough timestamps; one sentence: RPC vs `rt/arm_sdk` |
| 4 | Description of custom timeline (A-pose, waist yaw); video or instructor sign-off |

---

## References

| Resource | Link |
|----------|------|
| Unitree SDK (Python) | [github.com/unitreerobotics/unitree_sdk2_python](https://github.com/unitreerobotics/unitree_sdk2_python) |
| G1 arm action example | [example/g1/high_level/g1_arm_action_example.py](https://github.com/unitreerobotics/unitree_sdk2_python/blob/master/example/g1/high_level/g1_arm_action_example.py) |
| G1 arm7 SDK example | [example/g1/high_level/g1_arm7_sdk_dds_example.py](https://github.com/unitreerobotics/unitree_sdk2_python/blob/master/example/g1/high_level/g1_arm7_sdk_dds_example.py) |
| Day 5 readiness | [day-05/lab-02/fsm_readonly.py](../day-05/lab-02/fsm_readonly.py) |

---

## Next day

**[Day 7 — Audio & peripherals](../day-07/)**  
LED, audio, TTS — typically no locomotion.
