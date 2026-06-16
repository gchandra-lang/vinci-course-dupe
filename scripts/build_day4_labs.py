#!/usr/bin/env python3
"""
Build enhanced Day 04 lab workspace entries in syllabus.json,
matching the rich HTML format of Day 01 labs.

Day 04: B2 Rugged Inspection, Mock Scripts, Field Capture,
Telemetry, Reporting, and Maintenance.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SYLLABUS_PATH = REPO / "client" / "src" / "data" / "syllabus.json"


# ── Lab 00: Inspection Scenario & Run Folder ─────────────────────────────

def build_lab00() -> dict:
    content = """<div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5 text-xs mb-4 p-3 bg-muted/30 border border-border/60 rounded-lg"><div class="flex gap-2"><span class="font-semibold text-foreground">Platform:</span><span>Unitree B2</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Duration:</span><span>~40 min (20 min schema theory + 20 min hands-on build)</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Robot required:</span><span>No (mock workflow only)</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Motion:</span><span>None</span></div></div>

<div class="border border-primary/30 bg-primary/5 rounded-lg p-4 mb-6"><div class="flex items-center gap-2 mb-3"><span class="text-base">🎯</span><span class="text-sm font-bold text-foreground tracking-tight">Learning Objectives</span></div><ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Adapt the Day 2 <span class="font-bold text-foreground">run-folder schema</span> for B2, adding <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">robot_platform</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">robot_id</code>, and <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">interface</code> fields.</li><li>Author <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">metadata.json</code> and <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">patrol_plan.json</code> that set <span class="font-bold text-foreground">inspection intent</span> before any robot motion.</li><li>Build the complete <span class="font-bold text-foreground">folder scaffold</span>: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">checkpoints/</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">raw_captures/</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">logs/</code>.</li><li>Pass the <span class="font-bold text-foreground">validator gate</span> — structural PASS required before the B2 handoff gate.</li></ol></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">PDF coverage: Run-folder design · inspection scenario planning · mock-first workflow · validation readiness gates.</p>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Prerequisites: Day 03 Labs 0–2 complete (B2 telemetry + SportClient familiarity).</p>

<div class="border border-amber-500/40 bg-amber-500/10 rounded-lg p-3 mb-4"><span class="font-semibold text-amber-600 dark:text-amber-400 text-xs uppercase tracking-wide">Day 4 Rule</span><p class="text-xs text-muted-foreground leading-relaxed mt-1"><span class="font-bold text-foreground">Mock first, then hardware.</span> The mock scenario must pass validation and receive instructor approval before the B2 leaves its standby position. Hardware begins only after the mock workflow and folder structure are understandable enough for approval.</p></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Concepts — The Six-Box Inspection Workflow</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Day 4 is organized around one repeated workflow. Every activity connects to one step:</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">Plan → Capture → Log → Package → Validate → Report</pre>

<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Step</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">This Lab</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Artifact</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Plan</span></td><td class="p-2.5"><span class="font-bold text-foreground">Lab 0</span> — Define scenario, checkpoints, route, capture targets, roles</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">metadata.json</code> + <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">patrol_plan.json</code></td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Capture</span></td><td class="p-2.5">Lab 1 — Execute camera stills and RTSP clips at designated checkpoints</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">frame.jpg</code> per checkpoint</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Log</span></td><td class="p-2.5">Lab 2 — Record SportModeState continuously from pre-motion through final notes</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">sportmodestate.jsonl</code></td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Package</span></td><td class="p-2.5"><span class="font-bold text-foreground">Lab 0</span> — Organize into standard run folder</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">run_YYYYMMDD_HHMM/</code></td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Validate</span></td><td class="p-2.5">Lab 2 — Run validator; PASS → proceed; FAIL → repair</td><td class="p-2.5">Validator output</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Report</span></td><td class="p-2.5">Lab 2 — Artifact-backed claims with telemetry context and limitations</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">field_report.md</code></td></tr></tbody></table>

<div class="border-l-2 border-primary pl-3 py-1 mb-3 text-xs text-foreground italic">Workflow check: Can you draw the six boxes — Plan → Capture → Log → Package → Validate → Report — and name one concrete artifact produced at each step? If not, drill that step before the field run.</div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">B2 Run-Folder Schema</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Adapted from Day 2's schema with B2-specific additions:</p>

<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">run_YYYYMMDD_HHMM/
  metadata.json           # who, when, robot_platform: "B2", robot_id, interface, scenario
  patrol_plan.json        # checkpoints + legs (increment / velocity) + capture actions
  sportmodestate.jsonl    # one JSON object per line — full run window
  raw_captures/           # all original files, unmodified, timestamped
    front_cp01_20260604T091523Z.jpg
    rear_cp01_20260604T091523Z.jpg
    front_cp02_20260604T091847Z.jpg
    ...
  checkpoints/
    cp01/
      frame.jpg           # selected, verified evidence at this stop
    cp02/
      frame.jpg
  field_report.md         # claims + artifacts + telemetry context + limitations + confidence
  MAINTENANCE.md          # post-run hardware walkthrough</pre>

