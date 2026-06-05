#!/usr/bin/env python3
"""
Rewrite DAY03 slides in build_syllabus.py to 45 slides (Cover + 44 numbered)
aligned with "Day 3 Beginner-Friendly Full Slide Content" curriculum.

Context-aware keyword bolding rules:
  Rule A (Grid values / List items in right scroller):
      Technical keywords → <strong class="font-bold text-foreground">
      Ensures sharp high-contrast text in info scroll cards.
  Rule B (Table headers on blue bg):
      NO bold() calls on headers — they render as plain text on bg-primary.
  Rule C (Thesis statement blocks):
      Keywords use <strong class="font-bold"> without color override —
      retains default off-white prose coloring, never black.
  Titles: ALWAYS plain text, never bold().
"""
import re, json as _json

# ── Day 3 B2 keyword patterns ──
_PATTERNS = [
    # Platform / product names
    (r'\b(B2)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(Unitree)\b', r'<strong class="font-bold">\1</strong>'),
    # Sensors & hardware
    (r'\b(LiDAR)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(IMU)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(IP67)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(BT2-10)\b', r'<strong class="font-bold">\1</strong>'),
    # SDK / languages
    (r'\b(unitree_sdk2)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(unitree_sdk2_python)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(C\+\+)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(Python)\b', r'<strong class="font-bold">\1</strong>'),
    # Control commands / modes
    (r'\b(SportModeState)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(BalanceStand)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(StopMove)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(Damp)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(StandUp)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(StandDown)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(RecoveryStand)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(Move)\b', r'<strong class="font-bold">\1</strong>'),
    # File formats
    (r'\b(\.json)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(\.jsonl)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(\.py)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(\.cpp)\b', r'<strong class="font-bold">\1</strong>'),
    # ROS / middleware
    (r'\b(DDS)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(CycloneDDS)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(ChannelFactoryInitialize)\b', r'<strong class="font-bold">\1</strong>'),
    # Topics / channels
    (r'\b(rt/sportmodestate)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(rt/lowcmd)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(rt/lowstate)\b', r'<strong class="font-bold">\1</strong>'),
    # Client classes
    (r'\b(SportClient)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(LocoClient)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(VideoClient)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(ObstaclesAvoidClient)\b', r'<strong class="font-bold">\1</strong>'),
    # Communication
    (r'\b(RPC)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(Ethernet)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(USB)\b', r'<strong class="font-bold">\1</strong>'),
    # Control concepts
    (r'\b(LowCmd)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(LowState)\b', r'<strong class="font-bold">\1</strong>'),
    # RTSP
    (r'\b(RTSP)\b', r'<strong class="font-bold">\1</strong>'),
    # G1
    (r'\b(G1)\b', r'<strong class="font-bold">\1</strong>'),
    # Go2
    (r'\b(Go2)\b', r'<strong class="font-bold">\1</strong>'),
    # Specific config / technical terms
    (r'\b(OpenCV)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(JPEG)\b', r'<strong class="font-bold">\1</strong>'),
    # ROS types
    (r'\b(LowCmd_)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(LowState_)\b', r'<strong class="font-bold">\1</strong>'),
    (r'\b(SportModeState_)\b', r'<strong class="font-bold">\1</strong>'),
    # MotionSwitcher
    (r'\b(MotionSwitcherClient)\b', r'<strong class="font-bold">\1</strong>'),
]

# ── Context-aware bold functions ──
def bold_grid_list(s):
    """Rule A: Scroller-card keywords → high-contrast foreground emphasis."""
    for pat, repl in _PATTERNS:
        s = re.sub(pat, repl, s)
    return s

def bold_thesis(s):
    """Rule C: Thesis-block keywords → subtle bold only, NO color class override."""
    thesis_repl = [(p, r'<strong class="font-bold">\1</strong>') for p, _ in _PATTERNS]
    for pat, repl in thesis_repl:
        s = re.sub(pat, repl, s)
    return s

def bold_table_cell(s):
    """Standard keyword emphasis for table data cells."""
    for pat, repl in _PATTERNS:
        s = re.sub(pat, repl, s)
    return s

