# Lab 4 — Text-to-speech + wave capstone

**Duration:** ~30–45 min  
**Robot motion:** Yes — `LocoClient.WaveHand()` before speech; supervision required  
**Prerequisites:** [Labs 1–3](../lab-01/) complete; [Day 5 Lab 2](../../day-05/lab-02/) **Readiness: PASS**

---

## Learning objectives

1. Run **`TtsMaker(text, speaker_id)`** for **Chinese** or **English** speech output.
2. Combine **audio RPC** with **`LocoClient.WaveHand()`** in one supervised demo flow.
3. Plan a short **capstone script** that chains Day 6 arm actions with Day 7 speech/LED.
4. Apply volume and safety settings from earlier labs before a team presentation.

---

## 1. Concepts

### TTS parameters

[`tts.py`](tts.py) CLI:

| Flag | Values | Maps to |
|------|--------|---------|
| `--lang ch` | Chinese text | `speaker_id = 0` |
| `--lang en` | English text | `speaker_id = 1` |
| `--text "..."` | String to speak | Passed to `TtsMaker` |

Example:

```bash
python day-07/lab-04/tts.py en6 --lang en --text "Hello, welcome to the demo."
python day-07/lab-04/tts.py en6 --lang ch --text "你好，今天怎么样？"
```

The script sleeps **5 s** after TTS so speech can finish before exit.

### Capstone flow in this script

```
ChannelFactoryInitialize
    → AudioClient.Init()
    → LocoClient.Init()
    → LocoClient.WaveHand()      # motion — needs clear space
    → AudioClient.TtsMaker(...)  # speech
    → sleep(5)
```

**Note:** `WaveHand()` uses the **sport/loco** service. On many G1 units the visible arm motion may be subtle compared to Day 6 **`G1ArmActionClient`** `"face wave"`. For a stronger gesture, run [Day 6 Lab 2](../../day-06/lab-02/) in a separate step before TTS.

### Full team capstone (manual sequencing)

No single glue script is required. Typical order:

1. Day 5 Lab 2 — **Readiness: PASS**
2. Lab 3 — set volume (e.g. `--set 75`)
3. Day 6 — `arm_action_sequence.py` with `"face wave,release arm"`
4. Lab 4 — TTS introduction
5. Lab 1 — LED team colour

Wait for each step to complete; **one RPC focus at a time**.

---

## 2. Safety (required)

- Clear **≥ 2 m** around the robot before `WaveHand()`.
- Robot **feet on the floor**; spotter present.
- Confirm **Readiness: PASS** before running.
- Keep TTS text **short** for classroom demos (avoid long blocking utterances).
- Do not max volume in small rooms — use Lab 3 to set a comfortable level first.

---

## 3. Hands-on

### Step 0 — Readiness and volume

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/repo

python day-05/lab-02/fsm_readonly.py en6
python day-07/lab-03/volume.py en6 --set 75
```

### Step 1 — English TTS + wave

```bash
python day-07/lab-04/tts.py en6 --lang en --text "Hello, I am the Unitree G1 robot."
```

Watch for wave gesture (if any) and listen for speech.

### Step 2 — Chinese TTS (optional)

```bash
python day-07/lab-04/tts.py en6 --lang ch --text "语音测试成功，很高兴认识你。"
```

### Step 3 — Extend with arm action (supervised)

In a **separate** run after TTS completes:

```bash
python day-06/lab-02/arm_action_sequence.py en6 --sequence "face wave,release arm"
```

### Step 4 — LED finale (optional)

```bash
python day-07/lab-01/led.py en6
```

Document your team’s final ordering for the deliverable.

---

## 4. Exercises

### Exercise A — Language IDs

What `speaker_id` does `--lang en` use? What happens if you pass English text with `--lang ch`?

### Exercise B — Capstone design (written)

Write a **5-step** team demo outline using at least one Day 6 arm action, one TTS line, and one LED colour. No code required — instructor sign-off before live demo.

### Exercise C — WaveHand vs arm RPC

When would you prefer Day 6 `face wave` over Lab 4 `WaveHand()` for a public demo?

---

## 5. Troubleshooting

| Symptom | Action |
|---------|--------|
| Readiness FAIL | Fix Day 5 FSM/CheckMode before motion |
| No speech | Check volume (Lab 3); verify `--lang` matches text |
| No visible wave, TTS OK | Expected on some units; add Day 6 arm wave |
| TTS garbled wrong language | Match `--lang` to text script |
| Script exits before speech ends | Increase sleep or wait manually before next command |

---

## 6. Deliverable

- Log of one successful `--lang en` (or `ch`) TTS run with your custom `--text`
- Team capstone outline (Exercise B)
- Confirmation that Readiness was **PASS** before `WaveHand`
- Optional: short video of full team sequence

---

## 7. Course wrap-up

You have completed the G1 student track:

- **Day 5** — DDS, FSM, safety
- **Day 6** — Arm RPC and `rt/arm_sdk`
- **Day 7** — Audio, LED, TTS capstone

Use the [Day 7 overview](../README.md) capstone section for final presentations.

---

## References

- [Lab 3](../lab-03/) · [Lab 1](../lab-01/) · [`tts.py`](tts.py)
- [Day 6 Lab 2](../../day-06/lab-02/) · [Day 5 Lab 2](../../day-05/lab-02/)
- [Day 7 overview](../README.md)
