# Lab 2 — Obstacle avoidance forward move

| | |
|--|--|
| **Duration** | ~30–40 min |
| **Motion** | **Yes** |
| **Robot** | **Required** |
| **Prerequisite** | Day 1 [Lab 5](../../day-01/lab-05/); [Lab 0](../lab-00/) |

---

## What you will learn

- How **`ObstaclesAvoidClient`** differs from plain `SportClient.Move`.
- The camp sequence: **StandUp → BalanceStand → avoid on → `UseRemoteCommandFromApi(True)` → Move → stop → avoid off**.
- Optional preview of **increment** goals used in Labs 4–5.

---

## What you will run

| Script | Role |
|--------|------|
| [`lab02_obstacle_avoid_intro.py`](lab02_obstacle_avoid_intro.py) | Main lab (this folder’s script name matches **Lab 2**) |

Shared: [`../day-01/go2_motion_helpers.py`](../../day-01/go2_motion_helpers.py), [`go2_network_helpers.py`](../../day-01/go2_network_helpers.py).

---

## Steps

### 1. Safety briefing

- Cleared **~2 m** in front of the dog; cones not people.  
- **Spotter** and estop ready.  
- Default forward speed **≤ 0.35 m/s** in training.

### 2. Dry-run (no motion)

```bash
python course/student/day-02/lab-02/lab02_obstacle_avoid_intro.py $GO2_INTERFACE --dry-run
```

### 3. Live run

```bash
python course/student/day-02/lab-02/lab02_obstacle_avoid_intro.py $GO2_INTERFACE
# or skip prompt:
python course/student/day-02/lab-02/lab02_obstacle_avoid_intro.py $GO2_INTERFACE -y
```

### 4. Optional extensions

```bash
# SDK increment goal preview (used in Lab 4)
python course/student/day-02/lab-02/lab02_obstacle_avoid_intro.py $GO2_INTERFACE --increment-move

# Compare Sport FreeAvoid vs ObstaclesAvoidClient
python course/student/day-02/lab-02/lab02_obstacle_avoid_intro.py $GO2_INTERFACE --compare-free-avoid
```

---

## Expected results

| Step | PASS |
|------|------|
| Dry-run | Prints 7-step plan, exit 0 |
| Live | Dog stands, moves forward briefly under avoid, stops cleanly |
| DDS | No `rt/sportmodestate` error at start |

If the dog stands but does not translate: confirm avoid is on, teleop/remote not overriding, and you are on the correct NIC.

---

## Deliverable

- Log lines showing `[1/7]` … `[7/7]` completed  
- One note: how avoid motion felt vs Day 1 `lab05_safe_posture.py` walk  

**Next:** [Lab 3 — capture & probe](../lab-03/)
