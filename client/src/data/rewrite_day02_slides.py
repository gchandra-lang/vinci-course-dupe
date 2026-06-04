#!/usr/bin/env python3
"""
Rewrite DAY02 slides in build_syllabus.py to 43 slides
aligned with "Day 2 Beginner-Friendly Full Slide Content" curriculum.
Applies semantic keyword bolding ONLY on fields rendered through SafeHTML.
Titles and table headers are plain text — no bold() calls.
"""
import re, json as _json

# ── Semantic keyword bolding helper ──
# Only called on thesis, table cells, grid labels/values, list items, bottom_band.
# NEVER called on "title" or table "headers" — those render as plain text in Home.tsx.
def bold(s):
    patterns = [
        # Core robotics terms
        (r'\b(SLAM)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(LiDAR)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(IMU)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(GPS)\b', r'<strong class="font-bold">\1</strong>'),
        # Middleware / platforms
        (r'\b(ROS 2)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(Gazebo)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(RViz)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(DDS)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(CycloneDDS)\b', r'<strong class="font-bold">\1</strong>'),
        # Robot platform
        (r'\b(Go2)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(Unitree)\b', r'<strong class="font-bold">\1</strong>'),
        # Client classes
        (r'\b(ObstaclesAvoidClient)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(VideoClient)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(SportClient)\b', r'<strong class="font-bold">\1</strong>'),
        # ROS topics
        (r'\b(/cmd_vel)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(/odom)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(/scan)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(/costmap)\b', r'<strong class="font-bold">\1</strong>'),
        # Key concepts
        (r'\b(costmap)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(odometry)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(pose)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(inflation)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(planner)\b', r'<strong class="font-bold">\1</strong>'),
        # File extensions
        (r'\b(\.json)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(\.jsonl)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(\.jpg)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(\.md)\b', r'<strong class="font-bold">\1</strong>'),
        # SDK terms
        (r'\b(unitree_sdk2_python)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(unitree_sdk2)\b', r'<strong class="font-bold">\1</strong>'),
        # ROS types
        (r'\b(geometry_msgs)\b', r'<strong class="font-bold">\1</strong>'),
        (r'\b(Twist)\b', r'<strong class="font-bold">\1</strong>'),
        # Bridge
        (r'\b(ros_gz_bridge)\b', r'<strong class="font-bold">\1</strong>'),
    ]
    for pat, repl in patterns:
        s = re.sub(pat, repl, s)
    return s

