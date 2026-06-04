# Lab 2 — ROS 2 pub/sub (talker / listener)

**TtT Day 1 · ROS track**  
**Robot required:** No  
**Motion:** None

## Objectives

- Run a **publisher** and **subscriber** node on the same ROS 2 graph.
- Relate this to Unitree: ROS 2 uses the same DDS middleware as the SDK, but **different topic names** (see Day 1 main README).

## Prerequisites

- [Lab 0](../lab-00/) **PASS**
- `source /opt/ros/humble/setup.bash` (or use `run_lab.sh`, which sources it for you)

## Steps

### A — Manual (recommended first)

**Terminal A — listener:**

```bash
cd /path/to/vinci-unitree
chmod +x course/day-01/New-lab/lab-02/run_lab.sh
./course/day-01/New-lab/lab-02/run_lab.sh listener
```

**Terminal B — talker:**

```bash
./course/day-01/New-lab/lab-02/run_lab.sh talker
```

You should see `hello_from_unitree_camp 0`, `1`, `2`, … in the listener terminal. Stop with **Ctrl+C** in each terminal.

**Terminal C — inspect the graph:**

```bash
source /opt/ros/humble/setup.bash
ros2 topic list
ros2 topic echo /ros_basic_topic
```

### B — Automated verify

```bash
source /opt/ros/humble/setup.bash
python3 course/day-01/New-lab/lab-02/lab01_verify_pubsub.py
```

The checker runs talker/listener with **`/usr/bin/python3.10`** (system ROS), not conda `python3`. If you see `rclpy._rclpy_pybind11` / `cpython-311` errors, use `run_lab.sh` or `conda deactivate` before manual `python3 talker.py`.

A short `ExternalShutdownException` traceback after verify is **harmless** (talker was stopped by `timeout 5`); updated scripts exit quietly. What matters is **`PASS`** and the `[INFO] Published:` / listener lines above it.

### C — Optional: Unitree workspace sourced

After Lab 0, you can run talker/listener with only Humble (above). To practice the **same session** as robot labs:

```bash
source scripts/setup_unitree_ros2.sh enp0s31f6   # or your NIC; robot optional for this lab
./course/day-01/New-lab/lab-02/run_lab.sh talker
```

Pub/sub on `ros_basic_topic` does not require the robot to be on.

## Files

| File | Role |
|------|------|
| `talker.py` | Publishes `std_msgs/String` on `ros_basic_topic` |
| `listener.py` | Subscribes and logs messages |
| `run_lab.sh` | Sources Humble, runs talker or listener |
| `lab01_verify_pubsub.py` | One-shot PASS/FAIL check |

## Deliverable

One paragraph: what topic/type you used, and how that differs from Go2 DDS topic `rt/sportmodestate` (SDK lab-02).

**Next:** SDK [`lab-02`](../../lab-02/) or Lab 0 with `--robot-topics` when the dog is connected.
