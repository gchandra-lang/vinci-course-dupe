# Vinci Unitree Training — Day 4 Lecture Notes

## B2 Advanced Scenarios & Field Inspection

**Course block:** Vinci Unitree Train-the-Trainer, Day 4  
**Lecture duration:** 3 hours  
**Platform:** Unitree B2  
**Author:** Manus AI  
**Branding note:** © 2026 Vinci AI. All rights reserved. Property of Vinci AI — Do Not Distribute.

---

## 1. Lecture purpose and teaching stance

Day 4 converts the B2 from a robot that can be safely observed and commanded into an **inspection evidence system**. The central message for students is that a field inspection is not successful merely because the robot moved. It is successful when the team can explain what scenario was attempted, what data were captured, what state the robot reported during the run, which checkpoints were inspected, how artifacts were organized, and whether the run folder can be validated after the robot is powered down.

The Day 4 repository scaffold identifies the session as **“B2 Advanced Scenarios & Field Inspection”** and divides the day into three labs: a run-folder lab, a mock video inspection lab, and a field-run/reporting lab.[1] This three-hour lecture note is designed to prepare instructors to teach those labs as one coherent workflow rather than as separate scripts. The lecture should repeatedly connect the practical tools to a professional inspection loop: **plan, verify, capture, move, log, validate, and report**.

> **Instructor thesis:** Day 4 is the bridge between robot operation and auditable robotics practice. Students should leave able to defend a B2 inspection run with files, logs, timestamps, checkpoint evidence, and a short technical debrief.

| Teaching priority | What students should learn | Evidence that they understand it |
|---|---|---|
| Inspection framing | A robot field run must produce traceable evidence, not just motion. | Students can describe the run folder before touching the robot. |
| Video capture | Front/back cameras and RTSP streams are inspection assets. | Students can save still images and recordings with meaningful names. |
| State logging | SportModeState is the runtime witness of motion and posture. | Students can explain mode, gait, position, velocity, and body-height fields. |
| Supervised mobility | SportClient motion must remain bounded and human-supervised. | Students can choose StopMove, Damp, StandDown, or RecoveryStand appropriately. |
| Reporting | Validation and debrief convert raw files into engineering evidence. | Students submit a coherent run package and explain warnings or failures. |

---

## 2. Three-hour lecture structure

The Day 4 session should be paced as a **3-hour lecture with instructor-led demonstrations and short student checks**. Because the labs use live robot networking, video, and file artifacts, the lecture should not rush directly into command execution. A strong teaching flow first establishes what a valid inspection package looks like, then demonstrates video capture, then integrates state logs and movement into a reportable run.

| Time | Segment | Instructor focus | Student checkpoint |
|---:|---|---|---|
| 0:00–0:15 | Day 4 framing | Explain B2 inspection as an evidence pipeline. | Students can state the difference between “the robot moved” and “the run is auditable.” |
| 0:15–0:35 | B2 inspection hardware | Review B2 cameras, LiDAR context, weight, power, and safety implications. | Students identify front/back camera roles and why B2 needs wider safety margins. |
| 0:35–0:55 | Run-folder schema | Revisit Day 2 run-folder contract and adapt it for B2. | Students sketch the required folder tree from memory. |
| 0:55–1:20 | Mock inspection video | Explain SDK JPEG capture, front/back video clients, and RTSP recording. | Students map keys Q/E/A/D/ESC to artifacts and safe exit behavior. |
| 1:20–1:30 | Break and readiness reset | Pause robot activity, confirm space, battery, network, and files. | Students perform a verbal “ready/not ready” check. |
| 1:30–1:55 | Runtime state logging | Teach SportModeState as the audit trail for robot behavior. | Students interpret mode, gait, position, velocity, yaw speed, and body height. |
| 1:55–2:20 | SportClient between legs | Review supervised motion options and command semantics. | Students choose the least-risk command for a given inspection leg. |
| 2:20–2:45 | Field run and report | Combine video, state, motion, checkpoint evidence, and validation. | Students explain what goes into `metadata.json`, `patrol_plan.json`, and checkpoint folders. |
| 2:45–3:00 | Debrief and assessment | Use validation output and debrief questions to assess competence. | Students produce a short report claim backed by artifacts. |

The instructor should treat the schedule as a conceptual flow rather than a rigid script. If networking or camera access is slow, preserve the learning objective by using a mock run folder and previously captured video artifacts. The key outcome is not that every class completes the same physical route; it is that every class understands the **inspection evidence model**.

---

## 3. From Day 3 fundamentals to Day 4 inspection practice

Day 3 introduced the B2 as an industrial platform and emphasized readiness, safety, SDK setup, SportModeState observation, and high-level SportClient control. Day 4 assumes that students can already initialize the robot network interface, identify the correct interface name, subscribe to a state topic, and call conservative high-level commands. The new step is integration: students must now use those pieces to create a field-inspection record.

