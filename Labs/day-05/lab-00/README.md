# Lab 0 — Environment, Architecture & Readiness

**Duration:** ~45–60 min (theory + checks)  
**Robot required:** Optional for Sections A–C; **required** for Section D if you run on-robot checks  
**Motion:** None in this lab  
**Prerequisites:** `unitree_sdk2py` installed; CycloneDDS built with `CYCLONEDDS_HOME` set

---

## Learning objectives

By the end of Lab 0 you should be able to:

1. Describe how your PC talks to G1 over Ethernet and DDS (not ROS topics).
2. Explain why G1 code uses `unitree_hg` IDL types and the `sport` locomotion service.
3. Install and verify `unitree_sdk2_python` + CycloneDDS on your machine.
4. Run the readiness checks and interpret PASS / PARTIAL / FAIL.
5. State the safety rules before any lab that sends motion commands.

---

## 1. G1 system architecture (conceptual)

The G1 is a humanoid with onboard computers on a fixed subnet. Your laptop joins that LAN over **wired Ethernet**.

```
┌─────────────────┐     Ethernet      ┌──────────────────────────────┐
│  Your PC        │   192.168.123.x   │  G1 onboard computers        │
│  Python SDK     │ ◄──────────────► │  e.g. locomotion @ .161       │
│  CycloneDDS     │   UDP multicast   │  DDS topics + RPC services   │
└─────────────────┘                   └──────────────────────────────┘
```

| Role | Typical address | Notes |
|------|-----------------|-------|
| Your PC | e.g. `192.168.123.51/24` | Static IP; same subnet as robot |
| Locomotion computer | `192.168.123.161` | Ping before trusting DDS |
| Dev computer (optional) | `192.168.123.164` | May not respond on all configs |

**Communication model (SDK2):**

| Pattern | Use on G1 | Example |
|---------|-----------|---------|
| **Topic subscribe** | High-rate robot state | `rt/lowstate` → `LowState_` (`unitree_hg`) |
| **Topic publish** | Low-level commands (Day 6+ / advanced) | `rt/lowcmd` |
| **RPC client** | High-level sport / loco commands | `LocoClient` → service `"sport"` |

The Python SDK mirrors the C++ SDK2: same service names, same JSON parameter payloads for RPC.

---

## 2. Software stack

```
Your lab scripts
        │
        ▼
unitree_sdk2py          ← pip install -e vendor/unitree_sdk2_python
        │
        ├── core.channel     ChannelFactoryInitialize, pub/sub
        ├── g1.loco            LocoClient (high-level locomotion)
        ├── g1.arm             (Day 6)
        └── idl.unitree_hg     G1 message types (LowState_, …)
        │
        ▼
CycloneDDS 0.10.x       ← CYCLONEDDS_HOME must point to install prefix
```

### Session environment (every robot day)

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/repo
```

Optional: `export G1_INTERFACE=en6` (macOS) or `enp0s31f6` (Linux) so lab scripts pick your NIC automatically.

---

## 3. High-level locomotion API (preview)

Day 5 focuses on **`LocoClient`** — RPC to the `"sport"` service.

| Category | Methods (examples) | RPC IDs |
|----------|-------------------|---------|
| **Read state** | `GetFsmId`, `GetBalanceMode`, `GetStandHeight` | 7001–7005 |
| **Set state** | `SetFsmId`, `SetVelocity`, `SetStandHeight` | 7101–7105 |
| **Gestures / tasks** | `SetTaskId` → `WaveHand`, `ShakeHand` | 7106 |
| **Convenience** | `Damp()`, `Start()`, `Move(vx,vy,vyaw)`, `StopMove()` | wraps `SetFsmId` / `SetVelocity` |

Important FSM shortcuts:

| Call | FSM id | Meaning |
|------|--------|---------|
| `Damp()` | 1 | Damp — **robot will not do high-level wave/walk** |
| `Start()` | 500 | Start locomotion stack |
| `Squat2StandUp()` | 706 | Squat → stand |
| `ZeroTorque()` | 0 | Zero torque |

You will use these in Labs 2–3; Lab 0 only needs the vocabulary.

---

## 4. Safety and operating rules

Read before any lab that moves the robot.

1. **Clear space** — 2 m around the robot; no loose cables; floor flat and dry.
2. **Feet on the ground** — do not hang the robot for high-level tests.
3. **Power-on wait** — allow ~1 minute after boot before RPC.
4. **Do not call `Damp()` casually** — FSM = 1 blocks wave/walk until recovered (stand + remote or `SetFsmId(500)`).
5. **High-level vs low-level** — this course uses **high-level** `LocoClient` first. Low-level motor commands can conflict with sport mode.
6. **Emergency** — know how to power off or use the remote estop; keep a spotter for first motion tests.

---

## 5. Hands-on

### Step 0 — Machine setup (no robot)

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
python -c "import unitree_sdk2py; print('OK')"
```

