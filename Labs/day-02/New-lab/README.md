# Day 2 — Go2: Gazebo sandbox + patrol

> **New-lab track:** Includes [`gazebo/`](gazebo/) (CHAMP + `/cmd_vel`). **Not fully verified** everywhere; canonical merge layout is [`../`](../). See [`NOTICE.md`](NOTICE.md).

**Platform:** Unitree **GO2**  
**Stack:** **Gazebo** (sim) + Python SDK (field) · optional ROS 2

**Prerequisite:** [Day 1](../day-01/) Labs 0–5 (SDK stand/walk + ROS basics).

**Schedule:** [`SCHEDULE-TTT.md`](../SCHEDULE-TTT.md)  
**Gazebo:** [`gazebo/`](gazebo/) · [`docs/GAZEBO-GO2.md`](../docs/GAZEBO-GO2.md)

---

## What this day is for

| Block | Track | Focus |
|-------|--------|--------|
| **AM** | Gazebo | Sim Go2, `/cmd_vel`, validate motion in Gazebo |
| **AM** | SDK | Obstacle avoid, capture, patrol planning |
| **PM** | SDK | Integrated patrol, field trial, presentations |

---

## Lab sequence

| Lab | Folder | Motion? | Focus |
|-----|--------|---------|--------|
| **0** | [`lab-00/`](lab-00/) | No | Day 2 readiness |
| **1** | [`lab-01/`](lab-01/) | No | Patrol run-folder schema |
| **Gazebo 1** | [`gazebo/lab-01/`](gazebo/lab-01/) | No | Launch sim, verify topics |
| **Gazebo 2** | [`gazebo/lab-02/`](gazebo/lab-02/) | Sim | Short forward `/cmd_vel` |
| **2** | [`lab-02/`](lab-02/) | **Yes** | Obstacle avoid intro (hardware) |
| **3** | [`lab-03/`](lab-03/) | No* | Camera + platform probe |
| **4** | [`lab-04/`](lab-04/) | **Yes** | Increment patrol |
| **5** | [`lab-05/`](lab-05/) | **Yes** | Patrol runner |
| **6** | [`lab-06/`](lab-06/) | **Yes** | Field trial |
| **7** | [`lab-07/`](lab-07/) | Teams | Capstone presentation |

Shared: [`go2_patrol_helpers.py`](go2_patrol_helpers.py) · [`../day-01/go2_motion_helpers.py`](../day-01/go2_motion_helpers.py)

---

## Gazebo vs hardware (Day 2)

| | **Gazebo** (`gazebo/`) | **Patrol labs** (`lab-02`–`06`) |
|--|-------------------------|----------------------------------|
| API | ROS `geometry_msgs/Twist` → `/cmd_vel` | SDK `ObstaclesAvoidClient`, `SportClient` |
| Robot | None | Physical Go2 on Ethernet |
| Install | `~/go2_gazebo_ws` — see Gazebo guide | `unitree_sdk2_python` — Day 1 Lab 0 |

---

## Status

| Lab | Status |
|-----|--------|
| 0–6, Gazebo 1–2 | Ready |
| 7 | Scaffold (rubric in README) |

**Next:** [Day 3 — B2 fundamentals](../day-03/)
