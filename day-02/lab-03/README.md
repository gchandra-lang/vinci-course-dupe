# Lab 3 — Inspection capture & platform probe

| | |
|--|--|
| **Duration** | ~35–45 min |
| **Motion** | No sustained patrol (capture only) |
| **Robot** | **Required** |
| **Prerequisite** | [Lab 2](../lab-02/); Day 1 [Lab 3](../../day-01/lab-03/) |

---

## What you will learn

- How **`VideoClient`** saves a front-camera frame for a checkpoint folder.
- How to bundle **metadata + image + optional state log** for one inspection stop.
- How **`lab03_platform_probe.py`** reports lidar switch, VUI, and robot state (read-only).

---

## What you will run

| Script | Motion? | Focus |
|--------|---------|--------|
| [`lab03_capture_inspection.py`](lab03_capture_inspection.py) | No walk | Save `frame.jpg` + sidecar JSON |
| [`lab03_platform_probe.py`](lab03_platform_probe.py) | No | Lidar on/off, JSON probe export |

---

## Steps

### 1. Platform probe (read-only)

```bash
python3 course/student/day-02/lab-03/lab03_platform_probe.py $GO2_INTERFACE
python3 course/student/day-02/lab-03/lab03_platform_probe.py $GO2_INTERFACE --json-out probe.json
```

Optional: `--lidar on` to exercise lidar switch (arena policy permitting).

### 2. Single checkpoint capture

```bash
python3 course/student/day-02/lab-03/lab03_capture_inspection.py $GO2_INTERFACE \
  --out-dir ./checkpoint_test \
  --operator "$(whoami)"
```

Inspect `./checkpoint_test/` for image + metadata.

### 3. Optional GUI preview

```bash
python3 course/student/day-02/lab-03/lab03_capture_inspection.py $GO2_INTERFACE --gui
```

Requires display; skip on headless SSH.

### 4. Tie-in to Lab 5

Lab 5 calls the same capture path **after each patrol leg**. If capture fails here, fix before Lab 5.

---

## Expected results

| Script | PASS |
|--------|------|
| `platform_probe` | RPC OK; JSON lists services / lidar state |
| `capture_inspection` | `frame.jpg` (or documented fail) + metadata under `--out-dir` |

---

## Deliverable

- `probe.json` or terminal log from platform probe  
- One capture folder path with a visible `frame.jpg`  

**Next:** [Lab 4 — multi-leg increment patrol](../lab-04/)
