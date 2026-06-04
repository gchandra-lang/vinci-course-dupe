# Day 4 Beginner-Friendly Full Slide Content

## Course metadata
| Field | Value |
|---|---|
| Course | Vinci Unitree Train-the-Trainer |
| Day | Day 4 — B2 Rugged Inspection, Mock Scripts, Field Capture, Telemetry, Data Visualization, Reporting, and Maintenance |
| Audience | Beginner instructors and students who need only the concepts required for Day 4 outcomes |
| Platform focus | Unitree B2 field inspection workflow with necessary references to Gazebo, ROS 2/DDS-style communication concepts, camera/video capture, SportModeState, SportClient, payload data, and run-folder validation |
| Slide count | 1 cover plus 44 numbered slides |
| Source basis | Day 4 lecture notes, B2 inspection labs, run-folder validator, camera/video capture scripts, SportModeState telemetry, SportClient motion, and field reporting workflow [1] [4] [5] [6] [9] [10] [11] |
| Design identity | Vinci AI premium academic technology training style |

## Teaching design notes
This revised deck removes repeated explanation and keeps only material that directly supports the four required Day 4 outcomes. The organizing flow is **Plan → Capture → Log → Package → Validate → Report**, and every content slide must support rugged navigation and multi-sensor reasoning, mock inspection scripting, B2 field execution, or data visualization with reporting and maintenance.

Use a pale blue-gray background, dark navy typography, teal-blue rule systems, modular grids, and simple schematic visuals. Every slide should include a small top-right Vinci AI icon/logo, three subtle diagonal watermark bands reading **“Property of Vinci AI — Do Not Distribute”**, and the bottom-left copyright tag **“© 2026 Vinci AI. All rights reserved.”**. Diagrams should favor layered boxes, arrows, checklists, pipelines, comparison tables, top-down maps, timelines, dashboards, and validator decision trees.

Transition slides are intentionally minimal and contain only the section title plus a short subtitle. Content slides use a consistent structure: **Section**, **Purpose**, **On-slide text**, **Speaker notes**, and **Diagram cue**. Beginner explanations are included only where they help students complete the Day 4 workflow.

## Section summary table
| Section | Slide range | Teaching role |
|---|---|---|
| Orientation | Slides 1–3 | Define the four required Day 4 jobs, the single workflow, and the evidence standard. |
| Rugged Navigation and Multi-Sensor Arrays | Slides 4–12 | Cover rugged terrain, bounded navigation, SLAM, costmaps, obstacle supervision, sensor roles, timing, and telemetry context. |
| Mock Inspection Scripts | Slides 13–23 | Build mock and Gazebo rehearsal workflows, camera capture, OpenCV-derived outputs, JSONL logging, bounded motion, debugging, and validation gates. |
| B2 Field Execution | Slides 24–33 | Execute supervised B2 roles, readiness checks, stable capture, RTSP verification, telemetry logging, checkpoint mapping, notes, and fallbacks. |
| Logs, Reports, and Maintenance | Slides 34–41 | Parse telemetry and payload data, visualize motion, write artifact-backed reports, validate packages, debug failures, and complete B2 maintenance. |
| Closing | Slides 42–44 | Confirm the four required outcomes and define Day 4 success as reviewable evidence. |

## Cover
**Day 4 Beginner-Friendly Full Slide Content**

B2 Rugged Inspection, Mock Scripts, Field Capture, Telemetry, Reporting, and Maintenance

Vinci Unitree Train-the-Trainer · © 2026 Vinci AI

## Slide 1: Day 4 Has Four Jobs
**Section:** Orientation

**Purpose:** State the required Day 4 learning outcomes without adding unrelated review.

**On-slide text:** Rugged navigation → Inspection scripts → B2 field run → Logs, reports, maintenance.

**Speaker notes:** Day 4 is focused on four practical jobs. Students reason about rugged terrain and multi-sensor evidence, build mock inspection scripts, execute a supervised B2 inspection with camera capture and telemetry logging, then parse data into reports and maintenance notes. Anything outside those jobs is intentionally minimized.

