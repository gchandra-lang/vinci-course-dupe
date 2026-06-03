# Lab 4 — Multi-checkpoint increment patrol

| | |
|--|--|
| **Duration** | ~40–50 min |
| **Motion** | **Yes** |
| **Robot** | **Required** |
| **Prerequisite** | [Labs 0–2](../lab-02/); scenario JSON from [Lab 0](../lab-00/) |

---

## What you will learn

- How a **`patrol_plan.json`** lists checkpoints and **legs** (`increment` or `velocity`).
- How the dog executes **several avoid legs** in one script (preview of full patrol without camera logging).
- How **`--scenario`** clamps speeds to your team limits from Lab 0.

---

## What you will run

| File | Role |
|------|------|
| [`lab04_increment_patrol.py`](lab04_increment_patrol.py) | Run all legs in a plan |
| [`patrol_plan.cone_course.json`](patrol_plan.cone_course.json) | Default 3-checkpoint cone course |

Shared: [`../go2_patrol_helpers.py`](../go2_patrol_helpers.py).

---

## Steps

### 1. Inspect the default plan

```bash
cat course/student/day-02/lab-04/patrol_plan.cone_course.json
```

Note `checkpoints` and `legs` with `to_checkpoint` IDs matching your scenario.

### 2. Dry-run

```bash
python course/student/day-02/lab-04/lab04_increment_patrol.py $GO2_INTERFACE --dry-run
```

### 3. Live patrol (default plan)

```bash
python course/student/day-02/lab-04/lab04_increment_patrol.py $GO2_INTERFACE -y \
  --scenario ../lab-00/my_team_scenario.json
```

### 4. Tune leg timing (if legs undershoot)

```bash
python course/student/day-02/lab-04/lab04_increment_patrol.py $GO2_INTERFACE -y \
  --leg-wait 10 --plan patrol_plan.cone_course.json
```

---

## Expected results

| Step | PASS |
|------|------|
| Dry-run | Lists each leg and dwell |
| Live | Dog completes legs; avoid released at end |
| Scenario clamp | WARN lines if plan exceeded limits (then clamped) |

---

## Deliverable

- Log showing all legs executed  
- Note which checkpoint needed longer `--leg-wait` (feeds Lab 6 tuning)  

**Next:** [Lab 5 — full patrol + run folder](../lab-05/)
