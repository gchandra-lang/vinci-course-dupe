#!/usr/bin/env python3
"""
Build enhanced Day 03 lab workspace entries in syllabus.json,
matching the rich HTML format of Day 01 labs.

Reads README.md and script files from Labs/day-03/ and updates
client/src/data/syllabus.json with complete lab content.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SYLLABUS_PATH = REPO / "client" / "src" / "data" / "syllabus.json"
LABS_SRC = REPO / "Labs" / "day-03"


def read_file(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8')
    except Exception:
        return ''


# ── Lab content definitions ──────────────────────────────────────────────

def build_lab00() -> dict:
    script = read_file(LABS_SRC / "lab-01" / "lab01_b2_subscribe_sport_mode_state.py")

    content = """<div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5 text-xs mb-4 p-3 bg-muted/30 border border-border/60 rounded-lg"><div class="flex gap-2"><span class="font-semibold text-foreground">Platform:</span><span>Unitree B2</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Duration:</span><span>~20–30 min</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Robot required:</span><span>Yes — powered and on subnet</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Motion:</span><span>None (readiness check only)</span></div></div>

<div class="border border-primary/30 bg-primary/5 rounded-lg p-4 mb-6"><div class="flex items-center gap-2 mb-3"><span class="text-base">🎯</span><span class="text-sm font-bold text-foreground tracking-tight">Learning Objectives</span></div><ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Confirm <span class="font-bold text-foreground">B2 network</span> connectivity (<code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ping</code> robot IP, verify interface name).</li><li>Validate the <span class="font-bold text-foreground">SDK environment</span> — <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">conda activate unitree_env</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">CYCLONEDDS_HOME</code>, imports.</li><li>Subscribe to <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">rt/sportmodestate</code> and verify live telemetry (mode, gait, position, velocity, body height).</li><li>State the <span class="font-bold text-foreground">B2 safety checklist</span> before any motion lab (spotter, cleared area ≥ 3 m × 3 m, estop plan).</li></ol></div>

<div class="border border-amber-500/40 bg-amber-500/10 rounded-lg p-3 mb-4"><span class="font-semibold text-amber-600 dark:text-amber-400 text-xs uppercase tracking-wide">B2 vs Go2 Note</span><p class="text-xs text-muted-foreground leading-relaxed mt-1">The B2 uses the same <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">unitree_sdk2py</code> Python SDK as the Go2 but with different DDS topic namespaces and sport client imports from <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">unitree_sdk2py.b2.sport</code>. The B2 is a larger, more powerful platform — motion limits and safety rules are correspondingly stricter.</p></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Prerequisites</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">conda activate unitree_env</code> with <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">unitree_sdk2py</code> installed.</li><li>Laptop on the same subnet as the B2 (verify interface name, e.g. <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">eth0</code> or <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">en6</code>).</li><li>Instructor present for any motion commands (Labs 2–4).</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Safety Checklist — Before Any B2 Motion Lab</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><span class="font-bold text-foreground">Spotter</span> present (first run of every lab).</li><li><span class="font-bold text-foreground">Clear area</span> ≥ 3 m × 3 m for motion labs.</li><li>Confirm <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">rt/sportmodestate</code> is publishing and <span class="font-bold text-foreground">FSM ≠ damp</span>.</li><li>Have an <span class="font-bold text-foreground">emergency stop</span> procedure and power-off plan accessible.</li><li>Keep hands and tools away from legs during motion.</li><li>Be ready to press <span class="font-bold text-foreground">Ctrl+C</span> or use the StopMove menu option for emergencies.</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Hands-On Steps</h4></div>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step A — Activate environment</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/vinci-unitree</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step B — Identify network interface</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed"># macOS
ifconfig | grep -A 1 "en"
# Linux
ip link show</pre>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Find the wired interface connected to the B2 subnet. Common names: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">eth0</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">en6</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">enx...</code>.</p>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step C — Verify DDS connectivity (read-only)</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-03/lab-01/lab01_b2_subscribe_sport_mode_state.py eth0</pre>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Expected: Live telemetry lines printing every ~200 ms:</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">mode=1 gait=0 pos=( 0.12, 0.03) vel=( 0.00, 0.00) yaw= 0.01 height= 0.45</pre>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Press <span class="font-bold text-foreground">Ctrl+C</span> to exit. If no messages within 5s, re-check the interface and robot power.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Knowledge Check</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>What DDS topic do you subscribe to for B2 telemetry?</li><li>Why is subscribing to telemetry a safe first step before any motion lab?</li><li>Name three fields printed by the subscriber script.</li><li>What is the minimum cleared area for B2 motion labs?</li><li>What should you do if the robot's FSM mode is <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">damp</code>?</li></ol>