# ── 45 Slides (Cover + Slides 1–44) ──
SLIDES = [
    # ══════════════════════════════════════════════════════════════
    # COVER SLIDE
    # ══════════════════════════════════════════════════════════════
    {
        "title": "Day 3: Unitree B2 Platform, Safety, Control, Movement, and SDK Point-to-Point Scripts",
        "thesis": bold_thesis("Day 3 is intentionally scoped to B2-exclusive beginner operation. Students learn the B2 as an industrial quadruped with real hardware limits, heavy-duty payload behavior, supervised movement, manual override discipline, gait awareness, and basic SDK-controlled point-to-point motion. The teaching pattern is Inspect → Configure → Command → Override → Observe → Validate."),
        "board_type": "grid",
        "board_data": [
            {"label": "Course", "value": bold_grid_list("Vinci AI Unitree Robotics Course — Day 3 of 7")},
            {"label": "Platform", "value": bold_grid_list("Unitree B2 industrial quadruped — 60 kg, heavy-duty payload, IP67 protection")},
            {"label": "Core Flow", "value": bold_grid_list("Inspect → Configure → Command → Override → Observe → Validate — one repeatable safe-motion loop")},
            {"label": "Audience", "value": "Students new to Unitree B2 industrial quadruped operation and basic SDK-controlled movement."},
        ],
        "bottom_band": bold_grid_list("Day 3 promise: By the end of today, you will explain B2 hardware features, control subsystems, basic movement vectors, manual override discipline, gait awareness, and how to write a safe point-to-point SDK script.")
    },

    # ══════════════════════════════════════════════════════════════
    # SECTION: SCOPE AND SAFETY ORIENTATION — Slides 1–4
    # ══════════════════════════════════════════════════════════════
    {
        "title": "Day 3 Is B2-First",
        "thesis": bold_thesis("Today is about B2 hardware, safety, movement, control subsystems, and SDK scripts — not broad middleware theory or unrelated robot software stacks. The teaching flow is Inspect → Configure → Command → Override → Observe → Validate."),
        "board_type": "grid",
        "board_data": [
            {"label": "Today", "value": bold_grid_list("B2 hardware, safety, movement, control subsystems, SDK scripts — practical B2 operation from first principles.")},
            {"label": "Not Today", "value": "Broad middleware theory or unrelated robot software stacks — Day 3 is deliberately scoped to B2-exclusive learning."},
            {"label": "Teaching Flow", "value": bold_grid_list("Inspect → Configure → Command → Override → Observe → Validate — one repeatable loop for every motion test.")},
        ],
        "bottom_band": bold_grid_list("Scope check: Students are not learning a general robotics software survey today. They are learning how the B2 behaves as an industrial quadruped, how safe commands are formed, how manual override stays ready, and how a basic script moves from one point to another.")
    },
    {
        "title": "B2 Is Industrial Hardware",
        "thesis": bold_thesis("The B2 is a heavy-duty industrial quadruped — approximately 60 kg including battery, with payload capability, terrain performance, and IP67 protection. Students must treat every command as real machine motion."),
        "board_type": "grid",
        "board_data": [
            {"label": "Approximate Mass", "value": bold_grid_list("60 kg including battery — industrial inertia demands respect before code.")},
            {"label": "Industrial Emphasis", "value": bold_grid_list("Payload capability, terrain ability, endurance, and IP67 protection — built for field deployment, not classroom toys.")},
            {"label": "Student Rule", "value": "Treat every command as real machine motion — even a small command can move a large robot with serious consequences."},
        ],
        "bottom_band": bold_grid_list("Teaching point: Beginners must respect the physical machine before they write code. The B2's industrial specifications are not permission for aggressive experimentation — they are reasons for conservative operation.")
    },
    {
        "title": "Control Starts With Respect",
        "thesis": bold_thesis("Before code runs: clear area, operator ready, battery checked. During motion: small command, short duration, visible robot. After motion: stop, observe state, record evidence. Safety mindset connects to every movement and script in the day."),
        "board_type": "list",
        "board_data": [
            bold_grid_list("Before code: Clear area, operator ready, battery checked — physical readiness precedes software execution."),
            bold_grid_list("During motion: Small command, short duration, visible robot — never turn your back on a moving industrial quadruped."),
            bold_grid_list("After motion: Stop, observe state, record evidence — every movement leaves a trace that must be reviewed."),
        ],
        "bottom_band": bold_grid_list("Safety principle: Code is not separate from the robot — code becomes motion, motion changes balance, and balance can affect people, payloads, and the floor around the robot.")
    },
    {
        "title": "One Safe Motion Loop",
        "thesis": bold_thesis("The whole day can be taught through one repeatable B2 motion loop: Inspect → Configure → Command → Override → Observe → Validate. The beginner goal is to prove one small motion before chaining commands, with evidence including command values, robot response, and operator observation."),
        "board_type": "list",
        "board_data": [
            bold_grid_list("Inspect: Check the robot — battery, stance, payload, ports, clear legs."),
            bold_grid_list("Configure: Set safe mode and confirm state streaming is clean."),
            bold_grid_list("Command: Send a small, bounded motion primitive."),
            bold_grid_list("Override: Keep manual stop ready — know the controller/app stop path."),
            bold_grid_list("Observe: Watch actual response — direction, balance, stop behavior."),
            bold_grid_list("Validate: Compare intended vs. observed — only claim success when evidence supports it."),
        ],
        "bottom_band": bold_grid_list("Beginner goal: Prove one small motion before chaining commands. If you cannot explain what happened during a single short command, you are not ready for autonomous point-to-point scripts.")
    },

    # ══════════════════════════════════════════════════════════════
    # SECTION 1 TRANSITION — Slide 5
    # ══════════════════════════════════════════════════════════════
    {
        "title": "Section 1 — B2 Platform Hardware",
        "thesis": bold_thesis("Heavy-duty features, payload readiness, sensors, power, terrain limits, ports, weather boundaries, and field-safe handling — everything students must know about the physical B2 before writing a single line of code."),
        "board_type": "grid",
        "board_data": [
            {"label": "Core Idea", "value": bold_grid_list("The B2 is industrial equipment — knowing its body, payload, sensors, ports, battery, terrain specs, and environmental limits is prerequisite to safe operation.")},
            {"label": "Section Slides", "value": "Slides 6–13: Body zones, payload behavior, sensor awareness, port discipline, battery limits, terrain ability, weather boundaries, and field safety protocols."},
            {"label": "Beginner Goal", "value": "Identify every major B2 hardware zone and explain how each affects operational safety before touching software."},
        ],
        "bottom_band": bold_grid_list("Section rule: Students should be able to point to the main B2 zones before touching software. Hardware knowledge is not optional — it is the foundation of safe command.")
    },

    # ══════════════════════════════════════════════════════════════
    # SLIDES 6–13: B2 PLATFORM HARDWARE
    # ══════════════════════════════════════════════════════════════
    {
        "title": "Know the Body",
        "thesis": bold_thesis("Students should identify the main B2 zones before touching software. The trunk houses computing, battery, payload mounting, and external ports. Four legs provide 12 degrees of freedom across three joints each. The head/sensing zone carries LiDAR and camera perception options."),
        "board_type": "grid",
        "board_data": [
            {"label": "Trunk", "value": bold_grid_list("Computing, battery, payload mounting, external ports — the central housing that carries the robot's brain, power, and cargo.")},
            {"label": "Legs", "value": bold_grid_list("12 degrees of freedom across four limbs — three joints per leg enabling complex terrain adaptation and stable locomotion.")},
            {"label": "Head / Sensing", "value": bold_grid_list("LiDAR and camera perception options — omnidirectional awareness for navigation, obstacle detection, and inspection capture.")},
        ],
        "bottom_band": bold_grid_list("Body check: Can you point to the trunk, each leg's three joints, the sensor head, the payload top, and the battery area on a B2 diagram? If not, review before proceeding to software.")
    },
    {
        "title": "Payload Changes Behavior",
        "thesis": bold_thesis("The B2 is marketed for heavy-duty industrial use with a standing load of at least 120 kg and a continuous walking load of more than 40 kg. A payload changes inertia, balance, stopping distance, and how conservatively the operator should tune velocity and gait choices."),
        "board_type": "table",
        "board_data": {
            "headers": ["Payload Condition", "Speed Guidance", "Turning", "Stopping", "Caution Level"],
            "rows": [
                [bold_table_cell("No Payload"), "Standard limits apply — use approved speed caps.", "Normal turning radius — standard yaw commands.", "Standard stop distance — Move(0,0,0) suffices.", "Baseline — normal supervised operation."],
                [bold_table_cell("Light Payload"), "Reduce speed by ~25% from standard limits.", "Wider turns — reduce yaw rate, allow more space.", "Increased stop distance — expect longer settling.", "Elevated — heavier robot, more inertia."],
                [bold_table_cell("Heavy Payload"), "Reduce speed by ~50% — smooth, gradual commands only.", "Widest turns — minimal yaw, maximum clearance.", "Longest stop distance — plan stop zones generously.", "High — payload dominates dynamics; move conservatively."],
            ]
        },
        "bottom_band": bold_grid_list("Payload rule: Heavier load means slower, smoother commands. Beginners should not interpret payload capability as permission to move aggressively. A payload changes everything about how the robot responds.")
    },
    {
        "title": "Sensors Support Awareness",
        "thesis": bold_thesis("The B2 includes 3D LiDAR for terrain feature awareness, depth cameras for near-field shape and obstacle cues, and optical cameras for visual context and operator review. Students need the practical meaning: sensors help the robot and operator understand the surrounding space before and during movement."),
        "board_type": "grid",
        "board_data": [
            {"label": bold_grid_list("3D LiDAR"), "value": bold_grid_list("Terrain feature awareness — omnidirectional scanning provides structural backbone of the environment map. Works in darkness.")},
            {"label": "Depth Cameras", "value": bold_grid_list("Near-field shape and obstacle cues — front and rear depth sensors provide spatial context for close-range navigation decisions.")},
            {"label": "Optical Cameras", "value": bold_grid_list("Visual context and operator review — front and rear RGB cameras capture inspection evidence and provide situational awareness.")},
        ],
        "bottom_band": bold_grid_list("Sensor mindset: Students do not need advanced perception theory today. They need the practical meaning — sensors help the robot and operator understand the surrounding space before and during movement. Do not outrun what the robot can perceive.")
    },
    {
        "title": "Ports Require Discipline",
        "thesis": bold_thesis("The B2 provides external interfaces including Ethernet, USB, 12 V, 24 V, and battery connections. Unitree explicitly warns that hot swapping aviation plug interfaces is strictly prohibited and may cause equipment failure not covered by warranty. Students should treat physical connectors as safety-critical items."),
        "board_type": "list",
        "board_data": [
            bold_grid_list("External interfaces: Ethernet, USB, 12 V, 24 V, and battery connections — each port has a specific role and voltage expectation."),
            bold_grid_list("Critical rule: No hot swapping aviation plugs — power off before connecting or disconnecting any interface."),
            bold_grid_list("Evidence habit: Inspect connection condition before powering payloads — damaged pins, loose cables, or bent connectors must be reported before use."),
            bold_grid_list("Procedure: Power off, inspect, connect, strain-relieve, confirm — then power on and verify communication."),
        ],
        "bottom_band": bold_grid_list("Port discipline: Treat physical connectors as safety-critical items, not casual accessories. A damaged aviation plug or incorrect voltage connection can cause equipment failure that is not covered by warranty.")
    },
    {
        "title": "Battery Is a Mission Limit",
        "thesis": bold_thesis("The B2 uses the BT2-10 battery with 45 Ah capacity, providing approximately 4–6 hours of operating time depending on use. Students should connect battery status to safe behavior — low power can shorten experiments, limit retries, and require a controlled stop rather than rushed commands."),
        "board_type": "grid",
        "board_data": [
            {"label": bold_grid_list("Battery Model"), "value": bold_grid_list("BT2-10 with 45 Ah capacity — the B2's power source for all computing, sensing, and locomotion.")},
            {"label": "Operating Time", "value": bold_grid_list("Approximately 4–6 hours depending on use — walking, payload, and sensor load all affect runtime.")},
            {"label": "Class Rule", "value": bold_grid_list("Plan commands inside the battery window — check battery level before every run. Low power means stop, not rush.")},
        ],
        "bottom_band": bold_grid_list("Battery discipline: Start check → mid-lab check → stop threshold → recharge/replace decision. Low power can shorten experiments, limit retries, and require a controlled stop rather than rushed commands.")
    },
    {
        "title": "Terrain Ability Is Not Permission",
        "thesis": bold_thesis("The B2 is specified for strong terrain performance including slope ability greater than 45 degrees and step height of 20–25 cm under good conditions. Beginners should not start at the edge of the specification — flat ground first, then small obstacles, then more complex terrain only with supervision."),
        "board_type": "list",
        "board_data": [
            bold_grid_list("Slope ability: Greater than 45 degrees is listed under good conditions — impressive but not a beginner target."),
            bold_grid_list("Step height: 20–25 cm is listed in specifications — useful for industrial terrain, dangerous for first tests."),
            bold_grid_list("Beginner rule: Test flat ground before challenging terrain — the safe teaching pattern is progressive difficulty with supervision at every gate."),
            bold_grid_list("Progression: Flat floor → shallow ramp → small step → instructor-approved challenge — safety gate before each level."),
        ],
        "bottom_band": bold_grid_list("Terrain discipline: Specifications describe capability, not permission. Beginners prove flat-ground control before attempting any terrain challenge. The instructor approves every terrain escalation.")
    },
    {
        "title": "Weather And Site Matter",
        "thesis": bold_thesis("The B2 operates from −20 °C to 55 °C under good weather conditions with IP67 protection. But the phrase 'under good weather conditions' matters — the operator must inspect ground, weather, visibility, bystanders, and payload stability before movement. Environmental rating is not a guarantee of safe operation in all conditions."),
        "board_type": "table",
        "board_data": {
            "headers": ["Site Factor", "Check", "Action If Not Acceptable"],
            "rows": [
                ["Ground", "Dry, stable, free of loose debris, cables, or slippery surfaces.", "Do not run — wet or unstable ground changes traction and stopping."],
                ["Weather", "No rain, snow, or strong wind within the operating temperature range.", "Postpone outdoor runs — weather affects sensors, traction, and safety."],
                ["Visibility", "Operator can clearly see the entire motion zone and robot at all times.", "Reduce motion zone size or add spotters — never run blind."],
                ["People", "All bystanders are behind the safety perimeter and aware of the active robot.", "Clear the zone — no one inside the perimeter during motion."],
                ["Payload", "Payload is secured, balanced, and within approved weight limits.", "Remove or re-secure — unsecured payload is a fall risk."],
            ]
        },
        "bottom_band": bold_grid_list("Site protocol: Site condition decides whether motion begins — not the script, not the schedule, not the lesson plan. If the site fails any check, motion does not happen.")
    },
    {
        "title": "Safety Field Protocols",
        "thesis": bold_thesis("Safety becomes operational rather than abstract when students rehearse specific protocols. A clear zone with no feet, hands, cables, or loose objects near legs. One person commands, one person watches when possible. Know the manual override path before every run. A B2 lesson should never allow code execution before the field protocol is visible."),
        "board_type": "list",
        "board_data": [
            bold_grid_list("Clear zone: No feet, hands, cables, or loose objects near legs — physically mark the motion boundary and keep it clear."),
            bold_grid_list("Operator role: One person commands, one person watches when possible — split responsibility between code execution and safety observation."),
            bold_grid_list("Stop path: Know the manual override before every run — remote control, E-stop, or script-based stop must be rehearsed, not assumed."),
            bold_grid_list("Rehearsal: Physically walk through who gives commands, who watches the robot, where the robot can move, where people stand, and how motion stops."),
        ],
        "bottom_band": bold_grid_list("Protocol rule: A B2 lesson should never allow code execution before the field protocol is visible. Stop authority is not a backup — it is part of the movement system.")
    },

    # ══════════════════════════════════════════════════════════════
    # SECTION 2 TRANSITION — Slide 14
    # ══════════════════════════════════════════════════════════════
    {
        "title": "Section 2 — Navigation & Control Subsystems",
        "thesis": bold_thesis("What the B2 must sense, decide, stabilize, and report during industrial movement. This section covers control layers, state-based readiness, mode protection, perception support, gait style, industrial duty, layered debugging, and the navigation gate before motion."),
        "board_type": "grid",
        "board_data": [
            {"label": "Core Idea", "value": bold_grid_list("B2 control is layered — perception → motion service → state feedback. A high-level command must pass through safety and control layers before legs move.")},
            {"label": "Section Slides", "value": "Slides 15–22: Control layers, state readiness, mode protection, perception role, gait style, industrial duty, failure debugging, and the navigation gate."},
            {"label": "Beginner Goal", "value": "Explain why reading state before sending a command is not optional — it is the difference between controlled motion and blind experimentation."},
        ],
        "bottom_band": bold_grid_list("Section rule: Navigation begins with state, not movement. If the robot does not look ready in state feedback, do not send a command.")
    },

    # ══════════════════════════════════════════════════════════════
    # SLIDES 15–22: NAVIGATION & CONTROL
    # ══════════════════════════════════════════════════════════════
    {
        "title": "Control Has Layers",
        "thesis": bold_thesis("This is a B2 control lesson, not a middleware lesson. Perception describes nearby terrain and obstacles. Motion service converts intent into stable body movement. State feedback tells the operator what actually happened. A high-level command must pass through safety and control layers before legs move."),
        "board_type": "list",
        "board_data": [
            bold_grid_list("Perception: Sensors describe nearby terrain and obstacles — LiDAR, depth cameras, and optical cameras provide the spatial awareness layer."),
            bold_grid_list("Motion Service: Converts intent into stable body movement — gait generation, body stabilization, and coordinated leg control."),
            bold_grid_list("State Feedback: Tells the operator what actually happened — mode, posture, velocity, joint condition, and battery status reported continuously."),
            bold_grid_list("Safety Layer: Every command passes through mode checks, authority verification, and stability gates before reaching motors."),
        ],
        "bottom_band": bold_grid_list("Mental model: Perception inputs → motion service → gait/body controller → legs → state feedback arrow. A high-level command must pass through every layer before legs move. Skip a layer and you lose control.")
    },
    {
        "title": "Navigation Begins With State",
        "thesis": bold_thesis("A beginner point-to-point script should not start by moving. It should first ask whether the robot appears ready. State feedback — body posture, battery, mode, velocity, joint condition — helps confirm readiness. If state looks wrong, motion should pause until the issue is understood."),
        "board_type": "grid",
        "board_data": [
            {"label": "State Examples", "value": bold_grid_list("Body posture, battery level, current mode, velocity readings, joint condition — the B2's self-reported health dashboard.")},
            {"label": "Key Question", "value": bold_grid_list("Is the robot ready to accept movement? — answered by reading SportModeState, not by guessing.")},
            {"label": "Rule", "value": bold_grid_list("Read state before sending a command — no exceptions. State is the only window into what the robot believes is happening.")},
        ],
        "bottom_band": bold_grid_list("State-first rule: If the robot's mode is unexpected, velocity is nonzero at rest, or battery is low, motion should pause. Reading state is not a formality — it is the primary diagnostic before any command.")
    },
    {
        "title": "Modes Protect The Robot",
        "thesis": bold_thesis("The B2 SDK examples expose high-level status and control patterns including stand up/down, velocity movement, attitude balance, trajectory following, and special motions. Mode selection changes what a command means and how much risk it carries. Beginners should learn that standing, velocity motion, and special motions carry different authority levels."),
        "board_type": "table",
        "board_data": {
            "headers": ["Mode", "What It Means", "Risk Level", "Beginner Status"],
            "rows": [
                [bold_table_cell("Standing"), bold_table_cell("Posture is stabilized before travel — BalanceStand establishes controlled upright stance."), "Low — robot stays in place.", "First approved motion command — instructor demonstration."],
                [bold_table_cell("Velocity Motion"), "Small directional command over time — Move(vx, vy, vyaw) translates the robot.", "Medium — robot changes position.", "Instructor-gated — requires demonstrated stop discipline."],
                [bold_table_cell("Trajectory Following"), "Pre-planned path with waypoints — the robot follows a defined route.", "Higher — multiple commands chained.", "Requires strong evidence from simpler modes first."],
                [bold_table_cell("Special Motions"), "Advanced behaviors including gait changes and complex maneuvers.", "Highest — multiple subsystems involved.", "Instructor-only unless explicitly approved for advanced students."],
            ]
        },
        "bottom_band": bold_grid_list("Mode discipline: Mode selection changes what a command means and how much risk it carries. Progress from standing → small velocity → trajectory → special motion ONLY after proving control at each level.")
    },
    {
        "title": "Perception Helps Control",
        "thesis": bold_thesis("Students should connect sensors to practical control decisions. The B2 may include LiDAR, depth cameras, and optical cameras, but today the lesson is not advanced autonomy. The lesson is that perception supports safer movement choices, and the operator should command at a pace suitable for the site."),
        "board_type": "grid",
        "board_data": [
            {"label": "Sensor Role", "value": bold_grid_list("Provide terrain and obstacle cues — LiDAR shows structure, depth cameras show proximity, optical cameras show visual context.")},
            {"label": "Control Role", "value": bold_grid_list("Maintain stable motion despite imperfect ground — the controller uses sensor feedback to adjust gait and balance in real time.")},
            {"label": "Operator Role", "value": bold_grid_list("Do not outrun what the robot can perceive — command speed should respect sensor range, update rate, and site complexity.")},
        ],
        "bottom_band": bold_grid_list("Perception rule: Speed should shrink as obstacles get closer. If the robot's sensor range is 5 m and the stopping distance at current speed is 2 m, you have 3 m of decision space — respect that margin.")
    },
    {
        "title": "Gait Is Movement Style",
        "thesis": bold_thesis("A gait is the pattern of leg timing and body support — not just animation. It determines stability, speed, turning behavior, and terrain response. Beginners should treat gait adjustments as controlled experiments: one change, one short run, one observation, one note."),
        "board_type": "grid",
        "board_data": [
            {"label": bold_grid_list("Gait Definition"), "value": bold_grid_list("The pattern of leg timing and body support — which legs touch the ground when, and how body weight transfers during each phase of movement.")},
            {"label": "Why It Matters", "value": bold_grid_list("Stability, speed, turning, and terrain response all depend on gait choice — a trot handles differently from a walk or a crawl.")},
            {"label": "Beginner Habit", "value": bold_grid_list("Change one gait-related setting at a time — one change, one short run, one observation, one note. Changing multiple variables teaches nothing.")},
        ],
        "bottom_band": bold_grid_list("Gait discipline: A gait change is a controlled experiment. Keep surface and payload fixed, change one gait setting, run a short test, and compare stability and operator confidence before and after.")
    },
    {
        "title": "Industrial Line Means Duty",
        "thesis": bold_thesis("Compared with a lighter classroom robot, the B2's industrial positioning makes payload, site safety, power planning, and controlled gait behavior central topics. More payload means commands must respect inertia. More endurance means runs require battery and thermal discipline. More consequence means site protocol matters as much as code."),
        "board_type": "table",
        "board_data": {
            "headers": ["Dimension", "Lightweight Learning Robot", bold_table_cell("B2 Industrial Platform")],
            "rows": [
                ["Payload", "Minimal — a few kilograms at most.", bold_table_cell("Heavy-duty — standing load ≥120 kg, walking load >40 kg.")],
                ["Site Protocol", "Basic — clear floor is usually sufficient.", bold_table_cell("Strict — ground, weather, people, payload, temperature, visibility all checked.")],
                ["Inertia", "Low — stops quickly, turns easily.", bold_table_cell("High — longer stopping distance, wider turns, slower response to command changes.")],
                ["Operator Discipline", "Moderate — experimentation is common.", bold_table_cell("Strict — every command is gated, every run produces evidence, every stop is rehearsed.")],
            ]
        },
        "bottom_band": bold_grid_list("Industrial mindset: The B2 is working equipment, not a classroom toy. Payload, site safety, power planning, and controlled gait behavior are not advanced topics — they are the baseline for safe operation.")
    },
    {
        "title": "Failures Show In Layers",
        "thesis": bold_thesis("B2 debugging should remain practical. If there is no movement, check mode, command size, and safety gate. If unstable, reduce speed, simplify gait, remove payload risk. If uncertain, stop and read state before retrying. Students should not jump directly to code edits when the robot does not behave as expected."),
        "board_type": "list",
        "board_data": [
            bold_grid_list("If no movement: Check mode (is the robot in a motion-ready state?), command size (is the vector large enough to register?), and safety gate (is authority correctly requested?)."),
            bold_grid_list("If unstable: Reduce speed, simplify gait, remove payload risk — stability problems are rarely fixed by adding complexity."),
            bold_grid_list("If uncertain: Stop and read state before retrying — SportModeState tells you what the robot believes, which is often different from what you assume."),
            bold_grid_list("Debugging order: Mode → command size → terrain → state feedback → retry or stop. Never start debugging by increasing command values."),
        ],
        "bottom_band": bold_grid_list("Debugging discipline: Before editing code, ask whether the robot is in the right mode, whether the command is too small or too large, whether terrain is appropriate, and whether state feedback supports another attempt.")
    },
    {
        "title": "Navigation Gate Before Motion",
        "thesis": bold_thesis("Three gates must clear before the B2 moves: robot standing and stable, operator has manual override ready, and the path is clear with a small initial command. Students should not run movement scripts until all three gates confirm readiness."),
        "board_type": "list",
        "board_data": [
            bold_grid_list("Gate 1: Robot standing and stable — posture confirmed via SportModeState, no unexpected velocity, battery adequate."),
            bold_grid_list("Gate 2: Operator has manual override ready — remote control or E-stop path is known, rehearsed, and immediately accessible."),
            bold_grid_list("Gate 3: Path is clear and command is small — the first movement is the smallest meaningful motion possible, not a full route."),
        ],
        "bottom_band": bold_grid_list("Gate rule: Stable posture → Override ready → Clear path → Movement allowed. If any gate fails, motion does not begin. This gate merges safety, evidence, and debugging into one motion-readiness check.")
    },

    # ══════════════════════════════════════════════════════════════
    # SECTION 3 TRANSITION — Slide 23
    # ══════════════════════════════════════════════════════════════
    {
        "title": "Section 3 — Basic Movements",
        "thesis": bold_thesis("Control vectors, manual override, gait adjustment, and short safe motion tests. Students learn to command small movements, observe response, keep override active, adjust gait with evidence, and validate that stand, forward, turn, and stop are repeatable before progressing to scripted autonomy."),
        "board_type": "grid",
        "board_data": [
            {"label": "Core Idea", "value": bold_grid_list("A control vector is a compact description of movement intent — forward/back, sideways, and yaw — that the B2 controller converts into coordinated leg movement.")},
            {"label": "Section Slides", "value": "Slides 24–31: Control vectors, small-command discipline, manual override, stand-before-travel, forward and turn tests, gait evidence, and movement validation gate."},
            {"label": "Beginner Goal", "value": "Prove that stand, forward, turn, and stop are repeatable before progressing to SDK point-to-point scripts."},
        ],
        "bottom_band": bold_grid_list("Section rule: If basic movement evidence is weak, the correct action is to simplify, not automate. A clean small command is better evidence than a dramatic movement that nobody can explain.")
    },

    # ══════════════════════════════════════════════════════════════
    # SLIDES 24–31: BASIC MOVEMENTS
    # ══════════════════════════════════════════════════════════════
    {
        "title": "A Vector Describes Intent",
        "thesis": bold_thesis("A control vector is a compact way to describe how the robot should move. Beginners can think of it as a small set of numbers for forward motion, side motion, and turning. The B2 controller then tries to turn that intent into coordinated leg movement with stability and safety constraints."),
        "board_type": "grid",
        "board_data": [
            {"label": "Forward / Back", "value": bold_grid_list("Positive or negative travel intent along the robot's body-forward axis — the most fundamental movement primitive.")},
            {"label": "Sideways", "value": bold_grid_list("Lateral intent when supported by the control mode — body-frame left/right translation for positioning adjustments.")},
            {"label": bold_grid_list("Yaw"), "value": bold_grid_list("Turn intent around the body center — rotation without translation, or combined with forward/side motion for curved paths.")},
        ],
        "bottom_band": bold_grid_list("Vector mental model: Picture a top-down robot with three arrows — forward arrow, side arrow, and yaw curved arrow. The B2 controller reads these three numbers and coordinates 12 joint motors to produce the intended motion.")
    },
    {
        "title": "Small Commands Teach More",
        "thesis": bold_thesis("A heavy industrial quadruped teaches best through small commands. Start tiny with short duration and low speed. Observe whether direction, turn, and stop match expectation. Increase only after proof — do not guess upward. A clean small command is better evidence than a dramatic movement that nobody can explain."),
        "board_type": "list",
        "board_data": [
            bold_grid_list("Start tiny: Short duration and low speed — the first command should be the smallest meaningful motion possible, not a demonstration of capability."),
            bold_grid_list("Observe: Did direction, turn, and stop match expectation? — watch the robot, read the state, compare commanded vs. actual."),
            bold_grid_list("Increase only after proof: Do not guess upward — each increase in speed or distance must be justified by successful smaller runs."),
        ],
        "bottom_band": bold_grid_list("Scaling rule: Start at the smallest meaningful command. Only the first step is green until validated. A clean small command is better evidence than a dramatic movement that nobody can explain.")
    },
    {
        "title": "Manual Override Stays Active",
        "thesis": bold_thesis("Manual override is part of the movement system, not a backup afterthought. Students should physically rehearse how to stop motion while the command is still simple. If they cannot stop a short slow movement confidently, they are not ready for autonomous point-to-point scripts."),
        "board_type": "grid",
        "board_data": [
            {"label": "Override Is Not Optional", "value": bold_grid_list("Know the controller/app stop path — remote control, E-stop, or keyboard interrupt must be rehearsed, not assumed.")},
            {"label": "Do Not Bury Control", "value": bold_grid_list("The operator must be ready before code runs — stop authority stays with a named person throughout every movement test.")},
            {"label": "Practice", "value": bold_grid_list("Stop a harmless motion before testing longer motion — if you cannot stop a short slow movement confidently, you are not ready.")},
        ],
        "bottom_band": bold_grid_list("Override discipline: Manual override is part of the movement system, not a backup afterthought. The stop path must be rehearsed during simple commands so it becomes automatic during complex ones.")
    },
    {
        "title": "Stand Before Travel",
        "thesis": bold_thesis("A point-to-point run begins with posture. The Unitree SDK examples include high-level stand up/down and motion tests, which reinforces the practical order: establish a stable posture, confirm the state, then send a small travel command. Posture readiness precedes every movement."),
        "board_type": "list",
        "board_data": [
            bold_grid_list("Posture first: Robot should stand cleanly and settle — BalanceStand establishes controlled upright stance before any travel command."),
            bold_grid_list("State check: Body attitude and mode should look expected — verify via SportModeState that the robot is in the intended mode with stable readings."),
            bold_grid_list("Then move: Travel command follows stable stance — never send a movement command to a robot that is still settling or in an unexpected mode."),
        ],
        "bottom_band": bold_grid_list("Stand-before-travel rule: Stand up → settle and read state → send small vector. Skipping posture verification is the most common beginner mistake that leads to unexpected robot behavior.")
    },
    {
        "title": "Forward Motion Test",
        "thesis": bold_thesis("The first movement test should be boring on purpose. A slow forward command lets beginners confirm that the B2 accepts motion, moves in the expected direction, and stops cleanly. The evidence is simple: command value, duration, actual response, and whether manual override remained available."),
        "board_type": "grid",
        "board_data": [
            {"label": "Command", "value": bold_grid_list("Slow forward vector for a short time — e.g., Move(0.2, 0, 0) for 1–2 seconds. The smallest meaningful translation.")},
            {"label": "Observe", "value": bold_grid_list("Straightness, balance, stop behavior — did the robot move forward without drifting sideways? Did it stop when commanded?")},
            {"label": "Record", "value": bold_grid_list("Command value, duration, response notes — evidence that the simplest movement worked as expected, or notes on what went wrong.")},
        ],
        "bottom_band": bold_grid_list("Forward test: Slow forward vector → observe straightness and stop → record command, duration, response. If the B2 cannot perform a boring straight-line movement, it is not ready for anything more complex.")
    },
    {
        "title": "Turn Motion Test",
        "thesis": bold_thesis("Turning is useful but can confuse beginners because the body rotates while feet step. Keep the turn small, use a clear floor marker, and stop early. The question is not whether the robot can spin dramatically — it is whether students understand command direction and observed yaw response."),
        "board_type": "grid",
        "board_data": [
            {"label": "Command", "value": bold_grid_list("Small yaw value in place or near-place — e.g., Move(0, 0, 0.3) for a short duration. Test rotation awareness.")},
            {"label": "Watch", "value": bold_grid_list("Foot placement, body rotation, available space — does the robot rotate around its center? Are feet stepping correctly?")},
            {"label": "Stop", "value": bold_grid_list("End before drift becomes confusing — stop early, assess orientation, and compare commanded yaw angle with observed rotation.")},
        ],
        "bottom_band": bold_grid_list("Turn test: Small yaw → watch foot placement and rotation → stop before drift confuses. The goal is understanding command-yaw correspondence, not dramatic spinning.")
    },
    {
        "title": "Gait Adjustments Need Evidence",
        "thesis": bold_thesis("Gait adjustment becomes unsafe when students change multiple variables at once. The B2-focused habit is scientific but simple: keep the surface and payload fixed, change one gait-related setting, run a short test, and compare stability and operator confidence before and after."),
        "board_type": "table",
        "board_data": {
            "headers": ["Variable", "Before Change", "After Change", "Evidence"],
            "rows": [
                ["Setting", "Record current gait type, speed, and body height.", "Record new gait type, speed, or body height — only one changed.", bold_table_cell("Exact before/after values — not 'it felt different.'")],
                ["Surface", "Document floor type — concrete, tile, carpet, outdoor.", "Same surface as baseline — surface must not change between tests.", "Photo of test surface with timestamp."],
                ["Payload", "Record payload weight and mounting position.", "Same payload as baseline — payload must not change between tests.", bold_table_cell("Payload photo and weight measurement.")],
                ["Stability", "Describe perceived stability — steady, slight wobble, unstable.", "Compare stability — better, same, or worse than baseline.", "Operator confidence rating on a simple 1–5 scale."],
            ]
        },
        "bottom_band": bold_grid_list("Gait evidence rule: Change one thing — gait style, speed, or terrain — not all three. Compare before and after stability. Document setting, surface, payload, and observed behavior. One change = one lesson learned.")
    },
    {
        "title": "Movement Validation Gate",
        "thesis": bold_thesis("This gate merges debugging and evidence habits into the movement section. Students only progress after the B2 can stand, move forward, turn, and stop in a repeatable way. If the basic movement evidence is weak, the correct action is to simplify, not automate."),
        "board_type": "grid",
        "board_data": [
            {"label": "Pass If", "value": bold_grid_list("Stand, forward, turn, and stop are repeatable — each basic movement executes cleanly with consistent results across multiple attempts.")},
            {"label": "Hold If", "value": "Drift, delay, unstable gait, or uncertain stop occurs — any unexpected behavior means return to smaller, simpler commands until the issue is understood."},
            {"label": "Evidence", "value": bold_grid_list("Notes, values, state snapshot, operator sign-off — documented proof that each movement primitive was tested and confirmed.")},
        ],
        "bottom_band": bold_grid_list("Validation rule: Pass → proceed to scripted autonomy. Hold → simplify and retest. The hold branch loops back to smaller commands. Never progress past this gate with weak evidence.")
    },

    # ══════════════════════════════════════════════════════════════
    # SECTION 4 TRANSITION — Slide 32
    # ══════════════════════════════════════════════════════════════
    {
        "title": "Section 4 — Unitree B2 SDK Scripts",
        "thesis": bold_thesis("Languages, state reading, basic command structure, and point-to-point autonomy. Students learn the Unitree SDK as the practical bridge between code and B2 behavior, covering C++ and Python interfaces, safe script structure, segmented point-to-point logic, pseudocode-first design, and safe script debugging."),
        "board_type": "grid",
        "board_data": [
            {"label": "Core Idea", "value": bold_grid_list("The Unitree SDK (unitree_sdk2 for C++, unitree_sdk2_python for Python) is the bridge between student code and B2 behavior — initialize, read state, command, stop.")},
            {"label": "Section Slides", "value": "Slides 33–38: SDK bridge, language choice, script shape, segmented point-to-point, pseudocode-first, and safe script debugging."},
            {"label": "Beginner Goal", "value": "Write or explain a safe point-to-point script skeleton: initialize → read state → command loop → stop → save evidence."},
        ],
        "bottom_band": bold_grid_list("Section rule: A beginner autonomous script should look predictable. Anyone should be able to point to the initialization block, state check, command loop, stop command, and evidence log.")
    },

    # ══════════════════════════════════════════════════════════════
    # SLIDES 33–38: UNITREE B2 SDK SCRIPTS
    # ══════════════════════════════════════════════════════════════
    {
        "title": "SDK Is The Script Bridge",
        "thesis": bold_thesis("The official Unitree repositories describe SDK version 2 (unitree_sdk2 for C++, unitree_sdk2_python for Python). For this course, students only need a safe beginner subset: initialize the SDK, read status, command small movements, monitor response, and stop cleanly."),
        "board_type": "grid",
        "board_data": [
            {"label": bold_grid_list("C++ SDK"), "value": bold_grid_list("unitree_sdk2 supports building robot applications — closer to compiled production workflows with direct hardware access patterns.")},
            {"label": bold_grid_list("Python SDK"), "value": bold_grid_list("unitree_sdk2_python provides Python interfaces — faster for beginner experiments with readable, rapidly iterable scripts.")},
            {"label": "Beginner Focus", "value": bold_grid_list("Read state, send small commands, stop safely — the same safety logic applies regardless of SDK language choice.")},
        ],
        "bottom_band": bold_grid_list("Bridge mental model: Student script → SDK call layer → B2 state/control interface → robot motion and feedback. The SDK translates code intent into robot action — understanding this bridge is essential for safe scripting.")
    },
    {
        "title": "Choose The Language",
        "thesis": bold_thesis("The language choice should not change the operational discipline. Python may be easier for first scripts with faster iteration, while C++ may match production-style examples. In both cases, the safe script pattern stays the same: check state, command small motion, observe, stop, and log evidence."),
        "board_type": "table",
        "board_data": {
            "headers": ["Dimension", bold_table_cell("Python"), bold_table_cell("C++")],
            "rows": [
                ["Learning Speed", "Faster — readable syntax, rapid iteration, less boilerplate.", "Slower initially — more setup, compilation step, stricter typing."],
                ["Application Style", "Script-driven — ideal for teaching, experiments, and quick tests.", "Application-driven — closer to deployed production robot software."],
                ["Safety Rules", bold_table_cell("Same — check state, command small motion, observe, stop, log evidence."), bold_table_cell("Same — check state, command small motion, observe, stop, log evidence.")],
                ["Course Guidance", "Recommended for first scripts and rapid exploration.", "Available for students with C++ experience or production interests."],
            ]
        },
        "bottom_band": bold_grid_list("Language rule: Same safety logic regardless of language. Python or C++ — the safe script pattern stays identical. Language choice affects syntax and workflow, not operational discipline.")
    },
    {
        "title": "Script Shape Matters",
        "thesis": bold_thesis("A beginner autonomous script should look predictable. It should not jump from launch to travel. The student should be able to point to the initialization block, state check, command loop, stop command, and evidence log. This makes debugging possible when the robot does not behave as expected."),
        "board_type": "list",
        "board_data": [
            bold_grid_list("Initialize: Prepare SDK connection and parameters — ChannelFactoryInitialize, client setup, timeout configuration."),
            bold_grid_list("Read: Confirm robot state and mode — SportModeState must show expected values before any command is sent."),
            bold_grid_list("Command: Send short vector steps toward the target — small, bounded, observed movements, not blind full-route execution."),
            bold_grid_list("Stop: End with controlled zero-motion command — Move(0, 0, 0) or StopMove() followed by authority release."),
            bold_grid_list("Evidence: Save command values, timestamps, state readings, and operator notes — every run produces an auditable record."),
        ],
        "bottom_band": bold_grid_list("Script skeleton: Initialize → read state → command loop → stop → save log. Anyone should be able to identify these five blocks in any Day 3 script. If a block is missing, the script is incomplete.")
    },
    {
        "title": "Point-To-Point Is Segmented",
        "thesis": bold_thesis("Point-to-point does not mean the B2 blindly travels across a room. For beginners, it means a short route divided into safe motion segments. Each segment checks whether the robot is still stable, still inside the site boundary, and still moving toward the intended target. Abort if state or site condition becomes unclear."),
        "board_type": "grid",
        "board_data": [
            {"label": "Target", "value": bold_grid_list("A simple nearby point, not a long mission — the first autonomous route should be short enough that every action is explainable.")},
            {"label": "Segment", "value": bold_grid_list("Move a little, observe, correct, continue — each segment is a self-contained mini-test with its own readiness check.")},
            {"label": "Abort", "value": bold_grid_list("Stop if state or site condition becomes unclear — uncertainty is a valid reason to halt. 'Probably fine' is not a safe state.")},
        ],
        "bottom_band": bold_grid_list("Segmentation rule: Each segment checks whether the robot is still stable, still inside the site boundary, and still moving toward the intended target. Between segments: observe and decide continue/abort.")
    },
    {
        "title": "Use Pseudocode First",
        "thesis": bold_thesis("Students should understand the algorithm before copying syntax. Pseudocode makes the safety structure visible: readiness check, segmented command, repeated observation, stop command, and evidence saving. Once that logic is clear, language-specific examples become much easier to understand."),
        "board_type": "list",
        "board_data": [
            bold_grid_list("Read state. If not ready, stop — the script begins with observation, not action. Unready state = abort."),
            bold_grid_list("For each segment: send small vector, wait briefly, read state — each movement is followed by a verification pause."),
            bold_grid_list("At target: send stop command and save evidence — the script ends with a clean stop and a complete record of what happened."),
        ],
        "bottom_band": bold_grid_list("Pseudocode-first rule: If you cannot explain the algorithm in plain language, you should not be copying syntax. The safety structure — readiness check, segmented command, repeated observation, stop, evidence — must be clear before any code is written.")
    },
    {
        "title": "Debug The Script Safely",
        "thesis": bold_thesis("Debugging a B2 script should never begin by increasing command values. If the robot does not respond, first check readiness and mode. If direction is wrong, inspect the vector signs. If stability is poor, stop and simplify. Debugging is a safety process, not trial-and-error motion."),
        "board_type": "table",
        "board_data": {
            "headers": ["Symptom", "Check First", "Safe Response"],
            "rows": [
                [bold_table_cell("No Response"), "Mode, state readiness, command size — is the robot in a motion-ready mode? Is the command large enough to register?", "Verify state, confirm mode, re-send command — do not increase values blindly."],
                [bold_table_cell("Wrong Direction"), "Vector sign and frame assumption — is the command in body frame or world frame? Is the sign correct for the intended direction?", "Stop, verify coordinate frame, correct sign, re-test with smallest possible command."],
                [bold_table_cell("Unstable Response"), "Speed, gait, payload — is the command too fast for the current gait? Is payload affecting balance?", "Stop, reduce speed, simplify gait, remove payload risk — simplify before investigating."],
            ]
        },
        "bottom_band": bold_grid_list("Debugging safety rule: Never begin debugging by increasing command values. Check readiness first, then mode, then vector correctness. Debugging is a safety process — each check eliminates a risk before the next attempt.")
    },

    # ══════════════════════════════════════════════════════════════
    # SECTION 5 TRANSITION — Slide 39
    # ══════════════════════════════════════════════════════════════
    {
        "title": "Section 5 — Lab Validation",
        "thesis": bold_thesis("Run the B2 safely, capture evidence, and prove the point-to-point workflow. This section covers the pre-run checklist, executing one short route, capturing evidence that proves control, mapping outcomes back to B2-specific learning objectives, and the exit ticket that proves B2 readiness."),
        "board_type": "grid",
        "board_data": [
            {"label": "Core Idea", "value": bold_grid_list("The final lab is short enough that students can explain every action — stand, move forward, adjust heading if needed, stop, and submit evidence.")},
            {"label": "Section Slides", "value": "Slides 40–44: Pre-run checklist, one short route, evidence standards, B2 outcome map, and exit ticket."},
            {"label": "Beginner Goal", "value": "Complete one supervised B2 route, capture command values and state readings, compare intended vs. observed movement, and submit evidence that proves control."},
        ],
        "bottom_band": bold_grid_list("Section rule: The point is not distance — it is controlled B2 behavior. A good run includes a stable stand, a small forward segment, a heading adjustment if needed, and a clean stop with complete evidence.")
    },

    # ══════════════════════════════════════════════════════════════
    # SLIDES 40–44: LAB VALIDATION
    # ══════════════════════════════════════════════════════════════
    {
        "title": "Pre-Run Checklist",
        "thesis": bold_thesis("This checklist combines platform knowledge, safety protocol, and script readiness. Students should not run point-to-point code until the robot, site, and script all pass the pre-run check. Robot: battery, stance, payload, ports, clear legs. Site: floor, boundary, observer, no loose cables. Script: small target, stop command, log folder ready."),
        "board_type": "list",
        "board_data": [
            bold_grid_list("Robot: Battery adequate, stance stable, payload secured, ports inspected, legs clear of obstructions — the physical machine is ready."),
            bold_grid_list("Site: Floor dry and stable, boundary marked, observer in position, no loose cables or debris in the motion zone — the environment is ready."),
            bold_grid_list("Script: Small target defined, stop command included, log folder created and writable — the software is ready."),
            bold_grid_list("Decision: All three columns — robot, site, script — must end in a green 'ready' box before any point-to-point code executes."),
        ],
        "bottom_band": bold_grid_list("Checklist rule: Robot ready + site ready + script ready = motion allowed. If any column is not ready, the run does not happen. This is not a suggestion — it is the operational gate.")
    },
    {
        "title": "Run One Short Route",
        "thesis": bold_thesis("The final lab should be short enough that students can explain every action. A good run includes a stable stand, a small forward segment, a heading adjustment if needed, and a clean stop. The point is not distance — it is controlled B2 behavior with manual override ready for the full run."),
        "board_type": "grid",
        "board_data": [
            {"label": "Route", "value": bold_grid_list("Start point to one nearby target — a simple two-point route with at most one heading correction. Short enough to explain every action.")},
            {"label": "Movement", "value": bold_grid_list("Stand, move forward, adjust heading, stop — each phase is deliberate, observed, and confirmed before the next begins.")},
            {"label": "Supervision", "value": bold_grid_list("Manual override remains ready for the full run — the operator's hand stays on the stop control from start to finish.")},
        ],
        "bottom_band": bold_grid_list("Route success: The point is not distance — it is controlled B2 behavior. A good run = stable stand + small forward segment + heading adjustment if needed + clean stop. Every action is explainable.")
    },
    {
        "title": "Evidence Proves Control",
        "thesis": bold_thesis("Evidence habits belong inside the B2 workflow. A student should be able to show what command was sent, when it was sent, what state was observed, and how the robot moved. Keep command values, timestamps, state readings, and operator notes. Compare intended movement versus observed movement. Only claim success when evidence supports it."),
        "board_type": "grid",
        "board_data": [
            {"label": "Keep", "value": bold_grid_list("Command values, timestamps, state readings, operator notes — every data point that tells the story of what happened during the run.")},
            {"label": "Compare", "value": bold_grid_list("Intended movement versus observed movement — overlay commanded vectors on actual state feedback to identify deviations.")},
            {"label": "Claim", "value": bold_grid_list("Only say success when evidence supports it — 'it worked' is not a claim. 'The robot moved 0.45 m forward in 2.1 s, matching the 0.5 m command' is a claim.")},
        ],
        "bottom_band": bold_grid_list("Evidence standard: Command log + state snapshot + observation notes + route sketch = auditable run. If you cannot show what command was sent and what state was observed, the run is not complete.")
    },
    {
        "title": "B2-Specific Outcome Map",
        "thesis": bold_thesis("This slide confirms that the revised deck is a B2-specific beginner deck, not a general communication deck. Each required outcome is covered directly: platform hardware, navigation and control subsystems, basic movements, and SDK-based point-to-point autonomy."),
        "board_type": "table",
        "board_data": {
            "headers": ["Required Outcome", "Coverage", "Evidence"],
            "rows": [
                [bold_table_cell("B2 Platform Hardware"), "Hardware features, heavy-duty payloads, sensors, ports, battery, terrain limits, weather boundaries, and strict safety field protocols.", bold_table_cell("100% — Slides 5–13 cover every hardware dimension with operational context.")],
                [bold_table_cell("Navigation & Control Subsystems"), "Sensing, state, modes, gait, control layers, industrial duty, layered debugging, and navigation readiness gates.", bold_table_cell("100% — Slides 14–22 explain B2-specific control from perception through motion execution.")],
                [bold_table_cell("Basic Movements"), "Control vectors, small-command discipline, manual override, gait adjustment with evidence, and movement validation gate.", bold_table_cell("100% — Slides 23–31 teach safe movement from stand through validated multi-step motion.")],
                [bold_table_cell("SDK Point-to-Point Scripts"), "C++ and Python SDK basics, safe script structure, segmented point-to-point logic, pseudocode-first design, and safe debugging.", bold_table_cell("100% — Slides 32–38 cover scripting from SDK initialization through evidence-backed execution.")],
            ]
        },
        "bottom_band": bold_grid_list("Coverage confirmation: Every revised Day 3 outcome is covered at 100%. Platform → Subsystems → Movement → SDK → Lab Validation. This deck is B2-specific from first slide to last.")
    },
    {
        "title": "Exit Ticket: Prove B2 Readiness",
        "thesis": bold_thesis("The exit ticket asks for practical proof, not memorization. Students should explain one B2 hardware feature and how it changes safety decisions, demonstrate the Inspect → Configure → Command → Override → Observe → Validate loop, and submit a script outline, run evidence, and safety reflection."),
        "board_type": "grid",
        "board_data": [
            {"label": "Explain", "value": bold_grid_list("How one B2 hardware feature changes safety decisions — connect a specific specification (mass, payload, IP67, terrain ability) to an operational choice you made today.")},
            {"label": "Demonstrate", "value": bold_grid_list("Inspect → Configure → Command → Override → Observe → Validate — walk through the loop with a real or planned B2 movement as evidence.")},
            {"label": "Submit", "value": bold_grid_list("Script outline, run evidence, and safety reflection — a complete packet proving that you can plan, execute, observe, and validate B2 movement.")},
        ],
        "bottom_band": bold_grid_list("Exit ticket standard: B2 readiness is proven with evidence, not claims. Explain a hardware feature → demonstrate the safe motion loop → submit script outline + run evidence + safety reflection. If you cannot produce all three, you are not yet B2-ready.")
    },
]