**Diagram cue:** Four-column outcome map with one teal icon per job and a thin arrow connecting the columns.

## Slide 2: One Flow Organizes Everything
**Section:** Orientation

**Purpose:** Give students a single arrow-style workflow that prevents scattered activity.

**On-slide text:** Plan → Capture → Log → Package → Validate → Report.

**Speaker notes:** The whole day can be taught through one repeated workflow. Students plan the inspection, capture sensor evidence, log robot state, package artifacts into the run folder, validate the structure, and write the report. This reduces redundancy because every activity must connect to one step in the same flow.

**Diagram cue:** Large horizontal arrow flow with six boxes, a locked validation gate, and a report package at the end.

## Slide 3: Evidence Is the Standard
**Section:** Orientation

**Purpose:** Define the minimum evidence mindset needed for all four outcomes.

**On-slide text:** A claim is accepted only when a file, timestamp, and context support it.

**Speaker notes:** Students should not treat video, logs, or notes as separate assignments. They are parts of one evidence standard. A useful inspection claim should identify what was observed, where it happened, when it happened, and which artifact supports it. This standard guides navigation, scripting, field capture, and reporting.

**Diagram cue:** Claim card connected to four small boxes: file, timestamp, checkpoint, context note.

## Slide 4: Section 1 — Rugged Navigation and Multi-Sensor Arrays
**Section 1 — Rugged Navigation and Multi-Sensor Arrays**

Understand terrain, sensing roles, and runtime evidence for inspection.

## Slide 5: Rugged Terrain Changes the Run
**Section:** Rugged Navigation and Multi-Sensor Arrays

**Purpose:** Explain terrain complexity only as it affects Day 4 inspection evidence.

**On-slide text:** Slope, gravel, glare, occlusion, and vibration affect safety and proof.

**Speaker notes:** Rugged terrain is important because it changes both robot behavior and evidence quality. A slope may alter posture, loose surface may affect traction, glare may hide inspection details, and vibration may blur images. Students should record these conditions because they influence what the final report can honestly defend.

**Diagram cue:** Simple top-down rugged terrain map with slope, gravel, obstacle, glare zone, and safe operator boundary.

## Slide 6: Navigation Means Bounded Progress
**Section:** Rugged Navigation and Multi-Sensor Arrays

**Purpose:** Define navigation in beginner language without re-teaching unrelated planning theory.

**On-slide text:** Know the checkpoint, choose a safe path, move in small steps, stop to prove.

**Speaker notes:** For Day 4, navigation means making safe, explainable progress toward inspection checkpoints. Students do not need advanced autonomy theory to act professionally. They need a checkpoint goal, a visible hazard plan, bounded motion, a stop point, and evidence that the robot reached the inspection view safely.

**Diagram cue:** Top-down checkpoint route with short motion segments, stop points, hazard labels, and camera icons.

## Slide 7: SLAM Supports Location Confidence
**Section:** Rugged Navigation and Multi-Sensor Arrays

**Purpose:** Give the minimum SLAM explanation needed for rugged inspection context.

**On-slide text:** SLAM estimates where the robot is while building or updating a map.

**Speaker notes:** SLAM matters because inspection claims depend on location confidence. Students only need the beginner idea: the robot uses sensor observations to estimate its position and maintain a map. If localization is uncertain in cluttered or rugged terrain, the report should say so instead of overstating precision.

**Diagram cue:** Loop diagram showing Sensor Observation → Position Estimate → Map Update → Inspection Checkpoint.

## Slide 8: Costmaps Turn Space into Risk
**Section:** Rugged Navigation and Multi-Sensor Arrays

**Purpose:** Explain costmaps only as a practical inspection planning tool.

**On-slide text:** Free space is low cost; obstacles and uncertain terrain are high cost.