<div class="border border-amber-500/40 bg-amber-500/10 rounded-lg p-3 mb-4"><span class="font-semibold text-amber-600 dark:text-amber-400 text-xs uppercase tracking-wide">Answers</span><ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mt-2"><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">rt/sportmodestate</code></li><li>It confirms DDS is working and the robot is publishing state without sending any motion commands.</li><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">mode</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">gait_type</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">position</code> (or <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">velocity</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">body_height</code>).</li><li>At least 3 m × 3 m.</li><li>Do not attempt motion; consult field guide and instructor for recovery.</li></ol></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Troubleshooting</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Symptom</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Action</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">No output from subscriber</td><td class="p-2.5">Verify network interface name; check robot power and subnet</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Warning after 5 seconds</td><td class="p-2.5">Robot may be off or on different subnet; confirm DDS topics are publishing</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Import error for <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">unitree_sdk2py</code></td><td class="p-2.5">Activate <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">unitree_env</code>; verify package installation</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ChannelFactoryInitialize</code> fails</td><td class="p-2.5">Check interface name and local network configuration</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Deliverable</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Screenshot or log showing <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">lab01_b2_subscribe_sport_mode_state.py</code> successfully receiving telemetry</li><li>One sentence describing the meaning of <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">mode</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">gait_type</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">position</code>, and <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">body_height</code></li><li>Confirmation that no motion was commanded during this lab</li><li>Signed safety checklist (digital or paper)</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Next Lab</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3"><a href="../lab-01/" class="text-primary underline hover:text-primary/80">Lab 1 — Subscribe to B2 SportModeState</a> — Deeper dive into telemetry fields and DDS subscription callback mechanics.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">References</h4></div>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><a href="lab01_b2_subscribe_sport_mode_state.py" class="text-primary underline hover:text-primary/80">lab01_b2_subscribe_sport_mode_state.py</a></li><li>B2 Day 1 summary: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">day-03/README.md</code> (this file)</li><li>Field guide: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">docs/GO2-FIELD-GUIDE.md</code></li></ul>"""

    return {
        "id": "lab-00",
        "title": "B2 Readiness & Safety (No-Motion)",
        "content": content,
        "code_files": [
            {"name": "lab01_b2_subscribe_sport_mode_state.py", "code": script}
        ]
    }


