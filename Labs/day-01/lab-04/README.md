# Lab 4 — SDK sport RPC & motion modes (read-only)

**TtT Day 1 · afternoon SDK block**  
**Robot required:** Yes (Ethernet)  
**Motion:** None — no `StandUp` / `Move` in this lab

## Objectives

- Connect **SportClient** and **MotionSwitcherClient** without sending motion.
- Read **CheckMode** (Go2 often reports `mcf` — not G1’s `ai`).
- Confirm DDS + RPC before [Lab 5](../lab-05/) stand/walk.

## Prerequisites

- [Lab 0](../lab-00/) and [Lab 3](../lab-03/) PASS on your interface
- `conda activate unitree_env`, `CYCLONEDDS_HOME` set, `CYCLONEDDS_URI` unset

## Ethernet interface

Pass the **PC NIC** cabled to Go2 (not `192.168.123.161`). Examples: `enx207bd22b611a`, `enp0s31f6`, `ens33` (VM). Find yours: `ip -br addr` → `192.168.123.x`.

```bash
export GO2_INTERFACE=enx207bd22b611a   # recommended once per session
```

The script validates the interface (exists, robot subnet IP, ping) before DDS/RPC. If you **omit** the argument and exactly one NIC has `192.168.123.x`, that interface is chosen automatically.

## Steps

```bash
python3 course/day-01/New-lab/lab-04/lab04_sport_readonly.py
python3 course/day-01/New-lab/lab-04/lab04_sport_readonly.py enx207bd22b611a --watch 10
```

## What to observe

| Check | Meaning |
|-------|---------|
| `rt/sportmodestate` | DDS stream OK |
| `SportClient.Init` | Sport RPC service reachable |
| `CheckMode` name | Current motion mode (e.g. `mcf`) |

## Deliverable

Note your **CheckMode** name and one line: how RPC differs from the topic subscribe in Lab 3.

## Troubleshooting

| Message | Fix |
|---------|-----|
| Interface does not exist | `ip -br addr` — use the name that has `192.168.123.x` |
| No `192.168.123.x` on interface | Static IP on the Go2 port; script lists other candidate NICs |
| Ping failed | Robot on, correct cable, [GO2 Field Guide](../../../docs/GO2-FIELD-GUIDE.md) |

**Next:** [Lab 5 — stand + short walk](../lab-05/)
