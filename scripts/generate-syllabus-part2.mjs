import { readFileSync, writeFileSync } from 'fs';

const existing = JSON.parse(readFileSync('client/src/data/syllabus.json', 'utf8'));

// ===== DAY 04: B2 Advanced Scenarios & Field Inspection =====
const day04 = {
  day: "04",
  title: "B2 Advanced Scenarios & Field Inspection",
  eyebrow: "B2 INSPECTION EVIDENCE SYSTEM",
  thesis: "A B2 field inspection is not successful merely because the robot moved — it is successful when the team can explain the scenario, data captured, robot state, checkpoints inspected, and whether the run folder validates after power-down.",
  rules: [
    "Create the run folder and draft metadata BEFORE any robot motion — the inspection package is the contract.",
    "Capture checkpoint stills during stable dwell or stopped state, NOT during turning or translation.",
    "Preserve raw artifacts (video, JSONL, images) until the debrief is complete — a failed capture can still be diagnostic evidence."
  ],
  pacing: [
    { time: "00:00 – 00:15", session: "Day 4 Framing — B2 as Evidence Pipeline", path: "course/day-04/" },
    { time: "00:15 – 00:35", session: "B2 Inspection Hardware — Cameras, LiDAR, Safety", path: "course/day-04/" },
    { time: "00:35 – 00:55", session: "Run-Folder Schema — Contract Adaptation for B2", path: "course/day-04/lab-00/" },
    { time: "00:55 – 01:20", session: "Lab 1 — Mock Inspection Video (Front/Back Cameras)", path: "course/day-04/lab-01/" },
    { time: "01:20 – 01:30", session: "Break & Readiness Reset", path: "course/day-04/" },
    { time: "01:30 – 01:55", session: "Lab 2 — SportModeState as Runtime Audit Trail", path: "course/day-04/lab-02/" },
    { time: "01:55 – 02:20", session: "Supervised Motion Between Inspection Legs", path: "course/day-04/lab-02/" },
    { time: "02:20 – 03:00", session: "Field Run, Packaging, Validation & Debrief", path: "course/day-04/lab-02/" }
  ],
  slides: [
    {
      title: "Day 4 Purpose & Teaching Stance",
      thesis: "Day 4 converts the B2 from a robot that can be safely observed and commanded into an inspection evidence system.",
      board_type: "table",
      board_data: {
        headers: ["Teaching Priority", "What Students Learn", "Evidence of Understanding"],
        rows: [
          ["Inspection Framing", "A field run must produce traceable evidence, not just motion", "Students describe the run folder before touching the robot"],
          ["Video Capture", "Front/back cameras and RTSP streams are inspection assets", "Students save stills and recordings with meaningful names"],
          ["State Logging", "SportModeState is the runtime witness of motion and posture", "Students explain mode, gait, position, velocity, and body-height"],
          ["Supervised Mobility", "SportClient motion must remain bounded and supervised", "Students choose StopMove, Damp, StandDown, or RecoveryStand appropriately"],
          ["Reporting", "Validation and debrief convert raw files into engineering evidence", "Students submit coherent run package and explain warnings or failures"]
        ]
      },
      bottom_band: "The most important Day 4 concept: Inspection Run = Scenario + Safety + Video + State + Motion Notes + Checkpoint Package + Validation + Debrief."
    },
    {
      title: "From Day 3 Fundamentals to Day 4 Practice",
      thesis: "A field engineer says: 'At checkpoint C2, front camera frame.jpg was captured; the state log shows robot stationary during dwell; the video covers the approach; validation passed with one documented warning.'",
      board_type: "table",
      board_data: {
        headers: ["Day 3 Capability", "Day 4 Extension", "Instructor Emphasis"],
        rows: [
          ["Observe SportModeState", "Save state evidence into a run package", "Observability becomes auditability"],
          ["Use high-level SportClient", "Move between inspection legs under supervision", "Commanding remains bounded and reversible"],
          ["Confirm DDS/network readiness", "Combine camera, RTSP, and state channels", "A field run uses multiple data paths"],
          ["Explain B2 safety", "Apply safety to 60 kg robot near people/assets", "Safe field inspection is procedural, not improvised"]
        ]
      },
      bottom_band: "Never confuse 'the script ran without errors' with 'the inspection package is auditable' — validation output, not terminal silence, is the standard."
    },
    {
      title: "B2 Inspection Hardware Context",
      thesis: "Front/rear depth and optical cameras, wide-angle LiDAR, 60 kg mass, and 4–6 hour operating time shape the Day 4 safety and data strategy.",
      board_type: "grid",
      board_data: [
        { label: "Front Optical/Depth Perception", value: "Capture approach view, target asset, and obstacle context — use front stills for primary checkpoint evidence." },
        { label: "Rear Optical/Depth Perception", value: "Capture retreat view, rear-side hazards, or alternate evidence — use when turning is unsafe or unnecessary." },
        { label: "LiDAR Context", value: "Supports spatial awareness and terrain interpretation — discuss broadly even if lab focuses on video." },
        { label: "60 kg Class Body", value: "Motion risk is non-trivial — enforce wide exclusion zones and human stop authority at all times." },
        { label: "4–6 h Operating Time", value: "Long enough for field practice but not a reason to skip readiness — check battery and thermal conditions before repeated runs." }
      ],
      bottom_band: "Never hot-swap aviation plug interfaces — if a cable, camera, or payload needs attention, stop the exercise, place robot in safe state, and follow local hardware procedure."
    },
    {
      title: "Day 4 Inspection Evidence Pipeline",
      thesis: "A pipeline view prevents students from seeing labs as disconnected tasks — it begins with a scenario and ends with a reportable package.",
      board_type: "grid",
      board_data: [
        { label: "Scenario", value: "Defines what is being inspected and why — checkpoint IDs, inspection target descriptions." },
        { label: "Readiness", value: "Confirms robot, space, network, and operator state — metadata fields, readiness checklist." },
        { label: "Video Capture", value: "Records what robot saw at checkpoints and during travel — front/back stills and RTSP recordings." },
        { label: "State Logging", value: "Records robot motion/posture context — sportmodestate.jsonl with mode, gait, position, velocity, body height." },
        { label: "Motion Between Legs", value: "Moves B2 between inspection areas under supervision — SportClient command notes and plan leg records." },
        { label: "Checkpoint Packaging", value: "Associates images and state slices with checkpoint IDs — checkpoints/<id>/frame.jpg." },
        { label: "Validation", value: "Checks that package is structurally complete — PASS, PASS-with-warning, or FAIL output." },
        { label: "Debrief", value: "Converts files into technical conclusions — short field_report.md or oral debrief with cited file names." }
      ],
      bottom_band: "When a student asks 'Which script should I run?', answer with a pipeline question: 'Which evidence stage are you trying to complete?' This builds engineering judgment."
    },
    {
      title: "Lab 0: Run Folder as the Inspection Evidence Contract",
      thesis: "The Day 2 run-folder schema is reused as a platform-independent evidence contract for B2 inspection packages.",
      board_type: "table",
      board_data: {
        headers: ["Required Item", "Why It Exists", "B2-Specific Adaptation"],
        rows: [
          ["metadata.json", "Describes who ran the inspection, when, under what conditions", "Add robot_platform: B2, robot_id, interface, camera_mode, operator notes"],
          ["patrol_plan.json", "Declares checkpoint IDs and movement legs", "Use conservative B2 legs; document manual movement between checkpoints"],
          ["sportmodestate.jsonl", "Time-series state witness", "Log mode, gait, position, velocity, yaw speed, and body height"],
          ["checkpoints/", "Organizes evidence by inspection point", "Place front/rear stills as frame.jpg; add optional state_slice.jsonl"],
          ["Validator Output", "Confirms structural usability", "Explain warnings instead of hiding them"]
        ]
      },
      bottom_band: "The validator is a teaching instrument — it forces students to separate structural completeness from subjective success. Show PASS and FAIL examples."
    },
    {
      title: "Lab 1: Mock Inspection Video with B2 Cameras",
      thesis: "Front and back camera stills provide checkpoint evidence; RTSP recordings provide continuous video context — different artifacts for different purposes.",
      board_type: "table",
      board_data: {
        headers: ["Key", "Action", "Artifact Produced", "Teaching Note"],
        rows: [
          ["Q / q", "Save front camera image", "front_img_<timestamp>.jpg", "Primary checkpoint evidence"],
          ["E / e", "Save back camera image", "back_img_<timestamp>.jpg", "Reverse-view or context evidence"],
          ["A / a", "Start/stop front RTSP recording", "front_video_<timestamp>.mp4", "Confirm stream opens before claiming evidence"],
          ["D / d", "Start/stop back RTSP recording", "back_video_<timestamp>.mp4", "Retreat or rear-side context"],
          ["ESC", "Exit and release resources", "Clean release", "Always exit deliberately; never kill windows blindly"]
        ]
      },
      bottom_band: "G1 cameras: 1280×720 resolution, 15 Hz video, 100° HFOV, 56° VFOV — wide FOV helps context but does NOT guarantee text labels or small defects are readable."
    },
    {
      title: "JPEG Samples, RTSP Streams & OpenCV Under the Hood",
      thesis: "Students should understand the data path to troubleshoot failures: SDK client → byte array → NumPy buffer → cv2.imdecode → BGR frame.",
      board_type: "table",
      board_data: {
        headers: ["Layer", "What Happens", "Typical Failure", "Debugging Habit"],
        rows: [
          ["DDS/Channel Init", "ChannelFactoryInitialize binds to robot network", "Wrong interface or disconnected cable", "Confirm interface name and reachability before camera"],
          ["SDK Image Sample", "Front/back clients call GetImageSample", "Return code nonzero or no frame", "Test one camera at a time; watch terminal output"],
          ["JPEG Decoding", "Bytes become OpenCV frame", "Frame is None or corrupt", "Confirm sample data exists before saving"],
          ["RTSP Capture", "VideoCapture opens stream URL", "Stream cannot open", "Confirm robot IP, port, network path, firewall"],
          ["Video Writing", "VideoWriter saves MP4", "Writer cannot open or output empty", "Confirm codec, dimensions, frame rate"]
        ]
      },
      bottom_band: "Demonstrate one controlled failure — e.g., an unopened RTSP stream produces a clear error. Students should never assume a file exists just because a script was started."
    },
    {
      title: "SportModeState as the Field-Run Audit Trail",
      thesis: "A video shows what the camera saw; a state log shows what the robot estimated — together they answer whether the robot was moving, stationary, or dwelling during capture.",
      board_type: "table",
      board_data: {
        headers: ["Field", "Meaning", "Inspection Use"],
        rows: [
          ["mode", "Current high-level robot mode", "Confirms whether robot was standing, moving, or in another state"],
          ["gait_type", "Locomotion pattern or gait category", "Helps interpret motion behavior during approach or retreat"],
          ["position", "Estimated position vector", "Supports checkpoint sequencing and relative movement discussion"],
          ["velocity", "Estimated translational velocity", "Helps prove dwell versus motion during image capture"],
          ["yaw_speed", "Rotational speed", "Helps explain blur, turning, or unstable target framing"],
          ["body_height", "Body height state", "Helps explain camera perspective and clearance decisions"],
          ["foot_force", "Foot contact-related force", "Supports terrain/contact discussion in advanced analysis"]
        ]
      },
      bottom_band: "A minimal JSONL entry: {\"t_utc\":\"...\",\"mode\":1,\"gait_type\":1,\"position\":[0,0,0],\"velocity\":[0,0,0],\"yaw_speed\":0,\"body_height\":0.41,\"checkpoint\":\"cp01\"}"
    },
    {
      title: "Supervised Motion Between Inspection Legs",
      thesis: "Each command must be tied to an inspection-leg intention and a recovery plan — menu experimentation is forbidden on B2.",
      board_type: "table",
      board_data: {
        headers: ["Command", "Day 4 Meaning", "Safe-Use Guidance"],
        rows: [
          ["Damp", "Emergency-priority damping stop", "Only when safety situation requires immediate damping — brief beforehand"],
          ["StopMove", "Stop current high-level motion", "Preferred first stop for normal supervised trials"],
          ["StandUp / StandDown", "Stand high or lie down", "Only after space and posture verified"],
          ["RecoveryStand", "Recover to standing from nonstandard posture", "Under instructor supervision after checking surroundings"],
          ["Move", "Body-frame velocity command", "Keep speeds very low; define short duration; always follow with StopMove"],
          ["MoveToPos / TrajectoryFollow", "Position-style or path following", "Advanced and bounded; verify target area; discuss conceptually first"]
        ]
      },
      bottom_band: "Before every motion: 'We will issue a short forward Move at low speed for two seconds, then StopMove, then dwell and capture the front image.' State intent, then act."
    },
    {
      title: "Field Inspection Choreography",
      thesis: "A Day 4 field run should be choreographed like a small production — operator, safety observer, evidence lead, and instructor each have defined roles.",
      board_type: "list",
      board_data: [
        "Create the run folder and draft metadata BEFORE the robot moves — folder name, checkpoint list, metadata draft.",
        "Start the runtime witness — non-empty sportmodestate.jsonl or captured state records streaming before motion.",
        "Start video recording only when stream is confirmed — verify file path and visible frame before proceeding.",
        "Place robot at checkpoint 1, dwell, capture still image — stable dwell or stopped state, not during translation.",
        "Execute ONE short supervised motion leg — command note and observer confirmation.",
        "Stop before inspection — StopMove or stable dwell state confirmed before next capture.",
        "Package immediately — copy selected image to checkpoints/<id>/frame.jpg.",
        "Validate before debrief — run validator and explain any warnings; validate immediately after packaging."
      ],
      bottom_band: "Role separation: operator manages commands, safety observer watches robot/environment, evidence lead tracks filenames, instructor controls pace. No single person does everything."
    },
    {
      title: "Reporting: From Artifacts to Engineering Claims",
      thesis: "A field report links claims to evidence with exact file names — vague language ('robot worked well') is not acceptable.",
      board_type: "table",
      board_data: {
        headers: ["Weak Claim", "Stronger Day 4 Claim"],
        rows: [
          ["\"The robot inspected the target\"", "\"At cp02_asset_label, front camera frame shows the target label; state slice indicates robot was stationary during capture\""],
          ["\"The video recorded\"", "\"Front RTSP recording front_video_20260603_103251.mp4 covers the approach from cp01 to cp02 and was verified playable after the run\""],
          ["\"The robot moved safely\"", "\"Robot executed one low-speed forward leg; StopMove issued before capture; no person entered the exclusion zone\""],
          ["\"Validation passed\"", "\"Run folder passed structural validation; the only warning was a missing optional rear-camera frame explained in notes\""]
        ]
      },
      bottom_band: "A strong field_report.md: scenario, team roles, safety setup, command sequence, evidence table with file names, validation result, issues, and next improvement."
    },
    {
      title: "Validator Interpretation & Common Day 4 Failures",
      thesis: "The validator forces students to separate structural completeness from subjective success — PASS is necessary but not sufficient.",
      board_type: "table",
      board_data: {
        headers: ["Message Pattern", "Likely Cause", "Instructor Response"],
        rows: [
          ["missing file: metadata.json", "Students captured data before creating run package", "Reconstruct metadata; explain what may be uncertain"],
          ["metadata: missing 'operator'", "Metadata is incomplete", "Inspection evidence needs accountability"],
          ["patrol_plan: missing 'checkpoints'", "Plan lacks explicit checkpoint structure", "Define checkpoint IDs before moving again"],
          ["sportmodestate.jsonl: need ≥1 JSON line", "State logging was not saved or is empty", "Can the run be defended without runtime state evidence?"],
          ["checkpoints/<id>/frame.jpg missing", "Raw images not mapped into checkpoint folders", "Copy or rename selected still image"],
          ["metadata checkpoints list differs", "Metadata and plan disagree", "Configuration management lesson"]
        ]
      },
      bottom_band: "Show one PASS and one FAIL example during the lecture — students learn faster when they see validation as immediate feedback rather than an end-of-day penalty."
    },
    {
      title: "Troubleshooting Guide for Day 4 Instructors",
      thesis: "Day 4 combines network, GUI, OpenCV, robot state, and motion — failures should be expected and handled methodically.",
      board_type: "table",
      board_data: {
        headers: ["Symptom", "Probable Source", "First Diagnostic Step", "Safe Fallback"],
        rows: [
          ["Camera window does not appear", "No GUI, wrong interface, SDK not receiving frames", "Confirm interface; run minimal camera test", "Use saved sample frames for reporting exercise"],
          ["Front saves but rear does not", "Rear client or stream issue", "Test rear capture independently; verify return code", "Mark rear camera unavailable in metadata"],
          ["RTSP file is empty", "Stream did not open or writer failed", "Check terminal message, file size, playback", "Use still images + state log for checkpoint"],
          ["State subscriber prints nothing", "Wrong DDS interface or topic unavailable", "Confirm robot network and rt/sportmodestate subscription", "Use instructor-provided state log for schema"],
          ["Robot moves but checkpoint blurred", "Captured during motion or yaw turn", "Check velocity/yaw speed near capture time", "Repeat capture during dwell after StopMove"],
          ["Validator fails after good field work", "Artifacts not normalized into required paths", "Compare folder tree against schema", "Repackage raw captures into checkpoint folders"]
        ]
      },
      bottom_band: "The most important habit: preserve raw artifacts. Do not delete imperfect video, state logs, or images until the debrief is complete. A failed capture can still be diagnostic."
    },
    {
      title: "Knowledge Checks — Day 4",
      thesis: "Students who can run scripts but cannot explain why each artifact exists are not ready for field-style robotics.",
      board_type: "list",
      board_data: [
        "Why does Day 4 reuse the Day 2 run-folder schema? — The schema provides a platform-independent evidence contract for metadata, plan, state logs, and checkpoint artifacts.",
        "Why is video alone insufficient for an inspection report? — Video lacks structured metadata, checkpoint mapping, and runtime state context unless packaged with other artifacts.",
        "What is the difference between a raw capture and checkpoint evidence? — Raw capture is the original file; checkpoint evidence is selected, named, and placed under checkpoints/<id>/frame.jpg with context.",
        "When should students capture a checkpoint still? — During a stable dwell or stopped state, not during turning or translation.",
        "What does sportmodestate.jsonl contribute? — Time-series robot state evidence: mode, gait, position, velocity, yaw speed, and body height.",
        "What should happen if RTSP recording fails? — Document the failure, preserve terminal output, use still images/state logs as fallback, and explain the limitation.",
        "Why should optional OpenCV effects not replace raw frames? — Processed images are derived artifacts; raw frames preserve primary evidence integrity."
      ],
      bottom_band: "Day 4 is successful when the team can hand its run folder to another engineer and they can understand the scenario, evidence, state, safety context, and limitations without watching the live run."
    },
    {
      title: "Closing: Evidence-First Robotics",
      thesis: "Whether the robot is a quadruped, humanoid, arm, or sensor platform, students should plan what evidence they need before running the system.",
      board_type: "grid",
      board_data: [
        { label: "Scenario", value: "What are we inspecting, and where are the checkpoints? — define before any scripts run." },
        { label: "Safety", value: "Who can stop the robot, and what is the exclusion zone? — assign roles before power-on." },
        { label: "Evidence Chain", value: "Which camera and file prove visual context? What did SportModeState report during capture? Which command moved the robot?" },
        { label: "Validation", value: "Did the folder pass, fail, or pass with warnings? What claim can we defend with the artifacts?" }
      ],
      bottom_band: "The most transferable Day 4 habit: a detection result is useful only if the original frame, timestamp, checkpoint ID, robot state, and scenario are preserved together."
    }
  ],
  labs: [
    {
      id: "lab-00",
      title: "Inspection Scenario & Run Folder Setup",
      content: "Reuse the Day 2 run-folder schema for B2 inspection evidence. Create the folder tree before any robot motion.\n\n- Adapt metadata.json for B2 (robot_platform, robot_id, interface, camera_mode)\n- Define checkpoint IDs with descriptions\n- Plan conservative B2 motion legs\n- Sketch the required folder tree from memory",
      code_files: [
        { name: "metadata_template.json", code: "{\n  \"schema_version\": \"1.0\",\n  \"created_utc\": \"2026-06-03T02:30:00Z\",\n  \"operator\": \"team_alpha\",\n  \"robot_platform\": \"Unitree B2\",\n  \"robot_id\": \"b2-01\",\n  \"lab\": \"day-04-field-inspection\",\n  \"interface\": \"eth0\",\n  \"environment\": \"indoor corridor mock inspection\",\n  \"camera_sources\": [\"front\", \"back\"],\n  \"checkpoints\": [\"cp01_entry\", \"cp02_asset_label\", \"cp03_exit\"],\n  \"safety_observer\": \"instructor\",\n  \"notes\": \"B2 moved only under supervised SportClient commands; checkpoint frames selected after capture.\"\n}" }
      ]
    },
    {
      id: "lab-01",
      title: "Mock Inspection Video — B2 Front & Back Cameras",
      content: "Use camera_opencv-video.py to capture front/back still images and RTSP video recordings with keyboard controls.\n\n- Run the B2 camera script with the verified interface\n- Save front camera image (Q key) and back camera image (E key)\n- Toggle front RTSP recording (A key) and verify file is playable\n- Map keyboard controls to artifacts and safe exit (ESC) behavior",
      code_files: [] },
    {
      id: "lab-02",
      title: "Field Run & Reporting",
      content: "Combine video, state logging, supervised motion, checkpoint evidence, and validation into a complete B2 inspection run package.\n\n- Start state logging and confirm non-empty sportmodestate.jsonl\n- Execute one short supervised motion leg under instructor gate\n- Capture checkpoint stills during dwell periods\n- Package raw captures into checkpoints/<id>/frame.jpg\n- Run validator and produce field_report.md",
      code_files: [] }
  ]
};