**Speaker notes:** A costmap is a simple way to turn space into movement risk. Clear floor is low cost, blocked areas are not usable, and uncertain surfaces should increase caution. Students should use the costmap idea to explain why the B2 path avoids hazards and where human supervision remains necessary.

**Diagram cue:** Grid map with green free cells, yellow caution cells, dark obstacle cells, and a path avoiding high cost.

## Slide 9: Obstacle Avoidance Needs Supervision
**Section:** Rugged Navigation and Multi-Sensor Arrays

**Purpose:** Prevent beginners from treating sensor-based avoidance as automatic safety.

**On-slide text:** Sensors help, but spotters and stop authority define the safe envelope.

**Speaker notes:** Obstacle avoidance is useful, but it is not a guarantee. Sensors can miss low, reflective, moving, transparent, or poorly lit hazards. The safe envelope still depends on field roles, slow motion, visible boundaries, and immediate stop authority. This keeps rugged navigation connected to practical field discipline.

**Diagram cue:** Three-layer safety envelope: sensor detection, software caution, human supervision around the outside.

## Slide 10: Each Sensor Has a Job
**Section:** Rugged Navigation and Multi-Sensor Arrays

**Purpose:** Clarify multi-sensor arrays by assigning evidence roles to each channel.

**On-slide text:** Camera sees appearance. Telemetry explains motion. Payload measures condition. Notes explain limits.

**Speaker notes:** A multi-sensor array should not be described as collecting “more data.” Each channel answers a different question. Camera frames show visual condition, telemetry explains how the robot moved, payload data may measure the target, and notes document uncertainty. The report improves when these roles are explicit.

**Diagram cue:** Sensor-role comparison table with columns Sensor, Question, Artifact, Report Use.

## Slide 11: Timing Connects the Sensors
**Section:** Rugged Navigation and Multi-Sensor Arrays

**Purpose:** Show why camera, telemetry, payload data, and notes must align by checkpoint time.

**On-slide text:** A frame, a log line, and a payload value should describe the same moment.

**Speaker notes:** Multi-sensor evidence is strongest when timing is clear. A camera frame, telemetry line, payload measurement, and operator note should all point to the same checkpoint moment. Beginners can start with checkpoint IDs and approximate timestamps, then improve synchronization as their scripting skills mature.

**Diagram cue:** Timeline with checkpoint cp01 aligning frame.jpg, SportModeState line, payload row, and operator note.

## Slide 12: Telemetry Is Runtime Context
**Section:** Rugged Navigation and Multi-Sensor Arrays

**Purpose:** Connect SportModeState fields directly to rugged inspection interpretation.

**On-slide text:** Mode, gait, velocity, yaw speed, position, and body height explain what happened.

**Speaker notes:** SportModeState is the robot’s runtime context. If a checkpoint frame is blurred, velocity or yaw speed may explain it. If posture looks unusual, body height or mode may help. Students should use telemetry as supporting evidence, not as an isolated log file.

**Diagram cue:** Dashboard grouped into Motion, Posture, Mode, and Timing panels with one sample field in each.

## Slide 13: Section 2 — Mock Inspection Scripts
**Section 2 — Mock Inspection Scripts**

Build the inspection workflow safely before the B2 field run.

## Slide 14: Mock First, Then Hardware
**Section:** Mock Inspection Scripts

**Purpose:** Establish the simulation-to-hardware handoff as a Day 4 validation gate.

**On-slide text:** Mock scenario passes → folder structure passes → instructor approves B2 handoff.

**Speaker notes:** Students should prove the workflow before the hardware run. A mock scenario lets them define checkpoints, test capture placeholders, write metadata, and package the run folder. Hardware begins only after the mock workflow and folder structure are understandable enough for instructor approval.

**Diagram cue:** Gate diagram: Mock Scenario → Run Folder Check → Instructor Approval → B2 Handoff.

## Slide 15: Gazebo Rehearses the Logic
**Section:** Mock Inspection Scripts

