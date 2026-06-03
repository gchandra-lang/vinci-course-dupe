# Lab 0 — Day 2 readiness & patrol scenario

| | |
|--|--|
| **Duration** | ~45–60 min |
| **Motion** | No |
| **Robot** | Optional (Section D recommended) |
| **Prerequisite** | [Day 1 Lab 0–5](../../day-01/) — especially [Lab 5](../../day-01/lab-05/) on hardware |

---

## What you will learn

- How Day 2 **inspection patrol** fits after Day 1 (sense → log → act → report).
- What files and SDK imports Day 2 needs on your laptop.
- How to create and validate your team **`my_team_scenario.json`**.
- Day 2 **safety rules** before any avoid or patrol motion.

---

## What you will run

| Step | Command / file |
|------|----------------|
| Gate check (no robot) | `python course/student/day-02/lab-00/lab00_day2_readiness.py` |
| Copy scenario template | `patrol_scenario.template.json` → `my_team_scenario.json` |
| Validate scenario | `python …/lab00_day2_readiness.py --validate-scenario my_team_scenario.json` |
| Optional robot recap | `python …/lab00_day2_readiness.py <NIC>` |

---

## Steps

### 1. Environment (every session)

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
export GO2_INTERFACE=enx207bd22b611a   # your NIC
cd /path/to/vinci-unitree
```

### 2. Machine gate

```bash
python course/student/day-02/lab-00/lab00_day2_readiness.py
```

**PASS** when Day 1 student files, Day 2 lab scripts, and patrol SDK imports are found.

### 3. Scenario worksheet

Edit `my_team_scenario.json` (copy from `patrol_scenario.template.json`):

- Team name, operator, arena description  
- ≥ 3 checkpoint IDs (e.g. `cp_A`, `cp_B`, `cp_C`)  
- `motion_limits` (max speed, max increment per leg)  
- `abort_rules` and `deliverables`

Validate:

```bash
python course/student/day-02/lab-00/lab00_day2_readiness.py \
  --validate-scenario my_team_scenario.json
```

### 4. Optional Day 1 recap (robot on)

```bash
python course/student/day-01/lab-04/lab04_sport_readonly.py $GO2_INTERFACE
python course/student/day-01/lab-05/lab05_safe_posture.py $GO2_INTERFACE --dry-run
```

---

## Expected results

| Output | Meaning |
|--------|---------|
| All Day 1 / Day 2 file checks **PASS** | Proceed to [Lab 1](../lab-01/) |
| Scenario validation **PASS** | Use same file in Labs 4–6 via `--scenario` |
| Robot section **PASS** | DDS + sport OK; ready for [Lab 2](../lab-02/) motion |

---

## Deliverable

- Log snippet: `lab00_day2_readiness.py` → machine **PASS**
- Your `my_team_scenario.json` (validated)
- One sentence: what your team will inspect in the arena

**Next:** [Lab 1 — run folder schema](../lab-01/)
