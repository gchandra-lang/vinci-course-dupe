# Lab 3 — Volume get / set

**Duration:** ~15–25 min  
**Robot motion:** None — audio configuration only  
**Prerequisites:** [Lab 1](../lab-01/) or [Lab 2](../lab-02/) — `AudioClient` initialized successfully at least once

---

## Learning objectives

1. Read current speaker volume with **`GetVolume()`**.
2. Set volume to a value in **0–100** with **`SetVolume()`** and verify the change.
3. Use CLI flags **`--get`** and **`--set`** as mutually exclusive operations.
4. Choose a classroom-safe volume before WAV playback and TTS labs.

---

## 1. Concepts

### Volume RPC

| Method | Returns | Notes |
|--------|---------|-------|
| `GetVolume()` | `(code, data)` | `data['volume']` on success |
| `SetVolume(level)` | RPC result | Script clamps to **0–100** |

[`volume.py`](volume.py) behaviour:

- **`--get`** — print current volume only
- **`--set VOLUME`** — read original → set clamped value → read again → print confirmation

Example output for set:

```
Volume successfully set to 85 (original: 60).
```

### Why volume matters for Day 7

- Lab 2 **WAV playback** may be inaudible at low volume
- Lab 4 **TTS** should be comfortable for the room — avoid max volume in enclosed spaces
- Restore original volume after demos if your instructor requests it

---

## 2. Hands-on

### Step 0 — Session setup

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/repo
```

### Step 1 — Read current volume

```bash
python day-07/lab-03/volume.py en6 --get
```

**Expected:** `The current volume is <N>.`

Record this value as your **original** for the deliverable.

### Step 2 — Set volume

```bash
python day-07/lab-03/volume.py en6 --set 85
```

**Expected:** confirmation line with new and original values.

### Step 3 — Verify with get

```bash
python day-07/lab-03/volume.py en6 --get
```

Confirm the printed value matches what you set (or explain firmware rounding).

### Step 4 — Test with Lab 2 (optional)

Replay your WAV at the new volume:

```bash
python day-07/lab-02/audio.py en6 test.wav
```

---

## 3. Exercises

### Exercise A — Clamping

What happens if you run `--set 150` or `--set -10`? Run once and note the clamped result.

### Exercise B — Classroom policy

Write one sentence: what volume range would you use for a demo in a small lab vs a large hall?

### Exercise C — Error handling

If `GetVolume` returns a non-zero code, what Day 5 check would you run first?

---

## 4. Troubleshooting

| Symptom | Action |
|---------|--------|
| `one of the arguments --get --set is required` | Pass exactly one of `--get` or `--set` |
| `Error fetching volume. Code: …` | Check DDS/network; re-run Day 5 connection check |
| Set succeeds but get differs | Firmware may round; log both values |
| No audible change in Lab 2 | Volume may still be low; try `--set 70`–`85` |

---

## 5. Deliverable

- Output of `--get` before any changes
- Output of one `--set` run showing original and new volume
- Answer to Exercise A (clamping behaviour)

---

## 6. Next lab

**[Lab 4 — Text-to-speech + wave capstone](../lab-04/)**  
`TtsMaker` combined with `LocoClient.WaveHand()`.

---

## References

- [Lab 2](../lab-02/) · [Lab 1](../lab-01/) · [`volume.py`](volume.py)
- [Day 7 overview](../README.md)