# ── 43 Slides (Cover + Slides 1–42) ──
SLIDES = [
    # ── Slide 1: Cover → Title + Learning Outcomes ──
    {
        "title": "Day 2: Autonomy, Simulation, and Field Handoff",
        "thesis": "Day 2 is one connected story: how a robot observes the world, builds usable understanding, chooses motion, rehearses that motion in simulation, and then performs a controlled test on physical hardware. Beginners leave with a mental map of the full autonomy pipeline.",
        "board_type": "grid",
        "board_data": [
            {"label": "Pipeline", "value": bold("Sense → Understand → Plan → Simulate → Deploy → Prove — six stages that connect into one autonomy workflow.")},
            {"label": "Four Milestones", "value": bold("SLAM + Fusion, Planning + Costmaps, Gazebo Validation, Go2 Handoff — each milestone builds toward the final capstone demonstration.")},
            {"label": "Beginner Promise", "value": "By the end of Day 2, you will explain what SLAM, sensor fusion, costmaps, planning, and Gazebo validation mean, and you will connect those ideas to hardware field testing on the Go2."},
            {"label": "Platform", "value": bold("Unitree Go2 quadruped with ROS 2, Gazebo simulation, and Python SDK integration.")},
        ],
        "bottom_band": bold("Mental model check: Can you draw six connected blocks — Sense, Understand, Plan, Simulate, Deploy, Prove — and explain what data flows between them? If not, that is the goal for today.")
    },
    # ── Slide 2: Slide 1 — Today Builds One Autonomy Story ──
    {
        "title": "Today Builds One Autonomy Story",
        "thesis": bold("Day 2 is not a set of disconnected robotics topics. It is one story about how a robot observes the world, builds usable understanding, chooses motion, rehearses that motion in simulation, and then performs a controlled test on physical hardware."),
        "board_type": "list",
        "board_data": [
            bold("Sense: Sensors collect observations — LiDAR for shape, cameras for appearance, IMU for motion."),
            bold("Understand: Multi-sensor fusion and SLAM combine observations into a map and pose estimate the robot can use."),
            bold("Plan: Global and local planners convert intent into safe routes, using costmaps to mark risk."),
            bold("Simulate: Gazebo provides a rehearsal space — test routes, check sensor data, validate before hardware."),
            bold("Deploy: Controlled hardware handoff — network check, robot state check, safe command authority, field run."),
            bold("Prove: Every claim needs matching evidence — logs, screenshots, route traces, and a written conclusion."),
        ],
        "bottom_band": bold("Beginner checkpoint: After each section today, ask yourself — 'Which stage of the Sense → Prove chain did we just cover?' Keep a running map of where you are in the pipeline.")
    },
    # ── Slide 3: Slide 2 — Four Milestones Define Success ──
    {
        "title": "Four Milestones Define Success",
        "thesis": bold("The lecture is organized around four required academic milestones: SLAM + Fusion, Planning + Costmaps, Gazebo Validation, and Go2 Handoff. Each connects to the next — you cannot validate a route in simulation if you have not understood how the robot builds a map."),
        "board_type": "table",
        "board_data": {
            "headers": ["Milestone", "Key Question", "Evidence Required"],
            "rows": [
                [bold("SLAM + Fusion"), "How does the robot know where it is and what is around it?", bold("Map snapshot, pose trace, transform tree, sensor status, logs.")],
                [bold("Planning + Costmaps"), "How does the robot choose safe motion?", bold("Route plot, costmap snapshot, plan file, obstacle detection record.")],
                [bold("Gazebo Validation"), "Does the routine work safely in rehearsal?", bold("World screenshot, route trace, costmap snapshot, log file, conclusion.")],
                [bold("Go2 Handoff"), "Does the routine work on physical hardware?", bold("Field video, command log, stop events, route trace, tuning notes.")],
            ]
        },
        "bottom_band": bold("Milestone check: If you cannot answer the Key Question for a milestone, flag it now. Each milestone is a gate — the next one makes less sense without the previous one.")
    },
    # ── Slide 4: Slide 3 — Beginner Vocabulary Map ──
    {
        "title": "Beginner Vocabulary Map",
        "thesis": "Students do not need to memorize every robotics term immediately. They need a simple vocabulary map: a map describes the environment, a pose describes the robot's estimated location and orientation, a planner chooses movement, and a costmap marks risky nearby space so motion can be safer.",
        "board_type": "grid",
        "board_data": [
            {"label": bold("Map"), "value": bold("Where things are — an occupancy grid showing free space, obstacles, and unknown areas. Built and updated by SLAM.")},
            {"label": bold("Pose"), "value": bold("Where the robot is — its estimated position (x, y, z) and orientation (roll, pitch, yaw) in a coordinate frame.")},
            {"label": bold("Planner"), "value": bold("Where to go next — a global planner chooses the big-picture route; a local planner handles the next few safe steps.")},
            {"label": bold("Costmap"), "value": bold("Where it is risky — a local grid around the robot marking obstacles, inflated safety buffers, and unknown space.")},
        ],
        "bottom_band": bold("Vocabulary test: Can you explain Map, Pose, Planner, and Costmap to a classmate in one sentence each, without using any of those four words in the explanation? Try it.")
    },
    # ── Slide 5: Slide 4 — Autonomy Is Layered, Not Magical ──
    {
        "title": "Autonomy Is Layered, Not Magical",
        "thesis": "A robot does not become autonomous because one command says go. Autonomy is layered. Sensors collect observations, fusion combines them, SLAM estimates pose and map structure, planning chooses a path, costmaps protect local movement, control sends motion, and evidence tells us whether the claim is true.",
        "board_type": "list",
        "board_data": [
            bold("Sensors → Fusion: Raw observations are combined — LiDAR sees shape, cameras see appearance, IMU senses motion."),
            bold("Fusion → SLAM: Combined sensor data feeds simultaneous localization and mapping — pose estimate plus map structure."),
            bold("SLAM → Planning: The map and pose provide the spatial understanding planners need to choose routes."),
            bold("Planning → Costmap → Control: Global route is refined by local costmaps; control sends safe motion commands."),
            bold("Control → Evidence: Logs, images, traces, and reports prove what happened — without evidence, motion is just a demo."),
        ],
        "bottom_band": bold("Layering check: Draw the stack from bottom (Sensors) to top (Evidence). Can you add one data artifact at each layer that proves that layer worked?")
    },
    # ── Slide 6: Slide 5 — Section 1: SLAM and Fusion ──
    {
        "title": "Section 1 — SLAM and Fusion",
        "thesis": "How the robot builds a usable understanding of space. This section covers SLAM fundamentals, why quadruped SLAM is harder, multi-sensor fusion, coordinate frames, point cloud processing, and the evidence habits that make SLAM claims reviewable.",
        "board_type": "grid",
        "board_data": [
            {"label": "Core Idea", "value": bold("SLAM = Localization + Mapping, solved together. The robot estimates where it is while building or updating a map.")},
            {"label": "Why It Is Hard", "value": "Each job depends on the other. A wrong pose distorts the map. A poor map makes localization less reliable."},
            {"label": "Beginner Goal", "value": bold("Replace vague claims like 'SLAM worked' with evidence: map snapshot, pose trace, transform tree, sensor status, and saved log.")},
            {"label": "Section Slides", "value": "Slides 6–12: SLAM definition, quadruped challenges, multi-sensor fusion, coordinate frames, point clouds, evidence habits, and the data-path debugging routine."},
        ],
        "bottom_band": bold("Section framing: By the end of this section, you should be able to explain why SLAM is called 'simultaneous' and what kind of evidence proves it is working.")
    },
    # ── Slide 7: Slide 6 — SLAM Means Two Jobs at Once ──
    {
        "title": "SLAM Means Two Jobs at Once",
        "thesis": bold("SLAM stands for simultaneous localization and mapping. The robot estimates where it is (localization) while also building or updating a map (mapping). This is difficult because each job depends on the other — if the pose estimate is wrong, the map becomes distorted; if the map is poor, localization becomes less reliable."),
        "board_type": "grid",
        "board_data": [
            {"label": bold("Localize"), "value": bold("'Where am I?' — Estimate the robot's position and orientation relative to the map using sensor observations and motion predictions.")},
            {"label": bold("Map"), "value": bold("'What is around me?' — Build and update a representation of the environment: occupancy grid, feature map, or point cloud.")},
            {"label": bold("SLAM Loop"), "value": bold("Sensor readings → Pose estimate → Map update → Error correction → Better pose → Repeat. Each cycle refines both answers.")},
            {"label": "Failure Mode", "value": "If the robot loses localization (kidnapped robot problem), the map and pose both become unreliable until recovery."},
        ],
        "bottom_band": bold("Diagram exercise: Draw the SLAM loop on paper. Label where sensor data enters, where pose is estimated, where the map updates, and where error correction feeds back. Can you identify which arrow carries the most uncertainty?")
    },
    # ── Slide 8: Slide 7 — Why Quadruped SLAM Is Harder ──
    {
        "title": "Why Quadruped SLAM Is Harder",
        "thesis": "Quadrupeds move differently from wheeled robots. Their bodies rise, fall, pitch, and vibrate as they walk. These motions can disturb cameras, LiDAR, and inertial measurements. Robot locomotion and robot perception are connected — stable movement often improves mapping quality.",
        "board_type": "table",
        "board_data": {
            "headers": ["Motion Effect", "Sensor Impact", "SLAM Consequence"],
            "rows": [
                ["Body pitch/roll during gait", bold("IMU readings include walking vibration."), "Pose estimate becomes noisier — map features may misalign between frames."],
                ["Vertical bounce", bold("LiDAR scan lines shift upward and downward."), "Point cloud registration errors increase — walls may appear wavy or duplicated."],
                ["Foot strike vibration", "Camera images may blur at key moments.", "Visual features become harder to track — loop closures weaken."],
                ["Variable ground contact", bold("Odometry slip accumulates."), "Motion prediction drifts — the robot thinks it moved farther or shorter than reality."],
            ]
        },
        "bottom_band": bold("Key insight for beginners: Walking is not a sensor problem to ignore — it is a perception challenge. When mapping quality drops, check gait stability before changing SLAM parameters.")
    },
    # ── Slide 9: Slide 8 — Multi-Sensor Fusion Combines Strengths ──
    {
        "title": "Multi-Sensor Fusion Combines Strengths",
        "thesis": "No sensor is perfect. LiDAR can describe geometry but may not identify object meaning. Cameras provide appearance but depend on lighting. IMUs capture motion but drift over time. Odometry estimates movement but can accumulate error. Fusion combines these clues so the system has a more reliable state estimate.",
        "board_type": "table",
        "board_data": {
            "headers": ["Sensor", "Strength", "Weakness", "Fusion Role"],
            "rows": [
                [bold("LiDAR"), "Accurate 3D geometry, works in darkness.", "Cannot see through glass; no color or semantic meaning.", "Provides structural backbone of the map."],
                ["Camera", "Rich appearance, object recognition.", "Fails in low light or direct glare; depth estimation is indirect.", "Adds visual features for place recognition and loop closure."],
                [bold("IMU"), "Fast motion sensing, independent of environment.", "Drifts over seconds; cannot provide absolute position.", "Stabilizes pose between slower sensor updates."],
                [bold("Odometry"), "Direct motion estimate from leg/joint sensors.", "Slip and uneven terrain cause accumulating error.", "Provides short-term motion prediction for the filter."],
            ]
        },
        "bottom_band": bold("Fusion mental model: 'LiDAR gives the shape, camera gives the look, IMU gives the feel, and odometry gives the motion guess — fusion turns them into one reliable answer.'")
    },
    # ── Slide 10: Slide 9 — Frames Keep Everyone Speaking the Same Language ──
    {
        "title": "Frames Keep Everyone Speaking the Same Language",
        "thesis": "A frame is a coordinate language. The map has one language, the robot body has another, and each sensor may have its own. Transformations translate between those languages. When transforms are missing, stale, or inverted, a path can look correct on screen but become unsafe in the real world.",
        "board_type": "list",
        "board_data": [
            bold("Map Frame: The fixed world coordinate system. Everything is ultimately referenced to this frame — the global 'truth' of where things are."),
            bold("Odom Frame: The robot's estimated position from odometry. Drifts over time — useful for short-term motion, not long-term accuracy."),
            bold("Base Link / Body Frame: Attached to the robot chassis. Motion commands are expressed relative to this frame — 'go forward' means 'go forward from the robot's current facing direction.'"),
            bold("Sensor Frames: Each sensor (camera, LiDAR) has its own frame. Transforms map sensor data into the body frame and then into the world frame."),
            bold("Transform Tree: A directed graph connecting all frames. If any link breaks or is inverted, the entire perception chain may produce wrong results."),
        ],
        "bottom_band": bold("Frame debugging: When sensor data appears in the wrong place, check the transform tree first — not the algorithm. Missing or stale transforms are the most common beginner frame error.")
    },
    # ── Slide 11: Slide 10 — Point Clouds Become Navigation Information ──
    {
        "title": "Point Clouds Become Navigation Information",
        "thesis": "Point clouds are collections of spatial samples — not automatically a path. The system filters noisy points, identifies occupied space, projects relevant geometry into grids, and builds costmaps that planners can use. This conversion is the bridge from sensing to safe navigation.",
        "board_type": "list",
        "board_data": [
            bold("Raw Points: Sensor returns thousands of 3D points — scattered, noisy, unprocessed. Includes ghost points, reflections, and sensor artifacts."),
            bold("Filtered Points: Noise removal, downsampling, and outlier rejection produce a cleaner point set. Fewer points, but each is more reliable."),
            bold("Occupancy Grid: Points are projected into a 2D or 3D grid. Each cell is marked free, occupied, or unknown based on point evidence."),
            bold("Costmap: The occupancy grid is annotated with risk — obstacle cells are lethal, nearby cells are inflated with safety buffers, and unknown cells carry caution."),
            bold("Path Choice: The planner reads the costmap and selects the lowest-cost route that respects safety margins and reaches the goal."),
        ],
        "bottom_band": bold("Pipeline check: 'I have a point cloud — can I send it directly to the planner?' No. Walk through each conversion step and identify what information is added or removed at each stage.")
    },
    # ── Slide 12: Slide 11 — Beginner Evidence Habit for SLAM ──
    {
        "title": "Beginner Evidence Habit for SLAM",
        "thesis": bold("Replace vague success claims with artifacts. If students say 'SLAM worked,' they should show the map snapshot, pose trace, transform tree, sensor status, and saved log. Evidence makes robotics work reviewable, repeatable, and easier to debug."),
        "board_type": "table",
        "board_data": {
            "headers": ["Instead of Saying...", "Show This Evidence"],
            "rows": [
                [bold("\"SLAM worked.\""), bold("Map snapshot (screenshot of the built map), pose trace (x/y/yaw over time), and transform tree (all frames connected and timestamped).")],
                [bold("\"The robot knows where it is.\""), bold("Pose estimate plot with covariance bounds. If uncertainty is large, the robot does not really know.")],
                [bold("\"The sensors are fine.\""), bold("Sensor status dashboard: publication rate, timestamp freshness, data range. A sensor that publishes stale data is not fine.")],
                [bold("\"The map looks good.\""), "Quantitative comparison: map-to-ground-truth alignment, feature count, registration score. Aesthetics are not accuracy."],
            ]
        },
        "bottom_band": bold("Evidence rule: If you cannot show an artifact that proves your claim, you do not have evidence — you have an opinion. Opinions are fine for conversation; artifacts are required for engineering.")
    },
    # ── Slide 13: Slide 12 — Debugging Habit: Check the Data Path First ──
    {
        "title": "Debugging Habit: Check the Data Path First",
        "thesis": "When mapping or localization fails, beginners often change algorithms too quickly. First check the data path: confirm the sensor publishes, the frame transform exists, timestamps are current, the map updates, and the pose estimate stays reasonable. Many failures come from missing data, not bad theory.",
        "board_type": "list",
        "board_data": [
            bold("Step 1 — Sensor publishes? Confirm the topic or SDK stream is active. No data → no SLAM. Check rostopic list, rostopic hz, or SDK subscriber callbacks."),
            bold("Step 2 — Frame exists? Verify the transform from sensor to base and base to map exists. Missing transforms produce ghost obstacles or invisible walls."),
            bold("Step 3 — Timestamp valid? Check that sensor timestamps are current (not system time mismatch or stale data). Stale timestamps break filter updates."),
            bold("Step 4 — Map updates? Observe whether the occupancy grid changes as the robot moves. A static map when the robot is moving means SLAM is not updating."),
            bold("Step 5 — Pose stable? Monitor pose estimate over time. Large jumps, oscillation, or divergence indicate a filter or registration problem, not a planning problem."),
        ],
        "bottom_band": bold("Data-path first: Before touching any algorithm parameter, confirm that data enters the system, transforms exist, timestamps are valid, the map updates, and the pose is stable. Most 'SLAM failures' are actually data-path failures.")
    },
    # ── Slide 14: Slide 13 — Section 2: Planning and Costmaps ──
    {
        "title": "Section 2 — Planning and Costmaps",
        "thesis": "How goals become safer robot motion. This section covers global vs. local planners, costmap structure, inflation zones, the difference between obstacle avoidance and full navigation, the Go2 avoid-mode lifecycle, patrol plans as beginner route contracts, and the habit of separating plan, command, and robot failures.",
        "board_type": "grid",
        "board_data": [
            {"label": "Core Idea", "value": bold("Planning turns intent into motion: Goal → Route → Local motion → Robot command. Each layer refines the intent into safer, more specific instructions.")},
            {"label": "Key Concept", "value": bold("A costmap is a risk picture around the robot. It marks free, occupied, inflated, and unknown cells so the planner avoids dangerous space.")},
            {"label": "Common Mistake", "value": bold("Confusing obstacle avoidance (reactive, local) with navigation (planned, global). Both are needed — avoidance alone does not choose a destination.")},
            {"label": "Section Slides", "value": "Slides 14–21: Planning concepts, global/local split, costmap grid, inflation, avoidance vs. navigation, Go2 avoid lifecycle, patrol plans, and layered debugging."},
        ],
        "bottom_band": bold("Section framing: By the end of this section you should be able to read a costmap, explain why inflation exists, and describe how the Go2 avoid-mode lifecycle protects local motion.")
    },
    # ── Slide 15: Slide 14 — Planning Turns Intent into Motion ──
    {
        "title": "Planning Turns Intent into Motion",
        "thesis": bold("Path planning begins with intent. The robot needs to reach a checkpoint, inspect an object, or move through a corridor. The planner converts that intent into a route. A local motion layer then turns the route into near-term movement that respects obstacles, robot size, and safety margins."),
        "board_type": "grid",
        "board_data": [
            {"label": bold("Goal"), "value": bold("What the robot should achieve — reach a checkpoint, inspect a target, patrol a corridor. The goal is expressed in the map frame as a destination pose.")},
            {"label": bold("Route"), "value": bold("The global path from start to goal — a sequence of waypoints through free space. The global planner computes this using the full occupancy grid.")},
            {"label": bold("Local Motion"), "value": bold("The next few velocity or increment commands — refined by the local costmap to avoid nearby obstacles. Updated at a higher frequency than the global route.")},
            {"label": bold("Robot Command"), "value": bold("The final motion instruction — Move(vx, vy, vyaw) or MoveToIncrementPosition(dx, dy, dyaw) — sent to the robot through the appropriate client.")},
        ],
        "bottom_band": bold("Planning mental model: 'Goal is the destination postcard, Route is the highway map, Local Motion is the next three seconds of driving, and Robot Command is the steering wheel.' Each layer operates at a different time and space scale.")
    },
    # ── Slide 16: Slide 15 — Global and Local Planners Split the Job ──
    {
        "title": "Global and Local Planners Split the Job",
        "thesis": "A global planner reasons over the larger map and chooses a route toward the destination. A local planner focuses on the space near the robot and adapts to immediate obstacles. Beginners can remember this as: global chooses the trip, local watches the next few steps.",
        "board_type": "table",
        "board_data": {
            "headers": ["Dimension", "Global Planner", "Local Planner"],
            "rows": [
                ["Scope", "Full map — considers the entire known environment.", "Local window — typically a few meters around the robot."],
                ["Update Rate", "Slow — recomputed when the map changes or a new goal arrives.", "Fast — replanned at 5–20 Hz to react to dynamic obstacles."],
                ["Output", "A route: sequence of waypoints through free space.", "A trajectory: velocity commands or increment goals for the next few seconds."],
                ["Fails When", "The map is incomplete or the goal is unreachable.", "An unexpected obstacle appears too close for the stopping distance."],
                ["Beginner Analogy", bold("\"Which highway should I take to the city?\""), bold("\"Should I brake for the car that just pulled in front of me?\"")],
            ]
        },
        "bottom_band": bold("Key distinction: If the robot does not know the overall route, the problem is global planning. If the robot knows the route but hits nearby obstacles, the problem is local planning. Separate these before debugging.")
    },
    # ── Slide 17: Slide 16 — A Costmap Is a Risk Picture ──
    {
        "title": "A Costmap Is a Risk Picture",
        "thesis": "A local costmap is a grid around the robot. Each cell stores risk information. Some cells are free, some contain obstacles, some are unknown, and some are inflated safety areas around obstacles. The planner reads this grid to avoid choosing motion that is too close or unsafe.",
        "board_type": "grid",
        "board_data": [
            {"label": bold("Free Space (Low Risk)"), "value": bold("Cells with no detected obstacles. The planner can route through these cells at low cost. Color-coded green in most visualizers.")},
            {"label": bold("Obstacle (Blocked)"), "value": bold("Cells containing detected obstacles — lethal cost. The planner must never route through these. Color-coded dark/red.")},
            {"label": bold("Inflation (Safety Buffer)"), "value": bold("Cells near obstacles — cost increases with proximity. Creates a safety margin so the robot does not scrape walls or cones. Color-coded amber/yellow gradient.")},
            {"label": bold("Unknown (Be Careful)"), "value": "Cells with no sensor data — the robot does not know what is there. Conservative planners treat unknown as high-cost. Color-coded gray."},
        ],
        "bottom_band": bold("Costmap reading exercise: Look at a costmap visualization. Point to one free cell, one obstacle cell, one inflated cell, and one unknown cell. For each, explain what the planner will do with that information.")
    },
    # ── Slide 18: Slide 17 — Inflation Creates Breathing Room ──
    {
        "title": "Inflation Creates Breathing Room",
        "thesis": "Robots need space around obstacles. Inflation expands obstacle regions so the planner avoids scraping walls, cones, or people. The margin should consider robot width, pose uncertainty, and field safety rules. More inflation improves clearance, but too much inflation can block narrow routes.",
        "board_type": "table",
        "board_data": {
            "headers": ["Inflation Factor", "Effect on Planning", "Beginner Guidance"],
            "rows": [
                ["Robot Footprint Radius", "The minimum clearance — at least half the robot's width plus a margin.", "Measure the Go2 width and add 0.1–0.2 m. This is your absolute minimum inflation radius."],
                [bold("Pose Uncertainty"), "Additional margin for localization error — if the robot may be 0.1 m off, add 0.1 m.", "Larger in GPS-denied or feature-poor environments; smaller in well-mapped indoor spaces with good features."],
                ["Safety Policy", "Extra margin required by field safety rules — typically 0.2–0.5 m for classroom settings.", "Non-negotiable for student labs. The instructor sets this value; it overrides other considerations."],
                ["Narrow Passage Trade-off", "Too much inflation blocks legitimate routes through doors or corridors.", "If the robot refuses to pass through a wide-enough opening, reduce inflation slightly — but never below the minimum."],
            ]
        },
        "bottom_band": bold("Inflation test: 'My robot refuses to enter a 1.2 m corridor. The robot is 0.4 m wide. What should I check?' Answer: inflation radius — if it exceeds 0.4 m, the corridor looks blocked even though the robot physically fits.")
    },
    # ── Slide 19: Slide 18 — Obstacle Avoidance Is Not Full Navigation ──
    {
        "title": "Obstacle Avoidance Is Not Full Navigation",
        "thesis": "Obstacle avoidance helps the robot respond to nearby hazards, but it does not automatically understand the whole route. Planning chooses where to go over a larger space. Avoidance helps motion remain safe moment by moment. Beginners should not confuse reactive safety behavior with full autonomous navigation.",
        "board_type": "table",
        "board_data": {
            "headers": ["Dimension", "Obstacle Avoidance", "Full Navigation"],
            "rows": [
                ["Input", "Local sensor data — immediate surroundings.", "Global map + goal pose + local sensor data."],
                ["Time Horizon", "Seconds — the next few motion commands.", "Minutes — the complete route to the destination."],
                ["Output", "Safe velocity adjustment or stop command.", "Route waypoints + trajectory + avoidance overlay."],
                ["Answers the Question", bold("\"Is my next step safe?\""), bold("\"Where should I go, and is the path safe all the way?\"")],
                ["Fails When", "An obstacle appears inside the stopping distance.", "The global goal is unreachable or the map is wrong."],
            ]
        },
        "bottom_band": bold("Vocabulary check: 'The robot avoided the cone.' What does this mean? It means the local avoidance layer detected the cone and adjusted motion — it does NOT mean the robot planned a new global route around it.")
    },
    # ── Slide 20: Slide 19 — Unitree Avoid Mode Fits the Local Layer ──
    {
        "title": "Unitree Avoid Mode Fits the Local Layer",
        "thesis": "On the Go2, obstacle avoidance is controlled through a clear lifecycle. The program enables the avoidance client, requests command authority, sends controlled motion, stops the robot, releases authority, and disables avoid mode. This lifecycle belongs in the local safety layer of the autonomy stack.",
        "board_type": "list",
        "board_data": [
            bold("1. Enable Avoid Mode: ObstaclesAvoidClient.SwitchSet(True) and verify with SwitchGet(). The avoid service must actually be on — confirm with read-back."),
            bold("2. Gain Command Authority: UseRemoteCommandFromApi(True) transfers control from the remote to the API. Without this, your commands are ignored."),
            bold("3. Move Carefully: Send limited velocity or increment commands through the avoid service. The robot will slow or stop for nearby obstacles automatically."),
            bold("4. Stop: Send repeated Move(0, 0, 0) to halt all motion. Redundant stop commands are safer — one zero command may not be enough."),
            bold("5. Release Authority: UseRemoteCommandFromApi(False) returns control to the remote. The script must not retain control after completion."),
            bold("6. Disable Avoid: SwitchSet(False) turns off the avoid service. Clean shutdown prevents lingering command authority."),
        ],
        "bottom_band": bold("Lifecycle rule: Success, failure, and Ctrl+C paths must all converge on the same release sequence. A crash after step 2 leaves the robot in an unsafe state — always wrap in try/finally.")
    },
    # ── Slide 21: Slide 20 — Patrol Plans Are Beginner Route Contracts ──
    {
        "title": "Patrol Plans Are Beginner Route Contracts",
        "thesis": "A patrol plan is a simple route contract. It lists checkpoints, movement limits, capture expectations, and validation rules. Beginners can use it before full autonomy because it teaches disciplined route thinking. Later, the same structure can be compared with map-based goals and planner-generated paths.",
        "board_type": "grid",
        "board_data": [
            {"label": bold("Checkpoint"), "value": bold("A named stop on the route — cp_A (start), cp_B (corner), cp_C (end). Each checkpoint has an ID, label, dwell time, and optional capture requirement.")},
            {"label": bold("Motion Limit"), "value": bold("Speed cap (vx ≤ 0.25 m/s) and increment cap (dx ≤ 0.5 m). Limits are chosen for supervision and evidence quality, not for the robot's maximum capability.")},
            {"label": bold("Capture Action"), "value": bold("VideoClient.GetImageSample() at designated checkpoints — the camera records evidence after the robot stops, not during motion.")},
            {"label": bold("Validation Rule"), "value": bold("Each artifact has a structural requirement — metadata.json fields, image file size > 100 bytes, JSONL with at least one valid line.")},
        ],
        "bottom_band": bold("Patrol plan as contract: 'If I hand this plan to another team, can they execute it safely?' If the answer is no — the limits are vague, checkpoints are unnamed, or validation rules are missing — the plan is not ready for hardware.")
    },
    # ── Slide 22: Slide 21 — Debugging Habit: Separate Plan, Command, and Robot ──
    {
        "title": "Debugging Habit: Separate Plan, Command, and Robot",
        "thesis": "When motion fails, do not guess. Separate the problem into layers. First ask whether the plan is valid, then check whether the command was sent, next observe whether the robot moved as expected, and finally confirm that evidence was saved. This habit makes debugging less emotional and more systematic.",
        "board_type": "list",
        "board_data": [
            bold("1. Plan valid? Check patrol_plan.json structure — are all required fields present? Do checkpoint IDs match between checkpoints and legs? Are values within limits?"),
            bold("2. Command sent? Verify the SDK client sent the command — check console output, return codes, and any error messages. Did the client timeout or throw?"),
            bold("3. Robot moved? Observe physical behavior — did the robot move at all? In the expected direction? For the expected distance? Did it stop correctly?"),
            bold("4. Evidence saved? Check the run folder — are metadata.json, sportmodestate.jsonl, and checkpoint images present and valid? Does the validator pass?"),
        ],
        "bottom_band": bold("Debugging discipline: Before changing any code, answer all four questions. If the plan was never valid, tuning dx values will not help. If the command was never sent, the robot behavior is irrelevant.")
    },
    # ── Slide 23: Slide 22 — Section 3: Gazebo Sandbox ──
    {
        "title": "Section 3 — Gazebo Sandbox",
        "thesis": "Rehearse the inspection routine before field deployment. This section covers Gazebo as a required rehearsal space, building meaningful simulation worlds, checking simulated sensors, reading ROS 2 data flow, establishing validation gates, collecting simulation evidence, and the rule that simulation failures are fixed before hardware is touched.",
        "board_type": "grid",
        "board_data": [
            {"label": "Core Idea", "value": bold("Design in simulation → Test safely → Collect evidence → Decide readiness. Gazebo is the rehearsal space — not a replacement for hardware testing, but a required step before it.")},
            {"label": "Why Required", "value": "Simulation catches plan errors, route problems, sensor misconfigurations, and costmap issues without risking physical damage or safety incidents."},
            {"label": "ROS 2 Bridge", "value": bold("ros_gz_bridge exchanges messages between ROS 2 and Gazebo Transport. Topics like /cmd_vel, /odom, /scan, and /costmap become visible for debugging.")},
            {"label": "Section Slides", "value": "Slides 23–29: Gazebo as rehearsal, world design, sensor checking, ROS 2 topic flow, validation gates, simulation evidence, and the sim-before-hardware debugging rule."},
        ],
        "bottom_band": bold("Section rule: If a routine fails in simulation, fix it in simulation. If it passes simulation, still test hardware slowly. Simulation is a gate, not a guarantee.")
    },
    # ── Slide 24: Slide 23 — Gazebo Is the Rehearsal Space ──
    {
        "title": "Gazebo Is the Rehearsal Space",
        "thesis": bold("Gazebo is the rehearsal space for inspection routines. It allows students to test arena layout, route logic, obstacle placement, sensor assumptions, and costmap behavior before moving the physical robot. Simulation does not prove field safety, but it reduces avoidable uncertainty before hardware testing."),
        "board_type": "list",
        "board_data": [
            bold("Design: Build the arena in simulation — start zone, corridor, obstacles, inspection targets, restricted areas, finish zone. Make the world mirror the field task."),
            bold("Test: Run the patrol routine in Gazebo. Observe sensor output, route execution, obstacle avoidance behavior, and costmap updates."),
            bold("Collect Evidence: Save world screenshot, route trace, costmap snapshot, log file. Evidence lets another person understand what happened without re-running."),
            bold("Decide Readiness: Based on evidence — is the routine ready for hardware? Does it need tuning? Does it need redesign? Make an explicit decision, not an assumption."),
        ],
        "bottom_band": bold("Simulation mindset: 'I am not proving the routine works. I am finding what would fail on hardware before the hardware is at risk.' Design your simulation test to find failures, not to confirm hopes.")
    },
    # ── Slide 25: Slide 24 — Build the Inspection World on Purpose ──
    {
        "title": "Build the Inspection World on Purpose",
        "thesis": "A useful simulation world is not random decoration. It should represent the field task. Students should place a start zone, corridor boundaries, obstacles, inspection targets, restricted areas, and a finish zone. This makes the simulation test meaningful because it mirrors the decisions required during the real patrol.",
        "board_type": "grid",
        "board_data": [
            {"label": bold("Start Zone"), "value": bold("Where the robot initializes — clear of obstacles, near the first checkpoint. The simulated robot should spawn in the same pose the physical robot will start from.")},
            {"label": bold("Corridor Boundaries"), "value": "Walls, cones, or markers defining the patrol corridor. Should match the physical arena dimensions as closely as practical."},
            {"label": bold("Obstacles"), "value": "Objects the robot must avoid — placed at positions that test the costmap and avoidance response. Start with one obstacle; add more after confirming avoidance works."},
            {"label": bold("Inspection Targets"), "value": "Checkpoint locations — the robot should stop, dwell, and capture evidence here. Each target tests a different part of the route logic."},
            {"label": bold("Finish Zone"), "value": "Where the robot ends — clear of obstacles, with enough space for a clean stop and final capture."},
        ],
        "bottom_band": bold("World design test: 'Does my simulation world contain every decision the robot will face in the field?' If the field has a narrow turn but the sim doesn't, the simulation missed a critical test case.")
    },
    # ── Slide 26: Slide 25 — Simulated Sensors Must Be Checked ──
    {
        "title": "Simulated Sensors Must Be Checked",
        "thesis": "A simulated robot must provide usable sensor data. Students should confirm that camera, LiDAR, odometry, and state topics are publishing plausible information. If the simulated sensors are missing or unrealistic, the route validation becomes weak. Beginners should inspect the data before trusting the motion result.",
        "board_type": "table",
        "board_data": {
            "headers": ["Check", "What to Look For", "Red Flags"],
            "rows": [
                ["Robot Model", "Correct URDF/Xacro, joint limits, sensor plugins.", "Missing links, zero-mass bodies, sensors with no plugin."],
                ["Sensor Topics", "Topics publishing at expected rates with valid data types.", "Topics missing, publishing at 0 Hz, or with zero-filled messages."],
                ["Visualization", bold("Data visible in RViz — point clouds, laser scans, camera images."), "Data appears offset, inverted, or shows constant/default values."],
                ["Logs", "Logged values match visual inspection — ranges, timestamps, frame IDs.", "Timestamps frozen, frame IDs mismatched, ranges out of sensor spec."],
            ]
        },
        "bottom_band": bold("Sensor check rule: Before you trust the robot's motion in simulation, verify each sensor independently. A world with broken sensors trains you to ignore broken data — the opposite of what you need for hardware.")
    },
    # ── Slide 27: Slide 26 — ROS 2 Shows the Data Flow ──
    {
        "title": "ROS 2 Shows the Data Flow",
        "thesis": "In a beginner simulation workflow, ROS 2 topics make invisible data visible. Command topics show intended motion, odometry shows estimated movement, sensor topics show what the robot perceives, and costmap topics show how nearby risk is represented. This visibility helps students debug before hardware is involved.",
        "board_type": "grid",
        "board_data": [
            {"label": bold("/cmd_vel → Robot Motion"), "value": bold("Publishes geometry_msgs/Twist — linear and angular velocity commands. In simulation, this is how the robot is told to move. Compare commanded vs. actual velocity.")},
            {"label": bold("/odom → Pose Estimate"), "value": bold("Publishes odometry — position and orientation estimate from motion sensors. Drifts over time but useful for short-term motion tracking.")},
            {"label": bold("/scan or /points → Obstacles"), "value": bold("Publishes laser scan or point cloud data — what the robot detects around it. Feed this into RViz to visually confirm obstacle detection.")},
            {"label": bold("/costmap → Risk Grid"), "value": "Publishes the local costmap — the risk picture the planner reads. Watch how inflation zones expand around obstacles as the robot approaches."},
        ],
        "bottom_band": bold("Topic flow exercise: Run a simulation. Open a terminal and run rostopic list. For each topic above, run rostopic echo once and explain what the message means. If you cannot, that topic is a blind spot in your understanding.")
    },
    # ── Slide 28: Slide 27 — Validate the Routine Before the Robot Moves ──
    {
        "title": "Validate the Routine Before the Robot Moves",
        "thesis": "Validation is a gate, not a formality. Before hardware movement, students should verify that the plan file is valid, the route appears correctly, obstacles are detected, the simulated robot avoids collisions, and logs are saved. A failed validation means the system is protecting the field test.",
        "board_type": "list",
        "board_data": [
            bold("Plan file valid: All required fields present; checkpoint IDs match; motion values within limits; JSON structure parses without errors."),
            bold("Route visible: The planned path appears correctly on the map — no segments through walls, no impossible turns, no self-intersections."),
            bold("Obstacles detected: Sensor data shows obstacles at expected positions; costmap marks them correctly; inflation zones provide adequate clearance."),
            bold("No collision: The simulated robot completes the route without contacting obstacles, crossing safety boundaries, or entering restricted zones."),
            bold("Logs saved: All evidence artifacts exist — world screenshot, route trace, costmap snapshot, log file, short conclusion statement."),
        ],
        "bottom_band": bold("Validation gate rule: PASS → proceed to hardware (slowly). FAIL → fix the issue and re-validate. WARNING → document the concern and get instructor approval before hardware. Never skip validation because 'it will probably be fine.'")
    },
    # ── Slide 29: Slide 28 — Simulation Evidence Should Be Reviewable ──
    {
        "title": "Simulation Evidence Should Be Reviewable",
        "thesis": "Simulation evidence should let another person understand what happened. Students should save a world screenshot, route trace, costmap snapshot, log file, and short conclusion. The conclusion should state whether the routine is ready for field testing, needs tuning, or must be redesigned.",
        "board_type": "grid",
        "board_data": [
            {"label": bold("World Screenshot"), "value": "Top-down view of the simulation world with the robot's path overlaid. Shows the arena layout and the complete route in one image."},
            {"label": bold("Route Trace"), "value": bold("Plot of the robot's actual trajectory vs. the planned path. Deviations, overshoots, and correction points are visible.")},
            {"label": bold("Costmap Snapshot"), "value": bold("Screenshot of the local costmap at a critical moment — e.g., the narrowest turn or closest obstacle approach.")},
            {"label": bold("Log File"), "value": "Sensor topics, command messages, and state data saved during the run. Timestamps allow correlation with screenshots."},
            {"label": bold("Short Conclusion"), "value": bold("One explicit statement: ready for hardware / needs tuning (list what) / must be redesigned (explain why). No hedging.")},
        ],
        "bottom_band": bold("Reviewability test: 'If I give this evidence folder to someone who did not watch the simulation, can they: (a) understand what happened, (b) identify any problems, and (c) decide whether to proceed?' If any answer is no, add evidence.")
    },
    # ── Slide 30: Slide 29 — Debugging Habit: Simulation Before Hardware ──
    {
        "title": "Debugging Habit: Simulation Before Hardware",
        "thesis": "If a routine fails in simulation, fix it before using hardware. If it passes simulation, do not assume the real robot will behave perfectly. Start slowly, use small motion commands, keep a stop procedure ready, and compare field results against simulation evidence.",
        "board_type": "list",
        "board_data": [
            bold("Rule 1 — Fix in sim first: A failure in Gazebo means something is wrong with the plan, sensors, or logic. Fix it where it is safe and fast to iterate."),
            bold("Rule 2 — Passing sim is not a guarantee: Hardware introduces network latency, floor texture, lighting, battery state, and sensor noise that simulation cannot fully capture."),
            bold("Rule 3 — Start hardware slowly: First test = small speed, short duration, clear arena. Stop and review behavior before increasing scope."),
            bold("Rule 4 — Keep a stop procedure: Agree on who calls stop, how to stop (remote, script, or physical), and what conditions trigger an immediate halt."),
            bold("Rule 5 — Compare sim vs. hardware: After the field test, overlay the hardware route trace on the simulation route trace. Differences are evidence of real-world effects."),
        ],
        "bottom_band": bold("Conservative rule: 'Simulation is where you earn confidence. Hardware is where you confirm it cautiously.' Never reverse the order — hardware is not for debugging obvious plan errors.")
    },
    # ── Slide 31: Slide 30 — Section 4: Physical Go2 Handoff ──
    {
        "title": "Section 4 — Physical Go2 Handoff",
        "thesis": "Move from simulation evidence to controlled field testing. This section covers the handoff as a controlled process, network readiness checks, intentional command authority, staged motion testing, hardware-in-the-loop comparison, evidence-based claims, and the one-change-at-a-time experimental discipline.",
        "board_type": "grid",
        "board_data": [
            {"label": "Core Idea", "value": bold("Validated plan → Network check → Robot state check → Safe command authority → Field run. Handoff is a controlled process, not just copying a file.")},
            {"label": "Key Principle", "value": "Many field failures are network failures disguised as robot failures. Check connectivity, interface, DDS discovery, and topic visibility before debugging autonomy."},
            {"label": "Safety Rule", "value": "Command authority defines who controls the robot. Request only when ready, send limited commands, stop cleanly, release afterward. Treat it seriously."},
            {"label": "Section Slides", "value": "Slides 31–37: Controlled handoff, network readiness, command authority lifecycle, staged field testing, hardware-in-the-loop, evidence-based claims, and one-variable-at-a-time debugging."},
        ],
        "bottom_band": bold("Section rule: The first hardware test is not a full-speed patrol. It is a slow, short, supervised motion — then stop, review, and decide whether to expand.")
    },
    # ── Slide 32: Slide 31 — Handoff Means More Than Copying a File ──
    {
        "title": "Handoff Means More Than Copying a File",
        "thesis": "Hardware handoff is not simply copying a patrol file onto a machine. It is a controlled process. Students must confirm that the plan passed validation, the network is connected, robot state is safe, command authority is understood, and the field operator is ready before motion begins.",
        "board_type": "list",
        "board_data": [
            bold("1. Validated Plan: The patrol plan passed simulation validation. Artifacts exist — world screenshot, route trace, costmap snapshot, conclusion."),
            bold("2. Network Check: Robot is reachable (ping 192.168.123.161), correct interface is active (en6, eth0), DDS discovery works, topics or SDK responses are visible."),
            bold("3. Robot State Check: Posture is safe (BalanceStand confirmed), SportModeState is normal, battery is adequate, no error codes active."),
            bold("4. Safe Command Authority: Operator understands who has control (remote vs. API). UseRemoteCommandFromApi(True) is intentional and documented."),
            bold("5. Field Operator Ready: Spotter in position, arena marked, stop procedure agreed, abort rules reviewed, one-patrol-at-a-time rule enforced."),
        ],
        "bottom_band": bold("Handoff test: 'Before I run a single motion command, can I answer: is the network up, is the robot state safe, who has command authority, and what is the stop procedure?' If any answer is no, do not proceed.")
    },
    # ── Slide 33: Slide 32 — Network Readiness Comes First ──
    {
        "title": "Network Readiness Comes First",
        "thesis": "Many field failures are network failures disguised as robot failures. Before debugging autonomy, students should confirm the robot is reachable, the correct network interface is active, DDS discovery works, and expected topics or SDK responses are visible. Connectivity is the foundation for safe command and logging.",
        "board_type": "table",
        "board_data": {
            "headers": ["Check", "Command / Action", "Expected Result"],
            "rows": [
                [bold("Robot Reachable"), bold("ping 192.168.123.161"), "Consistent replies, latency < 5 ms, no packet loss."],
                [bold("Correct Interface"), bold("ip addr — identify the robot-facing adapter (en6, eth0, enp3s0)."), bold("Interface has IP on 192.168.123.x subnet, NOT .161 (the robot's onboard address).")],
                [bold("DDS Discovery"), bold("Initialize ChannelFactoryInitialize(0, \"<interface>\") without errors."), bold("SDK clients initialize; no CycloneDDS domain mismatch or discovery timeout.")],
                [bold("Topics Visible"), bold("Subscriber callbacks fire; SportModeState_ messages arrive."), "State messages contain valid mode, gait, position, velocity fields — not defaults or zeros."],
            ]
        },
        "bottom_band": bold("Network-first rule: If the robot is not reachable, nothing else matters. Do not debug autonomy, planning, or costmaps — debug the network. Connectivity problems are the #1 cause of beginner field failures.")
    },
    # ── Slide 34: Slide 33 — Command Authority Must Be Intentional ──
    {
        "title": "Command Authority Must Be Intentional",
        "thesis": "Command authority defines who is allowed to control the robot. Beginners must treat it seriously. The program should request authority only when ready, send limited commands, stop cleanly, and release authority afterward. This prevents confusion between manual control, SDK control, and emergency intervention.",
        "board_type": "list",
        "board_data": [
            bold("Request authority only when ready: UseRemoteCommandFromApi(True) is called after all checks pass — network, state, plan, operator. Not during initialization as a default."),
            bold("Send limited commands: Speed ≤ 0.25 m/s, increment ≤ 0.5 m, short duration. The first command should be the smallest meaningful motion possible."),
            bold("Stop cleanly: Move(0, 0, 0) sent repeatedly; SportClient.StopMove() as backup. Stop is as important as move — a script that can start but not stop is unsafe."),
            bold("Release authority afterward: UseRemoteCommandFromApi(False) and SwitchSet(False) in a finally block. Authority must not linger after the script exits."),
        ],
        "bottom_band": bold("Authority question: At any moment, ask: 'Who currently has command authority?' If the answer is unclear — the remote might be connected, the app might be open, another script might be running — stop and resolve before motion.")
    },
    # ── Slide 35: Slide 34 — Start with Small Field Motions ──
    {
        "title": "Start with Small Field Motions",
        "thesis": "The first hardware test should not be a full-speed patrol. Students should start with small speeds and short durations, then stop and review behavior. If the robot moves as expected, the test can expand gradually. This staged approach reduces risk and gives students time to learn from evidence.",
        "board_type": "list",
        "board_data": [
            bold("Stage 1 — Single small increment: One dx = 0.2 m forward. Stop. Review state log. Confirm the robot moved ~0.2 m, not 0.5 m or 0.0 m."),
            bold("Stage 2 — Increment + turn: One dx = 0.3 m, one dyaw = 0.3 rad. Stop. Review. Did the robot turn approximately the expected angle?"),
            bold("Stage 3 — Two-leg sequence: Forward to cp_B, turn, forward to cp_C. Capture at each checkpoint. Run validator. Review all artifacts."),
            bold("Stage 4 — Full patrol at low speed: Complete the patrol plan at minimum speeds. Compare with simulation route trace. Identify deviations."),
            bold("Stage 5 — Tuned patrol: One parameter change (e.g., increase leg 1 dx by 0.1 m). Compare baseline vs. tuned. Document the difference."),
        ],
        "bottom_band": bold("Staging rule: Never jump from simulation to full-speed patrol. Each stage confirms one new capability. If a stage fails, fix it before adding complexity.")
    },
    # ── Slide 36: Slide 35 — Hardware-in-the-Loop Tests Close the Gap ──
    {
        "title": "Hardware-in-the-Loop Tests Close the Gap",
        "thesis": "Simulation cannot capture every real-world effect. Hardware-in-the-loop testing exposes network latency, floor texture, sensor noise, lighting, battery condition, and physical dynamics. The purpose is not to prove simulation wrong — it is to compare expectations against reality and improve the routine responsibly.",
        "board_type": "table",
        "board_data": {
            "headers": ["Real-World Effect", "Simulation Gap", "Hardware Observation Method"],
            "rows": [
                ["Network Latency", "Simulation assumes instantaneous or low-latency communication.", bold("Timestamp command send time and state receipt time; compute round-trip delay.")],
                ["Floor Texture", "Simulation floor is uniform friction; real floors vary (carpet, tile, concrete).", "Compare odometry-reported distance with measured physical distance."],
                ["Sensor Noise", "Simulated sensors add modeled noise; real noise patterns are more complex.", bold("Plot sensor values over time during a static robot — noise floor should be visible.")],
                ["Lighting", "Simulation lighting is controlled; real lighting changes throughout the day.", "Capture checkpoint images at the same location under different lighting conditions."],
            ]
        },
        "bottom_band": bold("Comparison mindset: 'The simulation predicted X. The hardware showed Y. The difference Z tells me something about the real world.' Document Z — that is your engineering insight, not a failure.")
    },
    # ── Slide 37: Slide 36 — Field Evidence Must Match the Claim ──
    {
        "title": "Field Evidence Must Match the Claim",
        "thesis": "Every field claim needs matching evidence. If students claim the robot avoided an obstacle, they should show the field video, command log, stop event, or route trace. If they claim the plan is reliable, they should show repeated runs. Evidence turns a demo into an engineering result.",
        "board_type": "table",
        "board_data": {
            "headers": ["Claim", "Required Evidence", "Insufficient Evidence"],
            "rows": [
                [bold("\"The robot avoided the obstacle.\""), bold("Video of approach + costmap showing obstacle + velocity change before contact."), bold("'I saw it turn' — memory is not evidence.")],
                [bold("\"The plan is reliable.\""), bold("Three repeated runs with route traces overlaid, all within tolerance."), "One successful run — reliability requires repetition."],
                [bold("\"The checkpoint was reached.\""), bold("Checkpoint frame.jpg showing the expected scene + state slice showing velocity ≈ 0."), bold("Metadata entry alone — image content matters more than structural presence.")],
                [bold("\"The robot stopped safely.\""), bold("Velocity plot showing vx → 0 within expected time; no residual drift."), bold("'It looked stopped' — measure, do not estimate.")],
            ]
        },
        "bottom_band": bold("Evidence test: 'If someone disputes your claim, what artifact would you show to prove it?' If you cannot name a specific file, image, plot, or log entry, your claim is not yet evidence-backed.")
    },
    # ── Slide 38: Slide 37 — Debugging Habit: Change One Thing at a Time ──
    {
        "title": "Debugging Habit: Change One Thing at a Time",
        "thesis": "When field tests fail, beginners may change speed, route, sensor settings, and code all at once. That makes learning impossible. Change one variable at a time, run the test, save the log, write one conclusion. This habit makes tuning slower at first but much more reliable.",
        "board_type": "grid",
        "board_data": [
            {"label": bold("One Change"), "value": bold("Modify exactly one parameter — leg dx, turn dyaw, dwell time, or speed cap. Document: what changed, old value, new value, why this change.")},
            {"label": bold("One Run"), "value": bold("Execute the patrol under the same conditions as the baseline — same arena, same lighting, same operator. Only the one parameter differs.")},
            {"label": bold("One Log"), "value": bold("Save the complete run folder with a descriptive name — e.g., run_field_tuned_dx_0.4. The name should encode the change.")},
            {"label": bold("One Conclusion"), "value": bold("State what the change did: 'dx 0.3→0.4 reduced under-shoot at cp_B from ~0.15 m to ~0.03 m.' Or: 'Change had no measurable effect — dx is not the limiting factor.'")},
        ],
        "bottom_band": bold("Experimental discipline: If you change dx, dyaw, and dwell simultaneously and the robot reaches the checkpoint, you learned nothing about which change mattered. Control one variable to learn one lesson.")
    },
    # ── Slide 39: Slide 38 — Section 5: Capstone and Practical Habits ──
    {
        "title": "Section 5 — Capstone and Practical Habits",
        "thesis": "Combine SLAM, planning, simulation, and field evidence into an integrated capstone demonstration. This section covers the five-step capstone expectation, a reusable beginner debugging checklist, evidence habits for reproducible runs, and the final takeaway that good autonomy is motion with explanation, validation, and evidence.",
        "board_type": "grid",
        "board_data": [
            {"label": "Core Idea", "value": "The capstone is not judged only by whether the robot moves. Students explain the map, justify the route, validate in Gazebo, test on Go2, and report evidence."},
            {"label": "Debugging Checklist", "value": bold("Power → Network → Topics → Frames → Plan → Simulation → Command → Logs. Move through layers in order — most issues resolve before you reach the bottom.")},
            {"label": "Evidence Habit", "value": bold("Run folder = plan + settings + logs + screenshots + conclusion. Name folders by date, scenario, and attempt so results can be compared later.")},
            {"label": "Section Slides", "value": "Slides 39–42: Capstone integration, debugging checklist, reproducible run folders, and the final takeaway that autonomy is evidence-based."},
        ],
        "bottom_band": bold("Capstone mindset: Your presentation should let someone who never attended this class understand what you did, why it was safe, what evidence you collected, and what you would change next.")
    },
    # ── Slide 40: Slide 39 — The Capstone Connects Every Layer ──
    {
        "title": "The Capstone Connects Every Layer",
        "thesis": "The capstone should not be judged only by whether the robot moves. Students must explain the map or spatial assumptions, justify the route, validate behavior in Gazebo, run a controlled Go2 field test, and report evidence. This connects the full academic scope of Day 2.",
        "board_type": "list",
        "board_data": [
            bold("1. Explain the map: Show the occupancy grid or spatial assumptions. What does the robot know about the environment? What is the coordinate frame layout?"),
            bold("2. Justify the route: Present the patrol plan or planner output. Why this path? How do costmaps and inflation protect the robot at each turn?"),
            bold("3. Validate in Gazebo: Show simulation evidence — world screenshot, route trace, costmap snapshot, log file. State the validation outcome explicitly."),
            bold("4. Test on Go2: Present hardware results — field video, command log, checkpoint images, validator output. Compare hardware route trace with simulation trace."),
            bold("5. Report evidence: Provide the run folder with all artifacts. State one tuning action, one failure encountered or avoided, and one next improvement."),
        ],
        "bottom_band": bold("Capstone test: 'If I only read your evidence folder — no live demo, no verbal explanation — would I understand what happened and whether the routine was safe?' If the answer is no, add evidence until it is yes.")
    },
    # ── Slide 41: Slide 40 — Beginner Debugging Checklist ──
    {
        "title": "Beginner Debugging Checklist",
        "thesis": "A beginner debugging checklist prevents panic. Start with power and safety, check network connectivity, confirm topics or SDK responses, verify coordinate frames, validate the plan, test in simulation, send limited commands, and save logs. Most robotics debugging becomes manageable when students move through layers in order.",
        "board_type": "list",
        "board_data": [
            bold("Power: Is the robot on? Battery adequate? Emergency stop accessible? No error lights or warning beeps."),
            bold("Network: Can you ping the robot? Correct interface active? DDS discovery working? No IP conflicts on the subnet."),
            bold("Topics: Are expected topics publishing? Are message rates normal? Are timestamps current? No stale or zero-filled data."),
            bold("Frames: Does the transform tree exist? Are all expected frames connected? Are timestamps synchronized across frames?"),
            bold("Plan: Is the plan file valid? All fields present? Values within limits? Checkpoint IDs consistent between checkpoints and legs?"),
            bold("Simulation: Does the routine pass in Gazebo? Has evidence been collected? Is the conclusion explicit about readiness?"),
            bold("Command: Are commands being sent? Any error returns or timeouts? Is command authority explicitly controlled?"),
            bold("Logs: Are logs being written? Are files non-empty? Does the validator pass? Can another person understand the run folder?"),
        ],
        "bottom_band": bold("Checklist discipline: When something fails, start at the top and work down. Do not skip layers. 'My robot isn't moving' could be a dead battery (Power), a disconnected cable (Network), or a missing authority request (Command) — the checklist catches all three.")
    },
    # ── Slide 42: Slide 41 — Evidence Habit: Make Every Run Reproducible ──
    {
        "title": "Evidence Habit: Make Every Run Reproducible",
        "thesis": "A reproducible run folder lets another person understand and repeat the test. It should include the plan file, key settings, logs, screenshots, captured images, and a short conclusion. Students should name folders clearly by date, scenario, and attempt number so results can be compared later.",
        "board_type": "grid",
        "board_data": [
            {"label": bold("Plan File"), "value": bold("The exact patrol_plan.json or planner configuration used — not a similar version, not 'approximately what we ran.'")},
            {"label": bold("Key Settings"), "value": bold("Speed limits, increment caps, inflation radius, costmap parameters, interface name, DDS domain. Anyone should be able to recreate the configuration.")},
            {"label": bold("Logs"), "value": bold("State logs (sportmodestate.jsonl), command logs, sensor data snapshots. Timestamps allow correlation between events.")},
            {"label": bold("Visual Evidence"), "value": "World screenshot, route trace, costmap snapshot, checkpoint images, field video or photo. Visual evidence answers questions text cannot."},
            {"label": bold("Short Conclusion"), "value": bold("One paragraph: what was tested, what passed, what failed, what was changed, what should be tested next. No hedging, no unexplained success.")},
        ],
        "bottom_band": bold("Reproducibility test: 'Can someone else, using only this run folder, recreate the test and get similar results?' If not, what is missing? Add it and re-run.")
    },
    # ── Slide 43: Slide 42 — Final Takeaway: Autonomy Is Evidence-Based ──
    {
        "title": "Final Takeaway: Autonomy Is Evidence-Based",
        "thesis": "Good autonomy is not just motion. Good autonomy is motion with explanation, validation, and evidence. Students should learn to explain the system, validate the routine, test carefully, and preserve evidence. This beginner habit prepares them for more advanced SLAM, navigation, costmap tuning, and field autonomy work.",
        "board_type": "grid",
        "board_data": [
            {"label": bold("Explanation"), "value": bold("Can you explain the autonomy stack — sensors, fusion, SLAM, planning, costmaps, control — in plain language? Can you draw the data flow from /cmd_vel to robot motion to evidence?")},
            {"label": bold("Validation"), "value": bold("Did the routine pass structured validation gates in simulation? Were all artifacts collected? Was the readiness decision explicit and documented?")},
            {"label": bold("Evidence"), "value": bold("Does every claim have a matching artifact? If you say 'the robot avoided the obstacle,' can you show the costmap, video, or velocity plot that proves it?")},
            {"label": bold("Next Steps"), "value": "Day 3 builds on this foundation — more complex SLAM configurations, advanced costmap tuning, multi-sensor calibration, and longer autonomous patrol sequences."},
        ],
        "bottom_band": bold("Day 2 closing message: 'You now understand autonomy not as magic, but as a layered, testable, evidence-producing engineering discipline. Carry that mindset into every future robotics project.'")
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

print(f"Generated {len(SLIDES)} slides block ({len(slides_py)} chars)")
print("Slides:")
for i, s in enumerate(SLIDES):
    print(f"  {i+1:2d}. [{s['board_type']:5s}] {s['title'][:80]}")

# ── Replace in build_syllabus.py ──
build_path = "build_syllabus.py"
with open(build_path) as f:
    content = f.read()

# Find the slides array and replace
start_marker = '    "slides": ['
end_marker = '\n    "labs": ['

start_idx = content.index(start_marker)
end_idx = content.index(end_marker, start_idx)

new_content = content[:start_idx] + slides_py + content[end_idx:]

with open(build_path, "w") as f:
    f.write(new_content)

print(f"\nReplaced slides array in {build_path}")
print(f"Old slides block: {end_idx - start_idx} chars")
print(f"New slides block: {len(slides_py)} chars")
print("Done. Run build_syllabus_final.py to regenerate syllabus.json.")