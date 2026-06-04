# Lab 6 — RViz2 and Go2 ROS 2 data

**TtT Day 1 · 15:15–17:00**  
**Robot required:** Recommended (Ethernet on robot LAN)  
**Motion:** None

## What you will learn

- Open **RViz2** with the camp Unitree ROS 2 environment (same DDS path as Labs 1–2).
- Use RViz **panels and tools** (Displays, Fixed Frame, 3D view).
- See **live Go2 data** (LiDAR point cloud, odometry) when the dog publishes ROS topics.
- Connect RViz to what you saw in **Lab 3** (`rt/sportmodestate` on the **SDK** side — different names on the ROS graph).

---

## Prerequisites

| Lab | Why |
|-----|-----|
| [Lab 1](../lab-01/) | `unitree_ros2` built; you can `source scripts/setup_unitree_ros2.sh` |
| [Lab 2](../lab-02/) | You have used ROS 2 pub/sub (same graph idea) |
| [Lab 3](../lab-03/) *(optional)* | You know `sportmodestate` exists on DDS; ROS may expose `/sportmodestate` or similar |

**Ethernet:** Use the NIC with `192.168.123.x` (same as SDK labs), e.g. `enx207bd22b611a` — not `enp0s31f6` unless that is your link.

```bash
export GO2_INTERFACE=enx207bd22b611a   # your name from: ip -br addr
```

**Two terminals:** RViz in one; `ros2` CLI in the other (both need Unitree ROS sourced for robot data).

---

## Quick start

**Terminal A — RViz (this lab script):**

```bash
cd /path/to/vinci-unitree
chmod +x course/day-01/New-lab/lab-06/run_rviz.sh
./course/day-01/New-lab/lab-06/run_rviz.sh
# or explicitly:
./course/day-01/New-lab/lab-06/run_rviz.sh enx207bd22b611a
```

This calls [`scripts/run_rviz2.sh`](../../../../scripts/run_rviz2.sh) and loads [`config/rviz/unitree_go2_lidar.rviz`](../../../../config/rviz/unitree_go2_lidar.rviz) when the robot stack is used.

**No robot yet?** Practice the UI only:

```bash
./course/day-01/New-lab/lab-06/run_rviz.sh --ros-only
```

**Terminal B — inspect topics (robot on):**

```bash
source /path/to/vinci-unitree/scripts/setup_unitree_ros2.sh enx207bd22b611a
# (from repo root: scripts/setup_unitree_ros2.sh)
ros2 topic list
ros2 topic hz /sportmodestate    # if listed
ros2 topic echo /sportmodestate --once
```

---

## Hands-on tasks (click and explore)

Work in order. Tick each item in your notes.

### Task 1 — Launch and layout

1. Start `./course/day-01/New-lab/lab-06/run_rviz.sh` with Go2 powered and cabled.
2. Confirm the window title shows **RViz2** and the left **Displays** panel is visible.
3. In the menu: **Panels → Displays** (on) and **Panels → Tool Properties** (optional).

### Task 2 — Global Options (Fixed Frame)

1. In **Displays**, open **Global Options**.
2. Note **Fixed Frame** = `odom` (set by the camp config).
3. If the 3D view shows *Fixed Frame [map] does not exist* or similar, set **Fixed Frame** to `odom` or `utlidar_lidar` (try what appears in **TF** when the robot is on).
4. **Question:** Why does RViz need a fixed frame? *(Hint: all other frames are drawn relative to it.)*

### Task 3 — Pre-loaded displays (robot on)

With the default config and robot publishing:

| Display | Topic (typical) | What to look for |
|---------|-----------------|------------------|
| **Grid** | — | Ground reference in `odom` |
| **TF** | — | Expand tree; see frame names from the robot |
| **LiDAR** | `/utlidar/cloud_deskewed` | Colored points updating (~10 Hz) |
| **Robot odom** | `/utlidar/robot_odom` | Orange arrow moving if the dog moves |
| **Robot pose** | `/utlidar/robot_pose` | Pose marker |

