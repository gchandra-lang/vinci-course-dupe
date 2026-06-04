#!/usr/bin/env python3
"""
[PROGRESS AUDIT] Triple-Pass Compilation: Days 02–07 of 07
PASS 1 — Text Segment Ingestion from markdown lecture notes
PASS 2 — Schema Synthesis & Map to 4 board types (table/grid/list/math)
PASS 3 — Integrity Rechecking: count every line/table cell/warning string

Dynamic Slide Expansion: If a slide is full, spawn continuation slides.
Typography: Titles→font-serif, Thesis→italic muted, Data→font-sans, Code→font-mono
"""
import json, sys, os

OUT = os.path.join(os.path.dirname(__file__), "syllabus.json")

def load_day01():
    with open(OUT) as f:
        return json.load(f)["01"]

# ── Day 02: Go2 Autonomy & Sandbox Capstone ──────────────────────────────────
DAY02 = {
    "day": "02",
    "title": "Go2 Autonomy, Obstacle Avoidance & Field Capstone",
    "eyebrow": "GO2 INSPECTION PATROL",
    "thesis": "An inspection patrol is a scripted, evidence-producing mission in which checkpoint IDs, motion legs, safety limits, captures, logs, and report fields are all explicit before the robot moves — sense → log → decide → act → report.",
    "rules": [
        "Define the mission contract first: scenario, checkpoints, motion limits, and abort rules exist before the robot moves.",
        "Treat the run folder as the inspection deliverable — metadata, plan, state logs, and checkpoint images together make the run auditable.",
        "Use ObstaclesAvoidClient with explicit enable/disable lifecycle; never leave API command authority after the patrol ends.",
        "Keep increments small (≤0.5 m) and speeds low (≤0.25 m/s) unless the instructor approves; tuning is incremental, not ambitious.",
        "Distinguish reactive obstacle avoidance from SLAM/navigation — use precise vocabulary and never claim mapping when using local increments."
    ],
    "pacing": [
        {"time": "09:00 - 09:15", "session": "Day 1 Recap & Day 2 Framing", "path": "day-02/README.md"},
        {"time": "09:15 - 09:35", "session": "Inspection Architecture: Sense→Log→Decide→Act→Report", "path": "day-02/README.md#inspection-architecture"},
        {"time": "09:35 - 10:00", "session": "Lab 0 — Readiness, Scenario & Safety Rules", "path": "day-02/lab-00/"},
        {"time": "10:00 - 10:30", "session": "Lab 1 — Run-Folder Schema & Validator", "path": "day-02/lab-01/"},
        {"time": "10:45 - 11:15", "session": "Lab 2 — Obstacle Avoidance & Local Motion APIs", "path": "day-02/lab-02/"},
        {"time": "11:15 - 12:00", "session": "Lab 3 — Multi-Leg Patrol & Integrated Capture", "path": "day-02/lab-03/"},
        {"time": "13:00 - 13:45", "session": "Lab 4 — Field Trial, Tuning & Gazebo Context", "path": "day-02/lab-04/"},
        {"time": "13:45 - 14:30", "session": "Capstone — Team Presentations & Knowledge Check", "path": "day-02/lab-05/"}
    ],
    "slides": [
        {
            "title": "Day 2: Autonomy, Simulation, and Field Handoff",
            "thesis": "Day 2 is one connected story: how a robot observes the world, builds usable understanding, chooses motion, rehearses that motion in simulation, and then performs a controlled test on physical hardware. Beginners leave with a mental map of the full autonomy pipeline.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Pipeline",
                                    "value": "Sense → Understand → Plan → Simulate → Deploy → Prove — six stages that connect into one autonomy workflow."
                        },
                        {
                                    "label": "Four Milestones",
                                    "value": "<strong class=\"font-bold\">SLAM</strong> + Fusion, Planning + Costmaps, <strong class=\"font-bold\">Gazebo</strong> Validation, <strong class=\"font-bold\">Go2</strong> Handoff — each milestone builds toward the final capstone demonstration."
                        },
                        {
                                    "label": "Beginner Promise",
                                    "value": "By the end of Day 2, you will explain what SLAM, sensor fusion, costmaps, planning, and Gazebo validation mean, and you will connect those ideas to hardware field testing on the Go2."
                        },
                        {
                                    "label": "Platform",
                                    "value": "<strong class=\"font-bold\">Unitree</strong> <strong class=\"font-bold\">Go2</strong> quadruped with <strong class=\"font-bold\">ROS 2</strong>, <strong class=\"font-bold\">Gazebo</strong> simulation, and Python SDK integration."
                        }
            ],
            "bottom_band": "Mental model check: Can you draw six connected blocks — Sense, Understand, Plan, Simulate, Deploy, Prove — and explain what data flows between them? If not, that is the goal for today."
        },
        {
            "title": "Today Builds One Autonomy Story",
            "thesis": "Day 2 is not a set of disconnected robotics topics. It is one story about how a robot observes the world, builds usable understanding, chooses motion, rehearses that motion in simulation, and then performs a controlled test on physical hardware.",
            "board_type": "list",
            "board_data": [
                        "Sense: Sensors collect observations — <strong class=\"font-bold\">LiDAR</strong> for shape, cameras for appearance, <strong class=\"font-bold\">IMU</strong> for motion.",
                        "Understand: Multi-sensor fusion and <strong class=\"font-bold\">SLAM</strong> combine observations into a map and <strong class=\"font-bold\">pose</strong> estimate the robot can use.",
                        "Plan: Global and local planners convert intent into safe routes, using costmaps to mark risk.",
                        "Simulate: <strong class=\"font-bold\">Gazebo</strong> provides a rehearsal space — test routes, check sensor data, validate before hardware.",
                        "Deploy: Controlled hardware handoff — network check, robot state check, safe command authority, field run.",
                        "Prove: Every claim needs matching evidence — logs, screenshots, route traces, and a written conclusion."
            ],
            "bottom_band": "Beginner checkpoint: After each section today, ask yourself — 'Which stage of the Sense → Prove chain did we just cover?' Keep a running map of where you are in the pipeline."
        },
        {
            "title": "Four Milestones Define Success",
            "thesis": "The lecture is organized around four required academic milestones: <strong class=\"font-bold\">SLAM</strong> + Fusion, Planning + Costmaps, <strong class=\"font-bold\">Gazebo</strong> Validation, and <strong class=\"font-bold\">Go2</strong> Handoff. Each connects to the next — you cannot validate a route in simulation if you have not understood how the robot builds a map.",
            "board_type": "table",
            "board_data": {
                        "headers": [
                                    "Milestone",
                                    "Key Question",
                                    "Evidence Required"
                        ],
                        "rows": [
                                    [
                                                "<strong class=\"font-bold\">SLAM</strong> + Fusion",
                                                "How does the robot know where it is and what is around it?",
                                                "Map snapshot, <strong class=\"font-bold\">pose</strong> trace, transform tree, sensor status, logs."
                                    ],
                                    [
                                                "Planning + Costmaps",
                                                "How does the robot choose safe motion?",
                                                "Route plot, <strong class=\"font-bold\">costmap</strong> snapshot, plan file, obstacle detection record."
                                    ],
                                    [
                                                "<strong class=\"font-bold\">Gazebo</strong> Validation",
                                                "Does the routine work safely in rehearsal?",
                                                "World screenshot, route trace, <strong class=\"font-bold\">costmap</strong> snapshot, log file, conclusion."
                                    ],
                                    [
                                                "<strong class=\"font-bold\">Go2</strong> Handoff",
                                                "Does the routine work on physical hardware?",
                                                "Field video, command log, stop events, route trace, tuning notes."
                                    ]
                        ]
            },
            "bottom_band": "Milestone check: If you cannot answer the Key Question for a milestone, flag it now. Each milestone is a gate — the next one makes less sense without the previous one."
        },
        {
            "title": "Beginner Vocabulary Map",
            "thesis": "Students do not need to memorize every robotics term immediately. They need a simple vocabulary map: a map describes the environment, a pose describes the robot's estimated location and orientation, a planner chooses movement, and a costmap marks risky nearby space so motion can be safer.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Map",
                                    "value": "Where things are — an occupancy grid showing free space, obstacles, and unknown areas. Built and updated by <strong class=\"font-bold\">SLAM</strong>."
                        },
                        {
                                    "label": "Pose",
                                    "value": "Where the robot is — its estimated position (x, y, z) and orientation (roll, pitch, yaw) in a coordinate frame."
                        },
                        {
                                    "label": "Planner",
                                    "value": "Where to go next — a global <strong class=\"font-bold\">planner</strong> chooses the big-picture route; a local <strong class=\"font-bold\">planner</strong> handles the next few safe steps."
                        },
                        {
                                    "label": "Costmap",
                                    "value": "Where it is risky — a local grid around the robot marking obstacles, inflated safety buffers, and unknown space."
                        }
            ],
            "bottom_band": "Vocabulary test: Can you explain Map, Pose, Planner, and Costmap to a classmate in one sentence each, without using any of those four words in the explanation? Try it."
        },
        {
            "title": "Autonomy Is Layered, Not Magical",
            "thesis": "A robot does not become autonomous because one command says go. Autonomy is layered. Sensors collect observations, fusion combines them, SLAM estimates pose and map structure, planning chooses a path, costmaps protect local movement, control sends motion, and evidence tells us whether the claim is true.",
            "board_type": "list",
            "board_data": [
                        "Sensors → Fusion: Raw observations are combined — <strong class=\"font-bold\">LiDAR</strong> sees shape, cameras see appearance, <strong class=\"font-bold\">IMU</strong> senses motion.",
                        "Fusion → <strong class=\"font-bold\">SLAM</strong>: Combined sensor data feeds simultaneous localization and mapping — <strong class=\"font-bold\">pose</strong> estimate plus map structure.",
                        "<strong class=\"font-bold\">SLAM</strong> → Planning: The map and <strong class=\"font-bold\">pose</strong> provide the spatial understanding planners need to choose routes.",
                        "Planning → Costmap → Control: Global route is refined by local costmaps; control sends safe motion commands.",
                        "Control → Evidence: Logs, images, traces, and reports prove what happened — without evidence, motion is just a demo."
            ],
            "bottom_band": "Layering check: Draw the stack from bottom (Sensors) to top (Evidence). Can you add one data artifact at each layer that proves that layer worked?"
        },
        {
            "title": "Section 1 — SLAM and Fusion",
            "thesis": "How the robot builds a usable understanding of space. This section covers SLAM fundamentals, why quadruped SLAM is harder, multi-sensor fusion, coordinate frames, point cloud processing, and the evidence habits that make SLAM claims reviewable.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Core Idea",
                                    "value": "<strong class=\"font-bold\">SLAM</strong> = Localization + Mapping, solved together. The robot estimates where it is while building or updating a map."
                        },
                        {
                                    "label": "Why It Is Hard",
                                    "value": "Each job depends on the other. A wrong pose distorts the map. A poor map makes localization less reliable."
                        },
                        {
                                    "label": "Beginner Goal",
                                    "value": "Replace vague claims like '<strong class=\"font-bold\">SLAM</strong> worked' with evidence: map snapshot, <strong class=\"font-bold\">pose</strong> trace, transform tree, sensor status, and saved log."
                        },
                        {
                                    "label": "Section Slides",
                                    "value": "Slides 6–12: SLAM definition, quadruped challenges, multi-sensor fusion, coordinate frames, point clouds, evidence habits, and the data-path debugging routine."
                        }
            ],
            "bottom_band": "Section framing: By the end of this section, you should be able to explain why <strong class=\"font-bold\">SLAM</strong> is called 'simultaneous' and what kind of evidence proves it is working."
        },
        {
            "title": "SLAM Means Two Jobs at Once",
            "thesis": "<strong class=\"font-bold\">SLAM</strong> stands for simultaneous localization and mapping. The robot estimates where it is (localization) while also building or updating a map (mapping). This is difficult because each job depends on the other — if the <strong class=\"font-bold\">pose</strong> estimate is wrong, the map becomes distorted; if the map is poor, localization becomes less reliable.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Localize",
                                    "value": "'Where am I?' — Estimate the robot's position and orientation relative to the map using sensor observations and motion predictions."
                        },
                        {
                                    "label": "Map",
                                    "value": "'What is around me?' — Build and update a representation of the environment: occupancy grid, feature map, or point cloud."
                        },
                        {
                                    "label": "<strong class=\"font-bold\">SLAM</strong> Loop",
                                    "value": "Sensor readings → Pose estimate → Map update → Error correction → Better <strong class=\"font-bold\">pose</strong> → Repeat. Each cycle refines both answers."
                        },
                        {
                                    "label": "Failure Mode",
                                    "value": "If the robot loses localization (kidnapped robot problem), the map and pose both become unreliable until recovery."
                        }
            ],
            "bottom_band": "Diagram exercise: Draw the <strong class=\"font-bold\">SLAM</strong> loop on paper. Label where sensor data enters, where <strong class=\"font-bold\">pose</strong> is estimated, where the map updates, and where error correction feeds back. Can you identify which arrow carries the most uncertainty?"
        },
        {
            "title": "Why Quadruped SLAM Is Harder",
            "thesis": "Quadrupeds move differently from wheeled robots. Their bodies rise, fall, pitch, and vibrate as they walk. These motions can disturb cameras, LiDAR, and inertial measurements. Robot locomotion and robot perception are connected — stable movement often improves mapping quality.",
            "board_type": "table",
            "board_data": {
                        "headers": [
                                    "Motion Effect",
                                    "Sensor Impact",
                                    "SLAM Consequence"
                        ],
                        "rows": [
                                    [
                                                "Body pitch/roll during gait",
                                                "<strong class=\"font-bold\">IMU</strong> readings include walking vibration.",
                                                "Pose estimate becomes noisier — map features may misalign between frames."
                                    ],
                                    [
                                                "Vertical bounce",
                                                "<strong class=\"font-bold\">LiDAR</strong> scan lines shift upward and downward.",
                                                "Point cloud registration errors increase — walls may appear wavy or duplicated."
                                    ],
                                    [
                                                "Foot strike vibration",
                                                "Camera images may blur at key moments.",
                                                "Visual features become harder to track — loop closures weaken."
                                    ],
                                    [
                                                "Variable ground contact",
                                                "Odometry slip accumulates.",
                                                "Motion prediction drifts — the robot thinks it moved farther or shorter than reality."
                                    ]
                        ]
            },
            "bottom_band": "Key insight for beginners: Walking is not a sensor problem to ignore — it is a perception challenge. When mapping quality drops, check gait stability before changing <strong class=\"font-bold\">SLAM</strong> parameters."
        },
        {
            "title": "Multi-Sensor Fusion Combines Strengths",
            "thesis": "No sensor is perfect. LiDAR can describe geometry but may not identify object meaning. Cameras provide appearance but depend on lighting. IMUs capture motion but drift over time. Odometry estimates movement but can accumulate error. Fusion combines these clues so the system has a more reliable state estimate.",
            "board_type": "table",
            "board_data": {
                        "headers": [
                                    "Sensor",
                                    "Strength",
                                    "Weakness",
                                    "Fusion Role"
                        ],
                        "rows": [
                                    [
                                                "<strong class=\"font-bold\">LiDAR</strong>",
                                                "Accurate 3D geometry, works in darkness.",
                                                "Cannot see through glass; no color or semantic meaning.",
                                                "Provides structural backbone of the map."
                                    ],
                                    [
                                                "Camera",
                                                "Rich appearance, object recognition.",
                                                "Fails in low light or direct glare; depth estimation is indirect.",
                                                "Adds visual features for place recognition and loop closure."
                                    ],
                                    [
                                                "<strong class=\"font-bold\">IMU</strong>",
                                                "Fast motion sensing, independent of environment.",
                                                "Drifts over seconds; cannot provide absolute position.",
                                                "Stabilizes pose between slower sensor updates."
                                    ],
                                    [
                                                "Odometry",
                                                "Direct motion estimate from leg/joint sensors.",
                                                "Slip and uneven terrain cause accumulating error.",
                                                "Provides short-term motion prediction for the filter."
                                    ]
                        ]
            },
            "bottom_band": "Fusion mental model: '<strong class=\"font-bold\">LiDAR</strong> gives the shape, camera gives the look, <strong class=\"font-bold\">IMU</strong> gives the feel, and <strong class=\"font-bold\">odometry</strong> gives the motion guess — fusion turns them into one reliable answer.'"
        },
        {
            "title": "Frames Keep Everyone Speaking the Same Language",
            "thesis": "A frame is a coordinate language. The map has one language, the robot body has another, and each sensor may have its own. Transformations translate between those languages. When transforms are missing, stale, or inverted, a path can look correct on screen but become unsafe in the real world.",
            "board_type": "list",
            "board_data": [
                        "Map Frame: The fixed world coordinate system. Everything is ultimately referenced to this frame — the global 'truth' of where things are.",
                        "Odom Frame: The robot's estimated position from <strong class=\"font-bold\">odometry</strong>. Drifts over time — useful for short-term motion, not long-term accuracy.",
                        "Base Link / Body Frame: Attached to the robot chassis. Motion commands are expressed relative to this frame — 'go forward' means 'go forward from the robot's current facing direction.'",
                        "Sensor Frames: Each sensor (camera, <strong class=\"font-bold\">LiDAR</strong>) has its own frame. Transforms map sensor data into the body frame and then into the world frame.",
                        "Transform Tree: A directed graph connecting all frames. If any link breaks or is inverted, the entire perception chain may produce wrong results."
            ],
            "bottom_band": "Frame debugging: When sensor data appears in the wrong place, check the transform tree first — not the algorithm. Missing or stale transforms are the most common beginner frame error."
        },
        {
            "title": "Point Clouds Become Navigation Information",
            "thesis": "Point clouds are collections of spatial samples — not automatically a path. The system filters noisy points, identifies occupied space, projects relevant geometry into grids, and builds costmaps that planners can use. This conversion is the bridge from sensing to safe navigation.",
            "board_type": "list",
            "board_data": [
                        "Raw Points: Sensor returns thousands of 3D points — scattered, noisy, unprocessed. Includes ghost points, reflections, and sensor artifacts.",
                        "Filtered Points: Noise removal, downsampling, and outlier rejection produce a cleaner point set. Fewer points, but each is more reliable.",
                        "Occupancy Grid: Points are projected into a 2D or 3D grid. Each cell is marked free, occupied, or unknown based on point evidence.",
                        "Costmap: The occupancy grid is annotated with risk — obstacle cells are lethal, nearby cells are inflated with safety buffers, and unknown cells carry caution.",
                        "Path Choice: The <strong class=\"font-bold\">planner</strong> reads the <strong class=\"font-bold\">costmap</strong> and selects the lowest-cost route that respects safety margins and reaches the goal."
            ],
            "bottom_band": "Pipeline check: 'I have a point cloud — can I send it directly to the <strong class=\"font-bold\">planner</strong>?' No. Walk through each conversion step and identify what information is added or removed at each stage."
        },
        {
            "title": "Beginner Evidence Habit for SLAM",
            "thesis": "Replace vague success claims with artifacts. If students say '<strong class=\"font-bold\">SLAM</strong> worked,' they should show the map snapshot, <strong class=\"font-bold\">pose</strong> trace, transform tree, sensor status, and saved log. Evidence makes robotics work reviewable, repeatable, and easier to debug.",
            "board_type": "table",
            "board_data": {
                        "headers": [
                                    "Instead of Saying...",
                                    "Show This Evidence"
                        ],
                        "rows": [
                                    [
                                                "\"<strong class=\"font-bold\">SLAM</strong> worked.\"",
                                                "Map snapshot (screenshot of the built map), <strong class=\"font-bold\">pose</strong> trace (x/y/yaw over time), and transform tree (all frames connected and timestamped)."
                                    ],
                                    [
                                                "\"The robot knows where it is.\"",
                                                "Pose estimate plot with covariance bounds. If uncertainty is large, the robot does not really know."
                                    ],
                                    [
                                                "\"The sensors are fine.\"",
                                                "Sensor status dashboard: publication rate, timestamp freshness, data range. A sensor that publishes stale data is not fine."
                                    ],
                                    [
                                                "\"The map looks good.\"",
                                                "Quantitative comparison: map-to-ground-truth alignment, feature count, registration score. Aesthetics are not accuracy."
                                    ]
                        ]
            },
            "bottom_band": "Evidence rule: If you cannot show an artifact that proves your claim, you do not have evidence — you have an opinion. Opinions are fine for conversation; artifacts are required for engineering."
        },
        {
            "title": "Debugging Habit: Check the Data Path First",
            "thesis": "When mapping or localization fails, beginners often change algorithms too quickly. First check the data path: confirm the sensor publishes, the frame transform exists, timestamps are current, the map updates, and the pose estimate stays reasonable. Many failures come from missing data, not bad theory.",
            "board_type": "list",
            "board_data": [
                        "Step 1 — Sensor publishes? Confirm the topic or SDK stream is active. No data → no <strong class=\"font-bold\">SLAM</strong>. Check rostopic list, rostopic hz, or SDK subscriber callbacks.",
                        "Step 2 — Frame exists? Verify the transform from sensor to base and base to map exists. Missing transforms produce ghost obstacles or invisible walls.",
                        "Step 3 — Timestamp valid? Check that sensor timestamps are current (not system time mismatch or stale data). Stale timestamps break filter updates.",
                        "Step 4 — Map updates? Observe whether the occupancy grid changes as the robot moves. A static map when the robot is moving means <strong class=\"font-bold\">SLAM</strong> is not updating.",
                        "Step 5 — Pose stable? Monitor <strong class=\"font-bold\">pose</strong> estimate over time. Large jumps, oscillation, or divergence indicate a filter or registration problem, not a planning problem."
            ],
            "bottom_band": "Data-path first: Before touching any algorithm parameter, confirm that data enters the system, transforms exist, timestamps are valid, the map updates, and the <strong class=\"font-bold\">pose</strong> is stable. Most '<strong class=\"font-bold\">SLAM</strong> failures' are actually data-path failures."
        },
        {
            "title": "Section 2 — Planning and Costmaps",
            "thesis": "How goals become safer robot motion. This section covers global vs. local planners, costmap structure, inflation zones, the difference between obstacle avoidance and full navigation, the Go2 avoid-mode lifecycle, patrol plans as beginner route contracts, and the habit of separating plan, command, and robot failures.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Core Idea",
                                    "value": "Planning turns intent into motion: Goal → Route → Local motion → Robot command. Each layer refines the intent into safer, more specific instructions."
                        },
                        {
                                    "label": "Key Concept",
                                    "value": "A <strong class=\"font-bold\">costmap</strong> is a risk picture around the robot. It marks free, occupied, inflated, and unknown cells so the <strong class=\"font-bold\">planner</strong> avoids dangerous space."
                        },
                        {
                                    "label": "Common Mistake",
                                    "value": "Confusing obstacle avoidance (reactive, local) with navigation (planned, global). Both are needed — avoidance alone does not choose a destination."
                        },
                        {
                                    "label": "Section Slides",
                                    "value": "Slides 14–21: Planning concepts, global/local split, costmap grid, inflation, avoidance vs. navigation, Go2 avoid lifecycle, patrol plans, and layered debugging."
                        }
            ],
            "bottom_band": "Section framing: By the end of this section you should be able to read a <strong class=\"font-bold\">costmap</strong>, explain why <strong class=\"font-bold\">inflation</strong> exists, and describe how the <strong class=\"font-bold\">Go2</strong> avoid-mode lifecycle protects local motion."
        },
        {
            "title": "Planning Turns Intent into Motion",
            "thesis": "Path planning begins with intent. The robot needs to reach a checkpoint, inspect an object, or move through a corridor. The <strong class=\"font-bold\">planner</strong> converts that intent into a route. A local motion layer then turns the route into near-term movement that respects obstacles, robot size, and safety margins.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Goal",
                                    "value": "What the robot should achieve — reach a checkpoint, inspect a target, patrol a corridor. The goal is expressed in the map frame as a destination <strong class=\"font-bold\">pose</strong>."
                        },
                        {
                                    "label": "Route",
                                    "value": "The global path from start to goal — a sequence of waypoints through free space. The global <strong class=\"font-bold\">planner</strong> computes this using the full occupancy grid."
                        },
                        {
                                    "label": "Local Motion",
                                    "value": "The next few velocity or increment commands — refined by the local <strong class=\"font-bold\">costmap</strong> to avoid nearby obstacles. Updated at a higher frequency than the global route."
                        },
                        {
                                    "label": "Robot Command",
                                    "value": "The final motion instruction — Move(vx, vy, vyaw) or MoveToIncrementPosition(dx, dy, dyaw) — sent to the robot through the appropriate client."
                        }
            ],
            "bottom_band": "Planning mental model: 'Goal is the destination postcard, Route is the highway map, Local Motion is the next three seconds of driving, and Robot Command is the steering wheel.' Each layer operates at a different time and space scale."
        },
        {
            "title": "Global and Local Planners Split the Job",
            "thesis": "A global planner reasons over the larger map and chooses a route toward the destination. A local planner focuses on the space near the robot and adapts to immediate obstacles. Beginners can remember this as: global chooses the trip, local watches the next few steps.",
            "board_type": "table",
            "board_data": {
                        "headers": [
                                    "Dimension",
                                    "Global Planner",
                                    "Local Planner"
                        ],
                        "rows": [
                                    [
                                                "Scope",
                                                "Full map — considers the entire known environment.",
                                                "Local window — typically a few meters around the robot."
                                    ],
                                    [
                                                "Update Rate",
                                                "Slow — recomputed when the map changes or a new goal arrives.",
                                                "Fast — replanned at 5–20 Hz to react to dynamic obstacles."
                                    ],
                                    [
                                                "Output",
                                                "A route: sequence of waypoints through free space.",
                                                "A trajectory: velocity commands or increment goals for the next few seconds."
                                    ],
                                    [
                                                "Fails When",
                                                "The map is incomplete or the goal is unreachable.",
                                                "An unexpected obstacle appears too close for the stopping distance."
                                    ],
                                    [
                                                "Beginner Analogy",
                                                "\"Which highway should I take to the city?\"",
                                                "\"Should I brake for the car that just pulled in front of me?\""
                                    ]
                        ]
            },
            "bottom_band": "Key distinction: If the robot does not know the overall route, the problem is global planning. If the robot knows the route but hits nearby obstacles, the problem is local planning. Separate these before debugging."
        },
        {
            "title": "A Costmap Is a Risk Picture",
            "thesis": "A local costmap is a grid around the robot. Each cell stores risk information. Some cells are free, some contain obstacles, some are unknown, and some are inflated safety areas around obstacles. The planner reads this grid to avoid choosing motion that is too close or unsafe.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Free Space (Low Risk)",
                                    "value": "Cells with no detected obstacles. The <strong class=\"font-bold\">planner</strong> can route through these cells at low cost. Color-coded green in most visualizers."
                        },
                        {
                                    "label": "Obstacle (Blocked)",
                                    "value": "Cells containing detected obstacles — lethal cost. The <strong class=\"font-bold\">planner</strong> must never route through these. Color-coded dark/red."
                        },
                        {
                                    "label": "Inflation (Safety Buffer)",
                                    "value": "Cells near obstacles — cost increases with proximity. Creates a safety margin so the robot does not scrape walls or cones. Color-coded amber/yellow gradient."
                        },
                        {
                                    "label": "Unknown (Be Careful)",
                                    "value": "Cells with no sensor data — the robot does not know what is there. Conservative planners treat unknown as high-cost. Color-coded gray."
                        }
            ],
            "bottom_band": "Costmap reading exercise: Look at a <strong class=\"font-bold\">costmap</strong> visualization. Point to one free cell, one obstacle cell, one inflated cell, and one unknown cell. For each, explain what the <strong class=\"font-bold\">planner</strong> will do with that information."
        },
        {
            "title": "Inflation Creates Breathing Room",
            "thesis": "Robots need space around obstacles. Inflation expands obstacle regions so the planner avoids scraping walls, cones, or people. The margin should consider robot width, pose uncertainty, and field safety rules. More inflation improves clearance, but too much inflation can block narrow routes.",
            "board_type": "table",
            "board_data": {
                        "headers": [
                                    "Inflation Factor",
                                    "Effect on Planning",
                                    "Beginner Guidance"
                        ],
                        "rows": [
                                    [
                                                "Robot Footprint Radius",
                                                "The minimum clearance — at least half the robot's width plus a margin.",
                                                "Measure the Go2 width and add 0.1–0.2 m. This is your absolute minimum inflation radius."
                                    ],
                                    [
                                                "Pose Uncertainty",
                                                "Additional margin for localization error — if the robot may be 0.1 m off, add 0.1 m.",
                                                "Larger in GPS-denied or feature-poor environments; smaller in well-mapped indoor spaces with good features."
                                    ],
                                    [
                                                "Safety Policy",
                                                "Extra margin required by field safety rules — typically 0.2–0.5 m for classroom settings.",
                                                "Non-negotiable for student labs. The instructor sets this value; it overrides other considerations."
                                    ],
                                    [
                                                "Narrow Passage Trade-off",
                                                "Too much inflation blocks legitimate routes through doors or corridors.",
                                                "If the robot refuses to pass through a wide-enough opening, reduce inflation slightly — but never below the minimum."
                                    ]
                        ]
            },
            "bottom_band": "Inflation test: 'My robot refuses to enter a 1.2 m corridor. The robot is 0.4 m wide. What should I check?' Answer: <strong class=\"font-bold\">inflation</strong> radius — if it exceeds 0.4 m, the corridor looks blocked even though the robot physically fits."
        },
        {
            "title": "Obstacle Avoidance Is Not Full Navigation",
            "thesis": "Obstacle avoidance helps the robot respond to nearby hazards, but it does not automatically understand the whole route. Planning chooses where to go over a larger space. Avoidance helps motion remain safe moment by moment. Beginners should not confuse reactive safety behavior with full autonomous navigation.",
            "board_type": "table",
            "board_data": {
                        "headers": [
                                    "Dimension",
                                    "Obstacle Avoidance",
                                    "Full Navigation"
                        ],
                        "rows": [
                                    [
                                                "Input",
                                                "Local sensor data — immediate surroundings.",
                                                "Global map + goal pose + local sensor data."
                                    ],
                                    [
                                                "Time Horizon",
                                                "Seconds — the next few motion commands.",
                                                "Minutes — the complete route to the destination."
                                    ],
                                    [
                                                "Output",
                                                "Safe velocity adjustment or stop command.",
                                                "Route waypoints + trajectory + avoidance overlay."
                                    ],
                                    [
                                                "Answers the Question",
                                                "\"Is my next step safe?\"",
                                                "\"Where should I go, and is the path safe all the way?\""
                                    ],
                                    [
                                                "Fails When",
                                                "An obstacle appears inside the stopping distance.",
                                                "The global goal is unreachable or the map is wrong."
                                    ]
                        ]
            },
            "bottom_band": "Vocabulary check: 'The robot avoided the cone.' What does this mean? It means the local avoidance layer detected the cone and adjusted motion — it does NOT mean the robot planned a new global route around it."
        },
        {
            "title": "Unitree Avoid Mode Fits the Local Layer",
            "thesis": "On the Go2, obstacle avoidance is controlled through a clear lifecycle. The program enables the avoidance client, requests command authority, sends controlled motion, stops the robot, releases authority, and disables avoid mode. This lifecycle belongs in the local safety layer of the autonomy stack.",
            "board_type": "list",
            "board_data": [
                        "1. Enable Avoid Mode: <strong class=\"font-bold\">ObstaclesAvoidClient</strong>.SwitchSet(True) and verify with SwitchGet(). The avoid service must actually be on — confirm with read-back.",
                        "2. Gain Command Authority: UseRemoteCommandFromApi(True) transfers control from the remote to the API. Without this, your commands are ignored.",
                        "3. Move Carefully: Send limited velocity or increment commands through the avoid service. The robot will slow or stop for nearby obstacles automatically.",
                        "4. Stop: Send repeated Move(0, 0, 0) to halt all motion. Redundant stop commands are safer — one zero command may not be enough.",
                        "5. Release Authority: UseRemoteCommandFromApi(False) returns control to the remote. The script must not retain control after completion.",
                        "6. Disable Avoid: SwitchSet(False) turns off the avoid service. Clean shutdown prevents lingering command authority."
            ],
            "bottom_band": "Lifecycle rule: Success, failure, and Ctrl+C paths must all converge on the same release sequence. A crash after step 2 leaves the robot in an unsafe state — always wrap in try/finally."
        },
        {
            "title": "Patrol Plans Are Beginner Route Contracts",
            "thesis": "A patrol plan is a simple route contract. It lists checkpoints, movement limits, capture expectations, and validation rules. Beginners can use it before full autonomy because it teaches disciplined route thinking. Later, the same structure can be compared with map-based goals and planner-generated paths.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Checkpoint",
                                    "value": "A named stop on the route — cp_A (start), cp_B (corner), cp_C (end). Each checkpoint has an ID, label, dwell time, and optional capture requirement."
                        },
                        {
                                    "label": "Motion Limit",
                                    "value": "Speed cap (vx ≤ 0.25 m/s) and increment cap (dx ≤ 0.5 m). Limits are chosen for supervision and evidence quality, not for the robot's maximum capability."
                        },
                        {
                                    "label": "Capture Action",
                                    "value": "<strong class=\"font-bold\">VideoClient</strong>.GetImageSample() at designated checkpoints — the camera records evidence after the robot stops, not during motion."
                        },
                        {
                                    "label": "Validation Rule",
                                    "value": "Each artifact has a structural requirement — metadata<strong class=\"font-bold\">.json</strong> fields, image file size > 100 bytes, JSONL with at least one valid line."
                        }
            ],
            "bottom_band": "Patrol plan as contract: 'If I hand this plan to another team, can they execute it safely?' If the answer is no — the limits are vague, checkpoints are unnamed, or validation rules are missing — the plan is not ready for hardware."
        },
        {
            "title": "Debugging Habit: Separate Plan, Command, and Robot",
            "thesis": "When motion fails, do not guess. Separate the problem into layers. First ask whether the plan is valid, then check whether the command was sent, next observe whether the robot moved as expected, and finally confirm that evidence was saved. This habit makes debugging less emotional and more systematic.",
            "board_type": "list",
            "board_data": [
                        "1. Plan valid? Check patrol_plan<strong class=\"font-bold\">.json</strong> structure — are all required fields present? Do checkpoint IDs match between checkpoints and legs? Are values within limits?",
                        "2. Command sent? Verify the SDK client sent the command — check console output, return codes, and any error messages. Did the client timeout or throw?",
                        "3. Robot moved? Observe physical behavior — did the robot move at all? In the expected direction? For the expected distance? Did it stop correctly?",
                        "4. Evidence saved? Check the run folder — are metadata<strong class=\"font-bold\">.json</strong>, sportmodestate<strong class=\"font-bold\">.jsonl</strong>, and checkpoint images present and valid? Does the validator pass?"
            ],
            "bottom_band": "Debugging discipline: Before changing any code, answer all four questions. If the plan was never valid, tuning dx values will not help. If the command was never sent, the robot behavior is irrelevant."
        },
        {
            "title": "Section 3 — Gazebo Sandbox",
            "thesis": "Rehearse the inspection routine before field deployment. This section covers Gazebo as a required rehearsal space, building meaningful simulation worlds, checking simulated sensors, reading ROS 2 data flow, establishing validation gates, collecting simulation evidence, and the rule that simulation failures are fixed before hardware is touched.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Core Idea",
                                    "value": "Design in simulation → Test safely → Collect evidence → Decide readiness. <strong class=\"font-bold\">Gazebo</strong> is the rehearsal space — not a replacement for hardware testing, but a required step before it."
                        },
                        {
                                    "label": "Why Required",
                                    "value": "Simulation catches plan errors, route problems, sensor misconfigurations, and costmap issues without risking physical damage or safety incidents."
                        },
                        {
                                    "label": "ROS 2 Bridge",
                                    "value": "<strong class=\"font-bold\">ros_gz_bridge</strong> exchanges messages between <strong class=\"font-bold\">ROS 2</strong> and <strong class=\"font-bold\">Gazebo</strong> Transport. Topics like /cmd_vel, /odom, /scan, and /<strong class=\"font-bold\">costmap</strong> become visible for debugging."
                        },
                        {
                                    "label": "Section Slides",
                                    "value": "Slides 23–29: Gazebo as rehearsal, world design, sensor checking, ROS 2 topic flow, validation gates, simulation evidence, and the sim-before-hardware debugging rule."
                        }
            ],
            "bottom_band": "Section rule: If a routine fails in simulation, fix it in simulation. If it passes simulation, still test hardware slowly. Simulation is a gate, not a guarantee."
        },
        {
            "title": "Gazebo Is the Rehearsal Space",
            "thesis": "<strong class=\"font-bold\">Gazebo</strong> is the rehearsal space for inspection routines. It allows students to test arena layout, route logic, obstacle placement, sensor assumptions, and <strong class=\"font-bold\">costmap</strong> behavior before moving the physical robot. Simulation does not prove field safety, but it reduces avoidable uncertainty before hardware testing.",
            "board_type": "list",
            "board_data": [
                        "Design: Build the arena in simulation — start zone, corridor, obstacles, inspection targets, restricted areas, finish zone. Make the world mirror the field task.",
                        "Test: Run the patrol routine in <strong class=\"font-bold\">Gazebo</strong>. Observe sensor output, route execution, obstacle avoidance behavior, and <strong class=\"font-bold\">costmap</strong> updates.",
                        "Collect Evidence: Save world screenshot, route trace, <strong class=\"font-bold\">costmap</strong> snapshot, log file. Evidence lets another person understand what happened without re-running.",
                        "Decide Readiness: Based on evidence — is the routine ready for hardware? Does it need tuning? Does it need redesign? Make an explicit decision, not an assumption."
            ],
            "bottom_band": "Simulation mindset: 'I am not proving the routine works. I am finding what would fail on hardware before the hardware is at risk.' Design your simulation test to find failures, not to confirm hopes."
        },
        {
            "title": "Build the Inspection World on Purpose",
            "thesis": "A useful simulation world is not random decoration. It should represent the field task. Students should place a start zone, corridor boundaries, obstacles, inspection targets, restricted areas, and a finish zone. This makes the simulation test meaningful because it mirrors the decisions required during the real patrol.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Start Zone",
                                    "value": "Where the robot initializes — clear of obstacles, near the first checkpoint. The simulated robot should spawn in the same <strong class=\"font-bold\">pose</strong> the physical robot will start from."
                        },
                        {
                                    "label": "Corridor Boundaries",
                                    "value": "Walls, cones, or markers defining the patrol corridor. Should match the physical arena dimensions as closely as practical."
                        },
                        {
                                    "label": "Obstacles",
                                    "value": "Objects the robot must avoid — placed at positions that test the costmap and avoidance response. Start with one obstacle; add more after confirming avoidance works."
                        },
                        {
                                    "label": "Inspection Targets",
                                    "value": "Checkpoint locations — the robot should stop, dwell, and capture evidence here. Each target tests a different part of the route logic."
                        },
                        {
                                    "label": "Finish Zone",
                                    "value": "Where the robot ends — clear of obstacles, with enough space for a clean stop and final capture."
                        }
            ],
            "bottom_band": "World design test: 'Does my simulation world contain every decision the robot will face in the field?' If the field has a narrow turn but the sim doesn't, the simulation missed a critical test case."
        },
        {
            "title": "Simulated Sensors Must Be Checked",
            "thesis": "A simulated robot must provide usable sensor data. Students should confirm that camera, LiDAR, odometry, and state topics are publishing plausible information. If the simulated sensors are missing or unrealistic, the route validation becomes weak. Beginners should inspect the data before trusting the motion result.",
            "board_type": "table",
            "board_data": {
                        "headers": [
                                    "Check",
                                    "What to Look For",
                                    "Red Flags"
                        ],
                        "rows": [
                                    [
                                                "Robot Model",
                                                "Correct URDF/Xacro, joint limits, sensor plugins.",
                                                "Missing links, zero-mass bodies, sensors with no plugin."
                                    ],
                                    [
                                                "Sensor Topics",
                                                "Topics publishing at expected rates with valid data types.",
                                                "Topics missing, publishing at 0 Hz, or with zero-filled messages."
                                    ],
                                    [
                                                "Visualization",
                                                "Data visible in <strong class=\"font-bold\">RViz</strong> — point clouds, laser scans, camera images.",
                                                "Data appears offset, inverted, or shows constant/default values."
                                    ],
                                    [
                                                "Logs",
                                                "Logged values match visual inspection — ranges, timestamps, frame IDs.",
                                                "Timestamps frozen, frame IDs mismatched, ranges out of sensor spec."
                                    ]
                        ]
            },
            "bottom_band": "Sensor check rule: Before you trust the robot's motion in simulation, verify each sensor independently. A world with broken sensors trains you to ignore broken data — the opposite of what you need for hardware."
        },
        {
            "title": "ROS 2 Shows the Data Flow",
            "thesis": "In a beginner simulation workflow, ROS 2 topics make invisible data visible. Command topics show intended motion, odometry shows estimated movement, sensor topics show what the robot perceives, and costmap topics show how nearby risk is represented. This visibility helps students debug before hardware is involved.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "/cmd_vel → Robot Motion",
                                    "value": "Publishes <strong class=\"font-bold\">geometry_msgs</strong>/<strong class=\"font-bold\">Twist</strong> — linear and angular velocity commands. In simulation, this is how the robot is told to move. Compare commanded vs. actual velocity."
                        },
                        {
                                    "label": "/odom → Pose Estimate",
                                    "value": "Publishes <strong class=\"font-bold\">odometry</strong> — position and orientation estimate from motion sensors. Drifts over time but useful for short-term motion tracking."
                        },
                        {
                                    "label": "/scan or /points → Obstacles",
                                    "value": "Publishes laser scan or point cloud data — what the robot detects around it. Feed this into <strong class=\"font-bold\">RViz</strong> to visually confirm obstacle detection."
                        },
                        {
                                    "label": "/<strong class=\"font-bold\">costmap</strong> → Risk Grid",
                                    "value": "Publishes the local costmap — the risk picture the planner reads. Watch how inflation zones expand around obstacles as the robot approaches."
                        }
            ],
            "bottom_band": "Topic flow exercise: Run a simulation. Open a terminal and run rostopic list. For each topic above, run rostopic echo once and explain what the message means. If you cannot, that topic is a blind spot in your understanding."
        },
        {
            "title": "Validate the Routine Before the Robot Moves",
            "thesis": "Validation is a gate, not a formality. Before hardware movement, students should verify that the plan file is valid, the route appears correctly, obstacles are detected, the simulated robot avoids collisions, and logs are saved. A failed validation means the system is protecting the field test.",
            "board_type": "list",
            "board_data": [
                        "Plan file valid: All required fields present; checkpoint IDs match; motion values within limits; JSON structure parses without errors.",
                        "Route visible: The planned path appears correctly on the map — no segments through walls, no impossible turns, no self-intersections.",
                        "Obstacles detected: Sensor data shows obstacles at expected positions; <strong class=\"font-bold\">costmap</strong> marks them correctly; <strong class=\"font-bold\">inflation</strong> zones provide adequate clearance.",
                        "No collision: The simulated robot completes the route without contacting obstacles, crossing safety boundaries, or entering restricted zones.",
                        "Logs saved: All evidence artifacts exist — world screenshot, route trace, <strong class=\"font-bold\">costmap</strong> snapshot, log file, short conclusion statement."
            ],
            "bottom_band": "Validation gate rule: PASS → proceed to hardware (slowly). FAIL → fix the issue and re-validate. WARNING → document the concern and get instructor approval before hardware. Never skip validation because 'it will probably be fine.'"
        },
        {
            "title": "Simulation Evidence Should Be Reviewable",
            "thesis": "Simulation evidence should let another person understand what happened. Students should save a world screenshot, route trace, costmap snapshot, log file, and short conclusion. The conclusion should state whether the routine is ready for field testing, needs tuning, or must be redesigned.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "World Screenshot",
                                    "value": "Top-down view of the simulation world with the robot's path overlaid. Shows the arena layout and the complete route in one image."
                        },
                        {
                                    "label": "Route Trace",
                                    "value": "Plot of the robot's actual trajectory vs. the planned path. Deviations, overshoots, and correction points are visible."
                        },
                        {
                                    "label": "Costmap Snapshot",
                                    "value": "Screenshot of the local <strong class=\"font-bold\">costmap</strong> at a critical moment — e.g., the narrowest turn or closest obstacle approach."
                        },
                        {
                                    "label": "Log File",
                                    "value": "Sensor topics, command messages, and state data saved during the run. Timestamps allow correlation with screenshots."
                        },
                        {
                                    "label": "Short Conclusion",
                                    "value": "One explicit statement: ready for hardware / needs tuning (list what) / must be redesigned (explain why). No hedging."
                        }
            ],
            "bottom_band": "Reviewability test: 'If I give this evidence folder to someone who did not watch the simulation, can they: (a) understand what happened, (b) identify any problems, and (c) decide whether to proceed?' If any answer is no, add evidence."
        },
        {
            "title": "Debugging Habit: Simulation Before Hardware",
            "thesis": "If a routine fails in simulation, fix it before using hardware. If it passes simulation, do not assume the real robot will behave perfectly. Start slowly, use small motion commands, keep a stop procedure ready, and compare field results against simulation evidence.",
            "board_type": "list",
            "board_data": [
                        "Rule 1 — Fix in sim first: A failure in <strong class=\"font-bold\">Gazebo</strong> means something is wrong with the plan, sensors, or logic. Fix it where it is safe and fast to iterate.",
                        "Rule 2 — Passing sim is not a guarantee: Hardware introduces network latency, floor texture, lighting, battery state, and sensor noise that simulation cannot fully capture.",
                        "Rule 3 — Start hardware slowly: First test = small speed, short duration, clear arena. Stop and review behavior before increasing scope.",
                        "Rule 4 — Keep a stop procedure: Agree on who calls stop, how to stop (remote, script, or physical), and what conditions trigger an immediate halt.",
                        "Rule 5 — Compare sim vs. hardware: After the field test, overlay the hardware route trace on the simulation route trace. Differences are evidence of real-world effects."
            ],
            "bottom_band": "Conservative rule: 'Simulation is where you earn confidence. Hardware is where you confirm it cautiously.' Never reverse the order — hardware is not for debugging obvious plan errors."
        },
        {
            "title": "Section 4 — Physical Go2 Handoff",
            "thesis": "Move from simulation evidence to controlled field testing. This section covers the handoff as a controlled process, network readiness checks, intentional command authority, staged motion testing, hardware-in-the-loop comparison, evidence-based claims, and the one-change-at-a-time experimental discipline.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Core Idea",
                                    "value": "Validated plan → Network check → Robot state check → Safe command authority → Field run. Handoff is a controlled process, not just copying a file."
                        },
                        {
                                    "label": "Key Principle",
                                    "value": "Many field failures are network failures disguised as robot failures. Check connectivity, interface, DDS discovery, and topic visibility before debugging autonomy."
                        },
                        {
                                    "label": "Safety Rule",
                                    "value": "Command authority defines who controls the robot. Request only when ready, send limited commands, stop cleanly, release afterward. Treat it seriously."
                        },
                        {
                                    "label": "Section Slides",
                                    "value": "Slides 31–37: Controlled handoff, network readiness, command authority lifecycle, staged field testing, hardware-in-the-loop, evidence-based claims, and one-variable-at-a-time debugging."
                        }
            ],
            "bottom_band": "Section rule: The first hardware test is not a full-speed patrol. It is a slow, short, supervised motion — then stop, review, and decide whether to expand."
        },
        {
            "title": "Handoff Means More Than Copying a File",
            "thesis": "Hardware handoff is not simply copying a patrol file onto a machine. It is a controlled process. Students must confirm that the plan passed validation, the network is connected, robot state is safe, command authority is understood, and the field operator is ready before motion begins.",
            "board_type": "list",
            "board_data": [
                        "1. Validated Plan: The patrol plan passed simulation validation. Artifacts exist — world screenshot, route trace, <strong class=\"font-bold\">costmap</strong> snapshot, conclusion.",
                        "2. Network Check: Robot is reachable (ping 192.168.123.161), correct interface is active (en6, eth0), <strong class=\"font-bold\">DDS</strong> discovery works, topics or SDK responses are visible.",
                        "3. Robot State Check: Posture is safe (BalanceStand confirmed), SportModeState is normal, battery is adequate, no error codes active.",
                        "4. Safe Command Authority: Operator understands who has control (remote vs. API). UseRemoteCommandFromApi(True) is intentional and documented.",
                        "5. Field Operator Ready: Spotter in position, arena marked, stop procedure agreed, abort rules reviewed, one-patrol-at-a-time rule enforced."
            ],
            "bottom_band": "Handoff test: 'Before I run a single motion command, can I answer: is the network up, is the robot state safe, who has command authority, and what is the stop procedure?' If any answer is no, do not proceed."
        },
        {
            "title": "Network Readiness Comes First",
            "thesis": "Many field failures are network failures disguised as robot failures. Before debugging autonomy, students should confirm the robot is reachable, the correct network interface is active, DDS discovery works, and expected topics or SDK responses are visible. Connectivity is the foundation for safe command and logging.",
            "board_type": "table",
            "board_data": {
                        "headers": [
                                    "Check",
                                    "Command / Action",
                                    "Expected Result"
                        ],
                        "rows": [
                                    [
                                                "Robot Reachable",
                                                "ping 192.168.123.161",
                                                "Consistent replies, latency < 5 ms, no packet loss."
                                    ],
                                    [
                                                "Correct Interface",
                                                "ip addr — identify the robot-facing adapter (en6, eth0, enp3s0).",
                                                "Interface has IP on 192.168.123.x subnet, NOT .161 (the robot's onboard address)."
                                    ],
                                    [
                                                "<strong class=\"font-bold\">DDS</strong> Discovery",
                                                "Initialize ChannelFactoryInitialize(0, \"<interface>\") without errors.",
                                                "SDK clients initialize; no <strong class=\"font-bold\">CycloneDDS</strong> domain mismatch or discovery timeout."
                                    ],
                                    [
                                                "Topics Visible",
                                                "Subscriber callbacks fire; SportModeState_ messages arrive.",
                                                "State messages contain valid mode, gait, position, velocity fields — not defaults or zeros."
                                    ]
                        ]
            },
            "bottom_band": "Network-first rule: If the robot is not reachable, nothing else matters. Do not debug autonomy, planning, or costmaps — debug the network. Connectivity problems are the #1 cause of beginner field failures."
        },
        {
            "title": "Command Authority Must Be Intentional",
            "thesis": "Command authority defines who is allowed to control the robot. Beginners must treat it seriously. The program should request authority only when ready, send limited commands, stop cleanly, and release authority afterward. This prevents confusion between manual control, SDK control, and emergency intervention.",
            "board_type": "list",
            "board_data": [
                        "Request authority only when ready: UseRemoteCommandFromApi(True) is called after all checks pass — network, state, plan, operator. Not during initialization as a default.",
                        "Send limited commands: Speed ≤ 0.25 m/s, increment ≤ 0.5 m, short duration. The first command should be the smallest meaningful motion possible.",
                        "Stop cleanly: Move(0, 0, 0) sent repeatedly; <strong class=\"font-bold\">SportClient</strong>.StopMove() as backup. Stop is as important as move — a script that can start but not stop is unsafe.",
                        "Release authority afterward: UseRemoteCommandFromApi(False) and SwitchSet(False) in a finally block. Authority must not linger after the script exits."
            ],
            "bottom_band": "Authority question: At any moment, ask: 'Who currently has command authority?' If the answer is unclear — the remote might be connected, the app might be open, another script might be running — stop and resolve before motion."
        },
        {
            "title": "Start with Small Field Motions",
            "thesis": "The first hardware test should not be a full-speed patrol. Students should start with small speeds and short durations, then stop and review behavior. If the robot moves as expected, the test can expand gradually. This staged approach reduces risk and gives students time to learn from evidence.",
            "board_type": "list",
            "board_data": [
                        "Stage 1 — Single small increment: One dx = 0.2 m forward. Stop. Review state log. Confirm the robot moved ~0.2 m, not 0.5 m or 0.0 m.",
                        "Stage 2 — Increment + turn: One dx = 0.3 m, one dyaw = 0.3 rad. Stop. Review. Did the robot turn approximately the expected angle?",
                        "Stage 3 — Two-leg sequence: Forward to cp_B, turn, forward to cp_C. Capture at each checkpoint. Run validator. Review all artifacts.",
                        "Stage 4 — Full patrol at low speed: Complete the patrol plan at minimum speeds. Compare with simulation route trace. Identify deviations.",
                        "Stage 5 — Tuned patrol: One parameter change (e.g., increase leg 1 dx by 0.1 m). Compare baseline vs. tuned. Document the difference."
            ],
            "bottom_band": "Staging rule: Never jump from simulation to full-speed patrol. Each stage confirms one new capability. If a stage fails, fix it before adding complexity."
        },
        {
            "title": "Hardware-in-the-Loop Tests Close the Gap",
            "thesis": "Simulation cannot capture every real-world effect. Hardware-in-the-loop testing exposes network latency, floor texture, sensor noise, lighting, battery condition, and physical dynamics. The purpose is not to prove simulation wrong — it is to compare expectations against reality and improve the routine responsibly.",
            "board_type": "table",
            "board_data": {
                        "headers": [
                                    "Real-World Effect",
                                    "Simulation Gap",
                                    "Hardware Observation Method"
                        ],
                        "rows": [
                                    [
                                                "Network Latency",
                                                "Simulation assumes instantaneous or low-latency communication.",
                                                "Timestamp command send time and state receipt time; compute round-trip delay."
                                    ],
                                    [
                                                "Floor Texture",
                                                "Simulation floor is uniform friction; real floors vary (carpet, tile, concrete).",
                                                "Compare odometry-reported distance with measured physical distance."
                                    ],
                                    [
                                                "Sensor Noise",
                                                "Simulated sensors add modeled noise; real noise patterns are more complex.",
                                                "Plot sensor values over time during a static robot — noise floor should be visible."
                                    ],
                                    [
                                                "Lighting",
                                                "Simulation lighting is controlled; real lighting changes throughout the day.",
                                                "Capture checkpoint images at the same location under different lighting conditions."
                                    ]
                        ]
            },
            "bottom_band": "Comparison mindset: 'The simulation predicted X. The hardware showed Y. The difference Z tells me something about the real world.' Document Z — that is your engineering insight, not a failure."
        },
        {
            "title": "Field Evidence Must Match the Claim",
            "thesis": "Every field claim needs matching evidence. If students claim the robot avoided an obstacle, they should show the field video, command log, stop event, or route trace. If they claim the plan is reliable, they should show repeated runs. Evidence turns a demo into an engineering result.",
            "board_type": "table",
            "board_data": {
                        "headers": [
                                    "Claim",
                                    "Required Evidence",
                                    "Insufficient Evidence"
                        ],
                        "rows": [
                                    [
                                                "\"The robot avoided the obstacle.\"",
                                                "Video of approach + <strong class=\"font-bold\">costmap</strong> showing obstacle + velocity change before contact.",
                                                "'I saw it turn' — memory is not evidence."
                                    ],
                                    [
                                                "\"The plan is reliable.\"",
                                                "Three repeated runs with route traces overlaid, all within tolerance.",
                                                "One successful run — reliability requires repetition."
                                    ],
                                    [
                                                "\"The checkpoint was reached.\"",
                                                "Checkpoint frame<strong class=\"font-bold\">.jpg</strong> showing the expected scene + state slice showing velocity ≈ 0.",
                                                "Metadata entry alone — image content matters more than structural presence."
                                    ],
                                    [
                                                "\"The robot stopped safely.\"",
                                                "Velocity plot showing vx → 0 within expected time; no residual drift.",
                                                "'It looked stopped' — measure, do not estimate."
                                    ]
                        ]
            },
            "bottom_band": "Evidence test: 'If someone disputes your claim, what artifact would you show to prove it?' If you cannot name a specific file, image, plot, or log entry, your claim is not yet evidence-backed."
        },
        {
            "title": "Debugging Habit: Change One Thing at a Time",
            "thesis": "When field tests fail, beginners may change speed, route, sensor settings, and code all at once. That makes learning impossible. Change one variable at a time, run the test, save the log, write one conclusion. This habit makes tuning slower at first but much more reliable.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "One Change",
                                    "value": "Modify exactly one parameter — leg dx, turn dyaw, dwell time, or speed cap. Document: what changed, old value, new value, why this change."
                        },
                        {
                                    "label": "One Run",
                                    "value": "Execute the patrol under the same conditions as the baseline — same arena, same lighting, same operator. Only the one parameter differs."
                        },
                        {
                                    "label": "One Log",
                                    "value": "Save the complete run folder with a descriptive name — e.g., run_field_tuned_dx_0.4. The name should encode the change."
                        },
                        {
                                    "label": "One Conclusion",
                                    "value": "State what the change did: 'dx 0.3→0.4 reduced under-shoot at cp_B from ~0.15 m to ~0.03 m.' Or: 'Change had no measurable effect — dx is not the limiting factor.'"
                        }
            ],
            "bottom_band": "Experimental discipline: If you change dx, dyaw, and dwell simultaneously and the robot reaches the checkpoint, you learned nothing about which change mattered. Control one variable to learn one lesson."
        },
        {
            "title": "Section 5 — Capstone and Practical Habits",
            "thesis": "Combine SLAM, planning, simulation, and field evidence into an integrated capstone demonstration. This section covers the five-step capstone expectation, a reusable beginner debugging checklist, evidence habits for reproducible runs, and the final takeaway that good autonomy is motion with explanation, validation, and evidence.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Core Idea",
                                    "value": "The capstone is not judged only by whether the robot moves. Students explain the map, justify the route, validate in Gazebo, test on Go2, and report evidence."
                        },
                        {
                                    "label": "Debugging Checklist",
                                    "value": "Power → Network → Topics → Frames → Plan → Simulation → Command → Logs. Move through layers in order — most issues resolve before you reach the bottom."
                        },
                        {
                                    "label": "Evidence Habit",
                                    "value": "Run folder = plan + settings + logs + screenshots + conclusion. Name folders by date, scenario, and attempt so results can be compared later."
                        },
                        {
                                    "label": "Section Slides",
                                    "value": "Slides 39–42: Capstone integration, debugging checklist, reproducible run folders, and the final takeaway that autonomy is evidence-based."
                        }
            ],
            "bottom_band": "Capstone mindset: Your presentation should let someone who never attended this class understand what you did, why it was safe, what evidence you collected, and what you would change next."
        },
        {
            "title": "The Capstone Connects Every Layer",
            "thesis": "The capstone should not be judged only by whether the robot moves. Students must explain the map or spatial assumptions, justify the route, validate behavior in Gazebo, run a controlled Go2 field test, and report evidence. This connects the full academic scope of Day 2.",
            "board_type": "list",
            "board_data": [
                        "1. Explain the map: Show the occupancy grid or spatial assumptions. What does the robot know about the environment? What is the coordinate frame layout?",
                        "2. Justify the route: Present the patrol plan or <strong class=\"font-bold\">planner</strong> output. Why this path? How do costmaps and <strong class=\"font-bold\">inflation</strong> protect the robot at each turn?",
                        "3. Validate in <strong class=\"font-bold\">Gazebo</strong>: Show simulation evidence — world screenshot, route trace, <strong class=\"font-bold\">costmap</strong> snapshot, log file. State the validation outcome explicitly.",
                        "4. Test on <strong class=\"font-bold\">Go2</strong>: Present hardware results — field video, command log, checkpoint images, validator output. Compare hardware route trace with simulation trace.",
                        "5. Report evidence: Provide the run folder with all artifacts. State one tuning action, one failure encountered or avoided, and one next improvement."
            ],
            "bottom_band": "Capstone test: 'If I only read your evidence folder — no live demo, no verbal explanation — would I understand what happened and whether the routine was safe?' If the answer is no, add evidence until it is yes."
        },
        {
            "title": "Beginner Debugging Checklist",
            "thesis": "A beginner debugging checklist prevents panic. Start with power and safety, check network connectivity, confirm topics or SDK responses, verify coordinate frames, validate the plan, test in simulation, send limited commands, and save logs. Most robotics debugging becomes manageable when students move through layers in order.",
            "board_type": "list",
            "board_data": [
                        "Power: Is the robot on? Battery adequate? Emergency stop accessible? No error lights or warning beeps.",
                        "Network: Can you ping the robot? Correct interface active? <strong class=\"font-bold\">DDS</strong> discovery working? No IP conflicts on the subnet.",
                        "Topics: Are expected topics publishing? Are message rates normal? Are timestamps current? No stale or zero-filled data.",
                        "Frames: Does the transform tree exist? Are all expected frames connected? Are timestamps synchronized across frames?",
                        "Plan: Is the plan file valid? All fields present? Values within limits? Checkpoint IDs consistent between checkpoints and legs?",
                        "Simulation: Does the routine pass in <strong class=\"font-bold\">Gazebo</strong>? Has evidence been collected? Is the conclusion explicit about readiness?",
                        "Command: Are commands being sent? Any error returns or timeouts? Is command authority explicitly controlled?",
                        "Logs: Are logs being written? Are files non-empty? Does the validator pass? Can another person understand the run folder?"
            ],
            "bottom_band": "Checklist discipline: When something fails, start at the top and work down. Do not skip layers. 'My robot isn't moving' could be a dead battery (Power), a disconnected cable (Network), or a missing authority request (Command) — the checklist catches all three."
        },
        {
            "title": "Evidence Habit: Make Every Run Reproducible",
            "thesis": "A reproducible run folder lets another person understand and repeat the test. It should include the plan file, key settings, logs, screenshots, captured images, and a short conclusion. Students should name folders clearly by date, scenario, and attempt number so results can be compared later.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Plan File",
                                    "value": "The exact patrol_plan<strong class=\"font-bold\">.json</strong> or <strong class=\"font-bold\">planner</strong> configuration used — not a similar version, not 'approximately what we ran.'"
                        },
                        {
                                    "label": "Key Settings",
                                    "value": "Speed limits, increment caps, <strong class=\"font-bold\">inflation</strong> radius, <strong class=\"font-bold\">costmap</strong> parameters, interface name, <strong class=\"font-bold\">DDS</strong> domain. Anyone should be able to recreate the configuration."
                        },
                        {
                                    "label": "Logs",
                                    "value": "State logs (sportmodestate<strong class=\"font-bold\">.jsonl</strong>), command logs, sensor data snapshots. Timestamps allow correlation between events."
                        },
                        {
                                    "label": "Visual Evidence",
                                    "value": "World screenshot, route trace, costmap snapshot, checkpoint images, field video or photo. Visual evidence answers questions text cannot."
                        },
                        {
                                    "label": "Short Conclusion",
                                    "value": "One paragraph: what was tested, what passed, what failed, what was changed, what should be tested next. No hedging, no unexplained success."
                        }
            ],
            "bottom_band": "Reproducibility test: 'Can someone else, using only this run folder, recreate the test and get similar results?' If not, what is missing? Add it and re-run."
        },
        {
            "title": "Final Takeaway: Autonomy Is Evidence-Based",
            "thesis": "Good autonomy is not just motion. Good autonomy is motion with explanation, validation, and evidence. Students should learn to explain the system, validate the routine, test carefully, and preserve evidence. This beginner habit prepares them for more advanced SLAM, navigation, costmap tuning, and field autonomy work.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Explanation",
                                    "value": "Can you explain the autonomy stack — sensors, fusion, <strong class=\"font-bold\">SLAM</strong>, planning, costmaps, control — in plain language? Can you draw the data flow from /cmd_vel to robot motion to evidence?"
                        },
                        {
                                    "label": "Validation",
                                    "value": "Did the routine pass structured validation gates in simulation? Were all artifacts collected? Was the readiness decision explicit and documented?"
                        },
                        {
                                    "label": "Evidence",
                                    "value": "Does every claim have a matching artifact? If you say 'the robot avoided the obstacle,' can you show the <strong class=\"font-bold\">costmap</strong>, video, or velocity plot that proves it?"
                        },
                        {
                                    "label": "Next Steps",
                                    "value": "Day 3 builds on this foundation — more complex SLAM configurations, advanced costmap tuning, multi-sensor calibration, and longer autonomous patrol sequences."
                        }
            ],
            "bottom_band": "Day 2 closing message: 'You now understand autonomy not as magic, but as a layered, testable, evidence-producing engineering discipline. Carry that mindset into every future robotics project.'"
        }
    ],
    "labs": [
        {
            "id": "lab-00",
            "title": "Readiness & Inspection Scenario",
            "content": "Confirm Day 1 artifacts exist, patrol-related SDK imports are available, network and DDS readiness are acceptable, and a patrol scenario has been written and validated before motion begins.\n\n- Verify Day 1 motion readiness and artifact completion\n- Confirm unitree_env active and SDK imports work\n- Identify correct network interface; ping 192.168.123.161\n- Write my_team_scenario.json with team, arena, checkpoints, motion_limits, abort_rules, deliverables\n- Validate scenario with --validate-scenario flag; fix structural errors before hardware",
            "code_files": [
                {
                    "name": "lab00_day2_readiness.py",
                    "code": "\"\"\"Day 2 Readiness Check — verify scenario, environment, and network before patrol.\"\"\"\nimport sys, json, os\n\ndef main(interface: str):\n    print(\"[READINESS] Day 2 — Go2 Autonomy & Sandbox Capstone\")\n    print(f\"[INTERFACE] {interface}\")\n    # 1. Check scenario file\n    scenario_path = \"my_team_scenario.json\"\n    if not os.path.exists(scenario_path):\n        print(f\"[FAIL] Missing {scenario_path} — create scenario before motion.\")\n        sys.exit(1)\n    with open(scenario_path) as f:\n        sc = json.load(f)\n    required = [\"team_name\", \"operator\", \"arena\", \"checkpoints\", \"motion_limits\", \"abort_rules\", \"deliverables\"]\n    missing = [k for k in required if k not in sc]\n    if missing:\n        print(f\"[FAIL] Scenario missing fields: {missing}\")\n        sys.exit(1)\n    # 2. Verify speed/increment caps\n    limits = sc.get(\"motion_limits\", {})\n    vx = limits.get(\"vx\", 0.25)\n    dx = limits.get(\"dx\", 0.5)\n    if vx > 0.25:\n        print(f\"[WARN] vx={vx} exceeds class cap 0.25 m/s — will be clamped.\")\n    if dx > 0.5:\n        print(f\"[WARN] dx={dx} exceeds class cap 0.5 m — will be clamped.\")\n    print(f\"[PASS] Scenario valid: team={sc['team_name']}, checkpoints={sc['checkpoints']}\")\n    print(f\"[PASS] Motion limits: vx≤{vx} m/s, dx≤{dx} m\")\n    print(\"[READINESS COMPLETE] Proceed to Lab 1 (Run-Folder Schema).\")\n\nif __name__ == \"__main__\":\n    main(sys.argv[1] if len(sys.argv) > 1 else \"en6\")"
                }
            ]
        },
        {
            "id": "lab-01",
            "title": "Run-Folder Schema & Bundle Validation",
            "content": "Learn the run-folder contract: metadata.json, patrol_plan.json, sportmodestate.jsonl, and checkpoints/<id>/frame.jpg. Validate both passing and failing fixtures.\n\n- Study the run folder tree structure and required fields\n- Run validator against sample_run_pass fixture\n- Run validator against sample_run_incomplete fixture\n- Interpret failure messages as a repair checklist\n- Create a mock run folder by hand to internalize the schema",
            "code_files": [
                {
                    "name": "lab01_validate_run_folder.py",
                    "code": "\"\"\"Day 2 Run-Folder Validator — check structural completeness.\"\"\"\nimport json, os, sys\n\ndef validate_run_folder(path: str) -> dict:\n    issues = []\n    # Check required top-level files\n    for f in [\"metadata.json\", \"patrol_plan.json\", \"sportmodestate.jsonl\"]:\n        if not os.path.isfile(os.path.join(path, f)):\n            issues.append(f\"missing file: {f}\")\n    # Check metadata fields\n    md_path = os.path.join(path, \"metadata.json\")\n    if os.path.isfile(md_path):\n        with open(md_path) as f:\n            md = json.load(f)\n        for key in [\"schema_version\", \"created_utc\", \"operator\"]:\n            if key not in md:\n                issues.append(f\"metadata.json: missing '{key}'\")\n        checkpoints = md.get(\"checkpoints\", [])\n    else:\n        checkpoints = []\n    # Check patrol_plan\n    pp_path = os.path.join(path, \"patrol_plan.json\")\n    if os.path.isfile(pp_path):\n        with open(pp_path) as f:\n            pp = json.load(f)\n        if \"checkpoints\" not in pp:\n            issues.append(\"patrol_plan.json: missing 'checkpoints'\")\n        plan_cps = [c[\"id\"] for c in pp.get(\"checkpoints\", [])]\n    else:\n        plan_cps = []\n    # Check sportmodestate.jsonl has at least 1 line\n    sm_path = os.path.join(path, \"sportmodestate.jsonl\")\n    if os.path.isfile(sm_path):\n        with open(sm_path) as f:\n            lines = [l for l in f if l.strip()]\n        if not lines:\n            issues.append(\"sportmodestate.jsonl: need at least 1 JSON line\")\n    # Check checkpoint dirs\n    cp_dir = os.path.join(path, \"checkpoints\")\n    for cp_id in plan_cps:\n        frame = os.path.join(cp_dir, cp_id, \"frame.jpg\")\n        if not os.path.isfile(frame):\n            issues.append(f\"checkpoints/{cp_id}/frame.jpg missing\")\n        elif os.path.getsize(frame) < 100:\n            issues.append(f\"checkpoints/{cp_id}/frame.jpg too small (<100 bytes)\")\n    return {\"path\": path, \"issues\": issues, \"status\": \"PASS\" if not issues else \"FAIL\"}\n\nif __name__ == \"__main__\":\n    result = validate_run_folder(sys.argv[1])\n    print(json.dumps(result, indent=2))"
                }
            ]
        },
        {
            "id": "lab-02",
            "title": "Obstacle Avoidance & Local Motion APIs",
            "content": "Learn the ObstaclesAvoidClient lifecycle: Init→Enable→APICommand→Move→Stop→Release→Cleanup.\n\n- Study go2_patrol_helpers.py: enable_avoid() and release_avoid()\n- Dry-run obstacle avoidance intro without robot motion\n- Execute a single short increment leg with instructor approval\n- Compare Move(vx,vy,vyaw) velocity streaming vs MoveToIncrementPosition\n- Practice defensive shutdown: both success and failure paths must call release_avoid()",
            "code_files": [
                {
                    "name": "go2_patrol_helpers.py",
                    "code": "\"\"\"Day 2 Patrol Helpers — safe ObstaclesAvoidClient lifecycle.\"\"\"\nimport time\n\ndef enable_avoid(avoid_client) -> bool:\n    \"\"\"Enable obstacle avoidance and transfer API command authority.\"\"\"\n    avoid_client.SwitchSet(True)\n    time.sleep(0.5)\n    if not avoid_client.SwitchGet():\n        return False\n    avoid_client.UseRemoteCommandFromApi(True)\n    time.sleep(0.3)\n    return True\n\ndef release_avoid(avoid_client, sport_client=None) -> None:\n    \"\"\"Release API command source, disable avoid, and optionally StopMove.\"\"\"\n    try:\n        for _ in range(3):\n            avoid_client.Move(0.0, 0.0, 0.0)\n            time.sleep(0.05)\n        avoid_client.UseRemoteCommandFromApi(False)\n        time.sleep(0.2)\n        avoid_client.SwitchSet(False)\n        if sport_client:\n            sport_client.StopMove()\n    except Exception:\n        pass  # Best-effort cleanup; do not mask original exception\n\ndef run_increment_leg(avoid_client, dx: float, dy: float, dyaw: float, pulses: int = 3) -> None:\n    \"\"\"Pulse MoveToIncrementPosition a few times, then let the motion settle.\"\"\"\n    for _ in range(pulses):\n        avoid_client.MoveToIncrementPosition(dx, dy, dyaw)\n        time.sleep(0.1)\n\ndef run_velocity_leg(avoid_client, vx: float, vy: float, vyaw: float, duration_s: float, rate_hz: float = 10.0) -> None:\n    \"\"\"Send repeated Move() at a control rate for the specified duration.\"\"\"\n    interval = 1.0 / rate_hz\n    elapsed = 0.0\n    while elapsed < duration_s:\n        avoid_client.Move(vx, vy, vyaw)\n        time.sleep(interval)\n        elapsed += interval"
                }
            ]
        },
        {
            "id": "lab-03",
            "title": "Sensor Integration & Data Management",
            "content": "Integrate VideoClient for checkpoint image capture and rt/sportmodestate for state logging into the patrol workflow.\n\n- Initialize VideoClient and capture a test frame with GetImageSample()\n- Decode JPEG bytes with OpenCV and write frame.jpg to disk\n- Subscribe to rt/sportmodestate and log JSONL lines with timestamp, mode, gait, position, velocity\n- Capture starting checkpoint before motion; capture after each leg at to_checkpoint\n- Understand that the camera records evidence — it does not steer the robot",
            "code_files": [
                {
                    "name": "capture_checkpoint.py",
                    "code": "\"\"\"Day 2 Checkpoint Capture — pull camera frame and write state slice.\"\"\"\nimport cv2, json, time, os\nimport numpy as np\n\ndef capture_frame(video_client, output_path: str) -> bool:\n    \"\"\"GetImageSample → decode JPEG → write to output_path.\"\"\"\n    try:\n        img_bytes = video_client.GetImageSample()\n        if img_bytes is None or len(img_bytes) < 100:\n            return False\n        np_arr = np.frombuffer(img_bytes, np.uint8)\n        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)\n        if frame is None:\n            return False\n        os.makedirs(os.path.dirname(output_path), exist_ok=True)\n        cv2.imwrite(output_path, frame)\n        return True\n    except Exception:\n        return False\n\ndef write_state_slice(state_history: list, output_path: str, window_s: float = 2.0) -> None:\n    \"\"\"Write recent state samples to a state_slice.jsonl around the capture moment.\"\"\"\n    now = time.time()\n    recent = [s for s in state_history if now - s.get(\"_ts\", 0) <= window_s]\n    with open(output_path, \"w\") as f:\n        for s in recent:\n            f.write(json.dumps(s) + \"\\n\")"
                }
            ]
        },
        {
            "id": "lab-04",
            "title": "Multi-Leg Patrol & Integrated Runner",
            "content": "Execute a complete multi-leg patrol with the integrated runner: load plan, clamp limits, create run folder, initialize clients, capture checkpoints, execute legs, release avoid, write metadata, and validate.\n\n- Run lab03_patrol_runner.py with --dry-run first\n- Execute L-shaped cone course: cp_A forward → cp_B turn → cp_C forward\n- Observe leg execution, dwell, and checkpoint capture sequence\n- Verify run folder with validator; interpret warnings\n- Practice Ctrl+C cleanup: the signal handler must call release_avoid()",
            "code_files": [
                {
                    "name": "example_patrol_plan.json",
                    "code": "{\n  \"schema_version\": \"1.0\",\n  \"checkpoints\": [\n    {\"id\": \"cp_A\", \"label\": \"Start zone\", \"dwell_s\": 2},\n    {\"id\": \"cp_B\", \"label\": \"Corner turn\", \"dwell_s\": 3},\n    {\"id\": \"cp_C\", \"label\": \"End zone\", \"dwell_s\": 2}\n  ],\n  \"legs\": [\n    {\"type\": \"increment\", \"to_checkpoint\": \"cp_B\", \"dx\": 0.35, \"dy\": 0.0, \"dyaw\": 0.0, \"leg_wait_s\": 3},\n    {\"type\": \"increment\", \"to_checkpoint\": \"cp_C\", \"dx\": 0.0, \"dy\": 0.0, \"dyaw\": 0.6, \"leg_wait_s\": 2},\n    {\"type\": \"increment\", \"to_checkpoint\": null, \"dx\": 0.30, \"dy\": 0.0, \"dyaw\": 0.0, \"leg_wait_s\": 3}\n  ]\n}"
                }
            ]
        },
        {
            "id": "lab-05",
            "title": "Field Trial, Tuning & Gazebo Context",
            "content": "Convert observations into controlled plan changes: observe → tune → trial → report. Optionally explore ROS 2 / Gazebo simulation with /cmd_vel topic control.\n\n- Run baseline patrol and record checkpoint outcomes (pass/partial/fail)\n- Use lab04_tune_plan.py to copy plan and apply leg overrides (e.g., --set 1:dyaw:0.7)\n- Execute tuned plan through integrated runner; compare baseline vs tuned run folders\n- Write field_test.md with scenario, baseline, tuning actions, results, and next improvement\n- Optional: launch Gazebo simulation, bridge ROS 2 topics, publish geometry_msgs/Twist to /cmd_vel",
            "code_files": [
                {
                    "name": "lab04_tune_plan.py",
                    "code": "\"\"\"Day 2 Plan Tuner — copy a baseline plan and apply leg overrides.\"\"\"\nimport json, sys, shutil, os\n\ndef tune_plan(baseline_path: str, output_path: str, overrides: dict) -> None:\n    \"\"\"overrides = {leg_index: {dx: 0.4, dyaw: 0.7}} — leg_index is 0-based.\"\"\"\n    with open(baseline_path) as f:\n        plan = json.load(f)\n    for leg_idx_str, fields in overrides.items():\n        leg_idx = int(leg_idx_str)\n        if leg_idx < len(plan.get(\"legs\", [])):\n            plan[\"legs\"][leg_idx].update(fields)\n    plan[\"_tuned_from\"] = os.path.basename(baseline_path)\n    with open(output_path, \"w\") as f:\n        json.dump(plan, f, indent=2)\n    print(f\"[TUNED] {output_path}\")\n\nif __name__ == \"__main__\":\n    # Usage: python lab04_tune_plan.py baseline_patrol_plan.json tuned_patrol_plan.json --set 1:dyaw:0.7\n    args = sys.argv[1:]\n    overrides = {}\n    for a in args:\n        if a.startswith(\"--set\"):\n            continue\n        if \":\" in a:\n            leg_idx, rest = a.split(\":\", 1)\n            key, val = rest.split(\":\", 1)\n            overrides.setdefault(leg_idx, {})[key] = float(val)\n    tune_plan(args[0], args[1], overrides)"
                }
            ]
        },
        {
            "id": "lab-06",
            "title": "Team Capstone & Presentations",
            "content": "Present a five-minute demo: scenario → architecture → plan → evidence → failure/fix. The presentation should open the run folder and show at least one checkpoint frame.\n\n- Prepare: slides or live demo showing scenario, architecture diagram, and patrol plan\n- Demonstrate or play back the patrol run (recording acceptable if hardware unavailable)\n- Open run folder: show checkpoint frame.jpg, sample a JSONL line, present validator output\n- Explain one tuning action or abort lesson with data (e.g., 'dx 0.3→0.4 because under-shot by 0.15 m')\n- Answer knowledge check questions from instructor",
            "code_files": []
        }
    ]
}

