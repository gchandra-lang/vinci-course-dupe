# Lab 2 — Multi-Leg Patrol (Increment Goals)

**Duration:** ~60 min  
**Robot motion:** **Yes** — supervised increment legs under obstacle avoidance  
**Prerequisites:** [Lab 0](../lab-00/) · [Lab 1](../lab-01/) · Day 1 Labs 2 & 4 (stand + avoid intro)

**PDF coverage:** Autonomous inspection routines · deploying on hardware

---

## Learning objectives

1. Run a **multi-leg patrol** from `patrol_plan.json` (not a single timed `Move`).
2. Use **`MoveToIncrementPosition(dx, dy, dyaw)`** between checkpoints with avoid enabled.
3. Apply **scenario motion limits** and class speed caps.
4. Tune **`--leg-wait`** when a leg stops short of the cone.

---

## 1. Concepts

### Increment leg vs Day 1 velocity move

| | Day 1 Lab 4 | Lab 2 |
|--|-------------|--------|
| Command | `Move(vx,0,0)` for N seconds | `MoveToIncrementPosition(dx,dy,dyaw)` repeated |
| Goal | “move forward ~3 s” | “move ~0.4 m toward next cone” |
| Plan | Hard-coded in script | **`patrol_plan.json`** |

Increment goals use the onboard avoid stack in **mode=1** (SDK). They are **local** — not GPS or SLAM. Stay in a prepared cone course.

### Patrol sequence

```text
StandUp → BalanceStand
  → SwitchSet(True) → UseRemoteCommandFromApi(True)
  → for each leg in plan:
        MoveToIncrementPosition … (repeat ~10 Hz for leg-wait)
        dwell at to_checkpoint
  → Move(0,0,0) → API off → SwitchSet(False)
```

Shared code: [`../go2_patrol_helpers.py`](../go2_patrol_helpers.py) · stand prep from [`../../day-01/go2_motion_helpers.py`](../../day-01/go2_motion_helpers.py).

Upstream reference: `vendor/unitree_sdk2_python/example/obstacles_avoid/obstacles_avoid_move.py`

---

## 2. Patrol plan for this lab

Default file: [`patrol_plan.cone_course.json`](patrol_plan.cone_course.json)

**Layout (L-shaped)** — place cones so leg 2’s turn makes sense:

```text
        [cp_C] blue
          ↑
          |  leg 3: dx=0.3 forward
          |
[cp_B] yellow — turn ~0.6 rad at B (leg 2)
          |
          |  leg 1: dx=0.3 forward
          |
[cp_A] red (dog starts facing toward B)
```

| Checkpoint | Marker (example) |
|------------|------------------|
| `cp_A` | Red — start, facing first leg |
| `cp_B` | Yellow — **corner** (turn here) |
| `cp_C` | Blue — end of second leg |

| Leg | Type | Goal |
|-----|------|------|
| 1 | `increment` dx=0.3, dyaw=0 | A → B (straight) |
| 2 | `increment` dyaw=**0.6**, dx=0 | **Turn in place** at B (~34°) |
| 3 | `increment` dx=0.3, dyaw=0 | B → C (straight after turn) |

Tune **`dyaw`** in the JSON if the dog under/over-shoots the corner (try 0.4–0.8 rad; avoid >1.0 in class without instructor OK).

You may use your Lab 1 scaffold plan instead:

```bash
python course/day-02/lab-04/lab02_increment_patrol.py en6 \
  --plan ./run_dry_team_a/patrol_plan.json \
  --scenario course/day-02/lab-00/my_team_scenario.json
```

---

## 3. Script — `lab02_increment_patrol.py`

