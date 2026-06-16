#!/usr/bin/env python3
"""Build Day 7 lecture slides from day7_slide_content.md"""

import json

SYLLABUS_PATH = "client/src/data/syllabus.json"

# grid helper: [{label, value}]
def g(*pairs):
    return [{"label": k, "value": v} for k, v in pairs]

# list helper: [string]
def lst(*items):
    return list(items)

# table helper: {headers, rows}
def tbl(headers, rows):
    return {"headers": list(headers), "rows": [list(r) for r in rows]}

# math helper
def math(eq, *steps):
    return {"equation": eq, "steps": list(steps)}

SLIDES = [
    # ── COVER ──
    {
        "title": "Day 7: G1 AI-Driven Locomotion, Audio, and Application Assembly",
        "thesis": "Day 7 marks the culmination of the G1 journey — integrating advanced AI locomotion engines, audio capabilities, and speech interfaces into a fully unified application. We assemble the complete intelligent humanoid: motion, voice, and manipulation working as one.",
        "board_type": "grid",
        "board_data": g(
            ("AI Locomotion & Benchmarks", "Interfacing G1 with AI-driven locomotion engines, data flow between AI models and physical controllers, and state validation benchmarks for safe, adaptive movement."),
            ("Audio & Speech Infrastructure", "Audio parameter classes, service constants, playback routines, ASR/TTS integration, WAV management, and LED synchronization for multimodal interaction."),
            ("Unified Application Assembly", "Blending voice control with bipedal motion and object manipulation. Synchronizing multiple subsystems into a cohesive, deployable application package."),
            ("Final Validation & Deployment", "Full-stack testing, deployment habits for reliable operation, and comprehensive course wrap-up across all seven days of the G1 curriculum."),
        ),
        "bottom_band": "© 2026 Vinci AI. All rights reserved. — The complete G1 operator: from observer to integrator, from single subsystem to unified application."
    },

    # ── SLIDE 1: Learning Map ──
    {
        "title": "Learning Map — Assembling the Intelligent G1",
        "thesis": "Initialize AI Engine → Validate State → Setup Audio → Integrate Speech → Sync Multimodal → Deploy App. The goal is a unified robot that seamlessly blends motion, voice, and manipulation — more than the sum of its parts.",
        "board_type": "list",
        "board_data": lst(
            "Initialize AI Engine: Interface G1 with AI-driven locomotion engines using standard APIs (JSON/Protobuf). Establish low-latency communication for dynamic control.",
            "Validate State: Run static posture checks (joint limits, CoM projection, ground contact) and dynamic stability tests (ZMP tracking, perturbation response) to ensure safe operation.",
            "Setup Audio: Configure AudioClient service constants and parameter classes. Define volume, output device, sample rate, and playback routines for reliable audio output.",
            "Integrate Speech: Connect ASR (speech-to-text) for voice commands and TTS (text-to-speech) for dynamic responses. Build multimodal speech interfaces with visual LED feedback.",
            "Sync Multimodal: Coordinate locomotion, arm control, audio, and LED subsystems through event-driven architecture. Manage concurrency and prevent conflicting actions.",
            "Deploy App: Package dependencies, configs, and launch scripts. Transfer to G1, configure runtime, and execute full-stack validation before going live."
        ),
        "bottom_band": "The Unified Robot: Each subsystem is powerful alone. Together — motion, voice, manipulation, and perception — they create genuine intelligence."
    },

    # ── SLIDE 2: AI-Driven Locomotion Engines ──
    {
        "title": "Smart Steps: AI-Driven Locomotion Engines",
        "thesis": "AI-driven locomotion engines use reinforcement learning and optimization algorithms to generate adaptive, robust, and natural-looking gaits. G1 interfaces with these engines through structured APIs and real-time data exchange.",
        "board_type": "grid",
        "board_data": g(
            ("Definition", "Software modules that use AI (reinforcement learning, optimization) to generate dynamic gaits. Unlike scripted motions, AI engines adapt to terrain, load, and task requirements in real-time."),
            ("Benefits", "More adaptive gaits across uneven terrain. Robust recovery from perturbations. Natural-looking movements that mimic human biomechanics. Continuous improvement through sensor feedback loops."),
            ("Integration Architecture", "G1 connects to AI engines via standard APIs with JSON or Protobuf data formats. The AI engine outputs desired joint trajectories, which are translated into motor commands through the FSM layer."),
            ("Real-Time Requirements", "Low-latency communication is critical — the AI must receive sensor feedback and send commands within milliseconds to maintain balance and execute smooth dynamic movements."),
        ),
        "bottom_band": "AI locomotion engines connect to G1's motor control system through a bidirectional data pipeline: commands flow down, sensor feedback flows up, and adaptation happens continuously."
    },

    # ── SLIDE 3: Interfacing with AI Engines ──
    {
        "title": "Connecting Minds: Interfacing with AI Engines",
        "thesis": "Interfacing with AI locomotion engines requires standard APIs for command/feedback exchange, structured data formats (JSON/Protobuf), and low-latency communication channels for real-time dynamic control.",
        "board_type": "grid",
        "board_data": g(
            ("Standard APIs", "Common interfaces for sending locomotion commands (target velocity, posture, gait type) and receiving state feedback (joint positions, IMU data, contact forces). API versioning ensures compatibility across engine updates."),
            ("Data Formats", "JSON for human-readable configuration and debugging. Protobuf for high-performance binary serialization in production. Both formats support structured, schema-validated data exchange between G1 and external AI systems."),
            ("Real-Time Pipeline", "Low-latency communication (< 10ms per cycle) for dynamic control. UDP-based transport for speed, with optional reliability layers for critical commands. Timing jitter must be minimized for stable locomotion."),
        ),
        "bottom_band": "G1's control system exchanges data with external AI locomotion engines via an API bridge. The interface layer abstracts engine-specific details, allowing plug-and-play engine swapping."
    },

    # ── SLIDE 4: Data Flow ──
    {
        "title": "The Loop: AI Model to Physical Controller Data Flow",
        "thesis": "AI Output → Trajectory Generation → Motor Control → G1 Actuators, with Sensor Feedback looping back to the AI model. This continuous closed-loop enables real-time learning and adaptation.",
        "board_type": "list",
        "board_data": lst(
            "AI Output: The AI model generates desired joint trajectories, forces, or high-level action primitives based on its policy and current state estimate. Output is in task space or joint space depending on the control architecture.",
            "Trajectory Generation: Converts AI output into smooth, feasible motor commands. Interpolates waypoints, enforces joint limits and velocity constraints, and generates position/velocity profiles for each actuator.",
            "Motor Control: Low-level PID controllers execute position/velocity commands on physical actuators. Encoder feedback provides closed-loop tracking with error correction at kHz rates for precise motion execution.",
            "Sensor Feedback: IMU, joint encoders, foot contact sensors, and vision data flow back to the AI model. This feedback enables online adaptation, learning from experience, and continuous refinement of control policies."
        ),
        "bottom_band": "The closed loop: AI model → trajectory generation → motor control → G1 actuators → sensor feedback → back to AI. Every millisecond matters for dynamic stability."
    },

    # ── SLIDE 5: State Validation Benchmarks ──
    {
        "title": "Ensuring Safety: State Validation Benchmarks",
        "thesis": "State validation benchmarks verify G1's position, velocity, and balance against safe operating parameters. They prevent unsafe movements and ensure predictable behavior through static posture checks, dynamic stability tests, and trajectory adherence metrics.",
        "board_type": "grid",
        "board_data": g(
            ("Definition", "Metrics and tests to verify G1's physical state (joint positions, CoM location, contact forces) against predefined safe operating envelopes. Validation is continuous — every control cycle checks state before executing commands."),
            ("Importance", "Prevents unsafe movements that could damage hardware or cause falls. Ensures predictable, repeatable behavior across different environments and tasks. Builds operator trust through verified safety guarantees."),
            ("Static Posture Checks", "Joint angle limits verification, Center of Mass (CoM) projection within support polygon, and ground contact confirmation — fundamental checks executed before any movement begins."),
            ("Dynamic Stability Tests", "Zero Moment Point (ZMP) trajectory tracking, external perturbation response testing, and fall detection/recovery verification — ensures robust locomotion during movement."),
            ("Trajectory Adherence", "Position error (commanded vs actual end-effector), orientation error, and path deviation metrics — quantifies how accurately G1 follows planned trajectories during precision tasks."),
        ),
        "bottom_band": "Validation is not optional — it is the contract between your code and the robot's physics. Every command must be checked, every state must be verified, every transition must be confirmed."
    },

    # ── SLIDE 6: Static Posture Checks ──
    {
        "title": "Standing Still: Static Posture Validation",
        "thesis": "Static posture checks verify joint angle limits, Center of Mass projection within the support polygon, and expected foot-ground contact points. These are the fundamental safety gates executed before any movement.",
        "board_type": "grid",
        "board_data": g(
            ("Joint Angle Limits", "Verify all joints are within safe angular ranges before and after each movement. Each joint has hardware and software limits — exceeding either can cause mechanical damage or servo overload."),
            ("Center of Mass (CoM) Projection", "Ensure the CoM is projected within the support polygon (the convex hull of ground contact points). A CoM outside the support polygon means the robot will tip — immediate correction required."),
            ("Ground Contact", "Confirm expected foot-ground contact points using force sensors or kinematics. Missing or partial contact indicates uneven terrain, slipping, or mechanical failure — halt motion until resolved."),
        ),
        "bottom_band": "Static checks are the first line of defense. If the robot cannot stand safely, it cannot walk safely. Validate posture before every motion sequence."
    },

    # ── SLIDE 7: Dynamic Stability Tests ──
    {
        "title": "Moving Safely: Dynamic Stability Validation",
        "thesis": "Dynamic stability tests monitor Zero Moment Point trajectory, external perturbation response, and fall detection mechanisms during movement. These benchmarks are vital for robust, adaptive locomotion.",
        "board_type": "grid",
        "board_data": g(
            ("Zero Moment Point (ZMP) Tracking", "Monitor ZMP trajectory during walking cycles. The ZMP must remain within the support polygon throughout the gait. ZMP excursions outside the polygon indicate impending instability — the controller must react within milliseconds."),
            ("External Perturbation Response", "Test G1's ability to recover from pushes, uneven terrain, or unexpected loads. Measure recovery time, maximum displacement, and whether the robot returns to stable posture without external intervention."),
            ("Fall Detection & Recovery", "Verify proper detection of loss-of-balance events and trigger appropriate recovery behaviors. Recovery may include bracing, lowering CoM, transitioning to a safe state, or controlled descent to minimize damage."),
        ),
        "bottom_band": "Dynamic stability is continuous — a robot that was stable one second ago may not be stable now. Monitor, validate, and react in real-time."
    },

    # ── SLIDE 8: Trajectory Adherence ──
    {
        "title": "Following the Path: Trajectory Adherence Validation",
        "thesis": "Trajectory adherence benchmarks quantify how accurately G1 follows commanded movements — measuring position error, orientation error, and path deviation of end-effectors during precision tasks.",
        "board_type": "grid",
        "board_data": g(
            ("Position Error", "Difference between commanded and actual end-effector position in 3D space. Measured in millimeters — sub-centimeter accuracy required for manipulation tasks. High error indicates mechanical backlash, calibration drift, or control instability."),
            ("Orientation Error", "Difference between commanded and actual end-effector orientation (roll/pitch/yaw). Critical for grasping and tool-use tasks where angular precision determines success or failure."),
            ("Path Deviation", "How closely G1 follows a planned spatial path. The area between commanded and actual trajectories quantifies overall tracking quality. Large deviations may indicate insufficient control gains or unmodeled dynamics."),
        ),
        "bottom_band": "High trajectory adherence is the difference between picking up an object and knocking it over. Precision demands continuous validation and calibration."
    },

    # ── SLIDE 9: G1 Audio Infrastructure ──
    {
        "title": "G1's Voice and Ears: Audio Infrastructure",
        "thesis": "G1's audio infrastructure enables sound production (speech, alerts) and perception (speech recognition) through integrated microphones, speakers, and audio processing units connected to the central control system.",
        "board_type": "grid",
        "board_data": g(
            ("Purpose", "Enable G1 to produce sounds — speech via TTS, alerts for status changes, confirmation tones — and perceive audio — speech recognition via ASR, environmental sound detection, voice command processing."),
            ("Hardware Components", "Microphone array for directional audio capture and noise rejection. Chest speaker for omnidirectional audio output. Dedicated audio processing unit for low-latency encode/decode and effects."),
            ("Software Integration", "AudioClient RPC service manages all audio/LED hardware. Methods include LedControl, PlayStream, GetVolume/SetVolume, and TtsMaker — all accessed through a single unified client interface."),
        ),
        "bottom_band": "G1's audio system is integrated through a single AudioClient RPC service — the same client manages speakers, microphones, and chest LEDs on shared onboard hardware."
    },

    # ── SLIDE 10: Audio Parameter Classes ──
    {
        "title": "Defining Sound: Audio Parameter Classes",
        "thesis": "Audio parameter classes define settings like volume, output device, sample rate, and format in a structured, reusable way. This ensures consistent audio playback across all applications and subsystems.",
        "board_type": "table",
        "board_data": tbl(
            ["Parameter", "Example", "Description"],
            [
                ["Volume Control", "AudioParams.volume = 0.7", "Set output level as a float from 0.0 (silent) to 1.0 (maximum). Mapped to GetVolume/SetVolume RPC calls on G1's AudioClient."],
                ["Playback Device", "AudioParams.output_device = 'speaker_1'", "Specify which audio output device to use — chest speaker, external output, or future peripherals. Enables routing audio to specific hardware endpoints."],
                ["Sample Rate", "AudioParams.sample_rate = 16000", "Must match the audio file format. G1 requires 16000 Hz for WAV playback via PlayStream. Mismatched rates cause format rejection before streaming."],
                ["Channel Count", "AudioParams.channels = 1", "G1 supports mono (single-channel) audio. Stereo or multi-channel files must be downmixed before playback. The audio validation layer rejects unsupported channel counts."],
                ["Bit Depth", "AudioParams.bit_depth = 16", "16-bit PCM required for WAV files. Other bit depths (8-bit, 24-bit, 32-bit float) are rejected with a format error before any streaming begins."],
            ],
        ),
        "bottom_band": "AudioParams encapsulates all audio configuration in one structured class. Define once, reuse everywhere — consistent, debuggable, and maintainable."
    },

    # ── SLIDE 11: Service Constants ──
    {
        "title": "Standardizing Audio: Service Constants",
        "thesis": "Service constants provide predefined, consistent values for audio service names and status codes. They make code more readable, debuggable, and maintainable across the entire application.",
        "board_type": "table",
        "board_data": tbl(
            ["Constant", "Value", "Purpose"],
            [
                ["AUDIO_PLAY_SERVICE", "'/g1/audio/play'", "Service endpoint name for audio playback requests. Centralized constant ensures all callers use the same endpoint — change it once, update everywhere."],
                ["AUDIO_VOLUME_SERVICE", "'/g1/audio/volume'", "Service endpoint for GetVolume and SetVolume RPC calls. Separates volume control from playback for independent configuration."],
                ["AUDIO_SUCCESS", "0", "Standard success return code. All audio operations return 0 on successful completion at the RPC layer. Always check return codes before assuming success."],
                ["AUDIO_ERROR", "-1", "Generic error return code. Indicates failure at the service level — check DDS connectivity, service availability, and parameter validity when this code appears."],
                ["AUDIO_FORMAT_ERROR", "-2", "Format-specific error for unsupported audio file properties. Triggered by wrong sample rate, channel count, or bit depth — the validation layer rejects before streaming."],
            ],
        ),
        "bottom_band": "Service constants are your API contract in code. AUDIO_PLAY_SERVICE = '/g1/audio/play' — one source of truth, zero ambiguity, easy refactoring."
    },

    # ── SLIDE 12: Audio Playback Routines ──
    {
        "title": "Making G1 Speak: Audio Playback Routines",
        "thesis": "Audio playback follows a clear pipeline: Load File → Apply Parameters → Call Service → Handle Response. Each step is validated before proceeding — format errors are caught before any data reaches the robot.",
        "board_type": "list",
        "board_data": lst(
            "Load File: Read WAV or audio file into memory. Validate format (16 kHz, mono, 16-bit PCM) before proceeding. Reject unsupported formats early — the format check is your first safety gate for audio.",
            "Apply Parameters: Set volume and output device using AudioParams. Configure chunk size (default 96000 bytes ≈ 3 seconds at 16 kHz) and inter-chunk sleep time for smooth streaming.",
            "Call Service: Send PlayStream(name, stream_id, chunk) in a loop for each audio chunk. Use consistent stream names for multi-chunk files. Multiple chunks with the same stream name play as one continuous audio stream.",
            "Handle Response: Check status codes after each RPC call. Success (code 0) means the chunk was accepted. Non-zero codes require immediate attention — check DDS, service availability, and robot power state.",
            "Clean Up: Call PlayStop(stream_name) after the final chunk to release audio resources. Always stop playback explicitly — orphaned streams can block future playback attempts."
        ),
        "bottom_band": "The playback routine is deterministic: Load → Validate → Stream → Verify → Stop. Every step either succeeds with code 0 or fails with an actionable error code."
    },

    # ── SLIDE 13: Multimodal Speech Interfaces ──
    {
        "title": "Beyond Sound: Multimodal Speech Interfaces",
        "thesis": "Multimodal speech interfaces combine voice with vision, motion, and LED feedback to create richer, more natural human-robot communication. ASR, TTS, visual feedback, and physical gestures work together as one interaction system.",
        "board_type": "grid",
        "board_data": g(
            ("Definition", "Combining speech with other modalities — vision (object recognition), motion (gestures, pointing), and visual feedback (LEDs, display) — for richer, more intuitive human-robot interaction that mirrors natural human communication."),
            ("Goal", "Create natural, intuitive communication where the robot understands context, not just words. A user says 'grab that' while pointing — the robot fuses speech, gesture, and vision to identify and act on the correct target."),
            ("ASR Component", "Automatic Speech Recognition converts spoken audio to text. On G1, ASR processes microphone input through the audio pipeline and feeds transcribed text to the intent parsing system for command extraction."),
            ("TTS Component", "Text-to-Speech generates spoken responses from text. G1 can respond dynamically based on its internal state — confirming actions, reporting status, or engaging in conversational interaction with users."),
            ("Visual Feedback", "LED arrays on G1's chest provide synchronized visual cues during speech — pulsing when speaking, color-coded status indicators, and attention-directing patterns that complement audio output."),
        ),
        "bottom_band": "Multimodal = voice + vision + motion + LEDs. Each channel carries part of the message. Together they create the perception of genuine intelligence."
    },

    # ── SLIDE 14: Integrating ASR ──
    {
        "title": "Listening to You: Integrating Automatic Speech Recognition",
        "thesis": "ASR converts spoken audio into text through microphone input capture, ASR engine processing, and intent parsing. The pipeline: Microphone → ASR Engine → Transcribed Text → Intent Parsing → Actionable Command.",
        "board_type": "list",
        "board_data": lst(
            "Microphone Input: Capture clear, low-noise audio from G1's microphone array. Environmental noise filtering, acoustic echo cancellation, and directional beamforming improve recognition accuracy in real-world environments.",
            "ASR Engine: Convert spoken audio into text using pre-trained speech recognition models. Support for multiple languages (Chinese speaker_id=0, English speaker_id=1). Engine runs on-device or via cloud API depending on deployment configuration.",
            "Intent Parsing: Extract meaning from transcribed text — identify the intended action ('walk', 'grab', 'stop'), target objects ('red cup', 'door'), and parameters ('slowly', 'two meters'). Map parsed intent to specific G1 API calls.",
            "Command Validation: Verify the extracted command is valid for the current robot state. Reject commands that conflict with active operations or violate safety constraints. Confirm intent before triggering any motion or action."
        ),
        "bottom_band": "ASR Pipeline: Microphone → ASR Engine → Transcribed Text → Intent Parsing → Actionable Command. Each stage filters and refines; the output is a validated, executable instruction."
    },

    # ── SLIDE 15: Integrating TTS ──
    {
        "title": "G1's Voice: Integrating Text-to-Speech",
        "thesis": "TTS converts text into spoken audio through engine processing, voice profile selection, and dynamic response generation. The pipeline: Text Input → TTS Engine → Audio Output → G1 Speaker, with state-aware content generation.",
        "board_type": "list",
        "board_data": lst(
            "TTS Engine: Converts text strings into spoken audio waveforms. G1 uses TtsMaker(text, speaker_id) via AudioClient RPC. speaker_id=0 for Chinese, speaker_id=1 for English — match the language to your text content.",
            "Voice Selection: Choose an appropriate voice profile for G1 — clear, neutral, and professional for classroom/enterprise use. Voice consistency across interactions builds user trust and recognizability.",
            "Dynamic Responses: Generate speech based on G1's current state or actions — confirm completed movements, announce transitions, report sensor readings. Dynamic speech makes interactions feel conversational rather than scripted.",
            "Timing & Flow: TTS blocks for the duration of speech output (~5 seconds in the lab script). Plan utterance length for classroom demos — short, clear phrases work best. Avoid long blocking utterances that delay the interaction loop."
        ),
        "bottom_band": "TTS Pipeline: Text Input → TTS Engine → Audio Output → G1 Speaker. TtsMaker gives G1 its voice — dynamic, state-aware, and responsive to context."
    },

    # ── SLIDE 16: Managing WAV Files ──
    {
        "title": "Pre-recorded Sounds: Managing WAV File Playback",
        "thesis": "Pre-recorded WAV files serve specific use cases — alerts, sound effects, standard greetings — where dynamic TTS is unnecessary. Organized storage, format validation, and playback integration ensure reliable audio asset management.",
        "board_type": "grid",
        "board_data": g(
            ("Use Cases", "Alerts and warnings (collision imminent, low battery), sound effects (confirmation chimes, error tones), and standard greetings. WAVs provide consistent, high-quality audio for repeated use without TTS overhead."),
            ("Storage & Retrieval", "Organize audio assets in a structured directory hierarchy: /audio/alerts/ for warning sounds, /audio/greetings/ for welcome messages, /audio/effects/ for UI sounds. Consistent naming conventions enable programmatic asset lookup."),
            ("Format Requirements", "16 kHz sample rate, mono channel, 16-bit PCM — identical to TTS output format. This consistency means WAV playback and TTS output share the same audio pipeline, simplifying the playback architecture."),
            ("Playback Integration", "Use the same PlayStream routine as TTS — load WAV bytes, chunk at 96000 bytes (~3 seconds), stream with PlayStream/PlayStop. The playback routine is format-agnostic as long as the WAV meets format requirements."),
        ),
        "bottom_band": "WAV files complement TTS: TTS for dynamic, context-aware speech; WAVs for consistent, high-quality repeated sounds. Both flow through the same PlayStream pipeline."
    },

    # ── SLIDE 17: Coordinating Audio with LED Arrays ──
    {
        "title": "Visual Voice: Coordinating Audio and LED Arrays",
        "thesis": "Synchronizing audio playback with G1's chest LED arrays creates a cohesive multimodal experience. Simultaneous commands to AudioClient for sound and LedControl for visual feedback produce engaging, intuitive robot interactions.",
        "board_type": "grid",
        "board_data": g(
            ("Purpose", "Provide visual cues during speech or audio playback — LEDs pulse when G1 speaks, change color for different states (listening, processing, responding), and direct user attention to relevant information or actions."),
            ("Synchronization", "Match LED patterns to audio events: pulse brightness with speech amplitude, change colors at phrase boundaries, flash for alerts. Timing precision matters — LED changes must align with audio within ~100ms for perceived simultaneity."),
            ("Implementation", "Send simultaneous commands to audio and LED services through AudioClient. LedControl(r, g, b) controls chest RGB (0–255 per channel). Sequence LED changes to match the audio timeline — red during alerts, green for confirmations, blue for information."),
            ("Event Mapping", "Map audio events to LED states: speech start → LED on/pulse pattern, speech end → LED return to idle, error → flash red, success → solid green. Consistent event-to-color mapping builds user intuition over time."),
        ),
        "bottom_band": "Audio and LEDs share the same AudioClient — send commands to both simultaneously. When G1 speaks, its chest lights respond. Multimodal synchronization makes the robot feel alive."
    },

    # ── SLIDE 18: Complete Application Assembly ──
    {
        "title": "The Final Piece: Complete Application Assembly",
        "thesis": "Complete application assembly blends voice control, bipedal motion, and object manipulation into a single unified package. The challenge is synchronization; the outcome is a truly capable, interactive G1 application.",
        "board_type": "grid",
        "board_data": g(
            ("Goal", "Blend voice control (ASR/TTS), bipedal motion (locomotion FSM), and object manipulation (arm APIs) into one cohesive application. A user says 'walk to the table and grab the cup' — the robot executes all three modalities seamlessly."),
            ("Challenge", "Synchronizing multiple complex subsystems — each with different timing requirements, failure modes, and state machines. Locomotion runs at kHz control rates, audio streams in second-scale chunks, and arm actions complete in discrete gestures."),
            ("Architecture", "Event-driven design coordinates subsystems: a voice command triggers locomotion, which completes and fires an event that triggers arm control, which completes and triggers TTS confirmation. Each subsystem operates independently but coordinates through events."),
            ("Outcome", "A unified, interactive, and capable G1 application that responds to natural language, moves with purpose, and manipulates objects with precision. The whole is greater than the sum of its parts."),
        ),
        "bottom_band": "The unified application is a puzzle: Voice + Motion + Manipulation. Each piece is powerful alone. Together, they form a complete, interactive, intelligent robot."
    },

    # ── SLIDE 19: Blending Voice and Motion ──
    {
        "title": "\"Walk Forward\": Blending Voice Control and Bipedal Motion",
        "thesis": "Voice Command → ASR & Intent → Locomotion Trigger → TTS Feedback. When a user says 'Walk forward,' the system recognizes the command, triggers the locomotion controller, and confirms via speech — a seamless multimodal loop.",
        "board_type": "list",
        "board_data": lst(
            "Voice Command: User says 'Walk forward.' The microphone captures the audio and routes it to the ASR engine. Clear, simple commands with distinct phrasing improve recognition accuracy in noisy environments.",
            "ASR & Intent: ASR transcribes 'Walk forward' to text. Intent parser extracts the action ('walk') and direction ('forward'). The parsed intent is validated against the robot's current FSM state — walking requires FSM ≠ 1 (not damp).",
            "Locomotion Trigger: High-level controller sends velocity command (vx > 0 for forward) to the FSM. The FSM transitions to walking state and executes the motion. Low-level motor drivers translate the velocity target into joint trajectories.",
            "TTS Feedback: G1 confirms the action via TTS — 'Walking forward.' Feedback closes the interaction loop, confirming to the user that the command was understood and is being executed. The robot both acts and communicates."
        ),
        "bottom_band": "Voice → Intent → Motion → Confirmation. Four steps, one seamless interaction. The robot hears, understands, acts, and responds — a complete multimodal conversation."
    },

    # ── SLIDE 20: Blending Voice and Manipulation ──
    {
        "title": "\"Grab That\": Blending Voice Control and Object Manipulation",
        "thesis": "Voice Command → ASR & Intent → Arm Control Trigger → TTS Feedback. A command like 'Grab the red cup' is processed, the target is identified, the arm API executes the grasp, and TTS confirms — natural interaction through speech-guided manipulation.",
        "board_type": "list",
        "board_data": lst(
            "Voice Command: User says 'Grab the red cup.' The system must parse both the action ('grab') and the target object ('red cup'). Object references may require vision system integration for target identification and localization.",
            "ASR & Intent: ASR transcribes the full phrase. Intent parser extracts action=GRASP, target=red_cup. The system maps the target to a known object location or initiates visual search. Grasp planning determines approach angle and grip type.",
            "Arm Control Trigger: High-level arm API (G1ArmActionClient or custom arm_sdk trajectory) initiates the grasping sequence. The arm moves to the approach pose, closes the gripper, and verifies grasp stability through force feedback.",
            "TTS Feedback: G1 confirms — 'Grabbing the red cup.' Verbal confirmation is critical for manipulation tasks where the user may not have direct line of sight to the gripper. The robot narrates its own actions for transparency."
        ),
        "bottom_band": "Speech-guided manipulation: 'Grab the red cup' → ASR → Intent → Arm API → Grasp → TTS confirmation. The robot understands, reaches, grabs, and reports."
    },

    # ── SLIDE 21: Synchronizing All Modalities ──
    {
        "title": "The Symphony: Synchronizing Motion, Voice, and Manipulation",
        "thesis": "True multimodal coordination requires concurrency management, state-based conflict prevention, and event-driven architecture. All three subsystems — locomotion, arm control, and audio/speech — must work together without conflicting.",
        "board_type": "grid",
        "board_data": g(
            ("Concurrency", "Multiple tasks execute simultaneously — walking while speaking, gesturing while listening. Each subsystem runs on its own timeline: locomotion at kHz, audio in second-scale chunks, arm actions in discrete gestures. Coordination is the challenge."),
            ("State Management", "Ensure actions do not conflict. Walking while grasping requires the locomotion FSM to compensate for arm momentum. The state manager tracks which subsystems are active and prevents incompatible simultaneous operations."),
            ("Event-Driven Architecture", "Use events to trigger coordinated actions across subsystems. A locomotion-complete event triggers arm action start. An arm-complete event triggers TTS confirmation. Events decouple subsystems while enabling precise sequencing."),
            ("Safety Interlocks", "Critical safety rules: never start arm motion during active locomotion recovery, never play loud audio during emergency stop, always release arm SDK before switching control modes. Interlocks are enforced at the architecture level."),
        ),
        "bottom_band": "The symphony: Locomotion sets the rhythm, arms provide the melody, voice adds the lyrics, and LEDs paint the visuals. Event-driven architecture keeps everything in time."
    },

    # ── SLIDE 22: Practical Workflows for Packaging ──
    {
        "title": "Wrapping It Up: Packaging the Application",
        "thesis": "A well-packaged application bundles all dependencies, configuration files, and launch scripts into a single deployable unit. This ensures consistent, reproducible deployment across different G1 units and environments.",
        "board_type": "grid",
        "board_data": g(
            ("Dependencies", "Ensure all required Python packages (unitree_sdk2py, CycloneDDS), AI model files, and system libraries are included and versioned. Use requirements.txt or pyproject.toml for Python deps and document system-level requirements."),
            ("Configuration Files", "Bundle all necessary settings — audio parameters (volume, device), stance configurations (height, pitch, roll), FSM presets, and service endpoint constants. Externalize configs from code so behavior can be tuned without rebuilding."),
            ("Launch Scripts", "Create startup scripts that initialize all subsystems in the correct order: DDS channel → FSM check → AudioClient init → LocoClient init → application logic. Order matters — each subsystem depends on the ones initialized before it."),
            ("Environment Setup", "Document the runtime environment: conda environment name, CYCLONEDDS_HOME path, network interface configuration, and any environment variables. A setup script automates this so every deployment starts from a known-good state."),
        ),
        "bottom_band": "Package = dependencies + configs + launch scripts + environment docs. Bundle once, deploy anywhere. Reproducibility is reliability."
    },

    # ── SLIDE 23: Deploying to G1 ──
    {
        "title": "Going Live: Deploying a Full Multimodal Application to G1",
        "thesis": "Deployment transfers the application package to G1's onboard computer, configures the runtime environment, and executes launch scripts. A systematic deployment process ensures reliable, repeatable go-live events.",
        "board_type": "list",
        "board_data": lst(
            "Transfer: Move the application package to G1's onboard computer via SCP, rsync, or USB. Verify file integrity after transfer — checksums ensure no corruption during the copy. Organize files in a standard directory structure on the target.",
            "Environment Setup: Configure the runtime environment on G1 — activate conda environment, set CYCLONEDDS_HOME, verify network interface, and run connection check (g1_connection_check.py --interface en6). A green pre-flight check is mandatory before launch.",
            "Execution: Run the launch script and monitor startup. Watch for error messages in the first 30 seconds — most configuration issues surface immediately. Verify each subsystem initializes successfully before proceeding to the next.",
            "Monitoring: After launch, continuously monitor key metrics — DDS message rate, FSM state, audio service status. Automated monitoring catches degradation before it becomes failure. Log everything for post-session analysis and debugging."
        ),
        "bottom_band": "Deploy = Transfer + Configure + Execute + Monitor. Each step validated before the next. A systematic deployment is a safe deployment."
    },

    # ── SLIDE 24: Final Validation & Deployment ──
    {
        "title": "The Final Check: Validation and Deployment",
        "thesis": "Before considering the application complete, rigorous final validation through full-stack testing, deployment best practices, and a comprehensive course review ensures reliable, production-ready operation.",
        "board_type": "grid",
        "board_data": g(
            ("Full-Stack Testing", "End-to-end validation of the entire integrated system — from voice command input to physical robot action and TTS feedback. Every subsystem is tested together, not in isolation. Scenario-based testing mirrors real-world use cases."),
            ("Deployment Habits", "Best practices for reliable operation: version control for all code and configs, automated logging for debugging, regular maintenance schedules for hardware and software updates. Good habits prevent production incidents."),
            ("Course Review", "Days 1-4: fundamentals and basic control. Day 5: DDS communication and safety workflows. Day 6: locomotive and arm control infrastructure. Day 7: AI, audio, and complete application assembly. The full G1 journey in review."),
        ),
        "bottom_band": "The final check: test everything together, deploy with discipline, and review the complete journey. Validation is not the last step — it is the step that confirms all previous steps were correct."
    },

    # ── SLIDE 25: Full-Stack Testing ──
    {
        "title": "End-to-End: Full-Stack Testing",
        "thesis": "Full-stack testing validates complete use cases from user input to robot action and feedback. Scenario testing, edge case handling, and performance monitoring ensure the application works reliably under real-world conditions.",
        "board_type": "grid",
        "board_data": g(
            ("Scenario Testing", "Run through complete use cases end-to-end: 'Walk to table, grab cup, say Done.' Test the full pipeline — voice → locomotion → arm → TTS — in sequence. Each scenario validates the integration of all subsystems working together."),
            ("Edge Cases", "Test unusual inputs and unexpected situations: garbled speech, simultaneous commands, network interruptions, low battery states. The application must degrade gracefully — never crash, never execute unsafe commands, always return to a safe state."),
            ("Performance Monitoring", "Check CPU and memory usage during operation. Monitor DDS message latency and dropout rates. Track audio playback buffer health. Performance issues that are invisible in single-subsystem tests often emerge during full-stack integration."),
        ),
        "bottom_band": "Full-stack = scenario testing + edge cases + performance monitoring. Test the complete user journey, not just individual components. Integration reveals what isolation hides."
    },

    # ── SLIDE 26: Deployment Habits ──
    {
        "title": "Built to Last: Deployment Habits for Reliable Operation",
        "thesis": "Reliable operation requires disciplined deployment habits: version control for traceability, automated logging for debugging, and regular maintenance for sustained performance. These practices prevent incidents before they occur.",
        "board_type": "grid",
        "board_data": g(
            ("Version Control", "Track all changes to application code, configuration files, and launch scripts. Git provides an audit trail — every deployment can be traced to a specific commit. Tag releases for known-good configurations that can be rolled back instantly."),
            ("Automated Logging", "Ensure comprehensive logs are generated during operation — DDS message stats, FSM state transitions, RPC return codes, audio playback events. Structured logging enables post-hoc analysis. Log everything you might need to debug later."),
            ("Regular Maintenance", "Schedule periodic checks: verify DDS connectivity, test audio output, calibrate sensors, update SDK versions. Preventive maintenance catches degradation before it becomes failure. A maintained robot is a reliable robot."),
        ),
        "bottom_band": "Good habits = version control + automated logging + regular maintenance. These are not optional extras — they are the foundation of production-grade robotics."
    },

    # ── SLIDE 27: Course Wrap-Up ──
    {
        "title": "Our G1 Journey: A Comprehensive Look Back",
        "thesis": "From fundamentals to full application assembly — the seven-day G1 curriculum covers hardware basics, DDS communication, safety workflows, locomotion and arm control, AI integration, audio infrastructure, and unified deployment.",
        "board_type": "table",
        "board_data": tbl(
            ["Day", "Focus", "Key Achievement"],
            [
                ["Days 1–4", "Fundamentals, Hardware & Basic Control", "Go2 platform: DDS pub/sub, SportClient, obstacle avoidance, visual SLAM. Established the robotics development workflow and safety discipline."],
                ["Day 5", "Communication (DDS) & Safety Workflows", "G1 platform: DDS architecture, FSM state machine, LocoClient RPC, readiness gates, and supervised motion commands through interactive menus."],
                ["Day 6", "Locomotive & Arm Control Infrastructure", "G1 arm actions via G1ArmActionClient RPC and rt/arm_sdk streaming. Scripted sequences, custom joint trajectories, and arm SDK enable/disable patterns."],
                ["Day 7", "AI, Audio & Application Assembly", "AI locomotion engines, audio parameter classes, ASR/TTS integration, LED synchronization, multimodal coordination, and complete application packaging and deployment."],
            ],
        ),
        "bottom_band": "Seven days. Four platforms of learning. One complete robotics operator. From 'what is DDS?' to 'deploy the unified multimodal application.'"
    },

    # ── SLIDE 28: The Future of G1 ──
    {
        "title": "Beyond the Course: The Future of G1 Development",
        "thesis": "This course is the foundation. The future of G1 development extends into advanced AI, complex manipulation, and swarm robotics — each building on the DDS, FSM, and multimodal integration skills established here.",
        "board_type": "grid",
        "board_data": g(
            ("Advanced AI", "Deeper reinforcement learning for adaptive locomotion across extreme terrain. Computer vision integration for object detection, scene understanding, and visual servoing. Learning-based policies that improve with every interaction."),
            ("Complex Manipulation", "Intricate grasping and tool use — opening doors, operating switches, handling delicate objects. Multi-finger dexterity, force-controlled interactions, and bimanual coordination for tasks requiring two-arm collaboration."),
            ("Swarm Robotics", "Coordinating multiple G1 units for collaborative tasks — construction, search and rescue, warehouse logistics. Inter-robot DDS communication, distributed task allocation, and collective behavior emerge from individual skills."),
            ("Your Next Steps", "Continue exploring the Unitree SDK examples. Experiment with custom arm_sdk trajectories. Build your own multimodal application. The skills you've developed this week are the foundation for whatever you build next."),
        ),
        "bottom_band": "The journey continues: advanced AI, complex manipulation, swarm robotics. This course gave you the keys. Now drive."
    },

    # ── SLIDE 29: Outcome Coverage Report ──
    {
        "title": "Comprehensive Coverage: Day 7 Outcomes Achieved",
        "thesis": "All required Day 7 outcomes have been thoroughly covered — AI-driven locomotion with state validation benchmarks, complete audio infrastructure, multimodal speech interfaces, and unified application assembly with deployment practices.",
        "board_type": "table",
        "board_data": tbl(
            ["Outcome", "Coverage", "Topics Addressed"],
            [
                ["AI-Driven Locomotion & Validation", "100%", "AI engine interfacing, JSON/Protobuf data formats, real-time data flow, static posture checks (joint limits, CoM, ground contact), dynamic stability tests (ZMP, perturbation, fall recovery), trajectory adherence (position, orientation, path deviation)."],
                ["G1 Audio Infrastructure", "100%", "AudioClient RPC model, AudioParams class definition (volume, device, sample rate, channels, bit depth), service constants (AUDIO_PLAY_SERVICE, status codes), playback routines (Load → Apply → Stream → Verify → Stop)."],
                ["Multimodal Speech Interfaces", "100%", "ASR pipeline (microphone → engine → intent parsing → command validation), TTS pipeline (TtsMaker, voice selection, dynamic responses), WAV file management, LED synchronization with audio events."],
                ["Complete Application Assembly", "100%", "Blending voice with locomotion and manipulation, event-driven multimodal synchronization, application packaging (dependencies, configs, launch scripts), deployment workflow, full-stack testing, deployment habits."],
            ],
        ),
        "bottom_band": "100% coverage across all four Day 7 outcome areas. Every topic addressed with practical workflows and beginner-friendly explanations. Ready for production."
    },

    # ── SLIDE 30: Copyright ──
    {
        "title": "© 2026 Vinci AI. All rights reserved.",
        "thesis": "This material is for educational purposes only and should not be used for actual robot operation without proper training and supervision. Property of Vinci AI — Do Not Distribute.",
        "board_type": "grid",
        "board_data": g(
            ("Copyright", "© 2026 Vinci AI. All rights reserved. This course material, including all slides, labs, code examples, and documentation, is the intellectual property of Vinci AI."),
            ("Usage Restriction", "Property of Vinci AI — Do Not Distribute. This material is provided for the exclusive use of authorized course participants and may not be reproduced, shared, or redistributed without explicit written permission."),
            ("Disclaimer", "This material is for educational purposes only. Actual robot operation requires proper training, supervision, and adherence to all safety protocols. Always prioritize safety when working with robotics hardware."),
            ("Acknowledgments", "Built on the Unitree SDK2 Python framework and CycloneDDS. Course curriculum developed by Vinci AI for the G1 EDU Plus / Ultimate-D platform. Thank you for participating in the G1 operator training program."),
        ),
        "bottom_band": "End of Day 7 — End of Course. Thank you for your participation. Always prioritize safety. © 2026 Vinci AI."
    },
]


def main():
    with open(SYLLABUS_PATH, "r") as f:
        syllabus = json.load(f)

    day7 = syllabus["07"]
    day7["slides"] = SLIDES

    with open(SYLLABUS_PATH, "w") as f:
        json.dump(syllabus, f, indent=2, ensure_ascii=False)

    print(f"✅ Day 7: {len(SLIDES)} slides written.")
    types = {}
    for s in SLIDES:
        t = s["board_type"]
        types[t] = types.get(t, 0) + 1
    print(f"   board_type distribution: {types}")


if __name__ == "__main__":
    main()