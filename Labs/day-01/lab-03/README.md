# Lab 3 — DDS observation (`rt/sportmodestate`)

**Duration:** ~30–45 min  
**Robot motion:** None — subscribe only  
**Prerequisites:** [Lab 0](../lab-00/) PASS · [Lab 1](../lab-01/)–[Lab 2](../lab-02/) ROS (recommended)

**PDF coverage:** Topics & messages · managing sensor data (state streams)

---

## Learning objectives

1. Explain the difference between **DDS topics** (streaming state) and **RPC** (request/response commands).
2. Subscribe to `rt/sportmodestate` with the correct Go2 type: `SportModeState_` (`unitree_go`).
3. Optionally subscribe to `rt/lowstate` with **`unitree_go`** `LowState_` (not G1’s `unitree_hg`).
4. Read `mode`, `gait_type`, velocity, and position from live sport messages.
5. Estimate publish rate and optionally save a **JSONL log** for inspection workflows.

---

## 1. Concepts

### Pub/sub vs RPC

| Pattern | Direction | Go2 example | Used for |
|---------|-----------|-------------|----------|
| **Topic subscribe** | Robot → PC (stream) | `rt/sportmodestate` | High-level sport / gait state |
| **Topic subscribe** | Robot → PC | `rt/lowstate` | Joints, IMU, BMS (proprioception) |
| **RPC client** | PC ↔ Robot | `SportClient` | Stand, move, tricks (Lab 2+) |

Lab 1 uses **only** pub/sub. You are listening; you are not commanding motion.

### Topics and types (Go2)

| Topic | Python type | IDL package |
|-------|-------------|-------------|
| `rt/sportmodestate` | `SportModeState_` | **`unitree_go`** |
| `rt/lowstate` | `LowState_` | **`unitree_go`** |

G1 camp uses the same topic name `rt/lowstate` with a **different** message layout (`unitree_hg`). Wrong type → no messages or garbage.

### `SportModeState_` fields (useful for Day 1)

| Field | Role |
|-------|------|
| `mode` | Sport / behaviour mode id |
| `gait_type` | Gait classification |
| `progress` | Motion task progress |
| `error_code` | Sport error flag |
| `body_height` | Body height estimate |
| `velocity` | `[vx, vy, vz]`-style body velocity components |
| `position` | Position components (frame per firmware) |
| `yaw_speed` | Yaw rate |
| `imu_state` | IMU snapshot inside sport state |

`rt/lowstate` adds `tick`, per-motor `motor_state`, `bms_state`, etc. — use `--lowstate` to print one sample.

### Managing sensor data

Treat DDS streams as **observations** you can log for inspection:

| Stream | Inspection role |
|--------|-----------------|
| `sportmodestate` | Where the dog thinks it is in sport mode, gait, velocity |
| `lowstate` | Joint/IMU health, power, `tick` for freshness |

Camp script supports `--log sportmodestate_log.jsonl` (one JSON object per printed line).

### DDS session (same as Lab 0)

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
```

```python
ChannelFactoryInitialize(0, "enx207bd22b611a")  # YOUR NIC — not the robot IP
sub = ChannelSubscriber("rt/sportmodestate", SportModeState_)
sub.Init(callback, 10)  # queue depth 10
```

**Interface name** is the PC Ethernet port wired to Go2 — it is **not** `192.168.123.161`. Names vary by machine:

| Source | Example name |
|--------|----------------|
| Linux laptop | `enp0s31f6`, `enx207bd22b611a` (USB Ethernet) |
| VMware / docs | `ens33` |
| macOS | often `en6` |

Find yours: `ip -br addr` and look for `192.168.123.x`. Optional: `export GO2_INTERFACE=enx207bd22b611a`.

`lab03_listen_sportmodestate.py` checks the NIC **before** DDS and prints suggestions if the name is wrong or missing `192.168.123.x`.

Official hello-world (no robot): `vendor/unitree_sdk2_python/example/helloworld/`

---

## 2. Hands-on

### Step 1 — Quick readiness

```bash
cd /path/to/vinci-unitree
python course/day-01/New-lab/lab-00/lab00_readiness.py enx207bd22b611a
# or:
python scripts/go2_connection_check.py --interface enx207bd22b611a --skip-multicast
```

Expect **PASS** (or fix network/DDS per Lab 0).

### Step 2 — First message

```bash
python course/day-01/New-lab/lab-03/lab03_listen_sportmodestate.py enx207bd22b611a --once
```

**Expected:** `First rt/sportmodestate received:` with `mode`, `gait_type`, `vel`, `pos`, etc.

### Step 3 — Stream for 10 seconds

```bash
python course/day-01/New-lab/lab-03/lab03_listen_sportmodestate.py enx207bd22b611a --duration 15 --rate 1
```

Note the approximate **Hz** printed at the end. Print rate is throttled by `--rate`; underlying DDS rate is usually higher.

### Step 4 — Lowstate + log (inspection data bundle)

```bash
python course/day-01/New-lab/lab-03/lab03_listen_sportmodestate.py enx207bd22b611a --duration 20 --rate 1 \
  --lowstate --log sportmodestate_log.jsonl