<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Field</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Purpose</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">B2 Addition?</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">robot_platform</code></td><td class="p-2.5">Always <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">"B2"</code> for Day 4</td><td class="p-2.5"><span class="font-bold text-foreground">Yes</span> — distinguishes from Go2 runs</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">robot_id</code></td><td class="p-2.5">Physical robot identifier (e.g. <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">"B2-lab-1"</code>)</td><td class="p-2.5"><span class="font-bold text-foreground">Yes</span> — traceability across fleet</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">interface</code></td><td class="p-2.5">NIC used (<code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">"eth0"</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">"en6"</code>)</td><td class="p-2.5"><span class="font-bold text-foreground">Yes</span> — reproducibility</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">raw_captures/</code></td><td class="p-2.5">All original files preserved unmodified</td><td class="p-2.5"><span class="font-bold text-foreground">Yes</span> — B2 has front + rear cameras</td></tr></tbody></table>

<div class="border-l-2 border-primary pl-3 py-1 mb-3 text-xs text-foreground italic">Rule: <span class="font-bold text-foreground">Plan before motion.</span> The run folder is the inspection contract — create it and draft metadata before the robot moves.</div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Scenario Files Set Inspection Intent</h4></div>

<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">File</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Question It Answers</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Key Fields</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">metadata.json</code></td><td class="p-2.5">Who, when, what robot, what scenario, under what conditions?</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">operator</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">created_utc</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">robot_platform</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">robot_id</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">scenario</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">interface</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">checkpoints</code></td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">patrol_plan.json</code></td><td class="p-2.5">What checkpoints matter? What legs between them? What capture actions? What speed limits?</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">checkpoints[]</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">legs[]</code> with <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">type</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">dx</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">dyaw</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">dwell_sec</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">capture_action</code></td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">Intent check: Before any capture, open <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">metadata.json</code> and <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">patrol_plan.json</code>. Can you read exactly what inspection targets are planned? If the plan is vague, the evidence will be vague.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Evidence Standard — The Four Elements</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Element</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Meaning</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Example</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">File</span></td><td class="p-2.5">The concrete artifact supporting a claim</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">checkpoints/cp01/frame.jpg</code></td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Timestamp</span></td><td class="p-2.5">When the observation occurred — aligned across sensors</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">2026-06-04T09:15:23Z</code></td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Checkpoint</span></td><td class="p-2.5">Where the observation occurred — named location ID</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">cp01</code> (front-left corner)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Context Note</span></td><td class="p-2.5">What the file cannot show — glare, occlusion, vibration, fallback</td><td class="p-2.5">"Direct sunlight from right side, slight washout on left edge"</td></tr></tbody></table>

<div class="border-l-2 border-primary pl-3 py-1 mb-3 text-xs text-foreground italic">Evidence test: "If someone disputes this inspection claim, what specific file, timestamp, checkpoint, and note would I show to defend it?" If you cannot answer all four, the claim is not yet evidence-backed.</div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Hands-On Steps</h4></div>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 1 — Design your inspection scenario</p>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">On paper or whiteboard, define:</p>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>3 checkpoints (cp01, cp02, cp03) with clear physical markers</li><li>Inspection target at each checkpoint (what are you inspecting?)</li><li>Route between checkpoints — straight legs, turns, distances</li><li>Capture plan: front camera, rear camera, or both at each stop</li><li>Safety perimeter and known hazards</li></ul>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 2 — Author metadata.json</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">{
  "schema_version": 1,
  "created_utc": "2026-06-04T09:00:00Z",
  "operator": "Your Name",
  "team_name": "Team A",
  "robot_platform": "B2",
  "robot_id": "B2-lab-1",
  "interface": "eth0",
  "scenario": "Visual inspection of mock equipment bay — 3 checkpoints",
  "checkpoints": ["cp01", "cp02", "cp03"]
}</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 3 — Author patrol_plan.json</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">{
  "checkpoints": [
    {"id": "cp01", "label": "Equipment Bay Left", "marker": "red cone"},
    {"id": "cp02", "label": "Control Panel Center", "marker": "yellow cone"},
    {"id": "cp03", "label": "Cable Run Right", "marker": "blue cone"}
  ],
  "motion_limits": {
    "max_forward_vx_mps": 0.2,
    "max_increment_dx_m": 0.4
  },
  "legs": [
    {"type": "increment", "dx": 0.4, "dyaw": 0.0, "dwell_sec": 3, "from_cp": "cp01", "to_cp": "cp02"},
    {"type": "increment", "dx": 0.0, "dyaw": 0.8, "dwell_sec": 2, "from_cp": "cp02", "to_cp": "cp03"}
  ]
}</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 4 — Build the folder scaffold</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">mkdir -p run_dry_team_a/{raw_captures,logs,checkpoints/{cp01,cp02,cp03}}
cp metadata.json run_dry_team_a/
cp patrol_plan.json run_dry_team_a/
echo "# Field Report — Team A" > run_dry_team_a/field_report.md
echo "# B2 Maintenance Notes" > run_dry_team_a/MAINTENANCE.md</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 5 — Instructor approval gate</p>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Present to instructor:</p>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Scenario is defined — checkpoints, route, capture targets are clear</li><li>Folder structure is correct — all required paths exist</li><li>Capture plan is clear — which cameras at which checkpoints</li><li>Validation rules are understood — what PASS / FAIL means</li></ul>

