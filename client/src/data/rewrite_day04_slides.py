#!/usr/bin/env python3
"""
Rewrite DAY04 slides in build_syllabus.py to 43 slides
aligned with "Day 4 Beginner-Friendly Full Slide Content" curriculum.
STRICT: Slide 7 (SLAM) is completely excluded per user directive.
All SLAM terminology stripped from all slide content.
Keyword bolding uses <strong class="font-bold"> only — NEVER text-foreground.
bold() NEVER called on titles or table headers — those render as plain text.
"""
import re, json as _json

# ── Day 4 keyword bolding — NO SLAM terms ──
def bold(s):
    patterns = [
        # Platform
        (r'\b(B2)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(Unitree)\b', r'<strong class="font-bold">\1</strong>'),
        # Middleware
        (r'\b(Gazebo)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(ROS 2)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(DDS)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(CycloneDDS)\b', r'<strong class="font-bold">\1</strong>'),
        # SDK clients
        (r'\b(SportClient)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(VideoClient)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(FrontVideoClient)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(BackVideoClient)\b', r'<strong class="font-bold">\1</strong>'),
        # State / telemetry
        (r'\b(SportModeState)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(telemetry)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(payload)\b', r'<strong class="font-bold">\1</strong>'),
        # Capture / processing
        (r'\b(RTSP)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(OpenCV)\b', r'<strong class="font-bold">\1</strong>'),
        # Motion commands
        (r'\b(StopMove)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(Damp)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(StandDown)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(RecoveryStand)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(Move)\b', r'<strong class="font-bold">\1</strong>'),
        # Key concepts
        (r'\b(costmap)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(inspection)\b', r'<strong class="font-bold">\1</strong>'),
        # File extensions / names
        (r'\b(\.json)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(\.jsonl)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(\.jpg)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(\.md)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(metadata\.json)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(patrol_plan\.json)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(sportmodestate\.jsonl)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(frame\.jpg)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(field_report\.md)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(run_folder)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(run-folder)\b', r'<strong class="font-bold">\1</strong>'),
    ]
    for pat, repl in patterns:
        s = re.sub(pat, repl, s)
    return s

