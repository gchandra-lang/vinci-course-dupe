# Gazebo — Day 2 simulation block (optional)

| | |
|--|--|
| **When** | Typical TtT 13:30–15:00 |
| **Motion** | Sim only (`/cmd_vel`) |
| **Robot** | Not required |
| **Prerequisite** | Day 1 [Labs 1–2](../../day-01/lab-02/) (ROS pub/sub); hardware [Lab 2](../lab-02/) for comparison |

---

## What you will learn

- How **ROS 2 + Gazebo** moves the Go2 model vs **SDK avoid** on the real dog.
- How to verify sim topics and send a short **forward velocity**.
- What sim does **not** replace (checkpoint capture, `ObstaclesAvoidClient` on hardware).

Install: [`docs/GAZEBO-GO2.md`](../../../../docs/GAZEBO-GO2.md).

---

## What you will run

```bash
./scripts/install_gazebo_go2.sh          # once
source scripts/setup_gazebo_go2.sh
./scripts/run_gazebo_go2.sh              # terminal A

# terminal B:
python3 course/student/day-02/gazebo/lab-01/lab01_check_sim.py
python3 course/student/day-02/gazebo/lab-02/lab02_sim_move_forward.py --vx 0.25 --duration 3.0
```

| Lab | Script |
|-----|--------|
| [lab-01](lab-01/) | `lab01_check_sim.py` |
| [lab-02](lab-02/) | `lab02_sim_move_forward.py` |

---

## If Gazebo is unavailable

1. Dry-run [`../lab-05/lab05_patrol_runner.py`](../lab-05/lab05_patrol_runner.py) `--dry-run`  
2. Validate [`../lab-01/fixtures/sample_run_pass/`](../lab-01/fixtures/sample_run_pass/)  
3. Discuss what sim would add (map, synthetic lidar)

---

## Link to field track

Same *idea* as forward motion in [`../lab-02/lab02_obstacle_avoid_intro.py`](../lab-02/lab02_obstacle_avoid_intro.py) (`--vx` / `--move-sec`) — different API (`geometry_msgs/Twist` on `/cmd_vel`).

**Back:** [Day 2 field labs](../README.md)
