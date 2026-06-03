# Lab 5 — Stand, balance, and short walk (SDK)

**TtT Day 1 · afternoon**  
**Robot required:** Yes  
**Motion:** **Yes** — supervised; clear space

## Objectives

- First **visible** motion: `StandUp` → `BalanceStand`.
- Short forward walk via **`SportClient.Move`** (same idea as a small step, not a patrol).
- Optional classic gait toggle with `--classic-walk`.

## Prerequisites

- [Lab 4](../lab-04/) PASS
- Handler present; e-stop plan agreed

## Steps

```bash
python3 course/day-01/New-lab/lab-05/lab05_safe_posture.py en6 --dry-run
python3 course/day-01/New-lab/lab-05/lab05_safe_posture.py en6
python3 course/day-01/New-lab/lab-05/lab05_safe_posture.py en6 --vx 0.3 --move-sec 3
python3 course/day-01/New-lab/lab-05/lab05_safe_posture.py en6 --posture-only   # stand only
```

Uses shared [`../go2_motion_helpers.py`](../go2_motion_helpers.py).

## ROS vs SDK reminder

This lab uses **SDK SportClient**, not ROS `/cmd_vel`. Day 2 Gazebo uses ROS; Day 2 patrol uses SDK avoid client.

## Deliverable

Confirm **PASS** in terminal; note `vx` and duration used.

**Next:** [Lab 6 — RViz](../lab-06/) or optional [Lab 7 showcase](../lab-07/)
