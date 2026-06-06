# Day 7 — G1 Audio, Speech, LED & Capstone

**Platform:** Unitree **G1** (EDU Plus / Ultimate-D)  
**Stack:** [`unitree_sdk2_python`](https://github.com/unitreerobotics/unitree_sdk2_python) + CycloneDDS

**Prerequisite:** [Day 5](../day-05/) DDS session working; [Day 6](../day-06/) arm labs recommended.

---

## What this day is for

G1 **peripheral I/O** through the **`AudioClient`** RPC service — chest **RGB LEDs**, **WAV playback**, **volume**, and **text-to-speech** — ending with a **gesture + speech** capstone.

**By the end of Day 7** you should be able to:

- Control chest RGB LEDs via `AudioClient.LedControl(r, g, b)`.
- Stream **16 kHz mono PCM** from a `.wav` file with `PlayStream`.
- Read and set speaker volume (`GetVolume` / `SetVolume`).
- Run **`TtsMaker`** in Chinese or English and combine it with a **`LocoClient`** wave.

**Out of scope:** Dexterous hand control. Capstone **manipulation** = arm gestures from Day 6 + audio from this day.

---

## Lab sequence

| Lab | Folder | Motion? | Script | Focus |
|-----|--------|---------|--------|--------|
| **1** | [`lab-01/`](lab-01/) | No* | [`led.py`](lab-01/led.py) | Chest RGB LED sequence (red → green → blue → off) |
| **2** | [`lab-02/`](lab-02/) | No | [`audio.py`](lab-02/audio.py) + [`wav.py`](lab-02/wav.py) | WAV file playback via `PlayStream` |
| **3** | [`lab-03/`](lab-03/) | No | [`volume.py`](lab-03/volume.py) | Get / set volume (0–100) |
| **4** | [`lab-04/`](lab-04/) | **Yes** | [`tts.py`](lab-04/tts.py) | TTS + `WaveHand` capstone demo |

\*Lab 1 changes LEDs only; no locomotion. Lab 4 sends **`WaveHand()`** — supervision required.

Work through labs **in order**. Lab 4 requires [Day 5 Lab 2](../day-05/lab-02/) **Readiness: PASS** before running.

---

## Session setup (every lab)

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/repo
```

Set your NIC once per session:

```bash
export G1_INTERFACE=en6   # macOS example; use enp0s31f6 on Linux
```

Quick connectivity check:

```bash
python day-05/lab-00/g1_connection_check.py --interface en6 --skip-multicast
```

---

## Quick start

```bash
# Lab 1 — LED colour cycle
python day-07/lab-01/led.py en6

# Lab 2 — play a 16 kHz mono WAV (prepare file first — see Lab 2 README)
python day-07/lab-02/audio.py en6 test.wav

# Lab 3 — volume
python day-07/lab-03/volume.py en6 --get
python day-07/lab-03/volume.py en6 --set 85

# Lab 4 — TTS + wave (supervised)
python day-07/lab-04/tts.py en6 --lang en --text "Hello, welcome to the demo."
```

---

## Key concepts (Day 7)

| Topic | G1 detail |
|-------|-------------|
| Client | **`AudioClient`** → RPC service for speaker + chest LED hardware |
| LED control | `LedControl(r, g, b)` — each channel 0–255 |
| WAV playback | **16 kHz, mono, 16-bit PCM** only; streamed in chunks via `PlayStream` |
| TTS | `TtsMaker(text, speaker_id)` — `0` = Chinese, `1` = English |
| Volume | `GetVolume()` / `SetVolume(0–100)` |
| Capstone glue | Combine Day 6 arm sequence + Day 7 TTS/LED in your team demo |

### AudioClient vs other Day 5–6 clients

| Client | Service | Day 7 use |
|--------|---------|-----------|
| `AudioClient` | Audio / LED board | Labs 1–4 |
| `LocoClient` | `"sport"` locomotion | Lab 4 `WaveHand()` only |
| `G1ArmActionClient` | `"arm"` gestures | Optional capstone (Day 6) |

---

## Deliverables (day summary)

| Lab | Submit |
|-----|--------|
| 1 | Log showing four `LedControl` steps with return code 0 |
| 2 | WAV file specs + log of successful playback; note chunk behaviour |
| 3 | `--get` output + one `--set` run showing original and new volume |
| 4 | Log of TTS run (language + text); confirm wave was supervised |

---

## Capstone idea (team demo)

Combine pieces from earlier days without a single glue script:

1. [Day 6 Lab 2](../day-06/lab-02/) — `arm_action_sequence.py` with `"face wave,release arm"`
2. Lab 3 — set volume to a comfortable level
3. Lab 4 — TTS introduction in your language
4. Lab 1 — LED colour to match team branding

Run **one RPC client at a time**; wait for each action to finish before starting the next.

---

## References

| Resource | Link |
|----------|------|
| Unitree SDK (Python) | [github.com/unitreerobotics/unitree_sdk2_python](https://github.com/unitreerobotics/unitree_sdk2_python) |
| G1 audio example (upstream) | [example/g1/audio](https://github.com/unitreerobotics/unitree_sdk2_python/tree/master/example/g1) |
| Day 5 readiness | [day-05/lab-02/fsm_readonly.py](../day-05/lab-02/fsm_readonly.py) |
| Day 6 arm actions | [day-06/lab-02/arm_action_sequence.py](../day-06/lab-02/arm_action_sequence.py) |

---

## Course complete

After Day 7 you have worked through G1 **DDS**, **FSM safety**, **arm control**, and **audio/LED peripherals**. Use the capstone section above for final team presentations.
