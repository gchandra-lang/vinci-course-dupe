#!/usr/bin/env python3
"""
Day 05 Data Enrichment — Apply semantic emoji prefixes, risk markers, diagram
placeholders, and platform icons to the syllabus.json Day 05 slides.

All enrichments are PLAIN TEXT — no HTML tags. The CSS classes in index.css
are applied by the Home.tsx semanticClass() classifier based on keyword matching.
"""
import json, os, re

OUT = os.path.join(os.path.dirname(__file__), "syllabus.json")

with open(OUT) as f:
    syllabus = json.load(f)

d5 = syllabus["05"]
slides = d5["slides"]

# ── Emoji mapper for first-column table cells ──
EMOJI_TABLE = {
    # Platforms
    "Go2": "🐕 ", "B2": "🏭 ", "G1": "🤖 ",
    "Days 1–2": "🐕 ", "Days 3–4": "🏭 ", "Days 5–7": "🤖 ",
    # Communication lanes
    "Subscribe": "📥 ", "Publish": "📤 ", "RPC": "🔁 ",
    # Risk
    "Low": "🟢 ", "Medium": "🟡 ", "High": "🔴 ",
    # Readiness
    "Healthy Operation": "✅ ", "DDS Issue": "❌ ", "FSM in Damp": "❌ ",
    "Ownership Conflict": "❌ ", "In Transition": "⚠️ ", "Network Only": "❌ ",
    # Architecture
    "Physical Ethernet": "🔌 ", "DDS Communication": "📡 ",
    "State Topic": "📊 ", "High-Level RPC": "🔁 ",
    "Low-Level Command": "⚙️ ", "Perception/Video": "👁️ ",
    # FSM states
    "0": "0️⃣ ", "1": "1️⃣ ", "3": "3️⃣ ", "500": "5️⃣0️⃣0️⃣ ",
    "702": "7️⃣0️⃣2️⃣ ", "706": "7️⃣0️⃣6️⃣ ",
    # Check types
    "Repository Location": "📁 ", "SDK Environment": "🐍 ",
    "Interface Discovery": "🔌 ", "Robot Reachability": "📶 ",
    "DDS Readiness": "⚙️ ",
    # Outcomes
    "G1 Hardware Architecture": "🏗️ ", "DDS Communication Model": "📡 ",
    "rt/lowstate Interpretation": "📊 ", "FSM Read-Only Inspection": "🔍 ",
    "Readiness Classification": "✅ ",
    # Symptoms
    "SDK import fails.": "🐍 ", "ping fails.": "📶 ",
    "Lowstate subscription produces no output.": "📡 ", "Lowstate prints but tick does not increment.": "⏱️ ",
    "CheckMode returns unexpected ownership.": "👥 ", "mode_machine shows unexpected value.": "⚠️ ",
    # Lab record fields
    "Day & Date": "📅 ", "Operator / Team": "👤 ",
    "Interface Name": "🔌 ", "SDK Environment": "🐍 ",
    "CyclerDDS Version": "⚙️ ", "Robot IP": "📶 ",
    "rt/lowstate Fields Observed": "📊 ", "CheckMode Result": "🔍 ",
    "FSM Reading": "🔢 ", "Readiness Classification": "✅ ",
    "Safety Perimeter": "🛡️ ", "Next Steps": "➡️ ",
}

# ── Slide-specific enrichments ──

# Slide 1: Day 5 Position in the Course
# Enhance rows with platform emoji prefixes (already matched by key above)
# Add diagram placeholder to bottom_band
slides[0]["bottom_band"] = (
    "Day 5 is the single most important safety day in the course. If students cannot read "
    "rt/lowstate and classify readiness, they are not ready for any Day 6 command or Day 7 "
    "capstone motion. Observability is the foundation of humanoid operation.\n\n"
    "[DIAGRAM: Three-platform timeline — 🐕 Go2 (left, small quadruped) → 🏭 B2 (center, "
    "larger industrial quadruped) → 🤖 G1 (right, humanoid). A horizontal arrow labeled "
    "'SDK Pattern Transfer' runs beneath all three. A vertical dashed line drops from G1 "
    "with the label: 'Day 5 Gate — NO MOTION UNTIL OBSERVABILITY CONFIRMED.']"
)

# Enhance table rows
for row in slides[0]["board_data"]["rows"]:
    key = row[0]
    if key in EMOJI_TABLE:
        row[0] = EMOJI_TABLE[key] + key