**Purpose:** Use Gazebo only where it supports Day 4 inspection workflow rehearsal.

**On-slide text:** Simulation practices route logic, checkpoint timing, and failure handling without field risk.

**Speaker notes:** Gazebo is useful because it lets students rehearse inspection logic before field risk appears. It does not replace the B2 run, but it helps teams practice checkpoint sequencing, sensor thinking, timing, and recovery decisions. The lesson is rehearsal discipline, not simulation perfection.

**Diagram cue:** Two-lane diagram comparing Gazebo rehearsal outputs with later B2 field outputs.

## Slide 16: Scripts Should Show Procedure
**Section:** Mock Inspection Scripts

**Purpose:** Define a functional inspection script as a readable procedure, not a black box.

**On-slide text:** Setup → Capture → Log → Move → Package → Validate.

**Speaker notes:** A functional inspection script should make the run procedure visible. Students should see setup, capture, logging, movement, packaging, and validation as separate steps. This prevents a black-box script from hiding failures and makes the workflow easier to debug when camera, telemetry, or folder paths break.

**Diagram cue:** Script pipeline with six labeled blocks and small diagnostic taps between blocks.

## Slide 17: Scenario Files Set Intent
**Section:** Mock Inspection Scripts

**Purpose:** Show how patrol plans and metadata make the mock run reviewable.

**On-slide text:** metadata.json says who and when; patrol_plan.json says what checkpoints matter.

**Speaker notes:** The mock scenario should create intent before any capture occurs. Metadata identifies operator, date, robot, and run context. The patrol plan identifies checkpoint IDs and what each checkpoint should inspect. These files make the inspection script accountable and keep later report claims tied to planned targets.

**Diagram cue:** Layered document cards for metadata.json and patrol_plan.json feeding into checkpoint folders.

## Slide 18: Camera Scripts Capture Context
**Section:** Mock Inspection Scripts

**Purpose:** Explain camera capture scripts as inspection evidence producers.

**On-slide text:** Front/rear stills and RTSP clips become useful only after verification.

**Speaker notes:** Camera scripts produce visual context for inspection, but saved files should be checked before they are trusted. Students should confirm that a still image opens, a video plays, and the content matches the intended checkpoint. This keeps capture focused on usable evidence rather than file creation alone.

**Diagram cue:** Camera pipeline: Front/Rear Client or RTSP → Save File → Open/Play → Map to Checkpoint.

## Slide 19: OpenCV Outputs Are Derived
**Section:** Mock Inspection Scripts

**Purpose:** Prevent processed images from replacing raw inspection evidence.

**On-slide text:** Keep raw frames primary; label processed frames as derived outputs.

**Speaker notes:** OpenCV can help demonstrate simple image processing, but processing should not overwrite evidence. Raw frames are the primary record. Edge views, filters, annotations, and detection outputs are derived artifacts. Students should preserve both and explain which one supports the report claim.

**Diagram cue:** Branching image pipeline: raw frame archived, copy processed, derived output labeled separately.

## Slide 20: JSONL Makes Logs Inspectable
**Section:** Mock Inspection Scripts

**Purpose:** Explain why telemetry logging should use simple repeated records.

**On-slide text:** One JSON line per state sample makes the run easy to parse later.

**Speaker notes:** A JSONL telemetry log is beginner-friendly because each line can be inspected as one state sample. Students can open the file, read a line, and find fields such as mode, velocity, yaw speed, or body height. This structure prepares the file for later parsing and visualization.

**Diagram cue:** Horizontal strip of JSON lines feeding into a small parsed table.

## Slide 21: Motion Commands Stay Small
**Section:** Mock Inspection Scripts

**Purpose:** Set the scripting rule for safe high-level B2 motion.

**On-slide text:** Approved command → short duration → observe → StopMove → note result.

**Speaker notes:** Mock scripts should teach the same discipline used on hardware. A high-level motion command needs instructor approval, small values, short duration, visible observation, and an explicit stop. Students should record the result, because the report needs to explain what command produced the captured evidence.

