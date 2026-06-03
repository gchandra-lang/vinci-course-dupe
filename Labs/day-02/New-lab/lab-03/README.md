# Lab 3 — Sensor Integration & Data Management

**Duration:** ~45 min  
**Robot motion:** None  
**Prerequisites:** [Lab 2](../lab-02/) complete (sport RPC readiness)

**PDF coverage:** Integrating sensors · managing sensor data

---

## Learning objectives

1. Name **onboard sensor paths** in the Python SDK (camera RPC, DDS state, optional lidar/wireless).
2. Capture a **front camera** frame with `VideoClient` and save it to disk.
3. Build a small **inspection data bundle** (`metadata.json` + image + optional state log).
4. Explain what an inspector would look for in the saved image and metadata.

---

## 1. Concepts

### Go2 sensors in this track

| Source | API | This lab |
|--------|-----|----------|
| **Front camera** | `VideoClient.GetImageSample()` | **Primary** |
| **Sport / gait state** | `rt/sportmodestate` | Short JSONL log |
| **Proprioception** | `rt/lowstate` | Lab 1 (optional attach) |
| **UT lidar** | DDS `rt/utlidar/switch` publish | Lab 3b [`lab03_platform_probe.py`](lab03_platform_probe.py) |
| **Onboard services** | `RobotStateClient.ServiceList()` | Lab 3b |
| **Head UI** | `VuiClient` volume / brightness | Lab 3b |
| **Wireless remote** | `wireless_remote` in `lowstate` | Lab 1 `--inspect` |

`VideoClient` is **RPC** (like `SportClient`), not a DDS video topic in the camp examples. You pull JPEG/binary samples in a loop and decode with OpenCV.

### Python SDK — `VideoClient` (same pattern as upstream)

| Step | API |
|------|-----|
| 1 | `ChannelFactoryInitialize(0, "en6")` |
| 2 | `VideoClient()` → `SetTimeout(3.0)` → `Init()` |
| 3 | Loop: `code, data = client.GetImageSample()` |
| 4 | `code == 0` → decode with `cv2.imdecode(..., cv2.IMREAD_COLOR)` |

Minimal excerpt (see [`lab03_capture_inspection.py`](lab03_capture_inspection.py) and `vendor/.../camera_opencv.py`):

```python
from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.video.video_client import VideoClient
import cv2
import numpy as np

ChannelFactoryInitialize(0, "en6")
client = VideoClient()
client.SetTimeout(3.0)
client.Init()

code, data = client.GetImageSample()
while code == 0:
    code, data = client.GetImageSample()
    img = cv2.imdecode(np.frombuffer(bytes(data), np.uint8), cv2.IMREAD_COLOR)
    cv2.imshow("front_camera", img)
    if cv2.waitKey(20) == 27:  # ESC
        break
cv2.imwrite("front_image.jpg", img)
```

| Module | Path |
|--------|------|
| Client | `unitree_sdk2py.go2.video.video_client.VideoClient` |
| Upstream example | `vendor/unitree_sdk2_python/example/go2/front_camera/camera_opencv.py` |
| Camp lab script | [`lab03_capture_inspection.py`](lab03_capture_inspection.py) |

DDS state during capture uses the same pattern as [Lab 1](../lab-01/): `ChannelSubscriber("rt/sportmodestate", SportModeState_)`.

### Camp script — `lab03_capture_inspection.py`

| Flag | Purpose |
|------|---------|
| `en6` | Ethernet interface (positional) |
| `--out-dir PATH` | Bundle folder (default `inspection_capture_<UTC>/`) |
| `--operator NAME` | Stored in `metadata.json` |
| `--robot-id ID` | Stored in `metadata.json` |
| `--state-log-sec N` | Seconds of `sportmodestate.jsonl` (default 5; `0` = skip) |
| `--state-log-hz` | Max JSONL lines per second (default 2) |
| `--camera-wait SEC` | Max wait for first good frame (default 15) |
| `--gui` | Live OpenCV window: **`s`** save, **ESC** cancel |

```bash
python course/day-02/New-lab/lab-03/lab03_capture_inspection.py en6 --help
```

### How to view the camera output

| Goal | Command / action |
|------|------------------|
| **Saved snapshot** (default run) | `open inspection_capture_*/frame_001.jpg` (macOS) or open in Files / image viewer |
| **Live stream** | `python .../lab03_capture_inspection.py en6 --gui` then press **`s`** |
| **Official stream** | `cd vendor/unitree_sdk2_python && python example/go2/front_camera/camera_opencv.py en6` — **ESC** quits and saves `front_image.jpg` |

Default capture does **not** open a window; it only writes `frame_001.jpg` under the bundle directory.

### Inspection data bundle