The course schedule labels Day 4 as **B2 inspection and analytics**, following Day 3 B2 fundamentals and before Day 5 G1 architecture.[2] This placement matters pedagogically. Day 4 is the final B2 day, so instructors should ask students to think like field engineers. A field engineer does not simply say, “I saw the pipe,” or “the robot walked to the wall.” A field engineer says, “At checkpoint C2, front camera frame `frame.jpg` was captured; the state log shows the robot was stationary during dwell; the video file covers the approach; and the run passed validation except for a documented warning.”

| Day 3 capability | Day 4 extension | Instructor emphasis |
|---|---|---|
| Observe SportModeState | Save state evidence into a run package. | Observability becomes auditability. |
| Use high-level SportClient | Move between inspection legs under supervision. | Commanding remains bounded and reversible. |
| Confirm DDS/network readiness | Combine camera, RTSP, and state channels. | A field run uses multiple data paths. |
| Explain B2 safety | Apply safety to a 60 kg industrial robot near people and assets. | Safe field inspection is procedural, not improvised. |

---

## 4. B2 inspection hardware context

Unitree’s B2 documentation describes the robot as having depth and optical cameras in both the front and rear, supporting long-distance perception, anti-interference capability, high-definition image transmission, and video.[3] The same documentation lists a wide-angle omnidirectional LiDAR on the head, 12 degrees of freedom, a net weight of approximately 60 kg including battery, and an operating time of 4–6 hours using a 45 Ah / 2268 Wh battery.[3] These facts shape the Day 4 safety and data strategy.

Students should not treat the B2 camera system as a decorative feature. In an inspection workflow, front and rear views can answer different evidence questions. The front camera documents approach and target inspection. The rear camera can document retreat, operator context, or changes behind the robot. Video can capture continuous context, while still images are easier to attach to checkpoint reports.

| B2 capability | Inspection meaning | Teaching implication |
|---|---|---|
| Front optical/depth perception | Capture approach view, target asset, and obstacle context. | Use front stills for primary checkpoint evidence. |
| Rear optical/depth perception | Capture retreat view, rear-side hazards, or alternate evidence. | Use rear stills when turning around is unsafe or unnecessary. |
| LiDAR context | Supports spatial awareness and terrain interpretation. | Discuss perception broadly, even if the lab focuses on video. |
| 60 kg class body | Motion risk is non-trivial in classrooms and corridors. | Enforce wide exclusion zones and human stop authority. |
| 4–6 h nominal operating time | Long enough for field practice, but not a reason to skip readiness. | Check battery and thermal conditions before repeated runs. |

Unitree’s B2 documentation also warns that hot swapping aviation plug interfaces is strictly prohibited and may cause equipment failure not covered by warranty.[3] This should be elevated from a hardware footnote to a classroom rule. Students should never connect or disconnect power or aviation-plug peripherals casually during a live lab. If a cable, camera, or external payload needs attention, stop the exercise, place the robot in a safe state, and follow the local hardware procedure.

> **Classroom rule:** Treat every B2 inspection run as a controlled engineering operation. The robot’s camera evidence is only valuable if the team can also demonstrate safe setup, stable networking, and controlled shutdown.

---

## 5. The Day 4 inspection evidence pipeline

The most important Day 4 concept is the **inspection evidence pipeline**. A pipeline view prevents students from thinking of the lab as three disconnected tasks: making folders, opening camera windows, and driving the robot. The pipeline begins with a scenario and ends with a reportable package.

| Stage | Purpose | Typical Day 4 artifact |
|---|---|---|
| Scenario | Defines what is being inspected and why. | Scenario notes, checkpoint IDs, inspection target descriptions. |
| Readiness | Confirms robot, space, network, and operator state. | Metadata fields, readiness checklist, operator name. |
| Video capture | Records what the robot saw at checkpoints and during travel. | `front_img_*.jpg`, `back_img_*.jpg`, `front_video_*.mp4`, `output.mp4`. |
| State logging | Records robot motion/posture context. | `sportmodestate.jsonl` or terminal log transformed into JSONL. |
| Motion between legs | Moves the B2 between inspection areas under supervision. | SportClient command notes, plan leg records. |
| Checkpoint packaging | Associates images and state slices with checkpoint IDs. | `checkpoints/<id>/frame.jpg`, optional `state_slice.jsonl`. |
| Validation | Checks that the package is structurally complete. | Validator PASS, PASS-with-warning, or FAIL output. |
| Debrief | Converts files into technical conclusions. | Short `field_report.md` or oral debrief. |

The instructor should keep this table visible or repeatedly return to it. When a student asks, “Which script should I run?” the instructor can answer with a pipeline question: “Which evidence stage are you trying to complete?” This encourages engineering judgment rather than command memorization.