| Flag | Purpose |
|------|---------|
| `en6` | Ethernet interface |
| `--plan PATH` | `patrol_plan.json` (default: cone course) |
| `--scenario PATH` | Clamp legs to Lab 0 `motion_limits` |
| `--dry-run` | Print steps only |
| `--leg-wait SEC` | Settle time after each leg’s increment pulses (default **5**) |
| `--leg-pulses` | Times to send each increment goal (default **3**) |
| `--leg-hz` | Pulse rate (default **2**) |
| `--stream-increment` | Legacy continuous repeat (not recommended) |
| `--default-dwell` | Pause at each `to_checkpoint` (default **2**) |
| `--skip-stand` | Only if already in balanced stand |
| `-y` / `--yes` | Skip confirmation (instructor) |

**Class caps** (enforced with `--scenario`): forward increment **≤ 0.5 m**, prefer **0.4 m**; see Lab 0 scenario.

---

## 4. Safety

1. **Cone course** — 3 markers in a cleared lane; no people inside the lane during motion.
2. **Spotter** walks with the dog; one patrol at a time per Go2.
3. **Stop** — `Ctrl+C` runs cleanup (stop move, avoid off).
4. **Do not** chain large `dx` values without instructor approval.
5. If the dog enters **damp**, recover per [field guide](../../../docs/GO2-FIELD-GUIDE.md) before retrying.

---

## 5. Hands-on

### Step 0 — Session

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/vinci-unitree

python course/day-02/lab-00/lab00_day2_readiness.py en6
```

### Step 1 — Dry-run

```bash
python course/day-02/lab-04/lab02_increment_patrol.py en6 --dry-run
```

Review leg list and dwell times with your team.

### Step 2 — Lay out cones (L-shape)

Place **cp_A** (start), **cp_B** (corner), **cp_C** (end of second segment) as in the diagram above. Each straight segment ≈ **0.3 m**; the dog **turns at B** (leg 2, `dyaw=0.6`) before walking toward C.

### Step 3 — First patrol (supervised)

**Real terminal** (`yes` prompt):

```bash
python course/day-02/lab-04/lab02_increment_patrol.py en6
```

**Expected:** stand visible → short forward motion per leg → stop clean; console ends with `Summary: PASS`.

### Step 4 — Tune if needed

| Symptom | Try |
|---------|-----|
| Stops short of cone | `--leg-wait 10` or reduce `dx` in plan to 0.3 |
| Overshoots | Reduce `dx` to 0.3 |
| No motion | Day 1 avoid checklist; app sport mode; `SwitchGet` true |
| Turns wrong | Add small `dyaw` on second leg only with instructor OK |

```bash
python course/day-02/lab-04/lab02_increment_patrol.py en6 --leg-wait 10 --plan patrol_plan.cone_course.json
```

### Step 5 — Optional velocity leg

Add a leg to your plan (advanced):

```json
{
  "type": "velocity",
  "vx": 0.2,
  "vy": 0.0,
  "vyaw": 0.0,
  "duration_s": 2.0,
  "to_checkpoint": "cp_B"
}
```

Re-run with `--scenario` so `vx` is clamped.

---

## 6. Exercises

1. Run with your Lab 1 **`run_dry_* /patrol_plan.json`** — did both increment legs fire?
2. Change only `dx` on leg 1 to **0.3** — compare distance to cone B.
3. One sentence: difference between **`leg-wait`** and **`dwell_s`** on a checkpoint.

---

## 7. Deliverable

Submit:

1. Log: `--dry-run` output (leg summary)
2. Log: hardware run → **PASS** or describe tuning (`--leg-wait`, `dx`)
3. Your **`patrol_plan.json`** used (or diff from `patrol_plan.cone_course.json`)
4. Photo of cone layout (optional)

---

## 8. Next lab

**[Lab 5 — Integrated patrol runner + capture](../lab-03/)**  
Same legs plus `VideoClient` and run-folder output.

---

## References

- [`lab02_increment_patrol.py`](lab02_increment_patrol.py) · [`../go2_patrol_helpers.py`](../go2_patrol_helpers.py)
- Day 1 avoid: [`../../day-02/lab-02/`](../../day-02/lab-02/)
- [ObstaclesAvoidClient](https://support.unitree.com/home/en/developer/ObstaclesAvoidClient)