// ===== DAY 05: G1 Architecture, DDS & Safety Readiness =====
const day05 = {
  day: "05",
  title: "G1 Architecture, DDS Communication & Safety Readiness",
  eyebrow: "G1 HUMANOID PLATFORM",
  thesis: "Students must prove they can observe the G1 safely before they are allowed to command it — a robot that can stream state is not automatically safe to move.",
  rules: [
    "Observe before command: rt/lowstate must stream, CheckMode() must report expected ownership, and FSM must not indicate damp or unsafe transitional posture.",
    "No motion commands during Day 5 — Labs 0–2 are strictly read-only: DDS observation, FSM inspection, and mode verification only.",
    "Damping is not a casual stop — on a standing humanoid, damping removes active balance and can cause a fall. Treat mode transitions as operationally significant."
  ],
  pacing: [
    { time: "00:00 – 00:35", session: "Opening Safety Frame & G1 Hardware Architecture", path: "course/day-05/" },
    { time: "00:35 – 00:55", session: "SDK, CycloneDDS & Communication Patterns", path: "course/day-05/lab-00/" },
    { time: "00:55 – 01:10", session: "Break & Bench Readiness", path: "course/day-05/" },
    { time: "01:10 – 01:35", session: "Lab 0 — Environment, Network & SDK Verification", path: "course/day-05/lab-00/" },
    { time: "01:35 – 02:05", session: "Lab 1 — Subscribe to rt/lowstate", path: "course/day-05/lab-01/" },
    { time: "02:05 – 02:15", session: "Break & Synthesis — Compare Cases", path: "course/day-05/" },
    { time: "02:15 – 02:45", session: "Lab 2 — Read-Only FSM & Motion-Mode Inspection", path: "course/day-05/lab-02/" },
    { time: "02:45 – 03:00", session: "Debrief, Assessment & Day 6 Preview", path: "course/day-05/" }
  ],
  slides: [
    {
      title: "Day 5 Position in the Course",
      thesis: "Day 5 bridges quadruped inspection autonomy to humanoid readiness — changing from mission execution to readiness discipline.",
      board_type: "table",
      board_data: {
        headers: ["Day 5 Theme", "What Students Learn", "What Students Should NOT Do Yet"],
        rows: [
          ["G1 Architecture", "Distinguish G1 hardware, dev computer, control computer, DDS topics, high-level clients", "Treat G1 as 'a bigger Go2' or copy Go2/B2 code without checking IDL types"],
          ["Network Readiness", "Configure 192.168.123.x subnet, identify correct interface, verify reachability", "Pass an IP address where SDK expects an interface name"],
          ["DDS Observation", "Subscribe to rt/lowstate, inspect tick, IMU, motor count, mode fields", "Publish low-level commands to rt/lowcmd during Day 5"],
          ["Read-Only FSM Inspection", "Query motion-switcher mode and locomotion FSM readiness without commanding motion", "Use Damp(), Move(), arm commands, or special actions casually"],
          ["Safety Culture", "Apply humanoid-specific spacing, spotter, remote-control, and recovery discipline", "Assume streaming data means robot is ready to stand, wave, or walk"]
        ]
      },
      bottom_band: "G1 has 23–43 DOF, ~35 kg, bipedal balance — its morphology changes both the control problem and the classroom protocol. A quadruped's damped crouch is not a humanoid's fall risk."
    },
    {
      title: "Why Day 5 Is a No-Motion-First Day",
      thesis: "G1 is tall, bipedal, with a higher center of mass — entering damping can cause a fall if the robot is standing without support.",
      board_type: "table",
      board_data: {
        headers: ["Safety Item", "Day 5 Expectation", "Why It Matters"],
        rows: [
          ["Clear Working Area", "Keep students outside fall radius; remove loose obstacles", "A humanoid fall can travel outward and damage people/equipment"],
          ["Remote-Control Owner", "One trained person holds controller; calls out state changes", "State transitions must be coordinated, not improvised"],
          ["Spotter Role", "Use spotter per approved procedure; do not grab moving joints", "Human intervention near actuated limbs is dangerous"],
          ["No-Motion Default", "Labs 0–2 do not send walking, waving, arm, or low-level joint commands", "Learning objective is readiness, not performance"],
          ["Damped-Mode Awareness", "Damping treated as potentially falling state", "Damping can remove balance support — enter deliberately"],
          ["SDK Conflict Avoidance", "Ensure correct robot mode before SDK use", "SDK commands can conflict with built-in motion-control behavior"]
        ]
      },
      bottom_band: "Do NOT use Damp() as a casual 'stop button' during a standing humanoid demo. On G1, damping removes the active control needed to remain upright."
    },
    {
      title: "G1 Hardware & Computing Architecture",
      thesis: "G1 has a development computer (Jetson Orin NX), a dedicated control computer, and a separate DDS communication domain over Ethernet.",
      board_type: "grid",
      board_data: [
        { label: "Degrees of Freedom", value: "23 DOF base, 23–43 DOF for G1-EDU — higher DOF means more complex state and greater need for correct IDL bindings." },
        { label: "Bipedal Balance", value: "Standing stability depends on active control — mode changes have immediate physical consequences unlike quadruped crouch." },
        { label: "Sensing", value: "Depth camera and 3D LiDAR — Day 5 focuses on DDS state streaming, not perception algorithms." },
        { label: "Development Computer", value: "Jetson Orin NX at 192.168.123.164 — runs SDK scripts that communicate with robot services." },
        { label: "Control Computer", value: "Dedicated to Unitree motion control — built-in control program may periodically send commands." },
        { label: "Network Topology", value: "User PC on 192.168.123.x, robot control at 192.168.123.161 — SDK scripts need interface name, not just IP." }
      ],
      bottom_band: "The G1 IDL namespace is unitree_hg, not unitree_go — copying a quadruped subscriber may bind the wrong IDL type even if the topic string looks familiar."
    },
    {
      title: "Day 5 Communication Model: Three Lanes",
      thesis: "Subscribe (observe), publish (command stream), and request/response (RPC) — Day 5 uses only the safest subset: DDS topic subscription and read-only RPC.",
      board_type: "table",
      board_data: {
        headers: ["Communication Lane", "Day 5 Example", "Direction", "Day 5 Use", "Risk Level"],
        rows: [
          ["DDS Topic Subscription", "rt/lowstate", "Robot → Laptop", "Required for Lab 1 — observe state", "Low (read-only)"],
          ["DDS Topic Publication", "rt/lowcmd", "Laptop → Robot", "NOT used for Day 5 teaching", "High (affects joints at low level)"],
          ["RPC Service Client", "MotionSwitcherClient.CheckMode()", "Laptop → Robot Service", "Read-only in Lab 2", "Low (GET-only)"],
          ["RPC Service Client", "G1 LocoClient GET APIs", "Laptop → Robot Service", "Read-only FSM inspection", "Low (GET-only)"]
        ]
      },
      bottom_band: "Analogy: Lab 1 teaches students to read the instruments. Lab 2 teaches students to ask the avionics what mode the aircraft is in. Neither lab authorizes takeoff."
    },
    {
      title: "Network Readiness: Interface Name ≠ IP Address",
      thesis: "Many SDK examples initialize DDS using the local network interface name — the robot IP identifies the remote endpoint for ping, not the interface argument.",
      board_type: "table",
      board_data: {
        headers: ["Term", "Example", "Meaning", "How to Verify"],
        rows: [
          ["Robot Control IP", "192.168.123.161", "Address to test connectivity to robot control computer", "ping 192.168.123.161"],
          ["Dev Computer IP", "192.168.123.164", "G1 development computing unit address", "Network documentation and lab-specific needs"],
          ["User PC Interface IP", "192.168.123.99", "Address assigned to laptop Ethernet adapter on robot subnet", "ip addr or ifconfig"],
          ["User PC Interface Name", "enp2s0, eth0, en6", "The argument SDK scripts require", "Match interface that owns 192.168.123.x address"]
        ]
      },
      bottom_band: "The most common student mistake: passing '192.168.123.161' to a script that expects 'enp3s0'. Require students to copy the exact interface name into lab notes."
    },
    {
      title: "Lab 0: Architecture, Environment & Readiness Gate",
      thesis: "Lab 0 proves that the classroom has a controlled basis for observation — it does not prove G1 can move.",
      board_type: "table",
      board_data: {
        headers: ["Lab 0 Checkpoint", "Instructor Explanation", "Pass Evidence", "Failure Interpretation"],
        rows: [
          ["SDK Import", "Python can locate Unitree SDK modules", "Import or verification script succeeds", "Fix venv, package path, or installation"],
          ["CycloneDDS Found", "SDK can find DDS middleware", "No cyclonedds location error", "Set CYCLONEDDS_HOME or repair installation"],
          ["Interface Identified", "Student knows local adapter to G1", "Interface owns 192.168.123.x address", "Configure Ethernet or choose correct adapter"],
          ["Ping Succeeds", "Basic IP path exists", "Replies from 192.168.123.161", "Check cable, subnet, robot state, adapter, firewall"],
          ["Lowstate Readiness", "Robot may be publishing state", "Later confirmed in Lab 1", "Do not proceed to motion; diagnose observation first"]
        ]
      },
      bottom_band: "During Lab 0, ask repeatedly whether each test is local, network, DDS, or robot-service evidence — this vocabulary builds Day 6 troubleshooting discipline."
    },
    {
      title: "Lab 1: Subscribing to rt/lowstate",
      thesis: "Topic name AND message type must match the robot family — G1 uses unitree_hg (LowState_), not unitree_go (SportModeState_).",
      board_type: "grid",
      board_data: [
        { label: "First message received", value: "DDS discovery and subscription are functioning — record time to first message and script output." },
        { label: "tick", value: "Robot is publishing a changing state sequence — confirm values change over time (not stagnant)." },
        { label: "mode_machine / mode_pr", value: "Machine-state indicator for readiness interpretation — current value and whether it matches expected state." },
        { label: "IMU roll-pitch-yaw", value: "Orientation estimate for posture awareness — values should appear physically plausible for current robot pose." },
        { label: "Motor count", value: "Confirms size of joint-state array visible in message — should match expected G1 configuration." },
        { label: "Message rate", value: "Indicates data streaming continuously — approximate update rate and stability over 30+ seconds." }
      ],
      bottom_band: "If ping succeeds but rt/lowstate does not arrive, which layer is failing: physical Ethernet, IP routing, DDS discovery, topic/message binding, or robot service state? Diagnose layer by layer."
    },
    {
      title: "Interpreting Low-State Without Overclaiming",
      thesis: "Low-state is a state stream, not a permission slip — a robot can publish state while unsafe to move.",
      board_type: "table",
      board_data: {
        headers: ["Observation", "Valid Conclusion", "INValid Conclusion"],
        rows: [
          ["rt/lowstate messages arrive", "DDS observation path is working", "The robot is ready to walk"],
          ["IMU values are plausible", "Orientation telemetry decoded correctly", "Balance controller is healthy for commanded motion"],
          ["Motor array exists", "Joint-state data present in message", "Low-level command publication is safe"],
          ["mode_machine has a value", "Machine state available for interpretation", "Student understands all possible transitions"],
          ["Message rate is stable", "Streaming is continuous under current conditions", "High-level RPC clients must also work"]
        ]
      },
      bottom_band: "Present one ambiguous case: if lowstate streams while robot is in damped mode, students must explain why DDS health and motion readiness diverge."
    },
    {
      title: "Lab 2: Read-Only FSM & Motion-Mode Inspection",
      thesis: "Lab 2 introduces high-level service inspection without high-level motion — GET-only: inspect mode and readiness without issuing standing, walking, or damping.",
      board_type: "table",
      board_data: {
        headers: ["Read-Only Check", "API ID", "Expected Teaching Interpretation"],
        rows: [
          ["MotionSwitcherClient.CheckMode()", "—", "Identifies active motion service/mode — expects name == 'ai' for high-level examples"],
          ["FSM id GET", "7001", "Current locomotion finite-state-machine state — one of the main readiness indicators"],
          ["FSM mode GET", "7002", "Additional high-level state context for readiness classification"],
          ["Balance mode GET", "7003", "Balance-related configuration being reported — helps explain posture readiness"],
          ["Swing height GET", "7004", "Locomotion parameter readable before modification — demonstrates read-before-write habit"],
          ["Stand height GET", "7005", "Body-height configuration in read-only manner — verifies parameter access"]
        ]
      },
      bottom_band: "Known FSM hints: 0=zero torque, 1=damp, 3=sit, 500=start, 702=lie-to-stand, 706=squat/stand. Interpret FSM values, official docs, and observed physical state together."
    },
    {
      title: "Readiness States: FAIL, PARTIAL, READY",
      thesis: "Readiness is a layered diagnostic classification — not a binary pass/fail.",
      board_type: "table",
      board_data: {
        headers: ["Classification", "Evidence Pattern", "Meaning", "Instructor Action"],
        rows: [
          ["FAIL — Local Setup", "SDK imports or CycloneDDS fail before robot communication", "Laptop environment not ready", "Fix installation and env vars before touching robot"],
          ["FAIL — Network", "Interface lacks 192.168.123.x or ping fails", "Laptop cannot reach robot control path", "Check cable, adapter, subnet, robot power"],
          ["PARTIAL — IP Only", "Ping works but rt/lowstate does not stream", "Physical/IP path exists but DDS/topic not healthy", "Inspect interface binding, DDS profile, robot mode, IDL type"],
          ["PARTIAL — DDS Only", "Lowstate streams but RPC checks fail", "Topic subscription works, service access not proven", "Check service availability, SDK client init, mode"],
          ["PARTIAL — Not Motion-Ready", "Lowstate + RPC work but FSM indicates damp/transition", "Communication healthy but command readiness blocked", "Do not move; recover posture/mode via approved procedure"],
          ["READY for Day 6", "Lowstate streams, RPC succeeds, expected mode active, FSM safe, environment clear", "May proceed to supervised motion labs later", "Record evidence and obtain instructor sign-off"]
        ]
      },
      bottom_band: "READY means 'ready to proceed to the next supervised learning step' — NOT 'ready for arbitrary student commands.' Model this language precisely."
    },
    {
      title: "G1 vs. Go2/B2: Avoiding Transfer Errors",
      thesis: "Stop students from transferring quadruped assumptions into humanoid control — damp behavior, message namespace, and balance assumptions all differ.",
      board_type: "table",
      board_data: {
        headers: ["Topic", "Go2/B2 Course Habit", "G1 Day 5 Correction"],
        rows: [
          ["Physical Posture", "Stable quadruped stance or crouch assumed", "Humanoid balance depends on active control — damping may cause fall"],
          ["Message Namespace", "Quadruped examples use unitree_go", "G1 lowstate uses unitree_hg in Day 5 script"],
          ["First Useful Task", "Patrol, obstacle avoidance, or inspection evidence", "State observation and readiness proof"],
          ["Motion Confidence", "High-level motion tested after bounded checks", "No motion until mode, FSM, space, spotter, instructor sign-off align"],
          ["Failure Interpretation", "Stop may result in stable quadruped behavior", "Stop-like state may cause loss of balance depending on posture"],
          ["Student Excitement", "Students want to see walking or gestures", "Students must certify readiness before commanding walking/gestures"]
        ]
      },
      bottom_band: "Ask: which assumption from B2 would be most dangerous on G1? Top answers: 'assuming damp is safe,' 'assuming streaming topic = motion ready,' 'copying wrong IDL type.'"
    },
    {
      title: "Student Lab Record Template",
      thesis: "The lab record teaches traceability — if a Day 6 motion problem occurs, the Day 5 record identifies whether the system was genuinely ready.",
      board_type: "list",
      board_data: [
        "Date, team, robot identifier, laptop hostname — identity and accountability.",
        "Network interface name and laptop interface IP — exact adapter and 192.168.123.x address.",
        "Ping to 192.168.123.161 result — IP reachability before DDS diagnostics.",
        "SDK import verification and CycloneDDS status — environment and middleware health.",
        "CYCLONEDDS_URI status — is a stale DDS profile overriding the default behavior?",
        "First rt/lowstate message time, observed tick behavior, IMU values, motor count — observation evidence.",
        "CheckMode() output, FSM id and interpretation, classification (FAIL/PARTIAL/READY), instructor sign-off."
      ],
      bottom_band: "Students should write one sentence for every failure: 'The current evidence proves X, but does not yet prove Y.' This practice prevents unsafe leaps in reasoning."
    },
    {
      title: "Assessment Questions — Day 5",
      thesis: "Test readiness reasoning, not memorization — a practical assessment: classify a scenario where 'SDK passes, ping passes, lowstate streams, CheckMode ok, but FSM=1.'",
      board_type: "list",
      board_data: [
        "Why does Day 5 avoid motion commands even though the SDK supports control? — Humanoid fall risk, active balance dependence, debugging readiness, need to separate observation from command.",
        "What is the difference between robot IP and SDK network-interface argument? — Robot IP is remote address for reachability; interface argument is local adapter name bound to robot subnet.",
        "What does successful rt/lowstate subscription prove? — DDS topic observation working with correct topic/type; does not prove motion readiness.",
        "Why is using the correct IDL namespace important? — G1 uses G1/HG message types; quadruped examples use Go types. Wrong type binding breaks decoding.",
        "What does FSM = damp imply operationally? — Robot not ready for high-level motion; may lose balance if unsupported; recovery must follow approved procedure.",
        "If ping works but lowstate does not, what layer next? — DDS discovery, interface binding, CycloneDDS profile, topic name, message type, robot publishing state.",
        "Why is Damp() not a casual stop command on a standing humanoid? — Damping can remove active balance and may cause the robot to fall."
      ],
      bottom_band: "Practical assessment: SDK imports pass, ping passes, lowstate streams, CheckMode succeeds, but FSM id is 1. Answer: PARTIAL — not motion-ready (damped state blocks safe high-level motion)."
    },
    {
      title: "Day 5 Takeaways — Six Durable Habits",
      thesis: "Day 5 is the foundation of responsible G1 teaching — observation precedes command, ping is not DDS, and DDS is not motion readiness.",
      board_type: "grid",
      board_data: [
        { label: "1. Observation Precedes Command", value: "\"If we cannot read the robot safely, we do not command it.\" rt/lowstate is the first diagnostic window." },
        { label: "2. Ping Is Not DDS", value: "\"IP reachability is one layer, not the whole stack.\" DDS discovery, topic binding, and IDL matching are separate concerns." },
        { label: "3. DDS Is Not Motion Readiness", value: "\"Streaming state is evidence, not permission.\" A robot can publish state while unsafe to move." },
        { label: "4. Mode Matters", value: "\"A service mode or FSM state can block safe motion even when communication works.\" CheckMode and FSM are separate readiness dimensions." },
        { label: "5. Humanoid Damping Is Serious", value: "\"Damp can mean fall risk, not merely pause.\" On G1, removing active balance has immediate physical consequences." },
        { label: "6. G1 Is Not Go2/B2", value: "\"Use the right IDL, the right posture assumptions, and the right safety procedure.\" Transferring quadruped habits without verification is dangerous." }
      ],
      bottom_band: "Close with: 'Tomorrow we will only command what today we learned to observe, classify, and verify.' Readiness is the prerequisite for authority."
    }
  ],
  labs: [
    {
      id: "lab-00",
      title: "G1 Architecture, Environment & Readiness Gate",
      content: "Verify local SDK environment, network interface, and robot reachability without touching the robot.\n\n- Confirm Python can import unitree_sdk2py modules\n- Set CYCLONEDDS_HOME and verify CycloneDDS is found\n- Identify wired interface on 192.168.123.x subnet\n- Ping 192.168.123.161 to test IP path\n- Complete safety briefing — state perimeter, stop, and command approval rule",
      code_files: [
        { name: "g1_connection_check.py", code: "#!/usr/bin/env python3\n\"\"\"G1 Connection Check — verify SDK environment and network. No robot state access.\"\"\"\nimport sys\n\ndef main():\n    print(\"[G1 CHECK] Verifying SDK environment...\")\n    try:\n        from unitree_sdk2py.core.channel import ChannelFactoryInitialize\n        from unitree_sdk2py.idl.unitree_hg.msg.dds_ import LowState_\n        print(\"[PASS] G1 SDK imports verified (unitree_hg IDL)\")\n    except ImportError as e:\n        print(f\"[FAIL] SDK import error: {e}\")\n        return 1\n    print(\"[READY] Proceed to interface identification and ping test\")\n    return 0\n\nif __name__ == \"__main__\":\n    sys.exit(main())" }
      ]
    },
    {
      id: "lab-01",
      title: "Subscribe to G1 Low-State (rt/lowstate)",
      content: "First robot-observation lab for G1. Subscribe to rt/lowstate using G1/HG IDL type and verify streaming for 30+ seconds.\n\n- Subscribe with ChannelSubscriber(\"rt/lowstate\", LowState_)\n- Interpret tick, mode_machine, IMU, and motor count\n- Confirm message rate is stable\n- Explain why streaming state does not equal motion readiness",
      code_files: [
        { name: "subscribe_lowstate.py", code: "\"\"\"G1 LowState subscriber — the pre-motion observability channel.\"\"\"\nimport sys, time\nfrom unitree_sdk2py.core.channel import ChannelFactoryInitialize, ChannelSubscriber\nfrom unitree_sdk2py.idl.unitree_hg.msg.dds_ import LowState_\n\ndef callback(state: LowState_):\n    print(f\"tick={state.tick} mode_machine={state.mode_machine} \"\n          f\"imu=({state.imu_state.rpy[0]:.2f},{state.imu_state.rpy[1]:.2f},{state.imu_state.rpy[2]:.2f})\")\n\nif __name__ == \"__main__\":\n    ChannelFactoryInitialize(0, sys.argv[1])\n    sub = ChannelSubscriber(\"rt/lowstate\", LowState_)\n    sub.Init(callback, 10)\n    print(f\"[LOWSTATE] Listening on {sys.argv[1]}... Ctrl+C to stop\")\n    while True:\n        time.sleep(1)" }
      ]
    },
    {
      id: "lab-02",
      title: "Read-Only FSM & Motion-Mode Inspection",
      content: "Use MotionSwitcherClient and LocoClient GET APIs to inspect G1 readiness without sending any motion commands.\n\n- Run lab02_fsm_readonly.py with verified interface\n- Check MotionSwitcherClient.CheckMode() for 'ai' mode\n- Query FSM id (API 7001), FSM mode (7002), balance mode (7003)\n- Classify result as FAIL, PARTIAL, or READY\n- Record all evidence in lab report for Day 6 sign-off",
      code_files: [] }
  ]
};