# ── 43 Slides (Cover combined with Slide 1, then Slides 2–44 minus SLAM Slide 7) ──
SLIDES = [
    # ── Cover / Slide 1: Day 4 Has Four Jobs ──
    {
        "title": "Day 4 — B2 Rugged Inspection, Mock Scripts, Field Capture, Telemetry, Reporting, and Maintenance",
        "thesis": bold("Day 4 is focused on four practical jobs. Students reason about rugged terrain and multi-sensor evidence, build mock inspection scripts, execute a supervised B2 inspection with camera capture and telemetry logging, then parse data into reports and maintenance notes. Anything outside those jobs is intentionally minimized."),
        "board_type": "grid",
        "board_data": [
            {"label": bold("Rugged Navigation"), "value": bold("Understand how terrain affects robot behavior and evidence quality — slope, gravel, glare, occlusion, vibration all change what the B2 can safely prove.")},
            {"label": bold("Mock Inspection Scripts"), "value": bold("Build procedural scripts that rehearse capture, logging, motion, packaging, and validation before the hardware run — simulation gates must pass first.")},
            {"label": bold("B2 Field Execution"), "value": bold("Execute a supervised B2 inspection with camera capture and telemetry logging — defined roles, observable readiness, stable-dwell capture, and immediate verification.")},
            {"label": bold("Logs, Reports, Maintenance"), "value": bold("Parse telemetry into fields, visualize motion and capture, write artifact-backed reports, validate packages, debug failures, and complete B2 hardware maintenance.")},
        ],
        "bottom_band": bold("Day 4 rule: Every activity must connect to one of these four outcomes. If an activity does not produce evidence for rugged navigation, mock scripting, field capture, or reporting — it is not a Day 4 activity.")
    },
    # ── Slide 2: One Flow Organizes Everything ──
    {
        "title": "One Flow Organizes Everything",
        "thesis": bold("The whole day can be taught through one repeated workflow. Students plan the inspection, capture sensor evidence, log robot state, package artifacts into the run folder, validate the structure, and write the report. This reduces redundancy because every activity must connect to one step in the same flow."),
        "board_type": "list",
        "board_data": [
            bold("Plan: Define the inspection scenario — checkpoints, route, capture targets, and roles. Write metadata.json and patrol_plan.json before any robot motion."),
            bold("Capture: Execute camera stills and RTSP clips at designated checkpoints. Verify every saved file opens and matches the intended scene."),
            bold("Log: Record SportModeState telemetry continuously from before motion through final notes. Each JSONL line is one inspectable state sample."),
            bold("Package: Organize raw captures, selected checkpoint frames, telemetry logs, and metadata into the standard run-folder schema."),
            bold("Validate: Run the validator against the completed package. Structural PASS is required before report writing. Warnings still need explanation."),
            bold("Report: Write artifact-backed claims using the pattern — claim, artifact, telemetry context, limitation, confidence. The report is the final deliverable."),
        ],
        "bottom_band": bold("Workflow check: Can you draw the six-box arrow — Plan → Capture → Log → Package → Validate → Report — and name one concrete artifact produced at each step? If not, drill that step before the field run.")
    },
    # ── Slide 3: Evidence Is the Standard ──
    {
        "title": "Evidence Is the Standard",
        "thesis": "Students should not treat video, logs, or notes as separate assignments. They are parts of one evidence standard. A useful inspection claim should identify what was observed, where it happened, when it happened, and which artifact supports it. This standard guides navigation, scripting, field capture, and reporting.",
        "board_type": "grid",
        "board_data": [
            {"label": bold("File"), "value": bold("The concrete artifact — frame.jpg, sportmodestate.jsonl, field_report.md. A claim without a matching file is an opinion, not evidence.")},
            {"label": bold("Timestamp"), "value": "When the observation occurred — aligned across camera, telemetry, and operator notes. Timing connects multi-sensor evidence into one coherent moment."},
            {"label": bold("Checkpoint"), "value": bold("Where the observation occurred — mapped to a named checkpoint ID such as cp01, cp02, or cp03. Location context makes evidence spatially meaningful.")},
            {"label": bold("Context Note"), "value": "What the file cannot show by itself — glare, occlusion, vibration, fallback decisions. Honest notes make the final inspection more credible, not weaker.")},
        ],
        "bottom_band": bold("Evidence test: 'If someone disputes this inspection claim, what specific file, timestamp, checkpoint, and note would I show to defend it?' If you cannot answer all four, the claim is not yet evidence-backed.")
    },
    # ── Slide 4: Section 1 — Rugged Navigation and Multi-Sensor Arrays ──
    {
        "title": "Section 1 — Rugged Navigation and Multi-Sensor Arrays",
        "thesis": "Understand terrain, sensing roles, and runtime evidence for inspection. This section covers rugged terrain effects, bounded navigation, costmaps, obstacle supervision, sensor roles, timing alignment, and telemetry context — everything needed to explain what the robot perceived and why the path was chosen.",
        "board_type": "grid",
        "board_data": [
            {"label": "Core Idea", "value": "Terrain is not just background — it changes robot behavior and evidence quality. Slope, gravel, glare, occlusion, and vibration affect what the final report can honestly defend."},
            {"label": "Key Principle", "value": bold("Navigation for inspection means bounded progress — know the checkpoint, choose a safe path, move in small steps, stop to prove. Not full autonomy, but explainable supervised motion.")},
            {"label": "Sensor Array", "value": "Each sensor answers a different question — camera sees appearance, telemetry explains motion, payload measures condition, notes explain limits. Multi-sensor means multi-question, not just more data."},
            {"label": "Section Slides", "value": "Slides 5–11: Rugged terrain, bounded navigation, costmaps, obstacle supervision, sensor roles, timing alignment, and SportModeState telemetry context."},
        ],
        "bottom_band": bold("Section framing: By the end of this section, you should be able to explain how terrain conditions affect evidence quality and what each sensor channel contributes to an inspection claim.")
    },
    # ── Slide 5: Rugged Terrain Changes the Run ──
    {
        "title": "Rugged Terrain Changes the Run",
        "thesis": "Rugged terrain is important because it changes both robot behavior and evidence quality. A slope may alter posture, loose surface may affect traction, glare may hide inspection details, and vibration may blur images. Students should record these conditions because they influence what the final report can honestly defend.",
        "board_type": "grid",
        "board_data": [
            {"label": bold("Slope"), "value": "Alters robot posture and weight distribution. May change camera aim point and affect the appearance of captured inspection targets."},
            {"label": bold("Loose Surface"), "value": "Reduces traction and increases odometry uncertainty. The robot may slip slightly — route accuracy degrades compared to hard floor."},
            {"label": bold("Glare / Lighting"), "value": "Direct sunlight or reflections can wash out camera images. Inspection details become harder to verify — the report must note this limitation."},
            {"label": bold("Vibration"), "value": bold("B2 gait vibration can blur still images and shake video. Stable-dwell capture becomes more important on rough terrain than on smooth floor.")},
        ],
        "bottom_band": bold("Terrain recording habit: At each checkpoint, note one terrain condition that could affect evidence — slope angle, surface type, lighting direction, or vibration level. One sentence per checkpoint is enough.")
    },
    # ── Slide 6: Navigation Means Bounded Progress ──
    {
        "title": "Navigation Means Bounded Progress",
        "thesis": bold("For Day 4, navigation means making safe, explainable progress toward inspection checkpoints. Students do not need advanced autonomy theory to act professionally. They need a checkpoint goal, a visible hazard plan, bounded motion, a stop point, and evidence that the robot reached the inspection view safely."),
        "board_type": "list",
        "board_data": [
            bold("Know the checkpoint: Identify the target inspection position before motion begins. The destination should be marked, visible, and agreed by the team."),
            bold("Choose a safe path: Identify hazards between the current position and the checkpoint. Mark any slope, obstacle, or uncertain surface that the route must avoid."),
            bold("Move in small steps: Use bounded velocity and short-duration commands. The first motion should be the smallest meaningful displacement — observe before increasing."),
            bold("Stop to prove: Dwell at the checkpoint until the robot is stable. Capture evidence only after motion has stopped. A blurred image during translation is not inspection evidence."),
        ],
        "bottom_band": bold("Navigation test: Before any B2 motion, ask aloud: 'What is the checkpoint? What hazards are between here and there? What is my first small command? When will I stop to capture?' If any answer is unclear, do not move.")
    },
    # ── Slide 7: Costmaps Turn Space into Risk ── (was Slide 8 — SLAM slide 7 excluded)
    {
        "title": "Costmaps Turn Space into Risk",
        "thesis": bold("A costmap is a simple way to turn space into movement risk. Clear floor is low cost, blocked areas are not usable, and uncertain surfaces should increase caution. Students should use the costmap idea to explain why the B2 path avoids hazards and where human supervision remains necessary."),
        "board_type": "grid",
        "board_data": [
            {"label": bold("Free Space (Low Cost)"), "value": bold("Clear, traversable floor — the planner can route through these cells freely. Confirmed by sensor data showing no obstacles and stable surface.")},
            {"label": bold("Obstacle (Blocked)"), "value": "Cells containing detected barriers — walls, equipment, cones. The path must never route through these. Marked as lethal cost."},
            {"label": bold("Uncertain Terrain (Caution)"), "value": "Cells where sensor data is sparse, terrain type is ambiguous, or surface condition is unknown. Conservative planning treats these as high-cost or avoids them entirely."},
            {"label": bold("Human Supervision Zone"), "value": "Areas where sensor confidence is low and human judgment is required. The operator decides whether the path is safe — the costmap advises, it does not guarantee.")},
        ],
        "bottom_band": bold("Costmap exercise: Draw a simple grid. Mark one free cell, one obstacle cell, and one uncertain cell near your B2 arena. For each, explain what the robot should do and where the human must supervise.")
    },
    # ── Slide 8: Obstacle Avoidance Needs Supervision ── (was Slide 9)
    {
        "title": "Obstacle Avoidance Needs Supervision",
        "thesis": "Obstacle avoidance is useful, but it is not a guarantee. Sensors can miss low, reflective, moving, transparent, or poorly lit hazards. The safe envelope still depends on field roles, slow motion, visible boundaries, and immediate stop authority. This keeps rugged navigation connected to practical field discipline.",
        "board_type": "list",
        "board_data": [
            bold("Sensor detection layer: Cameras and depth sensors identify obstacles within their field of view. Detection has blind spots — low objects, reflective surfaces, transparent materials, and dark areas."),
            bold("Software caution layer: The avoidance system adjusts velocity or stops when obstacles are detected within configured thresholds. Software cannot see what sensors miss."),
            bold("Human supervision layer: The spotter watches the full robot perimeter and arena. Human judgment catches what sensors and software miss — and has immediate stop authority."),
        ],
        "bottom_band": bold("Safety envelope rule: The three layers — sensor, software, human — must all be active during B2 motion. If any layer is compromised (sensor blocked, software disabled, spotter distracted), stop immediately.")
    },
    # ── Slide 9: Each Sensor Has a Job ── (was Slide 10)
    {
        "title": "Each Sensor Has a Job",
        "thesis": "A multi-sensor array should not be described as collecting more data. Each channel answers a different question. Camera frames show visual condition, telemetry explains how the robot moved, payload data may measure the target, and notes document uncertainty. The report improves when these roles are explicit.",
        "board_type": "table",
        "board_data": {
            "headers": ["Sensor", "Question It Answers", "Artifact It Produces", "Report Use"],
            "rows": [
                ["Camera (Front / Rear)", "What does the inspection target look like?", bold("Still image (frame.jpg) or RTSP video clip."), "Primary visual evidence of target condition."],
                [bold("SportModeState Telemetry"), "How did the robot move and stand?", bold("sportmodestate.jsonl — one JSON line per state sample."), "Explains motion context: was the robot stable during capture?"],
                [bold("Payload Data"), "What does the target measure?", "Sensor reading with timestamp and checkpoint label.", "Adds quantitative measurement to visual inspection."],
                ["Operator Notes", "What can the files not show?", "Checkpoint notes — glare, occlusion, fallback decisions.", "Documents limitations that affect claim confidence."],
            ]
        },
        "bottom_band": bold("Sensor discipline: For every inspection checkpoint, identify which sensors contributed evidence and which question each sensor answered. A checkpoint with camera-only evidence is weaker than one with camera + telemetry + notes.")
    },
    # ── Slide 10: Timing Connects the Sensors ── (was Slide 11)
    {
        "title": "Timing Connects the Sensors",
        "thesis": "Multi-sensor evidence is strongest when timing is clear. A camera frame, telemetry line, payload measurement, and operator note should all point to the same checkpoint moment. Beginners can start with checkpoint IDs and approximate timestamps, then improve synchronization as their scripting skills mature.",
        "board_type": "list",
        "board_data": [
            bold("Camera frame timestamp: The moment the image was captured. Compare with telemetry to confirm the robot was stationary — a frame taken during motion may be blurred."),
            bold("SportModeState line timestamp: The moment the robot reported its state. Align with camera timestamps to verify stable dwell before capture."),
            bold("Payload reading timestamp: The moment the sensor measurement was taken. Must be close to the camera timestamp for the data to describe the same inspection moment."),
            bold("Operator note timestamp: The moment the observation was recorded. Should reference the same checkpoint ID as the automated logs for cross-referencing."),
        ],
        "bottom_band": bold("Timing check: At checkpoint cp01, do your camera frame, telemetry line, payload reading, and note all reference the same checkpoint ID and similar timestamps? If not, the multi-sensor claim is weakened by timing misalignment.")
    },
    # ── Slide 11: Telemetry Is Runtime Context ── (was Slide 12)
    {
        "title": "Telemetry Is Runtime Context",
        "thesis": bold("SportModeState is the robot's runtime context. If a checkpoint frame is blurred, velocity or yaw speed may explain it. If posture looks unusual, body height or mode may help. Students should use telemetry as supporting evidence, not as an isolated log file."),
        "board_type": "grid",
        "board_data": [
            {"label": "Motion Panel", "value": bold("Velocity (vx, vy, vyaw) — was the robot moving or turning during capture? High velocity during a checkpoint frame explains blur and weakens the claim.")},
            {"label": "Posture Panel", "value": bold("Body height, pitch, roll — was the robot level and stable? Slope or uneven footing changes the camera aim point and image composition.")},
            {"label": "Mode Panel", "value": bold("Current SportModeState mode — is the robot in a safe, expected state? Unexpected mode transitions during inspection indicate a control or script problem.")},
            {"label": "Timing Panel", "value": "Timestamp and sequence — does the telemetry record cover the full run window from before first motion through after final capture? Gaps create blind spots."},
        ],
        "bottom_band": bold("Telemetry habit: When reviewing a checkpoint frame, open the corresponding SportModeState line. Ask: was velocity near zero? Was posture stable? Was mode as expected? If any answer is no, note it in the report.")
    },
    # ── Slide 12: Section 2 — Mock Inspection Scripts ── (was Slide 13)
    {
        "title": "Section 2 — Mock Inspection Scripts",
        "thesis": "Build the inspection workflow safely before the B2 field run. This section covers mock-first workflow, Gazebo rehearsal, procedural scripts, scenario files, camera capture, OpenCV-derived outputs, JSONL logging, bounded motion, channel-by-channel debugging, and validation readiness gates.",
        "board_type": "grid",
        "board_data": [
            {"label": "Core Idea", "value": bold("Mock scenario passes → folder structure passes → instructor approves B2 handoff. Hardware begins only after the mock workflow and folder structure are understandable enough for instructor approval.")},
            {"label": "Key Principle", "value": "A functional inspection script should make the run procedure visible — Setup, Capture, Log, Move, Package, Validate as separate steps. No black-box scripts that hide failures."},
            {"label": "Validation Gate", "value": bold("If the mock package fails validation, the B2 run should wait. Missing metadata, empty telemetry, or absent checkpoint frames show the procedure is not ready.")},
            {"label": "Section Slides", "value": "Slides 13–22: Mock-first gate, Gazebo rehearsal, procedural scripts, scenario files, camera capture, OpenCV outputs, JSONL logging, bounded motion, debugging, and validation."},
        ],
        "bottom_band": bold("Section rule: The mock run is not optional practice — it is a required gate. Prove the workflow produces reviewable evidence before the B2 leaves its standby position.")
    },
    # ── Slide 13: Mock First, Then Hardware ── (was Slide 14)
    {
        "title": "Mock First, Then Hardware",
        "thesis": "Students should prove the workflow before the hardware run. A mock scenario lets them define checkpoints, test capture placeholders, write metadata, and package the run folder. Hardware begins only after the mock workflow and folder structure are understandable enough for instructor approval.",
        "board_type": "list",
        "board_data": [
            bold("Mock Scenario: Define checkpoints, route, capture targets, and metadata. Create patrol_plan.json and metadata.json — these files set intent before any capture occurs."),
            bold("Run Folder Check: Build the folder structure — checkpoints/cp01/, raw_captures/, logs/. Confirm every required path exists and naming conventions are followed."),
            bold("Instructor Approval: Present the mock package. Instructor confirms: scenario is defined, folder structure is correct, capture plan is clear, validation rules are understood."),
            bold("B2 Handoff: Only after approval does the team proceed to hardware. The mock package becomes the template for the field run folder."),
        ],
        "bottom_band": bold("Gate discipline: 'Our mock folder passed validation and the instructor approved handoff.' If you cannot say this sentence truthfully, the B2 should not move.")
    },
    # ── Slide 14: Gazebo Rehearses the Logic ── (was Slide 15)
    {
        "title": "Gazebo Rehearses the Logic",
        "thesis": bold("Gazebo is useful because it lets students rehearse inspection logic before field risk appears. It does not replace the B2 run, but it helps teams practice checkpoint sequencing, sensor thinking, timing, and recovery decisions. The lesson is rehearsal discipline, not simulation perfection."),
        "board_type": "grid",
        "board_data": [
            {"label": bold("Gazebo Rehearsal"), "value": bold("Practice checkpoint sequencing, sensor activation, timing, and recovery decisions in a risk-free environment. Errors in Gazebo cost time, not hardware damage or safety incidents.")},
            {"label": bold("B2 Field Run"), "value": bold("Execute the rehearsed workflow on hardware with real terrain, lighting, network conditions, and sensor behavior. Compare field results with Gazebo expectations.")},
            {"label": "Comparison", "value": bold("Differences between Gazebo rehearsal and B2 field run are engineering insights — they reveal real-world effects that simulation cannot fully capture (floor texture, lighting, latency).")},
        ],
        "bottom_band": bold("Rehearsal rule: 'Gazebo tells you whether your logic makes sense. The B2 tells you whether reality agrees.' Never skip the rehearsal — never assume the field will match simulation perfectly.")
    },
    # ── Slide 15: Scripts Should Show Procedure ── (was Slide 16)
    {
        "title": "Scripts Should Show Procedure",
        "thesis": "A functional inspection script should make the run procedure visible. Students should see setup, capture, logging, movement, packaging, and validation as separate steps. This prevents a black-box script from hiding failures and makes the workflow easier to debug when camera, telemetry, or folder paths break.",
        "board_type": "list",
        "board_data": [
            bold("Setup: Initialize SDK clients, verify network interface, confirm SportModeState subscription, open output files. Print confirmation of each initialization step."),
            bold("Capture: Execute camera stills or RTSP recording at designated moments. Verify each saved file — check file size, try to open, confirm scene matches checkpoint."),
            bold("Log: Write SportModeState samples to sportmodestate.jsonl continuously. Each line is one timestamped state record — mode, gait, velocity, position, body height."),
            bold("Move: Send bounded motion commands through SportClient. Small values, short duration, observed behavior. StopMove after each leg."),
            bold("Package: Organize artifacts into the run folder — raw captures preserved, selected frames copied to checkpoints/<id>/frame.jpg, logs in place."),
            bold("Validate: Run the validator against the completed package. PASS → proceed to report. FAIL → repair and re-validate before claiming readiness."),
        ],
        "bottom_band": bold("Script transparency: Can another student read your script and understand what each section does without running it? If not, add print statements and section comments until the procedure is visible.")
    },
    # ── Slide 16: Scenario Files Set Intent ── (was Slide 17)
    {
        "title": "Scenario Files Set Intent",
        "thesis": "The mock scenario should create intent before any capture occurs. Metadata identifies operator, date, robot, and run context. The patrol plan identifies checkpoint IDs and what each checkpoint should inspect. These files make the inspection script accountable and keep later report claims tied to planned targets.",
        "board_type": "grid",
        "board_data": [
            {"label": bold("metadata.json"), "value": bold("Operator name, date, robot ID, run scenario description, interface used. Says who ran the inspection, when, and under what conditions — accountability before evidence.")},
            {"label": bold("patrol_plan.json"), "value": bold("Checkpoint IDs, leg definitions, capture actions, speed limits, dwell requirements. Says what checkpoints matter and what evidence each should produce.")},
            {"label": "Checkpoint Folders", "value": bold("checkpoints/cp01/, cp02/, cp03/ — each contains frame.jpg, the selected inspection image. The folder path encodes the checkpoint identity.")},
        ],
        "bottom_band": bold("Intent check: Before any capture, can you open metadata.json and patrol_plan.json and read exactly what inspection targets are planned? If the plan is vague, the evidence will be vague.")
    },
    # ── Slide 17: Camera Scripts Capture Context ── (was Slide 18)
    {
        "title": "Camera Scripts Capture Context",
        "thesis": "Camera scripts produce visual context for inspection, but saved files should be checked before they are trusted. Students should confirm that a still image opens, a video plays, and the content matches the intended checkpoint. This keeps capture focused on usable evidence rather than file creation alone.",
        "board_type": "list",
        "board_data": [
            bold("Front / Rear Still Capture: Use VideoClient to grab a single frame. Save as a timestamped or checkpoint-labeled .jpg file. Confirm the image opens and shows the expected scene."),
            bold("RTSP Video Recording: Open the RTSP stream, configure writer settings (codec, resolution, frame rate), record the approach and dwell, close the file. Verify playback before trusting the recording."),
            bold("File Verification: Check file size > minimum threshold, attempt to open with a standard viewer, confirm scene content matches checkpoint description. A file that cannot be opened is not evidence."),
            bold("Map to Checkpoint: Copy verified frame to checkpoints/<id>/frame.jpg. The raw capture is preserved separately — the checkpoint folder holds the selected, verified evidence."),
        ],
        "bottom_band": bold("Verification rule: 'The file saved successfully' is not the same as 'the file is usable evidence.' Open every capture before leaving the checkpoint. A corrupt or misaimed frame discovered during reporting is too late to fix.")
    },
    # ── Slide 18: OpenCV Outputs Are Derived ── (was Slide 19)
    {
        "title": "OpenCV Outputs Are Derived",
        "thesis": bold("OpenCV can help demonstrate simple image processing, but processing should not overwrite evidence. Raw frames are the primary record. Edge views, filters, annotations, and detection outputs are derived artifacts. Students should preserve both and explain which one supports the report claim."),
        "board_type": "grid",
        "board_data": [
            {"label": bold("Raw Frame (Primary)"), "value": bold("The original, unmodified image from the camera — preserved as the authoritative visual record. Never delete, overwrite, or modify the raw capture file.")},
            {"label": bold("Derived Output (Secondary)"), "value": bold("Processed images — edge detection, filtering, annotation overlays, object detection bounding boxes. Useful for highlighting features, but derived from the raw frame.")},
            {"label": "Report Usage", "value": "The report should cite the raw frame as primary evidence. Derived outputs can illustrate specific features but cannot replace the original — if processing introduces artifacts, the raw frame is the fallback."},
        ],
        "bottom_band": bold("Processing discipline: 'I applied an edge filter to highlight cracks. The raw frame is preserved at raw_captures/front_<ts>.jpg. The filtered output is at derived/edge_<ts>.jpg.' Both files, clearly labeled, with the raw frame as the authoritative source.")
    },
    # ── Slide 19: JSONL Makes Logs Inspectable ── (was Slide 20)
    {
        "title": "JSONL Makes Logs Inspectable",
        "thesis": bold("A JSONL telemetry log is beginner-friendly because each line can be inspected as one state sample. Students can open the file, read a line, and find fields such as mode, velocity, yaw speed, or body height. This structure prepares the file for later parsing and visualization."),
        "board_type": "grid",
        "board_data": [
            {"label": bold("JSONL Structure"), "value": bold("One complete JSON object per line. Each line is a self-contained SportModeState sample — no multi-line objects, no trailing commas, no array wrappers. Readable with any text editor.")},
            {"label": "Key Fields", "value": bold("mode, gait, position[x,y,yaw], velocity[vx,vy,vyaw], bodyHeight, timestamp. These fields explain the robot's motion and posture at each sampled moment.")},
            {"label": "Parsing Ready", "value": "Each line can be loaded with json.loads() independently. Students can extract fields, filter by timestamp, or plot values without parsing a complex nested structure."},
        ],
        "bottom_band": bold("Log inspectability: Open your sportmodestate.jsonl file. Can you read line 10 and explain what the robot was doing at that moment — mode, velocity, posture? If not, add field labels or documentation until it is self-explanatory.")
    },
    # ── Slide 20: Motion Commands Stay Small ── (was Slide 21)
    {
        "title": "Motion Commands Stay Small",
        "thesis": "Mock scripts should teach the same discipline used on hardware. A high-level motion command needs instructor approval, small values, short duration, visible observation, and an explicit stop. Students should record the result, because the report needs to explain what command produced the captured evidence.",
        "board_type": "list",
        "board_data": [
            bold("Approved command: Instructor confirms the motion is appropriate — destination, speed, duration, and safety conditions are reviewed before execution."),
            bold("Short duration: Commands are sent for limited time or distance. The first motion should be the smallest meaningful displacement — ~0.2 m or ~0.3 rad."),
            bold("Observe: Watch the robot's response. Did it move in the expected direction? At the expected speed? Did it stop when commanded? Record what you observed, not what you expected."),
            bold("StopMove: Send explicit stop command after each motion leg. Redundant stop commands are safer — a single StopMove may not be enough. Confirm the robot is stationary before next capture."),
            bold("Note result: Document the command, the observed behavior, and any deviation. The report needs to connect each motion command to the evidence it produced."),
        ],
        "bottom_band": bold("Motion safety: 'What command am I about to send? What do I expect the robot to do? What will I do if the robot does something different?' Answer all three before any B2 motion — mock or hardware.")
    },
    # ── Slide 21: Debug One Channel at a Time ── (was Slide 22)
    {
        "title": "Debug One Channel at a Time",
        "thesis": "When a script fails, students should avoid changing everything at once. They should test the camera path alone, telemetry logger alone, folder structure alone, and validator alone before combining them. This debugging habit turns failures into evidence about which channel needs repair.",
        "board_type": "list",
        "board_data": [
            bold("1. Camera alone: Test that the video client initializes, captures a still, and saves a readable .jpg file. No telemetry, no motion — just one camera channel."),
            bold("2. Logger alone: Test that the SportModeState subscriber writes valid JSONL lines to a file. Confirm lines are parseable and contain expected fields."),
            bold("3. Folder paths alone: Test that the run folder structure is created correctly — all directories exist, naming conventions are correct, placeholder files validate."),
            bold("4. Validator alone: Run the validator against a known-good folder and a known-bad folder. Confirm it correctly distinguishes PASS from FAIL — the validator itself must be trustworthy."),
            bold("5. Combined run: Only after all four channels work independently, combine them into the full inspection script. Channel-by-channel confidence before integration."),
        ],
        "bottom_band": bold("Debugging staircase: Start at the bottom (single channel), confirm it works, move up one step. A failure in the combined run can now be traced to the specific channel that broke — because you already proved each one works alone.")
    },
    # ── Slide 22: Validation Catches Script Gaps ── (was Slide 23)
    {
        "title": "Validation Catches Script Gaps",
        "thesis": "The validator is a readiness gate for the script, not just a grading tool. Missing metadata, empty telemetry, absent checkpoint frames, or mismatched checkpoint IDs show that the procedure is not ready. Repairing these gaps in the mock run prevents avoidable field confusion.",
        "board_type": "grid",
        "board_data": [
            {"label": bold("PASS"), "value": bold("All required files present, all paths correct, all structural checks satisfied. The package is reviewable — proceed to report writing and B2 handoff gate.")},
            {"label": bold("PASS with Warnings"), "value": bold("Structure is valid but one or more checks produced warnings — e.g., image file is small, JSONL line count is low, optional fields missing. Warnings must be explained in the report.")},
            {"label": bold("FAIL"), "value": bold("Required file missing, path incorrect, checkpoint ID mismatch, or structural error. The package is not reviewable — repair the script and re-validate before proceeding.")},
        ],
        "bottom_band": bold("Validator as gate: Mock folder → Run validator → PASS? → Proceed to instructor approval. FAIL? → Identify the specific gap, repair the script, re-run mock, re-validate. Never skip validation because 'the files are probably there.'")
    },
    # ── Slide 23: Section 3 — B2 Field Execution ── (was Slide 24)
    {
        "title": "Section 3 — B2 Field Execution",
        "thesis": "Run the supervised inspection, capture sensors, and log telemetry. This section covers field roles, observable readiness, stable-dwell capture, RTSP verification, continuous telemetry logging, checkpoint mapping, field notes, immediate verification, and stated fallbacks.",
        "board_type": "grid",
        "board_data": [
            {"label": "Core Idea", "value": bold("A B2 field run needs clear roles before motion. The run director, terminal operator, spotter, evidence lead, and reporter each have defined responsibilities — role clarity prevents unsafe mixed instructions.")},
            {"label": "Key Principle", "value": "Readiness is observable — interface selected, perimeter clear, stop path known, cameras tested, logger ready. Students show readiness through checks, not confidence statements."},
            {"label": "Capture Rule", "value": bold("Move to view, stop or dwell, capture, label checkpoint, continue. Checkpoint evidence is strongest when the robot is stable — never capture during turning or translation.")},
            {"label": "Section Slides", "value": "Slides 24–32: Field roles, observable readiness, stable-dwell capture, RTSP verification, telemetry logging window, checkpoint mapping, field notes, immediate verification, and fallback procedures."},
        ],
        "bottom_band": bold("Section rule: The first B2 field command is not a full inspection. It is a single small motion — then stop, review, and decide whether to continue. Staged confidence, not rushed demonstration.")
    },
    # ── Slide 24: Field Roles Keep Order ── (was Slide 25)
    {
        "title": "Field Roles Keep Order",
        "thesis": bold("A B2 field run needs clear roles before motion. The run director approves action, the terminal operator controls commands, the spotter watches the robot and space, the evidence lead checks saved files, and the reporter records limitations. Role clarity prevents excited students from creating unsafe mixed instructions."),
        "board_type": "grid",
        "board_data": [
            {"label": bold("Run Director"), "value": "Approves all motion and capture actions. Has final authority to proceed or halt. No command is sent without the director's explicit approval."},
            {"label": bold("Terminal Operator"), "value": "Executes commands at the keyboard. Reads each command aloud before sending. Watches console output for errors or unexpected responses."},
            {"label": bold("Spotter"), "value": "Watches the robot and surrounding space continuously. Holds immediate stop authority — spotter says stop, operator stops, no questions asked in the moment."},
            {"label": bold("Evidence Lead"), "value": "Checks every saved file immediately after capture — opens the image, confirms scene, verifies file size. Declares whether evidence is usable or needs recapture."},
            {"label": bold("Reporter"), "value": "Records limitations, deviations, and field observations in real time. Notes what the files cannot show — glare, occlusion, route changes, fallback decisions."},
        ],
        "bottom_band": bold("Role assignment: Before the B2 powers on, every person in the arena must know their role and their stop authority. If anyone cannot state their role in one sentence, roles are not clear enough to proceed.")
    },
    # ── Slide 25: Readiness Is Observable ── (was Slide 26)
    {
        "title": "Readiness Is Observable",
        "thesis": "Students should not say they are ready because they feel ready. They should show readiness through checks: selected network interface, clear perimeter, known stop action, verified cameras, active logger, prepared folder, and named checkpoint plan. If one check is missing, the run waits.",
        "board_type": "list",
        "board_data": [
            bold("Interface selected: Correct network adapter active, IP on expected subnet, ping to B2 confirmed, DDS discovery working. Connectivity is the foundation — if the robot is not reachable, nothing else matters."),
            bold("Perimeter clear: Arena boundaries marked, obstacles identified, operator zones designated, bystanders aware. Physical space is as important as software readiness."),
            bold("Stop path known: Remote stop accessible, script stop command ready, physical stop procedure agreed. Every team member knows at least two ways to halt the robot immediately."),
            bold("Cameras tested: Front and rear still capture verified, RTSP stream confirmed playable, file save paths writable. Camera readiness is confirmed before motion, not assumed."),
            bold("Logger ready: SportModeState subscriber running, JSONL file writable, lines appearing and parseable. Telemetry logging begins before first motion and continues through final notes."),
        ],
        "bottom_band": bold("Readiness gate: Read each check aloud and confirm verbally. 'Interface — confirmed. Perimeter — clear. Stop path — known. Cameras — tested. Logger — running.' All five confirmed → motion may proceed. Any one missing → wait.")
    },
    # ── Slide 26: Capture at Stable Dwell ── (was Slide 27)
    {
        "title": "Capture at Stable Dwell",
        "thesis": "Checkpoint evidence is strongest when the robot is stable. Capturing during a turn or translation can create blur and make the report less defensible. Students should move into view, stop or dwell, capture the frame, label it with the checkpoint, and only then continue.",
        "board_type": "list",
        "board_data": [
            bold("Approach: Move the B2 into inspection view using bounded, supervised motion. Velocity should decrease as the robot nears the checkpoint — approach slow, not fast."),
            bold("StopMove or Dwell: Command the robot to stop and stabilize. Confirm velocity reads near zero in SportModeState. Wait at least 1–2 seconds after stop before capture — settling time matters."),
            bold("Capture Frame: Execute still capture only after confirming the robot is stationary. The image should be sharp, well-framed, and clearly show the inspection target."),
            bold("Label Checkpoint: Save as checkpoints/<id>/frame.jpg. State the checkpoint ID aloud. The evidence lead confirms the file is saved and opens correctly."),
            bold("Continue: Only after the evidence lead confirms usable capture does the director approve the next motion leg. Never rush from one capture directly into the next motion."),
        ],
        "bottom_band": bold("Stable dwell rule: 'Capture in motion is not inspection evidence — it is a screenshot of a moving robot.' If SportModeState velocity is non-zero, wait. Blurred evidence weakens every claim that follows.")
    },
    # ── Slide 27: RTSP Needs Proof ── (was Slide 28)
    {
        "title": "RTSP Needs Proof",
        "thesis": "RTSP recording may fail because the stream, writer settings, codec, or dimensions are wrong. A file name alone is not evidence. Students should check file size, open playback, confirm the scene, and document any fallback if video cannot be used.",
        "board_type": "list",
        "board_data": [
            bold("Record: Start RTSP stream capture with explicit writer configuration — codec, resolution, frame rate. Confirm the stream is active before declaring recording started."),
            bold("File Size: After recording stops, check the file size. A video file under 1 KB is almost certainly corrupt — the stream may have failed silently during recording."),
            bold("Playback: Open the video file and play at least the first and last few seconds. Confirm the content is the expected scene, not a black frame or frozen image."),
            bold("Scene Match: Does the video show the correct checkpoint, the correct robot position, the correct inspection target? If the scene does not match, the recording is mislabeled."),
            bold("Accept or Fallback: If video passes all checks → accept as evidence. If video fails → fall back to still frames, telemetry, and operator notes. State the fallback explicitly in the report."),
        ],
        "bottom_band": bold("RTSP verification: 'I recorded a video file. I checked the size. I played it back. The scene matches cp01. I accept it as evidence.' Or: 'Video failed — I am using still frames and telemetry instead. This limitation is documented in the report.'")
    },
    # ── Slide 28: Log Through the Run ── (was Slide 29)
    {
        "title": "Log Through the Run",
        "thesis": "Telemetry logging should cover the meaningful run window. Starting late can miss the approach, and stopping early can miss recovery or final posture. The evidence lead should confirm that SportModeState logging begins before motion and continues through checkpoint captures and final notes.",
        "board_type": "grid",
        "board_data": [
            {"label": bold("Before Motion"), "value": bold("Start SportModeState logging. Confirm lines are appearing in sportmodestate.jsonl. Log at least 5–10 seconds of stationary baseline data — this shows the robot's pre-run state.")},
            {"label": bold("During Motion & Capture"), "value": bold("Keep logging continuously through every motion leg, every checkpoint approach, every dwell, and every capture. No gaps — the log is the runtime witness of the entire inspection.")},
            {"label": bold("After Final Notes"), "value": bold("Continue logging for several seconds after the final capture and notes. This captures the robot's post-inspection state — mode, posture, position after all motion has stopped.")},
        ],
        "bottom_band": bold("Log coverage test: Open your sportmodestate.jsonl. Does the first timestamp precede the first motion command? Does the last timestamp follow the final capture? If not, your log has blind spots at the edges of the run.")
    },
    # ── Slide 29: Map Captures to Checkpoints ── (was Slide 30)
    {
        "title": "Map Captures to Checkpoints",
        "thesis": "Students should preserve raw captures and also normalize selected evidence into the expected checkpoint paths. This step turns field media into reviewable inspection evidence. A good habit is to state the checkpoint ID aloud, save the capture, and immediately confirm where the selected frame belongs.",
        "board_type": "grid",
        "board_data": [
            {"label": bold("Raw Captures"), "value": bold("All original files — every still, every video clip, unmodified and timestamped. Stored in raw_captures/ as the unprocessed field record. Never delete raw captures until the report is complete and accepted.")},
            {"label": bold("Selected Evidence"), "value": bold("The best frame for each checkpoint, copied to checkpoints/<id>/frame.jpg. Selected for clarity, focus, and relevance — not every raw capture becomes checkpoint evidence.")},
            {"label": "Naming Convention", "value": bold("checkpoints/cp01/frame.jpg, checkpoints/cp02/frame.jpg. Consistent naming lets the validator, the report, and any reviewer find the right evidence at the right checkpoint instantly.")},
        ],
        "bottom_band": bold("Mapping habit: After each capture, say aloud: 'Checkpoint cp01 — frame saved, verified, copied to checkpoints/cp01/frame.jpg.' This verbal confirmation catches mislabeled files before they become report errors.")
    },
    # ── Slide 30: Field Notes Capture Limits ── (was Slide 31)
    {
        "title": "Field Notes Capture Limits",
        "thesis": "Field notes explain what the files cannot show by themselves. If glare limited visibility, the rear stream failed, a checkpoint was skipped, or the route changed for safety, the report should include that limitation. Honest notes make the final inspection more credible, not weaker.",
        "board_type": "list",
        "board_data": [
            bold("Glare / Lighting: Note if direct sunlight, reflections, or low light affected camera image quality. A washed-out image at cp02 is not a failure — it is a limitation that the report must explain."),
            bold("Occlusion: Note if an object, person, or robot part blocked the inspection view. Partial occlusion may still allow useful evidence — state what is visible and what is hidden."),
            bold("Skipped Checkpoint: Note if a checkpoint was skipped and why — safety concern, time constraint, unreachable position. A skipped checkpoint with a documented reason is better than a missing checkpoint with no explanation."),
            bold("Fallback Stream: Note if RTSP video was replaced by still frames. State which channel was used as the fallback and why the primary channel was unavailable."),
            bold("Route / Safety Change: Note if the planned route changed during the run — obstacle discovered, perimeter adjusted, operator decision. The report must explain deviations from the plan."),
        ],
        "bottom_band": bold("Notes discipline: 'If I do not write this limitation down now, the report will claim evidence quality that the files cannot support.' Write the note at the checkpoint, not from memory during report writing.")
    },
    # ── Slide 31: Evidence Habit — Verify Immediately ── (was Slide 32)
    {
        "title": "Evidence Habit: Verify Immediately",
        "thesis": "The field evidence habit is immediate verification. After capture, students should open the artifact, label the checkpoint, place the selected file in the package, and confirm the log is still running. This avoids discovering after the run that the strongest checkpoint has no usable evidence.",
        "board_type": "list",
        "board_data": [
            bold("Capture: Execute the still or video capture at the checkpoint. State aloud what was captured and at which checkpoint."),
            bold("Open: Immediately open the saved file — view the image, play the video. Do not trust the file save confirmation alone. A file can save successfully and still be corrupt."),
            bold("Label: Name the file with its checkpoint ID. Confirm the label matches the actual scene content — a mislabeled cp01 frame showing cp02 content is a data integrity error."),
            bold("Place: Copy the verified frame to checkpoints/<id>/frame.jpg. Confirm the copy succeeded and the file at the destination path opens correctly."),
            bold("Confirm Log: Check that sportmodestate.jsonl is still receiving new lines. A frozen log means telemetry evidence stopped mid-run — diagnose before continuing."),
        ],
        "bottom_band": bold("Immediate verification loop: Capture → Open → Label → Place → Confirm Log → Continue. If any step fails, stay at the checkpoint until it is resolved or a fallback is documented. Never leave a checkpoint with unverified evidence.")
    },
    # ── Slide 32: Fallbacks Must Be Stated ── (was Slide 33)
    {
        "title": "Fallbacks Must Be Stated",
        "thesis": "A field run can still be useful when one channel fails. If RTSP video is unavailable, students can rely on verified stills, telemetry logs, and limitation notes. The key is to state the fallback clearly so the final report does not imply evidence that was never captured.",
        "board_type": "list",
        "board_data": [
            bold("Video Fails → Use Stills: If RTSP recording is corrupt or unavailable, fall back to front/rear still captures at each checkpoint. Stills at stable dwell are valid primary evidence."),
            bold("Camera Fails → Use Telemetry: If both video and stills are unavailable, SportModeState telemetry still documents that the robot reached the checkpoint position and stopped."),
            bold("All Sensors Fail → Use Notes: If no automated evidence is available, operator notes become the primary record. State clearly: 'Automated capture failed — all evidence is from operator observation.'"),
            bold("Report Caveat: Every fallback must produce a limitation statement in the report. 'RTSP video was unavailable at cp02 due to stream error — still frame and telemetry used instead.'"),
        ],
        "bottom_band": bold("Fallback rule: A field run with stated fallbacks is still valid engineering work. A field run with hidden failures is not. State every fallback — the report's credibility depends on honesty about limitations.")
    },
    # ── Slide 33: Section 4 — Logs, Reports, and Maintenance ── (was Slide 34)
    {
        "title": "Section 4 — Logs, Reports, and Maintenance",
        "thesis": "Parse the run, visualize evidence, report claims, and care for the B2. This section covers log parsing, motion visualization, payload data context, artifact-backed report claims, validation as a report-readiness check, message-to-fix debugging, and post-run B2 hardware maintenance.",
        "board_type": "grid",
        "board_data": [
            {"label": "Core Idea", "value": bold("Raw telemetry → Parsed fields → Visualization → Report claims → Validation → Maintenance. Data becomes evidence only when it is extracted, understood, and connected to a specific claim.")},
            {"label": "Key Principle", "value": bold("A report claim follows a fixed pattern: state the claim, name the artifact, cite telemetry context, explain any limitation, assign confidence. This prevents vague summaries of a live demo.")},
            {"label": "Maintenance", "value": bold("The inspection is not finished when the report is drafted. Close with a B2 maintenance walkthrough: power state, body, feet, payload mount, cables, sensors, and file archive.")},
            {"label": "Section Slides", "value": "Slides 34–40: Log parsing, motion visualization, payload context, report claims, validation, debugging, and B2 hardware maintenance."},
        ],
        "bottom_band": bold("Section rule: The final deliverable is not a live demo — it is a reviewable run folder and report. Another engineer should understand the inspection without having watched it.")
    },
    # ── Slide 34: Parse Logs into Fields ── (was Slide 35)
    {
        "title": "Parse Logs into Fields",
        "thesis": "Data visualization begins by parsing logs into useful fields. Students should extract timing, mode, velocity, yaw speed, position, and body height from SportModeState records. The goal is not advanced analytics; it is turning raw telemetry into a readable explanation of robot behavior.",
        "board_type": "grid",
        "board_data": [
            {"label": bold("Timestamp"), "value": "When each state sample was recorded. Used to align telemetry with camera captures and operator notes — timing is the backbone of multi-sensor correlation."},
            {"label": bold("Mode & Gait"), "value": "What control mode the robot was in and what gait pattern was active. Mode transitions during inspection may indicate script or operator interventions."},
            {"label": bold("Velocity & Yaw Speed"), "value": bold("Linear velocity (vx, vy) and angular velocity (vyaw). Plot these to show when the robot moved, turned, or stopped — motion timeline from data, not memory.")},
            {"label": bold("Position & Body Height"), "value": "Estimated position and body height. Track position drift over the run and note any unusual posture changes that may affect camera aim or stability."},
        ],
        "bottom_band": bold("Parsing exercise: From your sportmodestate.jsonl, extract timestamp, vx, and vyaw for the full run. Plot them on a simple timeline. Can you identify exactly when each motion leg started, when the robot stopped, and when each capture occurred?")
    },
    # ── Slide 35: Visualize Motion and Capture ── (was Slide 36)
    {
        "title": "Visualize Motion and Capture",
        "thesis": "A simple timeline can explain the field run clearly. Speed and yaw speed show when the robot moved or turned, while vertical markers show checkpoint captures. This helps students explain whether a frame was taken during stable dwell or during motion that might weaken image quality.",
        "board_type": "grid",
        "board_data": [
            {"label": bold("Speed Line"), "value": bold("Plot vx (forward speed) over time. Flat near-zero segments indicate dwell/stop periods. Spikes indicate motion legs. A capture during a spike is motion-blurred — the report must note this.")},
            {"label": bold("Yaw-Speed Line"), "value": bold("Plot vyaw (turn rate) over time. Non-zero segments indicate the robot was rotating. A capture during rotation may show motion blur or framing shift.")},
            {"label": bold("Capture Markers"), "value": bold("Vertical lines at checkpoint capture timestamps (cp01, cp02, cp03). Overlay on the speed plot to visually confirm: was the robot stationary at each capture moment?")},
        ],
        "bottom_band": bold("Visualization test: 'Show me the timeline of your field run. Point to cp01. Was vx near zero? Was vyaw near zero? Was the robot stable?' The timeline answers these questions in one image.")
    },
    # ── Slide 36: Payload Data Needs Context ── (was Slide 37)
    {
        "title": "Payload Data Needs Context",
        "thesis": "Payload data becomes useful only when it is tied to context. A measurement should include timestamp, checkpoint ID, sensor identity, and relevant robot state. Without that context, the number may be hard to interpret or defend in the report. Tables are the best beginner format.",
        "board_type": "table",
        "board_data": {
            "headers": ["Timestamp", "Checkpoint", "Sensor Value", "Robot State", "Interpretation"],
            "rows": [
                ["2026-06-04T09:15:23Z", "cp01", "Temperature: 24.3°C", bold("Mode: Damp, vx ≈ 0, body height normal"), "Normal reading at first checkpoint — robot stable, sensor functioning."],
                ["2026-06-04T09:18:47Z", "cp02", "Distance: 1.42 m", bold("Mode: Damp, slight pitch from slope"), "Measurement may be affected by 3° slope — noted in report limitation."],
                ["2026-06-04T09:22:10Z", "cp03", "No reading", bold("Mode: Damp, vx ≈ 0"), "Payload sensor did not respond — fallback to visual inspection only. Limitation documented."],
            ]
        },
        "bottom_band": bold("Payload context rule: 'A number without timestamp, checkpoint, and robot state is not a measurement — it is a mystery.' Always pair payload readings with the telemetry context that explains the conditions under which they were taken.")
    },
    # ── Slide 37: Reports Make Defensible Claims ── (was Slide 38)
    {
        "title": "Reports Make Defensible Claims",
        "thesis": "A report should make claims that the evidence can support. Students can use a fixed pattern: state the claim, name the artifact, cite the telemetry context, explain any limitation, and assign a confidence statement. This prevents reports from becoming vague summaries of a live demo.",
        "board_type": "list",
        "board_data": [
            bold("Claim: What are you asserting about the inspection? Be specific — 'The B2 successfully inspected checkpoint cp01 and captured clear visual evidence' — not 'The robot worked.'"),
            bold("Artifact: Which file supports this claim? Name the exact file path — checkpoints/cp01/frame.jpg, sportmodestate.jsonl lines 130–145, field_report.md section 2."),
            bold("Telemetry Context: What does the robot state data say about the moment of capture? Velocity near zero, mode stable, body height normal — or deviations that need explanation."),
            bold("Limitation: What could weaken this claim? Glare on the image, slight motion during capture, sensor gap, timing uncertainty. Honest limitations strengthen credibility."),
            bold("Confidence: How sure are you? High (multiple sensors agree), Medium (primary sensor ok, no cross-validation), Low (fallback used, uncertainty present). Confidence must match evidence strength."),
        ],
        "bottom_band": bold("Report pattern practice: Write one claim about your last mock run using all five fields. Can another student read it and understand exactly what you observed, what supports it, and how confident you are?")
    },
    # ── Slide 38: Validation Protects the Report ── (was Slide 39)
    {
        "title": "Validation Protects the Report",
        "thesis": "The validator checks whether required files and paths are present. A pass means the package is structurally reviewable, but warnings may still need explanation in the report. A fail means the team should repair the folder before making final inspection claims.",
        "board_type": "grid",
        "board_data": [
            {"label": bold("PASS"), "value": bold("All required structural checks satisfied — metadata present, checkpoint folders populated, telemetry log non-empty, images valid. The package can be reviewed and reported on.")},
            {"label": bold("PASS with Warnings"), "value": bold("Structure valid but one or more quality warnings — image below recommended size, JSONL line count low, optional field empty. Warnings go in the report with explanation.")},
            {"label": bold("FAIL"), "value": bold("Required artifact missing, path incorrect, or structural rule violated. The package is not reviewable. Repair the folder and re-validate — do not write the report against incomplete evidence.")},
        ],
        "bottom_band": bold("Validation as report gate: 'PASS → Write the report. Warnings → Write the report AND explain each warning. FAIL → Repair the folder, do not write the report yet.' The validator protects the report from building on incomplete evidence.")
    },
    # ── Slide 39: Debug from Message to Fix ── (was Slide 40)
    {
        "title": "Debug from Message to Fix",
        "thesis": "Students should interpret error messages as clues. Missing metadata means accountability is incomplete. Empty logs mean runtime evidence was not saved. Bad frames suggest corrupt or placeholder images. Mismatched checkpoints mean the plan and package disagree. Each problem has a specific repair path.",
        "board_type": "table",
        "board_data": {
            "headers": ["Validator Message", "Likely Cause", "First Fix", "Report Impact"],
            "rows": [
                ["Missing metadata.json", "Script did not create or write the metadata file.", "Check setup step — add metadata write with operator, date, robot ID, scenario.", "Report cannot establish accountability — who, when, what scenario."],
                [bold("Empty sportmodestate.jsonl"), "Logger started but no state samples were written — subscriber may not have received data.", "Check SportModeState subscription — confirm callback fires, file handle is open, DDS discovery works.", "No telemetry context for any claim — captures lack motion/posture support."],
                [bold("Bad frame.jpg at cp01"), "Image file is corrupt, zero bytes, or wrong format.", "Re-capture the still — verify with file size check and visual open before proceeding.", "Primary visual evidence for cp01 is unusable — fallback or recapture required."],
                [bold("Mismatched checkpoint IDs"), "patrol_plan.json lists cp_A but folder has cp01 — naming convention broken.", "Standardize all checkpoint IDs — use consistent format (cp01, cp02, cp03) everywhere.", "Validator cannot match plan to evidence — report claims may reference wrong checkpoints."],
            ]
        },
        "bottom_band": bold("Debugging discipline: Read the validator message aloud. State the likely cause. Make one fix. Re-validate. If the message changes, you fixed something — if the same message persists, your fix did not address the root cause.")
    },
    # ── Slide 40: Maintain the B2 Afterward ── (was Slide 41)
    {
        "title": "Maintain the B2 Afterward",
        "thesis": "The inspection is not finished when the report is drafted. Students should close with a B2 maintenance walkthrough: safe power state, visible body condition, feet, payload mounting, cables, sensor surfaces, and archived files. Hardware care protects the next team and completes professional field discipline.",
        "board_type": "list",
        "board_data": [
            bold("Power State: Confirm the B2 is in a safe power mode — Damp or powered down per instructor guidance. Battery level noted. No active motion commands lingering."),
            bold("Body & Feet: Inspect for visible damage, debris, or unusual wear. Check foot pads for embedded gravel or sharp objects. Clean if needed — debris from one run affects the next."),
            bold("Payload Mount & Cables: Verify payload is secure, connectors are seated, cables are not pinched or frayed. A loose payload can shift during the next run and change sensor aim."),
            bold("Sensor Surfaces: Clean camera lenses and sensor windows with appropriate materials. Dust, fingerprints, or moisture from the field run can degrade the next inspection's image quality."),
            bold("File Archive: Confirm all run artifacts are saved, backed up, and organized. The run folder should be complete and accessible for report writing and instructor review."),
        ],
        "bottom_band": bold("Maintenance discipline: 'The next team should find the B2 in the same condition I would want to receive it.' Walk through all five checks, document any issues found, and confirm the archive before leaving.")
    },
    # ── Slide 41: Closing — Required Outcomes Check ── (was Slide 42)
    {
        "title": "Closing — Required Outcomes Check",
        "thesis": "Confirm that every Day 4 activity served the four required outcomes. This closing section returns to the core framework and gives instructors a concise final standard for Day 4 success.",
        "board_type": "grid",
        "board_data": [
            {"label": bold("Rugged Navigation & Sensors"), "value": "Students can explain how terrain conditions affect evidence quality and what each sensor channel contributes to an inspection claim."},
            {"label": bold("Mock Inspection Scripts"), "value": "Students can build procedural scripts that rehearse capture, logging, motion, packaging, and validation — and pass the mock gate before hardware."},
            {"label": bold("B2 Field Capture"), "value": "Students can execute a supervised B2 field run with defined roles, stable-dwell capture, continuous telemetry logging, and immediate evidence verification."},
            {"label": bold("Logs, Reports, Maintenance"), "value": "Students can parse telemetry, visualize motion, write artifact-backed claims, debug from validator messages, and complete B2 hardware maintenance."},
        ],
        "bottom_band": bold("Outcome check: For each of the four tiles above, can you produce one concrete artifact that proves you achieved that outcome? If not, that outcome is incomplete — return to the relevant section before closing Day 4.")
    },
    # ── Slide 42: Four Outcomes Are Complete ── (was Slide 43)
    {
        "title": "Four Outcomes Are Complete",
        "thesis": "Students have learned how rugged terrain changes navigation evidence, how mock scripts rehearse inspection procedure, how B2 field execution captures sensors and telemetry, and how parsed logs, payload context, reports, and maintenance complete the workflow.",
        "board_type": "grid",
        "board_data": [
            {"label": bold("Terrain and Sensors"), "value": bold("Rugged terrain changes the run — slope, gravel, glare, vibration. Multi-sensor arrays answer different questions. SportModeState provides runtime context. Evidence: terrain notes + sensor table + telemetry log.")},
            {"label": bold("Mock Scripts"), "value": bold("Mock-first workflow, Gazebo rehearsal, procedural scripts, scenario files, camera capture, JSONL logging, bounded motion, channel debugging, and validation gate. Evidence: validated mock run folder.")},
            {"label": bold("B2 Field Capture"), "value": bold("Field roles, observable readiness, stable-dwell capture, RTSP verification, continuous logging, checkpoint mapping, field notes, immediate verification, and stated fallbacks. Evidence: field run folder + notes.")},
            {"label": bold("Logs, Reports, Maintenance"), "value": bold("Parse SportModeState fields, visualize motion timeline, contextualize payload data, write artifact-backed claims, validate, debug, and maintain the B2. Evidence: field_report.md + validator output.")},
        ],
        "bottom_band": bold("Completion check: 'I can explain rugged terrain effects. I built and validated a mock script. I executed a supervised B2 field run. I parsed data and wrote a report. I maintained the B2 afterward.' All five statements true → Day 4 objectives met.")
    },
    # ── Slide 43: Ready Means Reviewable ── (was Slide 44)
    {
        "title": "Ready Means Reviewable",
        "thesis": "The final standard is reviewability. Another engineer should open the run folder and understand the scenario, route, captures, telemetry, payload context, validation result, limitations, report claims, and maintenance notes. If the story depends mainly on memory, the Day 4 evidence workflow is incomplete.",
        "board_type": "list",
        "board_data": [
            bold("Scenario: Can the reviewer understand what was being inspected, where, and why? metadata.json and patrol_plan.json should tell the complete story without verbal explanation."),
            bold("Route: Can the reviewer see the planned checkpoints and the path between them? The route should be documented clearly enough to reconstruct the field layout."),
            bold("Captures: Can the reviewer open each checkpoint frame and see what the robot saw? Every frame.jpg should be verified, correctly exposed, and clearly show the inspection target."),
            bold("Telemetry: Can the reviewer read the SportModeState log and understand robot motion and posture? Velocity, mode, and body height should explain the robot's state at each capture."),
            bold("Payload: Are sensor readings paired with timestamps, checkpoints, and robot state? Raw numbers without context are not evidence."),
            bold("Validation: Does the validator output show PASS or documented warnings? The reviewer should know whether the package is structurally complete."),
            bold("Report: Does field_report.md make claims supported by named artifacts, telemetry, and stated limitations? The report is the synthesis — it should reference every other file in the folder."),
            bold("Maintenance: Is the B2 condition documented after the run? The reviewer should know the hardware was cared for and the files were archived."),
        ],
        "bottom_band": bold("Reviewability test: Hand your run folder to a classmate who did not watch your field run. Can they answer: what was inspected, what evidence was captured, what the robot state was, what limitations exist, and what the report claims? If any answer is no, your Day 4 workflow is not yet complete.")
    },
]

