# Day 5 — G1 Architecture, DDS & Safety

**Platform:** Unitree **G1** (EDU Plus / Ultimate-D)  
**Stack:** [`unitree_sdk2_python`](https://github.com/unitreerobotics/unitree_sdk2_python) + CycloneDDS

**Prerequisite:** B2 days or equivalent DDS experience (pub/sub vs RPC).

---

## What this day is for

G1 **system architecture**, **DDS pub/sub**, **FSM / motion-mode safety**, and a short **supervised LocoClient** exercise — before full locomotion and arm labs on [Day 6](../day-06/).

**By the end of Day 5** you should be able to:

- Bring up G1 Ethernet + `CYCLONEDDS_HOME` session.
- Subscribe to `rt/lowstate` and interpret mode fields (`tick`, `mode_machine`, IMU).
- Read FSM and `CheckMode` without sending motion.
- Run one supervised gesture (`ShakeHand`) and explain FSM recovery.
- State when it is safe to proceed to Day 6 motion labs.

---

## Lab sequence

| Lab | Folder | Motion? | Script | Focus |
|-----|--------|---------|--------|--------|
| **0** | [`lab-00/`](lab-00/) | No | [`g1_connection_check.py`](lab-00/g1_connection_check.py) | Architecture, stack, readiness checks |
| **1** | [`lab-01/`](lab-01/) | No | [`listen_lowstate.py`](lab-01/listen_lowstate.py) | DDS subscribe — `rt/lowstate` |
| **2** | [`lab-02/`](lab-02/) | No | [`fsm_readonly.py`](lab-02/fsm_readonly.py) | FSM id, `CheckMode`, readiness gate |
| **3** | [`lab-03/`](lab-03/) | **Yes** | [`setmode_action_fsm.py`](lab-03/setmode_action_fsm.py) | Interactive FSM read/set + `ShakeHand` |

Work through labs **in order**. Lab 3 requires **Readiness: PASS** from Lab 2 (`FSM ≠ 1`, `CheckMode → ai`).

**Arm control (next day):** [Day 6](../day-06/) Labs 1–4.

---

## Session setup (every lab)

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/repo
```

Set your NIC once per session (examples: `en6` on macOS, `enp0s31f6` on Linux):

```bash
export G1_INTERFACE=en6
```

Find the interface wired to the robot: `ip -br addr` or `ifconfig | grep 192.168.123` → look for `192.168.123.x` on your PC (not `192.168.123.161`, which is the robot).

---

## Quick start

```bash
# Lab 0 — full readiness (expect PASS or PARTIAL)
python day-05/lab-00/g1_connection_check.py --interface en6

# Lab 1 — first lowstate message
python day-05/lab-01/listen_lowstate.py en6 --once

# Lab 2 — FSM / CheckMode report
python day-05/lab-02/fsm_readonly.py en6

# Lab 3 — supervised motion menu (only after Lab 2 PASS)
python day-05/lab-03/setmode_action_fsm.py en6
```

---

## Key concepts (Day 5)

| Topic | G1 detail |
|-------|-------------|
| State stream | `rt/lowstate` → `LowState_` (**`unitree_hg`**, not Go2’s `unitree_go`) |
| High-level control | `LocoClient` → RPC service `"sport"` |
| Motion profile | `MotionSwitcherClient.CheckMode()` → expect **`ai`** |
| FSM damp | FSM id **1** blocks wave/walk until robot stands / FSM changes |
| Safety | Feet on floor; clear space; avoid `ZeroTorque()` and casual `Damp()` |

---

## Deliverables (day summary)

| Lab | Submit |
|-----|--------|
| 0 | `g1_connection_check.py` log (PASS or PARTIAL + notes); your interface name and IP |
| 1 | `listen_lowstate.py --once` snippet; approximate Hz from a 15s run |
| 2 | Full `fsm_readonly.py` output; damp vs ready FSM table |
| 3 | Supervised `ShakeHand` log/video; one-line descriptions of `Damp` / `SetFsmId` |

---

## References

| Resource | Link |
|----------|------|
| Unitree SDK (Python) | [github.com/unitreerobotics/unitree_sdk2_python](https://github.com/unitreerobotics/unitree_sdk2_python) |
| Quick start | [support.unitree.com — Quick start](https://support.unitree.com/home/en/developer/Quick_start) |
| Sports / locomotion services | [support.unitree.com — Sports services](https://support.unitree.com/home/en/developer/sports_services) |
| G1 examples (upstream) | [example/g1](https://github.com/unitreerobotics/unitree_sdk2_python/tree/master/example/g1) |

---

## Next day

**[Day 6 — G1 Arm Control](../day-06/)**  
Interactive and scripted arm actions + `rt/arm_sdk` — requires Day 5 Lab 2 **Readiness: PASS**.
