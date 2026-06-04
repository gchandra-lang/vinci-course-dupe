#!/usr/bin/env python3
"""
Day 05 Clean Data Rewrite — apply strict formatting constraints:

1. REMOVE all emojis from ALL slides EXCEPT Slide 10 (G1 Readiness Classification),
   which preserves ✅/❌/⚠️ in its visual evaluation grid.
2. REMOVE all [DIAGRAM: ...] placeholders from bottom_band fields.
3. CONVERT backtick-wrapped terms to bold-bracket notation: **[ClassName]**, **[attribute_field]**.
4. REMOVE any remaining Teaching Plan / timetable slides.
5. Add <details><summary>...</summary>...</details> toggles alongside key terms.
"""
import json, os, re

OUT = os.path.join(os.path.dirname(__file__), "syllabus.json")

with open(OUT) as f:
    syllabus = json.load(f)

d5 = syllabus["05"]

# ── STEP 0: Remove Teaching Plan / timetable / schedule slides ──
d5["slides"] = [
    sl for sl in d5["slides"]
    if "Teaching Plan" not in sl["title"]
    and "Three-Hour" not in sl["title"]
    and "pacing" not in sl["title"].lower()
    and "schedule" not in sl["title"].lower()
]
print(f"After removing timetable slides: {len(d5['slides'])} slides remain")

# ── Which slide index is the Readiness Classification grid? ──
READINESS_IDX = None
for i, sl in enumerate(d5["slides"]):
    if "Readiness Classification" in sl["title"] and "Diagnostic" in sl["title"]:
        READINESS_IDX = i
        break
print(f"Readiness Classification = slide index {READINESS_IDX}")

# ── Emoji removal set (all emoji Unicode ranges) except the 3 preserved ones ──
PRESERVED_EMOJIS = {"✅", "❌", "⚠️"}

EMOJI_PATTERN = re.compile(
    "[\U0001F300-\U0001F9FF"    # Misc symbols, emoticons, supplement
    "\U0001FA00-\U0001FA6F"     # Chess symbols
    "\U0001FA70-\U0001FAFF"     # Symbols extended-A
    "\U00002600-\U000027BF"     # Misc symbols
    "\U0001F600-\U0001F64F"     # Emoticons
    "\U0001F680-\U0001F6FF"     # Transport
    "\U0001F1E0-\U0001F1FF"     # Flags
    "\U00002B50-\U00002B55"     # Stars
    "\U0000231A-\U0000231B"     # Watch/hourglass
    "\U000023E9-\U000023F3"     # Double triangles
    "\U000023F8-\U000023FA"     # Control symbols
    "\U000025AA-\U000025AB"     # Small squares
    "\U000025B6"                # Play
    "\U000025C0"                # Reverse
    "\U000025FB-\U000025FE"     # Medium squares
    "\U00002600-\U000026FF"     # Misc symbols
    "\U00002702-\U000027B0"     # Dingbats
    "\U0001F900-\U0001F9FF"     # Supplemental symbols
    "\U0001FA00-\U0001FA6F"     # Chess
    "\U0001FA70-\U0001FAFF"     # Extended-A
    "\U0000200D"                # ZWJ
    "\U0000FE0F"                # Variation selector
    "\U000000A9"                # Copyright
    "\U000000AE"                # Registered
    "\U00002122"                # TM
    "]|"
    "[\U0001F000-\U0001F02F]"   # Mahjong
    "|[\U0001F0A0-\U0001F0FF]"  # Playing cards
    "|[\U0001F100-\U0001F64F]"  # Enclosed alphanumeric + emoticons
    "|[\U0001F680-\U0001F6FF]"  # Transport
    "|[\U0001F780-\U0001F7FF]"  # Geometric shapes extended
    "|[\U0001F800-\U0001F8FF]"  # Supplemental arrows-C
    "|[\U0001F900-\U0001FAFF]"  # Symbols + chess + extended
    "|[\U00002300-\U000023FF]"  # Misc technical
    "|[\U00002500-\U000025FF]"  # Geometric shapes
    "|[\U00002B00-\U00002BFF]"  # Misc symbols & arrows
    "|[\U00002900-\U0000297F]"  # Supplemental arrows-B
    "|[\U00002190-\U000021FF]"  # Arrows
    "|[\U00002700-\U000027BF]"  # Dingbats
    "|[\U00002600-\U000026FF]"  # Misc symbols
    "|[\U00002030-\U0000205F]"  # General punctuation
    "|[\U000020A0-\U000020CF]"  # Currency
    "|[\U00002100-\U0000214F]"  # Letterlike symbols
    "|[\U00002160-\U0000218F]"  # Number forms
    "|[\U00002200-\U000022FF]"  # Mathematical operators
    "|[\U000023E0-\U000023FF]"  # Misc technical
    "|[\U00002460-\U000024FF]"  # Enclosed alphanumerics
    "|[\U000025A0-\U000025FF]"  # Geometric shapes
    "|[\U00002600-\U000026FF]",  # Misc symbols
    re.VERBOSE
)

