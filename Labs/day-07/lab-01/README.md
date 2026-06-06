# Lab 1 — Chest RGB LED control

**Duration:** ~20–30 min  
**Robot motion:** None — LED colours only  
**Prerequisites:** [Day 5 Lab 0](../../day-05/lab-00/) connection check **PASS**; DDS session working

---

## Learning objectives

1. Initialize **`AudioClient`** and call **`LedControl(r, g, b)`** for chest RGB LEDs.
2. Confirm DDS connectivity via **`rt/lowstate`** before sending RPC commands.
3. Interpret RPC **return codes** for each LED step.
4. Explain why LED control shares the **`AudioClient`** API (same onboard hardware board).

---

## 1. Concepts

### `AudioClient` → speaker + LED hardware

On G1, the chest **RGB LED strip** and **speaker** are managed through the same RPC client:

| Method | Role |
|--------|------|
| `Init()` | Connect to audio/LED service |
| `LedControl(r, g, b)` | Set chest LED colour; each channel **0–255** |
| `GetVolume()` / `SetVolume()` | Speaker level (Lab 3) |
| `TtsMaker(text, id)` | Text-to-speech (Lab 4) |
| `PlayStream(...)` | PCM audio chunks (Lab 2) |

This lab uses **only** `LedControl`. No locomotion or arm commands are sent.

### Script sequence

[`led.py`](led.py) runs four steps with **1.5 s** between colours:

1. Red — `(255, 0, 0)`
2. Green — `(0, 255, 0)`
3. Blue — `(0, 0, 255)`
4. Off — `(0, 0, 0)`

Each step prints a **return code** (`0` = success at RPC layer).

### DDS preflight

The script waits up to **5 s** for `rt/lowstate` before calling `AudioClient`. If no messages arrive, fix networking per [Day 5 Lab 0](../../day-05/lab-00/) before debugging LEDs.

---

## 2. Hands-on

### Step 0 — Session setup

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/repo
```

### Step 1 — Quick connectivity

```bash
python day-05/lab-00/g1_connection_check.py --interface en6 --skip-multicast
```

### Step 2 — Run LED sequence

```bash
python day-07/lab-01/led.py en6
```

**Expected:**

- `DDS: rt/lowstate OK`
- Four `LedControl` steps with `return code: 0`
- Visible colour change on chest LED strip
- `Done. LED test sequence completed.`

### Step 3 — Observe timing

Watch the robot during the 1.5 s pauses. Note whether colours blend visually or switch sharply (firmware-dependent).

---

## 3. Exercises

### Exercise A — Custom colour

Pick one RGB triplet (e.g. orange `(255, 128, 0)`) and predict what the chest LED should look like. *(Do not modify the script unless instructor allows — answer on paper.)*

### Exercise B — Shared client

Why does LED control use `AudioClient` instead of a separate `LedClient`? (Hint: onboard hardware integration.)

### Exercise C — Failure modes

If `LedControl` returns non-zero but DDS is OK, list two things you would check (volume service, robot power state, …).

---

## 4. Troubleshooting

| Symptom | Action |
|---------|--------|
| `FAIL: no rt/lowstate in 5s` | Fix Day 5 network/DDS; verify interface |
| `CYCLONEDDS_HOME is not set` | Export before running |
| Non-zero return codes | Power-cycle robot audio board; retry after 1 min boot wait |
| No visible LED change, code 0 | Confirm you are looking at **chest** strip; check brightness in room |
| Import error | `conda activate unitree_env` |

---

## 5. Deliverable

- Log snippet showing all four `LedControl` steps with return code **0**
- Answer to Exercise B (one sentence)
- Photo of chest LED on one colour (optional)

---

## 6. Next lab

**[Lab 2 — WAV file playback](../lab-02/)**  
Stream 16 kHz mono audio through `PlayStream`.

---

## References

- [Day 7 overview](../README.md) · [`led.py`](led.py)
- [Day 5 Lab 0](../../day-05/lab-00/)