// ===== DAY 06: G1 Safe Locomotion & Arm Control =====
const day06 = {
  day: "06",
  title: "G1 Safe Locomotion, Arm Actions & Integration Policy",
  eyebrow: "G1 MOTION & ARM CONTROL",
  thesis: "Controlling a humanoid involves commanding through multiple software surfaces — the instructor must teach which surface is appropriate for each job and enforce one-command-path-at-a-time discipline.",
  rules: [
    "Readiness gate before every motion lab: rt/lowstate flowing, CheckMode == 'ai', and FSM not damp.",
    "One command path at a time — do not interleave arm SDK streaming and arm RPC gestures in one uncontrolled process.",
    "Neutral-first recovery: use release arm after arm gestures, send StopMove() after velocity commands, and never use Damp as routine classroom stop."
  ],
  pacing: [
    { time: "00:00 – 00:40", session: "Opening, Safety Contract & Readiness Gate", path: "course/day-06/lab-00/" },
    { time: "00:40 – 01:10", session: "High-Level Locomotion — LocoClient & Velocity Commands", path: "course/day-06/lab-01/ & lab-02/" },
    { time: "01:10 – 01:35", session: "Supervised Locomotion Demo (Short Walk)", path: "course/day-06/lab-02/" },
    { time: "01:35 – 01:45", session: "Break & Robot Settle", path: "course/day-06/" },
    { time: "01:45 – 02:15", session: "High-Level Arm Actions — G1ArmActionClient", path: "course/day-06/lab-03/" },
    { time: "02:15 – 02:45", session: "Arm SDK Streaming — rt/arm_sdk & Four-Stage Sequence", path: "course/day-06/lab-04/" },
    { time: "02:45 – 03:00", session: "Integration Policy, Troubleshooting & Knowledge Check", path: "course/day-06/lab-05/" }
  ],
  slides: [
    {
      title: "Day 6 Purpose & Learning Outcomes",
      thesis: "Day 6 is not a choreography day — it is a safety, command-ownership, and integration day moving from read-only readiness into bounded locomotion and arm actions.",
      board_type: "table",
      board_data: {
        headers: ["Outcome Area", "Competency", "Evidence"],
        rows: [
          ["Readiness Gate", "Re-run Day 5 readiness before every motion lab", "Dry-run log showing Readiness: PASS"],
          ["High-Level Locomotion", "Use LocoClient Move, StopMove, LowStand, HighStand under supervision", "Short motion log or observation note"],
          ["High-Level Arm Actions", "Use G1ArmActionClient for face wave and release arm through arm RPC", "--show-map output and supervised sequence"],
          ["Arm SDK Streaming", "Explain rt/arm_sdk vs arm RPC — arm5/arm7 variants and four stages", "Stage timing notes or source walkthrough"],
          ["Integration Policy", "Choose between locomotion, arm RPC, and arm SDK without mixing", "Completed decision guide and mixing-policy explanation"]
        ]
      },
      bottom_band: "The physical robot, not the terminal, is the final source of truth. RPC code 0 means the service accepted the request — it does NOT prove physical safety."
    },
    {
      title: "Day 6 Architecture Map: Three Control Layers",
      thesis: "Read-only observation (rt/lowstate), high-level service control (LocoClient, G1ArmActionClient), and streamed joint targets (rt/arm_sdk) — different authority levels.",
      board_type: "table",
      board_data: {
        headers: ["Surface", "Mechanism", "Course Use", "Main Risk"],
        rows: [
          ["rt/lowstate", "DDS subscription", "Read-only state observation; readiness check", "Misreading data absence as robot fault (may be network)"],
          ["LocoClient", "High-level sport RPC service", "Stance, short velocity motion, wave/handshake variants", "Forgetting StopMove() or using unsafe menu items"],
          ["G1ArmActionClient", "High-level arm RPC service 'arm'", "Predefined gestures: face wave, release arm", "Contact-style gestures near people; failing to release arms"],
          ["rt/arm_sdk", "DDS publishing LowCmd_ at ~20 ms intervals", "Custom upper-body interpolation (arm5 or arm7)", "Wrong DOF variant, unsafe gains, conflicting command owners"],
          ["rt/lowcmd", "Full-body low-level command topic", "OUT OF SCOPE for Day 6", "Whole-body low-level motor authority — different safety class"]
        ]
      },
      bottom_band: "The same robot can be controlled through multiple software surfaces — teach students to ask 'which surface is appropriate for this specific job?' before every script."
    },
    {
      title: "Lab 0: Readiness Gate & Control Surface Orientation",
      thesis: "Before any Day 6 motion, rerun the Day 5 readiness check: rt/lowstate flowing, CheckMode == 'ai', FSM not damp, correct DOF variant confirmed.",
      board_type: "grid",
      board_data: [
        { label: "rt/lowstate", value: "Messages must be flowing — DDS and network alive before any command." },
        { label: "CheckMode == 'ai'", value: "High-level behavior stack in expected mode — wrong mode blocks safe operation." },
        { label: "FSM Not Damp", value: "Damping blocks or makes high-level motion unsafe — must not be 1." },
        { label: "DOF Variant", value: "Instructor confirms arm5 (23-DOF) or arm7 (29-DOF) — wrong variant may command invalid joints." }
      ],
      bottom_band: "Joint index 29 is used in arm SDK examples as an enable/disable field — learn it as a file-specific convention, not a number to reuse blindly across scripts."
    },
    {
      title: "High-Level Locomotion with LocoClient",
      thesis: "G1 high-level movement is a service-mediated request to the onboard locomotion stack — not a raw motor command.",
      board_type: "table",
      board_data: {
        headers: ["Method", "Classroom Meaning", "Teaching Caution"],
        rows: [
          ["WaveHand()", "Loco-service wave gesture", "May be subtle or not visibly arm-like on some units"],
          ["HighStand() / LowStand()", "Requests taller/shorter standing posture", "May return code 0 with little visible change"],
          ["Move(vx, vy, vyaw)", "Sends body-frame velocity command", "Requires open space and following StopMove()"],
          ["StopMove()", "Sends zero velocity — USE after velocity", "Do NOT blindly send after arm gestures"],
          ["Damp()", "Sends robot toward damping behavior", "Avoid in normal Day 6 labs — emergency/special state only"]
        ]
      },
      bottom_band: "The default visible sequence: readiness → face wave via G1ArmActionClient → wait → release arm. Separate the locomotion wave (--loco-wave flag) as an optional comparison."
    },
    {
      title: "Locomotion Safety: Command Scenarios",
      thesis: "Each observable scenario has a recommended instructor response — never let 'RPC returned 0' be the end of the safety check.",
      board_type: "table",
      board_data: {
        headers: ["Scenario", "Recommended Instructor Response"],
        rows: [
          ["RPC returns 0, nothing visible happens", "Check FSM, posture, floor contact, and whether command was subtle stance/wave"],
          ["Student wants longer walk", "Reduce speed first, mark larger test area, run one segment at a time"],
          ["Robot drifts after velocity command", "Send StopMove() again through approved script or high-level menu"],
          ["Student tries damp as normal stop", "Reframe damp as emergency/special state, not routine classroom flow"]
        ]
      },
      bottom_band: "lab04_loco_motion.py validates speed, waits for rt/lowstate, checks motion mode, blocks damp, and always follows velocity segments with StopMove() — follow this pattern."
    },
    {
      title: "High-Level Arm Actions with G1ArmActionClient",
      thesis: "Named actions like 'face wave' are translated by the SDK's action_map into integer IDs — the onboard action player owns the motion plan, not your script.",
      board_type: "table",
      board_data: {
        headers: ["Action Name", "Typical Classroom Policy"],
        rows: [
          ["face wave", "Default safe visible gesture — start here"],
          ["high wave", "Possible approved variation with clearance"],
          ["release arm", "Neutral/release habit after every gesture sequence"],
          ["shake hand / high five", "Instructor-approved only — person-contact style"],
          ["hug", "Avoid in normal classroom demonstrations"],
          ["hands up / heart / clap / reject / x-ray", "Only after checking clearance and instructor allowlist"]
        ]
      },
      bottom_band: "Always print --show-map first (no robot required), then dry-run, then perform default sequence. GetActionList() may be firmware-specific — use the static action_map."
    },
    {
      title: "Arm SDK Streaming: rt/arm_sdk Deep Dive",
      thesis: "In high-level arm RPC, the robot plans the motion. In arm SDK, YOUR script owns interpolation, target positions, gains, and enable/disable timing — published at ~20 ms intervals.",
      board_type: "table",
      board_data: {
        headers: ["Comparison Point", "High-Level Arm RPC", "rt/arm_sdk Streaming"],
        rows: [
          ["Communication", "Request-response RPC service 'arm'", "DDS publish topic rt/arm_sdk"],
          ["Payload", "Integer action ID in RPC body", "LowCmd_ with joint targets, gains, and CRC"],
          ["Motion Planning", "Onboard action player", "Course or vendor script interpolates"],
          ["Typical Classroom Use", "Quick predefined gestures and release", "Demonstrating joint-stream control concepts"],
          ["Safety Concern", "Gesture sweep volume and person contact", "Wrong DOF variant, gains, conflicting publishers, enable/disable mistakes"]
        ]
      },
      bottom_band: "Default arm5 for 23-DOF units, arm7 for 29-DOF with wrist chains. The course wrapper adds safeguards: readiness gate, variant validation, macOS execution rejection, explicit confirmation."
    },
    {
      title: "Four-Stage Arm SDK Streaming Sequence",
      thesis: "Each stage has a distinct purpose: enable → demonstrate → blend back → disable — the script owns each transition.",
      board_type: "table",
      board_data: {
        headers: ["Stage", "Approx. Time (3s duration)", "What the Stream Does", "Teaching Interpretation"],
        rows: [
          ["1", "0–3 s", "Enables arm SDK (index-29 enable field), blends toward zero pose", "Script claims upper-body command authority"],
          ["2", "3–9 s", "Interpolates toward target arm pose", "Main visible arm lift — students observe"],
          ["3", "9–18 s", "Blends back toward measured/neutral pose", "Script exits demonstration trajectory gradually"],
          ["4", "18–21 s", "Ramps arm SDK enable field toward disable", "Command ownership returned cleanly"]
        ]
      },
      bottom_band: "The safest educational parameter change: increase duration in a copied file — this slows interpolation without changing stiffness (kp/kd). Never edit gains casually."
    },
    {
      title: "Integration Policy: One Command Path at a Time",
      thesis: "Integration means choosing and sequencing command paths — not mixing all APIs in one uncontrolled process.",
      board_type: "table",
      board_data: {
        headers: ["Decision Question", "Recommended Path"],
        rows: [
          ["Need a named gesture the robot already knows?", "G1ArmActionClient through the 'arm' RPC service"],
          ["Need a short forward or rotational body movement?", "LocoClient, with StopMove() after velocity"],
          ["Need to shape arm joint positions over several seconds?", "rt/arm_sdk, supervised, with correct DOF variant"],
          ["Need full-body low-level motor control?", "Out of scope for Day 6 — escalate to advanced safety review"],
          ["Unsure which path owns the robot right now?", "Stop, wait, run readiness, use release arm if appropriate"]
        ]
      },
      bottom_band: "Classroom mixing policy: finish one pipeline completely, wait 10+ seconds before switching, re-check readiness, never interleave arm SDK and RPC in same process. If motion looks wrong: stop scripts, return to observation, recover posture."
    },
    {
      title: "Troubleshooting Matrix — Day 6",
      thesis: "Start from the bottom of the stack — do not diagnose a gesture problem before confirming network, CycloneDDS, rt/lowstate, motion mode, and FSM state.",
      board_type: "table",
      board_data: {
        headers: ["Symptom", "Likely Cause", "Instructor Response"],
        rows: [
          ["No rt/lowstate messages", "Wrong interface, static IP issue, robot not booted, DDS setup", "Verify wired interface, ping robot, unset CYCLONEDDS_URI, rerun readiness"],
          ["CheckMode not 'ai'", "Robot in another mode or command ownership issue", "Follow field guide; do not begin motion"],
          ["FSM is 1 / damp", "Robot in damping or blocked state", "Recover posture; rerun Day 5 readiness; no Day 6 motion"],
          ["RPC returns 0 but motion subtle", "Stance/wave commands visually small on some firmware", "Compare with default arm RPC wave; confirm physical state"],
          ["Robot drifts after Move", "Velocity command not stopped", "Send StopMove() through approved high-level path"],
          ["Arm action name rejected", "Name doesn't match SDK action_map exactly", "Run --show-map; copy names precisely"],
          ["Arm SDK jerky or fighting", "Conflicting control path, wrong gains, wrong variant", "Abort, stop scripts, run readiness, do not edit gains"]
        ]
      },
      bottom_band: "If arms remain high after demo: try approved release arm once, then re-check readiness and posture. Never send competing commands to recover."
    },
    {
      title: "Assessment & Instructor Sign-Off",
      thesis: "A participant ready to facilitate Day 6 must show: readiness log, locomotion note, arm action map, arm SDK explanation, and integration policy understanding.",
      board_type: "list",
      board_data: [
        "What three conditions define the Day 6 readiness gate? — rt/lowstate flowing, CheckMode == 'ai', FSM not damp.",
        "When is StopMove() required? — After velocity commands (Move). Do NOT blindly call after a wave gesture.",
        "What service does G1ArmActionClient use? — The high-level arm RPC service named 'arm'.",
        "What topic does the arm SDK lab publish to? — rt/arm_sdk.",
        "Why arm5 vs arm7 selection? — Different G1 DOF variants have different available wrist joints.",
        "What is the safe integration policy after an arm SDK run? — Finish, wait, re-check readiness, neutral-first recovery, do not interleave streams and RPC.",
        "Why is rt/lowcmd excluded from Day 6? — Full-body low-level motor authority belongs to a different safety class."
      ],
      bottom_band: "Write a 5-sentence decision guide for a visitor demo: readiness gate, chosen API path, physical clearance, how action stops/returns to neutral, evidence to record."
    },
    {
      title: "Day 7 Readiness Bridge",
      thesis: "Day 7 adds audio, speech, LED — but still depends on the same discipline: establish communication, observe state, choose one control surface, run bounded command, collect evidence, stop cleanly.",
      board_type: "grid",
      board_data: [
        { label: "State Before Action", value: "Every future G1 feature should be introduced by asking: What state can we observe? Which client owns the subsystem? What is the stop or release behavior?" },
        { label: "One Command Owner", value: "Day 7 capstone sequences audio + LED + gesture in a single script — not multiple terminals competing for control." },
        { label: "Evidence Collection", value: "Return codes, timing, and observed behavior remain the foundation — even for 'expressive' features like speech and LEDs." }
      ],
      bottom_band: "The most important Day 6 habit to carry forward: state before action. Every future G1 feature begins with the same readiness gate pattern."
    }
  ],
  labs: [
    {
      id: "lab-00",
      title: "Day 6 Readiness & Control Surface Orientation",
      content: "Non-motion readiness block comparing G1ArmActionClient, rt/arm_sdk, and rt/lowcmd — rerun Day 5 readiness gate before any Day 6 motion.\n\n- Re-run Day 5 lab02_fsm_readonly.py\n- Confirm rt/lowstate, CheckMode='ai', FSM not damp\n- Identify DOF variant (arm5 or arm7)\n- Map all control surfaces to their authority levels",
      code_files: [
        { name: "day6_readiness.sh", code: "#!/bin/bash\n# Day 6 Readiness Gate — rerun Day 5 FSM check before any motion\necho \"=== Day 6 Readiness Gate ===\"\necho \"1. Confirm rt/lowstate is flowing\"\necho \"2. Confirm CheckMode == 'ai'\"\necho \"3. Confirm FSM is NOT damp (not 1)\"\necho \"4. Confirm DOF variant (arm5 for 23-DOF, arm7 for 29-DOF)\"\npython course/day-05/lab-02/lab02_fsm_readonly.py \"${1:-en6}\"" }
      ]
    },
    {
      id: "lab-01",
      title: "High-Level Locomotion Sequence",
      content: "Use LocoClient for safe velocity-based locomotion under instructor supervision. Default: visible arm wave via G1ArmActionClient.\n\n- Run lab03_loco_sequence.py --dry-run first\n- Default: face wave → wait → release arm\n- Optional --loco-wave flag for locomotion-service wave comparison\n- Always confirm StopMove() after velocity segments",
      code_files: [] },
    {
      id: "lab-02",
      title: "Supervised Locomotion Motion",
      content: "Short forward motion or stance demo with spotter and at least 3m forward clearance. Always follows velocity with StopMove().\n\n- Validate speed against class limits\n- Wait for rt/lowstate before motion\n- Check motion mode and block damp\n- Execute short forward Move, then StopMove()\n- Record command, return code, and observed behavior",
      code_files: [] },
    {
      id: "lab-03",
      title: "High-Level Arm Actions — G1ArmActionClient",
      content: "Use the arm RPC service for predefined gestures. Start with --show-map, then dry-run, then default sequence.\n\n- Print action_map with --show-map (no robot required)\n- Dry-run to verify client initialization\n- Execute face wave → release arm sequence\n- Explain why action names are not the same as safety approval",
      code_files: [
        { name: "arm_action_sequence.py", code: "\"\"\"G1 Arm Action Sequence — high-level RPC gestures.\"\"\"\nimport sys, time\nfrom unitree_sdk2py.core.channel import ChannelFactoryInitialize\nfrom unitree_sdk2py.g1.arm.g1_arm_action_client import G1ArmActionClient\n\nACTION_MAP = {\n    \"face wave\": 1, \"high wave\": 2, \"release arm\": 0,\n    \"shake hand\": 3, \"high five\": 4, \"hug\": 5,\n    \"hands up\": 6, \"heart\": 7, \"clap\": 8, \"reject\": 9, \"x-ray\": 10\n}\n\ndef main(interface: str, dry_run: bool = False):\n    if \"--show-map\" in sys.argv:\n        for name, aid in ACTION_MAP.items():\n            print(f\"  {name:15s} -> {aid}\")\n        return\n    ChannelFactoryInitialize(0, interface)\n    client = G1ArmActionClient()\n    client.SetTimeout(10.0)\n    client.Init()\n    if dry_run:\n        print(\"[DRY-RUN] Arm action client initialized — no motion sent\")\n        return\n    print(\"[ACTION] face wave\")\n    client.ExecuteAction(ACTION_MAP[\"face wave\"])\n    time.sleep(4)\n    print(\"[ACTION] release arm\")\n    client.ExecuteAction(ACTION_MAP[\"release arm\"])\n\nif __name__ == \"__main__\":\n    main(sys.argv[1], \"--dry-run\" in sys.argv)" }
      ]
    },
    {
      id: "lab-04",
      title: "Arm SDK Streaming — rt/arm_sdk",
      content: "Publish LowCmd_ at ~20 ms intervals on rt/arm_sdk for custom upper-body interpolation. Four-stage sequence: enable → demonstrate → blend back → disable.\n\n- Confirm arm5 (23-DOF) or arm7 (29-DOF) variant\n- Run readiness gate before streaming\n- Observe four-stage sequence timing\n- Explain why this lab requires supervisor and no overlapping arm-control process",
      code_files: [] },
    {
      id: "lab-05",
      title: "Integration Policy & Comparison",
      content: "Print decision guide comparing all control surfaces. Run RPC-only recap: release arm → face wave → release arm.\n\n- Run --compare-only (no robot needed) for decision guide\n- Execute integration recap with dry-run first\n- Explain: one path per run, pause, re-check, neutral-first recovery\n- Complete written decision guide for a visitor demonstration",
      code_files: [] }
  ]
};