<div class="border border-amber-500/40 bg-amber-500/10 rounded-lg p-3 mb-4"><span class="font-semibold text-amber-600 dark:text-amber-400 text-xs uppercase tracking-wide">Gate Discipline</span><p class="text-xs text-muted-foreground leading-relaxed mt-2">"Our mock folder passed validation and the instructor approved handoff." If you cannot say this sentence truthfully, the B2 should not move.</p></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Day 4 Rules — Applied in This Lab</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><span class="font-bold text-foreground">Plan before motion</span> — create the run folder and draft metadata before the robot moves — the run folder is the inspection contract.</li><li><span class="font-bold text-foreground">Every inspection run must produce traceable evidence</span> — video stills, state logs, checkpoint mapping, and validation output — not just a "successful walk."</li><li><span class="font-bold text-foreground">Separate raw capture from checkpoint evidence</span> — raw captures are original files; checkpoint evidence is selected, named, and placed under <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">checkpoints/&lt;id&gt;/frame.jpg</code> with context.</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Deliverable</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">metadata.json</code> with all required B2-specific fields</li><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">patrol_plan.json</code> with checkpoints, legs, and capture actions</li><li>Complete <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">run_dry_team_*/</code> folder with correct structure</li><li>Instructor sign-off confirming the mock scenario passes the gate</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Next Lab</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3"><a href="../lab-01/" class="text-primary underline hover:text-primary/80">Lab 1 — Mock Inspection Video with B2 Cameras</a> — Capture front/back stills, record RTSP streams, verify file integrity, and derive OpenCV outputs.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">References</h4></div>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Day 2 run-folder schema: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">day-02/lab-01/</code></li><li>B2 camera script: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">vendor/unitree_sdk2_python/example/b2/camera_opencv.py</code></li><li>Day 4 thesis: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">day-04/README.md</code></li></ul>"""

    # Use existing placeholder as JSON template reference
    example_metadata = """{
  "schema_version": 1,
  "created_utc": "2026-06-04T09:00:00Z",
  "operator": "Your Name",
  "team_name": "Team A",
  "robot_platform": "B2",
  "robot_id": "B2-lab-1",
  "interface": "eth0",
  "scenario": "Visual inspection of mock equipment bay — 3 checkpoints",
  "checkpoints": ["cp01", "cp02", "cp03"],
  "artifacts": {
    "metadata": "metadata.json",
    "plan": "patrol_plan.json",
    "telemetry": "sportmodestate.jsonl",
    "report": "field_report.md"
  }
}"""

    return {
        "id": "lab-00",
        "title": "Inspection Scenario & Run Folder",
        "content": content,
        "code_files": [
            {"name": "example_b2_metadata.json", "code": example_metadata}
        ]
    }


# ── Lab 01: Mock Inspection Video — B2 Front & Back Cameras ──────────────

