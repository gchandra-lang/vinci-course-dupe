# Extension — Gazebo sandbox (Day 2 AM)

**TtT Day 2 · 13:30–15:00**  
**Robot required:** No (simulation)

## Purpose

Design and validate an **autonomous inspection routine** in simulation before the afternoon **field deployment** on Go2.

## When Gazebo is not available

Use this fallback (instructor-approved):

1. Dry-run [`../../lab-05/lab03_patrol_runner.py`](../../lab-05/lab03_patrol_runner.py) with `--dry-run`.
2. Replay [`../../lab-01/fixtures/sample_run_pass/`](../../lab-01/fixtures/sample_run_pass/) through the validator.
3. Discuss which gaps sim would close (global map, synthetic lidar).

## Setup pointer

- ROS 2 + Unitree: [`docs/ROS2-INSTALL.md`](../../../../docs/ROS2-INSTALL.md)
- Add Gazebo / Unitree sim packages per upstream `unitree_ros2` docs when the lab image is ready.

## Deliverable

Short note: one behavior you validated in sim (or dry-run) vs what you will test on hardware in Lab 6.
