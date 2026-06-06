# Lab 2 — WAV file playback (`PlayStream`)

**Duration:** ~30–45 min  
**Robot motion:** None — audio output only  
**Prerequisites:** [Lab 1](../lab-01/) complete; WAV file prepared (see below)

---

## Learning objectives

1. Load a **16 kHz mono 16-bit PCM** WAV file and validate format with [`wav.py`](wav.py).
2. Stream audio to the robot in **chunks** via `AudioClient.PlayStream`.
3. Stop playback cleanly with `PlayStop`.
4. Understand why unsupported sample rates or channel counts are rejected before streaming.

---

## 1. Concepts

### WAV requirements (strict)

[`audio.py`](audio.py) accepts **only**:

| Property | Required value |
|----------|----------------|
| Sample rate | **16000 Hz** |
| Channels | **1** (mono) |
| Bit depth | **16-bit PCM** |

Other formats fail with:

`Failed to read WAV file or unsupported format (must be 16kHz mono)`

### Playback pipeline

```
read_wav(path)  →  PCM byte list
       ↓
play_pcm_stream(client, pcm_list, "example")
       ↓
PlayStream(name, stream_id, chunk)  in loops
       ↓
PlayStop("example")
```

[`wav.py`](wav.py) helper functions:

| Function | Role |
|----------|------|
| `read_wav(filename)` | Parse RIFF/WAVE; return `(pcm_list, sample_rate, num_channels, ok)` |
| `write_wave(filename, ...)` | Write 16-bit mono WAV (useful for creating test files) |
| `play_pcm_stream(...)` | Send **96000-byte** chunks (~3 s at 16 kHz) with sleep between chunks |

### Chunk streaming

Default `chunk_size = 96000` bytes and `sleep_time = 3.0` s between chunks. Long files play over multiple RPC calls with the same stream name `"example"`.

---

## 2. Hands-on

### Step 0 — Prepare a test WAV

The repo does not ship a sample file. Create **16 kHz mono** audio on your laptop:

**Option A — ffmpeg** (from any source file):

```bash
ffmpeg -i input.mp3 -ar 16000 -ac 1 -sample_fmt s16 test.wav
```

**Option B — Python** (using `write_wave` from this lab):

```python
import array
from wav import write_wave
# 1 second of 440 Hz tone at 16 kHz
samples = array.array('h', [int(8000 * __import__('math').sin(2 * 3.14159 * 440 * t / 16000)) for t in range(16000)])
write_wave("test.wav", 16000, samples)
```

Run from `day-07/lab-02/` so `from wav import ...` resolves.

### Step 1 — Session setup

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/repo
```

Optional: set a comfortable volume before playback (Lab 3):

```bash
python day-07/lab-03/volume.py en6 --set 70
```

### Step 2 — Play the WAV

```bash
python day-07/lab-02/audio.py en6 test.wav
```

**Expected debug output:**

```
[DEBUG] Read success: True
[DEBUG] Sample rate: 16000 Hz
[DEBUG] Channels: 1
[DEBUG] PCM byte length: ...
[INFO] Chunk 0 sent successfully
...
```

Audio should be audible from the robot speaker.

### Step 3 — Verify format rejection

Try a wrong file (e.g. stereo or 44.1 kHz) and confirm the script exits with the format error **before** streaming.

---

## 3. Exercises

### Exercise A — Duration math

If PCM byte length is 32000 bytes (16-bit mono), how many seconds of audio is that?

<details>
<summary>Answer</summary>

16000 samples/s × 2 bytes/sample = 32000 bytes/s → **1 second**.

</details>

### Exercise B — Chunk count

For a 10-second file, roughly how many `PlayStream` chunks are sent with default settings?

### Exercise C — Compare to TTS

In 2–3 sentences: how is `PlayStream` different from `TtsMaker` (Lab 4)?

---

## 4. Troubleshooting

| Symptom | Action |
|---------|--------|
| `Usage: ... <wav_file_path>` | Pass interface and path: `audio.py en6 test.wav` |
| Format error | Re-encode to 16 kHz mono with ffmpeg |
| `[ERROR] chunk_id != 'RIFF'` | File is not a valid WAV |
| No sound, chunks OK | Raise volume (Lab 3 `--set`); check robot speaker |
| `ModuleNotFoundError: wav` | Run from repo root or ensure `lab-02/` is on `PYTHONPATH`; run from directory containing both scripts |
| Import error for `unitree_sdk2py` | Activate `unitree_env` |

---

## 5. Deliverable

- Specifications of your test WAV (rate, channels, duration)
- Log showing `[DEBUG] Read success: True` and at least one `[INFO] Chunk … sent successfully`
- Answer to Exercise C

---

## 6. Next lab

**[Lab 3 — Volume control](../lab-03/)**  
`GetVolume` and `SetVolume` before TTS capstone.

---

## References

- [Lab 1](../lab-01/) · [`audio.py`](audio.py) · [`wav.py`](wav.py)
- [Day 7 overview](../README.md)