**Clicks:**

1. Click each display row — toggle **Enabled** off/on and watch the 3D view.
2. Select **LiDAR** → change **Size (Pixels)** — see point size change.
3. Use the mouse: **left-drag** orbit, **middle-drag** pan, **wheel** zoom (or **Move Camera** tool).

### Task 4 — Tools bar

1. Select **Move Camera** — orbit the scene.
2. Select **Focus Camera** — click a point in the 3D view to center on it.
3. Use **Views** panel (if open) — reset **Current View** if you get lost.

### Task 5 — Add a display yourself

1. Click **Add** (bottom of Displays).
2. Choose **By topic** → pick a `sensor_msgs/PointCloud2` or `nav_msgs/Odometry` topic if listed.
3. Or choose **By display type** → **PointCloud2** → set **Topic** manually to `/utlidar/cloud_deskewed`.
4. If nothing appears: run `ros2 topic list` in Terminal B — topic names must match exactly.

### Task 6 — ROS CLI vs SDK (Lab 3 comparison)

In Terminal B:

```bash
ros2 topic list | grep -E 'sport|low|utlidar|odom'
```

Fill in your table:

| Source | Example name | Message path |
|--------|--------------|--------------|
| SDK Lab 3 | `rt/sportmodestate` | CycloneDDS + `SportModeState_` |
| ROS 2 | `/sportmodestate` or `…` | *(your `ros2 topic list` line)* |
| RViz LiDAR | `/utlidar/cloud_deskewed` | Point cloud in 3D |

**Written (2 sentences):** How is ROS 2 on the PC related to the same robot you used with the Python SDK?

<details>
<summary>Hint</summary>

Same robot and often the same DDS domain; ROS wraps streams as **topics** with `/` names and types like `unitree_go/msg/…`. The SDK uses **`rt/…`** names and `unitree_sdk2py` IDL types.
</details>

### Task 7 — Optional: record a bag

```bash
ros2 bag record -o lab06_go2_snippet /utlidar/cloud_deskewed /utlidar/robot_odom -d 30
```

Compare to JSONL from Lab 3: bags are ROS-time-series files; SDK logs are your own script format.

---

## Troubleshooting

| Symptom | Action |
|---------|--------|
| `ROS 2 Humble not found` | `./scripts/install_ros2_humble.sh` |
| `unitree_ros2` / source errors | [Lab 1](../lab-01/); `./scripts/build_unitree_ros2.sh` |
| RViz empty, no points | Robot on? `ros2 topic list` — need `/utlidar/…` topics; LiDAR mode on dog |
| No 3D dog mesh | Normal — `unitree_ros2` does not ship URDF; you see clouds/odom, not a mesh |
| Wrong NIC | Use `GO2_INTERFACE` or pass your `enx…` / `ens33` to `run_rviz.sh` |
| Conda breaks `ros2` | Use a **clean** bash shell for ROS (no `conda activate`) for RViz + `ros2` CLI |

More detail: [`docs/ROS2-INSTALL.md`](../../../../docs/ROS2-INSTALL.md) · [`docs/GO2-FIELD-GUIDE.md`](../../../../docs/GO2-FIELD-GUIDE.md)

---

## Deliverable

Submit:

1. Screenshot: RViz with **LiDAR** or **Robot odom** visible (robot on), **or** screenshot of `--ros-only` with Grid + empty 3D view labeled “practice”.
2. One line from `ros2 topic list` showing a Unitree/Go2 topic (e.g. `utlidar` or `sportmodestate`).
3. One sentence: Fixed Frame you used and one display you toggled off/on.

---

## See also

- [Lab 8 — rqt](../lab-08/) — graph and topic monitor  
- [Lab 9 — PlotJuggler](../lab-09/) — time-series plots  
- Repo script: [`scripts/run_rviz2.sh`](../../../../scripts/run_rviz2.sh)

**Next:** [Lab 7 — Optional showcase](../lab-07/) · **Day 2:** [Gazebo + patrol](../../day-02/)
