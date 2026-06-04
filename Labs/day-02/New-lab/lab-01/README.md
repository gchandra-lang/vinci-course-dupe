# Lab 1 — Run Folder Schema & Bundle Validation

**Duration:** ~45 min  
**Robot motion:** None  
**Prerequisites:** [Lab 0](../lab-00/) complete (`my_team_scenario.json` validated)

**PDF coverage:** Managing sensor data · inspection task design (data layout)

---

## Learning objectives

1. Describe the **Day 2 run folder** layout and how it extends the Day 1 single-checkpoint bundle.
2. Author **`metadata.json`** and **`patrol_plan.json`** that Lab 3’s runner will consume.
3. Validate a run directory with **`lab01_validate_run_folder.py`** (PASS / FAIL).
4. Scaffold a dry-run folder from your **Lab 0 scenario** with **`lab01_scaffold_run_folder.py`**.

---

## 1. Concepts

### Day 1 bundle vs Day 2 run folder

| | Day 1 (`lab03_capture_inspection.py`) | Day 2 (patrol run) |
|--|--------------------------------------|---------------------|
| **Scope** | One checkpoint | Many checkpoints + legs |
| **Image** | `frame_001.jpg` at root | `checkpoints/<id>/frame.jpg` |
| **Plan** | Notes in `metadata.json` only | **`patrol_plan.json`** (legs + dwell) |
| **State log** | Short `sportmodestate.jsonl` | Full-patrol JSONL (+ optional per-CP slices) |

```text
run_YYYYMMDD_HHMM/
  metadata.json           # who, when, robot, CheckMode, checkpoint id list
  patrol_plan.json        # checkpoints + legs (increment / velocity)
  sportmodestate.jsonl    # one JSON object per line (DDS-style log)
  checkpoints/
    cp_A/
      frame.jpg           # front camera at this stop
      state_slice.jsonl   # optional — window around capture
    cp_B/
      ...
```

Treat this folder as the **inspection deliverable** for Day 2–5 presentations.

### `metadata.json` (required fields)

| Field | Purpose |
|-------|---------|
| `schema_version` | Camp format version (`1`) |
| `created_utc` | ISO-8601 timestamp |
| `operator` | Human or team operator |
| `team_name` | Optional — from scenario |
| `interface` | NIC used on hardware run (`en6`, …) |
| `checkpoints` | List of checkpoint ids (should match plan) |
| `check_mode` | From `MotionSwitcherClient` on capture (Lab 3) |
| `artifacts` | Map of filenames in this folder |

### `patrol_plan.json`

| Section | Purpose |
|---------|---------|
| `checkpoints[]` | `id`, `label`, `dwell_s` (seconds stopped before capture) |
| `legs[]` | Motion between stops |

**Leg types** (Lab 2–3):

| `type` | Meaning |
|--------|---------|
| `increment` | `ObstaclesAvoidClient.MoveToIncrementPosition(dx, dy, dyaw)` |
| `velocity` | Timed `Move(vx, vy, vyaw)` at ~20 Hz (Lab 4 tuning) |
| `dwell` | Wait at checkpoint (often folded into `dwell_s` on checkpoint) |

Template: [`patrol_plan.template.json`](patrol_plan.template.json)

### `sportmodestate.jsonl`

Same line format as [Day 1 Lab 1](../../day-01/lab-02/) / Lab 3 — one JSON object per line, e.g.:

```json
{"t": 1716712345.1, "mode": 9, "gait_type": 1, "error_code": 0, "body_height": 0.32, "velocity": [0.1, 0.0, 0.0]}
```

Validators require **at least one** valid line; patrol runs should have many.

---

## 2. Scripts

### `lab01_validate_run_folder.py`

| Argument | Purpose |
|----------|---------|
| `run_dir` | Folder to check |
| `--scenario PATH` | Cross-check checkpoint ids with Lab 0 scenario |
| `--relax-images` | Allow missing `frame.jpg` (scaffold / dry-run) |

```bash
cd /path/to/vinci-unitree

# Instructor fixture — should PASS
python course/day-02/New-lab/lab-01/lab01_validate_run_folder.py \
  course/day-02/New-lab/lab-01/fixtures/sample_run_pass

# Broken fixture — should FAIL (exercise)
python course/day-02/New-lab/lab-01/lab01_validate_run_folder.py \
  course/day-02/New-lab/lab-01/fixtures/sample_run_incomplete

# Your scaffold
python course/day-02/New-lab/lab-01/lab01_validate_run_folder.py ./run_XXXX --relax-images \
  --scenario course/day-02/New-lab/lab-00/my_team_scenario.json
```

