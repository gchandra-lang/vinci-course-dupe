# Day 2 — Go2 Autonomy & Sandbox Capstone

> **Experimental track:** Full **Gazebo Go2** labs and updated patrol scripts are under [`New-lab/`](New-lab/) (see [`NOTICE.md`](New-lab/NOTICE.md)). Root `lab-*` folders match **main**; `extension/gazebo/` here is still the thin scaffold.

**Platform:** Unitree **GO2**  
**Stack:** Python SDK + optional **Gazebo** / ROS 2 (AM) · patrol pipeline (PM)

**Prerequisite:** [Day 1](../day-01/) Labs 0–3 (DDS + sport RPC).

**Schedule:** [`SCHEDULE-TTT.md`](../SCHEDULE-TTT.md)

---

## What this day is for

Turn Day 1 skills into **inspection autonomy**: SLAM/planning concepts, **obstacle avoidance**, **sensor capture**, optional **simulation**, then **field patrol** and **team presentations**.

---

## Lab sequence

| Lab | Folder | Motion? | TtT block | Focus |
|-----|--------|---------|-----------|--------|
| **0** | [`lab-00/`](lab-00/) | No | Open | Day 2 readiness, scenario JSON |
| **1** | [`lab-01/`](lab-01/) | No | AM prep | Run folder schema & validation |
| **2** | [`lab-02/`](lab-02/) | **Yes** | 10:45 | `lab04_obstacle_avoid_intro.py` |
| **3** | [`lab-03/`](lab-03/) | No* | AM | Camera bundle, platform probe |
| **4** | [`lab-04/`](lab-04/) | **Yes** | AM | Increment patrol |
| **5** | [`lab-05/`](lab-05/) | **Yes** | PM | Integrated `lab03_patrol_runner.py` |
| **6** | [`lab-06/`](lab-06/) | **Yes** | PM | Field trial & tuning |
| **7** | [`lab-07/`](lab-07/) | Teams | PM | Capstone presentation |

| Extension | [`extension/gazebo/`](extension/gazebo/) | 13:30 | Gazebo sandbox *(scaffold)* |

Shared: [`go2_patrol_helpers.py`](go2_patrol_helpers.py) · [`../day-01/go2_motion_helpers.py`](../day-01/go2_motion_helpers.py)

---

## Status

| Lab | Status |
|-----|--------|
| 0–6 | Ready |
| 7 | Scaffold (rubric in README) |
| Gazebo extension | Scaffold |

## Lab 7 scenarios (pick one per team)

| # | Scenario | Must demonstrate |
|---|----------|------------------|
| 1 | Corridor patrol | ≥ 3 checkpoints; image + SOC in metadata |
| 2 | Anomaly abort | Stop + `incident.json` on SOC or rate drop |
| 3 | Return-to-base | Final increment leg toward start (supervised) |
| 4 | Post-run report | JSONL → summary table or CSV |

---

**Next:** [Day 3 — B2 fundamentals](../day-03/)