// ===== DAY 07: G1 Audio, Speech, LED & Capstone =====
const day07 = {
  day: "07",
  title: "G1 Audio, Speech, LED & Capstone Integration",
  eyebrow: "G1 AUDIO & CAPSTONE",
  thesis: "A humanoid robot becomes much easier to understand when it can communicate its state — audio and LEDs are not decorative features but operator-facing observability channels that make the robot inspectable, teachable, and safer to operate.",
  rules: [
    "Single DDS session owner — only one operator/script sends commands to the robot during the demonstration.",
    "Announce before moving: the robot should speak, indicate intent with LEDs, and only then perform a bounded physical action — never move first and explain later.",
    "Dexterous hand control is explicitly out of scope for Day 7 — all physical actions refer to Day 6 arm gestures, not grasping or hand manipulation."
  ],
  pacing: [
    { time: "00:00 – 00:15", session: "Opening & Day 6 Readiness Gate", path: "course/day-07/lab-00/" },
    { time: "00:15 – 00:35", session: "G1 Audio & Lighting Hardware — AudioClient Architecture", path: "course/day-07/" },
    { time: "00:35 – 01:00", session: "DDS Session Ownership & Script Anatomy Walkthrough", path: "course/day-07/" },
    { time: "01:00 – 01:25", session: "Lab 1 — Audio Client, Volume & TTS", path: "course/day-07/lab-01/" },
    { time: "01:25 – 01:35", session: "Break & Robot Reset", path: "course/day-07/" },
    { time: "01:35 – 02:00", session: "Lab 2 — LED Control & Gesture Debrief", path: "course/day-07/lab-02/" },
    { time: "02:00 – 02:30", session: "Capstone Design Pattern — Voice + LEDs + Arm", path: "course/day-07/lab-03/" },
    { time: "02:30 – 02:50", session: "Troubleshooting, Evidence Collection & Assessment", path: "course/day-07/" },
    { time: "02:50 – 03:00", session: "Course Closing & Capstone Sign-Off", path: "course/day-07/lab-03/" }
  ],
  slides: [
    {
      title: "Day 7 Purpose & Teaching Stance",
      thesis: "Day 7 is the human-facing integration day — audio and LEDs are not decorative; they are operator-facing observability channels that make the robot inspectable, teachable, and safer to operate.",
      board_type: "table",
      board_data: {
        headers: ["Teaching Priority", "What Students Learn", "Evidence of Understanding"],
        rows: [
          ["Audio as Status Channel", "Use TTS to announce intent and completion before/after physical actions", "Students narrate robot state changes verbally before sending commands"],
          ["LEDs as Visual State", "RGB colors make execution phase visible to all observers", "Students map blue=starting, red=action, green=complete, off=reset"],
          ["Capstone as Integration", "Combine previous modules without command-path conflicts", "Students design a bounded sequence with proper waits and return-code checks"],
          ["Single Session Owner", "Only one terminal sends commands — observers assist but don't compete", "Students identify the active command owner before every demonstration"],
          ["Safety Discipline", "Even expressive demos require readiness gates, stops, and recovery plans", "Students can explain how to stop an audio/LED sequence mid-demo"]
        ]
      },
      bottom_band: "The central Day 7 message: a robot that communicates its intent is easier to trust — but only if communication is paired with disciplined control."
    },
    {
      title: "G1 Audio & Lighting Hardware Context",
      thesis: "G1 includes speaker, microphone array, and RGB light strip — AudioClient is the single SDK class that exposes TTS, volume, and LED control.",
      board_type: "grid",
      board_data: [
        { label: "Speaker", value: "8Ω, 3 W rated, 5 W peak — voice announcements and TTS playback. Choose volume appropriate to the room." },
        { label: "RGB Light Strip", value: "256-color capability — each channel 0–255 with minimum 200 ms interval between calls." },
        { label: "Microphone Array", value: "4-mic array, 20 mm spacing — discussed as future ASR input; NOT used for Day 7 core lab." },
        { label: "AudioClient", value: "Single SDK class providing TtsMaker, GetVolume, SetVolume, LedControl — LED control lives through AudioClient, not a separate service." },
        { label: "Development Computer", value: "Jetson Orin NX runs SDK scripts that communicate with robot audio/lighting services." }
      ],
      bottom_band: "Audio is not merely sound — in robotics, sound is a communication channel. A professional robot should announce transitions: 'starting demonstration,' 'changing LED,' 'performing wave,' 'sequence complete.'"
    },
    {
      title: "Day 7 Communication Model: Same DDS. New Subsystem.",
      thesis: "Day 7 uses the same DDS initialization, the same rt/lowstate readiness gate, and the same single-owner policy — but now the service client is AudioClient instead of only LocoClient.",
      board_type: "table",
      board_data: {
        headers: ["Layer", "Day 5/6 Pattern", "Day 7 Extension"],
        rows: [
          ["DDS Initialization", "ChannelFactoryInitialize(0, interface)", "Same — DDS must bind to correct network adapter"],
          ["Readiness Gate", "rt/lowstate flowing, CheckMode == 'ai', FSM not damp", "Same — audio/LED scripts also wait for rt/lowstate"],
          ["Service Clients", "LocoClient, G1ArmActionClient", "AudioClient added — provides TTS, volume, and LED control"],
          ["Single Owner Policy", "One terminal sends commands", "Same — capstone sequences audio + gesture in ONE script"],
          ["Evidence Collection", "Return codes, timing, observed behavior", "Same — audio return codes, LED colors, TTS phrases logged"]
        ]
      },
      bottom_band: "Day 7 may feel 'less dangerous' because it focuses on audio and LEDs, but the same communication discipline still applies. Many Day 7 failures are environment, interface, or session-ownership failures — not audio failures."
    },
    {
      title: "AudioClient Service Model Deep Dive",
      thesis: "AudioClient implements TtsMaker, GetVolume, SetVolume, LedControl, PlayStream, and PlayStop — the key architectural point is that LED control lives through the audio client.",
      board_type: "table",
      board_data: {
        headers: ["Function", "Purpose", "Parameter Pattern", "Day 7 Use"],
        rows: [
          ["GetVolume()", "Read current system volume", "No user payload", "Probe before and after volume changes"],
          ["SetVolume(volume)", "Set system volume", "0–100 range", "Use conservative classroom values; clamp unsafe inputs"],
          ["TtsMaker(text, speaker_id)", "Convert text to speech", "Text + speaker role ID (0=Chinese, 1=English)", "Main speech-output primitive for announcements"],
          ["LedControl(R, G, B)", "Set RGB light-strip color", "Each channel 0–255", "State visualization: blue, red, green, off"],
          ["PlayStream(...)", "Play PCM stream audio", "App name, stream ID, PCM bytes", "Future extension — not required for Day 7 core"],
          ["PlayStop(app_name)", "Stop stream playback", "Application name", "Future extension and cleanup tool"]
        ]
      },
      bottom_band: "TtsMaker returns 0 on success — always print return codes, wait after long-running actions, and report nonzero results. Never treat service calls as magical commands that always work."
    },
    {
      title: "Speaker IDs & Language Discipline",
      thesis: "speaker_id 0 = Chinese, speaker_id 1 = English — mixed Chinese/English modes are not supported, and mismatched speaker ID is a common cause of TTS silence.",
      board_type: "table",
      board_data: {
        headers: ["TTS Choice", "Recommended Practice", "Reason"],
        rows: [
          ["Chinese phrase", "Use speaker_id=0", "Matches Unitree's documented Chinese role mapping"],
          ["English phrase", "Use speaker_id=1", "Matches Unitree's documented English role mapping"],
          ["Mixed-language sentence", "Avoid in Day 7", "Mixed Chinese/English modes are not supported"],
          ["Very long phrase", "Keep short; wait for completion", "Short utterances are easier to verify and less disruptive"],
          ["Loud volume", "Avoid; use moderate values", "Classroom demos should prioritize clarity and comfort"]
        ]
      },
      bottom_band: "Demonstrate the default phrase first, then run a short custom phrase like 'Day seven audio lab is ready.' The goal is reliable service invocation, not theatrical speech."
    },
    {
      title: "Lab 0: Readiness Before Interaction",
      thesis: "Lab 0 is short but critical — confirm Day 6 completion, single DDS session owner, environment, and motion envelope before ANY audio or LED demo.",
      board_type: "table",
      board_data: {
        headers: ["Readiness Gate Item", "Pass Criterion", "Evidence to Collect"],
        rows: [
          ["Day 6 Completion", "Team can explain Day 6 readiness and motion safety", "Verbal check or Day 6 log"],
          ["Environment", "unitree_env active; SDK imports verified", "Terminal prompt and package imports"],
          ["DDS Readiness", "Correct interface; rt/lowstate visible", "Connection check output"],
          ["Session Ownership", "One operator terminal selected", "Team role assignment"],
          ["Motion Envelope", "Clear space; robot supervised; remote/E-stop ready", "Instructor visual confirmation"],
          ["Script Scope", "Team knows which script will run and what it will do", "Pre-run explanation by student"]
        ]
      },
      bottom_band: "Instructor prompt: 'Before we let the robot speak or move, tell me which process owns DDS, which network interface you are using, what the script will do first, and how you will stop the demonstration if the robot behaves unexpectedly.'"
    },
    {
      title: "Lab 1: AudioClient — Volume & TTS",
      thesis: "The core audio sequence: initialize DDS → create AudioClient → probe volume → set volume → speak TTS phrase → wait for completion → observe return code.",
      board_type: "list",
      board_data: [
        "Initialize DDS on the selected network interface — communication must bind to the correct adapter. ChannelFactoryInitialize(0, interface)",
        "Create and initialize AudioClient — service client must be initialized before calls. client.SetTimeout(10.0); client.Init()",
        "Wait for rt/lowstate — readiness should precede action. require_lowstate(timeout_s=5.0)",
        "Call GetVolume() — always measure current state before changing it.",
        "Call SetVolume(volume) — use bounded, comfortable values for the room (default script targets 85).",
        "Call TtsMaker(text, speaker_id) — choose language mode per TTS call and match speaker ID to that language.",
        "Wait for speech to finish — speech is asynchronous enough that scripts need timing margins (~3–4 seconds).",
        "Print return code — nonzero results must be investigated, not ignored."
      ],
      bottom_band: "The infrastructure lesson: helper methods like audio.TtsMaker() are easier to use, but the raw view (API ID → JSON params → RPC call) shows the actual service design — each call has a name, parameters, return code, and timeout."
    },
    {
      title: "Lab 1 Teaching Scripts: From Raw to Helper",
      thesis: "The Day 7 repository provides a spectrum of scripts: raw API inspection (lab01_audio.py), combined demo (lab01_audio_client.py), audio-only (lab01_audio_only.py), and LED-only (lab01_led_only.py).",
      board_type: "table",
      board_data: {
        headers: ["Script", "Role", "Best Use"],
        rows: [
          ["lab01_audio.py", "Infrastructure inspection — prints API constants, IDs, raw JSON payloads", "Lecture: explain service architecture before live operation"],
          ["lab01_audio_client.py", "Expanded combined demo — readiness checks, dry-run, custom text, volume clamping", "Live demo: full TTS + LED + WaveHand sequence"],
          ["lab01_audio_only.py", "Narrow audio-only utility — TTS and volume without gesture or LED", "Constrained rooms or motion-disabled sessions"],
          ["lab01_led_only.py", "Narrow LED-only utility — RGB color cycling without speech or gesture", "Teaching RGB control in isolation"]
        ]
      },
      bottom_band: "Run --show-api first (lab01_audio.py) without robot connection to show the service catalog. If GetVolume works but TtsMaker fails, DDS and the audio service may be reachable but the specific TTS API, language role, or timeout may be wrong."
    },
    {
      title: "Lab 2: RGB LEDs & Gesture Debrief",
      thesis: "LED colors make robot state visible to all observers — the recommended color mapping creates a shared vocabulary across the classroom.",
      board_type: "table",
      board_data: {
        headers: ["LED Color", "R, G, B Call", "Suggested Classroom Meaning", "Teaching Use"],
        rows: [
          ["Blue", "LedControl(0, 0, 255)", "Starting, standby, or demo mode", "Announce 'demo starting' — LED blue"],
          ["Red", "LedControl(255, 0, 0)", "Attention, warning, or action in progress", "LED red during WaveHand() or active motion"],
          ["Green", "LedControl(0, 255, 0)", "Ready, safe, or successful completion", "LED green on completion — verify visually"],
          ["Off", "LedControl(0, 0, 0)", "Sequence complete or reset", "Return to off at end of sequence"]
        ]
      },
      bottom_band: "Unitree documents minimum 200 ms interval between LedControl calls. Course scripts use 1.0–1.5 s waits — conservative and classroom-friendly. LED timing matters: too fast and observers miss transitions; too slow and sequence drags."
    },
    {
      title: "Professional Sequencing Rule: Announce → Indicate → Move → Confirm",
      thesis: "In human-facing robotics, the robot should announce with speech, indicate with LEDs, perform a bounded physical action, settle, and then confirm completion.",
      board_type: "table",
      board_data: {
        headers: ["Phase", "Channel", "Example", "Why"],
        rows: [
          ["Announce Intent", "TTS", "\"Starting Day 7 capstone demonstration.\"", "Observers know what is about to happen"],
          ["Indicate State", "LEDs", "Set LED blue → wait 1s", "Visual confirmation of script progress even without audio"],
          ["Move (if approved)", "LocoClient / G1ArmActionClient", "WaveHand() — ONE bounded action", "Physical gesture is expected, not surprising"],
          ["Settle", "Wait", "time.sleep(4)", "Allow motion to complete; confirm robot posture stable"],
          ["Confirm Completion", "TTS + LEDs", "\"Sequence complete.\" + LED green", "Observers know demo is finished and robot is in safe state"]
        ]
      },
      bottom_band: "Never move first and explain later. In human-facing robotics, the robot should communicate before, during, and after every action. This is not decoration — it is operational transparency."
    },
    {
      title: "Capstone Design Pattern: Small State Machine",
      thesis: "A robust Day 7 capstone is a small explicit state machine — each state has a clear purpose, a visible or audible signal, a bounded physical action, and a return-code check.",
      board_type: "table",
      board_data: {
        headers: ["State", "Behavior", "Safety Principle"],
        rows: [
          ["READY_CHECK", "Confirm rt/lowstate, operator role, clear space", "No action before readiness"],
          ["ANNOUNCE_START", "TTS: 'Starting Day 7 capstone.' LED blue", "Observers know what is happening"],
          ["GESTURE", "WaveHand() or approved Day 6 arm action", "One physical action at a time"],
          ["STATUS_UPDATE", "LED green or TTS confirmation", "Robot communicates completion"],
          ["OPTIONAL_MOTION", "Only instructor-approved Day 6 locomotion fragment", "No new untested motion on capstone day"],
          ["SHUTDOWN_SIGNAL", "LED off or green; TTS: 'Demo complete.'", "Return to known safe state"],
          ["LOG_RESULTS", "Record return codes and observations", "Evidence supports assessment and debugging"]
        ]
      },
      bottom_band: "The capstone should be assessed not by how flashy it is, but by how well it demonstrates system discipline. A predictable, well-logged TTS + LED + wave sequence is more professional than an unstable improvised walking demo."
    },
    {
      title: "Capstone Pseudocode: Initialize Once, Sequence One at a Time",
      thesis: "From the lecture notes: initialize DDS, require rt/lowstate, create AudioClient and LocoClient, run each step as a named bounded action with return-code checks.",
      board_type: "list",
      board_data: [
        "initialize_dds(interface) — bind to the correct network adapter once.",
        "require_lowstate(timeout_s=5.0) — confirm robot state is visible before any action.",
        "Create AudioClient and LocoClient — set timeouts, call Init(), own the session.",
        "run_step('set LED blue', audio.LedControl(0,0,255)) — each step is named and bounded.",
        "run_step('announce start', audio.TtsMaker('[Day 7 capstone starting.]', 1)) — short phrase, correct speaker ID.",
        "time.sleep(4) — wait for speech to complete.",
        "run_step('wave hand', loco.WaveHand) — one bounded physical action.",
        "time.sleep(4) — wait for gesture completion.",
        "run_step('set LED green', audio.LedControl(0,255,0)) — confirm completion visually.",
        "run_step('announce complete', audio.TtsMaker('[Capstone complete.]', 1)) — spoken confirmation.",
        "run_step('LED off', audio.LedControl(0,0,0)) — return to known safe state.",
        "Log all return codes and observed behavior — evidence must survive the demo."
      ],
      bottom_band: "Integration does NOT mean concurrency. In a capstone, integration means different capabilities cooperate in a planned SEQUENCE. It does NOT mean every script is launched at once."
    },
    {
      title: "Command-Path Mixing Policy",
      thesis: "Day 7 layers speech and LEDs on top of the existing control surfaces — the psychological effect of an 'expressive' robot can lead teams to over-combine scripts.",
      board_type: "table",
      board_data: {
        headers: ["Mixing Case", "Allowed in Day 7?", "Reason"],
        rows: [
          ["One script uses AudioClient only", "Yes, after readiness", "No physical motion — sound and light only"],
          ["One script uses AudioClient + WaveHand()", "Yes, under supervision", "Physical gesture is bounded and expected"],
          ["Integrated script sequences audio + Day 6 arm action", "Instructor-approved only", "Must avoid simultaneous arm/locomotion paths"],
          ["Multiple terminals run separate robot scripts", "No", "Violates single DDS session ownership"],
          ["Voice recognition triggers movement automatically", "Not for Day 7 core", "Requires intent validation and safety architecture"],
          ["Dexterous hand manipulation", "No", "Explicitly out of scope per Day 7 README"]
        ]
      },
      bottom_band: "If a team runs an audio script that calls WaveHand() while another terminal runs an arm sequence, the problem is not software cleanliness — it is physical command conflict. One owner. One script. One sequence."
    },
    {
      title: "Troubleshooting Guide — Day 7",
      thesis: "Day 7 problems fall into five categories: environment setup, DDS visibility, audio service reachability, language/volume configuration, and timing/concurrency.",
      board_type: "table",
      board_data: {
        headers: ["Symptom", "Likely Cause", "Diagnostic Question", "Corrective Action"],
        rows: [
          ["Script exits: CYCLONEDDS_HOME not set", "SDK environment not activated", "Is unitree_env active? CycloneDDS installed?", "Activate environment; export CYCLONEDDS_HOME"],
          ["No rt/lowstate within 5 seconds", "Wrong interface, robot not reachable, DDS config", "Which network interface is connected to robot?", "Run Day 5/6 connection check; correct interface name"],
          ["GetVolume returns unexpected result", "Audio service unavailable or response format differs", "Did AudioClient.Init() complete?", "Recheck service version, timeout, robot state"],
          ["TTS does not sound", "Volume low, wrong speaker ID, service error, language mismatch", "What return code? Which speaker ID?", "Set moderate volume; match language to speaker ID; keep phrase short"],
          ["LED does not change", "RGB call failed or timing too fast", "Are return codes nonzero? Spaced ≥200 ms?", "Use 1-second waits; verify LedControl return code"],
          ["Wave occurs at wrong time", "Script sequence misunderstood; multiple clients", "Is another terminal running?", "Stop all extra scripts; restore single owner"],
          ["Robot jitters during SDK work", "Built-in controller or command path conflicts", "Is robot in appropriate debug/SDK mode?", "Follow Unitree quick-start debug guidance"]
        ]
      },
      bottom_band: "Preserve evidence: copy command output, return codes, selected interface, script name, phrase, volume, speaker ID, and observed robot behavior. Without those details, the instructor cannot distinguish a language issue from a DDS issue from a service issue."
    },
    {
      title: "Design an Interaction Contract — Student Activity",
      thesis: "Before any capstone-like sequence, each team should write a short contract: what the robot will say, what colors it will display, what physical actions it will perform, and how the team will stop.",
      board_type: "table",
      board_data: {
        headers: ["Contract Field", "Example Answer"],
        rows: [
          ["Operator", "\"Student A owns the terminal and runs all commands.\""],
          ["Interface", "\"Robot network interface is en6.\""],
          ["Initial Phrase", "\"Starting Day 7 capstone demonstration.\""],
          ["LED Mapping", "\"Blue = starting, red = action, green = complete, off = reset.\""],
          ["Physical Action", "\"One WaveHand() only; no walking.\""],
          ["Wait Periods", "\"4s after TTS, 4s after wave, 1s between LEDs.\""],
          ["Stop Condition", "\"Any unexpected motion, nonzero return code, or instructor stop call.\""],
          ["Evidence", "\"Save terminal output and note observed robot behavior.\""]
        ]
      },
      bottom_band: "This activity transforms Day 7 from a script-running exercise into a systems-design exercise. In professional robotics, a demonstration plan, safety case, and evidence log are often more important than a single impressive action."
    },
    {
      title: "Assessment Questions — Day 7",
      thesis: "Test conceptual understanding, not memorization — can students explain why audio still requires rt/lowstate readiness? Why LED control lives through AudioClient?",
      board_type: "list",
      board_data: [
        "Why does Day 7 still require rt/lowstate readiness if the main focus is audio? — Same DDS and robot connectivity assumptions apply; some scripts include physical actions. State visibility is a safety gate.",
        "Why does the LED script use AudioClient instead of a separate LED client? — G1 upper-body audio and lighting functions are grouped under the audio interaction hardware and exposed through AudioClient in the SDK.",
        "What range should SetVolume use? LedControl channels? — 0–100 for volume; 0–255 per RGB channel.",
        "Why should LED calls be spaced apart? — Unitree specifies minimum 200 ms interval; course scripts use 1s conservative waits.",
        "What is the speaker ID rule? — 0 for Chinese, 1 for English; avoid mixed Chinese/English in a single TTS call.",
        "Why is voice-command ASR not the Day 7 core? — ASR adds ambiguity; Day 7 focuses on safe output channels and supervised motion.",
        "What does 'single DDS session owner' mean? — Only one operator/script sends commands; others observe but do not run competing control scripts.",
        "Why is dexterous hand control excluded? — Day 7 README explicitly marks hand control out of scope; manipulation refers to Day 6 arm gestures.",
        "What makes a capstone sequence professional? — Bounded, announced, visible, logged, recoverable, and uses one command path at a time."
      ],
      bottom_band: "A team is ready to pass Day 7 when it can safely run an audio/LED demo, explain every command in the script, and propose a capstone sequence that respects single-owner policy and Day 6 safety boundaries."
    },
    {
      title: "Day 7 Takeaways — The Complete G1 Story",
      thesis: "Day 7 completes the G1 arc: observe (Day 5), move safely (Day 6), communicate (Day 7) — the robot is inspectable, controllable, and now expressible under disciplined supervision.",
      board_type: "grid",
      board_data: [
        { label: "1. Sound Is a Communication Channel", value: "\"A professional robot announces transitions.\" TTS makes system behavior legible to observers and helps operators detect whether the script has progressed as expected." },
        { label: "2. LEDs Are Visual Observability", value: "\"Color makes execution phase visible to everyone.\" Blue/red/green/off gives the classroom a shared vocabulary for robot state." },
        { label: "3. Expressive Features Still Need Gates", value: "\"Audio does not remove the need for DDS, readiness, and single owner.\" The same communication discipline applies — sound and light are just new service surfaces." },
        { label: "4. Capstones Are State Machines", value: "\"Integration means sequencing, not concurrency.\" A small explicit state machine with named steps, waits, and return-code checks." },
        { label: "5. Announce Before Action", value: "\"Never move first and explain later.\" The robot should speak, indicate, perform one bounded action, settle, and confirm — operational transparency." },
        { label: "6. Evidence Completes the Demo", value: "\"Return codes, timing, and observed behavior must survive the demo.\" Without logs, a successful capstone is indistinguishable from a lucky one." }
      ],
      bottom_band: "Closing message: A humanoid robot that can speak, light up, wave, and walk is compelling — but only when every subsystem is initialized once, sequenced cleanly, owned by one operator, and stopped gracefully."
    }
  ],
  labs: [
    {
      id: "lab-00",
      title: "Readiness Gate & DDS Session Ownership",
      content: "Confirm Day 6 completion, single DDS session owner, and motion envelope before any audio/LED demo.\n\n- Verify Day 6 readiness and motion safety understanding\n- Confirm unitree_env active and SDK imports working\n- Identify correct network interface; verify rt/lowstate visible\n- Assign single terminal operator; confirm remote/E-stop ready\n- State before demonstration: which script, what it will do, how to stop",
      code_files: [
        { name: "day7_readiness.sh", code: "#!/bin/bash\n# Day 7 Readiness Gate — confirm environment before audio/LED/capstone\necho \"=== Day 7 Readiness Gate ===\"\necho \"1. Confirm Day 6 completion and safety understanding\"\necho \"2. Activate unitree_env and export CYCLONEDDS_HOME\"\necho \"3. Verify rt/lowstate is flowing on correct interface\"\necho \"4. Assign single DDS session owner (one terminal only)\"\necho \"5. Confirm motion envelope: clear space, spotter, remote/E-stop\"\necho \"6. State: which script, what it will do, how to stop\"\npython course/day-05/lab-02/lab02_fsm_readonly.py \"${1:-en6}\"" }
      ]
    },
    {
      id: "lab-01",
      title: "Audio Client — Volume & TTS",
      content: "Use AudioClient to probe volume, set volume, and speak TTS phrases.\n\n- Run lab01_audio.py --show-api to inspect service catalog\n- Dry-run: initialize clients without audio/gesture output\n- Execute core sequence: GetVolume → SetVolume → TtsMaker\n- Verify return codes and observe speaker behavior\n- Practice language/speaker-ID matching for custom phrases",
      code_files: [
        { name: "audio_tts_sequence.py", code: "\"\"\"G1 Audio TTS Sequence — probe, speak, observe return codes.\"\"\"\nimport sys, time\nfrom unitree_sdk2py.core.channel import ChannelFactoryInitialize\nfrom unitree_sdk2py.g1.audio.g1_audio_client import AudioClient\n\ndef main(interface: str, text: str = \"Day seven audio lab is ready.\", speaker_id: int = 1):\n    ChannelFactoryInitialize(0, interface)\n    audio = AudioClient()\n    audio.SetTimeout(10.0)\n    audio.Init()\n    vol = audio.GetVolume()\n    print(f\"[VOLUME] Current: {vol}\")\n    if \"--set-volume\" in sys.argv:\n        target = int(sys.argv[sys.argv.index(\"--set-volume\") + 1])\n        rc = audio.SetVolume(target)\n        print(f\"[SET VOLUME] {target} -> rc={rc}\")\n    print(f\"[TTS] Speaking: {text}\")\n    rc = audio.TtsMaker(text, speaker_id)\n    print(f\"[TTS] rc={rc}\")\n    time.sleep(4)\n    print(\"[DONE]\")\n\nif __name__ == \"__main__\":\n    main(sys.argv[1])" }
      ]
    },
    {
      id: "lab-02",
      title: "RGB LEDs & Gesture Debrief",
      content: "Use LedControl to cycle RGB colors with conservative waits; integrate WaveHand() as a bounded physical action.\n\n- Map color meanings: blue=starting, red=action, green=complete, off=reset\n- Cycle LEDs with ≥1s waits between calls\n- Perform WaveHand() with LED transition (blue→red during wave→green after)\n- Debrief: why announce before motion? Why LED timing matters?",
      code_files: [
        { name: "led_wave_sequence.py", code: "\"\"\"G1 LED + Gesture Sequence — announce, indicate, act, confirm.\"\"\"\nimport sys, time\nfrom unitree_sdk2py.core.channel import ChannelFactoryInitialize\nfrom unitree_sdk2py.g1.audio.g1_audio_client import AudioClient\nfrom unitree_sdk2py.g1.loco.g1_loco_client import LocoClient\n\ndef main(interface: str):\n    ChannelFactoryInitialize(0, interface)\n    audio = AudioClient()\n    audio.SetTimeout(10.0)\n    audio.Init()\n    loco = LocoClient()\n    loco.SetTimeout(10.0)\n    loco.Init()\n    print(\"[LED] Blue — starting\")\n    audio.LedControl(0, 0, 255)\n    time.sleep(1.5)\n    print(\"[LED] Red — action\")\n    audio.LedControl(255, 0, 0)\n    time.sleep(0.5)\n    print(\"[GESTURE] WaveHand\")\n    loco.WaveHand()\n    time.sleep(4)\n    print(\"[LED] Green — complete\")\n    audio.LedControl(0, 255, 0)\n    time.sleep(1.5)\n    print(\"[LED] Off — reset\")\n    audio.LedControl(0, 0, 0)\n    print(\"[DONE] Sequence complete\")\n\nif __name__ == \"__main__\":\n    main(sys.argv[1])" }
      ]
    },
    {
      id: "lab-03",
      title: "Capstone: Voice + LED + Gesture Integration",
      content: "Design and execute a small safe state machine combining TTS, LEDs, and one approved arm gesture.\n\n- Write interaction contract: operator, interface, phrase, LED map, action, waits, stop condition, evidence\n- Sequence: READY_CHECK → ANNOUNCE_START (TTS+LED blue) → GESTURE (WaveHand, LED red) → STATUS_UPDATE (LED green) → SHUTDOWN_SIGNAL (TTS 'Demo complete', LED off)\n- Single script owner; no overlapping commands\n- Log all return codes and observed behavior",
      code_files: [
        { name: "capstone_state_machine.py", code: "\"\"\"G1 Day 7 Capstone — voice + LED + gesture state machine.\"\"\"\nimport sys, time\nfrom unitree_sdk2py.core.channel import ChannelFactoryInitialize, ChannelSubscriber\nfrom unitree_sdk2py.idl.unitree_hg.msg.dds_ import LowState_\nfrom unitree_sdk2py.g1.audio.g1_audio_client import AudioClient\nfrom unitree_sdk2py.g1.loco.g1_loco_client import LocoClient\n\ndef main(interface: str):\n    ChannelFactoryInitialize(0, interface)\n    audio = AudioClient()\n    audio.SetTimeout(10.0)\n    audio.Init()\n    loco = LocoClient()\n    loco.SetTimeout(10.0)\n    loco.Init()\n    log = []\n    def step(name: str, fn):\n        print(f\"[STEP] {name}\")\n        rc = fn()\n        log.append((name, rc))\n        print(f\"[RC] {name}: {rc}\")\n    step(\"LED blue — starting\", lambda: audio.LedControl(0, 0, 255))\n    time.sleep(1)\n    step(\"TTS — announce start\", lambda: audio.TtsMaker(\"Day seven capstone starting.\", 1))\n    time.sleep(4)\n    step(\"LED red — action\", lambda: audio.LedControl(255, 0, 0))\n    time.sleep(0.5)\n    step(\"WaveHand\", lambda: loco.WaveHand())\n    time.sleep(4)\n    step(\"LED green — complete\", lambda: audio.LedControl(0, 255, 0))\n    time.sleep(1)\n    step(\"TTS — announce complete\", lambda: audio.TtsMaker(\"Capstone complete.\", 1))\n    time.sleep(3)\n    step(\"LED off — reset\", lambda: audio.LedControl(0, 0, 0))\n    print(\"[CAPSTONE COMPLETE]\")\n    for name, rc in log:\n        print(f\"  {name:40s} rc={rc}\")\n\nif __name__ == \"__main__\":\n    main(sys.argv[1])" }
      ]
    }
  ]
};

// Transform syllabus object
existing["04"] = day04;
existing["05"] = day05;
existing["06"] = day06;
existing["07"] = day07;

writeFileSync('client/src/data/syllabus.json', JSON.stringify(existing, null, 2));
console.log('Days 04-07 appended. Syllabus.json is now complete.');
console.log('Day 04:', day04.slides.length, 'slides | Day 05:', day05.slides.length, 'slides | Day 06:', day06.slides.length, 'slides | Day 07:', day07.slides.length, 'slides');