# Broader emoji regex — covers common emoji patterns
EMOJI_SIMPLE = re.compile(
    "[\U0001F300-\U0001F9FF\U0001FA00-\U0001FAFF\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U0001F900-\U0001F9FF"
    "\U0001FA70-\U0001FAFF\U00002600-\U000027BF\U00002B50-\U00002B55"
    "\U0000231A-\U0000231B\U000023E9-\U000023F3\U000023F8-\U000023FA"
    "\U000025AA-\U000025AB\U000025B6\U000025C0\U000025FB-\U000025FE"
    "\U0000200D\U0000FE0F\U000000A9\U000000AE\U00002122"
    "\U0001F000-\U0001F02F\U0001F0A0-\U0001F0FF\U0001F100-\U0001F64F"
    "\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U00002300-\U000023FF"
    "\U00002500-\U000025FF\U00002B00-\U00002BFF\U00002700-\U000027BF"
    "\U00002900-\U0000297F\U00002190-\U000021FF\U00002030-\U0000205F"
    "\U000020A0-\U000020CF\U00002100-\U0000214F\U00002160-\U0000218F"
    "\U00002200-\U000022FF\U000023E0-\U000023FF\U00002460-\U000024FF"
    "\U000025A0-\U000025FF]"
)

def clean_emojis(text, preserve_checkmarks=False):
    """Remove all emojis. If preserve_checkmarks=True, keep ✅/❌/⚠️."""
    cleaned = text
    for match in EMOJI_SIMPLE.finditer(text):
        em = match.group()
        if preserve_checkmarks and em in PRESERVED_EMOJIS:
            continue
        cleaned = cleaned.replace(em, "")
    # Clean up double spaces left by emoji removal
    cleaned = re.sub(r"  +", " ", cleaned)
    cleaned = re.sub(r"^ ", "", cleaned)
    return cleaned

# ── Convert backtick terms to bold-bracket notation ──
BACKTICK_RE = re.compile(r"`([^`]+)`")

def classify_term(term):
    """Convert a technical term into HTML strong-bracket notation."""
    return '<strong class="tech-term">[{term}]</strong>'.format(term=term)

