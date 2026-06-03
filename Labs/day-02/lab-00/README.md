# Lab 0 — Day 2 Readiness & Inspection Scenario

**Duration:** ~45–60 min (recap + theory + checks)  
**Robot required:** Optional for Sections A–C; **recommended** for Section D  
**Motion:** None

**PDF coverage (Day 2):** Design inspection tasks · autonomous routines (planning) · deploy preparation

**Prerequisite:** [Day 1](../../day-01/) Labs 0–4 complete (including `lab02_safe_posture.py` and `lab04_obstacle_avoid_intro.py`).

---

## Learning objectives

By the end of Lab 0 you should be able to:

1. Confirm **Day 1 artifacts** and patrol-related SDK imports are present on your machine.
2. Sketch the **inspection pipeline** (sense → log → decide → act → report).
3. Fill in a **patrol scenario card** (checkpoints, speed limits, abort rules, deliverables).
4. State **Day 2 safety rules** for multi-stop patrol (arena, spotter, avoid API, no SLAM claims).
5. Run **`lab00_day2_readiness.py`** and interpret PASS / PARTIAL / FAIL before Lab 1.

---

## 1. Day 1 recap (5 min)

You should already have hands-on experience with:

| Day 1 lab | Skill | Day 2 use |
|-----------|--------|-----------|
| Lab 1 | Subscribe `rt/sportmodestate`, JSONL log | Patrol logging |
| Lab 2 | `SportClient`, `CheckMode`, stand + walk | Stand prep before patrol |
| Lab 3 | `VideoClient`, inspection bundle | Per-checkpoint `frame.jpg` |
| Lab 4 | `ObstaclesAvoidClient`, increment preview | Multi-leg patrol legs |

If any Day 1 motion lab did not pass on hardware, **fix that before Lab 2** (Day 2 patrol). Lab 1 today is still OK without motion.

Quick re-check (optional):

```bash
python course/day-01/lab-00/lab00_readiness.py en6
python course/day-01/lab-03/lab02_sport_readonly.py en6
```

---

## 2. Inspection architecture (conceptual)

Day 2 builds a **scripted inspection loop** in a **known cleared arena** — not full SLAM autonomy.

```text
┌──────────┐   ┌──────────┐   ┌─────────────┐   ┌──────────┐   ┌─────────┐
│ Sensors  │──►│ Log DDS  │──►│ Scenario /  │──►│ Patrol   │──►│ Run     │
│ camera,  │   │ JSONL +  │   │ abort rules │   │ avoid +  │   │ folder  │
│ state    │   │ images   │   │ (this lab)  │   │ capture  │   │ report  │
└──────────┘   └──────────┘   └─────────────┘   └──────────┘   └─────────┘
```

| Stage | Day 2 coverage |
|-------|----------------|
| **Sense** | `sportmodestate`, `lowstate`, front camera |
| **Log** | `sportmodestate.jsonl`, checkpoint images (Lab 1 schema) |
| **Decide** | Scenario card + optional SOC / rate rules (Lab 5) |
| **Act** | `ObstaclesAvoidClient` legs between checkpoints (Labs 2–3) |
| **Report** | `metadata.json`, `patrol_plan.json`, presentation (Labs 4–5) |

