# Lab 1 — Go2, ROS 2, and `unitree_ros2` setup

**TtT Day 1 · 10:45 ROS block**  
**Robot required:** No (optional `--robot-topics` with NIC)  
**Motion:** None

## What you will learn

- What the **Unitree Go2** is on the network (Ethernet, onboard IP, DDS).
- How **ROS 2** fits on top of the same middleware as the SDK.
- Why **ROS control** and **SDK control** are different APIs on the same dog.
- Whether **`unitree_ros2`** is installed and built on your PC.

## Concepts: three layers

```text
  Your PC
    ├── ROS 2 nodes (topics like /cmd_vel, lab talker/listener)
    │     └── needs: /opt/ros/humble + unitree_ros2 workspace
    └── Python SDK scripts (SportClient, rt/sportmodestate)
          └── needs: conda unitree_env + CYCLONEDDS_HOME
                    (separate terminal from ROS — see Day 1 README)
```

| Question | ROS 2 answer | SDK answer |
|----------|--------------|------------|
| How do I see state? | `ros2 topic list` / echo | Subscribe `rt/sportmodestate` |
| How do I move the dog? | ROS cmd API or Gazebo `/cmd_vel` | `SportClient.Move()` |
| Workspace for Unitree msgs | `unitree_ros2` | `unitree_sdk2_python` |

### `unitree_ros2` install paths (both valid)

| Path | How it gets there |
|------|-------------------|
| `~/unitree_ros2` | `./scripts/build_unitree_ros2.sh` (default) |
| `<vinci-unitree>/unitree_ros2` | `git clone … unitree_ros2` then `UNITREE_ROS2=$PWD/unitree_ros2 ./scripts/build_unitree_ros2.sh` |

Lab script and [`setup_unitree_ros2.sh`](../../../scripts/setup_unitree_ros2.sh) check **both** plus `$UNITREE_ROS2`.

## Steps

1. Read [`docs/ROS2-INSTALL.md`](../../../docs/ROS2-INSTALL.md) if this is your first ROS install.

2. Run readiness:

```bash
cd /path/to/vinci-unitree
python3 course/day-01/New-lab/lab-01/lab01_ros_readiness.py
```

3. Optional checks:

```bash
python3 course/day-01/New-lab/lab-01/lab01_ros_readiness.py --try-demo
python3 course/day-01/New-lab/lab-01/lab01_ros_readiness.py enp0s31f6 --robot-topics
```

4. When PASS, practice sourcing Unitree ROS (robot optional for Lab 2):

```bash
source scripts/setup_unitree_ros2.sh enp0s31f6
ros2 pkg list | grep unitree
```

## Files in this folder

| File | Purpose |
|------|---------|
| `lab01_ros_readiness.py` | Install/build checker + printed how-to |
| `README.md` | This guide |

Shared helpers live in [`../ros_basic_helpers.py`](../ros_basic_helpers.py).

## Deliverable

- Screenshot or log showing **`RESULT: PASS`**
- One sentence: where your `unitree_ros2` lives (`in-repo` vs `home`)

**Next:** [Lab 2 — ROS pub/sub](../lab-02/)
