import { readFileSync, writeFileSync } from 'fs';

// Read existing syllabus.json to preserve day 01
const existing = JSON.parse(readFileSync('client/src/data/syllabus.json', 'utf8'));

// ===== DAY 02: Go2 Autonomy & Sandbox Capstone =====
const day02 = {
  day: "02",
  title: "Go2 Autonomy, Obstacle Avoidance & Field Capstone",
  eyebrow: "GO2 INSPECTION PATROL",
  thesis: "Bounded autonomy is still autonomy when it is explicit, safe, and evidence-producing — local avoidance is not SLAM, and field robotics is an evidence discipline.",
  rules: [
    "Mark arena boundaries with cones and name the stop caller before any robot motion.",
    "Keep vx ≤ 0.25 m/s and dx ≤ 0.5 m unless instructor explicitly approves otherwise.",
    "Enable obstacle avoidance and API command source before any patrol leg; always clean-shutdown with zero motion, release, and disable."
  ],
  pacing: [
    { time: "00:00 – 00:35", session: "Day 1 Recap & Inspection Architecture", path: "course/day-02/lab-00/" },
    { time: "00:35 – 01:00", session: "Readiness, Scenario Definition & Safety Rules", path: "course/day-02/lab-00/" },
    { time: "01:00 – 01:30", session: "Run-Folder Schema & Bundle Validation", path: "course/day-02/lab-01/" },
    { time: "01:30 – 01:40", session: "Break — Reset Attention", path: "course/day-02/" },
    { time: "01:40 – 02:10", session: "ObstacleAvoidClient & Local Motion APIs", path: "course/day-02/lab-04/" },
    { time: "02:10 – 02:35", session: "Multi-Leg Patrol & Integrated Capture Runner", path: "course/day-02/lab-05/" },
    { time: "02:35 – 02:50", session: "Gazebo/ROS 2 Context & Simulation Contrast", path: "course/day-02/lab-03/" },
    { time: "02:50 – 03:00", session: "Field Trial Tuning, Capstone & Knowledge Check", path: "course/day-02/lab-06/ & lab-07/" }
  ],
  slides: [
    {
      title: "Day 2 Learning Outcomes",
      thesis: "By end of lecture, students can describe the full inspection patrol pipeline.",
      board_type: "table",
      board_data: {
        headers: ["Outcome Area", "Competency", "Evidence"],
        rows: [
          ["System Architecture", "Explain DDS/RPC control path to Go2", "Draw PC → DDS/RPC → Go2 → run folder"],
          ["Inspection Data", "Why metadata, plan, JSONL, images are separate", "Validate or diagnose a run folder"],
          ["Motion Semantics", "Difference between velocity streaming and increment goals", "Read a leg entry and predict robot behaviour"],
          ["Safety & Limits", "Why speeds, increments, cones, spotters required", "Name abort conditions before touching hardware"],
          ["Autonomy Boundaries", "Why Day 2 patrol ≠ GPS, map-navigation, or full SLAM", "Distinguish local avoidance from mapping/localization"]
        ]
      },
      bottom_band: "Always validate the run folder schema before declaring a patrol 'complete' — structural integrity is the first checkpoint."
    },
    {
      title: "Three-Hour Teaching Plan",
      thesis: "Compress the full-day arc into a concept-rich lecture with guided code walkthroughs.",
      board_type: "table",
      board_data: {
        headers: ["Time", "Segment", "Teaching Objective"],
        rows: [
          ["00:00–00:15", "Day 1 Recap & Day 2 Framing", "Connect Day 1 topics to patrol autonomy"],
          ["00:15–00:35", "Inspection Architecture", "Introduce sense → log → decide → act → report"],
          ["00:35–01:00", "Readiness, Scenario & Safety", "Explain my_team_scenario.json, limits, abort rules"],
          ["01:00–01:30", "Run-Folder Schema & Validation", "Treat the run folder as the inspection deliverable"],
          ["01:40–02:10", "Obstacle Avoidance & Motion APIs", "Teach ObstaclesAvoidClient lifecycle, Move, MoveToIncrementPosition"],
          ["02:10–02:35", "Multi-Leg Patrol & Capture", "Walk through patrol plan execution and lab03_patrol_runner.py"],
          ["02:35–02:50", "Gazebo & ROS 2 Context", "Contrast simulation /cmd_vel with hardware SDK clients"],
          ["02:50–03:00", "Field Trial, Tuning & Capstone", "Close with tuning/reporting and presentation expectations"]
        ]
      },
      bottom_band: "Never confuse a successful single command with a valid inspection patrol — a run is only complete when evidence validates."
    },
    {
      title: "What Inspection Autonomy Means on Day 2",
      thesis: "An inspection patrol is a scripted, evidence-producing mission where checkpoints, legs, limits, captures, logs, and reports are explicit before the robot moves.",
      board_type: "table",
      board_data: {
        headers: ["Term", "General Robotics Meaning", "Day 2 Meaning"],
        rows: [
          ["Reactive Obstacle Avoidance", "Robot responds locally to nearby obstacles", "Used directly through ObstaclesAvoidClient"],
          ["Open-Loop Patrol", "Sequence executed without closed-loop semantic correction", "Default Day 2 model: legs from patrol_plan.json"],
          ["SLAM", "Simultaneous mapping and localization", "Conceptual background — not core Python patrol"],
          ["Navigation Stack", "Map, localization, planner, controller, behaviours", "Mentioned to explain what Day 2 is not yet doing"],
          ["Inspection Evidence", "Data proving what was run and what was seen", "The run folder: metadata, plan, JSONL state, images, field report"]
        ]
      },
      bottom_band: "Use precise vocabulary: 'local increment patrol under obstacle avoidance' — never claim SLAM or GPS navigation without the actual mapping stack."
    },
    {
      title: "Day 1 Primitives → Day 2 Reuse",
      thesis: "Day 1 capabilities are the building blocks of Day 2 patrol — nothing is thrown away.",
      board_type: "table",
      board_data: {
        headers: ["Day 1 Capability", "Day 2 Reuse", "Why It Matters"],
        rows: [
          ["DDS Topic Subscription", "sportmodestate.jsonl during patrol", "Reconstruct motion state and error codes"],
          ["Sport State & Posture Checks", "Stand preparation before patrol", "Never enter avoid/patrol from unsafe posture"],
          ["Single Checkpoint Capture", "checkpoints/<id>/frame.jpg", "Visual evidence tied to patrol plan"],
          ["Obstacle Avoidance Preview", "Increment and velocity patrol legs", "Move from one short motion to planned sequence"],
          ["Clean Shutdown Habits", "Patrol cleanup on success, failure, Ctrl+C", "Robot must always stop and release API control"]
        ]
      },
      bottom_band: "If a team did not pass Day 1 motion on hardware, they should do schema/validation/simulation work — real movement waits until readiness is restored."
    },
    {
      title: "Inspection Pipeline: Sense → Log → Decide → Act → Report",
      thesis: "The pipeline makes inspection autonomy auditable — every stage has a Day 2 implementation and a question students should answer.",
      board_type: "table",
      board_data: {
        headers: ["Pipeline Stage", "Day 2 Implementation", "Student Question"],
        rows: [
          ["Sense", "VideoClient, rt/sportmodestate, optional platform probe", "What did the robot see, and what state was it in?"],
          ["Log", "sportmodestate.jsonl, checkpoint frame.jpg, optional state_slice.jsonl", "Is there enough data to reconstruct the run?"],
          ["Decide", "Scenario card, speed limits, abort rules, plan legs", "Why is this motion allowed, and when should it stop?"],
          ["Act", "ObstaclesAvoidClient, increment/velocity legs", "Which API command moves the robot, and in which frame?"],
          ["Report", "metadata.json, field_test.md, validator PASS/FAIL", "What evidence proves the run was valid?"]
        ]
      },
      bottom_band: "When the robot stops short of a cone, inspect the plan, compare baseline vs tuned runs, view checkpoint images, and read JSONL state — don't just re-run."
    },
    {
      title: "Readiness & Scenario Definition",
      thesis: "Define the mission and limits first, then move the robot. The scenario file is the safety and mission contract.",
      board_type: "table",
      board_data: {
        headers: ["Scenario Field", "Lecture Explanation", "Common Mistake"],
        rows: [
          ["team_name / operator", "Identifies who owns the run and report", "Leaving metadata anonymous"],
          ["arena", "Describes physical boundaries, floor, hazards", "Treating any open space as acceptable"],
          ["checkpoints", "Names the stops where evidence is captured", "Inconsistent IDs between scenario and plan"],
          ["motion_limits", "Defines allowed vx, dx, dy, and yaw rates/angles", "Copying SDK maximums instead of class limits"],
          ["abort_rules", "States when spotter or script must halt", "Writing vague rules that cannot be acted on"],
          ["deliverables", "Defines what must be submitted", "Ending with only a terminal transcript"]
        ]
      },
      bottom_band: "Ask: 'If I hand your scenario to another team, could they understand arena, checkpoints, limits, and abort conditions without asking you?' If no, rewrite it."
    },
    {
      title: "Safety Rules for Day 2 Patrol",
      thesis: "Day 2 adds multi-stop motion — the risk is whether a sequence continues after conditions change.",
      board_type: "table",
      board_data: {
        headers: ["Rule", "Required Behaviour", "Rationale"],
        rows: [
          ["Marked Arena", "Corners marked with cones; stop caller agreed before motion", "Everyone knows the physical operating envelope"],
          ["One Patrol at a Time", "Only one team commands a Go2 on the subnet", "Prevents command confusion and network contention"],
          ["Speed Cap", "Keep vx ≤ 0.25 m/s unless approved", "Preserves reaction time and reduces impact risk"],
          ["Increment Cap", "Keep dx ≤ 0.5 m unless approved", "Prevents large open-loop jumps"],
          ["Avoid Mode Default", "Use SwitchSet(True) and UseRemoteCommandFromApi(True)", "Commands flow through avoid service"],
          ["Clean Shutdown", "Send zero motion, release API command source, disable avoid", "Avoids lingering command authority"],
          ["No SLAM Claims", "Describe increments as local, not GPS/global navigation", "Prevents false mental models"],
          ["No Acrobatics", "Exclude flips/handstands from patrol paths", "Keeps day focused on inspection safety"]
        ]
      },
      bottom_band: "Class limits are chosen for supervision, evidence quality, and repeatability — not for demonstrating the robot's maximum capability."
    },
    {
      title: "Run-Folder Schema: The Inspection Deliverable",
      thesis: "A valid run folder contains metadata, a patrol plan, a state log, and checkpoint-specific files — transforming a demo into an auditable artifact.",
      board_type: "grid",
      board_data: [
        { label: "metadata.json", value: "Run identity and artifact index: who ran what, when, on which interface, with which robot state." },
        { label: "patrol_plan.json", value: "Mission and motion definition: what was supposed to happen — checkpoints, legs, dwells." },
        { label: "sportmodestate.jsonl", value: "Time-series state evidence: line-by-line JSONL records of mode, gait, position, velocity, error codes." },
        { label: "checkpoints/<id>/frame.jpg", value: "Visual evidence at a named stop: what the camera saw at each checkpoint." },
        { label: "state_slice.jsonl", value: "Optional local context around capture: nearby state samples for detailed reconstruction." },
        { label: "field_test.md", value: "Field trial interpretation: what changed, what passed, what still needs tuning." }
      ],
      bottom_band: "Teach validation as diagnosis — intentionally validate a passing fixture AND an incomplete fixture so students learn to read structured failure messages."
    },
    {
      title: "patrol_plan.json: How a Patrol Becomes Executable",
      thesis: "The patrol plan bridges human scenario and executable robot motion — checkpoints plus legs define the mission.",
      board_type: "table",
      board_data: {
        headers: ["Leg Type", "Command Relationship", "Meaning", "Day 2 Use"],
        rows: [
          ["increment", "MoveToIncrementPosition(dx, dy, dyaw)", "Move a local body-frame increment under avoid mode", "Default multi-leg patrol"],
          ["velocity", "Repeated Move(vx, vy, vyaw) for a duration", "Stream body velocity for a fixed time", "Optional advanced tuning or comparison"],
          ["dwell / dwell_s", "Sleep at checkpoint", "Stop long enough to settle and capture", "Used before images and between legs"]
        ]
      },
      bottom_band: "Tuning dx and dyaw changes open-loop behaviour — it does NOT cause the robot to recognize or steer toward a cone."
    },
    {
      title: "Python SDK & Unitree Context",
      thesis: "Day 2 materials use the Python SDK path for Go2 inspection patrol, not a full ROS navigation stack.",
      board_type: "grid",
      board_data: [
        { label: "ChannelFactoryInitialize(0, 'en6')", value: "Initialize SDK communication on the robot-facing network interface — the interface name varies by laptop and USB Ethernet adapter." },
        { label: "SportClient", value: "Prepare posture and stop sport movement when needed — foundational for pre-motion readiness." },
        { label: "MotionSwitcherClient.CheckMode()", value: "Record current mode in metadata and readiness checks — never assume the robot is in the expected mode." },
        { label: "ObstaclesAvoidClient", value: "Enable local obstacle avoidance and execute avoid-mode motion — the central motion API for Day 2 patrol." },
        { label: "VideoClient", value: "Pull camera frames for checkpoint evidence — primary evidence sensor for inspection deliverables." },
        { label: "ChannelSubscriber('rt/sportmodestate')", value: "Subscribe to state and write JSONL logs — the robot's runtime witness throughout patrol." }
      ],
      bottom_band: "Place the PC on the 192.168.123 subnet, do NOT assign the robot address 192.168.123.161 to the PC, and test with ping before SDK diagnostics."
    },
    {
      title: "ObstaclesAvoidClient: Lifecycle & Semantics",
      thesis: "The lifecycle is as important as the motion command — safe scripts initialize, enable, command, stop, and release in a disciplined sequence.",
      board_type: "table",
      board_data: {
        headers: ["Step", "API Action", "Teaching Explanation"],
        rows: [
          ["Initialize", "Create client, set timeout, Init()", "Script must bind to robot service before commanding"],
          ["Enable Avoid", "SwitchSet(True) and verify with SwitchGet()", "Avoid mode must actually be on — never assume"],
          ["API Command Source", "UseRemoteCommandFromApi(True)", "Unitree documentation requires this for API avoid control"],
          ["Move", "Move(...) or MoveToIncrementPosition(...)", "Commands are local body-frame velocity or increment requests"],
          ["Stop", "Send repeated Move(0,0,0)", "Stop commands should be explicit and redundant"],
          ["Release", "UseRemoteCommandFromApi(False), SwitchSet(False)", "Script must not retain control after completion"],
          ["Sport Cleanup", "SportClient.StopMove() when available", "Adds another layer of stop semantics"]
        ]
      },
      bottom_band: "Success and failure paths must converge on the same safe shutdown — defensive robotics means cleanup runs in both try and except blocks."
    },
    {
      title: "Velocity vs. Increment Commands",
      thesis: "A velocity command is a stream of desired body-frame speed; an increment command asks for a bounded local displacement — they serve different purposes.",
      board_type: "table",
      board_data: {
        headers: ["Question", "Velocity Leg", "Increment Leg"],
        rows: [
          ["What is specified?", "Speed and duration", "Local displacement and yaw increment"],
          ["What API?", "Move(vx, vy, vyaw)", "MoveToIncrementPosition(dx, dy, dyaw)"],
          ["How is it sent?", "Repeated at control rate for duration", "Pulsed a few times, then allowed to settle"],
          ["Student Mental Model", "\"Walk forward slowly for 2 seconds\"", "\"Move about 0.3 m forward\""],
          ["Main Risk", "Forgetting to stop or sending too fast", "Treating local increments as global goals"]
        ]
      },
      bottom_band: "The recommended pattern avoids flooding the increment command for the entire leg window while still making it robust enough for the service to receive."
    },
    {
      title: "Sensor Capture & Inspection Evidence",
      thesis: "The primary evidence sensor is the front camera via VideoClient.GetImageSample() — state evidence comes from rt/sportmodestate.",
      board_type: "table",
      board_data: {
        headers: ["Capture Artifact", "What It Proves", "What It Does NOT Prove"],
        rows: [
          ["frame.jpg", "A visual scene was recorded at a named checkpoint", "That the robot used vision to navigate"],
          ["metadata.json capture map", "Which checkpoint IDs have captured frames", "That the physical cone was exactly reached"],
          ["state_slice.jsonl", "Nearby state samples around capture", "Full localization or mapped position"],
          ["Full sportmodestate.jsonl", "Mode, gait, error code, velocity over time", "Semantic understanding of the environment"]
        ]
      },
      bottom_band: "Ask: 'What can an inspector learn from the image that JSONL alone cannot provide?' — obstacles, lighting, scene mismatch, wrong room, human safety issues."
    },
    {
      title: "Integrated Patrol Runner Pipeline",
      thesis: "The runner shows why Day 2 is more than motion — capture, validation, clamping, and metadata are part of the same pipeline.",
      board_type: "list",
      board_data: [
        "Load scenario + plan: Load, validate, and clamp motion limits against class safety caps.",
        "Create run directory: Timestamped run folder becomes the evidence container.",
        "Initialize clients: Sport, avoid, video, and state logging clients bind to robot services.",
        "Stand + balance: Prepare robot posture — never enter patrol from unsafe state.",
        "Start state logger: Begin sportmodestate.jsonl streaming before any motion.",
        "Capture cp_A: Starting checkpoint evidence before first leg.",
        "Enable avoid + API command source: Transfer control to script under obstacle avoidance.",
        "Execute legs → dwell → capture: For each leg, move, wait, capture at to_checkpoint.",
        "Release avoid + stop logger: Converge on safe shutdown regardless of outcome.",
        "Write metadata + validate: Produce metadata.json and run validator as final gate."
      ],
      bottom_band: "If capture fails but motion succeeds, the run is a partial outcome. If validation fails, the demo is not yet a valid deliverable."
    },
    {
      title: "Field Trial & Tuning",
      thesis: "The tuning loop is observe → tune → trial → report — plan adjustments are open-loop calibration, not camera-based steering.",
      board_type: "table",
      board_data: {
        headers: ["Observation", "Likely Tuning Action", "Report Language"],
        rows: [
          ["Robot stops short of cone B", "Increase dx slightly or increase --leg-wait", "\"Baseline under-reached cp_B; tuned leg 1 distance\""],
          ["Robot overshoots near wall", "Decrease final dx", "\"Reduced final forward increment to preserve wall clearance\""],
          ["Turn at B is too small", "Increase turn-leg dyaw", "\"Increased yaw increment to align with second corridor segment\""],
          ["Turn at B is too large", "Decrease dyaw", "\"Reduced yaw increment after over-rotation\""],
          ["Capture is blurry", "Increase dwell or capture wait", "\"Added settling time before checkpoint image\""]
        ]
      },
      bottom_band: "A strong field-trial report compares baseline vs tuned runs, lists outcomes as pass/partial/fail, and states one next change — never claim success just because the robot moved."
    },
    {
      title: "Gazebo & ROS 2 Context (Optional)",
      thesis: "Simulation helps understand timing, topic flow, and movement concepts — but it does not remove the need for hardware readiness.",
      board_type: "table",
      board_data: {
        headers: ["Aspect", "Gazebo Extension", "Physical Go2 Patrol"],
        rows: [
          ["Main Interface", "ROS 2 topic /cmd_vel with geometry_msgs/Twist", "Python SDK clients such as ObstaclesAvoidClient"],
          ["Robot Required?", "No", "Yes"],
          ["Primary Risk", "Software setup, display, ROS environment", "Physical motion and field safety"],
          ["Evidence", "Topic list, simulation screenshot, short motion result", "Valid run_* folder with images and state logs"],
          ["Lecture Message", "\"Simulation helps reason before field deployment\"", "\"Hardware requires conservative execution and evidence\""]
        ]
      },
      bottom_band: "Simulation reduces uncertainty but does not eliminate field safety requirements — spotters, cones, speed limits, and cleanup still govern hardware."
    },
    {
      title: "SLAM & Navigation: What to Claim and Not Claim",
      thesis: "Unitree's SLAM docs require EDU robot dogs with expansion dock and official lidar — Day 2 Python patrol does NOT automatically become SLAM.",
      board_type: "table",
      board_data: {
        headers: ["Claim", "Acceptable?", "Correction"],
        rows: [
          ["\"Robot executed a local increment patrol under obstacle avoidance\"", "Yes", "Accurately describes Day 2 Python workflow"],
          ["\"Camera captured evidence at checkpoints\"", "Yes", "Exactly what VideoClient contributes"],
          ["\"Robot used camera to steer to colored cones\"", "No", "Camera records evidence; it does not steer in this lab"],
          ["\"Patrol used GPS navigation\"", "No", "Increments are local body-frame commands, not GPS goals"],
          ["\"This is full SLAM\"", "No", "SLAM requires mapping/localization services not used in main Python patrol"],
          ["\"Simulation used ROS 2 /cmd_vel; hardware used SDK clients\"", "Yes", "Correct sim/hardware contrast"]
        ]
      },
      bottom_band: "Say: 'Our Day 2 patrol used a local obstacle-avoidance service and scripted increments from patrol_plan.json.' Never say: 'The robot mapped the room.'"
    },
    {
      title: "Capstone Presentation Expectations",
      thesis: "A strong team presentation links scenario, architecture, evidence, and one failure/fix — not just a moving robot.",
      board_type: "list",
      board_data: [
        "Scenario: Arena map, checkpoints, limits, abort rules — the team understands bounded operation.",
        "Architecture: PC, DDS/RPC, clients, robot, run folder — the team can explain data and control flow.",
        "Plan: patrol_plan.json legs and dwell times — the team distinguishes increments from global goals.",
        "Evidence: run_* folder, frame, JSONL sample, validator output — the team values evidence over anecdote.",
        "Failure & Fix: Tuning note, abort condition, or capture issue — the team can reason like field engineers."
      ],
      bottom_band: "Open the run folder live, show at least one checkpoint frame, report validator status, and explain ONE tuning or abort lesson — 5 minutes max."
    },
    {
      title: "Instructor Demo Script for 3-Hour Lecture",
      thesis: "Emphasize reading, prediction, and diagnosis before motion.",
      board_type: "table",
      board_data: {
        headers: ["Demo", "Command or Artifact", "Instructor Narration"],
        rows: [
          ["Readiness Dry-Run", "python lab00_day2_readiness.py", "\"Before motion, verify the machine and imports\""],
          ["Scenario Creation", "--write-scenario my_team_scenario.json", "\"This is the mission and safety contract\""],
          ["Scenario Validation", "--validate-scenario my_team_scenario.json", "\"Invalid mission definitions should fail early\""],
          ["Validate Good Fixture", "lab01_validate_run_folder.py ...sample_run_pass", "\"This is what valid evidence looks like\""],
          ["Validate Bad Fixture", "lab01_validate_run_folder.py ...sample_run_incomplete", "\"Use errors as a repair checklist\""],
          ["Avoid Dry-Run", "lab04_obstacle_avoid_intro.py en6 --dry-run", "\"Dry-run before physical motion\""],
          ["Field Tuning", "lab04_tune_plan.py ... --set 1:dyaw:0.7", "\"Tuning is documented plan editing\""],
          ["Final Validation", "lab01_validate_run_folder.py run_*", "\"A run is not complete until evidence validates\""]
        ]
      },
      bottom_band: "Every demo should end with: 'What did we prove? What did we NOT prove? What evidence would make this run auditable?'"
    },
    {
      title: "Common Misconceptions & Corrections",
      thesis: "Precise vocabulary prevents unsafe assumptions — separate command execution, local avoidance, evidence capture, and navigation intelligence.",
      board_type: "table",
      board_data: {
        headers: ["Misconception", "Why It's Wrong", "Correct Mental Model"],
        rows: [
          ["\"Obstacle avoidance = autonomy\"", "Avoidance is local/reactive; it does not define mission goals", "Autonomy requires goal definition, evidence, decision logic, and safety rules"],
          ["\"Checkpoint image = vision guided robot\"", "Image captured after stopping; not used for steering", "Vision is evidence capture in the main Day 2 labs"],
          ["\"Larger dx finishes faster = better\"", "Larger increments reduce supervision margin and increase open-loop error", "Use small increments and tune from evidence"],
          ["\"Terminal says PASS = complete\"", "Run folder may still lack useful evidence or field interpretation", "PASS is necessary but not sufficient; inspect artifacts"],
          ["\"Gazebo success = hardware safe\"", "Simulation omits many physical risks", "Sim reduces uncertainty; field rules still govern hardware"],
          ["\"SLAM = any robot movement with sensors\"", "SLAM specifically involves mapping and localization", "Day 2 mainly uses local avoidance and open-loop plans"]
        ]
      },
      bottom_band: "Correct misconceptions gently but firmly — a student who says 'the robot navigated to the cone' needs to learn the precise language of local increment patrol."
    },
    {
      title: "Knowledge Check — Day 2",
      thesis: "Students answer in complete sentences — conceptual precision matters more than command memorization.",
      board_type: "list",
      board_data: [
        "What are the five stages of the Day 2 inspection architecture? — Sense, log, decide, act, report.",
        "Why does patrol_plan.json exist separately from metadata.json? — Plan defines intended checkpoints/legs; metadata records run identity, environment, mode, and artifacts.",
        "What must happen before ObstaclesAvoidClient.Move() can control avoid-mode movement? — Avoidance enabled AND UseRemoteCommandFromApi(True) set.",
        "Why should Move() be sent repeatedly for velocity motion? — It represents a velocity stream over time, not a complete path by itself.",
        "What is the difference between leg-wait and checkpoint dwell? — leg-wait allows increment motion to settle; dwell is stop time at checkpoint before capture or next action.",
        "Why is Day 2 patrol not SLAM patrol? — It does not build/use a global map and localize to global goals; it executes local scripted increments under avoidance.",
        "What evidence should a team show in capstone? — Scenario, architecture, plan, valid run folder or recording, checkpoint image, validator status, and one failure/fix."
      ],
      bottom_band: "Before answering any knowledge check, pause and check: is the robot stationary, is the run folder open, and can I point to the artifact that proves my answer?"
    },
    {
      title: "Closing Summary — Three Principles",
      thesis: "Bounded autonomy is still autonomy when explicit, safe, and evidence-producing. Local avoidance is not SLAM. Field robotics is an evidence discipline.",
      board_type: "grid",
      board_data: [
        { label: "1. Bounded Autonomy", value: "When checkpoints, limits, captures, logs, and reports are explicit before the robot moves, the mission is auditable — that IS autonomy." },
        { label: "2. Vocabulary Discipline", value: "Use accurate language: 'local increment patrol under obstacle avoidance,' not 'GPS navigation' or 'SLAM patrol.' Words shape safety expectations." },
        { label: "3. Evidence Discipline", value: "If a patrol cannot be reconstructed from its plan, logs, images, metadata, and report, then the team has not completed an inspection mission." }
      ],
      bottom_band: "The robot does not simply execute commands — it operates inside a scenario, with safety limits, a plan, state logs, camera evidence, validation, tuning, and reporting."
    }
  ],
  labs: [
    {
      id: "lab-00",
      title: "Day 2 Readiness & Inspection Scenario",
      content: "Confirm Day 1 artifacts exist, patrol-related SDK imports are available, network/DDS readiness is acceptable, and a patrol scenario has been written and validated before motion begins.\n\n- Verify Python SDK imports and network connectivity\n- Write and validate my_team_scenario.json\n- Confirm ObstaclesAvoidClient, SportClient, VideoClient are importable\n- Record interface name and complete safety briefing",
      code_files: [
        { name: "lab00_day2_readiness.py", code: "#!/usr/bin/env python3\n\"\"\"Day 2 Readiness — verify SDK imports, network, and scenario.\"\"\"\nimport sys\nfrom unitree_sdk2py.core.channel import ChannelFactoryInitialize\nfrom unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_\nfrom unitree_sdk2py.go2.sport.sport_client import SportClient\nfrom unitree_sdk2py.go2.video.video_client import VideoClient\nfrom unitree_sdk2py.go2.obstacles_avoid.obstacles_avoid_client import ObstaclesAvoidClient\n\ndef main(interface: str):\n    print(f\"[READINESS] Testing imports on {interface}...\")\n    print(\"[PASS] SDK imports verified\")\n    print(\"[READY] Proceed to scenario creation or Lab 1\")\n\nif __name__ == \"__main__\":\n    main(sys.argv[1] if len(sys.argv) > 1 else \"en6\")" }
      ]
    },
    {
      id: "lab-01",
      title: "Run Folder Schema & Bundle Validation",
      content: "Learn the structure of a valid inspection run folder. Validate a passing fixture and an incomplete fixture to understand structured failure messages.\n\n- Inspect sample_run_pass/ and sample_run_incomplete/ fixtures\n- Run lab01_validate_run_folder.py against both\n- Interpret PASS, PASS-with-warning, and FAIL output\n- Explain why each required file matters to an inspector",
      code_files: [
        { name: "validate_schema.py", code: "\"\"\"Run folder validator — checks structural completeness.\"\"\"\nimport json, os, sys\n\ndef validate_run_folder(path: str) -> dict:\n    issues = []\n    for required in [\"metadata.json\", \"patrol_plan.json\", \"sportmodestate.jsonl\"]:\n        if not os.path.exists(os.path.join(path, required)):\n            issues.append(f\"missing file: {required}\")\n    # Validate metadata fields\n    meta_path = os.path.join(path, \"metadata.json\")\n    if os.path.exists(meta_path):\n        meta = json.load(open(meta_path))\n        for field in [\"schema_version\", \"created_utc\", \"operator\"]:\n            if field not in meta:\n                issues.append(f\"metadata.json: missing '{field}'\")\n    # Validate checkpoint directories\n    plan_path = os.path.join(path, \"patrol_plan.json\")\n    if os.path.exists(plan_path):\n        plan = json.load(open(plan_path))\n        for cp in plan.get(\"checkpoints\", []):\n            cp_dir = os.path.join(path, \"checkpoints\", cp[\"id\"])\n            frame = os.path.join(cp_dir, \"frame.jpg\")\n            if not os.path.exists(frame):\n                issues.append(f\"checkpoints/{cp['id']}/frame.jpg missing\")\n    return {\"status\": \"PASS\" if not issues else \"FAIL\", \"issues\": issues}\n\nif __name__ == \"__main__\":\n    result = validate_run_folder(sys.argv[1])\n    print(json.dumps(result, indent=2))" }
      ]
    },
    {
      id: "lab-02",
      title: "Obstacle Avoidance & Multi-Leg Increment Patrol",
      content: "Use ObstaclesAvoidClient to execute multi-leg patrol with increment and velocity commands. Practice the enable → move → stop → release lifecycle.\n\n- Implement enable_avoid() and release_avoid() helper functions\n- Execute a default L-shaped course: cp_A → forward → cp_B → turn → forward → cp_C\n- Compare velocity-leg and increment-leg behaviour\n- Practice dry-run mode before physical motion",
      code_files: [
        { name: "go2_patrol_helpers.py", code: "\"\"\"Day 2 patrol helpers — shared enable/disable and leg execution.\"\"\"\nimport time\n\ndef enable_avoid(avoid_client):\n    avoid_client.SwitchSet(True)\n    time.sleep(0.5)\n    if not avoid_client.SwitchGet():\n        raise RuntimeError(\"ObstacleAvoidClient.SwitchGet() returned False\")\n    avoid_client.UseRemoteCommandFromApi(True)\n    print(\"[AVOID] Enabled and API command source transferred\")\n\ndef release_avoid(avoid_client, sport_client=None):\n    for _ in range(5):\n        avoid_client.Move(0.0, 0.0, 0.0)\n        time.sleep(0.05)\n    avoid_client.UseRemoteCommandFromApi(False)\n    avoid_client.SwitchSet(False)\n    if sport_client:\n        sport_client.StopMove()\n    print(\"[AVOID] Released and command authority returned\")\n\ndef run_increment_leg(avoid_client, dx, dy, dyaw, pulses=3):\n    for _ in range(pulses):\n        avoid_client.MoveToIncrementPosition(dx, dy, dyaw)\n        time.sleep(0.2)\n    print(f\"[LEG] Increment: dx={dx}, dy={dy}, dyaw={dyaw}\")\n\ndef run_velocity_leg(avoid_client, vx, vy, vyaw, duration_s):\n    start = time.time()\n    while time.time() - start < duration_s:\n        avoid_client.Move(vx, vy, vyaw)\n        time.sleep(0.05)\n    print(f\"[LEG] Velocity: vx={vx}, vy={vy}, vyaw={vyaw}, t={duration_s}s\")" }
      ]
    },
    {
      id: "lab-03",
      title: "Integrated Patrol Runner & Checkpoint Capture",
      content: "Run the full integrated patrol pipeline: load scenario, create run folder, initialize clients, stand, capture checkpoints, execute legs, release, and validate.\n\n- Load and clamp patrol plan against scenario limits\n- Create timestamped run folder\n- Initialize sport, avoid, video, and state logging clients\n- Execute all plan legs with dwell and checkpoint capture\n- Write metadata.json and run validator",
      code_files: [] },
    {
      id: "lab-04",
      title: "Field Trial & Tuning Lab",
      content: "Convert observations into controlled plan changes using the observe → tune → trial → report loop.\n\n- Copy baseline plan and apply leg overrides with lab04_tune_plan.py\n- Run the tuned plan through the integrated runner\n- Write field_test.md comparing baseline and tuned run folders\n- List checkpoint outcomes as pass/partial/fail",
      code_files: [] },
    {
      id: "lab-05",
      title: "Gazebo Simulation Extension",
      content: "Optional: Launch Gazebo simulation, publish /cmd_vel Twist messages, and contrast the ROS 2 simulation interface with hardware SDK clients.\n\n- Launch Go2 Gazebo simulation\n- Publish geometry_msgs/Twist to /cmd_vel\n- Observe simulated sensor topics\n- Write a comparison note: sim vs hardware interfaces",
      code_files: [] },
    {
      id: "lab-06",
      title: "Team Capstone & Presentation Prep",
      content: "Prepare a 5-minute demo linking scenario, architecture, evidence, and one failure/fix. Present the run folder, checkpoint image, validator status, and tuning lesson.\n\n- Collect scenario, architecture diagram, plan, and evidence\n- Identify one tuning or abort lesson\n- Practice presenting the run folder live\n- Answer knowledge check questions as a team",
      code_files: [] }
  ]
};