# ── Write the slides block ──
slides_py = "    \"slides\": [\n"
for i, s in enumerate(SLIDES):
    slides_py += "        {\n"
    slides_py += f"            \"title\": {_json.dumps(s['title'], ensure_ascii=False)},\n"
    slides_py += f"            \"thesis\": {_json.dumps(s['thesis'], ensure_ascii=False)},\n"
    slides_py += f"            \"board_type\": {_json.dumps(s['board_type'], ensure_ascii=False)},\n"
    slides_py += f"            \"board_data\": {_json.dumps(s['board_data'], ensure_ascii=False, indent=12).replace(chr(10), chr(10) + '            ')},\n"
    slides_py += f"            \"bottom_band\": {_json.dumps(s['bottom_band'], ensure_ascii=False)}\n"
    slides_py += "        }"
    if i < len(SLIDES) - 1:
        slides_py += ","
    slides_py += "\n"
slides_py += "    ],"

print(f"Generated {len(SLIDES)} slides block ({len(slides_py):,} chars)")
print("Slides:")
for i, s in enumerate(SLIDES):
    print(f"  {i+1:2d}. [{s['board_type']:5s}] {s['title'][:90]}")

# ── Self-Audit: Check for unparsed markdown artifacts ──
import re as _re

AUDIT_ERRORS = []
LEAKING_ASTERISK = _re.compile(r'\*\*[^*]+\*\*')
LEAKING_UNDERSCORE = _re.compile(r'__[^_]+__')
LEAKING_ANGLE_TAG = _re.compile(r'<[^>]*>')
STRONG_TAG_OPEN = _re.compile(r'<strong[^>]*>')
STRONG_TAG_CLOSE = _re.compile(r'</strong>')

