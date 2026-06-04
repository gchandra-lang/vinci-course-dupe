# Lab 1 — Patrol run folder & validator

| | |
|--|--|
| **Duration** | ~40–50 min |
| **Motion** | No |
| **Robot** | No |
| **Prerequisite** | [Lab 0](../lab-00/) scenario JSON |

---

## What you will learn

- The **run folder** layout your team must produce after a patrol (`metadata.json`, `patrol_plan.json`, `sportmodestate.jsonl`, checkpoint images).
- How the instructor **validator** checks completeness before presentations.
- How to **scaffold** a dry-run folder from your scenario without moving the robot.

---

## What you will run

| Script | Purpose |
|--------|---------|
| [`lab01_validate_run_folder.py`](lab01_validate_run_folder.py) | Check a run directory against schema |
| [`lab01_scaffold_run_folder.py`](lab01_scaffold_run_folder.py) | Create empty/partial run tree from scenario |
| `fixtures/sample_run_pass/` | Example that should **PASS** |
| `fixtures/sample_run_incomplete/` | Example that should **FAIL** |

---

## Steps

### 1. Study a passing fixture

```bash
python3 course/student/day-02/lab-01/lab01_validate_run_folder.py \
  course/student/day-02/lab-01/fixtures/sample_run_pass
```

Read `metadata.json`, `patrol_plan.json`, and one line of `sportmodestate.jsonl` (same JSONL style as [Day 1 Lab 3](../../day-01/lab-03/)).

### 2. See a failing fixture

```bash
python3 course/student/day-02/lab-01/lab01_validate_run_folder.py \
  course/student/day-02/lab-01/fixtures/sample_run_incomplete
```

Note which checks fail (missing images, metadata, etc.).

### 3. Scaffold your team dry-run folder

```bash
python3 course/student/day-02/lab-01/lab01_scaffold_run_folder.py \
  ../lab-00/my_team_scenario.json --out-dir ./run_dry_$(whoami)
```

### 4. Validate with your scenario

```bash
python3 course/student/day-02/lab-01/lab01_validate_run_folder.py ./run_dry_$(whoami) \
  --relax-images \
  --scenario ../lab-00/my_team_scenario.json
```

`--relax-images` allows missing photos until you run a real patrol in Lab 5.

---

## Expected results

| Command | PASS means |
|---------|------------|
| `sample_run_pass` | You understand the target layout |
| `sample_run_incomplete` | Non-zero exit — expected |
| Scaffold + validate | Folder structure OK; images optional with `--relax-images` |

---

## Deliverable

- Screenshot or log: validator **PASS** on `sample_run_pass`
- Your `./run_dry_*` path noted for Lab 5

**Next:** [Lab 2 — obstacle avoid intro](../lab-02/)