---

## 6. Lab 0 — Run folder as the contract for inspection evidence

Day 4 Lab 0 explicitly reuses the Day 2 run-folder schema while pointing students to the B2 scripts.[4] This is a deliberate design choice. The folder contract is platform-agnostic enough to organize inspection data, while the scripts are platform-specific enough to acquire B2 camera and motion artifacts.

The reused validator checks for three top-level files and one checkpoint tree: `metadata.json`, `patrol_plan.json`, `sportmodestate.jsonl`, and `checkpoints/`.[5] The metadata must contain at least `schema_version`, `created_utc`, and `operator`; the plan must contain `schema_version`, `checkpoints`, and `legs`; the state log must contain at least one valid JSON line; and each planned checkpoint must have a directory under `checkpoints/`.[5]

| Required item | Why it exists | B2-specific adaptation |
|---|---|---|
| `metadata.json` | Describes who ran the inspection, when, and under what conditions. | Add `robot_platform: B2`, `robot_id`, `interface`, `camera_mode`, and operator notes. |
| `patrol_plan.json` | Declares checkpoint IDs and movement legs. | Use conservative B2 legs and document any manual movement between checkpoints. |
| `sportmodestate.jsonl` | Provides the time-series state witness. | Log mode, gait, position, velocity, yaw speed, and body height where possible. |
| `checkpoints/` | Organizes evidence by inspection point. | Place front or rear stills as `frame.jpg`; add optional `state_slice.jsonl`. |
| Validator output | Confirms whether the package is structurally usable. | Explain warnings instead of hiding them. |

A recommended Day 4 B2 run folder should look like the following. The exact file names from scripts may initially be timestamped, but the final report package should map them into the checkpoint schema.

```text
run_b2_day4_team_alpha_20260603_1030/
  metadata.json
  patrol_plan.json
  sportmodestate.jsonl
  videos/
    front_video_20260603_103251.mp4
    back_video_20260603_103251.mp4
  raw_images/
    front_img_20260603_103300.jpg
    back_img_20260603_103310.jpg
  checkpoints/
    cp01_entry/
      frame.jpg
      state_slice.jsonl
      notes.md
    cp02_asset_label/
      frame.jpg
      state_slice.jsonl
      notes.md
    cp03_exit/
      frame.jpg
      state_slice.jsonl
      notes.md
  field_report.md
```

The validator will not require every enrichment folder shown above, but the extra organization is useful for teaching. `videos/` and `raw_images/` preserve original captures, while `checkpoints/<id>/frame.jpg` provides the normalized evidence path expected by the validator. This distinction lets students keep raw data and still produce a clean report package.

---

## 7. Example B2 metadata and patrol-plan adaptation

The Day 2 scaffold may contain Go2-oriented defaults, so Day 4 instructors should explicitly show how to adapt the schema for B2. The following example is intentionally conservative and report-oriented. It is not meant to command the robot by itself; it describes the intended inspection package.

```json
{
  "schema_version": "1.0",
  "created_utc": "2026-06-03T02:30:00Z",
  "operator": "team_alpha",
  "robot_platform": "Unitree B2",
  "robot_id": "b2-01",
  "lab": "day-04-field-inspection",
  "interface": "eth0",
  "environment": "indoor corridor mock inspection",
  "camera_sources": ["front", "back"],
  "checkpoints": ["cp01_entry", "cp02_asset_label", "cp03_exit"],
  "safety_observer": "instructor",
  "notes": "B2 moved only under supervised SportClient commands; checkpoint frames selected after capture."
}
```

```json
{
  "schema_version": "1.0",
  "checkpoints": [
    {"id": "cp01_entry", "description": "Entry view before approaching mock asset"},
    {"id": "cp02_asset_label", "description": "Close view of asset label or target"},
    {"id": "cp03_exit", "description": "Exit or return view"}
  ],
  "legs": [
    {"type": "dwell", "to_checkpoint": "cp01_entry", "seconds": 5},
    {"type": "velocity", "to_checkpoint": "cp02_asset_label", "vx": 0.1, "vy": 0.0, "vyaw": 0.0, "seconds": 2},
    {"type": "dwell", "to_checkpoint": "cp02_asset_label", "seconds": 8},
    {"type": "velocity", "to_checkpoint": "cp03_exit", "vx": -0.1, "vy": 0.0, "vyaw": 0.0, "seconds": 2},
    {"type": "dwell", "to_checkpoint": "cp03_exit", "seconds": 5}
  ]
}
```

When teaching this example, emphasize that the validator accepts `increment`, `velocity`, and `dwell` leg types as known categories, and it warns rather than fails on some leg-specific omissions.[5] That behavior is pedagogically useful. Students can learn the difference between a **structural failure** that makes a package invalid and a **warning** that demands explanation in the debrief.