**What Day 2 does *not* do:** global map, GPS, Nav2 — those belong to the [ROS extension track](../../day-02/README.md#extension-track-ros--sim).

---

## 3. Patrol scenario worksheet

Each team maintains one JSON file for the day (used in Labs 2–5).

### 3.1 Create your file

```bash
cd /path/to/vinci-unitree
conda activate unitree_env

python course/day-02/lab-00/lab00_day2_readiness.py \
  --write-scenario my_team_scenario.json
```

Edit [`patrol_scenario.template.json`](patrol_scenario.template.json) fields:

| Field | Purpose |
|-------|---------|
| `team_name` / `operator` | Run folder metadata |
| `arena` | Size, floor, hazards |
| `checkpoints` | ≥ 2 stops (`id`, `label`, `marker`) |
| `motion_limits` | Class caps: `max_forward_vx_mps` ≤ **0.25**, `max_increment_dx_m` ≤ **0.5** unless instructor approves |
| `abort_rules` | When spotter / script must stop |
| `deliverables` | What you owe at end of day |

### 3.2 Validate

```bash
python course/day-02/lab-00/lab00_day2_readiness.py \
  --validate-scenario my_team_scenario.json
```

**Expected:** `PASS scenario valid: my_team_scenario.json (N checkpoints)`.

Keep this file in git or your lab notebook; Lab 3 will reference the same checkpoint IDs in `patrol_plan.json`.

---

## 4. Day 2 software focus

Extends Day 1 stack with **patrol** clients:

```
course/day-02/lab-*.py
        │
        ├── day-01/go2_motion_helpers.py   stand prep, periodic Move
        └── (later) go2_patrol_helpers.py  legs + capture
        │
        ▼
unitree_sdk2py
        ├── go2.obstacles_avoid    ObstaclesAvoidClient  ← patrol legs
        ├── go2.video              VideoClient           ← checkpoints
        ├── go2.sport              SportClient           ← stand prep
        └── idl.unitree_go
```

Upstream patrol references (read-only):

| Path | Purpose |
|------|---------|
| `example/obstacles_avoid/obstacles_avoid_move.py` | Velocity + increment / absolute goals |
| `example/obstacles_avoid/obstacles_avoid_switch.py` | Switch on/off |
| Day 1 [`lab04_obstacle_avoid_intro.py`](../../day-02/lab-02/lab04_obstacle_avoid_intro.py) | Camp avoid intro |

Docs: [ObstaclesAvoidClient](https://support.unitree.com/home/en/developer/ObstaclesAvoidClient)

---

## 5. Safety — multi-stop patrol

Day 1 rules still apply. **Additional** rules for Day 2:

1. **Arena boundary** — mark corners with cones; agree who calls halt.
2. **One patrol at a time** per Go2 on the subnet.
3. **Default speed cap** — forward `vx` ≤ **0.25 m/s**; increment `dx` ≤ **0.5 m** per leg unless instructor signs off in your scenario file.
4. **Avoid mode default** — patrol legs use `ObstaclesAvoidClient` with `SwitchSet(True)` and `UseRemoteCommandFromApi(True)` unless the lab README says otherwise.
5. **Clean shutdown** — every patrol script must stop with `Move(0,0,0)`, release API mode, and `SwitchSet(False)` on exit or `Ctrl+C`.
6. **Increment goals are local** — do not describe Day 2 as “GPS navigation” or “SLAM patrol”.
7. **No new acrobatics** — `HandStand` / flips stay off the patrol path.

Official example warning (same as Day 1):

> *Please ensure there are no obstacles around the robot while running this example.*

Full reference: [`docs/GO2-FIELD-GUIDE.md`](../../../docs/GO2-FIELD-GUIDE.md)

---

## 6. Hands-on checklist

Work through **A → D**. Tick each box in your notes.

### A. Machine + Day 1 prerequisite (no robot)

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/vinci-unitree

python course/day-02/lab-00/lab00_day2_readiness.py
```

- [ ] Summary: **PASS — Day 2 machine ready**
- [ ] All Day 1 required scripts reported PASS
- [ ] `ObstaclesAvoidClient` import PASS

### B. Scenario card (no robot)

```bash
python course/day-02/lab-00/lab00_day2_readiness.py \
  --write-scenario my_team_scenario.json
# edit file
python course/day-02/lab-00/lab00_day2_readiness.py \
  --validate-scenario my_team_scenario.json
```

- [ ] ≥ 2 checkpoints defined with unique `id`
- [ ] `motion_limits` within class caps (or instructor approval noted in `notes`)
- [ ] Abort rules include spotter halt

### C. Network (robot powered, PC wired)

Replace `en6` with your NIC — see [Go2 Field Guide](../../../docs/GO2-FIELD-GUIDE.md).

- [ ] `ping -c 2 192.168.123.161` → replies
- [ ] Session exports: `CYCLONEDDS_HOME`, `CYCLONEDDS_URI` unset

### D. Robot readiness (optional but recommended)

```bash
python course/day-02/lab-00/lab00_day2_readiness.py en6
```

| Result | Meaning | Next step |
|--------|---------|-----------|
| **PASS** (exit 0) | DDS + sport OK | [Lab 1](../lab-01/) |
| **PARTIAL** (exit 2) | DDS OK; unusual `CheckMode` | Lab 1 OK; fix before Lab 2 motion |
| **FAIL** (exit 1) | Network / DDS | Field guide; do not run patrol |

If motion was shaky on Day 1, re-run before Lab 2:

```bash
python course/day-01/lab-03/lab02_safe_posture.py en6
python course/day-02/lab-02/lab04_obstacle_avoid_intro.py en6 --dry-run
```

---

## 7. Knowledge check (self-test)

1. What is the difference between Day 1’s single **inspection bundle** and Day 2’s **run folder**?
2. Which client commands a forward **increment** leg in avoid mode?
3. Name two **abort rules** your team will use.
4. Why is increment-based patrol **not** the same as SLAM?
5. What is the maximum forward speed your scenario file should use in class by default?

<details>
<summary>Answers</summary>

1. Day 2 adds **`patrol_plan.json`**, multiple **`checkpoints/`**, and a full-patrol **JSONL** — one run, many stops.
2. **`ObstaclesAvoidClient.MoveToIncrementPosition(dx, dy, dyaw)`** (after `SwitchSet` + `UseRemoteCommandFromApi`).
3. Any two from your scenario (e.g. spotter halt, remote override, low SOC).
4. Increment goals are **local odometry-style legs** in a prepared arena — no global map or localization stack.
5. **0.25 m/s** (`max_forward_vx_mps` in template) unless instructor approves higher in writing.

</details>

---

## 8. Deliverable

Submit (notebook / wiki / PR comment):

1. Log: `lab00_day2_readiness.py` → **Day 2 machine ready**
2. Log: `lab00_day2_readiness.py en6` → **PASS** or **PARTIAL** (one line why)
3. Your validated **`my_team_scenario.json`** (or PDF export of the same fields)
4. One sentence: what your team will capture at **each checkpoint** (image only, or image + BMS)

---

## 9. Next lab

**[Lab 1 — Run folder schema & bundle validation](../lab-01/)**  
Define the standard run directory and validate inspection data — still no patrol motion.

---

## References

- Day 2 overview: [`../../day-02/README.md`](../../day-02/README.md)
- Day 1: [`../../day-01/README.md`](../../day-01/README.md)
- Script: [`lab00_day2_readiness.py`](lab00_day2_readiness.py) · template: [`patrol_scenario.template.json`](patrol_scenario.template.json)
- Field guide: [`docs/GO2-FIELD-GUIDE.md`](../../../docs/GO2-FIELD-GUIDE.md)
