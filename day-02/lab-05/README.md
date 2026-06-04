# Lab 5 — Integrated patrol runner

| | |
|--|--|
| **Duration** | ~45–60 min |
| **Motion** | **Yes** |
| **Robot** | **Required** |
| **Prerequisite** | [Labs 1–4](../lab-04/); [Lab 1](../lab-01/) validator understood |

---

## What you will learn

- How **one script** runs avoid legs, logs **`sportmodestate.jsonl`**, captures **per-checkpoint images**, and writes **`metadata.json`**.
- How to produce a **team run folder** that passes [`lab01_validate_run_folder.py`](../lab-01/lab01_validate_run_folder.py).
- This is the **main field deliverable** for Day 2.

---

## What you will run

| Script | Role |
|--------|------|
| [`lab05_patrol_runner.py`](lab05_patrol_runner.py) | Full patrol + run directory |

Default plan: `../lab-04/patrol_plan.cone_course.json`.

---

## Steps

### 1. Dry-run (plan + capture sequence)

```bash
python course/student/day-02/lab-05/lab05_patrol_runner.py $GO2_INTERFACE --dry-run \
  --scenario ../lab-00/my_team_scenario.json
```

### 2. Live run with validation

```bash
python course/student/day-02/lab-05/lab05_patrol_runner.py $GO2_INTERFACE -y --validate \
  --scenario ../lab-00/my_team_scenario.json \
  --out-dir ./run_$(date -u +%Y%m%dT%H%M%SZ)
```

### 3. Inspect output

```bash
ls -la ./run_*/
python course/student/day-02/lab-01/lab01_validate_run_folder.py ./run_* --scenario ../lab-00/my_team_scenario.json
```

### 4. Useful flags

| Flag | Use |
|------|-----|
| `--no-capture` | Motion/debug only |
| `--operator "Team A"` | Metadata |
| `--state-log-hz 5` | JSONL rate |

---

## Expected results

| Output | PASS |
|--------|------|
| `sportmodestate.jsonl` | Non-empty after patrol |
| `checkpoints/*/frame.jpg` | Image per checkpoint (unless `--no-capture`) |
| `metadata.json` | Operator, plan path, mode info |
| `--validate` | Validator exit 0 |

Exit **2** = partial (some captures failed); motion may still have completed.

---

## Deliverable

- One **`run_*`** folder that validates (or instructor-approved dry-run + sample pass fixture for Lab 7)

**Next:** [Lab 6 — field trial & tuning](../lab-06/)
