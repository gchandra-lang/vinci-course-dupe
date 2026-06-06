# Lab 1 — DDS Observation (`rt/lowstate`)

**Duration:** ~30–45 min  
**Robot motion:** None — subscribe only  
**Prerequisites:** [Lab 0](../lab-00/) connection check **PASS** on your interface

**PDF coverage:** Topics & messages · managing sensor data (state streams)

---

## Learning objectives

1. Explain the difference between **DDS topics** (streaming state) and **RPC** (request/response commands).
2. Subscribe to `rt/lowstate` with the correct G1 type: `LowState_` (`unitree_hg`).
3. Read `tick`, `mode_machine`, `mode_pr`, and IMU orientation from live messages.
4. Estimate publish rate and know when subscription fails (Lab 0 debugging path).

---

## 1. Concepts

### Pub/sub vs RPC

| Pattern | Direction | G1 example | Used for |
|---------|-----------|------------|----------|
| **Topic subscribe** | Robot → PC (stream) | `rt/lowstate` | Joint/IMU state, high rate |
| **Topic publish** | PC → Robot | `rt/lowcmd` | Low-level torque (advanced; not this lab) |
| **RPC client** | PC ↔ Robot (call) | `LocoClient` → `"sport"` | Stand, walk, wave (Lab 3+) |

Lab 1 uses **only** pub/sub. You are listening; you are not commanding motion.

### Topic and type

| Item | Value |
|------|--------|
| Topic name | `rt/lowstate` |
| IDL package | `unitree_hg` (G1 / H1-2) |
| Python type | `LowState_` from `unitree_sdk2py.idl.unitree_hg.msg.dds_` |

Go2 uses the same topic name with a **different** message layout (`unitree_go`). Wrong type → no messages or garbage.

Top-level `LowState_` fields (from SDK):

| Field | Role |
|-------|------|
| `version` | Message / firmware version bytes |
| `mode_pr` | Mode (PR) |
| `mode_machine` | Machine mode |
| `tick` | Monotonic counter (use for rate / freshness) |
| `imu_state` | Orientation, gyro, accel (`rpy`, etc.) |
| `motor_state` | Per-joint state array |
| `wireless_remote` | Remote input snapshot |

### DDS session (same as Lab 0)

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
```

```python
ChannelFactoryInitialize(0, "en6")  # YOUR NIC — not the robot IP
sub = ChannelSubscriber("rt/lowstate", LowState_)
sub.Init(callback, 10)  # queue depth 10
```

**Interface name** is the PC Ethernet port wired to G1 — it is **not** `192.168.123.161`. Names vary by machine:

| Source | Example name |
|--------|----------------|
| Linux laptop | `enp0s31f6`, `enx207bd22b611a` (USB Ethernet) |
| macOS | often `en6` |

Find yours: `ip -br addr` or `ifconfig | grep 192.168.123`. Optional: `export G1_INTERFACE=en6`.

---

## 2. Hands-on

### Step 1 — Quick readiness

```bash
cd /path/to/repo
python day-05/lab-00/g1_connection_check.py --interface en6 --skip-multicast
```

Expect **PASS** (or fix network/DDS per Lab 0).

### Step 2 — First message

```bash
python day-05/lab-01/listen_lowstate.py en6 --once
```

**Expected:** `First rt/lowstate received:` with `tick`, `mode_machine`, `imu_rpy`, `motors=…`.

### Step 3 — Stream for 15 seconds

```bash
python day-05/lab-01/listen_lowstate.py en6 --duration 15 --rate 1
```

Note the approximate **Hz** printed at the end. Typical rates are high (hundreds of Hz); your print rate is throttled by `--rate`.

### Step 4 — Compare with connection check

[`g1_connection_check.py`](../lab-00/g1_connection_check.py) subscribes to `rt/lowstate` and also calls `LocoClient` for FSM. This lab exposes the **same data path** with readable fields — the split before RPC motion in Lab 3 is intentional.

---

## 3. Exercises

### Exercise A — Rate

Run with `--duration 30` and record message count and Hz. What happens if you unplug Ethernet mid-run?

### Exercise B — Field watch

While the robot is standing, note `mode_machine` and `imu_rpy`. Gently tilt the torso (if safe and supervised). Do `imu_rpy` values change?

### Exercise C — Pub/sub vs RPC (written)

In 2–3 sentences: why does `g1_connection_check.py` use **both** `ChannelSubscriber("rt/lowstate")` and `LocoClient` for FSM?

<details>
<summary>Hint</summary>

`lowstate` proves the DDS **streaming** path is alive; `LocoClient` reads FSM via the sport **RPC** service — different channel than the topic alone.

</details>

### Exercise D — Wrong IDL (discussion)

What symptom would you expect if you used `unitree_go.LowState_` on G1 `rt/lowstate`?

<details>
<summary>Answer</summary>

No valid messages, decode errors, or nonsense values — always match IDL package to robot (G1 vs Go2).

</details>

---

## 4. Troubleshooting

| Symptom | Action |
|---------|--------|
| `Interface 'enp0s31f6' does not exist` | Use **your** NIC from `ip -br addr`, not a README placeholder |
| No message in 8s (after Lab 0 PASS) | `unset CYCLONEDDS_URI`; re-run Lab 0 |
| `ModuleNotFoundError: unitree_sdk2py` | `conda activate unitree_env`; install SDK |
| Wrong interface on macOS | `ifconfig \| grep 192.168.123` → often `en6` |
| `CYCLONEDDS_HOME is not set` | Export before running (see Lab 0) |

---

## 5. Deliverable

Submit:

- Log snippet: `listen_lowstate.py <your-iface> --once` (first line)
- Approximate Hz from a 15s run
- Answer to Exercise C

---

## 6. Next lab

**[Lab 2 — FSM, motion mode & safety](../lab-02/)**  
Read FSM id and `CheckMode('ai')` via RPC without sending motion commands.

---

## References

- [Lab 0](../lab-00/) · [`listen_lowstate.py`](listen_lowstate.py)
- [Unitree sports services](https://support.unitree.com/home/en/developer/sports_services)