**Diagram cue:** Command loop with SportClient request, observation box, StopMove block, and notes card.

## Slide 22: Debug One Channel at a Time
**Section:** Mock Inspection Scripts

**Purpose:** Include debugging habits only where they support Day 4 scripting outcomes.

**On-slide text:** Test camera alone, logger alone, folder paths alone, then combine.

**Speaker notes:** When a script fails, students should avoid changing everything at once. They should test the camera path alone, telemetry logger alone, folder structure alone, and validator alone before combining them. This debugging habit turns failures into evidence about which channel needs repair.

**Diagram cue:** Layered debugging staircase with Camera, Logger, Folder, Validator, Combined Run.

## Slide 23: Validation Catches Script Gaps
**Section:** Mock Inspection Scripts

**Purpose:** Use the validator as a script-readiness gate before field execution.

**On-slide text:** If the mock package fails validation, the B2 run should wait.

**Speaker notes:** The validator is a readiness gate for the script, not just a grading tool. Missing metadata, empty telemetry, absent checkpoint frames, or mismatched checkpoint IDs show that the procedure is not ready. Repairing these gaps in the mock run prevents avoidable field confusion.

**Diagram cue:** Validator decision tree: Mock Folder → PASS to B2 Gate, FAIL to Script Repair Loop.

## Slide 24: Section 3 — B2 Field Execution
**Section 3 — B2 Field Execution**

Run the supervised inspection, capture sensors, and log telemetry.

## Slide 25: Field Roles Keep Order
**Section:** B2 Field Execution

**Purpose:** Define field-testing discipline through clear human responsibilities.

**On-slide text:** Run director, terminal operator, spotter, evidence lead, reporter.

**Speaker notes:** A B2 field run needs clear roles before motion. The run director approves action, the terminal operator controls commands, the spotter watches the robot and space, the evidence lead checks saved files, and the reporter records limitations. Role clarity prevents excited students from creating unsafe mixed instructions.

**Diagram cue:** Top-down field map showing robot zone and five role cards positioned around the perimeter.

## Slide 26: Readiness Is Observable
**Section:** B2 Field Execution

**Purpose:** Turn readiness into visible checks rather than confidence statements.

**On-slide text:** Interface selected, perimeter clear, stop path known, cameras tested, logger ready.

**Speaker notes:** Students should not say they are ready because they feel ready. They should show readiness through checks: selected network interface, clear perimeter, known stop action, verified cameras, active logger, prepared folder, and named checkpoint plan. If one check is missing, the run waits.

**Diagram cue:** Checklist gate with seven items unlocking a teal Motion Approved box.

## Slide 27: Capture at Stable Dwell
**Section:** B2 Field Execution

**Purpose:** Teach the most important field capture timing rule.

**On-slide text:** Move to view, stop or dwell, capture, label checkpoint, continue.

**Speaker notes:** Checkpoint evidence is strongest when the robot is stable. Capturing during a turn or translation can create blur and make the report less defensible. Students should move into view, stop or dwell, capture the frame, label it with the checkpoint, and only then continue.

**Diagram cue:** Timeline: Approach → StopMove/Dwell → Capture Frame → Label cp01 → Continue.

## Slide 28: RTSP Needs Proof
**Section:** B2 Field Execution

**Purpose:** Make video verification a required field habit.

**On-slide text:** A video file counts only after it opens, plays, and matches the checkpoint.

**Speaker notes:** RTSP recording may fail because the stream, writer settings, codec, or dimensions are wrong. A file name alone is not evidence. Students should check file size, open playback, confirm the scene, and document any fallback if video cannot be used.

**Diagram cue:** Video verification flow: Record → File Size → Playback → Scene Match → Accept or Fallback.

## Slide 29: Log Through the Run
**Section:** B2 Field Execution

**Purpose:** Ensure telemetry logging covers the complete inspection window.

**On-slide text:** Start before motion, keep logging through capture, stop after final notes.