def build_lab01() -> dict:
    content = """<div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5 text-xs mb-4 p-3 bg-muted/30 border border-border/60 rounded-lg"><div class="flex gap-2"><span class="font-semibold text-foreground">Duration:</span><span>~35 min (15 min camera theory + 20 min hands-on)</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Robot required:</span><span>Yes — B2 powered with active camera services</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Motion:</span><span>None (mock capture only)</span></div></div>

<div class="border border-primary/30 bg-primary/5 rounded-lg p-4 mb-6"><div class="flex items-center gap-2 mb-3"><span class="text-base">🎯</span><span class="text-sm font-bold text-foreground tracking-tight">Learning Objectives</span></div><ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Use <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">VideoClient</code> to capture <span class="font-bold text-foreground">front and rear camera stills</span> from the B2.</li><li>Record and verify <span class="font-bold text-foreground">RTSP video streams</span> — confirm file size, playback, and scene match.</li><li>Produce <span class="font-bold text-foreground">derived OpenCV outputs</span> (edge detection, filtering) while preserving raw frames as the authoritative record.</li><li>Develop the <span class="font-bold text-foreground">immediate verification habit</span>: capture → open → label → place → confirm log → continue.</li></ol></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">Prerequisites: <a href="../lab-00/" class="text-primary underline hover:text-primary/80">Lab 0</a> complete (run folder scaffold + instructor approval).</p>

<div class="border border-amber-500/40 bg-amber-500/10 rounded-lg p-3 mb-4"><span class="font-semibold text-amber-600 dark:text-amber-400 text-xs uppercase tracking-wide">Capture Rule</span><p class="text-xs text-muted-foreground leading-relaxed mt-1">"The file saved successfully" is <span class="font-bold text-foreground">not</span> the same as "the file is usable evidence." Open every capture before leaving the checkpoint. A corrupt or misaimed frame discovered during reporting is too late to fix.</p></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Concepts — B2 Camera Sensors</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Each sensor channel answers a different inspection question. This lab focuses on the <span class="font-bold text-foreground">camera channels</span>:</p>

<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Sensor</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Question It Answers</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Artifact</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Report Use</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Front Camera</span></td><td class="p-2.5">What does the inspection target look like?</td><td class="p-2.5">Still image (<code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">frame.jpg</code>) or RTSP clip</td><td class="p-2.5">Primary visual evidence of target condition</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Rear Camera</span></td><td class="p-2.5">What is behind / around the robot?</td><td class="p-2.5">Still image or RTSP clip</td><td class="p-2.5">Contextual evidence — approach path, surrounding hazards</td></tr></tbody></table>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">VideoClient Capture Pattern</h4></div>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.video.video_client import VideoClient
import cv2, numpy as np, time

ChannelFactoryInitialize(0, "eth0")
client = VideoClient()
client.SetTimeout(3.0)
client.Init()

# Get one still frame
code, data = client.GetImageSample()
if code == 0:
    img = cv2.imdecode(np.frombuffer(bytes(data), np.uint8), cv2.IMREAD_COLOR)
    # Verify: is the image non-empty? Does it show the expected scene?
    cv2.imwrite("raw_captures/front_cp01_utc.jpg", img)
    print(f"Saved: {img.shape} — verify this opens correctly")
else:
    print(f"Capture failed with code {code} — check camera service")</pre>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Raw Frames vs Derived Outputs</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Type</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Status</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Path</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Modification</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Raw Frame</span></td><td class="p-2.5">Primary — authoritative record</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">raw_captures/front_cp01_utc.jpg</code></td><td class="p-2.5">Never modified — preserved exactly as captured</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Derived Output</span></td><td class="p-2.5">Secondary — highlights features</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">derived/edge_cp01_utc.jpg</code></td><td class="p-2.5">Can apply edge detection, filters, annotations, bounding boxes</td></tr></tbody></table>

<div class="border-l-2 border-primary pl-3 py-1 mb-3 text-xs text-foreground italic">Processing discipline: "I applied an edge filter to highlight cracks. The raw frame is preserved at <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">raw_captures/front_utc.jpg</code>. The filtered output is at <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">derived/edge_utc.jpg</code>." Both files, clearly labeled, with the raw frame as the authoritative source.</div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">RTSP Video Recording</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Step</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Action</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Verification</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">1. Record</td><td class="p-2.5">Start RTSP stream capture with explicit writer config — codec, resolution, frame rate</td><td class="p-2.5">Confirm stream is active before declaring recording started</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">2. File Size</td><td class="p-2.5">After recording stops, check the file size</td><td class="p-2.5">Video file under 1 KB is almost certainly corrupt — stream may have failed silently</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">3. Playback</td><td class="p-2.5">Open the video file and play at least first and last few seconds</td><td class="p-2.5">Confirm content is expected scene, not black frame or frozen image</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">4. Scene Match</td><td class="p-2.5">Does the video show the correct checkpoint?</td><td class="p-2.5">If scene does not match, recording is mislabeled — fix before continuing</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Hands-On Steps</h4></div>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 1 — Session & readiness</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/vinci-unitree

# Confirm camera service is alive
python course/day-03/lab-01/lab01_b2_subscribe_sport_mode_state.py eth0
# Press Ctrl+C after confirming telemetry flows</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 2 — Capture front still (mock inspection)</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-04/lab-01/b2_camera_capture_demo.py eth0 \\
  --camera front --checkpoint cp01 \\
  --out-dir ./run_dry_team_a

# Verify immediately:
open run_dry_team_a/raw_captures/front_cp01.jpg   # macOS
# or: xdg-open / eog / feh (Linux)</pre>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Expected: image opens, shows the scene in front of the B2, file size &gt; 10 KB.</p>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 3 — Capture rear still</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-04/lab-01/b2_camera_capture_demo.py eth0 \\
  --camera rear --checkpoint cp01 --out-dir ./run_dry_team_a

open run_dry_team_a/raw_captures/rear_cp01.jpg</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 4 — Generate derived output (OpenCV)</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-04/lab-01/b2_camera_capture_demo.py eth0 \\
  --camera front --checkpoint cp01 \\
  --edge-detect --out-dir ./run_dry_team_a

# Verify both files exist and are different:
ls -la run_dry_team_a/raw_captures/front_cp01.jpg
ls -la run_dry_team_a/derived/edge_cp01.jpg</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 5 — Immediate verification loop</p>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">For every capture, execute this verbal loop:</p>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><span class="font-bold text-foreground">Capture</span>: "Front camera, checkpoint cp01 — captured."</li><li><span class="font-bold text-foreground">Open</span>: Open the file — does it display a real image? Not black, not corrupt?</li><li><span class="font-bold text-foreground">Label</span>: "Checkpoint cp01 — frame verified, scene matches expected view."</li><li><span class="font-bold text-foreground">Place</span>: Copy to <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">checkpoints/cp01/frame.jpg</code></li><li><span class="font-bold text-foreground">Confirm Log</span>: Is sportmodestate.jsonl still receiving lines? (for Lab 2)</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Debugging — One Channel at a Time</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Channel</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Test in Isolation</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Camera alone</td><td class="p-2.5">Test that VideoClient initializes, captures a still, saves a readable .jpg. No telemetry, no motion — just one camera channel.</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Logger alone</td><td class="p-2.5">Test that SportModeState subscriber writes valid JSONL lines to a file. Confirm lines are parseable.</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Folder alone</td><td class="p-2.5">Test that the run folder structure is created correctly — all directories exist, naming conventions correct.</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Combined</td><td class="p-2.5">Only after all channels work independently, combine them. Channel-by-channel confidence before integration.</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Troubleshooting</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Symptom</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Action</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">GetImageSample returns non-zero code</td><td class="p-2.5">Verify camera service is active on the robot; check VideoClient initialization</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Saved image is all black</td><td class="p-2.5">Camera may be covered or in dark environment; check for lens cap or lighting</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">File size &lt; 1 KB</td><td class="p-2.5">Corrupt capture — stream may have failed. Re-capture and verify immediately.</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Image does not match expected scene</td><td class="p-2.5">Wrong camera selected (front vs rear) or robot is facing wrong direction</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">RTSP recording has 0 bytes</td><td class="p-2.5">Stream configuration error — check codec, resolution, frame rate settings</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Deliverable</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Front and rear still captures for at least one mock checkpoint, verified as openable</li><li>One derived OpenCV output (edge detection or filter) with raw frame preserved</li><li>Log of the verbal verification loop for one checkpoint (Capture → Open → Label → Place)</li><li>One sentence: what did the verification step catch that a file-save confirmation alone would have missed?</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Next Lab</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3"><a href="../lab-02/" class="text-primary underline hover:text-primary/80">Lab 2 — Field Run, State Logging &amp; Reporting</a> — Execute the complete B2 inspection: log telemetry, move between checkpoints, capture evidence, validate, and write artifact-backed reports.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">References</h4></div>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">vendor/unitree_sdk2_python/example/b2/camera_opencv.py</code></li><li>OpenCV docs: <a href="https://docs.opencv.org/" class="text-primary underline hover:text-primary/80">docs.opencv.org</a></li><li>Day 04 slides: Sections 13–22 (Mock Inspection Scripts)</li></ul>"""

    placeholder_script = """#!/usr/bin/env python3
\"\"\"
B2 Camera Capture Demo — Day 4, Lab 1
Mock inspection camera capture with verification.

Usage:
  conda activate unitree_env
  python b2_camera_capture_demo.py eth0 --camera front --checkpoint cp01 --out-dir ./run_dry_team_a
\"\"\"
import sys, time, argparse, json, os
from pathlib import Path
from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.video.video_client import VideoClient
import cv2, numpy as np


def capture_still(interface: str, camera: str, checkpoint: str, out_dir: str, edge_detect: bool = False):
    \"\"\"Capture one still frame from B2 front or rear camera.\"\"\"
    print(f"Initializing DDS on {interface}...")
    ChannelFactoryInitialize(0, interface)

    client = VideoClient()
    client.SetTimeout(5.0)
    client.Init()

    print(f"Capturing {camera} camera at {checkpoint}...")
    code, data = client.GetImageSample()

    if code != 0:
        print(f"ERROR: GetImageSample returned code {code}")
        return 1

    img = cv2.imdecode(np.frombuffer(bytes(data), np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        print("ERROR: Failed to decode image — data may be corrupt")
        return 1

    # Setup paths
    out_path = Path(out_dir)
    raw_dir = out_path / "raw_captures"
    raw_dir.mkdir(parents=True, exist_ok=True)

    # Save raw frame
    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    raw_path = raw_dir / f"{camera}_{checkpoint}_{ts}.jpg"
    cv2.imwrite(str(raw_path), img)
    file_size = raw_path.stat().st_size

    print(f"Saved: {raw_path} ({img.shape[1]}x{img.shape[0]}, {file_size} bytes)")

    # Copy selected evidence to checkpoint folder
    cp_dir = out_path / "checkpoints" / checkpoint
    cp_dir.mkdir(parents=True, exist_ok=True)
    cp_frame = cp_dir / "frame.jpg"
    cv2.imwrite(str(cp_frame), img)
    print(f"Checkpoint evidence: {cp_frame}")

    # Derived output (edge detection)
    if edge_detect:
        derived_dir = out_path / "derived"
        derived_dir.mkdir(parents=True, exist_ok=True)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        edge_path = derived_dir / f"edge_{checkpoint}_{ts}.jpg"
        cv2.imwrite(str(edge_path), edges)
        print(f"Derived (edge): {edge_path}")
        print("  Raw frame preserved as authoritative source.")

    # Verification check
    if file_size < 1024:
        print("WARNING: File size < 1 KB — capture may be corrupt!")
    else:
        print("VERIFY: Open the file and confirm scene matches checkpoint.")

    return 0


def main():
    parser = argparse.ArgumentParser(description="B2 Camera Capture Demo")
    parser.add_argument("interface", help="Network interface (e.g., eth0)")
    parser.add_argument("--camera", default="front", choices=["front", "rear"],
                        help="Camera to capture")
    parser.add_argument("--checkpoint", default="cp01", help="Checkpoint ID")
    parser.add_argument("--out-dir", default="./run_dry", help="Run folder root")
    parser.add_argument("--edge-detect", action="store_true",
                        help="Generate derived edge detection output")
    args = parser.parse_args()

    print("\\n" + "=" * 60)
    print("   B2 MOCK INSPECTION CAPTURE")
    print("=" * 60)
    print(f"Camera: {args.camera} | Checkpoint: {args.checkpoint}")
    print(f"Output: {args.out_dir}\\n")

    return capture_still(args.interface, args.camera, args.checkpoint,
                         args.out_dir, args.edge_detect)


if __name__ == "__main__":
    sys.exit(main())
"""

    return {
        "id": "lab-01",
        "title": "Mock Inspection Video — B2 Front & Back Cameras",
        "content": content,
        "code_files": [
            {"name": "b2_camera_capture_demo.py", "code": placeholder_script}
        ]
    }