def build_lab01() -> dict:
    script = read_file(LABS_SRC / "lab-01" / "lab01_b2_subscribe_sport_mode_state.py")

    content = """<div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5 text-xs mb-4 p-3 bg-muted/30 border border-border/60 rounded-lg"><div class="flex gap-2"><span class="font-semibold text-foreground">Duration:</span><span>~15–25 min</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Robot required:</span><span>Yes — powered and on same subnet</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Motion:</span><span>None (read-only status subscription)</span></div></div>

<div class="border border-primary/30 bg-primary/5 rounded-lg p-4 mb-6"><div class="flex items-center gap-2 mb-3"><span class="text-base">🎯</span><span class="text-sm font-bold text-foreground tracking-tight">Learning Objectives</span></div><ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Subscribe to DDS topic <span class="font-bold text-foreground"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">rt/sportmodestate</code></span> and receive <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">SportModeState_</code> messages.</li><li>Read the robot's current <span class="font-bold text-foreground">mode, gait, body position, velocity, yaw speed, and height</span>.</li><li>Understand the difference between <span class="font-bold text-foreground">status telemetry</span> and <span class="font-bold text-foreground">motion commands</span>.</li><li>Verify the network interface and DDS setup before attempting any control lab.</li></ol></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">Prerequisite: <a href="../lab-00/" class="text-primary underline hover:text-primary/80">Lab 0</a> complete (environment + network confirmed).</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Concepts — DDS Telemetry Pipeline</h4></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">The B2 publishes its current locomotion state on the DDS topic <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">rt/sportmodestate</code>. This lab <span class="font-bold text-foreground">does not send any motion commands</span>; it only listens for telemetry.</p>

<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Field</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Type</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Description</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">mode</code></td><td class="p-2.5">uint8</td><td class="p-2.5">Current control mode (FSM state)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">gait_type</code></td><td class="p-2.5">uint8</td><td class="p-2.5">Active gait (0 = idle, 1 = trot, ...)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">position</code></td><td class="p-2.5">float32[3]</td><td class="p-2.5">Robot body position [x, y, z] (odometry frame)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">velocity</code></td><td class="p-2.5">float32[3]</td><td class="p-2.5">Body velocity [vx, vy, vz]</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">yaw_speed</code></td><td class="p-2.5">float32</td><td class="p-2.5">Rotational speed around vertical axis</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">body_height</code></td><td class="p-2.5">float32</td><td class="p-2.5">Body height above the floor</td></tr></tbody></table>

<div class="border-l-2 border-primary pl-3 py-1 mb-3 text-xs text-foreground italic">Reading <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">rt/sportmodestate</code> is a <span class="font-bold text-foreground">safe first step</span> before commanding the robot. It confirms DDS is working, the robot is publishing state, and your interface is correct — all without any risk of motion.</div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Hands-On</h4></div>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 0 — Safety</p>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Clear the area around the robot even though no motion is commanded.</li><li>Confirm the robot is on a stable surface.</li><li>Use the correct network interface for your B2 robot.</li></ul>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 1 — Activate the environment</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">conda activate unitree_env
cd /path/to/vinci-unitree</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 2 — Run the subscriber</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-03/lab-01/lab01_b2_subscribe_sport_mode_state.py eth0</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 3 — Observe robot status</p>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">The script prints each received message as a single line. If no messages arrive within 5 seconds, the script warns you to check the connection.</p>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 4 — Stop cleanly</p>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Press <span class="font-bold text-foreground">Ctrl+C</span> to exit the subscriber.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Exercises</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><span class="font-bold text-foreground">Verify connection</span> — Run the script and confirm it prints live state lines. If not, check the interface and robot subnet.</li><li><span class="font-bold text-foreground">Inspect the payload</span> — Open <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">lab01_b2_subscribe_sport_mode_state.py</code> and identify where each printed field comes from in the callback function.</li><li><span class="font-bold text-foreground">Compare to motion labs</span> — Explain why this lab is safe to run before any locomotion control lab.</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Troubleshooting</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Symptom</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Action</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">No output, script starts normally</td><td class="p-2.5">Verify network interface and robot's DDS network connection</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Warning after 5 seconds</td><td class="p-2.5">Confirm B2 robot is powered on and on the same subnet</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Import error for <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">unitree_sdk2py</code></td><td class="p-2.5">Activate correct conda environment; ensure package is installed</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ChannelFactoryInitialize</code> fails</td><td class="p-2.5">Check interface name and local network configuration</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Deliverable</h4></div>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Screenshot or log showing the script successfully receiving <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">rt/sportmodestate</code> updates</li><li>One sentence describing the meaning of <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">mode</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">gait_type</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">position</code>, and <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">body_height</code></li><li>Confirmation that no motion was commanded during this lab</li></ul>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Next Lab</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3"><a href="../lab-02/" class="text-primary underline hover:text-primary/80">Lab 2 — Supervised B2 Motion Menu</a> — Send <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">BalanceStand</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">Move</code>, and <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">StopMove</code> via an interactive menu.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">References</h4></div>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><a href="lab01_b2_subscribe_sport_mode_state.py" class="text-primary underline hover:text-primary/80">lab01_b2_subscribe_sport_mode_state.py</a></li><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">vendor/unitree_sdk2_python/example/b2/</code></li></ul>"""

    return {
        "id": "lab-01",
        "title": "Subscribe to B2 SportModeState",
        "content": content,
        "code_files": [
            {"name": "lab01_b2_subscribe_sport_mode_state.py", "code": script}
        ]
    }


