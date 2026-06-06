# Lab 2 — Scripted arm action sequence

**Duration:** ~45–60 min  
**Robot motion:** Yes — default `face wave` then `release arm`; optional custom sequences  
**Prerequisites:** [Lab 1](../lab-01/) complete; [Day 5 Lab 2](../../day-05/lab-02/) **Readiness: PASS**

---

## Learning objectives

1. Call **`G1ArmActionClient.ExecuteAction`** from a **script** (not only the Lab 1 menu).
2. Relate static **`action_map`** to optional firmware **`GetActionList()`**.
3. Build **multi-step sequences** with pauses; end with **`release arm`**.
4. Use built-in **readiness checks** (`--dry-run`) before sending motion.

---

## 1. Concepts

### Script flags

| Flag | Robot? | Purpose |
|------|--------|---------|
| `--show-map` | No | Print all `action_map` name → id pairs |
| `--dry-run` | Yes | Readiness check only; no `ExecuteAction` |
| `--list-actions` | Yes | Call `GetActionList()` on firmware (may fail on some builds) |
| `--sequence "a,b,c"` | Yes | Comma-separated action names |
| `--pause SEC` | Yes | Sleep between steps (default 3 s) |

### Static action table (SDK — no robot)

Typical mapping (verify with `--show-map` after SDK updates):

| id | name |
|----|------|
| 11 | two-hand kiss |
| 17 | clap |
| 20 | heart |
| 25 | face wave |
| 26 | high wave |
| 27 | shake hand |
| 99 | release arm |

### Default classroom sequence

```
readiness PASS → face wave → pause 3s → release arm
```

Avoid unsupervised **`hug`**, **`high five`**, or **`shake hand`** until the instructor extends the allowlist.

### Readiness gate (built into script)

Before any motion, the script checks:

- `rt/lowstate` streaming
- `CheckMode → ai`
- FSM id ≠ 1 (not damp)

Same criteria as [Day 5 `fsm_readonly.py`](../../day-05/lab-02/fsm_readonly.py).

---

## 2. Safety (required)

- Clear **≥ 2 m**; spotter for first run.
- Confirm Lab 1 completed without stuck arms.
- Custom `--sequence` values need **instructor approval** before running.

---

## 3. Hands-on

### Step 0 — Session setup

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/repo
```

### Step 1 — Map without the robot

```bash
python day-06/lab-02/arm_action_sequence.py --show-map
```

Save the output for your deliverable.

### Step 2 — Dry run at the robot

```bash
python day-06/lab-02/arm_action_sequence.py en6 --dry-run
```

**Expected:** `Readiness: PASS — lowstate OK, CheckMode ai, FSM=…`

### Step 3 — Firmware action list (optional)

```bash
python day-06/lab-02/arm_action_sequence.py en6 --list-actions
```

If code ≠ 0, note that firmware may not expose this API — rely on `--show-map`.

### Step 4 — Main sequence (default)

```bash
python day-06/lab-02/arm_action_sequence.py en6
```

**Expected:** readiness PASS, `face wave` code 0 with visible motion, pause, `release arm` code 0.

### Step 5 — Custom sequence (instructor-approved)

Names must match `action_map` keys exactly (spaces matter):

```bash
python day-06/lab-02/arm_action_sequence.py en6 \
  --sequence "high wave,clap,release arm" --pause 4
```

Example from script help:

```bash
python day-06/lab-02/arm_action_sequence.py en6 \
  --sequence "heart,release arm,two-hand kiss,release arm,reject,release arm" --pause 0.5
```

---

## 4. Exercises

### Exercise A — RPC trace

Open `unitree_sdk2py/g1/arm/g1_arm_action_client.py`. Which API IDs correspond to `ExecuteAction` and `GetActionList`?

### Exercise B — Sequence design

Write a **three-step** sequence (names only, no run) that ends in **`release arm`** and avoids person-contact gestures. Get instructor sign-off before running.

### Exercise C — Return codes

If `ExecuteAction` returns **0** but nothing moves, list three things you would check first.

---

## 5. Troubleshooting

| Symptom | Action |
|---------|--------|
| Readiness FAIL | Same as Day 5 — fix `lowstate`, `CheckMode`, FSM before arm |
| `GetActionList` non-zero | Normal on some firmware; use `--show-map` |
| `Unknown action name` | Names are exact strings; use `--show-map` |
| `CYCLONEDDS_HOME is not set` | Export before running |
| Non-zero step return codes | Log which action failed; try `release arm`; re-check FSM |

---

## 6. Deliverable

Submit:

- Output of **`--show-map`**
- Output of **`--dry-run`** showing **Readiness: PASS**
- Either **`--list-actions`** JSON **or** one sentence explaining why it was unavailable
- Log of one successful run (default or approved custom `--sequence`)

---

## 7. Next lab

**[Lab 3 — Arm SDK streaming (`rt/arm_sdk`)](../lab-03/)**  
Low-level joint targets via DDS instead of RPC `"arm"`.

---

## References

- [Lab 1](../lab-01/) · [Day 5 Lab 2](../../day-05/lab-02/)
- [`arm_action_sequence.py`](arm_action_sequence.py)
- Upstream: [g1_arm_action_example.py](https://github.com/unitreerobotics/unitree_sdk2_python/blob/master/example/g1/high_level/g1_arm_action_example.py)