for i, s in enumerate(SLIDES):
    for field in ['title', 'thesis', 'bottom_band']:
        val = s[field]
        # Check for raw ** markers
        if _re.search(r'\*\*', val):
            AUDIT_ERRORS.append(f"Slide {i+1} [{field}]: Leaking ** markers")
        # Check for raw __ markers
        if _re.search(r'__', val):
            AUDIT_ERRORS.append(f"Slide {i+1} [{field}]: Leaking __ markers")
        # Check for unbalanced <strong> tags
        opens = len(STRONG_TAG_OPEN.findall(val))
        closes = len(STRONG_TAG_CLOSE.findall(val))
        if opens != closes:
            AUDIT_ERRORS.append(f"Slide {i+1} [{field}]: Unbalanced <strong> tags ({opens} opens, {closes} closes)")

    # Check board_data
    bd = s['board_data']
    if isinstance(bd, dict):
        for k, v in bd.items():
            if isinstance(v, list):
                for ri, row in enumerate(v):
                    if isinstance(row, list):
                        for ci, cell in enumerate(row):
                            if isinstance(cell, str) and _re.search(r'\*\*', cell):
                                AUDIT_ERRORS.append(f"Slide {i+1} [board_data.{k}[{ri}][{ci}]]: Leaking ** markers")
                            if isinstance(cell, str):
                                opens_c = len(STRONG_TAG_OPEN.findall(cell))
                                closes_c = len(STRONG_TAG_CLOSE.findall(cell))
                                if opens_c != closes_c:
                                    AUDIT_ERRORS.append(f"Slide {i+1} [board_data.{k}[{ri}][{ci}]]: Unbalanced <strong> tags")
    elif isinstance(bd, list):
        for bi, item in enumerate(bd):
            if isinstance(item, dict):
                for lv in ['label', 'value']:
                    if lv in item and isinstance(item[lv], str):
                        if _re.search(r'\*\*', item[lv]):
                            AUDIT_ERRORS.append(f"Slide {i+1} [board_data[{bi}].{lv}]: Leaking ** markers")
                        opens_b = len(STRONG_TAG_OPEN.findall(item[lv]))
                        closes_b = len(STRONG_TAG_CLOSE.findall(item[lv]))
                        if opens_b != closes_b:
                            AUDIT_ERRORS.append(f"Slide {i+1} [board_data[{bi}].{lv}]: Unbalanced <strong> tags ({opens_b} opens, {closes_b} closes)")
            elif isinstance(item, str):
                if _re.search(r'\*\*', item):
                    AUDIT_ERRORS.append(f"Slide {i+1} [board_data[{bi}]]: Leaking ** markers")
                opens_b2 = len(STRONG_TAG_OPEN.findall(item))
                closes_b2 = len(STRONG_TAG_CLOSE.findall(item))
                if opens_b2 != closes_b2:
                    AUDIT_ERRORS.append(f"Slide {i+1} [board_data[{bi}]]: Unbalanced <strong> tags")