# Slide 2: Learning Outcomes
slides[2]["bottom_band"] = (
    "Each segment must produce a written lab-record line — not just a conversation. The "
    "session ends with a complete student lab record covering environment, network, lowstate, "
    "FSM, and readiness classification."
)

# Slide 5: Communication Model — Three Lanes
# Add emoji prefixes to row headers
for row in slides[4]["board_data"]["rows"]:
    key = row[0]
    if key in EMOJI_TABLE:
        row[0] = EMOJI_TABLE[key] + key
    # Color risk level
    if "Low" in row[3]:
        row[3] = "🟢 Low — observation only"
    elif "Medium" in row[3]:
        row[3] = "🟡 Medium — can affect behaviour"

# Add diagram
slides[4]["bottom_band"] = (
    "Every Day 5 script should be classified by lane before it is run. The instructor should "
    "verify: 'This script subscribes only — it observes. Run it.' Or: 'This script publishes "
    "— we are not running that today.' This builds the habit of risk-aware operation.\n\n"
    "[DIAGRAM: Three vertical columns side by side. LEFT (green tint): 'Subscribe' — PC icon "
    "with downward arrows labeled 'rt/lowstate data flows in → PC receives passively.' CENTER "
    "(amber tint): 'Publish' — PC icon with upward arrows labeled 'Command data flows out → "
    "Robot acts.' RIGHT (purple tint): 'RPC' — PC icon with bidirectional arrows labeled "
    "'Request sent → Robot responds with result.' A large ✖ over the center & right columns: "
    "'Day 5: OBSERVE ONLY — No Publish, Read-Only RPCs.']"
)

# Slide 3: Teaching Plan — SKIP (it's a schedule, but user said no schedules)
# Actually keep it — it's already in the data and has important content

# Slide 4: G1 Hardware — grid, no table rows to enhance
# Add diagram
slides[3]["bottom_band"] += (
    "\n\n[DIAGRAM: Frontal outline of 🤖 G1 humanoid with 6 callout lines: head (🧠 Jetson "
    "Orin NX + 👁️ Depth Camera), torso (🔬 LiDAR sensor), arms (🔴 DOF variant callout — "
    "arm5 vs arm7 with joint count), legs (🦿 motion DOFs), feet (⚖️ stability envelope), "
    "full-body bounding box (1320×450×200 mm with exclusion zone radius). Each callout uses "
    "the same color as its corresponding grid card.]"
)

# Slide 6: Environment Setup
for row in slides[5]["board_data"]["rows"]:
    key = row[0]
    if key in EMOJI_TABLE:
        row[0] = EMOJI_TABLE[key] + key

slides[5]["bottom_band"] += (
    "\n\n[DIAGRAM: Vertical diagnostic ladder with 5 rungs. Bottom rung (1): 📁 file folder "
    "→ scripts found? Rung 2: 🐍 Python snake → import works? Rung 3: 🔌 Ethernet plug → "
    "interface named? Rung 4: 📶 ping waves → robot responds? Rung 5: ⚙️ gear → DDS configured? "
    "Arrow ascends the ladder: 'Narrow uncertainty — each rung gates the next.' All rungs "
    "turn 🟢 green only when confirmed; 🔴 red if missing.]"
)

# Slide 8: rt/lowstate subscription
for row in slides[7]["board_data"]["rows"]:
    key = row[0]
    if key in EMOJI_TABLE:
        row[0] = EMOJI_TABLE[key] + key
    elif "tick" in row[0].lower():
        row[0] = "⏱️ " + row[0]
    elif "motor" in row[0].lower():
        row[0] = "🔢 " + row[0]
    elif "imu" in row[0].lower():
        row[0] = "🧭 " + row[0]
    elif "message rate" in row[0].lower():
        row[0] = "📶 " + row[0]

# Slide 9: Interpreting lowstate
for row in slides[8]["board_data"]["rows"]:
    # Add semantic markers to observation column
    if "damp" in row[0].lower():
        row[0] = "🔴 " + row[0]
    elif "start" in row[0].lower() and "500" in row[0]:
        row[0] = "🟡 " + row[0]
    elif "incrementing" in row[0].lower():
        row[0] = "🟢 " + row[0]
    elif "near-level" in row[0].lower():
        row[0] = "🟢 " + row[0]
    elif "count matches" in row[0].lower():
        row[0] = "🟢 " + row[0]

# Slide 10: FSM API values
for row in slides[9]["board_data"]["rows"]:
    api_id = row[0]
    if api_id in EMOJI_TABLE:
        row[0] = EMOJI_TABLE[api_id] + api_id

