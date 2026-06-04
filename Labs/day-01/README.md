# Day 1 — Go2: ROS 2 vs SDK foundations

> **New-lab track:** Reorganized Day 1 sequence. **Not fully verified** on hardware; canonical merge layout is [`../`](../) (main). See [`NOTICE.md`](NOTICE.md).

**Platform:** Unitree **GO2**  
**Stack:** ROS 2 Humble + `unitree_ros2` (AM) · Python **SDK** / CycloneDDS (PM)

**Schedule:** [`SCHEDULE-TTT.md`](../SCHEDULE-TTT.md)

---

## What this day is for

1. **Morning (ROS):** What Go2 is, how **ROS 2** relates to the robot, and how that differs from **SDK control**.
2. **Afternoon (SDK):** Subscribe to live DDS state, check **motion modes**, then **stand** and a **short supervised walk**.

**By the end of Day 1** you should be able to:

- Explain **ROS 2 topic** vs **DDS topic** (`/cmd_vel` vs `rt/sportmodestate`).
- Install/source **`unitree_ros2`** from the repo clone or `~/unitree_ros2`.
- Run a ROS 2 **talker/listener** (no robot).
- Subscribe to `rt/sportmodestate` and use **SportClient** for stand + small move.

---

## ROS 2 control vs SDK control (Go2)

| | **ROS 2 + `unitree_ros2`** | **Python SDK (`unitree_sdk2_python`)** |
|--|---------------------------|----------------------------------------|
| **Use in camp** | Lab 1–2, rqt (8), PlotJuggler (9), RViz (6), Day 2 Gazebo | Lab 0, 3–5, 7 and all Day 2 patrol |
| **Wire** | ROS topics / services on CycloneDDS | DDS topics + RPC (`SportClient`) |
| **Motion example** | `/cmd_vel` (Gazebo CHAMP) or ROS nodes | `SportClient.Move()`, `StandUp()` |
| **State example** | `ros2 topic echo /sportmodestate` (if bridged) | `rt/sportmodestate` subscribe |
| **When** | Tools, sim, Nav2-style stacks | Real dog on Ethernet |

Same physical robot — **two software APIs**. Do not mix G1 examples (`unitree_hg`, `LocoClient`) on Go2.

---

## Lab sequence (ordered)

| Lab | Folder | Motion? | Focus |
|-----|--------|---------|--------|
| **0** | [`lab-00/`](lab-00/) | No | SDK env: CycloneDDS, `unitree_sdk2_python` |
| **1** | [`lab-01/`](lab-01/) | No | Go2 + ROS concepts; **`unitree_ros2`** install check |
| **2** | [`lab-02/`](lab-02/) | No | ROS 2 pub/sub (talker / listener) |
| **3** | [`lab-03/`](lab-03/) | No | SDK DDS: `rt/sportmodestate` subscribe |
| **4** | [`lab-04/`](lab-04/) | No | SDK RPC read-only: modes, `CheckMode`, `SportClient.Init` |
| **5** | [`lab-05/`](lab-05/) | **Yes** | **StandUp**, **BalanceStand**, short **walk** |
| **6** | [`lab-06/`](lab-06/) | No | RViz2 + Unitree topics (robot on LAN) |
| **7** | [`lab-07/`](lab-07/) | **Yes** | Optional gestures / showcase |
| **8** | [`lab-08/`](lab-08/) | No | **rqt** — graph & topic monitor |
| **9** | [`lab-09/`](lab-09/) | No | **PlotJuggler** — time-series plots |

Shared: [`go2_network_helpers.py`](go2_network_helpers.py) (NIC checks) · [`go2_motion_helpers.py`](go2_motion_helpers.py) · [`ros_basic_helpers.py`](ros_basic_helpers.py)

**Robot Ethernet:** `export GO2_INTERFACE=enx207bd22b611a` (your name from `ip -br addr`) — Labs 3–5, 7 auto-detect if omitted.

---

## `unitree_ros2` workspace locations

Checked by Lab 1 and [`scripts/setup_unitree_ros2.sh`](../../scripts/setup_unitree_ros2.sh):

| Location | Typical use |
|----------|----------------|
| `<repo>/unitree_ros2` | Clone inside this project |
| `~/unitree_ros2` | Default from [`build_unitree_ros2.sh`](../../scripts/build_unitree_ros2.sh) |
| `$UNITREE_ROS2` | Your override (either path above) |

---

## References

| Resource | Path |
|----------|------|
| ROS install | [`docs/ROS2-INSTALL.md`](../../docs/ROS2-INSTALL.md) |
| Go2 field | [`docs/GO2-FIELD-GUIDE.md`](../../docs/GO2-FIELD-GUIDE.md) |
| SDK setup | [`scripts/setup_unitree_sdk.sh`](../../scripts/setup_unitree_sdk.sh) |
| Unitree ROS session | [`scripts/setup_unitree_ros2.sh`](../../scripts/setup_unitree_ros2.sh) |

---

## Status

| Lab | Status |
|-----|--------|
| 0–5, 7 | Ready (SDK + motion) |
| 1–2 | Ready (ROS + `unitree_ros2`) |
| 6 | Ready (RViz guide) |
| 8–9 | Ready (rqt + PlotJuggler; extras via `install_ros2_gui_extras.sh`) |

**Next day:** [Day 2 — Gazebo + patrol](../day-02/)
