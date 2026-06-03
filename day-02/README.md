# Day 2 — Go2 inspection & patrol capstone

**Platform:** Unitree **Go2**  
**Path:** `course/student/day-02/` (all labs below)  
**Stack:** Python SDK (`unitree_sdk2_python`) on Ethernet · optional **Gazebo** block uses ROS 2 `/cmd_vel`

**Prerequisite:** [Day 1](../day-01/) in the same `course/student/` tree — not `course/day-*` or `New-lab`.

---

## Are you ready to start Day 2?

Complete **Day 1** first, then run the Day 2 gate script (no motion):

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/vinci-unitree

python course/student/day-02/lab-00/lab00_day2_readiness.py
```

| Day 1 (student) | Required before | Why |
|-----------------|-----------------|-----|
| [Lab 0](../day-01/lab-00/) `lab00_readiness.py` | **Yes** | SDK + optional robot ping |
| [Lab 3](../day-01/lab-03/) `lab03_listen_sportmodestate.py` | **Yes** | DDS logging for patrol |
| [Lab 4](../day-01/lab-04/) `lab04_sport_readonly.py` | **Yes** | `CheckMode` / RPC readiness |
| [Lab 5](../day-01/lab-05/) `lab05_safe_posture.py` | **Yes** | First **visible** stand + walk |
| Labs 1–2, 6–9 (ROS) | Recommended | RViz, rqt, pub/sub — needed for [Gazebo](gazebo/) only |

If Lab 5 never passed on hardware, **do not** run Day 2 motion labs (2, 4, 5, 6). Fix networking with [`go2_network_helpers.py`](../day-01/go2_network_helpers.py) and [`docs/GO2-FIELD-GUIDE.md`](../../../docs/GO2-FIELD-GUIDE.md).

**NIC:** `export GO2_INTERFACE=<your-enx-or-enp>` (from `ip -br addr` on `192.168.123.x`).

---

## What this day is for

Day 1 taught **connect, observe, and move once**. Day 2 chains those skills into a **supervised inspection patrol** in a cleared arena:

1. **Plan** — scenario JSON + run-folder schema  
2. **Move safely** — obstacle-avoid legs between waypoints  
3. **Record** — camera frames + `sportmodestate` JSONL per checkpoint  
4. **Integrate** — one script runs the full patrol and writes a deliverable folder  
5. **Present** — team capstone with evidence (Lab 7)

This is **scripted patrol** with avoid API and logging — **not** full SLAM/Nav2 autonomy. Concepts from the morning lecture (SLAM, fusion) apply to the architecture story; the camp scripts stay SDK-based on the real dog.

---

## Two parallel tracks (same day)

| Track | Folder | Robot |
|-------|--------|-------|
| **A — Field SDK** | `lab-00` … `lab-07` | Go2 on Ethernet |
| **B — Gazebo sim** | [`gazebo/`](gazebo/) | None (sim) |

Track B is optional if Gazebo is installed; Track A is the **main learning path**. Field labs 4–6 still use the **Python SDK**, not `/cmd_vel`, on hardware.

Install: [`docs/GAZEBO-GO2.md`](../../../docs/GAZEBO-GO2.md) · scripts `install_gazebo_go2.sh`, `run_gazebo_go2.sh`.

---

## Lab sequence (field track)

Do labs **in order** the first time; later labs assume artifacts from earlier ones.

| Lab | Folder | Motion? | You will |
|-----|--------|---------|----------|
| **0** | [`lab-00/`](lab-00/) | No | Gate check, patrol **scenario** JSON, safety rules |
| **1** | [`lab-01/`](lab-01/) | No | **Run folder** layout, validator, sample fixtures |
| **2** | [`lab-02/`](lab-02/) | **Yes** | `lab02_obstacle_avoid_intro.py` — avoid forward leg |
| **3** | [`lab-03/`](lab-03/) | No* | Front **camera** bundle, platform/lidar **probe** |
| **4** | [`lab-04/`](lab-04/) | **Yes** | **Multi-checkpoint** increment patrol (preview) |
| **5** | [`lab-05/`](lab-05/) | **Yes** | Full **`lab05_patrol_runner.py`** + run directory |
| **6** | [`lab-06/`](lab-06/) | **Yes** | Field trial, plan **tuning**, tuned JSON |
| **7** | [`lab-07/`](lab-07/) | Team | **Presentation** rubric & scenarios |

\*Lab 3 may open a GUI (`--gui`); default capture is still no sustained walking.

### Minimum path (timeboxed class)

If you are short on time, still do: **0 → 1 → 2 → 5 (dry-run) → 7** with instructor sample run folder. Add 3–4–6 when hardware time allows.

### Commands cheat sheet (robot on)

Set `export GO2_INTERFACE=<nic>` (see Day 1). Each lab README has full steps.

```bash
# After Lab 0 scenario file exists in lab-00/
python course/student/day-02/lab-02/lab02_obstacle_avoid_intro.py $GO2_INTERFACE --dry-run
python course/student/day-02/lab-02/lab02_obstacle_avoid_intro.py $GO2_INTERFACE -y