def build_lab02() -> dict:
    script = read_file(LABS_SRC / "lab-02" / "lab02_b2_motion_menu.py")

    content = """<div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5 text-xs mb-4 p-3 bg-muted/30 border border-border/60 rounded-lg"><div class="flex gap-2"><span class="font-semibold text-foreground">Duration:</span><span>~20–30 min</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Robot required:</span><span>Yes — sends motion commands</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Motion:</span><span>Yes (supervised — instructor required)</span></div></div>

<div class="border border-primary/30 bg-primary/5 rounded-lg p-4 mb-6"><div class="flex items-center gap-2 mb-3"><span class="text-base">🎯</span><span class="text-sm font-bold text-foreground tracking-tight">Learning Objectives</span></div><ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Use the <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">SportClient</code> API to send basic locomotion commands to the B2 robot.</li><li>Observe <span class="font-bold text-foreground">command sequencing</span> — stand before MoveToPos, gait switching, recovery.</li><li>Practice <span class="font-bold text-foreground">safe supervised motion</span>: issuing BalanceStand, Move, RecoveryStand, and emergency StopMove.</li></ol></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">Prerequisites: <a href="../lab-01/" class="text-primary underline hover:text-primary/80">Lab 1</a> complete (telemetry confirmed).</p>

<div class="border border-red-500/40 bg-red-500/10 rounded-lg p-3 mb-4"><span class="font-semibold text-red-600 dark:text-red-400 text-xs uppercase tracking-wide">⚠ Motion Enabled</span><p class="text-xs text-muted-foreground leading-relaxed mt-1">This lab <span class="font-bold text-foreground">sends motion commands</span> to the B2. Instructor supervision is mandatory. Clear the floor area (minimum 3 m × 3 m). No people or obstacles in front of the robot while it moves.</p></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Concepts — SportClient Command Menu</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">This lab demonstrates the difference between telemetry (read-only) and control (motion) labs. The script provides a simple numbered menu to execute common commands via the <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">SportClient</code>:</p>

<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">#</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Command</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Effect</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">1</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">BalanceStand()</code></td><td class="p-2.5">Bring robot to standing balance</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">2</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">StandDown()</code></td><td class="p-2.5">Sit down / relax stance</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">3</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">StopMove()</code></td><td class="p-2.5">Immediate motion stop (emergency)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">4</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">Move(0.5, 0.0, 0.0)</code></td><td class="p-2.5">Short relative translation (forward 0.5 m)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">5</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">RecoveryStand()</code></td><td class="p-2.5">Recovery from damp or fallen state</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">6</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">MoveToPos(0.5, 0.2, 0.0)</code></td><td class="p-2.5">Higher-level move-to (script stands first)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">7</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">SwitchGait(2)</code></td><td class="p-2.5">Switch gait mode (trot / walk / ...)</td></tr></tbody></table>

<div class="border-l-2 border-primary pl-3 py-1 mb-3 text-xs text-foreground italic">Issuing motion commands requires <span class="font-bold text-foreground">strict safety checks</span>. This lab keeps commands simple and supervised so you can observe effects and learn command semantics in a controlled way.</div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Safety (Required)</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Motion is <span class="font-bold text-foreground">ENABLED</span>. Clear floor area (minimum 3 m × 3 m).</li><li>No people or obstacles in front of the robot while it moves.</li><li><span class="font-bold text-foreground">Instructor</span> must supervise all movements.</li><li>Keep hands and tools away from the legs during motion.</li><li>Be ready to press <span class="font-bold text-foreground">Ctrl+C</span> or use StopMove (menu 3) for emergencies.</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Hands-On</h4></div>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 0 — Prepare environment</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">conda activate unitree_env
cd /path/to/vinci-unitree</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 1 — Run the motion menu</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-03/lab-02/lab02_b2_motion_menu.py eth0</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 2 — Suggested supervised sequence</p>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Order</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Menu #</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">What to observe</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">1st</td><td class="p-2.5">1 — BalanceStand</td><td class="p-2.5">Robot rises to standing; verify stable posture</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">2nd</td><td class="p-2.5">4 — Move forward 0.5m</td><td class="p-2.5">Controlled translation; note distance and speed</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">3rd</td><td class="p-2.5">5 — RecoveryStand</td><td class="p-2.5">Try if robot is damp; observe recovery posture</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">4th</td><td class="p-2.5">6 — MoveToPos</td><td class="p-2.5">Script calls BalanceStand then MoveToPos; verify sequencing</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Test</td><td class="p-2.5">3 — StopMove</td><td class="p-2.5">Only under instructor direction while moving</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">Note: Return codes of <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">0</code> indicate success for typical calls.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Exercises</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><span class="font-bold text-foreground">Validate MoveToPos sequencing</span> — Run option 6 and confirm the script explicitly issues <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">BalanceStand()</code> before <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">MoveToPos</code>.</li><li><span class="font-bold text-foreground">Observe return codes</span> — Record the printed return codes for each command and map them to expected outcomes.</li><li><span class="font-bold text-foreground">Gait switch</span> — Try option 7 to call <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">SwitchGait(2)</code> and observe changes in locomotion behaviour when issuing Movement afterwards.</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Troubleshooting</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Symptom</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Action</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Script fails to import SDK</td><td class="p-2.5">Activate <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">unitree_env</code> and ensure package is installed</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">No connection / timeouts</td><td class="p-2.5">Verify <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ChannelFactoryInitialize</code> interface name and network connectivity</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Robot does not stand or move</td><td class="p-2.5">Confirm robot safety switch is enabled and power state; retry <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">BalanceStand()</code></td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Unexpected motion or instability</td><td class="p-2.5">Stop immediately with <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">StopMove()</code> and call instructor</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Deliverable</h4></div>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Short log or video demonstrating: successful <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">BalanceStand</code>, one <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">Move</code> or <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">MoveToPos</code>, and a successful <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">StopMove</code></li><li>One sentence describing what <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">BalanceStand</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">Move</code>, and <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">StopMove</code> do</li></ul>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Next Lab</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3"><a href="../lab-03/" class="text-primary underline hover:text-primary/80">Lab 3 — B2 Stand Sequence (Low-Level Joint Control)</a> — Direct joint position control via <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">rt/lowcmd</code> at 500 Hz.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">References</h4></div>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><a href="lab02_b2_motion_menu.py" class="text-primary underline hover:text-primary/80">lab02_b2_motion_menu.py</a></li><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">vendor/unitree_sdk2_python/example/b2/b2_sport_client.py</code></li></ul>"""

    return {
        "id": "lab-02",
        "title": "Supervised B2 Sport RPC & Stand",
        "content": content,
        "code_files": [
            {"name": "lab02_b2_motion_menu.py", "code": script}
        ]
    }


