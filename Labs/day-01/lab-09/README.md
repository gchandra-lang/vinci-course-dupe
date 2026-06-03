# Lab 9 — PlotJuggler (time-series plots)

**TtT Day 1 · ROS visualization**  
**Robot required:** No for checker; optional for live Unitree streams  
**Motion:** None

## Objectives

- Install and launch **PlotJuggler** for ROS 2 topics.
- Plot numeric fields from a streaming topic (demo talker or robot state).
- Compare with JSONL logs from SDK labs ([Lab 3](../lab-03/)).

## Prerequisites

- [Lab 1](../lab-01/) **PASS**
- [Lab 2](../lab-02/) or demo script (sample topic)
- **PlotJuggler ROS package** — not in base desktop; install once:

```bash
./scripts/install_ros2_gui_extras.sh
# or: sudo apt install -y ros-humble-plotjuggler-ros
```

**Display** required for the GUI (`echo $DISPLAY`).

## Steps

### A — Automated check

```bash
python3 course/day-01/New-lab/lab-09/lab09_check_plotjuggler.py
```

### B — Plot demo scalar stream

**Terminal A:**

```bash
source /opt/ros/humble/setup.bash
./course/day-01/New-lab/lab-09/run_demo_plot.sh
```

**Terminal B:**

```bash
source /opt/ros/humble/setup.bash
ros2 run plotjuggler plotjuggler
```

In PlotJuggler:

1. **Streaming** → **ROS2 Topic Subscriber**
2. Select topic `/plot_demo/angle` (type `std_msgs/msg/Float32`)
3. Drag **data** into the plot area

You should see a ~0.5 Hz sine wave (demo node).

### C — Optional: robot or bag

With Unitree session sourced:

```bash
source scripts/setup_unitree_ros2.sh enp0s31f6
ros2 run plotjuggler plotjuggler
```

Pick a numeric field from a state topic, or **Load data file** → open a `.db3` from `ros2 bag record`.

## Files

| File | Purpose |
|------|---------|
| `lab09_check_plotjuggler.py` | Verifies `plotjuggler` package and executable |
| `plot_demo_publisher.py` | Publishes `/plot_demo/angle` (Float32) |
| `run_demo_plot.sh` | Launches demo publisher |
| `README.md` | This guide |

## Deliverable

- Log: `lab09_check_plotjuggler.py` → **RESULT: PASS**
- Screenshot: PlotJuggler showing `/plot_demo/angle` (or one robot field)

**Next:** [Lab 6 — RViz](../lab-06/) · [Lab 7 — Showcase](../lab-07/)
