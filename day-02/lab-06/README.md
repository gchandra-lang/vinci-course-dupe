# Lab 6 — Tune plan & field trial

| | |
|--|--|
| **Duration** | ~40–50 min |
| **Motion** | Yes (field trial script) |
| **Robot** | **Required** for field trial |
| **Prerequisite** | [Lab 5](../lab-05/) at least one run (or baseline run id) |

---

## What you will learn

- How to **adjust leg parameters** offline (`lab06_tune_plan.py`) after watching Lab 4/5.
- How to run a **documented field trial**: tuned plan → patrol → `field_test.md` report.
- How teams record **checkpoint pass/partial** results for Lab 7.

---

## What you will run

| Script | Robot? | Output |
|--------|--------|--------|
| [`lab06_tune_plan.py`](lab06_tune_plan.py) | No | `patrol_plan.tuned.json` |
| [`lab06_field_trial.py`](lab06_field_trial.py) | Yes | New `run_*` + `field_test.md` |

Templates: `field_test.template.md`, `tuning_notes.template.json`.

---

## Steps

### 1. Tune plan (desk)

After observing legs that were short or long:

```bash
python course/student/day-02/lab-06/lab06_tune_plan.py \
  ../lab-04/patrol_plan.cone_course.json \
  --out ../lab-04/patrol_plan.tuned.json \
  --leg 1 --dyaw 0.7 --leg 2 --dx 0.25
```

### 2. Field trial (robot)

```bash
python course/student/day-02/lab-06/lab06_field_trial.py $GO2_INTERFACE -y \
  --plan ../lab-04/patrol_plan.tuned.json \
  --baseline-run run_20260526T132200Z \
  --cp-results cp_A:pass,cp_B:partial,cp_C:pass \
  --notes "Adjusted dyaw on leg 1"
```

Replace `baseline-run` with your Lab 5 folder name.

### 3. Review report

Open `field_test.md` in the new run folder; attach to team slides for [Lab 7](../lab-07/).

---

## Expected results

| Step | PASS |
|------|------|
| Tune | Writes `patrol_plan.tuned.json`; prints next command |
| Field trial | Invokes `lab05_patrol_runner.py`; validator run; `field_test.md` filled |

Use `--skip-patrol` only if reusing an existing run dir for report writing practice.

---

## Deliverable

- `patrol_plan.tuned.json`  
- One field-trial `run_*` + `field_test.md`  

**Next:** [Lab 7 — presentation](../lab-07/)