**Speaker notes:** Telemetry logging should cover the meaningful run window. Starting late can miss the approach, and stopping early can miss recovery or final posture. The evidence lead should confirm that SportModeState logging begins before motion and continues through checkpoint captures and final notes.

**Diagram cue:** Parallel timeline with camera events above a continuous SportModeState logging lane.

## Slide 30: Map Captures to Checkpoints
**Section:** B2 Field Execution

**Purpose:** Make field artifacts align with the run-folder schema.

**On-slide text:** Raw files stay preserved; selected frames copy into checkpoints/<id>/frame.jpg.

**Speaker notes:** Students should preserve raw captures and also normalize selected evidence into the expected checkpoint paths. This step turns field media into reviewable inspection evidence. A good habit is to state the checkpoint ID aloud, save the capture, and immediately confirm where the selected frame belongs.

**Diagram cue:** Two-column file flow: Raw Captures folder to selected checkpoint folders cp01, cp02, cp03.

## Slide 31: Field Notes Capture Limits
**Section:** B2 Field Execution

**Purpose:** Keep notes focused on evidence limitations and field decisions.

**On-slide text:** Record glare, occlusion, skipped checkpoints, fallback streams, and safety changes.

**Speaker notes:** Field notes explain what the files cannot show by themselves. If glare limited visibility, the rear stream failed, a checkpoint was skipped, or the route changed for safety, the report should include that limitation. Honest notes make the final inspection more credible, not weaker.

**Diagram cue:** Notes panel connected to limitation tags: glare, occlusion, fallback, skipped, route change.

## Slide 32: Evidence Habit: Verify Immediately
**Section:** B2 Field Execution

**Purpose:** Merge evidence habit with field discipline to avoid repeated evidence slides.

**On-slide text:** Capture, open, label, place, and confirm before leaving the checkpoint.

**Speaker notes:** The field evidence habit is immediate verification. After capture, students should open the artifact, label the checkpoint, place the selected file in the package, and confirm the log is still running. This avoids discovering after the run that the strongest checkpoint has no usable evidence.

**Diagram cue:** Checkpoint mini-loop: Capture → Open → Label → Place → Confirm Log → Continue.

## Slide 33: Fallbacks Must Be Stated
**Section:** B2 Field Execution

**Purpose:** Teach safe recovery when a sensor or stream fails during the B2 run.

**On-slide text:** Use stills, telemetry, and notes if video fails; never hide the limitation.

**Speaker notes:** A field run can still be useful when one channel fails. If RTSP video is unavailable, students can rely on verified stills, telemetry logs, and limitation notes. The key is to state the fallback clearly so the final report does not imply evidence that was never captured.

**Diagram cue:** Fallback decision tree from Video Fails to Still Frame, Telemetry, Limitation Note, Report Caveat.

## Slide 34: Section 4 — Logs, Reports, and Maintenance
**Section 4 — Logs, Reports, and Maintenance**

Parse the run, visualize evidence, report claims, and care for the B2.

## Slide 35: Parse Logs into Fields
**Section:** Logs, Reports, and Maintenance

**Purpose:** Move from raw telemetry to useful inspection data.

**On-slide text:** Extract timestamp, mode, velocity, yaw speed, position, and body height.

**Speaker notes:** Data visualization begins by parsing logs into useful fields. Students should extract timing, mode, velocity, yaw speed, position, and body height from SportModeState records. The goal is not advanced analytics; it is turning raw telemetry into a readable explanation of robot behavior.

**Diagram cue:** Pipeline: sportmodestate.jsonl → Parser → Selected Fields → Clean Table.

## Slide 36: Visualize Motion and Capture
**Section:** Logs, Reports, and Maintenance

**Purpose:** Give students one concrete visualization that supports the report.

**On-slide text:** Plot speed, yaw speed, and checkpoint capture moments on one timeline.

