#!/usr/bin/env python3
"""
Build enhanced Day 02 lab workspace entries in syllabus.json,
matching the rich HTML format of Day 01 labs.

Reads README.md and script files from Labs/day-02/ and updates
client/src/data/syllabus.json with complete lab content.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SYLLABUS_PATH = REPO / "client" / "src" / "data" / "syllabus.json"
LABS_SRC = REPO / "Labs" / "day-02"


def md_to_html(md: str) -> str:
    """Convert markdown to the HTML format used in syllabus content fields.

    Handles: headings, code blocks, lists, tables, bold, links, images.
    Returns HTML string with step-header and other classes as needed.
    """
    lines = md.split('\n')
    html: list[str] = []
    in_code = False
    in_table = False
    in_list = False
    in_ul = False
    code_buf: list[str] = []
    table_buf: list[str] = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Code block
        if line.strip().startswith('```'):
            if in_code:
                if code_buf:
                    html.append(f'<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">{escape_html("\n".join(code_buf))}</pre>')
                code_buf = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue

        if in_code:
            code_buf.append(line)
            i += 1
            continue

        # Skip empty lines
        if not line.strip():
            if in_table:
                # End table
                if table_buf:
                    html.append(build_table(table_buf))
                table_buf = []
                in_table = False
            if in_list:
                html.append('</ul>')
                in_list = False
            if in_ul:
                html.append('</ul>')
                in_ul = False
            i += 1
            continue

        # Headings
        h1 = re.match(r'^# (.+)$', line)
        h2 = re.match(r'^## (.+)$', line)
        h3 = re.match(r'^### (.+)$', line)
        h4 = re.match(r'^#### (.+)$', line)

        if h1:
            heading = process_inline(h1.group(1))
            html.append(f'<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">{heading}</h4></div>')
            i += 1
            continue
        if h2:
            heading = process_inline(h2.group(1))
            html.append(f'<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">{heading}</h4></div>')
            i += 1
            continue
        if h3:
            heading = process_inline(h3.group(1))
            html.append(f'<p class="text-sm font-bold text-foreground mt-4 mb-2">{heading}</p>')
            i += 1
            continue
        if h4:
            heading = process_inline(h4.group(1))
            html.append(f'<p class="text-xs font-bold text-foreground mt-3 mb-1">{heading}</p>')
            i += 1
            continue

        # Divider
        if line.strip() == '---':
            html.append('<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>')
            i += 1
            continue

        # Table detection
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_buf = []
            table_buf.append(line)
            i += 1
            continue
        elif in_table:
            if table_buf:
                html.append(build_table(table_buf))
            table_buf = []
            in_table = False

        # Unordered list
        ul_match = re.match(r'^- (.+)$', line.strip())
        if ul_match:
            if not in_ul:
                html.append('<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4">')
                in_ul = True
            html.append(f'<li>{process_inline(ul_match.group(1))}</li>')
            i += 1
            continue
        elif in_ul and line.strip():
            pass  # fall through to regular paragraph

        # Numbered list
        ol_match = re.match(r'^\d+\.\s+(.+)$', line.strip())
        if ol_match:
            if not in_list:
                # Check if this is a task-style list (checkboxes)
                text = ol_match.group(1)
                if '[' in text and ']' in text:
                    if not in_ul:
                        html.append('<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4">')
                        in_ul = True
                    clean = process_inline(re.sub(r'\[([ x])\]', '', text).strip())
                    checked = '[x]' in text
                    icon = '✓' if checked else '○'
                    html.append(f'<li><span class="font-mono text-primary mr-1">{icon}</span>{clean}</li>')
                    i += 1
                    continue
                if not in_list:
                    html.append('<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4">')
                    in_list = True
            html.append(f'<li>{process_inline(ol_match.group(1))}</li>')
            i += 1
            continue
        elif in_list:
            html.append('</ol>')
            in_list = False

        # Blockquote
        bq_match = re.match(r'^>\s*(.+)$', line.strip())
        if bq_match:
            html.append(f'<div class="border-l-2 border-primary pl-3 py-1 mb-3 text-xs text-foreground italic">{process_inline(bq_match.group(1))}</div>')
            i += 1
            continue

        # Regular paragraph
        processed = process_inline(line.strip())
        if processed:
            html.append(f'<p class="text-xs text-muted-foreground leading-relaxed mb-3">{processed}</p>')
        i += 1

    # Close any open elements
    if in_code and code_buf:
        html.append(f'<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">{escape_html("\n".join(code_buf))}</pre>')
    if in_table and table_buf:
        html.append(build_table(table_buf))
    if in_list:
        html.append('</ol>')
    if in_ul:
        html.append('</ul>')

    return '\n'.join(html)


def build_table(lines: list[str]) -> str:
    """Build HTML table from markdown table lines."""
    if len(lines) < 2:
        return ''

    # Parse header
    header_cells = [c.strip() for c in lines[0].split('|') if c.strip()]
    # Skip separator line
    data_lines = [l for l in lines[1:] if '---' not in l and l.strip()]

    rows_html = '<thead><tr class="bg-muted/40">'
    for cell in header_cells:
        rows_html += f'<th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">{process_inline(cell)}</th>'
    rows_html += '</tr></thead><tbody>'

    for i, line in enumerate(data_lines):
        cells = [c.strip() for c in line.split('|') if c.strip()]
        stripe = 'even:bg-muted/20' if i % 2 == 0 else ''
        rows_html += f'<tr class="{stripe} border-b border-border/50">'
        for cell in cells:
            rows_html += f'<td class="p-2.5">{process_inline(cell)}</td>'
        rows_html += '</tr>'
    rows_html += '</tbody>'

    return f'<table class="w-full text-xs border-collapse mb-4">{rows_html}</table>'


def process_inline(text: str) -> str:
    """Process inline markdown: bold, code, links, line breaks."""
    text = escape_html(text)

    # Bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<span class="font-bold text-foreground">\1</span>', text)
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">\1</code>', text)
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" class="text-primary underline hover:text-primary/80">\1</a>', text)
    # <br>
    text = re.sub(r'<br>', '<br/>', text)

    return text


def escape_html(text: str) -> str:
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def read_file(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8')
    except Exception:
        return ''


# ── Lab content definitions ──────────────────────────────────────────────

def build_lab00() -> dict:
    readme = read_file(LABS_SRC / "lab-00" / "README.md")
    script = read_file(LABS_SRC / "lab-00" / "lab00_day2_readiness.py")

    content = """<div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5 text-xs mb-4 p-3 bg-muted/30 border border-border/60 rounded-lg"><div class="flex gap-2"><span class="font-semibold text-foreground">Duration:</span><span>~45–60 min (recap + theory + checks)</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Robot required:</span><span>Optional for Sections A–C; recommended for Section D</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Motion:</span><span>None</span></div></div>

