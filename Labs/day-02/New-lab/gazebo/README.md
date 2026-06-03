# Extension — Gazebo sandbox (Day 2)

**TtT Day 2 · 13:30–15:00**  
**Robot required:** No (simulation)  
**Platform:** Unitree **Go2** model in Gazebo Classic (CHAMP)

## Purpose

Design and validate motion **before** afternoon **field deployment** on the physical Go2. This block uses **ROS 2 + Gazebo**, not the Python SDK — field labs 4–6 still use **`unitree_sdk2_python`** on Ethernet.

| Lab | Folder | Focus |
|-----|--------|--------|
| **1** | [`lab-01/`](lab-01/) | Install, launch Gazebo, verify topics |
| **2** | [`lab-02/`](lab-02/) | Short forward move via `/cmd_vel` |

**Install guide:** [`docs/GAZEBO-GO2.md`](../../../../docs/GAZEBO-GO2.md)

## Quick start

```bash
./scripts/install_gazebo_go2.sh          # once
source scripts/setup_gazebo_go2.sh
./scripts/run_gazebo_go2.sh              # terminal A
# terminal B:
python3 course/day-02/New-lab/gazebo/lab-01/lab01_check_sim.py
python3 course/day-02/New-lab/gazebo/lab-02/lab02_sim_move_forward.py
```

## When Gazebo is not available

Instructor-approved fallback:

1. Dry-run [`../../lab-05/lab03_patrol_runner.py`](../../lab-05/lab03_patrol_runner.py) with `--dry-run`.
2. Replay [`../../lab-01/fixtures/sample_run_pass/`](../../lab-01/fixtures/sample_run_pass/) through the validator.
3. Discuss which gaps sim would close (global map, synthetic lidar).

## Stack

| Layer | Notes |
|-------|--------|
| ROS 2 Humble | [`docs/ROS2-INSTALL.md`](../../../../docs/ROS2-INSTALL.md) |
| Go2 Gazebo workspace | `~/go2_gazebo_ws` — [`scripts/install_gazebo_go2.sh`](../../../../scripts/install_gazebo_go2.sh) |
| Upstream | [anujjain-dev/unitree-go2-ros2](https://github.com/anujjain-dev/unitree-go2-ros2) (`humble`, pinned in install script) |

**Not required:** `unitree_ros2` robot DDS for these labs.

## Relation to Day 2 main labs

| Main lab | Gazebo tie-in |
|----------|----------------|
| [`lab-02`](../../lab-02/) obstacle avoid | Same forward-motion *idea*; hardware uses SDK |
| [`lab-05`](../../lab-05/) patrol | Optional narrative: timing validated in sim |
| [`lab-06`](../../lab-06/) field | Real Go2 — always after this block |

## Included simulation files

This extension includes a minimal Gazebo sandbox you can run locally for Day 2:

- `launch/spawn_unitree.launch.py` — launch file that starts Gazebo and spawns the Go2 URDF using `spawn_entity.py`.
- `worlds/unitree_world.world` — minimal world with sun and ground plane.

These files have been moved to a dedicated ament package to make them runnable from a ROS 2 workspace.

Package: `course_day02_extension_gazebo` (installed under `extensions/`)

How to run (in a ROS 2 workspace)

1. Build and install the package into your workspace (from the repository root):

```bash
colcon build --packages-select course_day02_extension_gazebo --symlink-install
source install/setup.bash
```

2. Launch the sandbox:

```bash
ros2 launch course_day02_extension_gazebo spawn_unitree.launch.py
```

If you don't want to build, the original fallback steps in this file still apply (dry-run or replay). The package expects `gazebo_ros` and `unitree_description` to be available in your environment.

## Deliverable

After Lab 2: one sentence comparing sim forward move to what you will run on hardware in Lab 6.