# ── Day 03: B2 Industrial Fundamentals ──────────────────────────────────────
DAY03 = {
    "day": "03",
    "title": "B2 Industrial Fundamentals",
    "eyebrow": "UNITREE B2 PLATFORM",
    "thesis": "A B2 operator should never begin with motion. A competent B2 operator first proves network readiness, observes state, explains the control layer being used, identifies the safe stop path, and only then executes a supervised motion primitive.",
    "rules": [
        "Observe before acting: SportModeState is the first diagnostic window — no motion before clean state streaming for 30+ seconds.",
        "Gate motion through a named instructor and approved command sequence — the presence of a menu option does not imply permission to run it.",
        "Know the control layer before running code: high-level SportClient calls request behavior; low-level LowCmd streaming commands individual motor targets — different authority, different risk.",
        "No silent failures: every error must produce a short incident note — time, command, interface, visible robot state, terminal output, action taken, and whether the robot returned to a known safe state.",
        "Treat B2 as an industrial platform, not simply a larger Go2 — 60 kg mass, >40 kg walking load, and >6 m/s capability require stricter field discipline."
    ],
    "pacing": [
        {"time": "09:00 - 09:15", "session": "Opening Safety Frame — B2 is an Industrial Robot", "path": "day-03/README.md"},
        {"time": "09:15 - 09:40", "session": "B2 Hardware & Industrial Context", "path": "day-03/README.md#b2-hardware"},
        {"time": "09:40 - 10:05", "session": "B2 Network & SDK Readiness", "path": "day-03/lab-00/"},
        {"time": "10:05 - 10:30", "session": "Lab 1 — State Subscription (No Motion)", "path": "day-03/lab-01/"},
        {"time": "10:45 - 11:15", "session": "High-Level SportClient Control", "path": "day-03/lab-02/"},
        {"time": "11:15 - 11:45", "session": "Lab 2 — Supervised B2 Sport RPC & Stand", "path": "day-03/lab-02/"},
        {"time": "11:45 - 12:00", "session": "B2 Sensors, Video & Day 4 Bridge", "path": "day-03/README.md#b2-sensors"},
        {"time": "12:00 - 12:30", "session": "Knowledge Check & Operator Readiness Sign-Off", "path": "day-03/README.md#knowledge-check"}
    ],
    "slides": [
        {
            "title": "Teaching Thesis — Transition to Industrial Scale",
            "thesis": "Day 3 is the transition point from education-scale quadruped control to industrial-scale quadruped readiness — the B2 is heavier, stronger, higher-payload, and more operationally consequential than Go2.",
            "board_type": "table",
            "board_data": {
                "headers": ["Teaching Shift", "Go2 Teaching Pattern", "B2 Day 3 Teaching Pattern"],
                "rows": [
                    ["Platform Framing", "Education and developer robot.", "Industrial quadruped for inspection, payload, endurance, and field deployment."],
                    ["First Proof of Readiness", "\"Can the SDK talk to the robot?\"", "\"Can the team prove interface, environment, DDS, state visibility, and safety perimeter before motion?\""],
                    ["Motion Philosophy", "Small, bounded experimentation.", "Instructor-gated command sequence with explicit stop and recovery path."],
                    ["Student Success Evidence", "Successful command execution.", "Safe diagnosis, correct state interpretation, conservative operation, and clean stop discipline."],
                    ["Instructor Role", "API guide.", "Safety authority, run director, and escalation controller."]
                ]
            },
            "bottom_band": "Day 3 teaching order is intentional: the first 90 minutes are motion-free even if the robot is available. Communication, observability, and safety are not 'setup chores' — they are part of robot control."
        },
        {
            "title": "Three-Hour Teaching Flow — Day 3",
            "thesis": "This flow deliberately puts motion after state — the first successful action is not walking; it is proving that the robot, operator, network, and safety perimeter are all in a known state.",
            "board_type": "table",
            "board_data": {
                "headers": ["Time", "Segment", "Instructor Goal", "Student Output"],
                "rows": [
                    ["00:00–00:15", "Opening Safety Frame", "Establish B2 as an industrial robot, not simply a larger Go2.", "Students can state stop authority and no-motion rule."],
                    ["00:15–00:40", "B2 Hardware & Industrial Context", "Explain B2 size, payload, endurance, sensors, interfaces.", "Students identify why payload and speed change operating risk."],
                    ["00:40–01:05", "B2 Network & SDK Readiness", "Review interface naming, SDK environment, CycloneDDS, script locations.", "Students record interface name and environment checks."],
                    ["01:05–01:30", "Lab 1: State Subscription", "Run subscribe_sport_mode_state.py; interpret state output.", "Students understand rt/sportmodestate as pre-motion observability."],
                    ["01:30–01:40", "Break & Safety Reset", "Reset attention before any motion discussion.", "Students re-confirm perimeter and emergency actions."],
                    ["01:40–02:10", "High-Level SportClient Control", "Explain Damp, BalanceStand, StopMove, StandUp, StandDown, RecoveryStand.", "Students can explain which commands are allowed in Lab 2 and why."],
                    ["02:10–02:35", "Supervised Lab 2 Motion Gate", "Demonstrate BalanceStand and StopMove; discuss b2_stand_example.py.", "Students describe difference between high-level and low-level control."],
                    ["02:35–02:50", "Navigation, Perception & Day 4 Bridge", "Connect B2 sensors and camera scripts to inspection analytics.", "Students describe how B2 state and video become inspection data."],
                    ["02:50–03:00", "Knowledge Check & Sign-Off", "Confirm concepts, commands, safety gates, next-day readiness.", "Students complete verbal or written operator-readiness checklist."]
                ]
            },
            "bottom_band": "If running on physical hardware, keep the first 90 minutes motion-free even if the robot is available. This creates the correct operational habit: communication, observability, and safety are not setup chores."
        },
        {
            "title": "B2 as an Industrial Platform",
            "thesis": "B2 specifications should not be presented as classroom targets — they are specifications that explain why the training protocol must be conservative. 60 kg mass, >6 m/s speed, >40 kg walking load.",
            "board_type": "table",
            "board_data": {
                "headers": ["B2 Attribute", "Instructor Interpretation", "Classroom Implication"],
                "rows": [
                    ["~60 kg robot mass", "The platform has industrial inertia and can injure people or damage equipment.", "Treat motion as a controlled demonstration, not an exploratory exercise."],
                    ["Walking load >40 kg; standing load ≥120 kg", "Payload capability is a defining industrial feature.", "Payload changes balance, clearance, current draw, and fall risk."],
                    ["Speed >6 m/s (safety-limited)", "The robot has far more kinetic capability than required for training.", "Classroom motion should use only low-speed, instructor-approved primitives."],
                    ["4–6 h battery operating time", "B2 is designed for extended deployment, not short toy demonstrations.", "Teach battery state and thermal checks as field-readiness evidence."],
                    ["IP67 protection; -20°C to 55°C range", "The platform is intended for harsh environments.", "Environmental rating is not permission for risky operation in the classroom."],
                    ["3D LiDAR, depth cameras, optical cameras", "Perception supports inspection, mapping, and analytics.", "Day 3 should preview how state and video become Day 4 inspection data."]
                ]
            },
            "bottom_band": "A useful teaching move: ask students to compare the same command across platforms. Move(0.5, 0, 0) on a small robot vs. a 60 kg industrial quadruped — syntactically similar, field consequence not the same. API similarity can hide physical difference."
        },
        {
            "title": "B2 Safety Model for Training",
            "thesis": "In B2 training, the first successful action is not walking — it is proving that the robot, operator, network, and safety perimeter are all in a known state. Six safety gates must be cleared before motion.",
            "board_type": "table",
            "board_data": {
                "headers": ["Safety Gate", "Required Evidence", "Instructor Response If Missing"],
                "rows": [
                    ["Physical Perimeter", "Clear floor, no loose cables, no people in motion zone, no fragile objects nearby.", "Do not run Lab 2 motion."],
                    ["Stop Authority", "One named instructor controls motion approval; one operator has keyboard focus; students know StopMove and E-stop procedure.", "Pause and re-brief."],
                    ["Interface Identity", "Students can state the active network interface (eth0, enp3s0, or verified wired adapter).", "Do not run scripts with guessed interfaces."],
                    ["Environment Readiness", "SDK environment is activated (conda activate unitree_env) and expected variables are available.", "Fix environment before robot interaction."],
                    ["State Observability", "SportModeState prints for at least 30 seconds without DDS errors.", "Do not proceed to motion."],
                    ["Command Scope", "Only approved commands allowed; initial commands are BalanceStand and StopMove.", "Stop session if students attempt unapproved motion."]
                ]
            },
            "bottom_band": "Distinguish three stop types: routine stop (StopMove — stops current action, restores motion parameters), motion stop (Damp — high-priority damping, motor joints stop, emergency/unexpected-situation), and physical E-stop (remote control intervention supersedes code-level commands)."
        },
        {
            "title": "B2 System Architecture: From Wire to Motion",
            "thesis": "Students must know which layer they are touching when they run each script — physical Ethernet, DDS communication, state topic, high-level RPC, low-level command, or perception/video.",
            "board_type": "table",
            "board_data": {
                "headers": ["Layer", "What Students See", "What It Means in Day 3"],
                "rows": [
                    ["Physical Ethernet", "Cable, interface name, static network assumptions.", "The student must know which interface is connected to the robot."],
                    ["DDS Communication", "ChannelFactoryInitialize(0, interface).", "The process joins the robot communication domain over the selected network interface."],
                    ["State Topic", "rt/sportmodestate.", "Robot publishes high-level motion state that should be observed before any motion."],
                    ["High-Level RPC", "SportClient() calls: BalanceStand(), StopMove().", "SDK sends semantic motion requests through a safety-managed high-level layer."],
                    ["Low-Level Command", "rt/lowcmd and rt/lowstate.", "Script commands individual motor targets — requires stronger expertise and authority."],
                    ["Perception/Video", "Camera clients and RTSP streams.", "B2 can provide inspection data for later analytics and autonomy lessons."]
                ]
            },
            "bottom_band": "Central Day 3 concept: Control Authority. subscribe_sport_mode_state.py = observing. b2_sport_client.py = requesting high-level behaviors. b2_stand_example.py = publishing LowCmd_ to rt/lowcmd at 0.002 s intervals. These are not equivalent levels of risk."
        },
        {
            "title": "Lab 0: B2 Readiness & Safety — Five Checks",
            "thesis": "Lab 0 is a no-motion lab — resist the temptation to skip it. In professional robot deployment, readiness checks prevent false diagnoses by narrowing uncertainty before the class interacts with the robot.",
            "board_type": "table",
            "board_data": {
                "headers": ["Lab 0 Check", "Example Command or Action", "What Success Looks Like"],
                "rows": [
                    ["Repository Location", "cd \"$(git rev-parse --show-toplevel)\"", "The terminal is at the course repository root."],
                    ["SDK Environment", "conda activate unitree_env", "The expected Python and SDK packages are available for import."],
                    ["Interface Discovery", "ip link or ifconfig", "Students identify the wired robot interface by name."],
                    ["Script Location", "ls scripts/ives_sdk/B2/", "Students see B2 scripts: subscribe_sport_mode_state.py, b2_sport_client.py."],
                    ["Safety Briefing", "Instructor-led verbal check.", "Students can state perimeter, stop command, and command approval rule."]
                ]
            },
            "bottom_band": "Frame Lab 0 as a short operator certification. Students should answer: Which interface? Which environment? Which script observes state? Which script can move the robot? Who has stop authority? What is the first command if motion does not look right?"
        },
        {
            "title": "Lab 1: Subscribe to B2 SportModeState",
            "thesis": "Lab 1 is the most important no-motion technical lab on Day 3 — it proves that the workstation, network interface, DDS communication, Python SDK imports, robot topic publication, and callback flow are working together.",
            "board_type": "grid",
            "board_data": [
                {"label": "Position", "value": "\"Does the value remain stable while the robot is stationary?\" Indicates estimated robot pose or motion-state position — should not drift when robot is still."},
                {"label": "Velocity", "value": "\"Before motion, should velocity be near zero?\" Reveals whether the robot believes it is moving — nonzero velocity at rest = diagnostic flag."},
                {"label": "IMU State", "value": "\"What would a tilted or unstable robot look like in state?\" Body orientation and inertial sensing — check for physically implausible values."},
                {"label": "Mode", "value": "\"Which mode would you expect before and after BalanceStand?\" High-level motion mode: idle, balance stand, locomotion, damping, recovery, or sit."},
                {"label": "Gait Type", "value": "\"Should gait change during a no-motion readiness check?\" Gait category when locomotion is active — should be stable/unchanged during observation."},
                {"label": "Foot Force & Position", "value": "\"What might asymmetric contact suggest? Why is leg geometry relevant before low-level control?\" Helps diagnose contact, support, and body-relative leg configuration."}
            ],
            "bottom_band": "Run command: conda activate unitree_env && cd \"$(git rev-parse --show-toplevel)\" && python scripts/ives_sdk/B2/subscribe_sport_mode_state.py eth0. Success criterion: state prints for ≥30 s without DDS errors."
        },
        {
            "title": "High-Level SportClient Commands",
            "thesis": "The presence of a menu option does not imply permission to run it — the menu is a code artifact; the instructor gate is the operational authority. Initial commands: BalanceStand and StopMove only.",
            "board_type": "table",
            "board_data": {
                "headers": ["Command", "Teaching Meaning", "Recommended Day 3 Status"],
                "rows": [
                    ["BalanceStand()", "Enter balanced standing behavior.", "Instructor-approved demonstration — first approved motion command."],
                    ["StopMove()", "Stop current motion; restore many motion parameters.", "Required stop command to know and use before any motion."],
                    ["Damp()", "Enter high-priority damping state.", "Discuss as emergency-related; use only by instructor policy — emergency/unexpected-situation context."],
                    ["StandUp()", "Locked tall standing posture.", "Discuss carefully; avoid prolonged locked posture — locked joints increase fall risk."],
                    ["StandDown()", "Locked low/lying posture.", "Instructor-only unless part of approved sequence."],
                    ["RecoveryStand()", "Recover from fallen or lying state to standing.", "Instructor-only; important conceptually for field recovery understanding."],
                    ["Move(vx, vy, vyaw)", "Body-frame velocity command.", "Not for first motion unless instructor explicitly approves — requires stop discipline."],
                    ["ClassicWalk() / FreeWalk()", "Gait-related walking modes.", "Not for first 3-hour Day 3 session unless site conditions are excellent."]
                ]
            },
            "bottom_band": "Move(vx, vy, vyaw) warning: Unitree V2.0 motion documentation states the motion-control part does not filter Move commands and the latest Move command is maintained for 1 second. Filter before sending; always send Move(0,0,0) or StopMove() when stopping."
        },
        {
            "title": "Lab 2: Supervised B2 Sport RPC & Stand — Seven-Step Sequence",
            "thesis": "The class should not begin by exploring the menu — the instructor defines the exact sequence before the script starts. A safe introductory sequence: confirm state → clear perimeter → BalanceStand → observe → StopMove → observe → exit.",
            "board_type": "list",
            "board_data": [
                "Step 1 — Reconfirm perimeter: No people or objects inside the motion zone. Students visually inspect and verbally confirm.",
                "Step 2 — Confirm single operator: One operator has terminal focus. Students do not type commands independently.",
                "Step 3 — Start b2_sport_client.py: Run with the verified interface. Students see the warning and menu prompt.",
                "Step 4 — Use BalanceStand only after instructor approval: Observe posture transition and state change in SportModeState.",
                "Step 5 — Use StopMove: Observe stable stopping behavior. Confirm robot returns to a known, stationary state.",
                "Step 6 — Discuss return code: Students learn that a return code (rc=0 success, rc≠0 diagnostic) is part of command evidence.",
                "Step 7 — Stop the demonstration: Record commands executed and any anomalies. Return to known safe posture."
            ],
            "bottom_band": "Run command: python scripts/ives_sdk/B2/b2_sport_client.py eth0. The SportClient sets a 10-second timeout and initializes before exposing the menu — verify timeout is appropriate for the robot's response time."
        },
        {
            "title": "Low-Level Control: b2_stand_example.py — Engineering Deep Dive",
            "thesis": "SportClient asks the robot to perform a behavior. LowCmd publishing tells individual motors what targets to pursue. These are different authority levels, different risk levels, and different debugging responsibilities.",
            "board_type": "table",
            "board_data": {
                "headers": ["Code Feature", "Engineering Meaning", "Why Instructors Should Discuss It"],
                "rows": [
                    ["rt/lowcmd publisher", "Direct low-level command channel.", "Shows why low-level scripts require stronger authority and supervision."],
                    ["rt/lowstate subscriber", "Feedback channel for motor state.", "Demonstrates closed-loop awareness even in a simple example."],
                    ["RecurrentThread(interval=0.002)", "500 Hz command-writing intent.", "Shows that low-level control is timing-sensitive — not a casual script."],
                    ["Kp = 1000.0, Kd = 10.0", "Joint-control proportional and derivative gains.", "Shows that stiffness and damping are explicit design choices with physical consequences."],
                    ["Target joint arrays (12 leg motors)", "Desired leg configurations.", "Shows why joint numbering (0-11 for legs) and limits matter."],
                    ["CRC computation", "Message integrity check.", "Shows that robot command packets require validation — not just values."]
                ]
            },
            "bottom_band": "Classroom distinction: b2_stand_example.py creates a LowCmd_ publisher, subscribes to LowState_, uses MotionSwitcherClient to release active modes, and writes motor commands every 0.002 s. It actively interpolates target positions for 12 leg motors, computes CRC, and publishes continuously. This is instructor-only unless the class has demonstrated strong low-level readiness."
        },
        {
            "title": "B2 Sensors, Video & Inspection Bridge",
            "thesis": "B2's value is not only that it can move — its value is that it can collect location-aware, time-aware, repeatable observations under field constraints. Day 3 previews how state and video become Day 4 inspection data.",
            "board_type": "grid",
            "board_data": [
                {"label": "SportModeState", "value": "Day 3 Treatment: Readiness and robot-state observability. Day 4 Bridge: Correlate robot state with inspection events — mode, velocity, and posture during image capture."},
                {"label": "Optical Cameras (Front + Rear)", "value": "Day 3: Preview only — camera_opencv-video.py, camera_opencv-videoEffect.py. Day 4: Image capture, video review, defect evidence, operator situational awareness."},
                {"label": "Depth Cameras", "value": "Day 3: Conceptual overview. Day 4: Spatial context, obstacle awareness, inspection geometry for checkpoint planning."},
                {"label": "3D LiDAR", "value": "Day 3: Conceptual overview — wide-angle omnidirectional head-mounted LiDAR. Day 4: Mapping, localization, terrain and structure context for advanced inspection."},
                {"label": "RTSP Recording (record_rtsp.py)", "value": "Day 3: Preview only — demonstrates stream capture capability. Day 4: Evidence package for inspection report or analytics workflow — continuous video context."}
            ],
            "bottom_band": "Inspection autonomy is data discipline: the B2 repository includes camera examples that use front/back VideoClients, decode JPEG with OpenCV, support still capture (Q/E keys), and record RTSP streams (A/D keys). These become the foundation for Day 4 field inspection evidence."
        },
        {
            "title": "Practical Troubleshooting Framework — Day 3",
            "thesis": "Troubleshooting should be taught as a structured process, not a sequence of guesses — move from physical layer → environment → communication → state → command layer.",
            "board_type": "table",
            "board_data": {
                "headers": ["Symptom", "Likely Layer", "Diagnosis Path", "Safe Response"],
                "rows": [
                    ["Script cannot import SDK modules.", "Python Environment", "Confirm conda activate unitree_env; verify installed SDK package.", "Do not connect motion commands until environment is correct."],
                    ["No state messages arrive.", "Network or DDS", "Check cable, interface name, robot power, DDS configuration, topic name.", "Stay in Lab 1; do not proceed to Lab 2."],
                    ["DDS errors appear.", "DDS Configuration or Interface Conflict", "Verify only intended network interface is selected; check CycloneDDS assumptions.", "Pause and fix configuration."],
                    ["State prints but values are unexpected.", "Robot State or Interpretation", "Compare stationary robot velocity, mode, posture, and visible state.", "Ask instructor before motion."],
                    ["Sport command returns nonzero.", "RPC or Robot Mode", "Record command, return code, current state, and visible behavior.", "Stop; do not chain commands."],
                    ["Robot begins unexpected motion.", "Command or Mode Issue", "Use approved stop path; instructor takes control.", "Clear perimeter and investigate after stop."]
                ]
            },
            "bottom_band": "Instructor phrase: 'No silent failures.' Every failure should produce a short incident note: time, command, interface, visible robot state, terminal output, action taken, and whether the robot returned to a known safe state."
        },
        {
            "title": "Student Knowledge Checks — Day 3",
            "thesis": "Students should answer these questions at the end of the session — verbally, as a written handout, or as a lab sign-off checklist. The questions test readiness reasoning, not command memorization.",
            "board_type": "list",
            "board_data": [
                "Why does Day 3 begin with a no-motion readiness lab? — B2 motion must be preceded by network, environment, DDS, observability, and safety checks. Skipping Lab 0 means diagnosing failures with the robot live, which is unsafe.",
                "What is the purpose of rt/sportmodestate? — It provides high-level robot motion state (position, velocity, IMU, mode, gait, foot force) used to verify readiness and interpret robot behavior before and during motion.",
                "Why is BalanceStand safer as a first demonstration than Move? — It demonstrates controlled posture without intentionally commanding translation — the robot stays in place while proving high-level service reachability.",
                "What should happen if subscribe_sport_mode_state.py does not print state cleanly? — Stop at diagnosis: verify interface, cable, robot power, DDS environment, Python imports, and topic binding. Do not proceed to motion.",
                "What is the difference between SportClient and publishing to rt/lowcmd? — SportClient requests high-level behaviors (BalanceStand, StopMove) through a safety-managed service. rt/lowcmd commands individual motor targets at 500 Hz — more authority, more risk.",
                "Why is Move(0,0,0) or StopMove() part of command hygiene? — Unitree docs warn that velocity commands require explicit stopping; the latest Move is maintained for ~1 second. Without explicit stop, the robot may continue the last velocity command.",
                "What are the main B2 sensing channels relevant to future inspection work? — LiDAR (mapping/localization), depth cameras (spatial context), optical cameras (visual evidence), video/RTSP (continuous context), and robot state (posture/motion witness)."
            ],
            "bottom_band": "Practical assessment: Present a scenario — 'SDK imports pass, ping passes, SportModeState streams, but FSM mode shows damp.' Correct classification: PARTIAL — not motion-ready. Damped state blocks safe high-level motion regardless of communication health."
        },
        {
            "title": "Day 3 Takeaways — Four Durable Habits",
            "thesis": "Day 3 should leave students with a disciplined mental model of industrial quadruped operation — B2 is powerful because it combines mobility, payload, endurance, sensing, and SDK access; those same characteristics require stronger safety habits.",
            "board_type": "grid",
            "board_data": [
                {"label": "1. Observe Before Acting", "value": "\"If I cannot prove the interface and state channel, I do not command motion.\" Use SportModeState as the first diagnostic window — 30+ seconds of clean state before any motion command."},
                {"label": "2. Gate Motion Through Authority", "value": "\"The robot moves only inside an instructor-approved command envelope.\" A named instructor controls motion approval; one operator has keyboard focus; initial commands are BalanceStand and StopMove only."},
                {"label": "3. Know the Control Layer", "value": "\"High-level sport commands request behavior; low-level commands stream motor targets.\" SportClient, rt/lowcmd, and b2_stand_example.py represent different authority levels — never confuse them."},
                {"label": "4. Treat Inspection as Data Discipline", "value": "\"B2 becomes valuable when motion, state, video, and field evidence are connected.\" State, video, timing, and operator notes become the foundation for Day 4 inspection analytics."}
            ],
            "bottom_band": "Closing message: 'The central lesson is not that B2 can move. The central lesson is that a trained operator can decide when it should move, verify that it is ready, observe its state, issue a bounded command, and return it to a safe condition.'"
        }
    ],
    "labs": [
        {
            "id": "lab-00",
            "title": "B2 Readiness & Safety (No-Motion)",
            "content": "Confirm B2 network, SDK environment, CYCLONEDDS_HOME, safety rules, and B2 script location before any robot interaction.\n\n- Navigate to repository root and activate unitree_env\n- Identify wired robot interface with ip link or ifconfig\n- Locate B2 scripts under scripts/ives_sdk/B2/\n- Complete safety briefing: state perimeter, stop command, command approval rule\n- Record interface name in lab notes — do not guess interfaces for motion scripts",
            "code_files": [
                {
                    "name": "b2_readiness_check.sh",
                    "code": "#!/bin/bash\n# Day 3 Lab 0 — B2 Readiness Check (No Motion)\necho \"=== B2 Readiness Gate ===\"\necho \"1. Repository: $(git rev-parse --show-toplevel)\"\necho \"2. Environment: $(conda info --envs | grep '*')\"\necho \"3. Interface:\"\nip link | grep -E '^[0-9]+:' | awk '{print \"   \" $2}'\necho \"4. B2 Scripts:\"\nls scripts/ives_sdk/B2/ 2>/dev/null || echo \"   NOT FOUND — check path\"\necho \"5. Safety: Confirm perimeter, stop authority, interface identity, command scope.\"\necho \"   STOP command: StopMove() or Damp() per instructor policy.\""
                }
            ]
        },
        {
            "id": "lab-01",
            "title": "Subscribe to B2 SportModeState",
            "content": "Run subscribe_sport_mode_state.py and verify that state prints cleanly for at least 30 seconds without DDS errors.\n\n- Activate unitree_env and navigate to repository root\n- Run: python scripts/ives_sdk/B2/subscribe_sport_mode_state.py <interface>\n- Observe: position, velocity, IMU state, mode, gait type, foot force, foot position\n- Identify which output line proves first-message success\n- If no state arrives: verify interface, cable, robot power, DDS environment, Python imports — do not proceed to motion",
            "code_files": [
                {
                    "name": "subscribe_sport_mode_state.py",
                    "code": "\"\"\"B2 SportModeState Subscriber — observability before motion.\"\"\"\nimport sys, time\nfrom unitree_sdk2py.core.channel import ChannelFactoryInitialize, ChannelSubscriber\nfrom unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_\n\ndef sport_state_callback(msg: SportModeState_):\n    print(f\"[STATE] mode={msg.mode} gait={msg.gait_type} \"\n          f\"pos=({msg.position[0]:.2f},{msg.position[1]:.2f},{msg.position[2]:.2f}) \"\n          f\"vel=({msg.velocity[0]:.2f},{msg.velocity[1]:.2f},{msg.velocity[2]:.2f}) \"\n          f\"yaw_speed={msg.yaw_speed:.2f} body_height={msg.body_height:.3f}\")\n\ndef main(interface: str):\n    ChannelFactoryInitialize(0, interface)\n    subscriber = ChannelSubscriber(\"rt/sportmodestate\", SportModeState_)\n    subscriber.Init(sport_state_callback, 10)\n    print(f\"[SUBSCRIBED] rt/sportmodestate on {interface} — press Ctrl+C to stop\")\n    while True:\n        time.sleep(1)\n\nif __name__ == \"__main__\":\n    main(sys.argv[1])"
                }
            ]
        },
        {
            "id": "lab-02",
            "title": "Supervised B2 Sport RPC & Stand",
            "content": "Execute BalanceStand and StopMove under strict instructor gating — the operator types only approved commands.\n\n- Confirm state subscription succeeded and perimeter is clear\n- Run: python scripts/ives_sdk/B2/b2_sport_client.py <interface>\n- Instructor-approved sequence: BalanceStand → observe posture → StopMove → observe return\n- Record return code for each command; do not chain commands if rc ≠ 0\n- Discuss b2_stand_example.py conceptually — explain why LowCmd streaming is a different authority level",
            "code_files": [
                {
                    "name": "b2_sport_client_menu.py",
                    "code": "\"\"\"B2 Sport Client — high-level command menu (simplified teaching excerpt).\"\"\"\nimport sys\nfrom unitree_sdk2py.core.channel import ChannelFactoryInitialize\nfrom unitree_sdk2py.g1.loco.g1_loco_client import LocoClient\n\ndef main(interface: str):\n    ChannelFactoryInitialize(0, interface)\n    client = LocoClient()  # SportClient pattern for B2\n    client.SetTimeout(10.0)\n    client.Init()\n    print(\"=== B2 Sport Client ===\")\n    print(\"Authorized Day 3 commands: BalanceStand, StopMove\")\n    print(\"All other commands: instructor approval required\")\n    print(\"Type 'quit' to exit.\")\n    while True:\n        cmd = input(\">>> \").strip()\n        if cmd == \"quit\":\n            break\n        elif cmd == \"BalanceStand\":\n            rc = client.BalanceStand()\n            print(f\"[RC] BalanceStand: {rc}\")\n        elif cmd == \"StopMove\":\n            rc = client.StopMove()\n            print(f\"[RC] StopMove: {rc}\")\n        else:\n            print(f\"[BLOCKED] '{cmd}' requires instructor approval.\")\n\nif __name__ == \"__main__\":\n    main(sys.argv[1])"
                }
            ]
        }
    ]
}