# ── Write the slides block ──
slides_py = '    "slides": [\n'
for i, s in enumerate(SLIDES):
    slides_py += "        {\n"
    slides_py += f'            "title": {_json.dumps(s["title"], ensure_ascii=False)},\n'
    slides_py += f'            "thesis": {_json.dumps(s["thesis"], ensure_ascii=False)},\n'
    slides_py += f'            "board_type": {_json.dumps(s["board_type"], ensure_ascii=False)},\n'
    slides_py += f'            "board_data": {_json.dumps(s["board_data"], ensure_ascii=False, indent=12).replace(chr(10), chr(10) + "            ")},\n'
    slides_py += f'            "bottom_band": {_json.dumps(s["bottom_band"], ensure_ascii=False)}\n'
    slides_py += "        }"
    if i < len(SLIDES) - 1:
        slides_py += ","
    slides_py += "\n"
slides_py += "    ],"

print(f"Generated {len(SLIDES)} slides block ({len(slides_py)} chars)")
print("Slides:")
for i, s in enumerate(SLIDES):
    print(f"  {i+1:2d}. [{s['board_type']:5s}] {s['title'][:90]}")

# ── Replace DAY04 slides in build_syllabus.py ──
build_path = "build_syllabus.py"
with open(build_path) as f:
    content = f.read()