def build_lab03() -> dict:
    script = read_file(LABS_SRC / "lab-03" / "lab03_b2_stand_sequence.py")
    const_file = read_file(LABS_SRC / "lab-03" / "unitree_legged_const.py")

    content = """<div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5 text-xs mb-4 p-3 bg-muted/30 border border-border/60 rounded-lg"><div class="flex gap-2"><span class="font-semibold text-foreground">Duration:</span><span>~30–45 min</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Robot required:</span><span>Yes — low-level joint commands move legs significantly</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Motion:</span><span>Yes (high risk — instructor supervision required)</span></div></div>

<div class="border border-primary/30 bg-primary/5 rounded-lg p-4 mb-6"><div class="flex items-center gap-2 mb-3"><span class="text-base">🎯</span><span class="text-sm font-bold text-foreground tracking-tight">Learning Objectives</span></div><ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Understand and run a <span class="font-bold text-foreground">multi-stage low-level stand sequence</span> using direct joint commands.</li><li>Learn how to publish <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">rt/lowcmd</code> and subscribe to <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">rt/lowstate</code> for closed-loop low-level control.</li><li>Practice <span class="font-bold text-foreground">releasing high-level motion modes</span> and returning the robot to remote controller (AI) mode.</li></ol></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">Prerequisites: <a href="../lab-02/" class="text-primary underline hover:text-primary/80">Lab 2</a> complete (SportClient familiarity); understanding of lowcmd concepts.</p>

<div class="border border-red-500/40 bg-red-500/10 rounded-lg p-3 mb-4"><span class="font-semibold text-red-600 dark:text-red-400 text-xs uppercase tracking-wide">⚠ High Motion Risk</span><p class="text-xs text-muted-foreground leading-relaxed mt-1">This script WILL move legs significantly through a multi-stage stand. Clear a large area (≥ 3 m × 3 m). Instructor must supervise at all times. Keep hands away from legs and mechanical linkages. The robot may not be in a stable posture if interrupted mid-sequence.</p></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Concepts — Low-Level Joint Control Pipeline</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">This lab implements a staged stand routine that transitions joint angles through several target poses using <span class="font-bold text-foreground">position control</span>:</p>

<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Component</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Role</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">rt/lowcmd</code> (<code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">LowCmd_</code>)</td><td class="p-2.5">Published at <span class="font-bold text-foreground">500 Hz</span> with joint position PD targets + CRC</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">rt/lowstate</code> (<code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">LowState_</code>)</td><td class="p-2.5">Captures current joint positions for initial conditions</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">MotionSwitcherClient</code></td><td class="p-2.5">Releases high-level controllers before low-level commands</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">SportClient</code></td><td class="p-2.5">Switches back to <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ai</code> mode after sequence completes</td></tr></tbody></table>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Key Parameters</p>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Param</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Value</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Meaning</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Joint <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">q</code> targets</td><td class="p-2.5">12 values per stage</td><td class="p-2.5">FR/FL/RR/RL × (hip, thigh, calf) in radians</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">Kp</code></td><td class="p-2.5">1000.0</td><td class="p-2.5">Joint position stiffness gain</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">Kd</code></td><td class="p-2.5">10.0</td><td class="p-2.5">Joint velocity damping gain</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Control interval</td><td class="p-2.5">2 ms</td><td class="p-2.5">500 Hz loop rate (RecurrentThread)</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Stand Sequence Stages</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Stage</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Duration</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Effect</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">1 — Semi-squat</td><td class="p-2.5">~1.0 s (500 cycles)</td><td class="p-2.5">From current pose to hips slightly spread, knees bent</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">2 — Lower crouch</td><td class="p-2.5">~1.8 s (900 cycles)</td><td class="p-2.5">Body lowered, tighter knee angles</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">3 — Hold</td><td class="p-2.5">~2.0 s (1000 cycles)</td><td class="p-2.5">Maintain crouch position</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">4 — Wider stance</td><td class="p-2.5">~1.8 s (900 cycles)</td><td class="p-2.5">Hips spread further apart (final stance)</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Safety (Required)</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>This script <span class="font-bold text-foreground">WILL move the legs significantly</span>. Clear a large area (≥ 3 m × 3 m).</li><li><span class="font-bold text-foreground">Instructor</span> must supervise at all times.</li><li>Keep hands away from legs and mechanical linkages.</li><li>Ensure robot is on a <span class="font-bold text-foreground">stable surface</span> and power/safety switches are correctly set.</li><li>Be prepared to stop (Ctrl+C) — robot may not be stable if interrupted.</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Hands-On</h4></div>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 0 — Prepare environment</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">conda activate unitree_env
cd /path/to/vinci-unitree</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 1 — Run the stand sequence script</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-03/lab-03/lab03_b2_stand_sequence.py eth0</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 2 — Use the menu</p>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Option</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Action</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">When</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">0</td><td class="p-2.5">Run low-level stand sequence</td><td class="p-2.5">To execute the 4-stage stand routine</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">1</td><td class="p-2.5">Switch to AI mode</td><td class="p-2.5">To regain remote controller control after low-level run</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">2</td><td class="p-2.5">Exit without action</td><td class="p-2.5">Safe exit</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">The stand sequence will: (1) Release any active high-level motion modes (<code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">StandDown()</code> + <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">MotionSwitcherClient.ReleaseMode()</code>), (2) Initialize <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">LowCmd_</code> with safe defaults and PD gains, (3) Publish joint position targets at 500 Hz through 4 stages.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Exercises</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><span class="font-bold text-foreground">Inspect stage targets</span> — Open <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">lab03_b2_stand_sequence.py</code> and identify the three target joint vectors (<code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">targetPos_1</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">targetPos_2</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">targetPos_3</code>). Describe how each stage changes posture.</li><li><span class="font-bold text-foreground">Adjust gains</span> — Experiment with smaller <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">Kp</code> / <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">Kd</code> values under strict supervision and observe effects on motion smoothness.</li><li><span class="font-bold text-foreground">Mode recovery</span> — After running the low-level sequence, choose menu option 1 and confirm the robot responds to the remote controller.</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Troubleshooting</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Symptom</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Action</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">No imports for <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">unitree_sdk2py</code></td><td class="p-2.5">Activate <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">unitree_env</code> and install the package</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Publisher or subscriber fails</td><td class="p-2.5">Verify <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ChannelFactoryInitialize</code> interface argument and network</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Unexpected joint behaviour</td><td class="p-2.5">Stop immediately (Ctrl+C). Check <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">Kp</code>/<code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">Kd</code> and target positions before retrying</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Cannot regain remote control</td><td class="p-2.5">Use menu option 1 to call <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">SelectMode("ai")</code> and verify return code</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Deliverable</h4></div>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Video or screenshots showing the stand sequence start and final stance</li><li>One paragraph describing what each target stage accomplishes and how PD gains affect behaviour</li><li>Confirmation that the robot was returned to <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ai</code> mode or remote controller after the exercise</li></ul>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Next Lab</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3"><a href="../lab-04/" class="text-primary underline hover:text-primary/80">Lab 4 — B2 Trajectory Following</a> — High-level autonomous path execution with <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">TrajectoryFollow</code> and <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">PathPoint</code> waypoints.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">References</h4></div>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><a href="lab03_b2_stand_sequence.py" class="text-primary underline hover:text-primary/80">lab03_b2_stand_sequence.py</a></li><li><a href="unitree_legged_const.py" class="text-primary underline hover:text-primary/80">unitree_legged_const.py</a> — joint ID constants</li><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">vendor/unitree_sdk2_python/example/b2/</code></li></ul>"""

    return {
        "id": "lab-03",
        "title": "B2 Stand Sequence (Low-Level Joint Control)",
        "content": content,
        "code_files": [
            {"name": "lab03_b2_stand_sequence.py", "code": script},
            {"name": "unitree_legged_const.py", "code": const_file}
        ]
    }