<div class="border border-primary/30 bg-primary/5 rounded-lg p-4 mb-6"><div class="flex items-center gap-2 mb-3"><span class="text-base">🎯</span><span class="text-sm font-bold text-foreground tracking-tight">Learning Objectives</span></div><ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Confirm <span class="font-bold text-foreground">Day 1 artifacts</span> and patrol-related SDK imports are present on your machine.</li><li>Sketch the <span class="font-bold text-foreground">inspection pipeline</span> (sense → log → decide → act → report).</li><li>Fill in a <span class="font-bold text-foreground">patrol scenario card</span> (checkpoints, speed limits, abort rules, deliverables).</li><li>State <span class="font-bold text-foreground">Day 2 safety rules</span> for multi-stop patrol (arena, spotter, avoid API, no SLAM claims).</li><li>Run <span class="font-bold text-foreground">lab00_day2_readiness.py</span> and interpret PASS / PARTIAL / FAIL before Lab 1.</li></ol></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">PDF coverage (Day 2): Design inspection tasks · autonomous routines (planning) · deploy preparation</p>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Prerequisite: Day 1 Labs 0–4 complete (including <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">lab02_safe_posture.py</code> and <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">lab04_obstacle_avoid_intro.py</code>).</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Day 1 Recap</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Day 1 Lab</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Skill</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Day 2 Use</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Lab 1</td><td class="p-2.5">Subscribe <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">rt/sportmodestate</code>, JSONL log</td><td class="p-2.5">Patrol logging</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Lab 2</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">SportClient</code>, CheckMode, stand + walk</td><td class="p-2.5">Stand prep before patrol</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Lab 3</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">VideoClient</code>, inspection bundle</td><td class="p-2.5">Per-checkpoint <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">frame.jpg</code></td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Lab 4</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ObstaclesAvoidClient</code>, increment preview</td><td class="p-2.5">Multi-leg patrol legs</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">Quick re-check (optional):</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-01/lab-00/lab00_readiness.py en6
python course/day-01/lab-03/lab02_sport_readonly.py en6</pre>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Inspection Architecture (Conceptual)</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Day 2 builds a <span class="font-bold text-foreground">scripted inspection loop</span> in a <span class="font-bold text-foreground">known cleared arena</span> — not full SLAM autonomy.</p>

<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">┌──────────┐   ┌──────────┐   ┌─────────────┐   ┌──────────┐   ┌─────────┐
│ Sensors  │──▶│ Log DDS  │──▶│ Scenario /  │──▶│ Patrol   │──▶│ Run     │
│ camera,  │   │ JSONL +  │   │ abort rules │   │ avoid +  │   │ folder  │
│ state    │   │ images   │   │ (this lab)  │   │ capture  │   │ report  │
└──────────┘   └──────────┘   └─────────────┘   └──────────┘   └─────────┘</pre>

<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Stage</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Day 2 Coverage</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Sense</span></td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">sportmodestate</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">lowstate</code>, front camera</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Log</span></td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">sportmodestate.jsonl</code>, checkpoint images (Lab 1 schema)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Decide</span></td><td class="p-2.5">Scenario card + optional SOC / rate rules (Lab 5)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Act</span></td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ObstaclesAvoidClient</code> legs between checkpoints (Labs 2–3)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Report</span></td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">metadata.json</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">patrol_plan.json</code>, presentation (Labs 4–5)</td></tr></tbody></table>

<div class="border-l-2 border-primary pl-3 py-1 mb-3 text-xs text-foreground italic">What Day 2 does <span class="font-bold text-foreground">not</span> do: global map, GPS, Nav2 — those belong to the ROS extension track.</div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Patrol Scenario Worksheet</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Each team maintains one JSON file for the day (used in Labs 2–5).</p>

<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">cd /path/to/vinci-unitree
conda activate unitree_env

python course/day-02/lab-00/lab00_day2_readiness.py \\
  --write-scenario my_team_scenario.json</pre>

