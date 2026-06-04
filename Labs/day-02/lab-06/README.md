# Lab 4 — Field Trial & Tuning

**Duration:** ~60 min  
**Robot motion:** **Yes** — re-run patrol with a **tuned** plan  
**Prerequisites:** [Lab 5](../lab-05/) produced at least one baseline `run_*` folder

**PDF coverage:** Field testing · troubleshooting · performance tuning

---

## Learning objectives

1. Turn field observations (short leg, weak turn, wall) into **`patrol_plan.json` edits**.
2. Run a **second patrol** with the tuned plan via Lab 3.
3. Produce **`field_test.md`** in the run folder for inspection sign-off.
4. Compare baseline vs field-trial runs (motion + captures).

---

## 1. Concepts

### Tune → trial → report

```text
Observe (Lab 2/3)  →  lab04_tune_plan.py  →  patrol_plan.tuned.json
                              ↓
                    lab04_field_trial.py  →  lab03_patrol_runner (motion + capture)
                              ↓
                         run_field_* / field_test.md
```

| Symptom | Typical tune |
|---------|----------------|
| Stops short of cone | Increase leg `dx` or `--leg-wait` on Lab 3 |
| Overshoots / hits wall | Decrease final leg `dx` |
| Turn too small | Increase turn leg `dyaw` |
| Turn too large | Decrease `dyaw` |

Tuning is still **open loop** — you are calibrating metres/radians, not using the camera to steer.

---

## 2. Scripts & templates

| File | Robot? | Purpose |
|------|--------|---------|
| [`lab04_tune_plan.py`](lab04_tune_plan.py) | No | Copy plan + apply `--leg N --dx` / `--dyaw` overrides |
| [`lab04_field_trial.py`](lab04_field_trial.py) | Yes | Run Lab 3 + write `field_test.md` |
| [`patrol_plan.tuned.json`](patrol_plan.tuned.json) | — | Example tuned plan (dyaw 0.7, final dx 0.25) |
| [`tuning_notes.template.json`](tuning_notes.template.json) | — | Document symptoms/changes |
| [`field_test.template.md`](field_test.template.md) | — | Manual checklist / sign-off |

---

## 3. Hands-on

### Step 1 — Review baseline (Lab 3)

Use your last Lab 3 folder, e.g. `run_20260526T132200Z`:

```bash
ls -R run_20260526T132200Z
open run_20260526T132200Z/checkpoints/cp_A/frame.jpg
open run_20260526T132200Z/checkpoints/cp_C/frame.jpg
```

Note: leg distances, turn angle, wall clearance.

### Step 2 — Tune the plan (no robot)

From repo root:

```bash
python course/day-02/lab-06/lab04_tune_plan.py \
  course/day-02/lab-02/patrol_plan.cone_course.json \
  --out course/day-02/lab-04/patrol_plan.tuned.json \
  --set 1:dyaw:0.7 \
  --set 2:dx:0.25
```

Or edit [`patrol_plan.tuned.json`](patrol_plan.tuned.json) by hand.

### Step 3 — Field trial run

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/vinci-unitree

python course/day-02/lab-06/lab04_field_trial.py en6 -y \
  --plan course/day-02/lab-04/patrol_plan.tuned.json \
  --baseline-run run_20260526T132200Z \
  --cp-results cp_A:pass,cp_B:partial,cp_C:pass \
  --notes "Stronger turn; shorter final leg to stay off wall"
```

**Expected:**

- Full Lab 3 patrol (motion + captures) into `run_field_<UTC>/`
- `field_test.md` inside that folder
- Validator **PASS**

Adjust `--cp-results` to match what you actually saw (`pass` / `partial` / `fail`).

### Step 4 — Debrief (team)

Fill remaining items in [`field_test.template.md`](field_test.template.md) if your instructor requires manual sign-off.

| Question | Discuss |
|----------|---------|
| Did tuned run fix the main issue? | |
| One change you would try next | |
| What Lab 5 scenario fits your data? | |

---

## 4. Flags reference — `lab04_field_trial.py`

| Flag | Purpose |
|------|---------|
| `--plan` | Tuned `patrol_plan.json` |
| `--baseline-run` | Lab 3 run path for report table |
| `--cp-results` | `cp_A:pass,cp_B:partial,...` |
| `--notes` | Free text in `field_test.md` |
| `--out-dir` | Force run folder name |
| `--dry-run` | Plan check only |
| `--skip-patrol` | Write report for an existing run folder |

---

## 5. Deliverable

Submit:

1. `patrol_plan.tuned.json` (or diff from cone course)  
2. `run_field_*` folder path + validator **PASS**  
3. `run_field_*/field_test.md`  
4. One sentence: what you tuned and whether it helped  

---

## 6. Next lab

**[Lab 5 — Mini-project](../lab-05/)**  
Team scenario, presentation, and polished run evidence.

---

## References

- Lab 3: [`../lab-05/lab03_patrol_runner.py`](../lab-05/lab03_patrol_runner.py)
- Field guide: [`docs/GO2-FIELD-GUIDE.md`](../../../docs/GO2-FIELD-GUIDE.md)
