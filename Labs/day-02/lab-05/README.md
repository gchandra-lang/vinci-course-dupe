# Lab 3 — Integrated Patrol Runner & Checkpoint Capture

**Duration:** ~75–90 min  
**Robot motion:** **Yes** — Lab 2 patrol + stop to capture images  
**Prerequisites:** [Lab 2](../lab-02/) on hardware · [Lab 1](../lab-01/) run-folder schema

**PDF coverage:** Autonomous inspection routines · managing sensor data (full run bundle)

---

## Learning objectives

1. Run **patrol + logging + camera** in one script (`lab03_patrol_runner.py`).
2. Produce a complete **run folder** valid for `lab01_validate_run_folder.py`.
3. Relate **checkpoint capture** to virtual plan IDs (still not vision-based navigation).
4. Inspect `metadata.json`, `sportmodestate.jsonl`, and per-checkpoint `frame.jpg`.

---

## 1. Concepts

### What Lab 3 adds to Lab 2

| Lab 2 | Lab 3 |
|-------|--------|
| Motion only | Motion + **data product** |
| Console PASS | **`run_YYYYMMDD_HHMM/`** on disk |
| — | `VideoClient` at **cp_A** (start) and after **each leg** at `to_checkpoint` |
| — | Continuous **`sportmodestate.jsonl`** during patrol |

Navigation is still **open loop** from `patrol_plan.json`. The camera records **what the dog saw when stopped** — it does not steer toward cone colors.

### Run folder (output)

```text
run_20260526T120000Z/
  metadata.json
  patrol_plan.json          # copy of input plan
  sportmodestate.jsonl
  checkpoints/
    cp_A/frame.jpg
    cp_A/state_slice.jsonl    # optional tail of state log
    cp_B/frame.jpg
    cp_C/frame.jpg
```

---

## 2. Script — `lab03_patrol_runner.py`

| Flag | Purpose |
|------|---------|
| `en6` | Ethernet interface |
| `--plan PATH` | Default: [`../lab-04/patrol_plan.cone_course.json`](../lab-04/patrol_plan.cone_course.json) |
| `--out-dir PATH` | Run root (default `run_<UTC>/`) |
| `--scenario PATH` | Clamp legs to Lab 0 limits |
| `--dry-run` | Print sequence only |
| `--no-capture` | Patrol without camera (debug motion) |
| `--validate` | Run Lab 1 validator after patrol |
| `--camera-wait SEC` | Max wait per frame (default 15) |
| `--state-log-hz` | JSONL rate (default 5) |
| Lab 2 flags | `--leg-wait`, `--leg-pulses`, `--leg-hz`, `--stream-increment`, `--skip-stand`, `-y` |

Shared helpers: [`../go2_patrol_helpers.py`](../go2_patrol_helpers.py)

---

## 3. Hands-on

### Step 0 — Session

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/vinci-unitree
```

### Step 1 — Dry-run

```bash
python course/day-02/lab-05/lab03_patrol_runner.py en6 --dry-run
```

### Step 2 — Full patrol + capture

```bash
python course/day-02/lab-05/lab03_patrol_runner.py en6 -y --validate
```

**Expected sequence:**

1. Stand up  
2. Capture **cp_A** (start)  
3. Patrol legs (forward, turn, forward — default L-plan)  
4. After each leg: capture at **`to_checkpoint`** (cp_B may be captured twice after turn leg)  
5. Write `metadata.json` + validator **PASS**

### Step 3 — Inspect artifacts

```bash
RUN=run_XXXXX   # your folder
ls -R "$RUN"
open "$RUN/checkpoints/cp_A/frame.jpg"    # macOS
head -3 "$RUN/sportmodestate.jsonl"
cat "$RUN/metadata.json"
```

### Step 4 — Validate manually

```bash
python course/day-02/lab-01/lab01_validate_run_folder.py "$RUN"
```

---

## 4. Exercises

1. Run with `--no-capture` then compare time and behaviour vs full run.  
2. Open three `frame.jpg` files — what changed between cp_A and cp_C?  
3. One sentence: what an inspector learns from images that JSONL alone does not provide.

---

## 5. Deliverable

Submit:

1. Path to your **`run_*`** folder  
2. Validator log → **PASS** (or explain missing frames)  
3. One **`frame.jpg`** screenshot in your report (any checkpoint)  
4. One line from `metadata.json` (`check_mode`, `checkpoints`)

---

## 6. Troubleshooting

| Issue | Check |
|-------|--------|
| No `frame.jpg` | `VideoClient` / robot video service; increase `--camera-wait` |
| Validator FAIL | Re-run with `--validate`; ensure captures succeeded |
| Same as Lab 2 motion | Expected — plan unchanged; only adds capture pauses |
| Capture slow | Normal — dog must be settled; dwell before capture helps |

---

## 7. Next lab

**[Lab 6 — Field trial & tuning](../lab-04/)**  
Formal test plan, tuning notes, and debrief.

---

## References

- [`lab03_patrol_runner.py`](lab03_patrol_runner.py)
- Lab 2: [`../lab-02/`](../lab-02/) · Lab 1: [`../lab-01/`](../lab-01/)
- Day 1 capture: [`../../day-02/lab-03/`](../../day-02/lab-03/)