---

## 8. Lab 1 — Mock inspection video with B2 front and back cameras

Day 4 Lab 1 uses `camera_opencv-video.py` as the primary B2 video script.[6] The script initializes the Unitree communication channel, creates separate `FrontVideoClient` and `BackVideoClient` instances, obtains image samples, decodes JPEG bytes into OpenCV images, displays front and back camera windows, and provides keyboard controls for still-image capture and RTSP recording.[6]

| Key | Action | Artifact | Teaching note |
|---|---|---|---|
| `Q` / `q` | Save front camera image. | `front_img_<timestamp>.jpg` | Use this for primary checkpoint evidence. |
| `E` / `e` | Save back camera image. | `back_img_<timestamp>.jpg` | Use this for reverse-view or context evidence. |
| `A` / `a` | Start or stop front RTSP recording. | `front_video_<timestamp>.mp4` | Confirm stream opens before claiming video evidence. |
| `D` / `d` | Start or stop back RTSP recording. | `back_video_<timestamp>.mp4` | Useful for retreat or rear-side inspection context. |
| `ESC` | Exit. | Releases active resources and closes windows. | Always exit deliberately; do not kill windows blindly. |

Unitree’s multimedia documentation states that application-layer camera access includes both image data and video streaming. It recommends directed UDP for image transmission or general streaming interfaces, while noting that DDS can be used for photography to obtain 720p JPEG images.[7] This distinction explains why Day 4 uses both SDK image samples and RTSP/OpenCV video capture. The still-image path is convenient for checkpoint evidence; the streaming path is appropriate for continuous video context.

The same Unitree multimedia reference documents a 1280×720 camera resolution, a 15 Hz video frame rate, a horizontal field of view of 100 degrees, and a vertical field of view of 56 degrees for the described video stream.[7] Instructors should use those numbers to teach practical limitations. A wide field of view helps document context, but it does not guarantee that text labels, small defects, or distant details are readable. Inspection teams should capture deliberate stills at dwell points and verify image quality before leaving the site.

---

## 9. Under the hood: JPEG samples, RTSP streams, and OpenCV

Students do not need to become computer vision experts on Day 4, but they should understand the data path well enough to troubleshoot failures. The camera script uses SDK clients to request JPEG samples, converts byte arrays into NumPy buffers, decodes them with `cv2.imdecode`, and displays the resulting BGR frames. For recording, it opens RTSP URLs with `cv2.VideoCapture`, creates a `cv2.VideoWriter`, and writes frames until recording is toggled off.[6]

| Layer | What happens | Typical failure | Debugging habit |
|---|---|---|---|
| DDS/channel initialization | `ChannelFactoryInitialize` binds communication to the robot network. | Wrong interface or disconnected cable. | Confirm interface name and robot reachability before camera testing. |
| SDK image sample | Front/back clients call `GetImageSample`. | Return code is nonzero or no frame appears. | Test one camera at a time and watch terminal output. |
| JPEG decoding | Bytes become an OpenCV frame. | Frame is `None` or corrupt. | Confirm sample data exists before saving. |
| Display window | `cv2.imshow` shows live front/back view. | No GUI or window does not update. | Use a GUI-capable host; avoid headless execution unless adapted. |
| RTSP capture | `VideoCapture` opens a stream URL. | Stream cannot open. | Confirm robot IP, port, network path, and firewall. |
| Video writing | `VideoWriter` saves MP4 output. | Writer cannot open or output is empty. | Confirm codec, dimensions, and frame rate. |
| Cleanup | Capture/writer/window resources are released. | Locked files or half-written videos. | Stop recording before exit and verify file size. |

The instructor should demonstrate one controlled failure if time allows. For example, show how an unopened RTSP stream produces a clear error rather than a valid video. This helps students avoid the most common reporting mistake: assuming a file exists simply because a script was started.

---

## 10. Optional analytics extension: video effects and lightweight perception

The optional `camera_opencv-videoEffect.py` script adds simple OpenCV effects to the front camera: normal view, face detection, red color tracking, and sketch effect.[8] This script is useful for introducing the idea of **inspection analytics**, but it should not be oversold. Face detection and color thresholding are demonstrations of image processing, not robust industrial defect detection.

| Mode | Method | What it teaches | Limitation |
|---|---|---|---|
| Normal | Display raw decoded frame. | Baseline evidence capture matters. | No automated interpretation. |
| Face detection | Haar cascade on grayscale image. | Classical computer vision uses hand-engineered detectors. | Sensitive to lighting, pose, and scale. |
| Red tracking | HSV threshold mask for red regions. | Color segmentation can identify simple visual markers. | Fails under lighting changes and non-red targets. |
| Sketch effect | Grayscale, inversion, blur, and divide. | Image transforms can emphasize edges. | Aesthetic effect, not inspection proof. |