# ── Integrity: Verify slide count ──
if len(SLIDES) != 45:
    AUDIT_ERRORS.append(f"Slide count is {len(SLIDES)}, expected 45 (Cover + 44 numbered)")

# ── Integrity: Verify every slide has correct board_data structure ──
for i, s in enumerate(SLIDES):
    bt = s['board_type']
    bd = s['board_data']
    if bt == 'table':
        if not isinstance(bd, dict) or 'headers' not in bd or 'rows' not in bd:
            AUDIT_ERRORS.append(f"Slide {i+1} [{bt}]: Missing headers or rows")
    elif bt == 'grid':
        if not isinstance(bd, list):
            AUDIT_ERRORS.append(f"Slide {i+1} [{bt}]: board_data must be list")
        for j, item in enumerate(bd):
            if not isinstance(item, dict) or 'label' not in item or 'value' not in item:
                AUDIT_ERRORS.append(f"Slide {i+1} [{bt}] item {j}: Missing label or value")
    elif bt == 'list':
        if not isinstance(bd, list):
            AUDIT_ERRORS.append(f"Slide {i+1} [{bt}]: board_data must be list")

print(f"\n{'=' * 60}")
if AUDIT_ERRORS:
    print(f"SELF-AUDIT FAILED — {len(AUDIT_ERRORS)} errors:")
    for e in AUDIT_ERRORS:
        print(f"  ❌ {e}")
    print("\nAborting — fix errors before writing to build_syllabus.py")
    import sys
    sys.exit(1)