### `lab01_scaffold_run_folder.py`

Builds a new run directory from your Lab 0 scenario (no images).

```bash
python course/day-02/New-lab/lab-01/lab01_scaffold_run_folder.py \
  course/day-02/New-lab/lab-00/my_team_scenario.json

python course/day-02/New-lab/lab-01/lab01_scaffold_run_folder.py \
  course/day-02/New-lab/lab-00/my_team_scenario.json \
  --out-dir ./run_dry_team_a --increment-dx 0.4
```

---

## 3. Hands-on

### Step 1 — Validate the passing fixture

```bash
conda activate unitree_env
cd /path/to/vinci-unitree

python course/day-02/New-lab/lab-01/lab01_validate_run_folder.py \
  course/day-02/New-lab/lab-01/fixtures/sample_run_pass
```

**Expected:** `Summary: PASS — run folder valid`

Open the fixture and map files to the diagram in Section 1.

### Step 2 — Find failures in the incomplete fixture

```bash
python course/day-02/New-lab/lab-01/lab01_validate_run_folder.py \
  course/day-02/New-lab/lab-01/fixtures/sample_run_incomplete
```

**Expected:** multiple `FAIL` lines (missing `sportmodestate.jsonl`, incomplete metadata, missing `checkpoints/`, …).

In your notebook, list each error and which file you would add or fix.

### Step 3 — Scaffold from your scenario

```bash
python course/day-02/New-lab/lab-01/lab01_scaffold_run_folder.py \
  course/day-02/New-lab/lab-00/my_team_scenario.json \
  --out-dir ./run_dry_$(whoami)
```

```bash
python course/day-02/New-lab/lab-01/lab01_validate_run_folder.py ./run_dry_$(whoami) \
  --relax-images \
  --scenario course/day-02/New-lab/lab-00/my_team_scenario.json
```

**Expected:** PASS with warnings about missing images (OK until Lab 3).

### Step 4 — Optional: migrate a Day 1 bundle

If you have `inspection_capture_*` from Day 1 Lab 3:

1. Create `checkpoints/cp_A/` (use your first scenario checkpoint id).
2. Copy `frame_001.jpg` → `checkpoints/cp_A/frame.jpg`.
3. Copy `sportmodestate.jsonl` to run root.
4. Add `patrol_plan.json` (one checkpoint, empty `legs`).
5. Extend `metadata.json` with `"schema_version": 1` and `"checkpoints": ["cp_A"]`.
6. Re-run the validator.

---

## 4. Exercises

1. Add a third checkpoint to `patrol_plan.json` in your scaffold **without** creating directories — run validator (with and without `--relax-images`). What fails first?
2. Add an invalid JSON line to `sportmodestate.jsonl` — confirm the validator reports the line number.
3. Write one sentence: what an inspector learns from **`metadata.json`** vs **`patrol_plan.json`**.

---

## 5. Deliverable

Submit:

1. Log: `lab01_validate_run_folder.py fixtures/sample_run_pass` → **PASS**
2. Log: `lab01_validate_run_folder.py fixtures/sample_run_incomplete` → **FAIL** (paste error list)
3. Path to your **`run_dry_*`** folder + validator output with `--relax-images`
4. Copy of your **`patrol_plan.json`** (or diff from template)

---

## 6. Next lab

**[Lab 2 — Multi-leg patrol (increment goals)](../lab-02/)**  
Supervised motion between checkpoints with `ObstaclesAvoidClient`.

---

## References

- Day 2 overview: [`../README.md`](../README.md)
- Lab 0 scenario: [`../lab-00/patrol_scenario.template.json`](../lab-00/patrol_scenario.template.json)
- Day 1 capture: [`../../day-02/lab-03/lab03_capture_inspection.py`](../../day-02/lab-03/lab03_capture_inspection.py)
- Scripts: [`lab01_validate_run_folder.py`](lab01_validate_run_folder.py) · [`lab01_scaffold_run_folder.py`](lab01_scaffold_run_folder.py)