# Slide 11: FSM Reference Card
for row in slides[10]["board_data"]["rows"]:
    fsm_val = row[0]
    if fsm_val in EMOJI_TABLE:
        row[0] = EMOJI_TABLE[fsm_val] + fsm_val
    # Color the classification cell
    if "FAIL" in row[3]:
        row[3] = "🔴 FAIL"
    elif "PARTIAL" in row[3]:
        row[3] = "🟡 PARTIAL"
    elif "READY" in row[3]:
        row[3] = "🟢 READY"

slides[10]["bottom_band"] += (
    "\n\n[DIAGRAM: FSM state transition graph — 6 nodes arranged left to right. 🔴 Zero Torque "
    "(0) → 🔴 Damp (1) → 🟡 Lie-to-Stand (702) → 🟡 Sit (3) → 🟡 Start (500) → 🟢 Squat/Stand "
    "(706). Arrows show permitted transitions. Large ❌ over states 0 and 1 labeled 'MOTION "
    "BLOCKED.' ⚠️ over transitional states 702/500 labeled 'WAIT FOR STABILITY.' ✅ over 706 "
    "labeled 'MOTION-READY (pending other gates).']"
)

# Slide 12: Readiness Classification
for row in slides[11]["board_data"]["rows"]:
    name = row[0]
    if name in EMOJI_TABLE:
        row[0] = EMOJI_TABLE[name] + name
    cls = row[7]
    if cls == "READY":
        row[7] = "🟢 READY"
    elif cls == "FAIL":
        row[7] = "🔴 FAIL"
    elif cls == "PARTIAL":
        row[7] = "🟡 PARTIAL"

# Slide 13: G1 vs Go2/B2 transfer errors
for row in slides[12]["board_data"]["rows"]:
    row[0] = "⚠️ " + row[0]

# Slide 14: Troubleshooting
for row in slides[13]["board_data"]["rows"]:
    key = row[0]
    if key in EMOJI_TABLE:
        row[0] = EMOJI_TABLE[key] + key

# Slide 15: Lab Record Template
for row in slides[14]["board_data"]["rows"]:
    key = row[0]
    if key in EMOJI_TABLE:
        row[0] = EMOJI_TABLE[key] + key

# Slide 16: Knowledge Check — list, no table rows
# Add diagram
slides[15]["bottom_band"] = (
    "Present a readiness scenario: 'Environment passes, ping passes, lowstate streams but "
    "mode_machine=1.' Classification: FAIL (damp detected). Correct response: 'The robot is "
    "damped — motion is blocked. We must investigate why damping is active before any further "
    "action.' This tests judgment, not trivia.\n\n"
    "[DIAGRAM: Decision flowchart — 6 readiness gates (📁 Repository → 🐍 Environment → 🔌 "
    "Interface → 📶 Ping → 📊 Lowstate → 🔍 FSM). All 6 feed into a single classifier node "
    "labeled 'Readiness Decision.' Three outputs: 🟢 READY (all gates green), 🟡 PARTIAL "
    "(transitional FSM or unknown field), 🔴 FAIL (any gate red). Example path highlighted: "
    "'Lowstate streams but FSM=damp → 🔴 FAIL — investigate damping root cause.']"
)

# Slide 17: Day 6 Preview — grid
slides[16]["bottom_band"] += (
    "\n\n[DIAGRAM: Bridge arch from Day 5 to Day 6. Left pillar labeled 'Day 5 Deliverables' "
    "— 🟢 READY classification, 📊 Lowstate streaming, 🔍 FSM inspection, 📋 Complete lab "
    "record. Right pillar labeled 'Day 6 Entry Gates' — 🚶 WaveHand first, 🦾 Arm actions "
    "(face wave → shake hand → high five), 📡 Arm SDK streaming (advanced). Arch keystone: "
    "'ONLY ONE COMMAND PATH AT A TIME.' Bridge deck: 'Observability → Classification → "
    "Readiness → Controlled Motion.']"
)

# ── Apply emoji prefixes to ALL table first-column cells ──
for slide in slides:
    if slide["board_type"] == "table":
        for row in slide["board_data"]["rows"]:
            key = row[0]
            if key in EMOJI_TABLE:
                row[0] = EMOJI_TABLE[key] + key

# ── Save ──
with open(OUT, "w") as f:
    json.dump(syllabus, f, indent=2, ensure_ascii=False)

print("✅ Day 05 data enrichment complete — emoji prefixes, risk markers, diagram placeholders applied.")
print(f"   {len([s for s in slides if '[DIAGRAM:' in s['bottom_band']])} slides now contain diagram placeholders.")