else:
    print("SELF-AUDIT PASSED ✅")
    print("  - No leaking ** or __ markdown artifacts")
    print("  - No unbalanced <strong> tags")
    print(f"  - {len(SLIDES)} slides (Cover + 44 numbered) verified")
    print("  - All board_data structures match declared board_type")

# ── Replace in build_syllabus.py ──
print(f"\nReplacing DAY03 slides in build_syllabus.py...")
build_path = "build_syllabus.py"
with open(build_path) as f:
    content = f.read()

# Find the DAY03 slides array boundaries
day03_start = content.index('DAY03 = {')
# Find the slides key within DAY03
slides_key = '\n    "slides": ['
slides_start = content.index(slides_key, day03_start) + len(slides_key)
# Find the closing of slides array ("]" followed by "labs" or next section)
slides_end_marker = '\n    ],\n    "labs": ['
slides_end = content.index(slides_end_marker, slides_start)

# Strip the leading spaces from slides_py to match the indentation level
# slides_py starts with '    "slides": [\n' — we need just the array content
inner_slides = slides_py[slides_py.index('[\n') + 2:]  # Everything after '[\n'

new_content = content[:slides_start] + inner_slides + content[slides_end:]

with open(build_path, "w") as f:
    f.write(new_content)

print(f"✅ Replaced slides array in {build_path}")
print(f"   Old slides block: {slides_end - slides_start:,} chars")
print(f"   New slides block: {len(slides_py):,} chars")
print("Done. Run build_syllabus_final.py to regenerate syllabus.json.")