**Speaker notes:** A simple timeline can explain the field run clearly. Speed and yaw speed show when the robot moved or turned, while vertical markers show checkpoint captures. This helps students explain whether a frame was taken during stable dwell or during motion that might weaken image quality.

**Diagram cue:** Timeline chart cue with speed line, yaw-speed line, and vertical markers cp01, cp02, cp03.

## Slide 37: Payload Data Needs Context
**Section:** Logs, Reports, and Maintenance

**Purpose:** Teach payload data parsing without drifting into unrelated analytics.

**On-slide text:** Payload value + timestamp + checkpoint + robot state = usable measurement.

**Speaker notes:** Payload data becomes useful only when it is tied to context. A measurement should include timestamp, checkpoint ID, sensor identity, and relevant robot state. Without that context, the number may be hard to interpret or defend in the report. Tables are the best beginner format.

**Diagram cue:** Payload table with columns Timestamp, Checkpoint, Sensor Value, Robot State, Interpretation.

## Slide 38: Reports Make Defensible Claims
**Section:** Logs, Reports, and Maintenance

**Purpose:** Connect visual evidence, telemetry, payload data, and notes to report writing.

**On-slide text:** Claim → artifact → telemetry → limitation → confidence.

**Speaker notes:** A report should make claims that the evidence can support. Students can use a fixed pattern: state the claim, name the artifact, cite the telemetry context, explain any limitation, and assign a confidence statement. This prevents reports from becoming vague summaries of a live demo.

**Diagram cue:** Five-part report card template with Claim, Artifact, Telemetry, Limitation, Confidence.

## Slide 39: Validation Protects the Report
**Section:** Logs, Reports, and Maintenance

**Purpose:** Keep validation as a final report-readiness check, not a repeated theme.

**On-slide text:** PASS means the package can be reviewed; warnings still need explanation.

**Speaker notes:** The validator checks whether required files and paths are present. A pass means the package is structurally reviewable, but warnings may still need explanation in the report. A fail means the team should repair the folder before making final inspection claims.

**Diagram cue:** Validator board with PASS, PASS with Warnings, and FAIL leading to Repair or Report Review.

## Slide 40: Debug from Message to Fix
**Section:** Logs, Reports, and Maintenance

**Purpose:** Provide one consolidated debugging slide for validation and data issues.

**On-slide text:** Missing metadata, empty logs, bad frames, and mismatched checkpoints each point to a fix.

**Speaker notes:** Students should interpret error messages as clues. Missing metadata means accountability is incomplete. Empty logs mean runtime evidence was not saved. Bad frames suggest corrupt or placeholder images. Mismatched checkpoints mean the plan and package disagree. Each problem has a specific repair path.

**Diagram cue:** Troubleshooting table with columns Validator Message, Likely Cause, First Fix, Report Impact.

## Slide 41: Maintain the B2 Afterward
**Section:** Logs, Reports, and Maintenance

**Purpose:** Include the required B2 hardware maintenance walkthrough as part of field closure.

**On-slide text:** Power state, body, feet, payload mount, cables, sensors, and file archive.

**Speaker notes:** The inspection is not finished when the report is drafted. Students should close with a B2 maintenance walkthrough: safe power state, visible body condition, feet, payload mounting, cables, sensor surfaces, and archived files. Hardware care protects the next team and completes professional field discipline.

**Diagram cue:** B2 silhouette surrounded by maintenance checklist callouts and a final archive box.

## Slide 42: Closing — Required Outcomes Check
**Closing — Required Outcomes Check**

Confirm that every Day 4 activity served the four required outcomes.

## Slide 43: Four Outcomes Are Complete
**Section:** Closing

**Purpose:** Summarize achievement without adding new material.

**On-slide text:** Terrain and sensors. Mock scripts. B2 field capture. Logs, reports, maintenance.

**Speaker notes:** The revised deck closes by returning to the four required outcomes. Students have learned how rugged terrain changes navigation evidence, how mock scripts rehearse inspection procedure, how B2 field execution captures sensors and telemetry, and how parsed logs, payload context, reports, and maintenance complete the workflow.

