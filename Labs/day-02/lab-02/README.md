# Lab 4 — SLAM Concepts & Obstacle Avoidance Introduction

**Duration:** ~60 min (20 min theory + 40 min hands-on)  
**Robot motion:** **Yes** — short supervised forward move with avoidance on  
**Prerequisites:** Labs 0–3 complete; clear space; spotter

**PDF coverage:** SLAM (introduction) · path planning · obstacle avoidance

**End of Day 1** — after this lab, continue to [Day 2](../../day-02/).

---

## Learning objectives

1. Sketch the **SLAM / navigation pipeline** and what Go2 covers today vs ROS later.
2. Use **`ObstaclesAvoidClient`** (`SwitchSet`, `Move`, `UseRemoteCommandFromApi`).
3. Contrast **reactive avoidance** with **global path planning** (Day 2 / Nav2).
4. Run [`lab04_obstacle_avoid_intro.py`](lab04_obstacle_avoid_intro.py) safely and stop cleanly.

---

## 1. Concepts — SLAM & planning (theory)

```text
┌──────────┐   ┌──────────┐   ┌─────────────┐   ┌──────────┐
│ Sensors  │──►│ Mapping  │──►│ Localization│──►│ Planner  │──► Actuators
│ lidar,   │   │ (SLAM)   │   │ on map      │   │ (path)   │     (sport)
│ camera   │   └──────────┘   └─────────────┘   └──────────┘
└──────────┘
```

| Stage | Day 1 |
|-------|--------|
| Mapping / SLAM | **Concept**; optional `go2_utlidar_switch.py` demo |
| Global path planning | **Concept** — Day 2 / ROS |
| Local obstacle avoidance | **Hands-on** — this lab |

---

## 2. Concepts — Python SDK avoidance

### Two APIs (know both)

| API | Module | Role |
|-----|--------|------|
| **`ObstaclesAvoidClient`** | `unitree_sdk2py.go2.obstacles_avoid` | Dedicated avoid service — **this lab** |
| **`SportClient.FreeAvoid`** | `go2.sport` | Sport-menu toggle (Lab 2 id 15) |

### `ObstaclesAvoidClient` pattern (from upstream)

```python
from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.obstacles_avoid.obstacles_avoid_client import ObstaclesAvoidClient

ChannelFactoryInitialize(0, "en6")
client = ObstaclesAvoidClient()
client.SetTimeout(3.0)
client.Init()

client.SwitchSet(True)
client.UseRemoteCommandFromApi(True)
client.Move(0.2, 0.0, 0.0)   # repeat ~20–50 Hz while moving
# ...
client.Move(0.0, 0.0, 0.0)
client.UseRemoteCommandFromApi(False)
client.SwitchSet(False)
```

| Method | Purpose |
|--------|---------|
| `SwitchSet(True/False)` | Enable / disable onboard avoid processor |
| `SwitchGet()` | Read enable state |
| `UseRemoteCommandFromApi(True)` | Take velocity from API (not only remote) |
| `Move(vx, vy, vyaw)` | Velocity in avoid mode (`_CallNoReply` — send repeatedly) |

Upstream references:

| File | Purpose |
|------|---------|
| `example/obstacles_avoid/obstacles_avoid_move.py` | Forward move under avoid |
| `example/obstacles_avoid/obstacles_avoid_switch.py` | Cycle switch on/off (no motion) |
| Camp script | [`lab04_obstacle_avoid_intro.py`](lab04_obstacle_avoid_intro.py) |

