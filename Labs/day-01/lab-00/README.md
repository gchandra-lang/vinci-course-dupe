# Lab 0 — Environment, Architecture & Readiness

**Duration:** ~45–60 min (theory + checks)  
**Robot required:** Optional for Sections A–C; **required** for Section D  
**Motion:** None

**PDF coverage (Day 1):** GO2 introduction · development environment · basic operations

This lab is **Python + CycloneDDS only**. Optional ROS 2 (RViz, Nav2, etc.): [`docs/ROS2-INSTALL.md`](../../../docs/ROS2-INSTALL.md) at the repo root.

---

## Learning objectives

By the end of Lab 0 you should be able to:

1. Describe how your PC talks to Go2 over **Ethernet** and **DDS** (not ROS).
2. Explain why Go2 code uses **`unitree_go`** IDL types and **`SportClient`** for high-level control.
3. Install and verify **`unitree_sdk2_python`** + CycloneDDS on your machine.
4. Run readiness checks and interpret **PASS** / **PARTIAL** / **FAIL**.
5. State safety rules before any lab that sends motion commands (Lab 2+).

---

## 1. Go2 system architecture (conceptual)

The Go2 is a quadruped with an onboard computer (typically Jetson) on a fixed subnet. Your laptop joins that LAN over **wired Ethernet**.

```
┌─────────────────┐     Ethernet      ┌──────────────────────────────┐
│  Your PC        │   192.168.123.x   │  Go2 onboard (Jetson)        │
│  Python SDK     │ ◄──────────────► │  192.168.123.161 (typical)   │
│  CycloneDDS     │   UDP multicast   │  DDS topics + RPC services   │
└─────────────────┘                   └──────────────────────────────┘
```

| Role | Typical address | Notes |
|------|-----------------|-------|
| Your PC | e.g. `192.168.123.98/24` | Static IP on the port cabled to the robot |
| Go2 onboard | `192.168.123.161` | Ping before trusting DDS |
| Interface arg | e.g. `en6` (macOS), `enp0s31f6` (Linux) | Passed to `ChannelFactoryInitialize(0, iface)` — **not** the robot IP |

**Do not** pass `192.168.123.161` into `ChannelFactoryInitialize`. DDS discovery uses multicast on the robot subnet once your PC is on the correct NIC.

### Communication model (SDK2)

| Pattern | Use on Go2 | Example |
|---------|------------|---------|
| **Topic subscribe** | High-rate robot state | `rt/sportmodestate` → `SportModeState_` |
| **Topic subscribe** | Joints, IMU, power | `rt/lowstate` → `LowState_` (`unitree_go`) |
| **RPC client** | High-level sport commands | `SportClient` → `Move`, `StandUp`, … |

The Python SDK mirrors the C++ SDK2: same topic names and RPC clients as upstream examples under `example/go2/`.

### Go2 vs G1 in this camp (do not mix)

| | Go2 (Day 1) | G1 (Day 5+) |
|--|-------------|-------------|
| IDL | **`unitree_go`** | **`unitree_hg`** |
| High-level client | **`SportClient`** | **`LocoClient`** |
| Primary state topic (labs) | **`rt/sportmodestate`** | **`rt/lowstate`** |
| `CheckMode` name | Often **`mcf`** | Expect **`ai`** |