| File | Purpose |
|------|---------|
| `metadata.json` | Who, when, robot id, NIC, `CheckMode`, artifact names |
| `frame_001.jpg` | Visual checkpoint of the scene |
| `sportmodestate.jsonl` | Optional 5–10 s context (mode, velocity, …) |

Later (Day 2+) you may add poses, goals, or ROS bags; Day 1 keeps the bundle minimal and SDK-native.

### What to look for in the image

| Check | Why it matters |
|-------|----------------|
| Clear floor / obstacles | Safe path for patrol |
| Lighting / glare | Vision and human review quality |
| Expected scene | Wrong room = wrong mission |
| Robot visible parts | Confirms camera aim and focus |

---

## 2. Hands-on

### Step 1 — Session

```bash
conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/vinci-unitree
python course/day-01/lab-03/lab02_sport_readonly.py en6
```

Expect **PASS** before capturing data.

### Step 2 — Capture bundle (headless-friendly)

```bash
python course/day-02/New-lab/lab-03/lab03_capture_inspection.py en6 \
  --operator "Your Name" --robot-id go2-lab-1
```

**Expected:**

```text
Frame: <width>x<height>
Saved .../frame_001.jpg
Saved .../sportmodestate.jsonl (N lines)
Saved .../metadata.json
Summary: PASS — inspection bundle ready
```

Inspect output:

```bash
ls inspection_capture_*/
cat inspection_capture_*/metadata.json
open inspection_capture_*/frame_001.jpg    # macOS — view the camera frame
```

### Step 3 — Optional live preview

Requires a display (OpenCV window):

```bash
python course/day-02/New-lab/lab-03/lab03_capture_inspection.py en6 --gui
```

Press **`s`** to save, **ESC** to cancel. Same files as Step 2.

### Step 4 — Compare with upstream example

Official viewer (ESC exits, saves `front_image.jpg` in cwd):

```bash
cd vendor/unitree_sdk2_python
python example/go2/front_camera/camera_opencv.py en6
```

Camp script adds **metadata**, **bundle directory**, and **sportmodestate** log without requiring a GUI.

### Step 3b — Platform probe (more SDK clients)

Read-only RPC plus optional lidar DDS publish:

```bash
python course/day-02/New-lab/lab-03/lab03_platform_probe.py en6
python course/day-02/New-lab/lab-03/lab03_platform_probe.py en6 --json-out probe.json

# Instructor — clear space before toggling lidar
python course/day-02/New-lab/lab-03/lab03_platform_probe.py en6 --lidar on
```

Merge probe JSON into the inspection bundle:

```bash
python course/day-02/New-lab/lab-03/lab03_capture_inspection.py en6 --probe-json probe.json
```

### Step 5 — Optional extras (instructor)

| Demo | Command |
|------|---------|
| Wireless | `python example/wireless_controller/wireless_controller.py en6` *(edit imports to `unitree_go` + `rt/lowstate` if needed)* |
| Lidar switch (upstream) | `python example/go2/high_level/go2_utlidar_switch.py en6` |

---

## 3. Exercises

### Exercise A — Bundle review

Open `frame_001.jpg` and write two sentences: what is visible, and one risk for an inspection mission.

### Exercise B — Align timestamps

Compare `metadata.json` `created_utc` with the first line of `sportmodestate.jsonl`. Are they close enough for a report footnote?

### Exercise C — Missing camera

If `GetImageSample` fails (`code != 0`), list three checks from Lab 0 / field guide before blaming the script.

<details>
<summary>Hints</summary>

Power, ping, DDS PASS, video service / firmware, wait time (`--camera-wait 30`).

</details>

---

## 4. Troubleshooting

| Symptom | Action |
|---------|--------|
| `FAIL: no valid frame` | Increase `--camera-wait`; power-cycle robot; confirm Lab 2 PASS |
| Black or corrupt image | Retry capture; check lens; verify `code==0` on sample |
| No GUI on SSH | Omit `--gui`; use headless save (default) |
| Empty JSONL | Increase `--state-log-sec`; confirm `sportmodestate` (Lab 1) |
| `ModuleNotFoundError: cv2` | `conda activate unitree_env`; `verify_install.py` |

---

## 5. Deliverable

Submit the **directory** or zip containing:

- `metadata.json`
- `frame_001.jpg`
- `sportmodestate.jsonl` (if generated)
- Short answers to Exercise A and B

---

## 6. Next lab

**[Lab 4 — Increment concepts & obstacle avoidance](../lab-04/)**  
Theory plus `obstacles_avoid` hands-on (supervised motion).

---

## References

- [`lab03_capture_inspection.py`](lab03_capture_inspection.py)  
- `vendor/unitree_sdk2_python/example/go2/front_camera/camera_opencv.py`  
- [`docs/GO2-FIELD-GUIDE.md`](../../../docs/GO2-FIELD-GUIDE.md)  
- [Lab 1 state logging](../lab-01/)