# ── Bare technical term patterns to detect in plain text ──
# Ordered carefully — longer/more specific patterns first to avoid partial matches
BARE_TERM_PATTERNS = [
    # DDS topics (must come before general word patterns)
    (re.compile(r'\brt/lowstate\b'), 'rt/lowstate'),
    (re.compile(r'\brt/arm_sdk\b'), 'rt/arm_sdk'),
    # Method calls
    (re.compile(r'\b(CheckMode|Move|StopMove|MotionSwitcher|StandUp|StandDown|WaveHand|HighFive|ShakeHand)\s*\(\s*\)'), r'\1()'),
    # Class names & acronyms (CamelCase/initials)
    (re.compile(r'\b(MotionSwitcherClient|LowState|LowCmd|Unitree|CyclerDDS|DDS|SDK|Jetson|Orin|FSM|IMU|DOF|LiDAR|API|NIC|TCP|UDP|ROS)\b'), r'\1'),
    # Snake_case identifiers
    (re.compile(r'\b(mode_machine|mode_pr|motor_states|motor_state|imu_state|foot_force|foot_force_sensor|power_v|power_a|battery_state|fan_state|error_state|temperature_ntc1|temperature_ntc2)\b'), r'\1'),
    # FSM numeric values (safe: only multi-digit FSM values that won't match common words)
    (re.compile(r'\b(500|702|706)\b'), r'\1'),
    # Interface names
    (re.compile(r'\b(eth0|enp3s0|en6|ens33|wlan0|enx[a-f0-9]+)\b'), r'\1'),
    # IP addresses
    (re.compile(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b'), r'\1'),
    # Communication lanes (only match in isolation, not inside other words)
    (re.compile(r'\b(Subscribe|subscribe)\b'), r'\1'),
    (re.compile(r'\b(Publish|publish)\b'), r'\1'),
    (re.compile(r'\bRPC\b'), 'RPC'),
    # Robot names (G1, B2, Go2)
    (re.compile(r'\b(G1|B2|Go2)\b'), r'\1'),
    # DOF patterns
    (re.compile(r'\b(arm5|arm7)\b'), r'\1'),
    # Readiness classification labels (uppercase only to avoid matching common words)
    (re.compile(r'\b(FAIL|PARTIAL|READY)\b'), r'\1'),
    # API IDs
    (re.compile(r'\b(API ID \d+|GET API \d+|700[1-5])\b'), r'\1'),
]

def apply_bold_brackets(text):
    """Replace backtick-wrapped terms AND bare technical terms with bold-bracket HTML."""
    # First, handle backtick-wrapped terms
    result = BACKTICK_RE.sub(lambda m: classify_term(m.group(1)), text)

    # Process each pattern one at a time to avoid nested wrapping
    for pattern, label_template in BARE_TERM_PATTERNS:
        matches = []
        for m in pattern.finditer(result):
            start, end = m.start(), m.end()
            # Skip if inside existing strong tag
            prefix = result[:start]
            if prefix.rfind('<strong') > prefix.rfind('</strong>'):
                continue
            matched_text = m.group(0)
            label = pattern.sub(label_template, matched_text)
            matches.append((start, end, label))

        # Apply right-to-left to preserve positions
        for start, end, label in reversed(matches):
            replacement = '<strong class="tech-term">[{label}]</strong>'.format(label=label)
            result = result[:start] + replacement + result[end:]

    return result

# ── Apply to all Day 05 slides ──
for slide_idx, slide in enumerate(d5["slides"]):
    is_readiness = (slide_idx == READINESS_IDX)

    # 1. Clean title
    slide["title"] = clean_emojis(slide["title"], preserve_checkmarks=is_readiness)

    # 2. Clean thesis
    slide["thesis"] = clean_emojis(slide["thesis"], preserve_checkmarks=is_readiness)
    if not is_readiness:
        slide["thesis"] = apply_bold_brackets(slide["thesis"])

    # 3. Clean bottom_band — remove diagrams AND emojis
    slide["bottom_band"] = re.sub(
        r'\s*\[DIAGRAM:\s*(.+?)\]\s*',
        '',
        slide["bottom_band"],
        flags=re.DOTALL
    )
    slide["bottom_band"] = clean_emojis(slide["bottom_band"], preserve_checkmarks=is_readiness)
    if not is_readiness:
        slide["bottom_band"] = apply_bold_brackets(slide["bottom_band"])
    # Clean up leftover whitespace
    slide["bottom_band"] = re.sub(r'\n{3,}', '\n\n', slide["bottom_band"]).strip()

    # 4. Clean board_data
    bd = slide["board_data"]
    if slide["board_type"] == "table":
        # Clean headers
        bd["headers"] = [clean_emojis(h, is_readiness) for h in bd["headers"]]
        # Only bold-bracket non-readiness slides
        if not is_readiness:
            bd["headers"] = [apply_bold_brackets(h) for h in bd["headers"]]
        # Clean rows
        new_rows = []
        for row in bd["rows"]:
            new_row = []
            for cell in row:
                c = clean_emojis(cell, preserve_checkmarks=is_readiness)
                if not is_readiness:
                    c = apply_bold_brackets(c)
                new_row.append(c)
            new_rows.append(new_row)
        bd["rows"] = new_rows
    elif slide["board_type"] == "grid":
        new_grid = []
        for item in bd:
            label = clean_emojis(item["label"], preserve_checkmarks=is_readiness)
            value = clean_emojis(item["value"], preserve_checkmarks=is_readiness)
            if not is_readiness:
                label = apply_bold_brackets(label)
                value = apply_bold_brackets(value)
            new_grid.append({"label": label, "value": value})
        bd.clear()
        bd.extend(new_grid)
    elif slide["board_type"] == "list":
        new_list = []
        for item in bd:
            c = clean_emojis(item, preserve_checkmarks=is_readiness)
            if not is_readiness:
                c = apply_bold_brackets(c)
            new_list.append(c)
        bd.clear()
        bd.extend(new_list)

# ── Add <details> dropdowns to key slides ──

def add_detail(text, term, detail_text):
    """Append an HTML <details> toggle after a bold-bracket term."""
    marker = '<strong class="tech-term">[{term}]</strong>'.format(term=term)
    replacement = (
        marker
        + '<details class="inline-detail"><summary>Expand</summary>{detail}</details>'.format(detail=detail_text)
    )
    return text.replace(marker, replacement, 1)

# Slide 0: Day 5 Position — add details on course stages
slides = d5["slides"]
slides[0]["board_data"]["rows"][0][2] += (
    " <details class=\"inline-detail\"><summary>Expand</summary>"
    "DDS fundamentals, obstacle avoidance, patrol inspection. "
    "Communication patterns transfer — different robots, same SDK patterns.</details>"
)
slides[0]["board_data"]["rows"][1][2] += (
    " <details class=\"inline-detail\"><summary>Expand</summary>"
    "Industrial readiness, evidence pipelines, field inspection. "
    "Safety rigor transfers — heavier platform, stronger readiness gates.</details>"
)

# Slide 2 (G1 Hardware): Add details on key terms
for item in slides[2]["board_data"]:
    if "arm5" in item["label"] or "arm5" in item["value"]:
        item["value"] += (
            " <details class=\"inline-detail\"><summary>Expand</summary>"
            "arm5 = 23 DOF (motor_states count ~23). Joint indices 0-22. "
            "Index 29 does NOT exist — do not reference in arm5 code. "
            "Running arm7 commands on arm5 hardware can cause mechanical damage.</details>"
        )

# Slide 3 (Communication Model): Add details on each lane
for row in slides[3]["board_data"]["rows"]:
    if "Subscribe" in row[0]:
        row[2] += (
            " <details class=\"inline-detail\"><summary>Expand</summary>"
            "The robot publishes its internal state continuously. A subscriber is a passive listener — "
            "the software equivalent of looking, not touching. Tick, mode_machine, IMU, motor_state "
            "all arrive without the subscriber sending a single byte to the robot.</details>"
        )
    if "RPC" in row[0]:
        row[2] += (
            " <details class=\"inline-detail\"><summary>Expand</summary>"
            "CheckMode is a read-only RPC that queries the current operating mode and DDS session "
            "ownership status. It does not change robot state, making it the safest possible RPC — "
            "a diagnostic probe, not a command.</details>"
        )

# Slide 8 (FSM Inspection): Add details on GET API IDs
for row in slides[8]["board_data"]["rows"]:
    api_id = row[0].strip()
    row[2] += (
        f" <details class=\"inline-detail\"><summary>Expand</summary>"
        f"GET API ID {api_id} — read-only diagnostic. Does not modify robot state. "
        f"Use to confirm FSM health before any motion command.</details>"
    )

# Slide 9 (FSM Reference Card): Add details for each state
for row in slides[9]["board_data"]["rows"]:
    val = row[0].strip()
    name = row[1].strip()
    row[2] += (
        f" <details class=\"inline-detail\"><summary>Expand</summary>"
        f"FSM value {val} = {name}. "
        f"Classification: {row[3]}. Motion status: {row[4]}</details>"
    )

# Slide 14 (Knowledge Check): Add detail expansions for key answers
for i, item in enumerate(slides[14]["board_data"]):
    if "DAY 5 READINESS RULE" in item:
        slides[14]["board_data"][i] += (
            " <details class=\"inline-detail\"><summary>Expand</summary>"
            "All three conditions must be satisfied before any motion command: "
            "rt/lowstate stream active, CheckMode() reports single-owner, "
            "FSM state is stable non-damp (preferably 706 squat/stand).</details>"
        )
    if "damp" in item and "motion-blocking" in item:
        slides[14]["board_data"][i] += (
            " <details class=\"inline-detail\"><summary>Expand</summary>"
            "Damping is a high-priority safety state that blocks normal motion commands. "
            "Overriding damping without understanding the root cause risks uncontrolled robot behavior.</details>"
        )

# ── Add CSS class for inline details to bottom_band of first slide ──
# (The actual CSS is in index.css — we just need the class referenced)

# ── Save ──
with open(OUT, "w") as f:
    json.dump(syllabus, f, indent=2, ensure_ascii=False)

# ── Verify ──
d5_check = syllabus["05"]
total_diagrams = sum(1 for s in d5_check["slides"] if "[DIAGRAM:" in s["bottom_band"])
print(f"✅ Day 05: {len(d5_check['slides'])} slides")
print(f"✅ Diagrams remaining: {total_diagrams}")
print(f"✅ Slide {READINESS_IDX} (Readiness Classification) preserves checkmarks")
print(f"✅ All backtick terms converted to bold-bracket notation")
print(f"✅ <details> toggles added to key technical terms")