If G1 and Go2 share a lab network, read [G1 vs Go2 §4](../../../docs/G1-vs-GO2.md#4-lab-topology-one-switch-vs-two) (duplicate `.161` pitfall).

---

## 2. Software stack

```
Your lab scripts (course/day-01/)
        │
        ▼
unitree_sdk2py          ← pip install -e vendor/unitree_sdk2_python
        │
        ├── core.channel       ChannelFactoryInitialize, pub/sub
        ├── go2.sport            SportClient (high-level locomotion)
        ├── go2.obstacles_avoid  (Lab 4)
        ├── go2.video, vui, robot_state
        └── idl.unitree_go       SportModeState_, LowState_, …
        │
        ▼
CycloneDDS 0.10.x       ← CYCLONEDDS_HOME must point to install prefix
```

### 2.1 Clone and install (once per machine)

From the **repo root**:

```bash
conda create -n unitree_env python=3.11 -y
conda activate unitree_env
cd /path/to/vinci-unitree

cd vendor && git clone https://github.com/unitreerobotics/unitree_sdk2_python.git && cd ..
./scripts/setup_unitree_sdk.sh
```

Add to `~/.bashrc` or `~/.zshrc`:

```bash
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
```

Official install FAQ (CycloneDDS not found):  
https://github.com/unitreerobotics/unitree_sdk2_python#faq

### 2.2 Lab 0 script — verify **without** the robot

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/vinci-unitree

python course/day-01/New-lab/lab-00/lab00_readiness.py
```

**Expected:** environment PASS, vendor tree PASS, Go2 imports PASS, `verify_install.py` PASS, summary **machine ready**.

Equivalent manual check:

```bash
python scripts/verify_install.py
python scripts/verify_install.py --dds-test   # optional local pub/sub
```

### 2.3 Explore the upstream Go2 layout

After clone, skim these paths (read-only — do not edit `vendor/`):

| Path | Purpose |
|------|---------|
| `example/go2/high_level/go2_sport_client.py` | Interactive sport menu (Lab 2) |
| `example/go2/front_camera/camera_opencv.py` | Front camera (Lab 3) |
| `example/obstacles_avoid/obstacles_avoid_switch.py` | Avoidance (Lab 4) |
| `unitree_sdk2py/go2/sport/sport_client.py` | `SportClient` API |

Optional DDS tutorial (no robot): `example/helloworld/publisher.py` + `subscriber.py` in two terminals.

---

## 3. High-level sport API (preview)

Day 1 Labs 2–4 use **`SportClient`** — RPC to the onboard sport service.

| Category | Methods (examples) | Notes |
|----------|-------------------|--------|
| **Posture** | `StandUp()`, `StandDown()`, `BalanceStand()`, `RecoveryStand()` | Lab 2 menu |
| **Velocity** | `Move(vx, vy, vyaw)`, `StopMove()` | Sustained move may need periodic sends (upstream docs) |
| **Modes** | `Damp()`, `FreeAvoid(True/False)` | **Avoid `Damp()`** in labs unless recovering |
| **Readiness** | `Init()`, timeout via `SetTimeout()` | Used in connection check |

Menu ids in `go2_sport_client.py` (for reference):

| Id | Name | Lab use |
|----|------|---------|
| 9 | `balanced stand` | Safe first motion (Lab 2) |
| 1 | `stand_up` | OK with supervision |
| 6 | `stop_move` | Stop after move tests |
| 0 | `damp` | **Avoid** — blocks normal sport until recovered |
| 11–12, 19 | flips / jump | **Not for training** |

Details: [Sports services](https://support.unitree.com/home/en/developer/sports_services) · [`docs/GO2-FIELD-GUIDE.md`](../../../docs/GO2-FIELD-GUIDE.md)

---

## 4. Safety and operating rules

Read before any lab that moves the robot.

1. **Clear space** — ~2 m around the dog; flat floor; no loose cables.
2. **Wired Ethernet** — robot LAN only; confirm NIC with `ip -br addr` or `ifconfig`.
3. **Power-on wait** — ~1 minute after boot before RPC.
4. **Do not call `Damp()` casually** — recovery needs `stand_up`, `balanced stand`, or remote.
5. **High-level vs low-level** — Day 1 uses **sport** first. Low-level examples need sport disabled in the Unitree app (upstream `example/go2/low_level/`).
6. **Shared lab** — only one robot at `192.168.123.161` per switch, or renumber IPs — see [G1 vs Go2](../../../docs/G1-vs-GO2.md).
7. **Emergency** — know power switch and remote estop; spotter for first motion (Lab 2+).

Official sport example warning:

> *Please ensure there are no obstacles around the robot while running this example.*

---

## 5. Hands-on checklist

Work through **A → D**. Tick each box in your notes.

### A. Machine setup (no robot)

- [ ] `conda activate unitree_env`
- [ ] `export CYCLONEDDS_HOME="$HOME/cyclonedds/install"`
- [ ] `unset CYCLONEDDS_URI`
- [ ] `python course/day-01/New-lab/lab-00/lab00_readiness.py` → **machine ready**
- [ ] `vendor/unitree_sdk2_python/example/go2/high_level/go2_sport_client.py` exists

### B. Network preparation (robot powered, PC wired)

Replace `en6` with your interface (`enp0s31f6` on Linux — see [Go2 Field Guide §macOS](../../../docs/GO2-FIELD-GUIDE.md)).

- [ ] Static IP on robot subnet, e.g. `192.168.123.98/24`
- [ ] `ping -c 2 192.168.123.161` → replies
- [ ] Cable goes to **this** Go2 (not another robot on the same `.161`)

### C. Session environment (every robot day)

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/vinci-unitree
```

- [ ] Both exports active in the shell you will use for labs

### D. Readiness check (robot on)

```bash
python course/day-01/New-lab/lab-00/lab00_readiness.py en6
```

Or:

```bash
./scripts/go2_quickstart.sh en6
# python scripts/go2_connection_check.py --interface en6
```

| Result | Meaning | Next step |
|--------|---------|-----------|
| **PASS** (exit 0) | SDK, IP, ping, `sportmodestate`, `lowstate`, `SportClient.Init` | [Lab 1](../lab-01/) |
| **PARTIAL** (exit 2) | DDS + sport OK; unusual `CheckMode` | Read log; may still proceed to Lab 1; fix before Lab 2 motion |
| **FAIL** (exit 1) | SDK, IP, ping, or no DDS | [GO2 Field Guide](../../../docs/GO2-FIELD-GUIDE.md); do not run motion labs |

**Note:** Go2 `CheckMode` name **`mcf`** is normal — do not apply G1’s `'ai'` rule.

---

## 6. Knowledge check (self-test)

Answer without looking, then verify against Sections 1–3 or the field guide.

1. Which IDL package does Go2 use — `unitree_go` or `unitree_hg`?
2. Which DDS topic is the primary **high-level** sport state stream on Go2?
3. Which RPC client drives stand / walk / tricks in Day 1?
4. What onboard IP do you ping before trusting DDS?
5. Why must `CYCLONEDDS_URI` usually be **unset** when passing the interface name to `ChannelFactoryInitialize(0, iface)`?

<details>
<summary>Answers</summary>

1. **`unitree_go`**
2. **`rt/sportmodestate`** (`SportModeState_`)
3. **`SportClient`**
4. **`192.168.123.161`** (typical)
5. A preset URI can bind DDS to the wrong interface; camp examples use the **NIC name** only

</details>

---

## 7. Deliverable

For Lab 0 submission (notebook / wiki / PR comment):

- Log snippet: `lab00_readiness.py` (no iface) → **machine ready**
- Log snippet: `lab00_readiness.py en6` → **PASS** or **PARTIAL** with one-line explanation
- Your PC **interface name** and **IP** on `192.168.123.0/24`
- One sentence: what you would check if `rt/sportmodestate` never arrives

---

## 8. Next lab

**[Lab 1 — DDS observation (`rt/sportmodestate`)](../lab-01/)**  
Subscribe to sport mode state, estimate rate, and optional `rt/lowstate` — still no motion commands.

---

## References

- Repo: [GO2 Field Guide](../../../docs/GO2-FIELD-GUIDE.md) · [G1 vs Go2](../../../docs/G1-vs-GO2.md)
- Script: [`lab00_readiness.py`](lab00_readiness.py) · [`scripts/go2_connection_check.py`](../../../scripts/go2_connection_check.py)
- Upstream: [unitree_sdk2_python](https://github.com/unitreerobotics/unitree_sdk2_python) · [Quick start](https://support.unitree.com/home/en/developer/Quick_start)
