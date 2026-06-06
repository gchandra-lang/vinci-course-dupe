# Lab 2 — FSM, Motion Mode & Safety

**Duration:** ~30–45 min  
**Robot motion:** None by default — **read-only RPC** only  
**Prerequisites:** [Lab 1](../lab-01/) complete (`rt/lowstate` streaming)

---

## Learning objectives

1. Read locomotion **FSM id** and related sport RPC values without sending motion.
2. Use **`MotionSwitcherClient.CheckMode()`** and interpret `name='ai'`.
3. Relate **FSM id** to high-level readiness (especially **FSM = 1 damp**).
4. Document recovery steps before [Lab 3](../lab-03/) motion commands.

---

## 1. Concepts

### Two layers of “mode”

| Layer | API | What it tells you |
|-------|-----|-------------------|
| **Motion switcher** | `MotionSwitcherClient.CheckMode()` | Which sport profile is active (expect **`ai`** for high-level SDK) |
| **Loco FSM** | `LocoClient` RPC `7001` GET FSM id | Finite-state machine phase (stand, damp, walk, …) |

Lab 1 proved the **DDS topic** path (`rt/lowstate`). Lab 2 uses the **RPC** path to the `"sport"` service — same service `LocoClient` uses in Lab 3, but we only call **GET** APIs here.

### FSM ids you will see (from SDK helpers)

| FSM id | SDK helper | Typical meaning for labs |
|--------|------------|---------------------------|
| **1** | `Damp()` | **Damp** — high-level wave/walk usually **blocked** |
| **0** | `ZeroTorque()` | Zero torque |
| **3** | `Sit()` | Sit |
| **500** | `Start()` | Start locomotion stack |
| **706** | `Squat2StandUp()` / `StandUp2Squat()` | Squat ↔ stand transitions |
| **802** | *(no named helper)* | Often seen when standing and ready (robot-dependent) |

Other ids may appear during transitions. Treat any **`fsm_id != 1`** with `CheckMode → ai` as a good sign before Lab 3.

### RPC API ids (`g1_loco_api.py`)

| ID | Name |
|----|------|
| 7001 | GET FSM id |
| 7002 | GET FSM mode |
| 7003 | GET balance mode |
| 7004 | GET swing height |
| 7005 | GET stand height |

The upstream `LocoClient` exposes **Set** helpers (`SetFsmId`, `Move`, …) but reads use `_Call(700x, "{}")` — our lab script wraps that pattern.

---

## 2. Hands-on

### Step 0 — Session setup

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/repo
```

### Step 1 — Read-only report

```bash
python day-05/lab-02/fsm_readonly.py en6
```

**Expected sections:**

1. `[DDS topic]` — `rt/lowstate: OK`
2. `[Motion switcher RPC]` — `CheckMode: OK  name='ai'`
3. `[LocoClient RPC]` — FSM id, mode, balance, heights
4. `Readiness: PASS` — ready for Lab 3

### Step 2 — Watch FSM during a safe state change (supervised)

With instructor approval, put the robot in **damp** via remote — then stand it again. In another terminal:

```bash
python day-05/lab-02/fsm_readonly.py en6 --watch 30
```

Observe FSM id change **away from 1** when the robot is ready.

### Step 3 — Compare with connection check

```bash
python day-05/lab-00/g1_connection_check.py --interface en6 --skip-multicast
```

Values should match Lab 2’s FSM and `CheckMode` lines.

---

## 3. Exercises

### Exercise A — Damp vs ready

Record FSM id and readiness line when:

1. Robot is hanging or freshly powered in damp  
2. Robot is standing on the floor with sport mode `ai`

### Exercise B — lowstate vs FSM

When FSM = 1 (damp), does `rt/lowstate` still stream? (Yes — topic is independent of FSM.) Run Lab 1 and Lab 2 back-to-back and note both still work.

### Exercise C — Recovery plan (written)

Write 3 bullet steps you would use if Lab 2 reports `FSM=1` before Lab 3. Include when to use the remote vs PC.

<details>
<summary>Example answer</summary>

- Confirm feet on floor and clear space  
- Stand robot: remote **L1+UP** if paired, or wait for automatic stand after power-on  
- Re-run `fsm_readonly.py` until `Readiness: PASS` (FSM ≠ 1, `ai`)  
- Only then open Lab 3  

</details>

---

## 4. Safety — recovery without Lab 3 motion

This lab script **never** calls `SetFsmId`, `Move`, or `Damp`. Recovery is manual:

| Situation | Action |
|-----------|--------|
| FSM = 1 (damp) | Stand robot; avoid `Damp()` in examples until intentional |
| CheckMode ≠ `ai` | See field guide — `SelectMode('ai')` if needed after low-level use |
| DDS fails | Return to [Lab 0](../lab-00/) |

Optional PC-side recovery (Lab 3 only, clear space): `LocoClient().Start()` → `SetFsmId(500)`. Not exercised in Lab 2.

---

## 5. Troubleshooting

| Symptom | Action |
|---------|--------|
| `Readiness: PARTIAL` FSM=1 | Normal in damp; recover per §4 |
| CheckMode fails | Robot service / DDS RPC; power-cycle if stuck |
| lowstate FAIL | Fix Lab 0 network before debugging FSM |
| FSM id unlike table | Log the value; transitions are OK if readiness is PASS |
| GET balance/height `code=7301` | Optional RPC on some builds; FSM id + CheckMode are enough |

---

## 6. Deliverable

Submit:

- Full output of `fsm_readonly.py en6` with `Readiness: PASS` (or PARTIAL + your recovery notes)
- Exercise A table (two FSM ids)
- Exercise C recovery bullets

---

## 7. Next lab

**[Lab 3 — Interactive FSM & LocoClient actions](../lab-03/)**  
Supervised motion: shake hand, read/set FSM — requires **Readiness: PASS** here.

---

## References

- [Lab 1](../lab-01/) · [Lab 0](../lab-00/)
- [`fsm_readonly.py`](fsm_readonly.py) · [`g1_connection_check.py`](../lab-00/g1_connection_check.py)
- [Unitree `LocoClient` API](https://github.com/unitreerobotics/unitree_sdk2_python/blob/master/unitree_sdk2py/g1/loco/g1_loco_client.py)