def build_lab04() -> dict:
    script = read_file(LABS_SRC / "lab-04" / "lab04_b2_trajectory.py")

    content = """<div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5 text-xs mb-4 p-3 bg-muted/30 border border-border/60 rounded-lg"><div class="flex gap-2"><span class="font-semibold text-foreground">Duration:</span><span>~30–45 min</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Robot required:</span><span>Yes — high-level autonomous path execution</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Motion:</span><span>Yes (supervised — instructor required)</span></div></div>

<div class="border border-primary/30 bg-primary/5 rounded-lg p-4 mb-6"><div class="flex items-center gap-2 mb-3"><span class="text-base">🎯</span><span class="text-sm font-bold text-foreground tracking-tight">Learning Objectives</span></div><ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Understand how to execute a <span class="font-bold text-foreground">pre-defined autonomous trajectory</span> using <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">SportClient</code> and <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">TrajectoryFollow</code>.</li><li>Learn how to read robot state from <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">rt/sportmodestate</code> and verify mode/gait information.</li><li>Practice safe transition between <span class="font-bold text-foreground">standing, classic walk mode, and return-to-menu</span> behaviour.</li></ol></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">Prerequisites: <a href="../lab-02/" class="text-primary underline hover:text-primary/80">Lab 2</a> complete (SportClient familiarity). Lab 3 (low-level) is helpful but not required.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Concepts — High-Level Trajectory Following</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">This lab runs a high-level trajectory sequence using the B2 sport mode API — <span class="font-bold text-foreground">no low-level joint control</span>:</p>

<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Component</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Role</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">TrajectoryFollow</code></td><td class="p-2.5">Sends a padded list of <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">PathPoint</code> objects to the robot</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">rt/sportmodestate</code> subscription</td><td class="p-2.5">Reads robot mode, gait, position, velocity, yaw speed, and body height once</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ClassicWalk(True/False)</code></td><td class="p-2.5">Enables / disables classic walk mode around trajectory execution</td></tr></tbody></table>

<p class="text-sm font-bold text-foreground mt-4 mb-2">PathPoint API</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">PathPoint(timeFromStart, x, y, yaw, vx, vy, vyaw)
# timeFromStart: seconds from trajectory start
# x, y: target position in odometry frame
# yaw: target orientation (radians)
# vx, vy, vyaw: target velocities at this point</pre>

<div class="border-l-2 border-primary pl-3 py-1 mb-3 text-xs text-foreground italic">SDK constraint: trajectory must have <span class="font-bold text-foreground">exactly 30 points</span>. The script defines 5 waypoints and pads the remaining 25 by repeating the final point with zero velocities.</div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Predefined Path Segments</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Segment</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">From</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">To</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Duration</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">1 — Move forward</td><td class="p-2.5">(0, 0.2) yaw=0</td><td class="p-2.5">(0.5, 0.2) yaw=0</td><td class="p-2.5">5 s</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">2 — Turn</td><td class="p-2.5">(0.5, 0.2) yaw=0</td><td class="p-2.5">(0.5, 0) yaw=1.5708</td><td class="p-2.5">5 s (~90° turn)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">3 — Move sideways</td><td class="p-2.5">(0.5, 0) yaw=1.5708</td><td class="p-2.5">(0.5, 0.5) yaw=1.5708</td><td class="p-2.5">5 s</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">4 — Turn back</td><td class="p-2.5">(0.5, 0.5) yaw=1.5708</td><td class="p-2.5">(0.5, 0.5) yaw=0</td><td class="p-2.5">5 s (~90° return)</td></tr></tbody></table>

<div class="border border-amber-500/40 bg-amber-500/10 rounded-lg p-3 mb-4"><span class="font-semibold text-amber-600 dark:text-amber-400 text-xs uppercase tracking-wide">Yaw Convention</span><p class="text-xs text-muted-foreground leading-relaxed mt-1">In the Unitree convention, <span class="font-bold text-foreground">positive yaw = left turn</span>. The script's comments note that the turn segment uses positive vyaw which turns left, despite the comment saying "intended as right." Verify direction on hardware and adjust signs if needed.</p></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Safety (Required)</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>This script <span class="font-bold text-foreground">WILL move</span> the robot forward, turn, and move sideways.</li><li>Clear area: ≥ 1.5 m in front and to the sides.</li><li><span class="font-bold text-foreground">Instructor</span> must supervise at all times.</li><li>Keep hands away from legs and any moving parts.</li><li>Be prepared to stop (Ctrl+C) if the robot behaves unexpectedly.</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Hands-On</h4></div>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 0 — Prepare environment</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">conda activate unitree_env
cd /path/to/vinci-unitree</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 1 — Run the trajectory script</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-03/lab-04/lab04_b2_trajectory.py eth0</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 2 — Use the menu</p>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Option</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Action</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">0</td><td class="p-2.5">Display sport mode state once (mode, gait, position, velocity, yaw, height)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">1</td><td class="p-2.5">Run the predefined trajectory (stand → ClassicWalk → path → stop)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">2</td><td class="p-2.5">Exit</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">The trajectory will: (1) Call <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">RecoveryStand()</code> to stand up, (2) Enable <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ClassicWalk(True)</code>, (3) Send 30-point trajectory, (4) Wait ~23 s while the trajectory executes, (5) Disable <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ClassicWalk(False)</code> and return to menu.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Exercises</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><span class="font-bold text-foreground">Inspect the trajectory</span> — Open <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">lab04_b2_trajectory.py</code> and identify the five defined <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">PathPoint</code> waypoints. Describe how each segment changes the robot's motion.</li><li><span class="font-bold text-foreground">Adjust the path</span> — Change one path point to modify the forward travel distance or the turn angle, then run the script under supervision and observe the effect.</li><li><span class="font-bold text-foreground">Verify state output</span> — Use menu option 0 and confirm the robot state prints mode, gait, position, velocity, yaw speed, and body height.</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Troubleshooting</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Symptom</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Action</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">No <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">unitree_sdk2py</code> imports</td><td class="p-2.5">Activate <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">unitree_env</code> and install the package</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ChannelSubscriber</code> fails</td><td class="p-2.5">Verify <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ChannelFactoryInitialize</code> interface argument and network</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Trajectory does not execute</td><td class="p-2.5">Confirm <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">TrajectoryFollow</code> return value and robot mode; ensure <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ClassicWalk(True)</code> completed</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Robot does not stop</td><td class="p-2.5">Use menu option 2 to exit; verify <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ClassicWalk(False)</code> is called</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Deliverable</h4></div>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Short video or screenshots showing robot executing the autonomous trajectory and final stance</li><li>One paragraph describing each path segment and how the trajectory commands affect motion</li><li>Confirmation that the robot returned to normal mode or remote controller after the exercise</li></ul>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Previous Lab</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3"><a href="../lab-03/" class="text-primary underline hover:text-primary/80">Lab 3 — B2 Stand Sequence (Low-Level Joint Control)</a> — Direct joint position control via <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">rt/lowcmd</code>.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">References</h4></div>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><a href="lab04_b2_trajectory.py" class="text-primary underline hover:text-primary/80">lab04_b2_trajectory.py</a></li><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">vendor/unitree_sdk2_python/example/b2/b2_trajectory_follow.py</code></li></ul>"""

    return {
        "id": "lab-04",
        "title": "B2 Trajectory Following (Autonomous Path)",
        "content": content,
        "code_files": [
            {"name": "lab04_b2_trajectory.py", "code": script}
        ]
    }