If this extension is used, require students to label processed images clearly. A processed frame should not silently replace the raw checkpoint frame. The best practice is to preserve the raw evidence and store processed outputs as derived artifacts, such as `checkpoints/cp02_asset_label/processed_red_mask.jpg`.

---

## 11. Lab 2 — SportModeState as the field-run audit trail

Day 4 Lab 2 lists `subscribe_sport_mode_state.py` as the state-log script for field reporting.[9] The script subscribes to the `rt/sportmodestate` topic and prints key fields including mode, gait type, position, velocity, yaw speed, and body height.[10] These values are not decoration; they are the runtime context that helps explain what the robot was doing when each image or video segment was captured.

| Field | Meaning in lecture | Inspection use |
|---|---|---|
| `mode` | Current high-level robot mode. | Confirms whether the robot was standing, moving, or in another state. |
| `gait_type` | Locomotion pattern or gait category. | Helps interpret motion behavior during approach or retreat. |
| `position` | Estimated position vector. | Supports checkpoint sequencing and relative movement discussion. |
| `velocity` | Estimated translational velocity. | Helps prove dwell versus motion during image capture. |
| `yaw_speed` | Rotational speed. | Helps explain blur, turning, or unstable target framing. |
| `body_height` | Body height state. | Helps explain camera perspective and clearance decisions. |
| `foot_force` | Foot contact-related force information. | Can support terrain/contact discussion in advanced analysis. |

The repository script prints state continuously to the terminal. For a reportable Day 4 run, instructors should require students to convert or capture the relevant state data into `sportmodestate.jsonl`. Each line should be a valid JSON object. A minimal entry can include timestamp, mode, gait type, position, velocity, yaw speed, and body height. The validator requires at least one non-empty valid JSON line in this file.[5]

```json
{"t_utc":"2026-06-03T02:33:12.250Z","mode":1,"gait_type":1,"position":[0.00,0.00,0.00],"velocity":[0.00,0.00,0.00],"yaw_speed":0.00,"body_height":0.41,"checkpoint":"cp01_entry"}
```

The teaching point is that a state log becomes more valuable when it is connected to checkpoints. A video alone shows what the camera saw. A state log alone shows what the robot estimated. Together, they help students answer whether the robot was moving, stationary, turning, recovering, or dwelling during inspection capture.

---

## 12. Supervised motion between inspection legs

Day 4 Lab 2 lists `b2_sport_client.py` as the script for SportClient control between field-run legs.[9] The script provides a menu of high-level commands such as Damp, BalanceStand, StopMove, StandUp, StandDown, RecoveryStand, Move, FreeWalk, ClassicWalk, MoveToPos, and TrajectoryFollow, although the trajectory-follow call is commented in the menu branch in the repository version.[11]

Unitree’s sports-services documentation describes high-level SportClient control for posture, speed, and trajectory commands. It identifies Damp as a high-priority damping state used for emergency stops, StopMove as a command to stop current motion and restore internal motion parameters, Move as body-coordinate velocity control, and TrajectoryFollow as a path-following interface based on 30 future trajectory points.[12] Even where the documentation is written for Go2 interfaces, the Day 4 B2 scripts use the B2 SportClient API with similar high-level control semantics.[11] [12]

| Command | Day 4 teaching meaning | Safe-use guidance |
|---|---|---|
| `Damp` | Emergency-priority damping stop. | Use only when the safety situation requires immediate damping; brief students beforehand. |
| `StopMove` | Stop current high-level motion. | Preferred first stop for normal supervised trials. |
| `StandUp` | Stand high with joint locking. | Use only after space and posture are verified. |
| `StandDown` | Lie down / low stand state. | Use for end-of-run or safe pause. |
| `RecoveryStand` | Recover to standing from nonstandard posture. | Use under instructor supervision after checking surroundings. |
| `Move` | Body-frame velocity command. | Keep speeds very low in class and define a short duration. |
| `ClassicWalk` | Toggles classic walking behavior in the script. | Confirm mode before issuing movement. |
| `MoveToPos` | Position-style command in the script. | Treat as advanced and bounded; verify target area. |
| `TrajectoryFollow` | Path of future points. | Discuss conceptually unless the instructor has validated the route and script branch. |

The instructor should explicitly discourage “menu experimentation.” Because the B2 is heavy and powerful, a student should not enter commands merely to see what happens. Each command should be tied to an inspection-leg intention and a recovery plan. For example: “We will issue a short forward Move at low speed for two seconds, then StopMove, then dwell and capture the front image.”

---

## 13. Field inspection choreography

A Day 4 field run should be choreographed like a small production. The operator manages commands, the safety observer watches the robot and environment, the evidence lead watches files and timestamps, and the instructor controls the pace. This division of labor reduces cognitive load and makes the run auditable.