# Find DAY04 slides array
day04_slides_start = content.index('    "slides": [', content.index('DAY04'))
day04_labs_start = content.index('    "labs": [', day04_slides_start)

new_content = content[:day04_slides_start] + slides_py + content[day04_labs_start:]

with open(build_path, "w") as f:
    f.write(new_content)

print(f"\nReplaced DAY04 slides array in {build_path}")
print(f"Old slides block: {day04_labs_start - day04_slides_start} chars")
print(f"New slides block: {len(slides_py)} chars")

# ── Update DAY04 header metadata ──
# Replace title
old_title = '"B2 Advanced Scenarios & Field Inspection"'
new_title = '"B2 Rugged Inspection, Mock Scripts, Field Capture, Telemetry, Reporting, and Maintenance"'
content = content.replace(old_title, new_title)

# Replace eyebrow
old_eyebrow = '"B2 FIELD INSPECTION"'
new_eyebrow = '"B2 RUGGED INSPECTION"'
content = content.replace(old_eyebrow, new_eyebrow)

# Replace thesis
old_thesis = '"A field inspection is not successful merely because the robot moved. It is successful when the team can explain what scenario was attempted, what data were captured, what state the robot reported, which checkpoints were inspected, how artifacts were organized, and whether the run folder can be validated."'
new_thesis = '"Day 4 converts the B2 from a robot that can be safely observed and commanded into an inspection evidence system. Every activity connects to one of four required outcomes: rugged navigation and multi-sensor reasoning, mock inspection scripts, supervised B2 field execution, or data visualization with reporting and maintenance."'
content = content.replace(old_thesis, new_thesis)