**Diagram cue:** Four outcome tiles with check marks and one example artifact under each tile.

## Slide 44: Ready Means Reviewable
**Section:** Closing

**Purpose:** Give instructors a concise final standard for Day 4 success.

**On-slide text:** A successful run folder can be reviewed by someone who was not there.

**Speaker notes:** The final standard is reviewability. Another engineer should open the run folder and understand the scenario, route, captures, telemetry, payload context, validation result, limitations, report claims, and maintenance notes. If the story depends mainly on memory, the Day 4 evidence workflow is incomplete.

**Diagram cue:** Final checklist: Scenario, Route, Captures, Telemetry, Payload, Validation, Report, Maintenance.

## Revision and validation checklist
| Requirement | Status | Evidence in revised deck |
|---|---:|---|
| Cover slide included | Pass | The deck begins with `## Cover` containing only title, subtitle, and course/presenter information. |
| 40–60 slide target | Pass | The revised deck contains 1 cover plus 44 numbered slides, for 45 total slide items. |
| Non-redundant topic focus | Pass | The deck was reduced from 52 numbered slides to 44 and organized only around the four required Day 4 outcomes. |
| Section transition slides | Pass | Slides 4, 13, 24, 34, and 42 are minimal transition slides. |
| Arrow-style teaching flow | Pass | Slide 2 uses `Plan → Capture → Log → Package → Validate → Report`, and several content diagrams use arrow workflows. |
| Debugging habits | Pass | Slides 22 and 40 consolidate debugging habits without repeated standalone explanations. |
| Evidence habits | Pass | Slides 3, 30, 32, 38, and 39 teach evidence standards only where required by Day 4 work. |
| Validation gates | Pass | Slides 14, 23, and 39 use validation as mock-readiness and report-readiness gates. |
| Simulation-to-hardware handoff | Pass | Slides 14 and 15 establish mock/Gazebo rehearsal before B2 hardware execution. |
| Field-testing discipline | Pass | Slides 25–33 cover field roles, readiness, capture timing, verification, logging, notes, and fallbacks. |
| Diagram cues for every content slide | Pass | Every non-transition slide includes a specific visual cue using maps, pipelines, tables, dashboards, timelines, checklists, or decision trees. |
| Vinci AI styling guidance | Pass | Teaching design notes specify background, typography, rule systems, logo, watermark, and copyright requirements. |

## Updated Day 4 outcome coverage evaluation
| Updated outcome | Coverage | Supporting slides | Rationale |
|---|---:|---|---|
| Navigation through complex, rugged terrains and processing multi-sensor arrays | 100% | Slides 4–12 | This section directly covers rugged terrain effects, bounded navigation, SLAM, costmaps, obstacle supervision, sensor roles, timing alignment, and SportModeState telemetry context. |
| Building functional inspection scripts for mock simulated scenarios | 100% | Slides 13–23 | This section directly covers mock-first workflow, Gazebo rehearsal, procedural scripts, metadata and patrol plans, camera capture, OpenCV-derived outputs, JSONL logging, bounded motion, debugging, and validation readiness. |
| Field Work: Real-world mock inspection execution, sensor capture, and telemetry logging with the B2 | 100% | Slides 24–33 | This section directly covers B2 field roles, readiness, stable capture, RTSP verification, continuous telemetry logging, checkpoint mapping, field notes, immediate verification, and fallbacks. |
| Data Visualization: Extracting logs, parsing payload data, report generation, and B2 hardware maintenance walkthroughs | 100% | Slides 34–41 | This section directly covers log parsing, motion timelines, payload data context, artifact-backed report claims, validation, debugging, and post-run B2 maintenance. |

Overall coverage is assessed at **100%**. Redundancy was reduced by merging broad evidence explanations into the specific navigation, scripting, field execution, validation, reporting, and maintenance moments where they are needed.

## References
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