# ── Main ────────────────────────────────────────────────────────────────

def main():
    print(f"Reading syllabus from: {SYLLABUS_PATH}")
    with open(SYLLABUS_PATH) as f:
        syllabus = json.load(f)

    if "03" not in syllabus:
        print("ERROR: Day 03 not found in syllabus")
        sys.exit(1)

    day03 = syllabus["03"]
    if "labs" not in day03:
        print("ERROR: No labs array in Day 03")
        sys.exit(1)

    print(f"Found {len(day03['labs'])} labs in Day 03")

    builders = {
        "lab-00": build_lab00,
        "lab-01": build_lab01,
        "lab-02": build_lab02,
        "lab-03": build_lab03,
        "lab-04": build_lab04,
    }

    new_labs = []
    for lab in day03["labs"]:
        lab_id = lab.get("id", "")
        if lab_id in builders:
            print(f"  Building {lab_id}...")
            new_lab = builders[lab_id]()
            new_labs.append(new_lab)
        else:
            print(f"  Keeping {lab_id} as-is (no builder)")
            new_labs.append(lab)

    # Append any new labs (lab-03, lab-04) not in the original array
    existing_ids = {lab.get("id", "") for lab in day03["labs"]}
    for lab_id in ["lab-03", "lab-04"]:
        if lab_id not in existing_ids:
            print(f"  Adding new {lab_id}...")
            new_labs.append(builders[lab_id]())

    day03["labs"] = new_labs

    print(f"\nWriting updated syllabus to: {SYLLABUS_PATH}")
    with open(SYLLABUS_PATH, 'w') as f:
        json.dump(syllabus, f, indent=2, ensure_ascii=False)

    print("Done! Enhanced Day 03 lab workspaces written to syllabus.json")


if __name__ == "__main__":
    main()