python course/student/day-02/lab-03/lab03_capture_inspection.py $GO2_INTERFACE --out-dir ./checkpoint_test

python course/student/day-02/lab-04/lab04_increment_patrol.py $GO2_INTERFACE --dry-run
python course/student/day-02/lab-05/lab05_patrol_runner.py $GO2_INTERFACE --dry-run
python course/student/day-02/lab-05/lab05_patrol_runner.py $GO2_INTERFACE -y --validate

python course/student/day-02/lab-01/lab01_validate_run_folder.py ./run_team_a --relax-images
```

---

## Shared code (student tree)

| Module | Location | Used by |
|--------|----------|---------|
| `go2_patrol_helpers.py` | this folder | Labs 4–6 |
| `go2_motion_helpers.py` | [`../day-01/`](../day-01/) | Labs 2, 4, 5 (stand prep) |
| `go2_network_helpers.py` | [`../day-01/`](../day-01/) | Optional; Day 2 scripts take iface arg |

Repo install scripts (unchanged): [`scripts/`](../../../scripts/) — `go2_connection_check.py`, `setup_unitree_sdk.sh`.

---

## Lab 7 — team capstone (pick one)

| # | Scenario | Must demonstrate |
|---|----------|------------------|
| 1 | Corridor patrol | ≥ 3 checkpoints; image + SOC in `metadata.json` |
| 2 | Anomaly abort | Stop + `incident.json` on SOC or rate rule |
| 3 | Return-to-base | Final leg toward start (supervised) |
| 4 | Post-run report | JSONL → summary table or CSV |

Details: [`lab-07/README.md`](lab-07/README.md).

---

## Status

| Item | Notes |
|------|--------|
| Labs 0–6 | Ready — paths under `course/student/day-02/` |
| Lab 7 | Rubric + scenarios; team deliverable |
| [`gazebo/`](gazebo/) | Labs 1–2 ready when Gazebo workspace built |

---

## Troubleshooting

| Symptom | Check |
|---------|--------|
| `ModuleNotFoundError: go2_motion_helpers` | Run from repo root; keep [`../day-01/go2_motion_helpers.py`](../day-01/go2_motion_helpers.py) |
| Avoid on, dog does not move | Lab 2 README — `UseRemoteCommandFromApi`, stand prep, clear arena |
| Empty run folder after patrol | Lab 5 `-y`, plan path, write permissions on `--out-dir` |
| Validator fails | Lab 1 — compare to `fixtures/sample_run_pass/` |

Field guide: [`docs/GO2-FIELD-GUIDE.md`](../../../docs/GO2-FIELD-GUIDE.md)

---

**Previous:** [Day 1 — ROS vs SDK](../day-01/) · **Gazebo:** [extension labs](gazebo/)