// ===== DAY 03: B2 Industrial Fundamentals =====
const day03 = {
  day: "03",
  title: "B2 Industrial Fundamentals",
  eyebrow: "B2 HEAVY-DUTY QUADRUPED",
  thesis: "A B2 operator should never begin with motion — a competent operator first proves network readiness, observes state, explains the control layer, identifies the safe stop path, and only then executes a supervised motion primitive.",
  rules: [
    "First prove interface, environment, DDS, state visibility, and safety perimeter before any motion — observation precedes command.",
    "Only approved commands may run under instructor gate — initial commands are BalanceStand and StopMove; Damp is an emergency state, not a casual stop.",
    "Never hot-swap aviation plug interfaces — treat all cabling and interface handling as part of the safety protocol."
  ],
  pacing: [
    { time: "00:00 – 00:15", session: "Opening Safety Frame — B2 as Industrial Robot", path: "course/day-03/lab-00/" },
    { time: "00:15 – 00:40", session: "B2 Hardware & Industrial Context", path: "course/day-03/" },
    { time: "00:40 – 01:05", session: "B2 Network & SDK Readiness", path: "course/day-03/lab-00/" },
    { time: "01:05 – 01:30", session: "Lab 1 — Subscribe to SportModeState", path: "course/day-03/lab-01/" },
    { time: "01:30 – 01:40", session: "Break & Safety Reset", path: "course/day-03/" },
    { time: "01:40 – 02:10", session: "High-Level SportClient Control & Command Semantics", path: "course/day-03/lab-02/" },
    { time: "02:10 – 02:35", session: "Supervised Lab 2 Motion Gate — BalanceStand & StopMove", path: "course/day-03/lab-02/" },
    { time: "02:35 – 03:00", session: "Navigation, Perception Bridge & Knowledge Check", path: "course/day-03/" }
  ],
  slides: [
    {
      title: "Teaching Thesis — Transition to Industrial Scale",
      thesis: "Day 3 is the transition point from education-scale quadruped control to industrial-scale quadruped readiness — B2 is heavier, stronger, higher-payload, and more operationally consequential.",
      board_type: "grid",
      board_data: [
        { label: "Platform Framing", value: "Industrial quadruped for inspection, payload, endurance, and field deployment — not merely a larger Go2." },
        { label: "First Proof of Readiness", value: "Can the team prove interface, environment, DDS, state visibility, and safety perimeter before motion?" },
        { label: "Motion Philosophy", value: "Instructor-gated command sequence with explicit stop and recovery path — never exploratory experimentation." },
        { label: "Student Success Evidence", value: "Safe diagnosis, correct interpretation of state, conservative operation, and clean stop discipline." },
        { label: "Instructor Role", value: "Safety authority, run director, and escalation controller — not merely an API guide." }
      ],
      bottom_band: "The API similarity between Go2 and B2 is helpful for learning but dangerous if it hides the physical difference — a Move(0.5,0,0) on a 60 kg robot is not the same."
    },
    {
      title: "B2 as an Industrial Platform",
      thesis: "B2 specifications — 60 kg, >6 m/s, 360 N·m torque, 120 kg standing load — explain why the training protocol must be conservative.",
      board_type: "table",
      board_data: {
        headers: ["B2 Attribute", "Specification", "Classroom Implication"],
        rows: [
          ["Robot Mass", "~60 kg including battery", "Industrial inertia — motion is a controlled demonstration, not exploration"],
          ["Walking Load", ">40 kg", "Payload changes balance, clearance, current draw, and fall risk"],
          ["Max Speed", ">6 m/s (safety-limited)", "Far more kinetic capability than needed for training — use low-speed primitives only"],
          ["Battery Life", "4–6 hours", "Extended deployment design — teach battery/thermal checks as field-readiness evidence"],
          ["IP Rating", "IP67", "Harsh environment design — rating is not permission for risky classroom operation"],
          ["Sensing", "3D LiDAR, depth cameras, optical cameras", "Perception supports inspection, mapping, and analytics — preview for Day 4"]
        ]
      },
      bottom_band: "When introducing B2 specs, always pair each number with the safety implication — speed, mass, and payload numbers without context create dangerous overconfidence."
    },
    {
      title: "B2 Safety Model for Training",
      thesis: "The first successful action is proving that the robot, operator, network, and safety perimeter are all in a known state — not walking.",
      board_type: "table",
      board_data: {
        headers: ["Safety Gate", "Required Evidence", "Instructor Response If Missing"],
        rows: [
          ["Physical Perimeter", "Clear floor, no loose cables, nobody in motion zone", "Do not run Lab 2 motion"],
          ["Stop Authority", "Named instructor controls motion; operator has keyboard focus", "Pause and re-brief"],
          ["Interface Identity", "Students state active interface (eth0, enp3s0, etc.)", "Do not run scripts with guessed interfaces"],
          ["Environment Readiness", "SDK env activated, expected variables available", "Fix environment before robot interaction"],
          ["State Observability", "SportModeState prints ≥30s without DDS errors", "Do not proceed to motion"],
          ["Command Scope", "Only approved commands — BalanceStand and StopMove initially", "Stop session if unapproved motion attempted"]
        ]
      },
      bottom_band: "Distinguish routine stop (StopMove), motion stop (StopMove), and emergency stop (Damp) — teach students when each applies and what physical response to expect."
    },
    {
      title: "B2 System Architecture: Wire to Motion",
      thesis: "Students must know which layer they are touching — physical Ethernet, DDS, state topic, high-level RPC, or low-level command.",
      board_type: "table",
      board_data: {
        headers: ["Layer", "What Students See", "Day 3 Meaning"],
        rows: [
          ["Physical Ethernet", "Cable, interface name, static network", "Must know which interface connects to robot"],
          ["DDS Communication", "ChannelFactoryInitialize(0, interface)", "Process joins robot communication domain"],
          ["State Topic", "rt/sportmodestate", "Robot publishes high-level motion state — observe before motion"],
          ["High-Level RPC", "SportClient() calls: BalanceStand(), StopMove()", "SDK sends semantic motion requests through safety-managed layer"],
          ["Low-Level Command", "rt/lowcmd and rt/lowstate", "Script commands individual motor targets — requires stronger expertise"],
          ["Perception/Video", "Camera clients and RTSP streams", "B2 provides inspection data for Day 4 analytics"]
        ]
      },
      bottom_band: "Control authority is not binary — SportClient asks for behavior, LowCmd publishing tells individual motors what to do. These are different risk levels."
    },
    {
      title: "Lab 0: B2 Readiness & Safety (No-Motion)",
      thesis: "Readiness checks prevent false diagnoses — a failed motion script could be network, environment, DDS, robot state, firmware, or safety lock.",
      board_type: "table",
      board_data: {
        headers: ["Lab 0 Check", "Command or Action", "Success Looks Like"],
        rows: [
          ["Repository Location", "cd \"$(git rev-parse --show-toplevel)\"", "Terminal at course repo root"],
          ["SDK Environment", "conda activate unitree_env", "Expected Python and SDK packages available"],
          ["Interface Discovery", "ip link or ifconfig", "Students identify wired robot interface"],
          ["Script Location", "ls scripts/ives_sdk/B2/", "B2 scripts visible: subscribe_sport_mode_state.py, b2_sport_client.py"],
          ["Safety Briefing", "Instructor-led", "Students state perimeter, stop command, and approval rule"]
        ]
      },
      bottom_band: "Frame Lab 0 as operator certification: 'Which interface? Which environment? Which script observes state? Which moves the robot? Who has stop authority?'"
    },
    {
      title: "Lab 1: Subscribe to B2 SportModeState",
      thesis: "Lab 1 is the first proof that workstation, network, DDS, SDK imports, robot topic publication, and callback flow work together.",
      board_type: "grid",
      board_data: [
        { label: "Position", value: "Indicates estimated robot pose or motion-state position — should remain stable when stationary." },
        { label: "Velocity", value: "Reveals whether robot believes it is moving — should be near zero before motion." },
        { label: "IMU State", value: "Body orientation and inertial sensing — what would a tilted or unstable robot look like?" },
        { label: "Mode", value: "High-level motion mode (idle, balance stand, locomotion, damping, recovery, sit) — expected before/after BalanceStand." },
        { label: "Gait Type", value: "Gait category when locomotion is active — should gait change during a no-motion readiness check?" },
        { label: "Foot Force & Position", value: "Contact/support diagnosis and leg geometry relative to body — why relevant before low-level control." }
      ],
      bottom_band: "If state does not arrive cleanly for 30 seconds, do not proceed to motion — verify interface, cable, robot power, DDS environment, and topic binding first."
    },
    {
      title: "High-Level SportClient Commands",
      thesis: "The menu is a code artifact; the instructor gate is the operational authority — presence of a menu option does not imply permission.",
      board_type: "table",
      board_data: {
        headers: ["Command", "Teaching Meaning", "Day 3 Status"],
        rows: [
          ["BalanceStand()", "Enter balanced standing behavior", "Instructor-approved demonstration"],
          ["StopMove()", "Stop current motion, restore parameters", "Required stop command — know before motion"],
          ["Damp()", "High-priority damping state", "Emergency-related — instructor policy only"],
          ["StandUp() / StandDown()", "Locked standing/lying posture", "Instructor-only unless approved"],
          ["RecoveryStand()", "Recover from fallen/lying to standing", "Instructor-only; important conceptually"],
          ["Move(vx,vy,vyaw)", "Body-frame velocity command", "Not for first motion without explicit approval"],
          ["ClassicWalk() / FreeWalk()", "Gait-related walking modes", "Not for first 3-hour session unless conditions excellent"],
          ["MoveToPos() / TrajectoryFollow()", "Targeted position / path following", "Discuss but do not execute in basic Day 3"]
        ]
      },
      bottom_band: "Unitree docs warn: Move commands are NOT filtered by the motion-control part — the latest Move is held for 1 second. Always send Move(0,0,0) or StopMove() when stopping."
    },
    {
      title: "Lab 2: Supervised B2 Sport RPC & Stand",
      thesis: "The first motion lab — BalanceStand and StopMove only, under strict instructor-gated sequence.",
      board_type: "list",
      board_data: [
        "Step 1: Reconfirm no people/objects in motion zone — students visually inspect and verbally confirm.",
        "Step 2: Confirm one operator has terminal focus — students do NOT type commands independently.",
        "Step 3: Start b2_sport_client.py with verified interface — students see warning and menu prompt.",
        "Step 4: Use BalanceStand only after instructor approval — observe posture transition and state change.",
        "Step 5: Use StopMove — observe stable stopping behavior and discuss return code meaning.",
        "Step 6: Stop the demonstration — students record commands executed and any anomalies observed."
      ],
      bottom_band: "A return code of 0 means the service accepted the request — it does NOT prove the physical motion was safe, complete, or visually correct. The robot body is the final source of truth."
    },
    {
      title: "Low-Level Control: b2_stand_example.py",
      thesis: "LowCmd publishing at 500 Hz is not 'cooler' than SportClient — it removes abstraction and increases responsibility.",
      board_type: "table",
      board_data: {
        headers: ["Code Feature", "Engineering Meaning", "Why Discuss It"],
        rows: [
          ["rt/lowcmd publisher", "Direct low-level command channel", "Shows why low-level scripts require stronger authority"],
          ["rt/lowstate subscriber", "Feedback channel for motor state", "Demonstrates closed-loop awareness even in simple example"],
          ["RecurrentThread(interval=0.002)", "500 Hz command-writing intent", "Low-level control is timing-sensitive"],
          ["Kp=1000.0, Kd=10.0", "Joint-control gains", "Stiffness and damping are explicit design choices"],
          ["Target joint arrays", "Desired leg configurations", "Joint numbering and limits matter"],
          ["CRC computation", "Message integrity check", "Robot command packets require validation"]
        ]
      },
      bottom_band: "When explaining low-level control, always state: 'This script publishes 20 motor command slots at 500 Hz — one mistyped gain or wrong joint index can cause unexpected behaviour.'"
    },
    {
      title: "B2 Sensors, Video & Inspection Bridge",
      thesis: "Inspection autonomy is data discipline — the robot's value is not only movement, but location-aware, time-aware, repeatable observations.",
      board_type: "grid",
      board_data: [
        { label: "SportModeState", value: "Day 3 readiness and robot-state observability → Day 4: correlate state with inspection events." },
        { label: "Optical Cameras", value: "Preview today → Day 4: image capture, video review, defect evidence, operator situational awareness." },
        { label: "Depth Cameras", value: "Conceptual overview → Day 4: spatial context, obstacle awareness, inspection geometry." },
        { label: "LiDAR", value: "Conceptual overview → Day 4: mapping, localization, terrain and structure context." },
        { label: "RTSP Recording", value: "Preview today → Day 4: evidence package for inspection report or analytics workflow." }
      ],
      bottom_band: "The B2 camera scripts (camera_opencv-video.py, record_rtsp.py) bridge to Day 4 — preview them now, but the primary Day 3 deliverable is state observation and safe posture control."
    },
    {
      title: "Troubleshooting Framework",
      thesis: "Move from physical layer → environment layer → communication layer → state layer → command layer — not random guesses.",
      board_type: "table",
      board_data: {
        headers: ["Symptom", "Likely Layer", "Diagnostic Path", "Safe Response"],
        rows: [
          ["Cannot import SDK", "Python environment", "Confirm conda activate unitree_env; verify SDK package", "Do not connect motion until env correct"],
          ["No state messages", "Network or DDS", "Check cable, interface, robot power, DDS config, topic name", "Stay in Lab 1; do not proceed"],
          ["DDS errors", "DDS config / interface conflict", "Verify only intended interface selected; check CycloneDDS", "Pause and fix configuration"],
          ["State prints but values unexpected", "Robot state / interpretation", "Compare stationary velocity, mode, posture, visible state", "Ask instructor before motion"],
          ["Sport command returns nonzero", "RPC or robot mode", "Record command, return code, state, visible behavior", "Stop; do not chain commands"],
          ["Unexpected motion", "Command or mode issue", "Use approved stop path; instructor takes control", "Clear perimeter; investigate after stop"]
        ]
      },
      bottom_band: "Every failure should produce a short incident note: time, command, interface, visible robot state, terminal output, action taken, and whether robot returned to safe state."
    },
    {
      title: "Student Knowledge Checks — Day 3",
      thesis: "Test readiness reasoning, not command memorization — a student who can name commands but not explain stop authority is not ready.",
      board_type: "list",
      board_data: [
        "Why does Day 3 begin with a no-motion readiness lab? — B2 motion must be preceded by network, environment, DDS, observability, and safety checks.",
        "What is the purpose of rt/sportmodestate? — High-level robot motion state used to verify readiness and interpret robot behavior.",
        "Why is BalanceStand safer as first demo than Move? — Demonstrates controlled posture without intentionally commanding translation.",
        "What should happen if subscribe_sport_mode_state.py does not print state cleanly? — Stop at diagnosis; do not proceed to motion.",
        "What is the difference between SportClient and rt/lowcmd? — High-level behavior requests versus low-level motor command streaming.",
        "Why is Move(0,0,0) or StopMove() part of command hygiene? — Velocity commands require explicit stopping; Unitree warns about hold behavior.",
        "What are the main B2 sensing channels relevant to future inspection? — LiDAR, depth cameras, optical cameras, video/RTSP, and robot state."
      ],
      bottom_band: "A student who cannot distinguish SportClient from LowCmd streaming should not teach B2 labs — this is the most important conceptual boundary in robot safety."
    },
    {
      title: "Day 3 Takeaways — Four Durable Habits",
      thesis: "B2 is powerful because it combines mobility, payload, endurance, sensing, and SDK access — those same characteristics require stronger safety habits.",
      board_type: "grid",
      board_data: [
        { label: "1. Observe Before Acting", value: "Use SportModeState as your first diagnostic window — 'If I cannot prove the interface and state channel, I do not command motion.'" },
        { label: "2. Gate Motion", value: "Through a named instructor and approved command sequence — 'The robot moves only inside an instructor-approved command envelope.'" },
        { label: "3. Know the Control Layer", value: "High-level sport commands request behavior; low-level commands stream motor targets — never confuse the two." },
        { label: "4. Treat Inspection as Data Discipline", value: "State, video, timing, and operator notes become the foundation for Day 4 analytics and auditable field inspection." }
      ],
      bottom_band: "Close Day 3 with: 'Tomorrow we will only capture what today we learned to observe, classify, and bound.' This reinforces the progression from state awareness to evidence production."
    }
  ],
  labs: [
    {
      id: "lab-00",
      title: "B2 Readiness & Safety",
      content: "No-motion lab confirming B2 network, SDK environment, CycloneDDS assumptions, and safety briefing before proceeding.\n\n- Identify network interface connected to robot\n- Activate SDK environment and verify imports\n- Confirm CycloneDDS is found\n- Run interface discovery and ping test\n- Complete instructor-led safety briefing",
      code_files: [
        { name: "b2_readiness.py", code: "#!/usr/bin/env python3\n\"\"\"B2 Readiness — import checks and interface verification.\"\"\"\nimport sys, subprocess\n\ndef check_interface(iface: str):\n    print(f\"[READINESS] Checking interface: {iface}\")\n    # SDK import check\n    try:\n        from unitree_sdk2py.core.channel import ChannelFactoryInitialize\n        from unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_\n        print(\"[PASS] SDK imports verified\")\n    except ImportError as e:\n        print(f\"[FAIL] SDK import error: {e}\")\n        return False\n    return True\n\nif __name__ == \"__main__\":\n    check_interface(sys.argv[1] if len(sys.argv) > 1 else \"eth0\")" }
      ]
    },
    {
      id: "lab-01",
      title: "Subscribe to B2 SportModeState",
      content: "First robot-observation lab. Subscribe to rt/sportmodestate and verify continuous state streaming for at least 30 seconds.\n\n- Run subscribe_sport_mode_state.py with correct interface\n- Interpret position, velocity, IMU, mode, gait_type, foot_force fields\n- Explain what each field reveals about robot readiness\n- Document state observations in lab notes",
      code_files: [
        { name: "subscribe_sport_mode_state.py", code: "\"\"\"B2 SportModeState subscriber — the pre-motion observability channel.\"\"\"\nimport sys, time\nfrom unitree_sdk2py.core.channel import ChannelFactoryInitialize, ChannelSubscriber\nfrom unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_\n\ndef callback(state: SportModeState_):\n    print(f\"mode={state.mode} gait={state.gait_type} \"\n          f\"pos=({state.position[0]:.2f},{state.position[1]:.2f},{state.position[2]:.2f}) \"\n          f\"vel=({state.velocity[0]:.2f},{state.velocity[1]:.2f},{state.velocity[2]:.2f})\")\n\nif __name__ == \"__main__\":\n    ChannelFactoryInitialize(0, sys.argv[1])\n    sub = ChannelSubscriber(\"rt/sportmodestate\", SportModeState_)\n    sub.Init(callback, 10)\n    print(f\"[STATE] Listening on {sys.argv[1]}... press Ctrl+C to stop\")\n    while True:\n        time.sleep(1)" }
      ]
    },
    {
      id: "lab-02",
      title: "Supervised B2 Sport RPC & Stand",
      content: "First motion lab under instructor gate. Use BalanceStand and StopMove through the sport client menu.\n\n- Confirm state subscription succeeded and perimeter is clear\n- Run b2_sport_client.py with verified interface\n- Execute approved sequence: BalanceStand → observe → StopMove → observe\n- Record commands, return codes, and visible robot behavior\n- Discuss the difference between SportClient and LowCmd streaming",
      code_files: [] }
  ]
};

// Helper to write output
const syllabus = { ...existing };
syllabus["02"] = day02;
syllabus["03"] = day03;

// Write partial — days 04-07 will be appended next
writeFileSync('client/src/data/syllabus.json', JSON.stringify(syllabus, null, 2));
console.log('Days 02-03 written to syllabus.json. Days 04-07 coming in part 2.');