<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Field</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Purpose</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">team_name</code> / <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">operator</code></td><td class="p-2.5">Run folder metadata</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">arena</code></td><td class="p-2.5">Size, floor, hazards</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">checkpoints</code></td><td class="p-2.5">≥ 2 stops (<code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">id</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">label</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">marker</code>)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">motion_limits</code></td><td class="p-2.5">Class caps: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">max_forward_vx_mps</code> ≤ <span class="font-bold text-foreground">0.25</span>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">max_increment_dx_m</code> ≤ <span class="font-bold text-foreground">0.5</span></td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">abort_rules</code></td><td class="p-2.5">When spotter / script must stop</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">deliverables</code></td><td class="p-2.5">What you owe at end of day</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">Validate:</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-02/lab-00/lab00_day2_readiness.py \\
  --validate-scenario my_team_scenario.json</pre>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">Expected: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">PASS scenario valid</code>.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Safety — Multi-Stop Patrol</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><span class="font-bold text-foreground">Arena boundary</span> — mark corners with cones; agree who calls halt.</li><li><span class="font-bold text-foreground">One patrol at a time</span> per Go2 on the subnet.</li><li><span class="font-bold text-foreground">Default speed cap</span> — forward <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">vx</code> ≤ <span class="font-bold text-foreground">0.25 m/s</span>; increment <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">dx</code> ≤ <span class="font-bold text-foreground">0.5 m</span> per leg unless instructor signs off.</li><li><span class="font-bold text-foreground">Avoid mode default</span> — patrol legs use <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ObstaclesAvoidClient</code> with <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">SwitchSet(True)</code> and <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">UseRemoteCommandFromApi(True)</code>.</li><li><span class="font-bold text-foreground">Clean shutdown</span> — every patrol script must stop with <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">Move(0,0,0)</code>, release API mode, and <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">SwitchSet(False)</code> on exit or Ctrl+C.</li><li><span class="font-bold text-foreground">Increment goals are local</span> — do not describe Day 2 as "GPS navigation" or "SLAM patrol".</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Hands-On Checklist</h4></div>

<p class="text-sm font-bold text-foreground mt-4 mb-2">A. Machine + Day 1 prerequisite (no robot)</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/vinci-unitree

python course/day-02/lab-00/lab00_day2_readiness.py</pre>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><span class="font-mono text-primary mr-1">○</span> Summary: <span class="font-bold text-foreground">PASS — Day 2 machine ready</span></li><li><span class="font-mono text-primary mr-1">○</span> All Day 1 required scripts reported PASS</li><li><span class="font-mono text-primary mr-1">○</span> <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ObstaclesAvoidClient</code> import PASS</li></ul>

<p class="text-sm font-bold text-foreground mt-4 mb-2">B. Scenario card (no robot)</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-02/lab-00/lab00_day2_readiness.py \\
  --write-scenario my_team_scenario.json
# edit file
python course/day-02/lab-00/lab00_day2_readiness.py \\
  --validate-scenario my_team_scenario.json</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">C. Network (robot powered, PC wired)</p>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><span class="font-mono text-primary mr-1">○</span> <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ping -c 2 192.168.123.161</code> → replies</li><li><span class="font-mono text-primary mr-1">○</span> Session exports: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">CYCLONEDDS_HOME</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">CYCLONEDDS_URI</code> unset</li></ul>

<p class="text-sm font-bold text-foreground mt-4 mb-2">D. Robot readiness (optional but recommended)</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-02/lab-00/lab00_day2_readiness.py en6</pre>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Result</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Meaning</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Next Step</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">PASS</span> (exit 0)</td><td class="p-2.5">DDS + sport OK</td><td class="p-2.5"><a href="../lab-01/" class="text-primary underline hover:text-primary/80">Lab 1</a></td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">PARTIAL</span> (exit 2)</td><td class="p-2.5">DDS OK; unusual CheckMode</td><td class="p-2.5">Lab 1 OK; fix before Lab 2 motion</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">FAIL</span> (exit 1)</td><td class="p-2.5">Network / DDS</td><td class="p-2.5">Field guide; do not run patrol</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Knowledge Check (Self-Test)</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>What is the difference between Day 1's single <span class="font-bold text-foreground">inspection bundle</span> and Day 2's <span class="font-bold text-foreground">run folder</span>?</li><li>Which client commands a forward <span class="font-bold text-foreground">increment</span> leg in avoid mode?</li><li>Name two <span class="font-bold text-foreground">abort rules</span> your team will use.</li><li>Why is increment-based patrol <span class="font-bold text-foreground">not</span> the same as SLAM?</li><li>What is the maximum forward speed your scenario file should use by default?</li></ol>

<div class="border border-amber-500/40 bg-amber-500/10 rounded-lg p-3 mb-4"><span class="font-semibold text-amber-600 dark:text-amber-400 text-xs uppercase tracking-wide">Answers</span><ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mt-2"><li>Day 2 adds <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">patrol_plan.json</code>, multiple <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">checkpoints/</code>, and a full-patrol <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">JSONL</code> — one run, many stops.</li><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ObstaclesAvoidClient.MoveToIncrementPosition(dx, dy, dyaw)</code> (after SwitchSet + UseRemoteCommandFromApi).</li><li>Any two from your scenario (e.g. spotter halt, remote override, low SOC).</li><li>Increment goals are local odometry-style legs in a prepared arena — no global map or localization stack.</li><li><span class="font-bold text-foreground">0.25 m/s</span> unless instructor approves higher in writing.</li></ol></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Deliverable</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Log: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">lab00_day2_readiness.py</code> → <span class="font-bold text-foreground">Day 2 machine ready</span></li><li>Log: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">lab00_day2_readiness.py en6</code> → PASS or PARTIAL (one line why)</li><li>Your validated <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">my_team_scenario.json</code></li><li>One sentence: what your team will capture at each checkpoint</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Next Lab</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3"><a href="../lab-01/" class="text-primary underline hover:text-primary/80">Lab 1 — Run folder schema &amp; bundle validation</a> — Define the standard run directory and validate inspection data — still no patrol motion.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">References</h4></div>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Day 2 overview: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">day-02/README.md</code></li><li>Day 1: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">day-01/README.md</code></li><li>Script: <a href="lab00_day2_readiness.py" class="text-primary underline hover:text-primary/80">lab00_day2_readiness.py</a></li><li>Field guide: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">docs/GO2-FIELD-GUIDE.md</code></li></ul>"""

    return {
        "id": "lab-00",
        "title": "Lab 0 — Readiness & Inspection Scenario",
        "content": content,
        "code_files": [
            {
                "name": "lab00_day2_readiness.py",
                "code": script
            }
        ]
    }


def build_lab01() -> dict:
    validator_script = read_file(LABS_SRC / "lab-01" / "lab01_validate_run_folder.py")
    scaffold_script = read_file(LABS_SRC / "lab-01" / "lab01_scaffold_run_folder.py")

    content = """<div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5 text-xs mb-4 p-3 bg-muted/30 border border-border/60 rounded-lg"><div class="flex gap-2"><span class="font-semibold text-foreground">Duration:</span><span>~45 min</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Robot required:</span><span>No</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Motion:</span><span>None</span></div></div>

<div class="border border-primary/30 bg-primary/5 rounded-lg p-4 mb-6"><div class="flex items-center gap-2 mb-3"><span class="text-base">🎯</span><span class="text-sm font-bold text-foreground tracking-tight">Learning Objectives</span></div><ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Describe the <span class="font-bold text-foreground">Day 2 run folder</span> layout and how it extends the Day 1 single-checkpoint bundle.</li><li>Author <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">metadata.json</code> and <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">patrol_plan.json</code> that Lab 3's runner will consume.</li><li>Validate a run directory with <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">lab01_validate_run_folder.py</code> (PASS / FAIL).</li><li>Scaffold a dry-run folder from your Lab 0 scenario with <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">lab01_scaffold_run_folder.py</code>.</li></ol></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">PDF coverage: Managing sensor data · inspection task design (data layout)</p>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Prerequisites: <a href="../lab-00/" class="text-primary underline hover:text-primary/80">Lab 0</a> complete (<code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">my_team_scenario.json</code> validated).</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Concepts: Day 1 Bundle vs Day 2 Run Folder</h4></div>

<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border"></th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Day 1 (<code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">lab03_capture_inspection.py</code>)</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Day 2 (patrol run)</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Scope</span></td><td class="p-2.5">One checkpoint</td><td class="p-2.5">Many checkpoints + legs</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Image</span></td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">frame_001.jpg</code> at root</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">checkpoints/&lt;id&gt;/frame.jpg</code></td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Plan</span></td><td class="p-2.5">Notes in <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">metadata.json</code> only</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">patrol_plan.json</code> (legs + dwell)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">State log</span></td><td class="p-2.5">Short <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">sportmodestate.jsonl</code></td><td class="p-2.5">Full-patrol JSONL (+ optional per-CP slices)</td></tr></tbody></table>

<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">run_YYYYMMDD_HHMM/
  metadata.json           # who, when, robot, CheckMode, checkpoint id list
  patrol_plan.json        # checkpoints + legs (increment / velocity)
  sportmodestate.jsonl    # one JSON object per line (DDS-style log)
  checkpoints/
    cp_A/
      frame.jpg           # front camera at this stop
      state_slice.jsonl   # optional — window around capture
    cp_B/
      ...</pre>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">Treat this folder as the <span class="font-bold text-foreground">inspection deliverable</span> for Day 2 team presentations.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">metadata.json (Required Fields)</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Field</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Purpose</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">schema_version</code></td><td class="p-2.5">Camp format version (<code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">1</code>)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">created_utc</code></td><td class="p-2.5">ISO-8601 timestamp</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">operator</code></td><td class="p-2.5">Human or team operator</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">team_name</code></td><td class="p-2.5">Optional — from scenario</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">interface</code></td><td class="p-2.5">NIC used on hardware run</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">checkpoints</code></td><td class="p-2.5">List of checkpoint ids (should match plan)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">check_mode</code></td><td class="p-2.5">From MotionSwitcherClient on capture</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">artifacts</code></td><td class="p-2.5">Map of filenames in this folder</td></tr></tbody></table>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">patrol_plan.json Leg Types</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Type</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Meaning</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">increment</code></td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ObstaclesAvoidClient.MoveToIncrementPosition(dx, dy, dyaw)</code></td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">velocity</code></td><td class="p-2.5">Timed <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">Move(vx, vy, vyaw)</code> at ~20 Hz</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">dwell</code></td><td class="p-2.5">Wait at checkpoint</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Scripts</h4></div>

<p class="text-sm font-bold text-foreground mt-4 mb-2">lab01_validate_run_folder.py</p>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Argument</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Purpose</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">run_dir</code></td><td class="p-2.5">Folder to check</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--scenario PATH</code></td><td class="p-2.5">Cross-check checkpoint ids with Lab 0 scenario</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--relax-images</code></td><td class="p-2.5">Allow missing <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">frame.jpg</code> (scaffold / dry-run)</td></tr></tbody></table>

<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">cd /path/to/vinci-unitree

