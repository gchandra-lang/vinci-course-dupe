# Gazebo Lab 2 — Forward move in sim

**Motion:** Sim only  
**Prerequisite:** [Gazebo Lab 1](../lab-01/)

## Learn

- Publish a short forward `vx` on `/cmd_vel` (CHAMP controller).
- Compare parameters with hardware [`../../lab-02/lab02_obstacle_avoid_intro.py`](../../lab-02/lab02_obstacle_avoid_intro.py).

## Run

```bash
python3 course/student/day-02/gazebo/lab-02/lab02_sim_move_forward.py --dry-run
python3 course/student/day-02/gazebo/lab-02/lab02_sim_move_forward.py --vx 0.25 --duration 3.0
```

## PASS

Dog model translates in Gazebo; script exits 0.

**Back:** [Gazebo overview](../README.md)