```

Confirm `sportmodestate_log.jsonl` exists and contains JSON lines with `mode`, `velocity`, `position`.

### Step 4b — Inspection fields on `lowstate` *(optional)*

```bash
python course/day-01/New-lab/lab-03/lab03_listen_sportmodestate.py enx207bd22b611a --once --inspect
```

**Expected:** first `lowstate` line includes `power_v`, `bms_soc`, and `wireless_remote` bytes (remote vs API debugging).

### Step 5 — Compare with connection check

`go2_connection_check.py` already subscribes to both topics for PASS. Lab 1 exposes the **same data path** with readable fields — the split before `SportClient` motion in Lab 2 is intentional.

---

## 3. Exercises

### Exercise A — Rate

Run with `--duration 30` and record message count and Hz. What happens if you unplug Ethernet mid-run?

### Exercise B — Field watch

While the robot is standing still, note `mode`, `gait_type`, and `velocity`. When a teammate gently commands a small move (Lab 2, supervised), do `velocity` components change on the next Lab 1 run?

### Exercise C — Pub/sub vs RPC (written)

In 2–3 sentences: why does `go2_connection_check.py` use **both** `ChannelSubscriber("rt/sportmodestate")` and `SportClient.Init()`?

<details>
<summary>Hint</summary>

`sportmodestate` proves the DDS **streaming** path is alive; `SportClient` proves the sport **RPC** service answers — different channel than the topic alone.

</details>

### Exercise D — Wrong IDL (discussion)

What symptom would you expect if you used `unitree_hg.LowState_` on Go2 `rt/lowstate`?

<details>
<summary>Answer</summary>

No valid messages, decode errors, or nonsense values — always match IDL package to robot line ([G1 vs Go2](../../../docs/G1-vs-GO2.md)).

</details>

---

## 4. Troubleshooting

| Symptom | Action |
|---------|--------|
| `Interface 'enp0s31f6' does not exist` | Use **your** NIC from `ip -br addr`, not a README placeholder |
| `no 192.168.123.x on interface` | Set static IP on the Go2 cable port; script lists other NICs on robot LAN |
| `ping 192.168.123.161 failed` | Power/cable; confirm only one robot on `.161` |
| No message in 8s (after preflight PASS) | `unset CYCLONEDDS_URI`; try another interface from script hints |
| `ModuleNotFoundError: unitree_sdk2py` | `conda activate unitree_env`; `./scripts/setup_unitree_sdk.sh` |
| Wrong interface on macOS | `ifconfig \| grep 192.168.123` → often `en6` |
| `--lowstate` never prints | Wait full `--duration`; lowstate may arrive after sport; re-run with `--once --lowstate` |

---

## 5. Deliverable

Submit:

- Log snippet: `lab03_listen_sportmodestate.py <your-iface> --once` (first line)
- Approximate Hz from a 15s run
- Optional: first line of `sportmodestate_log.jsonl`
- Answer to Exercise C

---

## 6. Next lab

**[Lab 2 — Sport RPC & readiness](../lab-02/)**  
`SportClient`, `CheckMode`, and supervised sport menu — still minimal motion.

---

## References

- [Lab 0](../lab-00/) · [`lab01_listen_sportmodestate.py`](lab01_listen_sportmodestate.py)
- [GO2 Field Guide](../../../docs/GO2-FIELD-GUIDE.md) · [G1 vs Go2](../../../docs/G1-vs-GO2.md)
- [G1 Lab 1 (pattern)](../../day-05/lab-01/)
