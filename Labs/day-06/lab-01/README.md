# Lab 1 — Interactive arm actions (`G1ArmActionClient`)

**Duration:** ~30–45 min  
**Robot motion:** Yes — arm gestures; supervision required  
**Prerequisites:** [Day 5 Lab 2](../../day-05/lab-02/) **Readiness: PASS** (`FSM ≠ 1`, `CheckMode → ai`)

---

## Learning objectives

1. Use **`G1ArmActionClient`** to send discrete arm gestures via RPC service **`"arm"`**.
2. Navigate the interactive menu and map gesture names to **`action_map`** ids in the SDK.
3. Practice **`release arm`** after contact-style gestures (shake hand, hug, heart, …).
4. Compare high-level arm RPC to locomotion gestures from Day 5 Lab 3.

---

## 1. Concepts

### `G1ArmActionClient` → RPC service `"arm"`

| Method | Role |
|--------|------|
| `Init()` | Register API version and method IDs |
| `ExecuteAction(action_id)` | Send one discrete gesture by numeric id |

Names like `"face wave"` map to ids via **`action_map`** in `unitree_sdk2py.g1.arm.g1_arm_action_client`. Return **code `0`** means the RPC layer accepted the call — always watch the physical robot.

### Menu options (this lab script)

| id | name | Notes |
|----|------|-------|
| 0 | release arm | Return arms to neutral — use after gestures |
| 1 | shake hand | Auto `release arm` after 2 s |
| 2 | high five | Auto `release arm` after 2 s |
| 3 | hug | Auto `release arm` after 2 s |
| 4 | high wave | Continuous until next command |
| 5 | clap | |
| 6 | face wave | Good classroom demo |
| 7–15 | kiss, heart, hands up, x-ray, … | Supervised only |

Type **`list`** at the prompt to print all options.

### Why this lab matters

The official upstream example is interactive. Understanding the menu prepares you for Lab 2, where the same actions run from a **scripted sequence** with a readiness gate.

---

## 2. Safety (required)

- Clear **≥ 2 m** around the robot; ceiling clearance for raised arms.
- Robot **feet on the floor** — standing stable.
- **Spotter** mandatory for first run.
- Avoid person-contact gestures (`hug`, `high five`, `shake hand`) until instructor approval.
- Always finish with **`release arm`** (id `0`) before leaving the session.

---

## 3. Hands-on

### Step 0 — Confirm readiness

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/repo

python day-05/lab-02/fsm_readonly.py en6
```

Expect **Readiness: PASS**.

### Step 1 — Run the interactive menu

```bash
python day-06/lab-01/g1_arm_action_example.py en6
```

- Press **Enter** at the safety prompt.
- Type **`list`** to see all gesture names and ids.
- Enter an **id** or **name** to execute.

Suggested sequence (supervised):

1. `6` or `face wave` — visible arm wave
2. `0` or `release arm` — return to neutral
3. `5` or `clap` — short gesture
4. `0` — release again

### Step 2 — Observe auto-release behaviour

Some options (e.g. `shake hand`, `heart`) call **`release arm`** automatically after 2 seconds. Others (`face wave`, `clap`) do not — you must release manually.

### Step 3 — Re-check readiness

```bash
python day-05/lab-02/fsm_readonly.py en6
```

Confirm FSM is still ≠ 1 before proceeding to Lab 2.

---

## 4. Exercises

### Exercise A — action_map lookup

Open `unitree_sdk2py/g1/arm/g1_arm_action_client.py` and find the numeric id for `"face wave"` and `"release arm"`. Do they match what the menu prints?

### Exercise B — RPC vs LocoClient

In 2–3 sentences: how is `G1ArmActionClient.ExecuteAction` different from Day 5’s `LocoClient.ShakeHand()`?

### Exercise C — Release discipline

Which menu ids auto-call `release arm`? Why does the official example release after contact-style gestures?

---

## 5. Troubleshooting

| Symptom | Action |
|---------|--------|
| Readiness FAIL | Fix Day 5 — FSM damp, wrong CheckMode, or no `lowstate` |
| `ExecuteAction` code 0, no motion | FSM may be damp; re-run Day 5 Lab 2; try `release arm` first |
| Arms stuck after session | Run option `0` (`release arm`); if needed, power-cycle with instructor |
| Import / CycloneDDS errors | Activate `unitree_env`; set `CYCLONEDDS_HOME` |
| Wrong interface | Use PC NIC with `192.168.123.x`, not robot IP |

---

## 6. Deliverable

- Log showing **`list`** output and two supervised gestures with **`release arm`** at the end
- Answer to Exercise B
- Confirmation that Readiness was **PASS** before and after the lab

---

## 7. Next lab

**[Lab 2 — Scripted arm action sequence](../lab-02/)**  
Same RPC client, but automated sequences with `--dry-run`, `--show-map`, and custom `--sequence`.

---

## References

- [Day 5 Lab 2](../../day-05/lab-02/) · [`g1_arm_action_example.py`](g1_arm_action_example.py)
- Upstream: [g1_arm_action_example.py](https://github.com/unitreerobotics/unitree_sdk2_python/blob/master/example/g1/high_level/g1_arm_action_example.py)