Docs: [ObstaclesAvoidClient](https://support.unitree.com/home/en/developer/ObstaclesAvoidClient)

### Safety

1. **Cones or boxes** in a small course — not people.  
2. Default **`vx=0.2`** m/s — do not exceed ~0.25 in class without instructor approval.  
3. Spotter + estop; `Ctrl+C` runs cleanup in the camp script.  
4. Avoidance ≠ SLAM ≠ full autonomy.

---

## 3. Hands-on

### Step 0 — Session & readiness

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/vinci-unitree
python course/day-01/lab-03/lab02_sport_readonly.py en6
```

### Step 1 — Dry-run (no motion)

```bash
python course/day-02/lab-02/lab04_obstacle_avoid_intro.py en6 --dry-run
```

Review the printed 6-step plan with your team.

### Step 2 — Upstream switch demo (optional, no forward move)

```bash
cd vendor/unitree_sdk2_python
python example/obstacles_avoid/obstacles_avoid_switch.py en6
```

Cycles API version and switch on/off (long loop — `Ctrl+C` to stop). Discuss what changed on the robot.

### Step 3 — Camp scripted move (supervised)

**Real terminal** required (`yes` prompt):

```bash
cd /path/to/vinci-unitree
python course/day-02/lab-02/lab04_obstacle_avoid_intro.py en6
```

**Visible motion sequence** (shared [`go2_motion_helpers.py`](../go2_motion_helpers.py)):

1. **`StandUp()`** + 5 s wait  
2. **`BalanceStand()`** + 2 s wait  
3. Enable avoid → **`Move(0.3, 0, 0)`** for **3 s** (default)  
4. Stop and disable avoid  

| Flag | Purpose |
|------|---------|
| `--vx` | Forward speed (default **0.3** m/s) |
| `--move-sec` | Move duration (default **3** s) |
| `--move-hz` | Move rate (default 20 Hz) |
| `--skip-stand` | Only if already standing (less visible) |
| `--stand-up-wait` | After StandUp (default 5 s) |
| `--dry-run` | Plan only |
| `-y` | Skip prompt (instructor) |
| `--increment-move` | After velocity move, `MoveToIncrementPosition(dx,0,0)` |
| `--increment-dx` | Metres for increment goal (default **0.4**) |
| `--compare-free-avoid` | Toggle `SportClient.FreeAvoid` vs dedicated avoid client |

**Optional SDK depth:**

```bash
python course/day-02/lab-02/lab04_obstacle_avoid_intro.py en6 --increment-move
python course/day-02/lab-02/lab04_obstacle_avoid_intro.py en6 --compare-free-avoid
```

**Expected:** numbered steps ending in `Summary: PASS`.

### Step 4 — Optional lidar mention (instructor)

```bash
python example/go2/high_level/go2_utlidar_switch.py en6
```

Lidar data feeds mapping in ROS — not full SLAM in this Python-only day.

### Step 5 — Debrief

| Question | Answer |
|----------|--------|
| Is this SLAM? | No — local reactive avoidance |
| What’s missing for inspection autonomy? | Map, goals, logging pipeline (Day 2) |

---

## 4. Exercises

### Exercise A

Draw the pipeline diagram and circle the box Lab 4 implements.

### Exercise B

Why must `Move()` be sent periodically instead of once?

<details>
<summary>Hint</summary>

`Move` uses `_CallNoReply`; sport/avoid stacks expect a continuous velocity stream (~20–50 Hz).

</details>

### Exercise C

Name one difference between `ObstaclesAvoidClient.Move` and `SportClient.Move`.

---

## 5. Troubleshooting

| Symptom | Action |
|---------|--------|
| `FAIL: could not enable obstacle avoidance` | Firmware / mode; try sport menu first; re-run Lab 2 |
| Robot does not move | `UseRemoteCommandFromApi(True)`? Switch on? Standing? |
| Will not stop | `Ctrl+C` (script cleanup); remote estop |
| `EOFError` on prompt | Use your terminal or `--dry-run` |
| Moves too fast | Lower `--vx` (e.g. 0.15) |

---

## 6. Deliverable

- Log snippet: dry-run plan + motion run ending in `Summary: PASS`  
- Answers to Exercise A and B  
- One sentence: what you would add in Day 2 for “inspection patrol”

---

## 7. Day 1 complete

You have covered: environment, DDS state, sport RPC, camera bundle, and avoid intro.

**Next:** [Day 2 — GO2 inspection & projects](../../day-02/)

---

## References

- [`lab04_obstacle_avoid_intro.py`](lab04_obstacle_avoid_intro.py)  
- `vendor/unitree_sdk2_python/example/obstacles_avoid/`  
- [Day 1 overview](../README.md) · [GO2 Field Guide](../../../docs/GO2-FIELD-GUIDE.md)