# Instructor fixture — should PASS
python course/day-02/lab-01/lab01_validate_run_folder.py \\
  course/day-02/lab-01/fixtures/sample_run_pass

# Broken fixture — should FAIL (exercise)
python course/day-02/lab-01/lab01_validate_run_folder.py \\
  course/day-02/lab-01/fixtures/sample_run_incomplete</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">lab01_scaffold_run_folder.py</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-02/lab-01/lab01_scaffold_run_folder.py \\
  course/day-02/lab-00/my_team_scenario.json

python course/day-02/lab-01/lab01_scaffold_run_folder.py \\
  course/day-02/lab-00/my_team_scenario.json \\
  --out-dir ./run_dry_team_a --increment-dx 0.4</pre>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Hands-On Steps</h4></div>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 1 — Validate the passing fixture</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">conda activate unitree_env
cd /path/to/vinci-unitree

python course/day-02/lab-01/lab01_validate_run_folder.py \\
  course/day-02/lab-01/fixtures/sample_run_pass</pre>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Expected: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">Summary: PASS — run folder valid</code>. Open the fixture and map files to the diagram.</p>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 2 — Find failures in the incomplete fixture</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-02/lab-01/lab01_validate_run_folder.py \\
  course/day-02/lab-01/fixtures/sample_run_incomplete</pre>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Expected: multiple FAIL lines. In your notebook, list each error and which file you would fix.</p>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 3 — Scaffold from your scenario</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-02/lab-01/lab01_scaffold_run_folder.py \\
  course/day-02/lab-00/my_team_scenario.json \\
  --out-dir ./run_dry_$(whoami)

python course/day-02/lab-01/lab01_validate_run_folder.py ./run_dry_$(whoami) \\
  --relax-images \\
  --scenario course/day-02/lab-00/my_team_scenario.json</pre>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Expected: PASS with warnings about missing images (OK until Lab 3).</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Deliverable</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Log: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">lab01_validate_run_folder.py fixtures/sample_run_pass</code> → <span class="font-bold text-foreground">PASS</span></li><li>Log: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">lab01_validate_run_folder.py fixtures/sample_run_incomplete</code> → <span class="font-bold text-foreground">FAIL</span> (paste error list)</li><li>Path to your <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">run_dry_*</code> folder + validator output with <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--relax-images</code></li><li>Copy of your <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">patrol_plan.json</code> (or diff from template)</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Next Lab</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3"><a href="../lab-02/" class="text-primary underline hover:text-primary/80">Lab 2 — Obstacle Avoidance &amp; Local Motion APIs</a> — Supervised motion between checkpoints with <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ObstaclesAvoidClient</code>.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">References</h4></div>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Day 2 overview: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">../README.md</code></li><li>Lab 0 scenario: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">../lab-00/patrol_scenario.template.json</code></li><li>Scripts: <a href="lab01_validate_run_folder.py" class="text-primary underline hover:text-primary/80">lab01_validate_run_folder.py</a> · <a href="lab01_scaffold_run_folder.py" class="text-primary underline hover:text-primary/80">lab01_scaffold_run_folder.py</a></li></ul>"""

    return {
        "id": "lab-01",
        "title": "Lab 1 — Run-Folder Schema & Bundle Validation",
        "content": content,
        "code_files": [
            {"name": "lab01_validate_run_folder.py", "code": validator_script},
            {"name": "lab01_scaffold_run_folder.py", "code": scaffold_script}
        ]
    }


def build_lab02() -> dict:
    avoid_script = read_file(LABS_SRC / "lab-02" / "lab04_obstacle_avoid_intro.py")
    patrol_helpers = read_file(LABS_SRC / "go2_patrol_helpers.py")

    content = """<div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5 text-xs mb-4 p-3 bg-muted/30 border border-border/60 rounded-lg"><div class="flex gap-2"><span class="font-semibold text-foreground">Duration:</span><span>~60 min (20 min theory + 40 min hands-on)</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Robot required:</span><span>Yes — short supervised forward move with avoidance on</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Motion:</span><span>Yes (supervised)</span></div></div>