| Role | Responsibility | Stop authority |
|---|---|---|
| Operator | Executes only the agreed command sequence. | Can stop immediately if command behavior is unexpected. |
| Safety observer | Watches people, obstacles, robot posture, and exclusion zone. | Has absolute stop authority at all times. |
| Evidence lead | Records filenames, checkpoint IDs, and validation notes. | Can pause the run if evidence capture fails. |
| Instructor | Approves readiness, motion plan, and debrief standard. | Can terminate the exercise. |

A recommended field-run sequence is as follows. First, create the run folder and draft metadata before the robot moves. Second, start state logging and confirm non-empty state output. Third, start video recording if continuous evidence is required. Fourth, place the robot at checkpoint 1, dwell, and capture a still image. Fifth, execute one short supervised motion leg. Sixth, stop and dwell before capturing checkpoint 2. Seventh, repeat only if the space remains safe. Eighth, stop recording, stop motion, place the robot in a safe state, and validate the folder.

| Step | Instructor cue | Required evidence |
|---:|---|---|
| 1 | “Create the run folder before movement.” | Folder name, metadata draft, checkpoint list. |
| 2 | “Start the runtime witness.” | Non-empty `sportmodestate.jsonl` or captured state records. |
| 3 | “Start video only when the stream is confirmed.” | Video file path and visible frame confirmation. |
| 4 | “Dwell before capture.” | Checkpoint still image and state slice. |
| 5 | “Move only for the approved leg.” | Motion command note and observer confirmation. |
| 6 | “Stop before inspection.” | StopMove or stable dwell state. |
| 7 | “Package immediately.” | `checkpoints/<id>/frame.jpg`. |
| 8 | “Validate before debrief.” | Validator output and explanation of warnings. |

---

## 14. Reporting: from artifacts to engineering claims

A field report should not be a diary. It should be a short engineering argument that links claims to evidence. Students should avoid vague statements such as “the robot worked well” or “camera was good.” Instead, they should write claims that can be checked against files.

| Weak claim | Stronger Day 4 claim |
|---|---|
| “The robot inspected the target.” | “At `cp02_asset_label`, the front camera frame shows the target label, and the associated state slice indicates the robot was stationary during capture.” |
| “The video recorded.” | “The front RTSP recording `front_video_20260603_103251.mp4` covers the approach from `cp01_entry` to `cp02_asset_label` and was verified playable after the run.” |
| “The robot moved safely.” | “The robot executed one low-speed supervised forward leg, then StopMove was issued before checkpoint capture; no person entered the exclusion zone.” |
| “Validation passed.” | “The run folder passed structural validation; the only warning was explained as a missing optional rear-camera frame.” |

A concise `field_report.md` should include the scenario, team roles, safety setup, command sequence, evidence table, validation result, issues, and next improvement. The instructor should require students to cite exact file names. This habit is essential in robotics because evidence without traceability becomes difficult to audit, reproduce, or troubleshoot.

---

## 15. Validator interpretation and common Day 4 failures

The validator is not merely a grading tool; it is a teaching instrument. It forces students to separate structural completeness from subjective success. A run can have beautiful video and still fail validation if it lacks metadata or checkpoint organization. Conversely, a run may pass with warnings and still require a careful debrief.

| Validator message pattern | Likely cause | Instructor response |
|---|---|---|
| `missing file: metadata.json` | Students captured data before creating the run package. | Ask them to reconstruct metadata and explain what may be uncertain. |
| `metadata.json: missing 'operator'` | Metadata is incomplete. | Reinforce that inspection evidence needs accountability. |
| `patrol_plan.json: missing 'checkpoints'` | The plan lacks explicit checkpoint structure. | Have students define checkpoint IDs before moving again. |
| `sportmodestate.jsonl: need at least 1 JSON line` | State logging was not saved or is empty. | Ask whether the run can be defended without runtime state evidence. |
| `checkpoints/<id>/frame.jpg missing` | Raw images were not mapped into checkpoint folders. | Require students to copy or rename the selected still image. |
| `frame.jpg too small` | Corrupt image or placeholder file. | Verify image can open and recapture if possible. |
| `metadata checkpoints list differs` | Metadata and plan disagree. | Treat as a configuration-management lesson. |

For a three-hour lecture, instructors should show at least one PASS and one FAIL example if possible. Students learn faster when they see validation as immediate feedback rather than as an end-of-day penalty.

---

## 16. Troubleshooting guide for Day 4 instructors

Day 4 combines network communication, GUI display, OpenCV recording, robot state topics, and motion commands. Failures should be expected and handled methodically. The instructor’s tone should remain calm: every failure is an opportunity to teach evidence-based debugging.