### Step 1 — Network preparation (robot powered, PC wired)

Replace `en6` with your interface (`enp0s31f6` on Linux, `en6` on macOS — find yours with `ip -br addr` or `ifconfig | grep 192.168.123`).

- Static IP on robot subnet, e.g. `192.168.123.51/24`
- `ping -c 2 192.168.123.161` → replies
- `unset CYCLONEDDS_URI`

### Step 2 — Readiness check (robot on, sport mode)

```bash
python day-05/lab-00/g1_connection_check.py --interface en6
```

Example with optional wave smoke test (clear space; FSM must not be 1):

```bash
python day-05/lab-00/g1_connection_check.py --interface en6 --try-wave
```

| Result | Meaning | Next step |
|--------|---------|-----------|
| **PASS** | SDK, IP, ping, `lowstate`, mode `ai`, FSM ≠ 1 | Proceed to [Lab 1](../lab-01/) |
| **PARTIAL** (exit 2) | Network + DDS OK but FSM=1 (damp) or wrong mode | Stand robot; re-run check |
| **FAIL** (exit 1) | SDK, IP, ping, or no `lowstate` | Fix per step hints; do not run motion labs |

The script checks (in order): SDK env → PC IP → ping → optional multicast → DDS `rt/lowstate` → `CheckMode('ai')` → FSM id.

---

## 6. Exercises

### Exercise A — Interface discovery

Record your PC interface name and IP on `192.168.123.0/24`. Why is the interface name **not** `192.168.123.161`?

### Exercise B — PASS vs PARTIAL

Run `g1_connection_check.py` and note the summary line. If PARTIAL, what FSM id did you see and what recovery would you try?

### Exercise C — IDL package (written)

Which IDL package does G1 use — `unitree_go` or `unitree_hg`? What happens if you subscribe to `rt/lowstate` with the wrong type?

<details>
<summary>Answer</summary>

G1 uses **`unitree_hg`**. Wrong type → no valid messages or garbage values.

</details>

---

## 7. Troubleshooting

| Symptom | Action |
|---------|--------|
| `CYCLONEDDS_HOME is not set` | `export CYCLONEDDS_HOME="$HOME/cyclonedds/install"` |
| No `192.168.123.x` on interface | Set static IP on the port wired to the robot |
| Ping failed | Power robot, check cable/switch |
| No `lowstate` in 8s | Robot on? `unset CYCLONEDDS_URI`; verify interface |
| FSM=1 (Damp) | Stand robot (feet on floor); remote L1+UP if paired; re-run check |
| `CheckMode` not `ai` | Stand robot; wait after power-on; see field guide |

---

## 8. Deliverable

Submit:

- Log snippet: `g1_connection_check.py` summary line (`PASS` or `PARTIAL` with explanation)
- Your PC interface name and IP on `192.168.123.0/24`
- One sentence: what you would do if `lowstate` never arrives

---

## 9. Next lab

**[Lab 1 — DDS observation (`rt/lowstate`)](../lab-01/)**  
Subscribe to robot state, print `mode_machine` and `tick`, and relate messages to the architecture above.