<div class="border border-primary/30 bg-primary/5 rounded-lg p-4 mb-6"><div class="flex items-center gap-2 mb-3"><span class="text-base">🎯</span><span class="text-sm font-bold text-foreground tracking-tight">Learning Objectives</span></div><ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Sketch the <span class="font-bold text-foreground">SLAM / navigation pipeline</span> and what Go2 covers today vs ROS later.</li><li>Use <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ObstaclesAvoidClient</code> (<code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">SwitchSet</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">Move</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">UseRemoteCommandFromApi</code>).</li><li>Contrast <span class="font-bold text-foreground">reactive avoidance</span> with <span class="font-bold text-foreground">global path planning</span> (ROS / Nav2).</li><li>Run <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">lab04_obstacle_avoid_intro.py</code> safely and stop cleanly.</li></ol></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">PDF coverage: SLAM (introduction) · path planning · obstacle avoidance</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Concepts — Python SDK Avoidance</h4></div>

<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">API</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Module</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Role</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ObstaclesAvoidClient</code></td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">unitree_sdk2py.go2.obstacles_avoid</code></td><td class="p-2.5">Dedicated avoid service — <span class="font-bold text-foreground">this lab</span></td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">SportClient.FreeAvoid</code></td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">go2.sport</code></td><td class="p-2.5">Sport-menu toggle</td></tr></tbody></table>

<p class="text-sm font-bold text-foreground mt-4 mb-2">ObstaclesAvoidClient Pattern (from upstream)</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.obstacles_avoid.obstacles_avoid_client import ObstaclesAvoidClient

ChannelFactoryInitialize(0, "en6")
client = ObstaclesAvoidClient()
client.SetTimeout(3.0)
client.Init()

client.SwitchSet(True)
client.UseRemoteCommandFromApi(True)
client.Move(0.2, 0.0, 0.0)   # repeat ~20–50 Hz while moving
# ...
client.Move(0.0, 0.0, 0.0)
client.UseRemoteCommandFromApi(False)
client.SwitchSet(False)</pre>

<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Method</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Purpose</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">SwitchSet(True/False)</code></td><td class="p-2.5">Enable / disable onboard avoid processor</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">SwitchGet()</code></td><td class="p-2.5">Read enable state</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">UseRemoteCommandFromApi(True)</code></td><td class="p-2.5">Take velocity from API (not only remote)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">Move(vx, vy, vyaw)</code></td><td class="p-2.5">Velocity in avoid mode (<code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">_CallNoReply</code> — send repeatedly)</td></tr></tbody></table>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Safety</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><span class="font-bold text-foreground">Cones or boxes</span> in a small course — not people.</li><li>Default <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">vx=0.2</code> m/s — do not exceed ~0.25 in class without instructor approval.</li><li>Spotter + estop; <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">Ctrl+C</code> runs cleanup in the camp script.</li><li>Avoidance ≠ SLAM ≠ full autonomy.</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Hands-On</h4></div>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 0 — Session &amp; readiness</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/vinci-unitree
python course/day-01/lab-03/lab02_sport_readonly.py en6</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 1 — Dry-run (no motion)</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-02/lab-02/lab04_obstacle_avoid_intro.py en6 --dry-run</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 2 — Camp scripted move (supervised)</p>
<p class="text-xs text-muted-foreground leading-relaxed mb-3"><span class="font-bold text-foreground">Real terminal</span> required (<code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">yes</code> prompt):</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-02/lab-02/lab04_obstacle_avoid_intro.py en6</pre>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">Visible motion sequence: StandUp → BalanceStand → Enable avoid → Move(0.3,0,0) for 3s → Stop → Disable avoid.</p>

<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Flag</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Purpose</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--vx</code></td><td class="p-2.5">Forward speed (default 0.3 m/s)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--move-sec</code></td><td class="p-2.5">Move duration (default 3s)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--dry-run</code></td><td class="p-2.5">Plan only</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">-y</code></td><td class="p-2.5">Skip prompt (instructor)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--increment-move</code></td><td class="p-2.5">After velocity move, use MoveToIncrementPosition</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--compare-free-avoid</code></td><td class="p-2.5">Toggle SportClient.FreeAvoid vs dedicated avoid client</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">Expected: numbered steps ending in <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">Summary: PASS</code>.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Exercises</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Draw the pipeline diagram and circle the box Lab 4 implements.</li><li>Why must <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">Move()</code> be sent periodically instead of once? (<code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">_CallNoReply</code> — sport/avoid stacks expect continuous velocity stream)</li><li>Name one difference between <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">ObstaclesAvoidClient.Move</code> and <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">SportClient.Move</code>.</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Troubleshooting</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Symptom</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Action</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">FAIL: could not enable obstacle avoidance</td><td class="p-2.5">Firmware / mode; try sport menu first; re-run Lab 2</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Robot does not move</td><td class="p-2.5">UseRemoteCommandFromApi(True)? Switch on? Standing?</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Will not stop</td><td class="p-2.5">Ctrl+C (script cleanup); remote estop</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Moves too fast</td><td class="p-2.5">Lower --vx (e.g. 0.15)</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Deliverable</h4></div>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Log snippet: dry-run plan + motion run ending in <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">Summary: PASS</code></li><li>Answers to Exercises 1–3</li><li>One sentence: what you would add in Day 2 for "inspection patrol"</li></ul>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Next Lab</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3"><a href="../lab-03/" class="text-primary underline hover:text-primary/80">Lab 3 — Sensor Integration &amp; Data Management</a> — Camera capture, platform probe, and inspection bundle.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">References</h4></div>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><a href="lab04_obstacle_avoid_intro.py" class="text-primary underline hover:text-primary/80">lab04_obstacle_avoid_intro.py</a></li><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">vendor/unitree_sdk2_python/example/obstacles_avoid/</code></li><li><a href="https://support.unitree.com/home/en/developer/ObstaclesAvoidClient" class="text-primary underline hover:text-primary/80">ObstaclesAvoidClient docs</a></li><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">docs/GO2-FIELD-GUIDE.md</code></li></ul>"""

    return {
        "id": "lab-02",
        "title": "Lab 2 — Obstacle Avoidance & Local Motion APIs",
        "content": content,
        "code_files": [
            {"name": "lab04_obstacle_avoid_intro.py", "code": avoid_script},
            {"name": "go2_patrol_helpers.py", "code": patrol_helpers}
        ]
    }


def build_lab03() -> dict:
    capture_script = read_file(LABS_SRC / "lab-03" / "lab03_capture_inspection.py")
    probe_script = read_file(LABS_SRC / "lab-03" / "lab03_platform_probe.py")

    content = """<div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5 text-xs mb-4 p-3 bg-muted/30 border border-border/60 rounded-lg"><div class="flex gap-2"><span class="font-semibold text-foreground">Duration:</span><span>~45 min</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Robot required:</span><span>Yes (camera RPC, DDS state)</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Motion:</span><span>None</span></div></div>

<div class="border border-primary/30 bg-primary/5 rounded-lg p-4 mb-6"><div class="flex items-center gap-2 mb-3"><span class="text-base">🎯</span><span class="text-sm font-bold text-foreground tracking-tight">Learning Objectives</span></div><ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Name <span class="font-bold text-foreground">onboard sensor paths</span> in the Python SDK (camera RPC, DDS state, optional lidar/wireless).</li><li>Capture a <span class="font-bold text-foreground">front camera</span> frame with <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">VideoClient</code> and save it to disk.</li><li>Build a small <span class="font-bold text-foreground">inspection data bundle</span> (<code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">metadata.json</code> + image + optional state log).</li><li>Explain what an inspector would look for in the saved image and metadata.</li></ol></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">PDF coverage: Integrating sensors · managing sensor data</p>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Prerequisites: <a href="../lab-02/" class="text-primary underline hover:text-primary/80">Lab 2</a> complete (sport RPC readiness).</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Concepts — Go2 Sensors in This Track</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Source</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">API</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">This Lab</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Front camera</span></td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">VideoClient.GetImageSample()</code></td><td class="p-2.5"><span class="font-bold text-foreground">Primary</span></td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Sport / gait state</span></td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">rt/sportmodestate</code></td><td class="p-2.5">Short JSONL log</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Proprioception</span></td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">rt/lowstate</code></td><td class="p-2.5">Optional attach</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">UT lidar</span></td><td class="p-2.5">DDS <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">rt/utlidar/switch</code></td><td class="p-2.5">Platform probe</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><span class="font-bold text-foreground">Onboard services</span></td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">RobotStateClient.ServiceList()</code></td><td class="p-2.5">Platform probe</td></tr></tbody></table>

<div class="border-l-2 border-primary pl-3 py-1 mb-3 text-xs text-foreground italic"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">VideoClient</code> is <span class="font-bold text-foreground">RPC</span> (like <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">SportClient</code>), not a DDS video topic. You pull JPEG/binary samples in a loop and decode with OpenCV.</div>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Minimal VideoClient excerpt</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">from unitree_sdk2py.go2.video.video_client import VideoClient
import cv2, numpy as np

ChannelFactoryInitialize(0, "en6")
client = VideoClient()
client.SetTimeout(3.0); client.Init()

code, data = client.GetImageSample()
while code == 0:
    code, data = client.GetImageSample()
    img = cv2.imdecode(np.frombuffer(bytes(data), np.uint8), cv2.IMREAD_COLOR)
    cv2.imshow("front_camera", img)
    if cv2.waitKey(20) == 27: break
cv2.imwrite("front_image.jpg", img)</pre>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Inspection Data Bundle</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">File</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Purpose</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">metadata.json</code></td><td class="p-2.5">Who, when, robot id, NIC, CheckMode, artifact names</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">frame_001.jpg</code></td><td class="p-2.5">Visual checkpoint of the scene</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">sportmodestate.jsonl</code></td><td class="p-2.5">Optional 5–10s context (mode, velocity, …)</td></tr></tbody></table>

<p class="text-sm font-bold text-foreground mt-4 mb-2">What to look for in the image</p>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Check</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Why it matters</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Clear floor / obstacles</td><td class="p-2.5">Safe path for patrol</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Lighting / glare</td><td class="p-2.5">Vision and human review quality</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Expected scene</td><td class="p-2.5">Wrong room = wrong mission</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Robot visible parts</td><td class="p-2.5">Confirms camera aim and focus</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Hands-On</h4></div>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 1 — Session</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/vinci-unitree
python course/day-01/lab-03/lab02_sport_readonly.py en6</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 2 — Capture bundle (headless-friendly)</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-02/lab-03/lab03_capture_inspection.py en6 \\
  --operator "Your Name" --robot-id go2-lab-1</pre>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Expected: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">frame_001.jpg</code> saved, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">sportmodestate.jsonl</code> written, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">metadata.json</code> created.</p>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 3 — Platform probe (more SDK clients)</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-02/lab-03/lab03_platform_probe.py en6
python course/day-02/lab-03/lab03_platform_probe.py en6 --json-out probe.json</pre>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">———-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Exercises</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Open <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">frame_001.jpg</code> and write two sentences: what is visible, and one risk for an inspection mission.</li><li>Compare <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">metadata.json</code> <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">created_utc</code> with the first line of <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">sportmodestate.jsonl</code>. Are they close enough for a report footnote?</li><li>If <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">GetImageSample</code> fails, list three checks from Lab 0 / field guide before blaming the script.</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Deliverable</h4></div>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">metadata.json</code></li><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">frame_001.jpg</code></li><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">sportmodestate.jsonl</code> (if generated)</li><li>Short answers to Exercises 1–2</li></ul>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Next Lab</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3"><a href="../lab-04/" class="text-primary underline hover:text-primary/80">Lab 4 — Multi-Leg Patrol &amp; Increment Goals</a> — Supervised motion between checkpoints with <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">MoveToIncrementPosition</code>.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">References</h4></div>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><a href="lab03_capture_inspection.py" class="text-primary underline hover:text-primary/80">lab03_capture_inspection.py</a></li><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">vendor/unitree_sdk2_python/example/go2/front_camera/camera_opencv.py</code></li><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">docs/GO2-FIELD-GUIDE.md</code></li></ul>"""

    return {
        "id": "lab-03",
        "title": "Lab 3 — Sensor Integration & Data Management",
        "content": content,
        "code_files": [
            {"name": "lab03_capture_inspection.py", "code": capture_script},
            {"name": "lab03_platform_probe.py", "code": probe_script}
        ]
    }


def build_lab04() -> dict:
    patrol_script = read_file(LABS_SRC / "lab-04" / "lab02_increment_patrol.py")

    content = """<div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5 text-xs mb-4 p-3 bg-muted/30 border border-border/60 rounded-lg"><div class="flex gap-2"><span class="font-semibold text-foreground">Duration:</span><span>~60 min</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Robot required:</span><span>Yes — supervised increment legs under obstacle avoidance</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Motion:</span><span>Yes (supervised)</span></div></div>

<div class="border border-primary/30 bg-primary/5 rounded-lg p-4 mb-6"><div class="flex items-center gap-2 mb-3"><span class="text-base">🎯</span><span class="text-sm font-bold text-foreground tracking-tight">Learning Objectives</span></div><ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Run a <span class="font-bold text-foreground">multi-leg patrol</span> from <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">patrol_plan.json</code> (not a single timed <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">Move</code>).</li><li>Use <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">MoveToIncrementPosition(dx, dy, dyaw)</code> between checkpoints with avoid enabled.</li><li>Apply <span class="font-bold text-foreground">scenario motion limits</span> and class speed caps.</li><li>Tune <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--leg-wait</code> when a leg stops short of the cone.</li></ol></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">Prerequisites: Lab 0 · Lab 1 · Day 1 Labs 2 &amp; 4 (stand + avoid intro).</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Concepts — Increment Leg vs Day 1 Velocity Move</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border"></th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Day 1 Lab 4</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Day 2 Lab 4</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Command</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">Move(vx,0,0)</code> for N seconds</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">MoveToIncrementPosition(dx,dy,dyaw)</code> repeated</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Goal</td><td class="p-2.5">"move forward ~3s"</td><td class="p-2.5">"move ~0.4m toward next cone"</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Plan</td><td class="p-2.5">Hard-coded in script</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">patrol_plan.json</code></td></tr></tbody></table>

<div class="border-l-2 border-primary pl-3 py-1 mb-3 text-xs text-foreground italic">Increment goals use the onboard avoid stack in <span class="font-bold text-foreground">mode=1</span> (SDK). They are <span class="font-bold text-foreground">local</span> — not GPS or SLAM. Stay in a prepared cone course.</div>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Patrol Sequence</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">StandUp → BalanceStand
  → SwitchSet(True) → UseRemoteCommandFromApi(True)
  → for each leg in plan:
        MoveToIncrementPosition … (repeat ~10 Hz for leg-wait)
        dwell at to_checkpoint
  → Move(0,0,0) → API off → SwitchSet(False)</pre>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Patrol Plan — L-Shaped Cone Course</h4></div>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">        [cp_C] blue
          ↑
          |  leg 3: dx=0.3 forward
          |
[cp_B] yellow — turn ~0.6 rad at B (leg 2)
          |
          |  leg 1: dx=0.3 forward
          |
[cp_A] red (dog starts facing toward B)</pre>

<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Leg</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Type</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Goal</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">1</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">increment</code> dx=0.3, dyaw=0</td><td class="p-2.5">A → B (straight)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">2</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">increment</code> dyaw=0.6, dx=0</td><td class="p-2.5">Turn in place at B (~34°)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">3</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">increment</code> dx=0.3, dyaw=0</td><td class="p-2.5">B → C (straight after turn)</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Script Flags — lab02_increment_patrol.py</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Flag</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Purpose</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">en6</code></td><td class="p-2.5">Ethernet interface</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--plan PATH</code></td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">patrol_plan.json</code> (default: cone course)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--scenario PATH</code></td><td class="p-2.5">Clamp legs to Lab 0 motion_limits</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--dry-run</code></td><td class="p-2.5">Print steps only</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--leg-wait SEC</code></td><td class="p-2.5">Settle time after each leg (default 5s)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--skip-stand</code></td><td class="p-2.5">Only if already standing</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">-y</code></td><td class="p-2.5">Skip confirmation (instructor)</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">Class caps (enforced with <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--scenario</code>): forward increment ≤ <span class="font-bold text-foreground">0.5 m</span>, prefer 0.4 m.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Safety</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><span class="font-bold text-foreground">Cone course</span> — 3 markers in a cleared lane; no people inside during motion.</li><li><span class="font-bold text-foreground">Spotter</span> walks with the dog; one patrol at a time per Go2.</li><li><span class="font-bold text-foreground">Stop</span> — Ctrl+C runs cleanup (stop move, avoid off).</li><li>Do not chain large <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">dx</code> values without instructor approval.</li><li>If the dog enters <span class="font-bold text-foreground">damp</span>, recover per field guide before retrying.</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Hands-On</h4></div>
<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 0 — Session</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">conda activate unitree_env
export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
unset CYCLONEDDS_URI
cd /path/to/vinci-unitree
python course/day-02/lab-00/lab00_day2_readiness.py en6</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 1 — Dry-run</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-02/lab-04/lab02_increment_patrol.py en6 --dry-run</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 2 — First patrol (supervised)</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-02/lab-04/lab02_increment_patrol.py en6</pre>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Expected: stand visible → short forward motion per leg → stop clean; console ends with <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">Summary: PASS</code>.</p>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 3 — Tune if needed</p>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Symptom</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Try</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Stops short of cone</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--leg-wait 10</code> or reduce <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">dx</code> in plan to 0.3</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Overshoots</td><td class="p-2.5">Reduce <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">dx</code> to 0.3</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">No motion</td><td class="p-2.5">Day 1 avoid checklist; app sport mode; SwitchGet true</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Turns wrong</td><td class="p-2.5">Adjust <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">dyaw</code> on turn leg</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Deliverable</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Log: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--dry-run</code> output (leg summary)</li><li>Log: hardware run → <span class="font-bold text-foreground">PASS</span> or describe tuning</li><li>Your <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">patrol_plan.json</code> used</li><li>Photo of cone layout (optional)</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Next Lab</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3"><a href="../lab-05/" class="text-primary underline hover:text-primary/80">Lab 5 — Integrated Patrol Runner &amp; Capture</a> — Same legs plus <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">VideoClient</code> and run-folder output.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">References</h4></div>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><a href="lab02_increment_patrol.py" class="text-primary underline hover:text-primary/80">lab02_increment_patrol.py</a></li><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">../go2_patrol_helpers.py</code></li><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">vendor/.../obstacles_avoid/obstacles_avoid_move.py</code></li></ul>"""

    return {
        "id": "lab-04",
        "title": "Lab 4 — Multi-Leg Patrol & Integrated Runner",
        "content": content,
        "code_files": [
            {"name": "lab02_increment_patrol.py", "code": patrol_script}
        ]
    }


def build_lab05() -> dict:
    runner_script = read_file(LABS_SRC / "lab-05" / "lab03_patrol_runner.py")

    content = """<div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5 text-xs mb-4 p-3 bg-muted/30 border border-border/60 rounded-lg"><div class="flex gap-2"><span class="font-semibold text-foreground">Duration:</span><span>~75–90 min</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Robot required:</span><span>Yes — patrol + stop to capture images</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Motion:</span><span>Yes (supervised)</span></div></div>

<div class="border border-primary/30 bg-primary/5 rounded-lg p-4 mb-6"><div class="flex items-center gap-2 mb-3"><span class="text-base">🎯</span><span class="text-sm font-bold text-foreground tracking-tight">Learning Objectives</span></div><ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Run <span class="font-bold text-foreground">patrol + logging + camera</span> in one script (<code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">lab03_patrol_runner.py</code>).</li><li>Produce a complete <span class="font-bold text-foreground">run folder</span> valid for <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">lab01_validate_run_folder.py</code>.</li><li>Relate <span class="font-bold text-foreground">checkpoint capture</span> to virtual plan IDs (still not vision-based navigation).</li><li>Inspect <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">metadata.json</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">sportmodestate.jsonl</code>, and per-checkpoint <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">frame.jpg</code>.</li></ol></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">Prerequisites: Lab 4 on hardware · Lab 1 run-folder schema.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Concepts — What Lab 5 Adds to Lab 4</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Lab 4</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Lab 5</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Motion only</td><td class="p-2.5">Motion + <span class="font-bold text-foreground">data product</span></td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Console PASS</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">run_YYYYMMDD_HHMM/</code> on disk</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">—</td><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">VideoClient</code> at cp_A (start) and after each leg at to_checkpoint</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">—</td><td class="p-2.5">Continuous <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">sportmodestate.jsonl</code> during patrol</td></tr></tbody></table>

<div class="border-l-2 border-primary pl-3 py-1 mb-3 text-xs text-foreground italic">Navigation is still <span class="font-bold text-foreground">open loop</span> from <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">patrol_plan.json</code>. The camera records <span class="font-bold text-foreground">what the dog saw when stopped</span> — it does not steer toward cone colors.</div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Script — lab03_patrol_runner.py</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Flag</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Purpose</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">en6</code></td><td class="p-2.5">Ethernet interface</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--plan PATH</code></td><td class="p-2.5">Default: cone course patrol plan</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--out-dir PATH</code></td><td class="p-2.5">Run root (default <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">run_&lt;UTC&gt;/</code>)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--dry-run</code></td><td class="p-2.5">Print sequence only</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--no-capture</code></td><td class="p-2.5">Patrol without camera (debug motion)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--validate</code></td><td class="p-2.5">Run Lab 1 validator after patrol</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--camera-wait SEC</code></td><td class="p-2.5">Max wait per frame (default 15)</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">-y</code></td><td class="p-2.5">Skip confirmation</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Hands-On</h4></div>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 1 — Dry-run</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-02/lab-05/lab03_patrol_runner.py en6 --dry-run</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 2 — Full patrol + capture</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-02/lab-05/lab03_patrol_runner.py en6 -y --validate</pre>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Expected: Stand up → Capture cp_A → Patrol legs → Capture after each leg → Write metadata + validator PASS.</p>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 3 — Inspect artifacts</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">RUN=run_XXXXX   # your folder
ls -R "$RUN"
open "$RUN/checkpoints/cp_A/frame.jpg"    # macOS
head -3 "$RUN/sportmodestate.jsonl"
cat "$RUN/metadata.json"</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 4 — Validate manually</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-02/lab-01/lab01_validate_run_folder.py "$RUN"</pre>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Exercises</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Run with <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--no-capture</code> then compare time and behaviour vs full run.</li><li>Open three <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">frame.jpg</code> files — what changed between cp_A and cp_C?</li><li>One sentence: what an inspector learns from images that JSONL alone does not provide.</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Deliverable</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Path to your <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">run_*</code> folder</li><li>Validator log → <span class="font-bold text-foreground">PASS</span> (or explain missing frames)</li><li>One <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">frame.jpg</code> screenshot (any checkpoint)</li><li>One line from <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">metadata.json</code> (<code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">check_mode</code>, <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">checkpoints</code>)</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Troubleshooting</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Issue</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Check</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">No frame.jpg</td><td class="p-2.5">VideoClient / robot video service; increase --camera-wait</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Validator FAIL</td><td class="p-2.5">Re-run with --validate; ensure captures succeeded</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Same as Lab 4 motion</td><td class="p-2.5">Expected — plan unchanged; only adds capture pauses</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Next Lab</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3"><a href="../lab-06/" class="text-primary underline hover:text-primary/80">Lab 6 — Field Trial, Tuning &amp; Gazebo Context</a> — Formal test plan, tuning notes, and debrief.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">References</h4></div>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><a href="lab03_patrol_runner.py" class="text-primary underline hover:text-primary/80">lab03_patrol_runner.py</a></li><li>Lab 4: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">../lab-02/</code> · Lab 1: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">../lab-01/</code></li></ul>"""

    return {
        "id": "lab-05",
        "title": "Lab 5 — Field Trial, Tuning & Gazebo Context",
        "content": content,
        "code_files": [
            {"name": "lab03_patrol_runner.py", "code": runner_script}
        ]
    }


def build_lab06() -> dict:
    field_trial_script = read_file(LABS_SRC / "lab-06" / "lab04_field_trial.py")
    tune_script = read_file(LABS_SRC / "lab-06" / "lab04_tune_plan.py")

    content = """<div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5 text-xs mb-4 p-3 bg-muted/30 border border-border/60 rounded-lg"><div class="flex gap-2"><span class="font-semibold text-foreground">Duration:</span><span>~60 min</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Robot required:</span><span>Yes — re-run patrol with tuned plan</span></div><div class="flex gap-2"><span class="font-semibold text-foreground">Motion:</span><span>Yes (supervised)</span></div></div>

<div class="border border-primary/30 bg-primary/5 rounded-lg p-4 mb-6"><div class="flex items-center gap-2 mb-3"><span class="text-base">🎯</span><span class="text-sm font-bold text-foreground tracking-tight">Learning Objectives</span></div><ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li>Turn field observations (short leg, weak turn, wall) into <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">patrol_plan.json</code> edits.</li><li>Run a <span class="font-bold text-foreground">second patrol</span> with the tuned plan via Lab 5.</li><li>Produce <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">field_test.md</code> in the run folder for inspection sign-off.</li><li>Compare baseline vs field-trial runs (motion + captures).</li></ol></div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">Prerequisites: Lab 5 produced at least one baseline <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">run_*</code> folder.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Concepts — Tune → Trial → Report</h4></div>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">Observe (Lab 4/5)  →  lab04_tune_plan.py  →  patrol_plan.tuned.json
                           ↓
                 lab04_field_trial.py  →  lab03_patrol_runner (motion + capture)
                           ↓
                      run_field_* / field_test.md</pre>

<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Symptom</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Typical Tune</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Stops short of cone</td><td class="p-2.5">Increase leg <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">dx</code> or <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">--leg-wait</code></td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Overshoots / hits wall</td><td class="p-2.5">Decrease final leg <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">dx</code></td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Turn too small</td><td class="p-2.5">Increase turn leg <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">dyaw</code></td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Turn too large</td><td class="p-2.5">Decrease <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">dyaw</code></td></tr></tbody></table>

<div class="border-l-2 border-primary pl-3 py-1 mb-3 text-xs text-foreground italic">Tuning is still <span class="font-bold text-foreground">open loop</span> — you are calibrating metres/radians, not using the camera to steer.</div>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Scripts &amp; Templates</h4></div>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">File</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Purpose</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">lab04_tune_plan.py</code></td><td class="p-2.5">Copy plan + apply --set leg:dx:value overrides</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">lab04_field_trial.py</code></td><td class="p-2.5">Run Lab 5 + write field_test.md</td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5"><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">field_test.template.md</code></td><td class="p-2.5">Manual checklist / sign-off</td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Hands-On</h4></div>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 1 — Review baseline (Lab 5)</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">ls -R run_20260526T132200Z
open run_20260526T132200Z/checkpoints/cp_A/frame.jpg
open run_20260526T132200Z/checkpoints/cp_C/frame.jpg</pre>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Note: leg distances, turn angle, wall clearance.</p>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 2 — Tune the plan (no robot)</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-02/lab-06/lab04_tune_plan.py \\
  course/day-02/lab-02/patrol_plan.cone_course.json \\
  --out course/day-02/lab-04/patrol_plan.tuned.json \\
  --set 1:dyaw:0.7 \\
  --set 2:dx:0.25</pre>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 3 — Field trial run</p>
<pre class="bg-muted/50 border border-border rounded-lg p-4 mb-4 overflow-x-auto text-[11px] font-mono leading-relaxed">python course/day-02/lab-06/lab04_field_trial.py en6 -y \\
  --plan course/day-02/lab-04/patrol_plan.tuned.json \\
  --baseline-run run_20260526T132200Z \\
  --cp-results cp_A:pass,cp_B:partial,cp_C:pass \\
  --notes "Stronger turn; shorter final leg to stay off wall"</pre>
<p class="text-xs text-muted-foreground leading-relaxed mb-3">Expected: Full Lab 5 patrol into <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">run_field_&lt;UTC&gt;/</code> with <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">field_test.md</code> and validator PASS.</p>

<p class="text-sm font-bold text-foreground mt-4 mb-2">Step 4 — Debrief (team)</p>
<table class="w-full text-xs border-collapse mb-4"><thead><tr class="bg-muted/40"><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Question</th><th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">Discuss</th></tr></thead><tbody><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">Did tuned run fix the main issue?</td><td class="p-2.5"></td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">One change you would try next</td><td class="p-2.5"></td></tr><tr class="even:bg-muted/20 border-b border-border/50"><td class="p-2.5">What Lab 7 scenario fits your data?</td><td class="p-2.5"></td></tr></tbody></table>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Deliverable</h4></div>
<ol class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">patrol_plan.tuned.json</code> (or diff from cone course)</li><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">run_field_*</code> folder path + validator <span class="font-bold text-foreground">PASS</span></li><li><code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">run_field_*/field_test.md</code></li><li>One sentence: what you tuned and whether it helped</li></ol>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">Next Lab</h4></div>
<p class="text-xs text-muted-foreground leading-relaxed mb-3"><a href="../lab-07/" class="text-primary underline hover:text-primary/80">Lab 7 — Team Capstone &amp; Presentations</a> — Scenario, architecture, run folder evidence, and team demo.</p>

<p class="text-xs text-muted-foreground leading-relaxed mb-3">—-</p>

<div class="step-header mb-6"><h4 class="text-base font-bold text-primary tracking-tight mb-2">References</h4></div>
<ul class="list-disc pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4"><li><a href="lab04_field_trial.py" class="text-primary underline hover:text-primary/80">lab04_field_trial.py</a> · <a href="lab04_tune_plan.py" class="text-primary underline hover:text-primary/80">lab04_tune_plan.py</a></li><li>Lab 5: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">../lab-05/lab03_patrol_runner.py</code></li><li>Field guide: <code class="font-mono text-[10px] bg-muted/60 px-1 py-0.5 rounded text-primary">docs/GO2-FIELD-GUIDE.md</code></li></ul>"""

    return {
        "id": "lab-06",
        "title": "Lab 6 — Team Capstone & Presentations",
        "content": content,
        "code_files": [
            {"name": "lab04_field_trial.py", "code": field_trial_script},
            {"name": "lab04_tune_plan.py", "code": tune_script}
        ]
    }


# ── Main ────────────────────────────────────────────────────────────────

def main():
    print(f"Reading syllabus from: {SYLLABUS_PATH}")
    with open(SYLLABUS_PATH) as f:
        syllabus = json.load(f)

    if "02" not in syllabus:
        print("ERROR: Day 02 not found in syllabus")
        sys.exit(1)

    day02 = syllabus["02"]
    if "labs" not in day02:
        print("ERROR: No labs array in Day 02")
        sys.exit(1)

    print(f"Found {len(day02['labs'])} labs in Day 02")

    # Build enhanced labs
    builders = {
        "lab-00": build_lab00,
        "lab-01": build_lab01,
        "lab-02": build_lab02,
        "lab-03": build_lab03,
        "lab-04": build_lab04,
        "lab-05": build_lab05,
        "lab-06": build_lab06,
    }

    new_labs = []
    for lab in day02["labs"]:
        lab_id = lab.get("id", "")
        if lab_id in builders:
            print(f"  Building {lab_id}...")
            new_lab = builders[lab_id]()
            new_labs.append(new_lab)
        else:
            print(f"  Keeping {lab_id} as-is (no builder)")
            new_labs.append(lab)

    day02["labs"] = new_labs

    # Write back
    print(f"\nWriting updated syllabus to: {SYLLABUS_PATH}")
    with open(SYLLABUS_PATH, 'w') as f:
        json.dump(syllabus, f, indent=2, ensure_ascii=False)

    print("Done! Enhanced Day 02 lab workspaces written to syllabus.json")


if __name__ == "__main__":
    main()