# ── Lab 02: Field Run, State Logging & Reporting ─────────────────────────

def build_lab02() -> dict:
    content = """<div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5 text-xs mb-4 p-3 bg-muted/30 border border-border/60 rounded-lg"><div class="flex gap-2"><span class="font-semibold text-foreground">Duration:</span><span>~90 min (30 min field run + 30 min validation + 30 min report)</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Robot required:</span><span>Yes — supervised B2 motion between checkpoints</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Motion:</span><span>Yes (supervised — field roles required)</span></div></div>

<div class="border border-primary/30 bg-primary/5 rounded-lg p-4 mb-6"><div class="flex items-center gap-2 mb-3"><span class="text-base">🎯</span><span class="text-sm font-bold text-foreground tracking-tight">Learning Objectives</span></div><ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Execute a <span class="font-bold text-foreground">complete B2 field inspection</span> with defined roles, supervised motion, and continuous telemetry logging.</li><li>Apply the <span class="font-bold text-foreground">stable-dwell capture rule</span> — stop before capture, verify velocity is near zero.</li><li>Produce a <span class="font-bold text-foreground">validated run folder</span> and write an <span class="font-bold text-foreground">artifact-backed field report</span> with the 5-field claim pattern.</li><li>Complete <span class="font-bold text-foreground">B2 hardware maintenance</span> — power state, body, feet, payload, sensors, file archive.</li></ol></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">Prerequisites: Lab 0 (run folder approval) + Lab 1 (camera capture verified).</p>

<div class="border border-red-500/40 bg-red-500/10 rounded-lg p-3 mb-4"><span class="font-semibold text-red-600 dark:text-red-400 text-xs uppercase tracking-wide">⚠ Supervised B2 Motion</span><p class="text-xs text-muted-foreground leading-relaxed mt-1">This lab commands B2 motion between checkpoints. <span class="font-bold text-foreground">Field roles must be assigned</span> before the B2 powers on. The spotter has immediate stop authority. No motion command is sent without the run director's explicit approval.</p></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Concepts — Field Roles (Assign Before Motion)</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Role</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Responsibility</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Stop Authority</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Run Director</span></td><td class="p-2.5">Approves all motion and capture actions. Has final authority to proceed or halt.</td><td class="p-2.5">Full — no command sent without approval</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Terminal Operator</span></td><td class="p-2.5">Executes commands at keyboard. Reads each command aloud before sending. Watches console.</td><td class="p-2.5">Immediate — Ctrl+C or StopMove on command</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Spotter</span></td><td class="p-2.5">Watches robot and surrounding space continuously.</td><td class="p-2.5">Immediate — spotter says stop, operator stops, no questions</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Evidence Lead</span></td><td class="p-2.5">Checks every saved file immediately after capture — opens image, confirms scene, verifies size.</td><td class="p-2.5">Can halt the run if evidence is unusable</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Reporter</span></td><td class="p-2.5">Records limitations, deviations, and field observations in real time.</td><td class="p-2.5">Can flag gaps that need recapture before proceeding</td></tr></tbody></table>

<div class="border-l-2 border-primary pl-3 py-1 mb-3 text-xs text-foreground italic">Role assignment check: Before the B2 powers on, every person in the arena must know their role and their stop authority. If anyone cannot state their role in one sentence, roles are not clear enough to proceed.</div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Observable Readiness — Five Confirmed Checks</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">#</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Check</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">How to Confirm</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">1</td><td class="p-2.5"><span class="font-bold text-foreground">Interface</span></td><td class="p-2.5">Correct NIC active, IP on expected subnet, ping to B2 confirmed, DDS discovery working</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">2</td><td class="p-2.5"><span class="font-bold text-foreground">Perimeter</span></td><td class="p-2.5">Arena boundaries marked, obstacles identified, operator zones designated, bystanders aware</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">3</td><td class="p-2.5"><span class="font-bold text-foreground">Stop Path</span></td><td class="p-2.5">Remote stop accessible, script stop command ready (Ctrl+C), physical stop procedure agreed</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">4</td><td class="p-2.5"><span class="font-bold text-foreground">Cameras</span></td><td class="p-2.5">Front still capture verified, RTSP stream confirmed playable, file save paths writable</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">5</td><td class="p-2.5"><span class="font-bold text-foreground">Logger</span></td><td class="p-2.5">SportModeState subscriber running, JSONL file writable, lines appearing and parseable</td></tr></tbody></table>

<div class="border-l-2 border-primary pl-3 py-1 mb-3 text-xs text-foreground italic">Readiness gate: Read each check aloud. "Interface — confirmed. Perimeter — clear. Stop path — known. Cameras — tested. Logger — running." All five confirmed → motion may proceed. Any one missing → wait.</div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Stable-Dwell Capture Rule</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Checkpoint evidence is strongest when the robot is <span class="font-bold text-foreground">stationary</span>. Follow this sequence at every checkpoint:</p>

<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><span class="font-bold text-foreground">Approach</span> — Move the B2 into inspection view using bounded, supervised motion. Velocity should decrease as the robot nears the checkpoint — approach slow, not fast.</li><li><span class="font-bold text-foreground">StopMove or Dwell</span> — Command the robot to stop and stabilize. Confirm velocity reads near zero in SportModeState. Wait at least 1–2 seconds after stop before capture — settling time matters.</li><li><span class="font-bold text-foreground">Capture Frame</span> — Execute still capture only after confirming the robot is stationary. The image should be sharp, well-framed, and clearly show the inspection target.</li><li><span class="font-bold text-foreground">Label Checkpoint</span> — Save as <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">checkpoints/&lt;id&gt;/frame.jpg</code>. State the checkpoint ID aloud. Evidence lead confirms file is saved and opens correctly.</li><li><span class="font-bold text-foreground">Continue</span> — Only after evidence lead confirms usable capture does the director approve the next motion leg.</li></ol>

<div class="border border-amber-500/40 bg-amber-500/10 rounded-lg p-3 mb-4"><span class="font-semibold text-amber-600 dark:text-amber-400 text-xs uppercase tracking-wide">Capture Rule</span><p class="text-xs text-muted-foreground leading-relaxed mt-1">"Capture in motion is not inspection evidence — it is a screenshot of a moving robot." If SportModeState velocity is non-zero, wait. Blurred evidence weakens every claim that follows.</p></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Continuous Telemetry — Log Through the Run</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Phase</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Logging Action</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Before Motion</span></td><td class="p-2.5">Start SportModeState logging. Confirm lines appearing. Log at least 5–10 seconds of stationary baseline — shows pre-run state.</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">During Motion & Capture</span></td><td class="p-2.5">Keep logging continuously through every motion leg, every checkpoint approach, every dwell, every capture. No gaps — the log is the runtime witness.</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">After Final Notes</span></td><td class="p-2.5">Continue logging for several seconds after final capture and notes — captures robot's post-inspection state.</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">Log coverage test: Open your <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">sportmodestate.jsonl</code>. Does the first timestamp precede the first motion command? Does the last timestamp follow the final capture?</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">The 5-Field Report Claim Pattern</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Every claim in your field report must follow this fixed pattern. A vague summary of a live demo is not a report.</p>

<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Field</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Question</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Example</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Claim</span></td><td class="p-2.5">What are you asserting?</td><td class="p-2.5">"The B2 successfully inspected cp01 and captured clear visual evidence."</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Artifact</span></td><td class="p-2.5">Which file supports this claim?</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">checkpoints/cp01/frame.jpg</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">sportmodestate.jsonl</code> lines 130–145</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Telemetry Context</span></td><td class="p-2.5">What does robot state data say about the capture moment?</td><td class="p-2.5">"Velocity near zero (vx=0.02), mode stable (Damp), body height normal (0.45m)"</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Limitation</span></td><td class="p-2.5">What could weaken this claim?</td><td class="p-2.5">"Direct sunlight from right side caused slight washout on left edge of image"</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Confidence</span></td><td class="p-2.5">How sure are you?</td><td class="p-2.5">"High — multiple sensors agree, robot was stationary, image is sharp"</td></tr></tbody></table>

<div class="border-l-2 border-primary pl-3 py-1 mb-3 text-xs text-foreground italic">Report standard: "Not 'the robot worked.' Claim + Artifact + Telemetry + Limitation + Confidence."</div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Hands-On — Field Execution</h4></div>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 0 — Role assignment & readiness</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed"># Assign roles aloud:
# "Run Director: [name]. Terminal Operator: [name]. Spotter: [name].
#  Evidence Lead: [name]. Reporter: [name]."

# Confirm readiness (all five checks):
# Interface — confirmed. Perimeter — clear. Stop path — known.
# Cameras — tested. Logger — running.</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 1 — Start telemetry logging</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed"># Start SportModeState subscriber, redirect to run folder
python course/day-03/lab-01/lab01_b2_subscribe_sport_mode_state.py eth0 \
  > run_field_team_a/sportmodestate.jsonl &
LOGGER_PID=$!
echo "Logger PID: $LOGGER_PID"

# Verify lines are appearing:
tail -3 run_field_team_a/sportmodestate.jsonl</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 2 — Supervised motion & capture at each checkpoint</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed"># For each checkpoint:
# 1. Director: "Approaching cp01 — move forward 0.4 m"
# 2. Operator: "Sending Move(0.4, 0.0, 0.0) — sent."
# 3. Spotter: "Robot moving — clear path."
# 4. Operator: "StopMove sent. Robot stationary."
# 5. Evidence Lead: "Velocity near zero. Capturing..."
python course/day-04/lab-01/b2_camera_capture_demo.py eth0 \\
  --camera front --checkpoint cp01 --out-dir ./run_field_team_a
# 6. Evidence Lead: "Frame verified — opens, scene matches cp01. Copied to checkpoints/cp01/frame.jpg"
# 7. Reporter: "cp01: slight glare from overhead lights — noted."
# 8. Director: "cp01 complete. Approving leg to cp02..."</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 3 — Stop logging & validate</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed"># Stop logger
kill $LOGGER_PID

# Validate run folder
python course/day-02/lab-01/lab01_validate_run_folder.py run_field_team_a

# Expected: Summary: PASS — run folder valid (or PASS with warnings)</pre>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Hands-On — Report Writing & Validation</h4></div>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 4 — Parse telemetry into fields</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed"># Extract key fields from JSONL
python -c "
import json
with open('run_field_team_a/sportmodestate.jsonl') as f:
    for line in f:
        if not line.strip(): continue
        d = json.loads(line)
        # Extract timestamp, velocity, mode for visualization
        print(f'{d.get(\"timestamp\",\"?\")} vx={d.get(\"velocity\",[0,0,0])[0]:.3f} vyaw={d.get(\"yaw_speed\",0):.3f} mode={d.get(\"mode\",\"?\")}')
"</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 5 — Write field_report.md using the 5-field pattern</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed"># Field Report — Team A — B2 Inspection

## Run Summary
- Date: 2026-06-04
- Operator: Your Name
- Robot: B2-lab-1
- Scenario: Visual inspection of mock equipment bay — 3 checkpoints
- Validation: PASS

## Checkpoint Claims

### cp01 — Equipment Bay Left
- **Claim:** The B2 successfully inspected cp01 and captured clear visual evidence of the equipment bay left panel.
- **Artifact:** checkpoints/cp01/frame.jpg
- **Telemetry Context:** Velocity near zero (vx=0.02), mode Damp, body height 0.45m — robot was stationary during capture.
- **Limitation:** Overhead fluorescent lights caused slight glare on the top-right corner of the image.
- **Confidence:** High — visual evidence is sharp, telemetry confirms stable dwell.

### cp02 — Control Panel Center
[repeat pattern]

## Limitations Summary
- cp01: Slight glare from overhead lights — still usable.
- cp02: Rear camera frame was dark — front frame used as primary evidence.

## Maintenance Notes
See MAINTENANCE.md</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 6 — B2 hardware maintenance walkthrough</p>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Check</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Action</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Power State</span></td><td class="p-2.5">Confirm B2 is in safe power mode — Damp or powered down. Battery level noted. No active motion commands.</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Body & Feet</span></td><td class="p-2.5">Inspect for visible damage, debris, or unusual wear. Check foot pads for embedded gravel. Clean if needed.</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Payload Mount & Cables</span></td><td class="p-2.5">Verify payload secure, connectors seated, cables not pinched or frayed.</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Sensor Surfaces</span></td><td class="p-2.5">Clean camera lenses and sensor windows — dust/fingerprints from this run affect the next inspection.</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">File Archive</span></td><td class="p-2.5">Confirm all run artifacts are saved, backed up, and organized for report writing and instructor review.</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">Maintenance discipline: "The next team should find the B2 in the same condition I would want to receive it."</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Fallback Procedures — State Every Limitation</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">If This Fails...</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Fall Back To...</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Report Caveat</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">RTSP video</td><td class="p-2.5">Front/rear still captures at each checkpoint</td><td class="p-2.5">"RTSP video was unavailable — still frame and telemetry used instead."</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Both cameras</td><td class="p-2.5">SportModeState telemetry + operator notes</td><td class="p-2.5">"Automated capture failed — all evidence is from operator observation."</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">All sensors</td><td class="p-2.5">Operator notes become primary record</td><td class="p-2.5">"No automated evidence available — report based solely on field observations."</td></tr></tbody></table>

<div class="border-l-2 border-primary pl-3 py-1 mb-3 text-xs text-foreground italic">Fallback rule: A field run with stated fallbacks is still valid engineering work. A field run with hidden failures is not. State every fallback — the report's credibility depends on honesty about limitations.</div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Debrief — Four Outcome Check</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Outcome</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Evidence You Should Have</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Rugged Navigation & Sensors</span></td><td class="p-2.5">Terrain notes + sensor table + telemetry log — can you explain how terrain affected evidence?</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Mock Inspection Scripts</span></td><td class="p-2.5">Validated mock run folder — did you pass the gate before hardware?</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">B2 Field Capture</span></td><td class="p-2.5">Field run folder with checkpoints, captures, and continuous telemetry</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Logs, Reports, Maintenance</span></td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">field_report.md</code> + validator output + <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">MAINTENANCE.md</code></td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Reviewability Test</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Hand your run folder to a classmate who did not watch your field run. Can they answer:</p>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>What was inspected?</li><li>What evidence was captured?</li><li>What was the robot's state at each capture?</li><li>What limitations exist?</li><li>What does the report claim?</li></ul>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">If any answer is "no," your Day 4 workflow is not yet complete.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Deliverable</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">run_field_team_*/</code> folder with complete structure and validated (PASS)</li><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">sportmodestate.jsonl</code> covering full run window (pre-motion through post-capture)</li><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">field_report.md</code> with at least one claim per checkpoint using the 5-field pattern</li><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">MAINTENANCE.md</code> with all five checks completed</li><li>Field notes from the reporter (limitations, deviations, fallback decisions)</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Next</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3"><a href="../../day-05/" class="text-primary underline hover:text-primary/80">Day 5</a> — Capstone integration and advanced topics.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">References</h4></div>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Day 2 run-folder validator: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">day-02/lab-01/lab01_validate_run_folder.py</code></li><li>Day 3 B2 telemetry: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">day-03/lab-01/lab01_b2_subscribe_sport_mode_state.py</code></li><li>B2 sport client: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">vendor/unitree_sdk2_python/example/b2/b2_sport_client.py</code></li><li>Field guide: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">docs/GO2-FIELD-GUIDE.md</code></li></ul>"""

    field_report_template = """# Field Report — Team [Name] — B2 Inspection

## Run Summary
- **Date:** YYYY-MM-DD
- **Operator:** Your Name
- **Robot Platform:** B2
- **Robot ID:** B2-lab-[N]
- **Interface:** [eth0 / en6]
- **Scenario:** [Brief description]
- **Validation Result:** [PASS / PASS with Warnings]

## Checkpoint Claims

### cp01 — [Checkpoint Label]
- **Claim:** [What are you asserting? Be specific.]
- **Artifact:** checkpoints/cp01/frame.jpg
- **Telemetry Context:** [Velocity, mode, body height at capture moment.
  Include specific JSONL line numbers or timestamps.]
- **Limitation:** [Glare, occlusion, vibration, etc. What could weaken this claim?]
- **Confidence:** [High / Medium / Low] — [Reasoning]

### cp02 — [Checkpoint Label]
- **Claim:**
- **Artifact:**
- **Telemetry Context:**
- **Limitation:**
- **Confidence:**

### cp03 — [Checkpoint Label]
- **Claim:**
- **Artifact:**
- **Telemetry Context:**
- **Limitation:**
- **Confidence:**

## Limitations Summary
[Collect all limitations from above. Note any skipped checkpoints or fallbacks.]

## Field Notes
[Reporter's real-time observations during the run.]

## Log Coverage
- First telemetry timestamp: [UTC]
- Last telemetry timestamp: [UTC]
- Total JSONL lines: [N]
- Log covers: [Before first motion through after final capture? Any gaps?]

## Validation Output
```
[Paste validator output here]
```
"""

    return {
        "id": "lab-02",
        "title": "Field Run, State Logging & Reporting",
        "content": content,
        "code_files": [
            {"name": "field_report_template.md", "code": field_report_template}
        ]
    }