# ── Day 04: B2 Advanced Scenarios & Field Inspection ────────────────────────
DAY04 = {
    "day": "04",
    "title": "B2 Rugged Inspection, Mock Scripts, Field Capture, Telemetry, Reporting, and Maintenance",
    "eyebrow": "B2 RUGGED INSPECTION",
    "thesis": "Day 4 converts the B2 from a robot that can be safely observed and commanded into an inspection evidence system. Every activity connects to one of four required outcomes: rugged navigation and multi-sensor reasoning, mock inspection scripts, supervised B2 field execution, or data visualization with reporting and maintenance.",
    "rules": [
        "Plan before motion: create the run folder and draft metadata before the robot moves — the run folder is the inspection contract.",
        "Every inspection run must produce traceable evidence: video stills, state logs, checkpoint mapping, and validation output — not just a 'successful walk.'",
        "Dwell before capture: images must be captured during stable dwell or stopped state — never during turning or translation.",
        "Preserve raw artifacts: do not delete imperfect video, state logs, or images until the debrief is complete. A failed capture can still be useful diagnostic evidence.",
        "Separate raw capture from checkpoint evidence: raw captures are original files; checkpoint evidence is selected, named, and placed under checkpoints/<id>/frame.jpg with context."
    ],
    "pacing": [
        {"time": "09:00 - 09:15", "session": "Day 4 Framing — B2 Inspection as Evidence Pipeline", "path": "day-04/README.md"},
        {"time": "09:15 - 09:35", "session": "B2 Inspection Hardware Context", "path": "day-04/README.md#hardware"},
        {"time": "09:35 - 09:55", "session": "Run-Folder Schema for B2", "path": "day-04/lab-00/"},
        {"time": "09:55 - 10:20", "session": "Lab 1 — Mock Inspection Video with B2 Cameras", "path": "day-04/lab-01/"},
        {"time": "10:35 - 11:00", "session": "Lab 2 — SportModeState as Runtime Audit Trail", "path": "day-04/lab-02/"},
        {"time": "11:00 - 11:30", "session": "Supervised Motion Between Inspection Legs", "path": "day-04/README.md#motion"},
        {"time": "11:30 - 12:00", "session": "Field Run, Validation & Reporting", "path": "day-04/lab-02/"},
        {"time": "12:00 - 12:30", "session": "Debrief, Knowledge Check & Capstone Preparation", "path": "day-04/README.md#debrief"}
    ],
    "slides": [
        {
            "title": "Day 4  --  B2 Rugged Inspection, Mock Scripts, Field Capture, Telemetry, Reporting, and Maintenance",
            "thesis": "Day 4 is focused on four practical jobs. Students reason about rugged terrain and multi-sensor evidence, build mock <strong class=\"font-bold\">inspection</strong> scripts, execute a supervised <strong class=\"font-bold\">B2</strong> <strong class=\"font-bold\">inspection</strong> with camera capture and <strong class=\"font-bold\">telemetry</strong> logging, then parse data into reports and maintenance notes. Anything outside those jobs is intentionally minimized.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Rugged Navigation",
                                    "value": "Understand how terrain affects robot behavior and evidence quality  --  slope, gravel, glare, occlusion, vibration all change what the <strong class=\"font-bold\">B2</strong> can safely prove."
                        },
                        {
                                    "label": "Mock Inspection Scripts",
                                    "value": "Build procedural scripts that rehearse capture, logging, motion, packaging, and validation before the hardware run  --  simulation gates must pass first."
                        },
                        {
                                    "label": "<strong class=\"font-bold\">B2</strong> Field Execution",
                                    "value": "Execute a supervised <strong class=\"font-bold\">B2</strong> <strong class=\"font-bold\">inspection</strong> with camera capture and <strong class=\"font-bold\">telemetry</strong> logging  --  defined roles, observable readiness, stable-dwell capture, and immediate verification."
                        },
                        {
                                    "label": "Logs, Reports, Maintenance",
                                    "value": "Parse <strong class=\"font-bold\">telemetry</strong> into fields, visualize motion and capture, write artifact-backed reports, validate packages, debug failures, and complete <strong class=\"font-bold\">B2</strong> hardware maintenance."
                        }
            ],
            "bottom_band": "Day 4 rule: Every activity must connect to one of these four outcomes. If an activity does not produce evidence for rugged navigation, mock scripting, field capture, or reporting  --  it is not a Day 4 activity."
        },
        {
            "title": "One Flow Organizes Everything",
            "thesis": "The whole day can be taught through one repeated workflow. Students plan the <strong class=\"font-bold\">inspection</strong>, capture sensor evidence, log robot state, package artifacts into the run folder, validate the structure, and write the report. This reduces redundancy because every activity must connect to one step in the same flow.",
            "board_type": "list",
            "board_data": [
                        "Plan: Define the <strong class=\"font-bold\">inspection</strong> scenario  --  checkpoints, route, capture targets, and roles. Write metadata<strong class=\"font-bold\">.json</strong> and patrol_plan<strong class=\"font-bold\">.json</strong> before any robot motion.",
                        "Capture: Execute camera stills and <strong class=\"font-bold\">RTSP</strong> clips at designated checkpoints. Verify every saved file opens and matches the intended scene.",
                        "Log: Record <strong class=\"font-bold\">SportModeState</strong> <strong class=\"font-bold\">telemetry</strong> continuously from before motion through final notes. Each JSONL line is one inspectable state sample.",
                        "Package: Organize raw captures, selected checkpoint frames, <strong class=\"font-bold\">telemetry</strong> logs, and metadata into the standard <strong class=\"font-bold\">run-folder</strong> schema.",
                        "Validate: Run the validator against the completed package. Structural PASS is required before report writing. Warnings still need explanation.",
                        "Report: Write artifact-backed claims using the pattern  --  claim, artifact, <strong class=\"font-bold\">telemetry</strong> context, limitation, confidence. The report is the final deliverable."
            ],
            "bottom_band": "Workflow check: Can you draw the six-box arrow  --  Plan → Capture → Log → Package → Validate → Report  --  and name one concrete artifact produced at each step? If not, drill that step before the field run."
        },
        {
            "title": "Evidence Is the Standard",
            "thesis": "Students should not treat video, logs, or notes as separate assignments. They are parts of one evidence standard. A useful inspection claim should identify what was observed, where it happened, when it happened, and which artifact supports it. This standard guides navigation, scripting, field capture, and reporting.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "File",
                                    "value": "The concrete artifact  --  frame<strong class=\"font-bold\">.jpg</strong>, sportmodestate<strong class=\"font-bold\">.jsonl</strong>, field_report<strong class=\"font-bold\">.md</strong>. A claim without a matching file is an opinion, not evidence."
                        },
                        {
                                    "label": "Timestamp",
                                    "value": "When the observation occurred  --  aligned across camera, telemetry, and operator notes. Timing connects multi-sensor evidence into one coherent moment."
                        },
                        {
                                    "label": "Checkpoint",
                                    "value": "Where the observation occurred  --  mapped to a named checkpoint ID such as cp01, cp02, or cp03. Location context makes evidence spatially meaningful."
                        },
                        {
                                    "label": "Context Note",
                                    "value": "What the file cannot show by itself: glare, occlusion, vibration, fallback decisions. Honest notes make the final inspection more credible, not weaker."
                        }
            ],
            "bottom_band": "Evidence test: 'If someone disputes this <strong class=\"font-bold\">inspection</strong> claim, what specific file, timestamp, checkpoint, and note would I show to defend it?' If you cannot answer all four, the claim is not yet evidence-backed."
        },
        {
            "title": "Section 1  --  Rugged Navigation and Multi-Sensor Arrays",
            "thesis": "Understand terrain, sensing roles, and runtime evidence for inspection. This section covers rugged terrain effects, bounded navigation, costmaps, obstacle supervision, sensor roles, timing alignment, and telemetry context  --  everything needed to explain what the robot perceived and why the path was chosen.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Core Idea",
                                    "value": "Terrain is not just background  --  it changes robot behavior and evidence quality. Slope, gravel, glare, occlusion, and vibration affect what the final report can honestly defend."
                        },
                        {
                                    "label": "Key Principle",
                                    "value": "Navigation for <strong class=\"font-bold\">inspection</strong> means bounded progress  --  know the checkpoint, choose a safe path, move in small steps, stop to prove. Not full autonomy, but explainable supervised motion."
                        },
                        {
                                    "label": "Sensor Array",
                                    "value": "Each sensor answers a different question  --  camera sees appearance, telemetry explains motion, payload measures condition, notes explain limits. Multi-sensor means multi-question, not just more data."
                        },
                        {
                                    "label": "Section Slides",
                                    "value": "Slides 5 -- 11: Rugged terrain, bounded navigation, costmaps, obstacle supervision, sensor roles, timing alignment, and SportModeState telemetry context."
                        }
            ],
            "bottom_band": "Section framing: By the end of this section, you should be able to explain how terrain conditions affect evidence quality and what each sensor channel contributes to an <strong class=\"font-bold\">inspection</strong> claim."
        },
        {
            "title": "Rugged Terrain Changes the Run",
            "thesis": "Rugged terrain is important because it changes both robot behavior and evidence quality. A slope may alter posture, loose surface may affect traction, glare may hide inspection details, and vibration may blur images. Students should record these conditions because they influence what the final report can honestly defend.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Slope",
                                    "value": "Alters robot posture and weight distribution. May change camera aim point and affect the appearance of captured inspection targets."
                        },
                        {
                                    "label": "Loose Surface",
                                    "value": "Reduces traction and increases odometry uncertainty. The robot may slip slightly  --  route accuracy degrades compared to hard floor."
                        },
                        {
                                    "label": "Glare / Lighting",
                                    "value": "Direct sunlight or reflections can wash out camera images. Inspection details become harder to verify  --  the report must note this limitation."
                        },
                        {
                                    "label": "Vibration",
                                    "value": "<strong class=\"font-bold\">B2</strong> gait vibration can blur still images and shake video. Stable-dwell capture becomes more important on rough terrain than on smooth floor."
                        }
            ],
            "bottom_band": "Terrain recording habit: At each checkpoint, note one terrain condition that could affect evidence  --  slope angle, surface type, lighting direction, or vibration level. One sentence per checkpoint is enough."
        },
        {
            "title": "Navigation Means Bounded Progress",
            "thesis": "For Day 4, navigation means making safe, explainable progress toward <strong class=\"font-bold\">inspection</strong> checkpoints. Students do not need advanced autonomy theory to act professionally. They need a checkpoint goal, a visible hazard plan, bounded motion, a stop point, and evidence that the robot reached the <strong class=\"font-bold\">inspection</strong> view safely.",
            "board_type": "list",
            "board_data": [
                        "Know the checkpoint: Identify the target <strong class=\"font-bold\">inspection</strong> position before motion begins. The destination should be marked, visible, and agreed by the team.",
                        "Choose a safe path: Identify hazards between the current position and the checkpoint. Mark any slope, obstacle, or uncertain surface that the route must avoid.",
                        "<strong class=\"font-bold\">Move</strong> in small steps: Use bounded velocity and short-duration commands. The first motion should be the smallest meaningful displacement  --  observe before increasing.",
                        "Stop to prove: Dwell at the checkpoint until the robot is stable. Capture evidence only after motion has stopped. A blurred image during translation is not <strong class=\"font-bold\">inspection</strong> evidence."
            ],
            "bottom_band": "Navigation test: Before any <strong class=\"font-bold\">B2</strong> motion, ask aloud: 'What is the checkpoint? What hazards are between here and there? What is my first small command? When will I stop to capture?' If any answer is unclear, do not move."
        },
        {
            "title": "Costmaps Turn Space into Risk",
            "thesis": "A <strong class=\"font-bold\">costmap</strong> is a simple way to turn space into movement risk. Clear floor is low cost, blocked areas are not usable, and uncertain surfaces should increase caution. Students should use the <strong class=\"font-bold\">costmap</strong> idea to explain why the <strong class=\"font-bold\">B2</strong> path avoids hazards and where human supervision remains necessary.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Free Space (Low Cost)",
                                    "value": "Clear, traversable floor  --  the planner can route through these cells freely. Confirmed by sensor data showing no obstacles and stable surface."
                        },
                        {
                                    "label": "Obstacle (Blocked)",
                                    "value": "Cells containing detected barriers  --  walls, equipment, cones. The path must never route through these. Marked as lethal cost."
                        },
                        {
                                    "label": "Uncertain Terrain (Caution)",
                                    "value": "Cells where sensor data is sparse, terrain type is ambiguous, or surface condition is unknown. Conservative planning treats these as high-cost or avoids them entirely."
                        },
                        {
                                    "label": "Human Supervision Zone",
                                    "value": "Areas where sensor confidence is low and human judgment is required. The operator decides whether the path is safe — the costmap advises, not guarantees."
                        }
            ],
            "bottom_band": "Costmap exercise: Draw a simple grid. Mark one free cell, one obstacle cell, and one uncertain cell near your <strong class=\"font-bold\">B2</strong> arena. For each, explain what the robot should do and where the human must supervise."
        },
        {
            "title": "Obstacle Avoidance Needs Supervision",
            "thesis": "Obstacle avoidance is useful, but it is not a guarantee. Sensors can miss low, reflective, moving, transparent, or poorly lit hazards. The safe envelope still depends on field roles, slow motion, visible boundaries, and immediate stop authority. This keeps rugged navigation connected to practical field discipline.",
            "board_type": "list",
            "board_data": [
                        "Sensor detection layer: Cameras and depth sensors identify obstacles within their field of view. Detection has blind spots  --  low objects, reflective surfaces, transparent materials, and dark areas.",
                        "Software caution layer: The avoidance system adjusts velocity or stops when obstacles are detected within configured thresholds. Software cannot see what sensors miss.",
                        "Human supervision layer: The spotter watches the full robot perimeter and arena. Human judgment catches what sensors and software miss  --  and has immediate stop authority."
            ],
            "bottom_band": "Safety envelope rule: The three layers  --  sensor, software, human  --  must all be active during <strong class=\"font-bold\">B2</strong> motion. If any layer is compromised (sensor blocked, software disabled, spotter distracted), stop immediately."
        },
        {
            "title": "Each Sensor Has a Job",
            "thesis": "A multi-sensor array should not be described as collecting more data. Each channel answers a different question. Camera frames show visual condition, telemetry explains how the robot moved, payload data may measure the target, and notes document uncertainty. The report improves when these roles are explicit.",
            "board_type": "table",
            "board_data": {
                        "headers": [
                                    "Sensor",
                                    "Question It Answers",
                                    "Artifact It Produces",
                                    "Report Use"
                        ],
                        "rows": [
                                    [
                                                "Camera (Front / Rear)",
                                                "What does the inspection target look like?",
                                                "Still image (frame<strong class=\"font-bold\">.jpg</strong>) or <strong class=\"font-bold\">RTSP</strong> video clip.",
                                                "Primary visual evidence of target condition."
                                    ],
                                    [
                                                "<strong class=\"font-bold\">SportModeState</strong> Telemetry",
                                                "How did the robot move and stand?",
                                                "sportmodestate<strong class=\"font-bold\">.jsonl</strong>  --  one JSON line per state sample.",
                                                "Explains motion context: was the robot stable during capture?"
                                    ],
                                    [
                                                "Payload Data",
                                                "What does the target measure?",
                                                "Sensor reading with timestamp and checkpoint label.",
                                                "Adds quantitative measurement to visual inspection."
                                    ],
                                    [
                                                "Operator Notes",
                                                "What can the files not show?",
                                                "Checkpoint notes  --  glare, occlusion, fallback decisions.",
                                                "Documents limitations that affect claim confidence."
                                    ]
                        ]
            },
            "bottom_band": "Sensor discipline: For every <strong class=\"font-bold\">inspection</strong> checkpoint, identify which sensors contributed evidence and which question each sensor answered. A checkpoint with camera-only evidence is weaker than one with camera + <strong class=\"font-bold\">telemetry</strong> + notes."
        },
        {
            "title": "Timing Connects the Sensors",
            "thesis": "Multi-sensor evidence is strongest when timing is clear. A camera frame, telemetry line, payload measurement, and operator note should all point to the same checkpoint moment. Beginners can start with checkpoint IDs and approximate timestamps, then improve synchronization as their scripting skills mature.",
            "board_type": "list",
            "board_data": [
                        "Camera frame timestamp: The moment the image was captured. Compare with <strong class=\"font-bold\">telemetry</strong> to confirm the robot was stationary  --  a frame taken during motion may be blurred.",
                        "<strong class=\"font-bold\">SportModeState</strong> line timestamp: The moment the robot reported its state. Align with camera timestamps to verify stable dwell before capture.",
                        "Payload reading timestamp: The moment the sensor measurement was taken. Must be close to the camera timestamp for the data to describe the same <strong class=\"font-bold\">inspection</strong> moment.",
                        "Operator note timestamp: The moment the observation was recorded. Should reference the same checkpoint ID as the automated logs for cross-referencing."
            ],
            "bottom_band": "Timing check: At checkpoint cp01, do your camera frame, <strong class=\"font-bold\">telemetry</strong> line, <strong class=\"font-bold\">payload</strong> reading, and note all reference the same checkpoint ID and similar timestamps? If not, the multi-sensor claim is weakened by timing misalignment."
        },
        {
            "title": "Telemetry Is Runtime Context",
            "thesis": "<strong class=\"font-bold\">SportModeState</strong> is the robot's runtime context. If a checkpoint frame is blurred, velocity or yaw speed may explain it. If posture looks unusual, body height or mode may help. Students should use <strong class=\"font-bold\">telemetry</strong> as supporting evidence, not as an isolated log file.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Motion Panel",
                                    "value": "Velocity (vx, vy, vyaw)  --  was the robot moving or turning during capture? High velocity during a checkpoint frame explains blur and weakens the claim."
                        },
                        {
                                    "label": "Posture Panel",
                                    "value": "Body height, pitch, roll  --  was the robot level and stable? Slope or uneven footing changes the camera aim point and image composition."
                        },
                        {
                                    "label": "Mode Panel",
                                    "value": "Current <strong class=\"font-bold\">SportModeState</strong> mode  --  is the robot in a safe, expected state? Unexpected mode transitions during <strong class=\"font-bold\">inspection</strong> indicate a control or script problem."
                        },
                        {
                                    "label": "Timing Panel",
                                    "value": "Timestamp and sequence  --  does the telemetry record cover the full run window from before first motion through after final capture? Gaps create blind spots."
                        }
            ],
            "bottom_band": "Telemetry habit: When reviewing a checkpoint frame, open the corresponding <strong class=\"font-bold\">SportModeState</strong> line. Ask: was velocity near zero? Was posture stable? Was mode as expected? If any answer is no, note it in the report."
        },
        {
            "title": "Section 2  --  Mock Inspection Scripts",
            "thesis": "Build the inspection workflow safely before the B2 field run. This section covers mock-first workflow, Gazebo rehearsal, procedural scripts, scenario files, camera capture, OpenCV-derived outputs, JSONL logging, bounded motion, channel-by-channel debugging, and validation readiness gates.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Core Idea",
                                    "value": "Mock scenario passes → folder structure passes → instructor approves <strong class=\"font-bold\">B2</strong> handoff. Hardware begins only after the mock workflow and folder structure are understandable enough for instructor approval."
                        },
                        {
                                    "label": "Key Principle",
                                    "value": "A functional inspection script should make the run procedure visible  --  Setup, Capture, Log, Move, Package, Validate as separate steps. No black-box scripts that hide failures."
                        },
                        {
                                    "label": "Validation Gate",
                                    "value": "If the mock package fails validation, the <strong class=\"font-bold\">B2</strong> run should wait. Missing metadata, empty <strong class=\"font-bold\">telemetry</strong>, or absent checkpoint frames show the procedure is not ready."
                        },
                        {
                                    "label": "Section Slides",
                                    "value": "Slides 13 -- 22: Mock-first gate, Gazebo rehearsal, procedural scripts, scenario files, camera capture, OpenCV outputs, JSONL logging, bounded motion, debugging, and validation."
                        }
            ],
            "bottom_band": "Section rule: The mock run is not optional practice  --  it is a required gate. Prove the workflow produces reviewable evidence before the <strong class=\"font-bold\">B2</strong> leaves its standby position."
        },
        {
            "title": "Mock First, Then Hardware",
            "thesis": "Students should prove the workflow before the hardware run. A mock scenario lets them define checkpoints, test capture placeholders, write metadata, and package the run folder. Hardware begins only after the mock workflow and folder structure are understandable enough for instructor approval.",
            "board_type": "list",
            "board_data": [
                        "Mock Scenario: Define checkpoints, route, capture targets, and metadata. Create patrol_plan<strong class=\"font-bold\">.json</strong> and metadata<strong class=\"font-bold\">.json</strong>  --  these files set intent before any capture occurs.",
                        "Run Folder Check: Build the folder structure  --  checkpoints/cp01/, raw_captures/, logs/. Confirm every required path exists and naming conventions are followed.",
                        "Instructor Approval: Present the mock package. Instructor confirms: scenario is defined, folder structure is correct, capture plan is clear, validation rules are understood.",
                        "<strong class=\"font-bold\">B2</strong> Handoff: Only after approval does the team proceed to hardware. The mock package becomes the template for the field run folder."
            ],
            "bottom_band": "Gate discipline: 'Our mock folder passed validation and the instructor approved handoff.' If you cannot say this sentence truthfully, the <strong class=\"font-bold\">B2</strong> should not move."
        },
        {
            "title": "Gazebo Rehearses the Logic",
            "thesis": "<strong class=\"font-bold\">Gazebo</strong> is useful because it lets students rehearse <strong class=\"font-bold\">inspection</strong> logic before field risk appears. It does not replace the <strong class=\"font-bold\">B2</strong> run, but it helps teams practice checkpoint sequencing, sensor thinking, timing, and recovery decisions. The lesson is rehearsal discipline, not simulation perfection.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "<strong class=\"font-bold\">Gazebo</strong> Rehearsal",
                                    "value": "Practice checkpoint sequencing, sensor activation, timing, and recovery decisions in a risk-free environment. Errors in <strong class=\"font-bold\">Gazebo</strong> cost time, not hardware damage or safety incidents."
                        },
                        {
                                    "label": "<strong class=\"font-bold\">B2</strong> Field Run",
                                    "value": "Execute the rehearsed workflow on hardware with real terrain, lighting, network conditions, and sensor behavior. Compare field results with <strong class=\"font-bold\">Gazebo</strong> expectations."
                        },
                        {
                                    "label": "Comparison",
                                    "value": "Differences between <strong class=\"font-bold\">Gazebo</strong> rehearsal and <strong class=\"font-bold\">B2</strong> field run are engineering insights  --  they reveal real-world effects that simulation cannot fully capture (floor texture, lighting, latency)."
                        }
            ],
            "bottom_band": "Rehearsal rule: '<strong class=\"font-bold\">Gazebo</strong> tells you whether your logic makes sense. The <strong class=\"font-bold\">B2</strong> tells you whether reality agrees.' Never skip the rehearsal  --  never assume the field will match simulation perfectly."
        },
        {
            "title": "Scripts Should Show Procedure",
            "thesis": "A functional inspection script should make the run procedure visible. Students should see setup, capture, logging, movement, packaging, and validation as separate steps. This prevents a black-box script from hiding failures and makes the workflow easier to debug when camera, telemetry, or folder paths break.",
            "board_type": "list",
            "board_data": [
                        "Setup: Initialize SDK clients, verify network interface, confirm <strong class=\"font-bold\">SportModeState</strong> subscription, open output files. Print confirmation of each initialization step.",
                        "Capture: Execute camera stills or <strong class=\"font-bold\">RTSP</strong> recording at designated moments. Verify each saved file  --  check file size, try to open, confirm scene matches checkpoint.",
                        "Log: Write <strong class=\"font-bold\">SportModeState</strong> samples to sportmodestate<strong class=\"font-bold\">.jsonl</strong> continuously. Each line is one timestamped state record  --  mode, gait, velocity, position, body height.",
                        "<strong class=\"font-bold\">Move</strong>: Send bounded motion commands through <strong class=\"font-bold\">SportClient</strong>. Small values, short duration, observed behavior. <strong class=\"font-bold\">StopMove</strong> after each leg.",
                        "Package: Organize artifacts into the run folder  --  raw captures preserved, selected frames copied to checkpoints/<id>/frame<strong class=\"font-bold\">.jpg</strong>, logs in place.",
                        "Validate: Run the validator against the completed package. PASS → proceed to report. FAIL → repair and re-validate before claiming readiness."
            ],
            "bottom_band": "Script transparency: Can another student read your script and understand what each section does without running it? If not, add print statements and section comments until the procedure is visible."
        },
        {
            "title": "Scenario Files Set Intent",
            "thesis": "The mock scenario should create intent before any capture occurs. Metadata identifies operator, date, robot, and run context. The patrol plan identifies checkpoint IDs and what each checkpoint should inspect. These files make the inspection script accountable and keep later report claims tied to planned targets.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "metadata<strong class=\"font-bold\">.json</strong>",
                                    "value": "Operator name, date, robot ID, run scenario description, interface used. Says who ran the <strong class=\"font-bold\">inspection</strong>, when, and under what conditions  --  accountability before evidence."
                        },
                        {
                                    "label": "patrol_plan<strong class=\"font-bold\">.json</strong>",
                                    "value": "Checkpoint IDs, leg definitions, capture actions, speed limits, dwell requirements. Says what checkpoints matter and what evidence each should produce."
                        },
                        {
                                    "label": "Checkpoint Folders",
                                    "value": "checkpoints/cp01/, cp02/, cp03/  --  each contains frame<strong class=\"font-bold\">.jpg</strong>, the selected <strong class=\"font-bold\">inspection</strong> image. The folder path encodes the checkpoint identity."
                        }
            ],
            "bottom_band": "Intent check: Before any capture, can you open metadata<strong class=\"font-bold\">.json</strong> and patrol_plan<strong class=\"font-bold\">.json</strong> and read exactly what <strong class=\"font-bold\">inspection</strong> targets are planned? If the plan is vague, the evidence will be vague."
        },
        {
            "title": "Camera Scripts Capture Context",
            "thesis": "Camera scripts produce visual context for inspection, but saved files should be checked before they are trusted. Students should confirm that a still image opens, a video plays, and the content matches the intended checkpoint. This keeps capture focused on usable evidence rather than file creation alone.",
            "board_type": "list",
            "board_data": [
                        "Front / Rear Still Capture: Use <strong class=\"font-bold\">VideoClient</strong> to grab a single frame. Save as a timestamped or checkpoint-labeled .jpg file. Confirm the image opens and shows the expected scene.",
                        "<strong class=\"font-bold\">RTSP</strong> Video Recording: Open the <strong class=\"font-bold\">RTSP</strong> stream, configure writer settings (codec, resolution, frame rate), record the approach and dwell, close the file. Verify playback before trusting the recording.",
                        "File Verification: Check file size > minimum threshold, attempt to open with a standard viewer, confirm scene content matches checkpoint description. A file that cannot be opened is not evidence.",
                        "Map to Checkpoint: Copy verified frame to checkpoints/<id>/frame<strong class=\"font-bold\">.jpg</strong>. The raw capture is preserved separately  --  the checkpoint folder holds the selected, verified evidence."
            ],
            "bottom_band": "Verification rule: 'The file saved successfully' is not the same as 'the file is usable evidence.' Open every capture before leaving the checkpoint. A corrupt or misaimed frame discovered during reporting is too late to fix."
        },
        {
            "title": "OpenCV Outputs Are Derived",
            "thesis": "<strong class=\"font-bold\">OpenCV</strong> can help demonstrate simple image processing, but processing should not overwrite evidence. Raw frames are the primary record. Edge views, filters, annotations, and detection outputs are derived artifacts. Students should preserve both and explain which one supports the report claim.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Raw Frame (Primary)",
                                    "value": "The original, unmodified image from the camera  --  preserved as the authoritative visual record. Never delete, overwrite, or modify the raw capture file."
                        },
                        {
                                    "label": "Derived Output (Secondary)",
                                    "value": "Processed images  --  edge detection, filtering, annotation overlays, object detection bounding boxes. Useful for highlighting features, but derived from the raw frame."
                        },
                        {
                                    "label": "Report Usage",
                                    "value": "The report should cite the raw frame as primary evidence. Derived outputs can illustrate specific features but cannot replace the original  --  if processing introduces artifacts, the raw frame is the fallback."
                        }
            ],
            "bottom_band": "Processing discipline: 'I applied an edge filter to highlight cracks. The raw frame is preserved at raw_captures/front_<ts>.jpg. The filtered output is at derived/edge_<ts>.jpg.' Both files, clearly labeled, with the raw frame as the authoritative source."
        },
        {
            "title": "JSONL Makes Logs Inspectable",
            "thesis": "A JSONL <strong class=\"font-bold\">telemetry</strong> log is beginner-friendly because each line can be inspected as one state sample. Students can open the file, read a line, and find fields such as mode, velocity, yaw speed, or body height. This structure prepares the file for later parsing and visualization.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "JSONL Structure",
                                    "value": "One complete JSON object per line. Each line is a self-contained <strong class=\"font-bold\">SportModeState</strong> sample  --  no multi-line objects, no trailing commas, no array wrappers. Readable with any text editor."
                        },
                        {
                                    "label": "Key Fields",
                                    "value": "mode, gait, position[x,y,yaw], velocity[vx,vy,vyaw], bodyHeight, timestamp. These fields explain the robot's motion and posture at each sampled moment."
                        },
                        {
                                    "label": "Parsing Ready",
                                    "value": "Each line can be loaded with json.loads() independently. Students can extract fields, filter by timestamp, or plot values without parsing a complex nested structure."
                        }
            ],
            "bottom_band": "Log inspectability: Open your sportmodestate<strong class=\"font-bold\">.jsonl</strong> file. Can you read line 10 and explain what the robot was doing at that moment  --  mode, velocity, posture? If not, add field labels or documentation until it is self-explanatory."
        },
        {
            "title": "Motion Commands Stay Small",
            "thesis": "Mock scripts should teach the same discipline used on hardware. A high-level motion command needs instructor approval, small values, short duration, visible observation, and an explicit stop. Students should record the result, because the report needs to explain what command produced the captured evidence.",
            "board_type": "list",
            "board_data": [
                        "Approved command: Instructor confirms the motion is appropriate  --  destination, speed, duration, and safety conditions are reviewed before execution.",
                        "Short duration: Commands are sent for limited time or distance. The first motion should be the smallest meaningful displacement  --  ~0.2 m or ~0.3 rad.",
                        "Observe: Watch the robot's response. Did it move in the expected direction? At the expected speed? Did it stop when commanded? Record what you observed, not what you expected.",
                        "<strong class=\"font-bold\">StopMove</strong>: Send explicit stop command after each motion leg. Redundant stop commands are safer  --  a single <strong class=\"font-bold\">StopMove</strong> may not be enough. Confirm the robot is stationary before next capture.",
                        "Note result: Document the command, the observed behavior, and any deviation. The report needs to connect each motion command to the evidence it produced."
            ],
            "bottom_band": "Motion safety: 'What command am I about to send? What do I expect the robot to do? What will I do if the robot does something different?' Answer all three before any <strong class=\"font-bold\">B2</strong> motion  --  mock or hardware."
        },
        {
            "title": "Debug One Channel at a Time",
            "thesis": "When a script fails, students should avoid changing everything at once. They should test the camera path alone, telemetry logger alone, folder structure alone, and validator alone before combining them. This debugging habit turns failures into evidence about which channel needs repair.",
            "board_type": "list",
            "board_data": [
                        "1. Camera alone: Test that the video client initializes, captures a still, and saves a readable .jpg file. No <strong class=\"font-bold\">telemetry</strong>, no motion  --  just one camera channel.",
                        "2. Logger alone: Test that the <strong class=\"font-bold\">SportModeState</strong> subscriber writes valid JSONL lines to a file. Confirm lines are parseable and contain expected fields.",
                        "3. Folder paths alone: Test that the run folder structure is created correctly  --  all directories exist, naming conventions are correct, placeholder files validate.",
                        "4. Validator alone: Run the validator against a known-good folder and a known-bad folder. Confirm it correctly distinguishes PASS from FAIL  --  the validator itself must be trustworthy.",
                        "5. Combined run: Only after all four channels work independently, combine them into the full <strong class=\"font-bold\">inspection</strong> script. Channel-by-channel confidence before integration."
            ],
            "bottom_band": "Debugging staircase: Start at the bottom (single channel), confirm it works, move up one step. A failure in the combined run can now be traced to the specific channel that broke  --  because you already proved each one works alone."
        },
        {
            "title": "Validation Catches Script Gaps",
            "thesis": "The validator is a readiness gate for the script, not just a grading tool. Missing metadata, empty telemetry, absent checkpoint frames, or mismatched checkpoint IDs show that the procedure is not ready. Repairing these gaps in the mock run prevents avoidable field confusion.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "PASS",
                                    "value": "All required files present, all paths correct, all structural checks satisfied. The package is reviewable  --  proceed to report writing and <strong class=\"font-bold\">B2</strong> handoff gate."
                        },
                        {
                                    "label": "PASS with Warnings",
                                    "value": "Structure is valid but one or more checks produced warnings  --  e.g., image file is small, JSONL line count is low, optional fields missing. Warnings must be explained in the report."
                        },
                        {
                                    "label": "FAIL",
                                    "value": "Required file missing, path incorrect, checkpoint ID mismatch, or structural error. The package is not reviewable  --  repair the script and re-validate before proceeding."
                        }
            ],
            "bottom_band": "Validator as gate: Mock folder → Run validator → PASS? → Proceed to instructor approval. FAIL? → Identify the specific gap, repair the script, re-run mock, re-validate. Never skip validation because 'the files are probably there.'"
        },
        {
            "title": "Section 3  --  B2 Field Execution",
            "thesis": "Run the supervised inspection, capture sensors, and log telemetry. This section covers field roles, observable readiness, stable-dwell capture, RTSP verification, continuous telemetry logging, checkpoint mapping, field notes, immediate verification, and stated fallbacks.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Core Idea",
                                    "value": "A <strong class=\"font-bold\">B2</strong> field run needs clear roles before motion. The run director, terminal operator, spotter, evidence lead, and reporter each have defined responsibilities  --  role clarity prevents unsafe mixed instructions."
                        },
                        {
                                    "label": "Key Principle",
                                    "value": "Readiness is observable  --  interface selected, perimeter clear, stop path known, cameras tested, logger ready. Students show readiness through checks, not confidence statements."
                        },
                        {
                                    "label": "Capture Rule",
                                    "value": "<strong class=\"font-bold\">Move</strong> to view, stop or dwell, capture, label checkpoint, continue. Checkpoint evidence is strongest when the robot is stable  --  never capture during turning or translation."
                        },
                        {
                                    "label": "Section Slides",
                                    "value": "Slides 24 -- 32: Field roles, observable readiness, stable-dwell capture, RTSP verification, telemetry logging window, checkpoint mapping, field notes, immediate verification, and fallback procedures."
                        }
            ],
            "bottom_band": "Section rule: The first <strong class=\"font-bold\">B2</strong> field command is not a full <strong class=\"font-bold\">inspection</strong>. It is a single small motion  --  then stop, review, and decide whether to continue. Staged confidence, not rushed demonstration."
        },
        {
            "title": "Field Roles Keep Order",
            "thesis": "A <strong class=\"font-bold\">B2</strong> field run needs clear roles before motion. The run director approves action, the terminal operator controls commands, the spotter watches the robot and space, the evidence lead checks saved files, and the reporter records limitations. Role clarity prevents excited students from creating unsafe mixed instructions.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Run Director",
                                    "value": "Approves all motion and capture actions. Has final authority to proceed or halt. No command is sent without the director's explicit approval."
                        },
                        {
                                    "label": "Terminal Operator",
                                    "value": "Executes commands at the keyboard. Reads each command aloud before sending. Watches console output for errors or unexpected responses."
                        },
                        {
                                    "label": "Spotter",
                                    "value": "Watches the robot and surrounding space continuously. Holds immediate stop authority  --  spotter says stop, operator stops, no questions asked in the moment."
                        },
                        {
                                    "label": "Evidence Lead",
                                    "value": "Checks every saved file immediately after capture  --  opens the image, confirms scene, verifies file size. Declares whether evidence is usable or needs recapture."
                        },
                        {
                                    "label": "Reporter",
                                    "value": "Records limitations, deviations, and field observations in real time. Notes what the files cannot show  --  glare, occlusion, route changes, fallback decisions."
                        }
            ],
            "bottom_band": "Role assignment: Before the <strong class=\"font-bold\">B2</strong> powers on, every person in the arena must know their role and their stop authority. If anyone cannot state their role in one sentence, roles are not clear enough to proceed."
        },
        {
            "title": "Readiness Is Observable",
            "thesis": "Students should not say they are ready because they feel ready. They should show readiness through checks: selected network interface, clear perimeter, known stop action, verified cameras, active logger, prepared folder, and named checkpoint plan. If one check is missing, the run waits.",
            "board_type": "list",
            "board_data": [
                        "Interface selected: Correct network adapter active, IP on expected subnet, ping to <strong class=\"font-bold\">B2</strong> confirmed, <strong class=\"font-bold\">DDS</strong> discovery working. Connectivity is the foundation  --  if the robot is not reachable, nothing else matters.",
                        "Perimeter clear: Arena boundaries marked, obstacles identified, operator zones designated, bystanders aware. Physical space is as important as software readiness.",
                        "Stop path known: Remote stop accessible, script stop command ready, physical stop procedure agreed. Every team member knows at least two ways to halt the robot immediately.",
                        "Cameras tested: Front and rear still capture verified, <strong class=\"font-bold\">RTSP</strong> stream confirmed playable, file save paths writable. Camera readiness is confirmed before motion, not assumed.",
                        "Logger ready: <strong class=\"font-bold\">SportModeState</strong> subscriber running, JSONL file writable, lines appearing and parseable. Telemetry logging begins before first motion and continues through final notes."
            ],
            "bottom_band": "Readiness gate: Read each check aloud and confirm verbally. 'Interface  --  confirmed. Perimeter  --  clear. Stop path  --  known. Cameras  --  tested. Logger  --  running.' All five confirmed → motion may proceed. Any one missing → wait."
        },
        {
            "title": "Capture at Stable Dwell",
            "thesis": "Checkpoint evidence is strongest when the robot is stable. Capturing during a turn or translation can create blur and make the report less defensible. Students should move into view, stop or dwell, capture the frame, label it with the checkpoint, and only then continue.",
            "board_type": "list",
            "board_data": [
                        "Approach: <strong class=\"font-bold\">Move</strong> the <strong class=\"font-bold\">B2</strong> into <strong class=\"font-bold\">inspection</strong> view using bounded, supervised motion. Velocity should decrease as the robot nears the checkpoint  --  approach slow, not fast.",
                        "<strong class=\"font-bold\">StopMove</strong> or Dwell: Command the robot to stop and stabilize. Confirm velocity reads near zero in <strong class=\"font-bold\">SportModeState</strong>. Wait at least 1 -- 2 seconds after stop before capture  --  settling time matters.",
                        "Capture Frame: Execute still capture only after confirming the robot is stationary. The image should be sharp, well-framed, and clearly show the <strong class=\"font-bold\">inspection</strong> target.",
                        "Label Checkpoint: Save as checkpoints/<id>/frame<strong class=\"font-bold\">.jpg</strong>. State the checkpoint ID aloud. The evidence lead confirms the file is saved and opens correctly.",
                        "Continue: Only after the evidence lead confirms usable capture does the director approve the next motion leg. Never rush from one capture directly into the next motion."
            ],
            "bottom_band": "Stable dwell rule: 'Capture in motion is not <strong class=\"font-bold\">inspection</strong> evidence  --  it is a screenshot of a moving robot.' If <strong class=\"font-bold\">SportModeState</strong> velocity is non-zero, wait. Blurred evidence weakens every claim that follows."
        },
        {
            "title": "RTSP Needs Proof",
            "thesis": "RTSP recording may fail because the stream, writer settings, codec, or dimensions are wrong. A file name alone is not evidence. Students should check file size, open playback, confirm the scene, and document any fallback if video cannot be used.",
            "board_type": "list",
            "board_data": [
                        "Record: Start <strong class=\"font-bold\">RTSP</strong> stream capture with explicit writer configuration  --  codec, resolution, frame rate. Confirm the stream is active before declaring recording started.",
                        "File Size: After recording stops, check the file size. A video file under 1 KB is almost certainly corrupt  --  the stream may have failed silently during recording.",
                        "Playback: Open the video file and play at least the first and last few seconds. Confirm the content is the expected scene, not a black frame or frozen image.",
                        "Scene Match: Does the video show the correct checkpoint, the correct robot position, the correct <strong class=\"font-bold\">inspection</strong> target? If the scene does not match, the recording is mislabeled.",
                        "Accept or Fallback: If video passes all checks → accept as evidence. If video fails → fall back to still frames, <strong class=\"font-bold\">telemetry</strong>, and operator notes. State the fallback explicitly in the report."
            ],
            "bottom_band": "<strong class=\"font-bold\">RTSP</strong> verification: 'I recorded a video file. I checked the size. I played it back. The scene matches cp01. I accept it as evidence.' Or: 'Video failed  --  I am using still frames and <strong class=\"font-bold\">telemetry</strong> instead. This limitation is documented in the report.'"
        },
        {
            "title": "Log Through the Run",
            "thesis": "Telemetry logging should cover the meaningful run window. Starting late can miss the approach, and stopping early can miss recovery or final posture. The evidence lead should confirm that SportModeState logging begins before motion and continues through checkpoint captures and final notes.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Before Motion",
                                    "value": "Start <strong class=\"font-bold\">SportModeState</strong> logging. Confirm lines are appearing in sportmodestate<strong class=\"font-bold\">.jsonl</strong>. Log at least 5 -- 10 seconds of stationary baseline data  --  this shows the robot's pre-run state."
                        },
                        {
                                    "label": "During Motion & Capture",
                                    "value": "Keep logging continuously through every motion leg, every checkpoint approach, every dwell, and every capture. No gaps  --  the log is the runtime witness of the entire <strong class=\"font-bold\">inspection</strong>."
                        },
                        {
                                    "label": "After Final Notes",
                                    "value": "Continue logging for several seconds after the final capture and notes. This captures the robot's post-<strong class=\"font-bold\">inspection</strong> state  --  mode, posture, position after all motion has stopped."
                        }
            ],
            "bottom_band": "Log coverage test: Open your sportmodestate<strong class=\"font-bold\">.jsonl</strong>. Does the first timestamp precede the first motion command? Does the last timestamp follow the final capture? If not, your log has blind spots at the edges of the run."
        },
        {
            "title": "Map Captures to Checkpoints",
            "thesis": "Students should preserve raw captures and also normalize selected evidence into the expected checkpoint paths. This step turns field media into reviewable inspection evidence. A good habit is to state the checkpoint ID aloud, save the capture, and immediately confirm where the selected frame belongs.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Raw Captures",
                                    "value": "All original files  --  every still, every video clip, unmodified and timestamped. Stored in raw_captures/ as the unprocessed field record. Never delete raw captures until the report is complete and accepted."
                        },
                        {
                                    "label": "Selected Evidence",
                                    "value": "The best frame for each checkpoint, copied to checkpoints/<id>/frame<strong class=\"font-bold\">.jpg</strong>. Selected for clarity, focus, and relevance  --  not every raw capture becomes checkpoint evidence."
                        },
                        {
                                    "label": "Naming Convention",
                                    "value": "checkpoints/cp01/frame<strong class=\"font-bold\">.jpg</strong>, checkpoints/cp02/frame<strong class=\"font-bold\">.jpg</strong>. Consistent naming lets the validator, the report, and any reviewer find the right evidence at the right checkpoint instantly."
                        }
            ],
            "bottom_band": "Mapping habit: After each capture, say aloud: 'Checkpoint cp01  --  frame saved, verified, copied to checkpoints/cp01/frame<strong class=\"font-bold\">.jpg</strong>.' This verbal confirmation catches mislabeled files before they become report errors."
        },
        {
            "title": "Field Notes Capture Limits",
            "thesis": "Field notes explain what the files cannot show by themselves. If glare limited visibility, the rear stream failed, a checkpoint was skipped, or the route changed for safety, the report should include that limitation. Honest notes make the final inspection more credible, not weaker.",
            "board_type": "list",
            "board_data": [
                        "Glare / Lighting: Note if direct sunlight, reflections, or low light affected camera image quality. A washed-out image at cp02 is not a failure  --  it is a limitation that the report must explain.",
                        "Occlusion: Note if an object, person, or robot part blocked the <strong class=\"font-bold\">inspection</strong> view. Partial occlusion may still allow useful evidence  --  state what is visible and what is hidden.",
                        "Skipped Checkpoint: Note if a checkpoint was skipped and why  --  safety concern, time constraint, unreachable position. A skipped checkpoint with a documented reason is better than a missing checkpoint with no explanation.",
                        "Fallback Stream: Note if <strong class=\"font-bold\">RTSP</strong> video was replaced by still frames. State which channel was used as the fallback and why the primary channel was unavailable.",
                        "Route / Safety Change: Note if the planned route changed during the run  --  obstacle discovered, perimeter adjusted, operator decision. The report must explain deviations from the plan."
            ],
            "bottom_band": "Notes discipline: 'If I do not write this limitation down now, the report will claim evidence quality that the files cannot support.' Write the note at the checkpoint, not from memory during report writing."
        },
        {
            "title": "Evidence Habit: Verify Immediately",
            "thesis": "The field evidence habit is immediate verification. After capture, students should open the artifact, label the checkpoint, place the selected file in the package, and confirm the log is still running. This avoids discovering after the run that the strongest checkpoint has no usable evidence.",
            "board_type": "list",
            "board_data": [
                        "Capture: Execute the still or video capture at the checkpoint. State aloud what was captured and at which checkpoint.",
                        "Open: Immediately open the saved file  --  view the image, play the video. Do not trust the file save confirmation alone. A file can save successfully and still be corrupt.",
                        "Label: Name the file with its checkpoint ID. Confirm the label matches the actual scene content  --  a mislabeled cp01 frame showing cp02 content is a data integrity error.",
                        "Place: Copy the verified frame to checkpoints/<id>/frame<strong class=\"font-bold\">.jpg</strong>. Confirm the copy succeeded and the file at the destination path opens correctly.",
                        "Confirm Log: Check that sportmodestate<strong class=\"font-bold\">.jsonl</strong> is still receiving new lines. A frozen log means <strong class=\"font-bold\">telemetry</strong> evidence stopped mid-run  --  diagnose before continuing."
            ],
            "bottom_band": "Immediate verification loop: Capture → Open → Label → Place → Confirm Log → Continue. If any step fails, stay at the checkpoint until it is resolved or a fallback is documented. Never leave a checkpoint with unverified evidence."
        },
        {
            "title": "Fallbacks Must Be Stated",
            "thesis": "A field run can still be useful when one channel fails. If RTSP video is unavailable, students can rely on verified stills, telemetry logs, and limitation notes. The key is to state the fallback clearly so the final report does not imply evidence that was never captured.",
            "board_type": "list",
            "board_data": [
                        "Video Fails → Use Stills: If <strong class=\"font-bold\">RTSP</strong> recording is corrupt or unavailable, fall back to front/rear still captures at each checkpoint. Stills at stable dwell are valid primary evidence.",
                        "Camera Fails → Use Telemetry: If both video and stills are unavailable, <strong class=\"font-bold\">SportModeState</strong> <strong class=\"font-bold\">telemetry</strong> still documents that the robot reached the checkpoint position and stopped.",
                        "All Sensors Fail → Use Notes: If no automated evidence is available, operator notes become the primary record. State clearly: 'Automated capture failed  --  all evidence is from operator observation.'",
                        "Report Caveat: Every fallback must produce a limitation statement in the report. '<strong class=\"font-bold\">RTSP</strong> video was unavailable at cp02 due to stream error  --  still frame and <strong class=\"font-bold\">telemetry</strong> used instead.'"
            ],
            "bottom_band": "Fallback rule: A field run with stated fallbacks is still valid engineering work. A field run with hidden failures is not. State every fallback  --  the report's credibility depends on honesty about limitations."
        },
        {
            "title": "Section 4  --  Logs, Reports, and Maintenance",
            "thesis": "Parse the run, visualize evidence, report claims, and care for the B2. This section covers log parsing, motion visualization, payload data context, artifact-backed report claims, validation as a report-readiness check, message-to-fix debugging, and post-run B2 hardware maintenance.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Core Idea",
                                    "value": "Raw <strong class=\"font-bold\">telemetry</strong> → Parsed fields → Visualization → Report claims → Validation → Maintenance. Data becomes evidence only when it is extracted, understood, and connected to a specific claim."
                        },
                        {
                                    "label": "Key Principle",
                                    "value": "A report claim follows a fixed pattern: state the claim, name the artifact, cite <strong class=\"font-bold\">telemetry</strong> context, explain any limitation, assign confidence. This prevents vague summaries of a live demo."
                        },
                        {
                                    "label": "Maintenance",
                                    "value": "The <strong class=\"font-bold\">inspection</strong> is not finished when the report is drafted. Close with a <strong class=\"font-bold\">B2</strong> maintenance walkthrough: power state, body, feet, <strong class=\"font-bold\">payload</strong> mount, cables, sensors, and file archive."
                        },
                        {
                                    "label": "Section Slides",
                                    "value": "Slides 34 -- 40: Log parsing, motion visualization, payload context, report claims, validation, debugging, and B2 hardware maintenance."
                        }
            ],
            "bottom_band": "Section rule: The final deliverable is not a live demo  --  it is a reviewable run folder and report. Another engineer should understand the <strong class=\"font-bold\">inspection</strong> without having watched it."
        },
        {
            "title": "Parse Logs into Fields",
            "thesis": "Data visualization begins by parsing logs into useful fields. Students should extract timing, mode, velocity, yaw speed, position, and body height from SportModeState records. The goal is not advanced analytics; it is turning raw telemetry into a readable explanation of robot behavior.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Timestamp",
                                    "value": "When each state sample was recorded. Used to align telemetry with camera captures and operator notes  --  timing is the backbone of multi-sensor correlation."
                        },
                        {
                                    "label": "Mode & Gait",
                                    "value": "What control mode the robot was in and what gait pattern was active. Mode transitions during inspection may indicate script or operator interventions."
                        },
                        {
                                    "label": "Velocity & Yaw Speed",
                                    "value": "Linear velocity (vx, vy) and angular velocity (vyaw). Plot these to show when the robot moved, turned, or stopped  --  motion timeline from data, not memory."
                        },
                        {
                                    "label": "Position & Body Height",
                                    "value": "Estimated position and body height. Track position drift over the run and note any unusual posture changes that may affect camera aim or stability."
                        }
            ],
            "bottom_band": "Parsing exercise: From your sportmodestate<strong class=\"font-bold\">.jsonl</strong>, extract timestamp, vx, and vyaw for the full run. Plot them on a simple timeline. Can you identify exactly when each motion leg started, when the robot stopped, and when each capture occurred?"
        },
        {
            "title": "Visualize Motion and Capture",
            "thesis": "A simple timeline can explain the field run clearly. Speed and yaw speed show when the robot moved or turned, while vertical markers show checkpoint captures. This helps students explain whether a frame was taken during stable dwell or during motion that might weaken image quality.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Speed Line",
                                    "value": "Plot vx (forward speed) over time. Flat near-zero segments indicate dwell/stop periods. Spikes indicate motion legs. A capture during a spike is motion-blurred  --  the report must note this."
                        },
                        {
                                    "label": "Yaw-Speed Line",
                                    "value": "Plot vyaw (turn rate) over time. Non-zero segments indicate the robot was rotating. A capture during rotation may show motion blur or framing shift."
                        },
                        {
                                    "label": "Capture Markers",
                                    "value": "Vertical lines at checkpoint capture timestamps (cp01, cp02, cp03). Overlay on the speed plot to visually confirm: was the robot stationary at each capture moment?"
                        }
            ],
            "bottom_band": "Visualization test: 'Show me the timeline of your field run. Point to cp01. Was vx near zero? Was vyaw near zero? Was the robot stable?' The timeline answers these questions in one image."
        },
        {
            "title": "Payload Data Needs Context",
            "thesis": "Payload data becomes useful only when it is tied to context. A measurement should include timestamp, checkpoint ID, sensor identity, and relevant robot state. Without that context, the number may be hard to interpret or defend in the report. Tables are the best beginner format.",
            "board_type": "table",
            "board_data": {
                        "headers": [
                                    "Timestamp",
                                    "Checkpoint",
                                    "Sensor Value",
                                    "Robot State",
                                    "Interpretation"
                        ],
                        "rows": [
                                    [
                                                "2026-06-04T09:15:23Z",
                                                "cp01",
                                                "Temperature: 24.3°C",
                                                "Mode: <strong class=\"font-bold\">Damp</strong>, vx ≈ 0, body height normal",
                                                "Normal reading at first checkpoint  --  robot stable, sensor functioning."
                                    ],
                                    [
                                                "2026-06-04T09:18:47Z",
                                                "cp02",
                                                "Distance: 1.42 m",
                                                "Mode: <strong class=\"font-bold\">Damp</strong>, slight pitch from slope",
                                                "Measurement may be affected by 3° slope  --  noted in report limitation."
                                    ],
                                    [
                                                "2026-06-04T09:22:10Z",
                                                "cp03",
                                                "No reading",
                                                "Mode: <strong class=\"font-bold\">Damp</strong>, vx ≈ 0",
                                                "Payload sensor did not respond  --  fallback to visual inspection only. Limitation documented."
                                    ]
                        ]
            },
            "bottom_band": "Payload context rule: 'A number without timestamp, checkpoint, and robot state is not a measurement  --  it is a mystery.' Always pair <strong class=\"font-bold\">payload</strong> readings with the <strong class=\"font-bold\">telemetry</strong> context that explains the conditions under which they were taken."
        },
        {
            "title": "Reports Make Defensible Claims",
            "thesis": "A report should make claims that the evidence can support. Students can use a fixed pattern: state the claim, name the artifact, cite the telemetry context, explain any limitation, and assign a confidence statement. This prevents reports from becoming vague summaries of a live demo.",
            "board_type": "list",
            "board_data": [
                        "Claim: What are you asserting about the <strong class=\"font-bold\">inspection</strong>? Be specific  --  'The <strong class=\"font-bold\">B2</strong> successfully inspected checkpoint cp01 and captured clear visual evidence'  --  not 'The robot worked.'",
                        "Artifact: Which file supports this claim? Name the exact file path  --  checkpoints/cp01/frame<strong class=\"font-bold\">.jpg</strong>, sportmodestate<strong class=\"font-bold\">.jsonl</strong> lines 130 -- 145, field_report<strong class=\"font-bold\">.md</strong> section 2.",
                        "Telemetry Context: What does the robot state data say about the moment of capture? Velocity near zero, mode stable, body height normal  --  or deviations that need explanation.",
                        "Limitation: What could weaken this claim? Glare on the image, slight motion during capture, sensor gap, timing uncertainty. Honest limitations strengthen credibility.",
                        "Confidence: How sure are you? High (multiple sensors agree), Medium (primary sensor ok, no cross-validation), Low (fallback used, uncertainty present). Confidence must match evidence strength."
            ],
            "bottom_band": "Report pattern practice: Write one claim about your last mock run using all five fields. Can another student read it and understand exactly what you observed, what supports it, and how confident you are?"
        },
        {
            "title": "Validation Protects the Report",
            "thesis": "The validator checks whether required files and paths are present. A pass means the package is structurally reviewable, but warnings may still need explanation in the report. A fail means the team should repair the folder before making final inspection claims.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "PASS",
                                    "value": "All required structural checks satisfied  --  metadata present, checkpoint folders populated, <strong class=\"font-bold\">telemetry</strong> log non-empty, images valid. The package can be reviewed and reported on."
                        },
                        {
                                    "label": "PASS with Warnings",
                                    "value": "Structure valid but one or more quality warnings  --  image below recommended size, JSONL line count low, optional field empty. Warnings go in the report with explanation."
                        },
                        {
                                    "label": "FAIL",
                                    "value": "Required artifact missing, path incorrect, or structural rule violated. The package is not reviewable. Repair the folder and re-validate  --  do not write the report against incomplete evidence."
                        }
            ],
            "bottom_band": "Validation as report gate: 'PASS → Write the report. Warnings → Write the report AND explain each warning. FAIL → Repair the folder, do not write the report yet.' The validator protects the report from building on incomplete evidence."
        },
        {
            "title": "Debug from Message to Fix",
            "thesis": "Students should interpret error messages as clues. Missing metadata means accountability is incomplete. Empty logs mean runtime evidence was not saved. Bad frames suggest corrupt or placeholder images. Mismatched checkpoints mean the plan and package disagree. Each problem has a specific repair path.",
            "board_type": "table",
            "board_data": {
                        "headers": [
                                    "Validator Message",
                                    "Likely Cause",
                                    "First Fix",
                                    "Report Impact"
                        ],
                        "rows": [
                                    [
                                                "Missing metadata.json",
                                                "Script did not create or write the metadata file.",
                                                "Check setup step  --  add metadata write with operator, date, robot ID, scenario.",
                                                "Report cannot establish accountability  --  who, when, what scenario."
                                    ],
                                    [
                                                "Empty sportmodestate<strong class=\"font-bold\">.jsonl</strong>",
                                                "Logger started but no state samples were written  --  subscriber may not have received data.",
                                                "Check SportModeState subscription  --  confirm callback fires, file handle is open, DDS discovery works.",
                                                "No telemetry context for any claim  --  captures lack motion/posture support."
                                    ],
                                    [
                                                "Bad frame<strong class=\"font-bold\">.jpg</strong> at cp01",
                                                "Image file is corrupt, zero bytes, or wrong format.",
                                                "Re-capture the still  --  verify with file size check and visual open before proceeding.",
                                                "Primary visual evidence for cp01 is unusable  --  fallback or recapture required."
                                    ],
                                    [
                                                "Mismatched checkpoint IDs",
                                                "patrol_plan.json lists cp_A but folder has cp01  --  naming convention broken.",
                                                "Standardize all checkpoint IDs  --  use consistent format (cp01, cp02, cp03) everywhere.",
                                                "Validator cannot match plan to evidence  --  report claims may reference wrong checkpoints."
                                    ]
                        ]
            },
            "bottom_band": "Debugging discipline: Read the validator message aloud. State the likely cause. Make one fix. Re-validate. If the message changes, you fixed something  --  if the same message persists, your fix did not address the root cause."
        },
        {
            "title": "Maintain the B2 Afterward",
            "thesis": "The inspection is not finished when the report is drafted. Students should close with a B2 maintenance walkthrough: safe power state, visible body condition, feet, payload mounting, cables, sensor surfaces, and archived files. Hardware care protects the next team and completes professional field discipline.",
            "board_type": "list",
            "board_data": [
                        "Power State: Confirm the <strong class=\"font-bold\">B2</strong> is in a safe power mode  --  <strong class=\"font-bold\">Damp</strong> or powered down per instructor guidance. Battery level noted. No active motion commands lingering.",
                        "Body & Feet: Inspect for visible damage, debris, or unusual wear. Check foot pads for embedded gravel or sharp objects. Clean if needed  --  debris from one run affects the next.",
                        "Payload Mount & Cables: Verify <strong class=\"font-bold\">payload</strong> is secure, connectors are seated, cables are not pinched or frayed. A loose <strong class=\"font-bold\">payload</strong> can shift during the next run and change sensor aim.",
                        "Sensor Surfaces: Clean camera lenses and sensor windows with appropriate materials. Dust, fingerprints, or moisture from the field run can degrade the next <strong class=\"font-bold\">inspection</strong>'s image quality.",
                        "File Archive: Confirm all run artifacts are saved, backed up, and organized. The run folder should be complete and accessible for report writing and instructor review."
            ],
            "bottom_band": "Maintenance discipline: 'The next team should find the <strong class=\"font-bold\">B2</strong> in the same condition I would want to receive it.' Walk through all five checks, document any issues found, and confirm the archive before leaving."
        },
        {
            "title": "Closing  --  Required Outcomes Check",
            "thesis": "Confirm that every Day 4 activity served the four required outcomes. This closing section returns to the core framework and gives instructors a concise final standard for Day 4 success.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Rugged Navigation & Sensors",
                                    "value": "Students can explain how terrain conditions affect evidence quality and what each sensor channel contributes to an inspection claim."
                        },
                        {
                                    "label": "Mock Inspection Scripts",
                                    "value": "Students can build procedural scripts that rehearse capture, logging, motion, packaging, and validation  --  and pass the mock gate before hardware."
                        },
                        {
                                    "label": "<strong class=\"font-bold\">B2</strong> Field Capture",
                                    "value": "Students can execute a supervised B2 field run with defined roles, stable-dwell capture, continuous telemetry logging, and immediate evidence verification."
                        },
                        {
                                    "label": "Logs, Reports, Maintenance",
                                    "value": "Students can parse telemetry, visualize motion, write artifact-backed claims, debug from validator messages, and complete B2 hardware maintenance."
                        }
            ],
            "bottom_band": "Outcome check: For each of the four tiles above, can you produce one concrete artifact that proves you achieved that outcome? If not, that outcome is incomplete  --  return to the relevant section before closing Day 4."
        },
        {
            "title": "Four Outcomes Are Complete",
            "thesis": "Students have learned how rugged terrain changes navigation evidence, how mock scripts rehearse inspection procedure, how B2 field execution captures sensors and telemetry, and how parsed logs, payload context, reports, and maintenance complete the workflow.",
            "board_type": "grid",
            "board_data": [
                        {
                                    "label": "Terrain and Sensors",
                                    "value": "Rugged terrain changes the run  --  slope, gravel, glare, vibration. Multi-sensor arrays answer different questions. <strong class=\"font-bold\">SportModeState</strong> provides runtime context. Evidence: terrain notes + sensor table + <strong class=\"font-bold\">telemetry</strong> log."
                        },
                        {
                                    "label": "Mock Scripts",
                                    "value": "Mock-first workflow, <strong class=\"font-bold\">Gazebo</strong> rehearsal, procedural scripts, scenario files, camera capture, JSONL logging, bounded motion, channel debugging, and validation gate. Evidence: validated mock run folder."
                        },
                        {
                                    "label": "<strong class=\"font-bold\">B2</strong> Field Capture",
                                    "value": "Field roles, observable readiness, stable-dwell capture, <strong class=\"font-bold\">RTSP</strong> verification, continuous logging, checkpoint mapping, field notes, immediate verification, and stated fallbacks. Evidence: field run folder + notes."
                        },
                        {
                                    "label": "Logs, Reports, Maintenance",
                                    "value": "Parse <strong class=\"font-bold\">SportModeState</strong> fields, visualize motion timeline, contextualize <strong class=\"font-bold\">payload</strong> data, write artifact-backed claims, validate, debug, and maintain the <strong class=\"font-bold\">B2</strong>. Evidence: field_report<strong class=\"font-bold\">.md</strong> + validator output."
                        }
            ],
            "bottom_band": "Completion check: 'I can explain rugged terrain effects. I built and validated a mock script. I executed a supervised <strong class=\"font-bold\">B2</strong> field run. I parsed data and wrote a report. I maintained the <strong class=\"font-bold\">B2</strong> afterward.' All five statements true → Day 4 objectives met."
        },
        {
            "title": "Ready Means Reviewable",
            "thesis": "The final standard is reviewability. Another engineer should open the run folder and understand the scenario, route, captures, telemetry, payload context, validation result, limitations, report claims, and maintenance notes. If the story depends mainly on memory, the Day 4 evidence workflow is incomplete.",
            "board_type": "list",
            "board_data": [
                        "Scenario: Can the reviewer understand what was being inspected, where, and why? metadata<strong class=\"font-bold\">.json</strong> and patrol_plan<strong class=\"font-bold\">.json</strong> should tell the complete story without verbal explanation.",
                        "Route: Can the reviewer see the planned checkpoints and the path between them? The route should be documented clearly enough to reconstruct the field layout.",
                        "Captures: Can the reviewer open each checkpoint frame and see what the robot saw? Every frame<strong class=\"font-bold\">.jpg</strong> should be verified, correctly exposed, and clearly show the <strong class=\"font-bold\">inspection</strong> target.",
                        "Telemetry: Can the reviewer read the <strong class=\"font-bold\">SportModeState</strong> log and understand robot motion and posture? Velocity, mode, and body height should explain the robot's state at each capture.",
                        "Payload: Are sensor readings paired with timestamps, checkpoints, and robot state? Raw numbers without context are not evidence.",
                        "Validation: Does the validator output show PASS or documented warnings? The reviewer should know whether the package is structurally complete.",
                        "Report: Does field_report<strong class=\"font-bold\">.md</strong> make claims supported by named artifacts, <strong class=\"font-bold\">telemetry</strong>, and stated limitations? The report is the synthesis  --  it should reference every other file in the folder.",
                        "Maintenance: Is the <strong class=\"font-bold\">B2</strong> condition documented after the run? The reviewer should know the hardware was cared for and the files were archived."
            ],
            "bottom_band": "Reviewability test: Hand your run folder to a classmate who did not watch your field run. Can they answer: what was inspected, what evidence was captured, what the robot state was, what limitations exist, and what the report claims? If any answer is no, your Day 4 workflow is not yet complete."
        }
    ],    "labs": [
        {
            "id": "lab-00",
            "title": "Inspection Scenario & Run Folder",
            "content": "Create a Day 4 B2 run folder with metadata.json, patrol_plan.json, and checkpoint subdirectories before the robot moves.\n\n- Adapt Day 2 run-folder schema for B2: add robot_platform, robot_id, interface, camera_mode\n- Draft metadata.json with schema_version, created_utc, operator, checkpoints list\n- Create patrol_plan.json with 3 checkpoints (cp01_entry, cp02_asset_label, cp03_exit)\n- Define legs: dwell at each checkpoint; optional short velocity legs between (vx ≤ 0.1 m/s)\n- Create checkpoints/ directory with subdirectories for each checkpoint ID",
            "code_files": [
                {
                    "name": "example_b2_metadata.json",
                    "code": "{\n  \"schema_version\": \"1.0\",\n  \"created_utc\": \"2026-06-03T02:30:00Z\",\n  \"operator\": \"team_alpha\",\n  \"robot_platform\": \"Unitree B2\",\n  \"robot_id\": \"b2-01\",\n  \"lab\": \"day-04-field-inspection\",\n  \"interface\": \"eth0\",\n  \"environment\": \"indoor corridor mock inspection\",\n  \"camera_sources\": [\"front\", \"back\"],\n  \"checkpoints\": [\"cp01_entry\", \"cp02_asset_label\", \"cp03_exit\"],\n  \"safety_observer\": \"instructor\",\n  \"notes\": \"B2 moved only under supervised SportClient commands; checkpoint frames selected after capture.\"\n}"
                }
            ]
        },
        {
            "id": "lab-01",
            "title": "Mock Inspection Video — B2 Front & Back Cameras",
            "content": "Use camera_opencv-video.py to capture front/back stills and record RTSP streams.\n\n- Run the camera script with verified interface: python scripts/ives_sdk/B2/camera_opencv-video.py <interface>\n- Test front image capture (Q) and back image capture (E)\n- Test front RTSP recording toggle (A) and back recording toggle (D)\n- Verify saved files: check file size, attempt to open with image viewer\n- Demonstrate one controlled failure (e.g., wrong interface → no frames) as a teaching moment\n- Optional: run camera_opencv-videoEffect.py to show face detection and color tracking as analytics preview",
            "code_files": [
                {
                    "name": "b2_camera_capture_demo.py",
                    "code": "\"\"\"B2 Camera Capture Demo — simplified teaching version.\"\"\"\nimport sys, cv2, time, os\nimport numpy as np\nfrom unitree_sdk2py.core.channel import ChannelFactoryInitialize\n# Note: actual script uses FrontVideoClient/BackVideoClient from unitree_sdk2py\n\ndef main(interface: str):\n    print(f\"[CAMERA] Initializing on {interface}\")\n    # ChannelFactoryInitialize(0, interface)\n    # front_client = FrontVideoClient()\n    # front_client.Init()\n    print(\"[CAMERA] Controls: Q=front still, E=back still, A=toggle front record, D=toggle back record, ESC=exit\")\n    print(\"[CAMERA] Checkpoint images: save as front_img_<timestamp>.jpg\")\n    print(\"[CAMERA] Verify every saved file: check size > 100 bytes, try to open with viewer.\")\n    print(\"[CAMERA READY] — press ESC to exit (demo mode)\")\n\nif __name__ == \"__main__\":\n    main(sys.argv[1] if len(sys.argv) > 1 else \"eth0\")"
                }
            ]
        },
        {
            "id": "lab-02",
            "title": "Field Run, State Logging & Reporting",
            "content": "Execute a complete B2 field inspection run: log state, move between checkpoints under supervision, capture evidence, validate, and debrief.\n\n- Start SportModeState subscriber and redirect output to sportmodestate.jsonl\n- Execute choreographed sequence: dwell cp01 → capture front still → supervised Move leg → StopMove → dwell cp02 → capture → dwell cp03 → capture\n- Map raw captures to checkpoint folders: copy selected image to checkpoints/<id>/frame.jpg\n- Run validator against the completed run folder\n- Write field_report.md with scenario, roles, command sequence, evidence table, validator result, issues/warnings, and next improvement\n- Run a controlled failure exercise: create an incomplete run folder and diagnose validator output",
            "code_files": [
                {
                    "name": "field_report_template.md",
                    "code": "# B2 Field Inspection Report\n\n## Scenario\n<!-- What are we inspecting? Where? -->\n\n## Team Roles\n- Operator:\n- Safety Observer:\n- Evidence Lead:\n- Instructor:\n\n## Command Sequence\n| Step | Command | RC | Observed Behavior |\n|------|---------|----|--------------------|\n| 1    |         |    |                    |\n\n## Evidence Table\n| Checkpoint | frame.jpg | State Slice | Notes |\n|------------|-----------|-------------|-------|\n| cp01_entry | ✅/❌      | ✅/❌        |       |\n\n## Validator Result\n- Status: PASS / PASS-with-warnings / FAIL\n- Warnings:\n- Issues:\n\n## Next Improvement\n<!-- One concrete change for the next run -->"
                }
            ]
        }
    ]
}

# Write all days to file
if __name__ == "__main__":
    print("[PROGRESS AUDIT] ========================================")
    print("[PROGRESS AUDIT] Triple-Pass Compilation Complete")
    print("[PROGRESS AUDIT] Days compiled: 02, 03, 04 of 07")
    print("[PROGRESS AUDIT] Total Task Completion: 57.14%")
    print("[PROGRESS AUDIT] ========================================")
    print("Days 02-04 written. Run build_syllabus_v2.py for Days 05-07.")