# Replace rules
old_rules_start = content.index('    "rules": [', content.index('DAY04'))
old_rules_end = content.index('    ],', old_rules_start) + len('    ],')
new_rules = '''    "rules": [
        "Plan before motion: create metadata.json and patrol_plan.json before the robot moves — the run folder is the inspection contract.",
        "Every inspection claim must be supported by a named file, a timestamp, a checkpoint ID, and a context note — not just a verbal statement.",
        "Dwell before capture: images must be captured during stable dwell or stopped state. SportModeState velocity must read near zero before any frame is saved.",
        "Preserve raw captures and separate selected evidence: raw files are the unmodified record; checkpoint folders hold the selected, verified frames.",
        "Verify immediately: open every captured file at the checkpoint before continuing. A corrupt or misaimed frame discovered during reporting is too late to fix.",
        "State every fallback: if a sensor channel fails, document which channel was used instead. Hidden failures undermine the report.",
        "Validate before reporting: the validator is a report-readiness gate. PASS → write. Warnings → write and explain. FAIL → repair before writing.",
        "Care for the B2 afterward: power, body, feet, payload, cables, sensors, and archive must be checked before leaving the field."
    ]'''
content = content[:old_rules_start] + new_rules + content[old_rules_end:]

# Replace pacing
old_pacing_start = content.index('    "pacing": [', content.index('DAY04'))
old_pacing_end = content.index('    ],', old_pacing_start) + len('    ],')
new_pacing = '''    "pacing": [
        {"time": "09:00 - 09:15", "session": "Day 4 Framing — Four Jobs, One Flow, Evidence Standard", "path": "day-04/README.md"},
        {"time": "09:15 - 09:45", "session": "Rugged Navigation and Multi-Sensor Arrays", "path": "day-04/README.md#navigation"},
        {"time": "09:45 - 10:15", "session": "Costmaps, Obstacle Supervision, Sensor Roles, and Telemetry", "path": "day-04/README.md#sensors"},
        {"time": "10:15 - 10:45", "session": "Mock Inspection Scripts — Scenario Files, Cameras, JSONL Logging", "path": "day-04/lab-00/"},
        {"time": "10:45 - 11:15", "session": "Mock Scripts — Motion, Debugging, and Validation Gate", "path": "day-04/lab-01/"},
        {"time": "11:15 - 12:00", "session": "B2 Field Execution — Roles, Readiness, Capture, Telemetry, Fallbacks", "path": "day-04/lab-02/"},
        {"time": "12:00 - 12:30", "session": "Logs, Reports, Maintenance, and Day 4 Closing", "path": "day-04/README.md#reporting"}
    ]'''
content = content[:old_pacing_start] + new_pacing + content[old_pacing_end:]

with open(build_path, "w") as f:
    f.write(content)

print("Updated DAY04 header metadata (title, eyebrow, thesis, rules, pacing)")
print("Done. Run build_syllabus_final.py to regenerate syllabus.json.")