# ── Main ────────────────────────────────────────────────────────────────

def main():
    print(f"Reading syllabus from: {SYLLABUS_PATH}")
    with open(SYLLABUS_PATH) as f:
        syllabus = json.load(f)

    if "04" not in syllabus:
        print("ERROR: Day 04 not found in syllabus")
        sys.exit(1)

    day04 = syllabus["04"]
    if "labs" not in day04:
        print("ERROR: No labs array in Day 04")
        sys.exit(1)

    print(f"Found {len(day04['labs'])} labs in Day 04")

    builders = {
        "lab-00": build_lab00,
        "lab-01": build_lab01,
        "lab-02": build_lab02,
    }

    new_labs = []
    for lab in day04["labs"]:
        lab_id = lab.get("id", "")
        if lab_id in builders:
            print(f"  Building {lab_id}...")
            new_lab = builders[lab_id]()
            new_labs.append(new_lab)
        else:
            print(f"  Keeping {lab_id} as-is (no builder)")
            new_labs.append(lab)

    day04["labs"] = new_labs

    print(f"\nWriting updated syllabus to: {SYLLABUS_PATH}")
    with open(SYLLABUS_PATH, 'w') as f:
        json.dump(syllabus, f, indent=2, ensure_ascii=False)

    print("Done! Enhanced Day 04 lab workspaces written to syllabus.json")


if __name__ == "__main__":
    main()