| Symptom | Probable source | First diagnostic step | Safe fallback |
|---|---|---|---|
| Camera window does not appear. | No GUI, wrong interface, SDK client not receiving frames. | Confirm `eth0` or correct interface and run a minimal camera test. | Use saved sample frames for the reporting exercise. |
| Front image saves but rear does not. | Rear client or rear stream issue. | Test rear capture independently and verify return code. | Mark rear camera as unavailable in metadata. |
| RTSP recording file is empty. | Stream did not open or writer dimensions/codec failed. | Check terminal message, file size, and playback. | Use still images plus state log for checkpoint report. |
| State subscriber prints nothing. | Wrong DDS interface, topic unavailable, robot not publishing. | Confirm robot network and `rt/sportmodestate` subscription. | Use instructor-provided state log for schema practice. |
| Robot moves but checkpoint image is blurred. | Captured during motion or yaw turn. | Check velocity/yaw speed near capture time. | Repeat capture during dwell after StopMove. |
| Validator fails after good field work. | Artifacts not normalized into required paths. | Compare folder tree against schema. | Repackage raw captures into checkpoint folders. |
| Students want to try advanced commands. | Curiosity without safety plan. | Ask for purpose, boundary, stop command, and observer approval. | Demonstrate concept verbally or in simulation instead. |

The most important troubleshooting habit is to preserve raw artifacts. Do not delete imperfect video, state logs, or images until the debrief is complete. A failed capture can still be useful evidence for diagnosing what went wrong.

---

## 17. Instructor demonstration script

The following demonstration script is designed for a classroom where the B2 is available, connected, and supervised. It should be adapted to the local environment and never used to override site-specific safety rules.

| Demonstration moment | Instructor action | Explanation to students |
|---|---|---|
| Readiness | Confirm robot space, interface, battery, and observers. | “Inspection begins before the first command.” |
| Run folder | Show an empty Day 4 folder tree. | “This folder is the contract we must satisfy.” |
| Camera still | Run the camera script and save a front image. | “A still image is a checkpoint artifact.” |
| RTSP recording | Toggle front recording briefly, then stop and verify file. | “A recording is not evidence until it is playable.” |
| State observation | Start SportModeState subscriber and identify fields. | “This is the robot’s runtime witness.” |
| Motion cue | Issue a conservative movement or demonstrate the menu without motion. | “Commands must have purpose, limit, and stop plan.” |
| Packaging | Copy selected image to `checkpoints/cp01/frame.jpg`. | “Raw capture becomes report evidence when normalized.” |
| Validation | Run the validator and interpret results. | “PASS means structurally usable; warnings still need explanation.” |

The instructor should deliberately pause after each artifact is created and ask, “Where will this go in the report package?” This prevents the common mistake of accumulating files in the working directory without a final evidence model.

---

## 18. Student knowledge checks

Use knowledge checks throughout the lecture rather than saving all assessment for the end. The following prompts work well as oral questions, written checks, or team debrief prompts.

| Prompt | Expected answer quality |
|---|---|
| Why does Day 4 reuse the Day 2 run-folder schema? | Students should say that the schema provides a platform-independent evidence contract for metadata, plan, state logs, and checkpoint artifacts. |
| Why is video alone insufficient for an inspection report? | Students should explain that video lacks structured metadata, checkpoint mapping, and runtime state context unless packaged with other artifacts. |
| What is the difference between a raw capture and checkpoint evidence? | A raw capture is an original file; checkpoint evidence is selected, named, and placed under `checkpoints/<id>/frame.jpg` with context. |
| When should students capture a checkpoint still? | During a stable dwell or stopped state, not during turning or translation. |
| What does `sportmodestate.jsonl` contribute? | It provides time-series robot state evidence such as mode, gait, position, velocity, yaw speed, and body height. |
| What should happen if RTSP recording fails? | Students should document the failure, preserve terminal output if possible, use still images/state logs as fallback, and explain the limitation. |
| Why should optional OpenCV effects not replace raw frames? | Processed images are derived artifacts; raw frames preserve primary evidence integrity. |

---

## 19. Suggested 3-hour board narrative

A useful way to teach Day 4 is to write the following equation on the board:

> **Inspection Run = Scenario + Safety + Video + State + Motion Notes + Checkpoint Package + Validation + Debrief**

Each time students produce an artifact, place it under one term in the equation. This keeps the class focused on the professional goal: a field run that can be understood by someone who was not present during the demonstration.

| Equation term | Concrete Day 4 question |
|---|---|
| Scenario | What are we inspecting, and where are the checkpoints? |
| Safety | Who can stop the robot, and what is the exclusion zone? |
| Video | Which camera and file prove visual context? |
| State | What did SportModeState report during capture? |
| Motion notes | Which command moved the robot, for how long, and why? |
| Checkpoint package | Which `frame.jpg` belongs to each checkpoint ID? |
| Validation | Did the folder pass, fail, or pass with warnings? |
| Debrief | What claim can we defend with the artifacts? |

---

## 20. Capstone preparation for later course days

Although Day 5 moves to G1, Day 4 establishes habits that remain important across platforms. The most transferable habit is **evidence-first robotics**. Whether the robot is a quadruped, humanoid, arm, or sensor platform, students should plan what evidence they need before running the system.

Day 4 also prepares students for analytics discussions. The optional video-effects script shows that computer vision can process inspection imagery, but the stronger professional lesson is that analytics depends on good data organization. A detection result is useful only if the original frame, timestamp, checkpoint ID, robot state, and scenario are preserved.

| Future topic | Day 4 foundation |
|---|---|
| G1 architecture | DDS readiness, interface discipline, and safety observer roles. |
| Humanoid locomotion | Conservative command boundaries and stop authority. |
| Manipulation or arm demos | Evidence packaging and role separation. |
| Speech/audio/LED capstone | Multimodal artifact organization and reportability. |
| Automated analytics | Raw-data preservation, derived outputs, and validation checks. |

---

## 21. Final instructor checklist

Before ending the lecture, the instructor should make students demonstrate comprehension in three forms: verbal explanation, file organization, and validation interpretation. A student who can only run the scripts has not yet mastered Day 4. A student who can explain why each artifact exists and how it supports a report is ready for field-style robotics practice.

| Competency | Minimum acceptable performance | Strong performance |
|---|---|---|
| Safety framing | Names the stop authority and checks the area. | Explains why B2 mass and motion require procedural discipline. |
| Camera operation | Saves at least one usable still image. | Captures front/back stills and verifies a playable video. |
| State awareness | Identifies SportModeState fields. | Connects state fields to checkpoint timing and image quality. |
| Motion supervision | Uses only approved high-level commands. | Explains command purpose, boundary, and recovery plan. |
| Run packaging | Creates required folder/files. | Preserves raw files and maps selected evidence into checkpoint folders. |
| Validation | Runs the validator. | Interprets warnings and updates the report accordingly. |
| Debrief | Gives a general summary. | Makes artifact-backed claims with file names and limitations. |

The closing message should be direct: Day 4 is successful when the team can hand its run folder to another engineer and that engineer can understand the scenario, evidence, robot state, safety context, and limitations without watching the live run.

---

## 22. References

[1]: https://github.com/Vinci-AI-Analytics/vinci-unitree/blob/main/course/day-04/README.md "Vinci-AI-Analytics — Day 4: B2 Advanced Scenarios & Field Inspection"

[2]: https://github.com/Vinci-AI-Analytics/vinci-unitree/blob/main/course/SCHEDULE-TTT.md "Vinci-AI-Analytics — TtT Schedule Map"

[3]: https://support.unitree.com/home/en/B2_developer/About%20B2 "Unitree Robotics — B2 SDK Development Guide: About B2"

[4]: https://github.com/Vinci-AI-Analytics/vinci-unitree/blob/main/course/day-04/lab-00/README.md "Vinci-AI-Analytics — Day 4 Lab 0: Inspection Scenario & Run Folder"

[5]: https://github.com/Vinci-AI-Analytics/vinci-unitree/blob/main/course/day-02/lab-01/lab01_validate_run_folder.py "Vinci-AI-Analytics — Day 2/Day 4 Run Folder Validator"

[6]: https://github.com/Vinci-AI-Analytics/vinci-unitree/blob/main/course/day-04/lab-01/README.md "Vinci-AI-Analytics — Day 4 Lab 1: Mock Inspection Video"

[7]: https://support.unitree.com/home/en/developer/Multimedia_Services "Unitree Robotics — Multimedia Services Interface"

[8]: https://github.com/Vinci-AI-Analytics/vinci-unitree/blob/main/scripts/ives_sdk/B2/camera_opencv-videoEffect.py "Vinci-AI-Analytics — B2 OpenCV Video Effect Script"

[9]: https://github.com/Vinci-AI-Analytics/vinci-unitree/blob/main/course/day-04/lab-02/README.md "Vinci-AI-Analytics — Day 4 Lab 2: Field Run & Reporting"

[10]: https://github.com/Vinci-AI-Analytics/vinci-unitree/blob/main/scripts/ives_sdk/B2/subscribe_sport_mode_state.py "Vinci-AI-Analytics — B2 SportModeState Subscriber Script"

[11]: https://github.com/Vinci-AI-Analytics/vinci-unitree/blob/main/scripts/ives_sdk/B2/b2_sport_client.py "Vinci-AI-Analytics — B2 Sport Client Script"

[12]: https://support.unitree.com/home/en/developer/sports_services "Unitree Robotics — Sports Services Interface"
