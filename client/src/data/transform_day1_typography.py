#!/usr/bin/env python3
"""
Typography overhaul for Day 1 lab content in syllabus.json:
  1. Wrap "Step N" / "Exercise N" / "Task N" headings in prominent step headers
  2. Style learning objectives section with a callout background
  3. Bold critical technical keywords inline (DDS, ROS 2, .py, etc.)
  4. Clean up remaining artifacts (—- dividers, stray metadata, etc.)
"""
import json
import re
from pathlib import Path

SYLLABUS = Path("/Users/glennjeffersonchandra/course-vinci/client/src/data/syllabus.json")


# ── Keyword bolding ──────────────────────────────────────────────────────────

# Terms to bold: protocols, file types, SDK names — wrapped in <span class="font-bold text-foreground">
KEYWORD_PATTERNS = [
    # Protocols / middleware
    (r'\b(DDS)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(Cyclone\s*DDS)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(Ethernet)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(ROS\s*2)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(RViz2?)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(Nav2)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(rqt)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(PlotJuggler)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(UDP)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(TCP)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(RPC)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(pub/sub)\b', r'<span class="font-bold text-foreground">\1</span>'),
    # SDK / libraries
    (r'\b(SportClient)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(LocoClient)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(ChannelFactoryInitialize)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(ChannelSubscriber)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(unitree_sdk2)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(unitree_ros2)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(unitree_go)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(unitree_hg)\b', r'<span class="font-bold text-foreground">\1</span>'),
    # File types
    (r'(\.[a-zA-Z0-9_]+\.py\b)', r'<span class="font-bold text-foreground">\1</span>'),
    (r'(\.[a-zA-Z0-9_]+\.sh\b)', r'<span class="font-bold text-foreground">\1</span>'),
    (r'(\.jsonl\b)', r'<span class="font-bold text-foreground">\1</span>'),
    (r'(\.db3\b)', r'<span class="font-bold text-foreground">\1</span>'),
    (r'(setup\.bash\b)', r'<span class="font-bold text-foreground">\1</span>'),
    # Topics / types
    (r'\b(rt/sportmodestate)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(rt/lowstate)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(SportModeState_)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(LowState_)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(ros_basic_topic)\b', r'<span class="font-bold text-foreground">\1</span>'),
    # Robot models
    (r'\b(Go2)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(G1)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(B2)\b', r'<span class="font-bold text-foreground">\1</span>'),
    # IP / network
    (r'\b(192\.168\.123\.\d+)\b', r'<span class="font-bold text-foreground">\1</span>'),
    # Conda / environment
    (r'\b(unitree_env)\b', r'<span class="font-bold text-foreground">\1</span>'),
    # Misc important
    (r'\b(IMU)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(BMS)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(TF)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(JSONL)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(PASS)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(FAIL)\b', r'<span class="font-bold text-foreground">\1</span>'),
    (r'\b(PASS/FAIL)\b', r'<span class="font-bold text-foreground">\1</span>'),
]


def bold_keywords(html: str) -> str:
    """Wrap technical keywords in <span class='font-bold text-foreground'>."""
    for pattern, replacement in KEYWORD_PATTERNS:
        # Only apply inside text content — not inside existing HTML tags
        # We use a negative lookahead to avoid matching inside tag names/attributes
        html = re.sub(pattern, replacement, html)
    return html


def bold_keywords_in_text_nodes(html: str) -> str:
    """
    Apply keyword bolding ONLY inside the text content of HTML elements,
    not inside tag names or attribute values.
    """
    def replace_in_text(m: re.Match) -> str:
        prefix = m.group(1)  # > or nothing
        text = m.group(2)
        suffix = m.group(3)
        for pattern, replacement in KEYWORD_PATTERNS:
            # Avoid double-wrapping
            if '<span class="font-bold text-foreground">' in text:
                continue
            text = re.sub(pattern, replacement, text)
        return f"{prefix}{text}{suffix}"

    # Match text between: > ... </tag>  or between tags
    return re.sub(
        r'(>)\s*([^<]+?)\s*(<)',
        replace_in_text,
        html,
        flags=re.DOTALL,
    )


# ── Step / Exercise / Task headers ───────────────────────────────────────────

def wrap_step_headers(html: str) -> str:
    """
    Detect paragraphs starting with:
      - "Step N — ..."
      - "Step Nb — ..."
      - "Exercise N — ..."
      - "Task N — ..."
      - "A — ..." / "B — ..." (letter sections)
      - "Terminal A — ..." / "Terminal B:"
    Wrap them in prominent step-header divs.
    """
    def upgrade_header(m: re.Match) -> str:
        prefix = m.group(1)  # class attribute
        text = m.group(2).strip()

        # Determine header label
        header_type = None
        header_label = text

        # Step patterns
        step_m = re.match(r'^(Step\s+\d+[a-z]?\s*[—\-–]\s*.+)', text, re.IGNORECASE)
        if step_m:
            header_type = "step"
            header_label = step_m.group(1)

        # Exercise patterns
        ex_m = re.match(r'^(Exercise\s+[A-E]\s*[—\-–]\s*.+)', text, re.IGNORECASE)
        if ex_m:
            header_type = "exercise"
            header_label = ex_m.group(1)

        # Task patterns
        task_m = re.match(r'^(Task\s+\d+[a-z]?\s*[—\-–]\s*.+)', text, re.IGNORECASE)
        if task_m:
            header_type = "task"
            header_label = task_m.group(1)

        # Letter section patterns: "A — Automated check" or "B — Demo graph"
        letter_m = re.match(r'^([A-E])\s[—\-–]\s(.+)', text)
        if letter_m and not header_type:
            header_type = "section"
            header_label = text

        # Terminal patterns
        term_m = re.match(r'^(Terminal\s+[A-E][\s:—\-–].*)', text)
        if term_m:
            header_type = "terminal"
            header_label = term_m.group(1)

        # Short standalone section headers: "Objectives", "Prerequisites", "Steps",
        # "Deliverable", "Files", "Troubleshooting", "References", "What you will learn"
        short_m = re.match(
            r'^(Objectives|Prerequisites|Steps|Deliverable|Files|Troubleshooting|'
            r'References|What you will learn|Submit|Quick start|'
            r'Managing sensor data|Concepts:.*|Communication model.*|'
            r'Hands-on tasks.*|Clicks:|Confirm you see:|What to observe|'
            r'See also|Next:.*|Ethernet interface|Other useful plugins|'
            r'DDS session.*|Pub/sub vs RPC|Topics and types.*|'
            r'With Unitree session sourced:|From the repo root:|'
            r'Your lab scripts.*|Add to.*|Equivalent manual check:|'
            r'In PlotJuggler:|In Terminal B:|Official sport example.*|'
            r'No robot yet.*|Or:|Fill in your table:|'
            r'Files in this folder)$',
            text, re.IGNORECASE
        )
        if short_m:
            header_type = "subsection"
            header_label = text

        if header_type:
            # Build styled header div + retain body text if there is more
            return (
                f'<div class="step-header mb-6">'
                f'<h4 class="text-base font-bold text-primary tracking-tight mb-2">{header_label}</h4>'
                f'</div>'
            )

        # Not a header — return as-is (already an <p> block, will be rendered normally)
        return m.group(0)

    # Match <p> blocks that start with header-like text
    return re.sub(
        r'<p( class="[^"]*")>((?:[^<]|\n)*?)</p>',
        upgrade_header,
        html,
        flags=re.DOTALL,
    )


# ── Learning objectives callout ──────────────────────────────────────────────

def style_learning_objectives(html: str) -> str:
    """
    Wrap the learning objectives section in a distinct callout block.
    The objectives are followed by a <ul> — detect the heading + list pattern.
    """
    # Pattern: <div class="font-serif...">Learning Objectives:</div> followed by <ul...>...</ul>
    pattern = (
        r'(<div class="font-serif italic text-foreground text-xs mb-2">'
        r'Learning Objectives:</div>\s*)'
        r'(<ul class="list-decimal[^"]*">.*?</ul>)'
    )

    replacement = (
        r'<div class="border border-primary/30 bg-primary/5 rounded-lg p-4 mb-6">'
        r'<div class="flex items-center gap-2 mb-3">'
        r'<span class="text-base">🎯</span>'
        r'<span class="text-sm font-bold text-foreground tracking-tight">Learning Objectives</span>'
        r'</div>'
        r'\2'
        r'</div>'
    )
    return re.sub(pattern, replacement, html, flags=re.DOTALL)


# ── Final cleanup ────────────────────────────────────────────────────────────

def final_cleanup(html: str) -> str:
    """Remove stray artifacts."""
    # Remove standalone em-dash divider <p> blocks
    html = re.sub(r'<p[^>]*>\s*—{1,3}\s*</p>', '', html)
    # Remove any remaining ** markers
    html = re.sub(r'\*\*', '', html)
    # Collapse 3+ newlines
    html = re.sub(r'\n{3,}', '\n', html)
    # Remove duplicate metadata paragraphs that survived earlier passes
    html = re.sub(
        r'<p class="text-xs text-muted-foreground leading-relaxed mb-3">\s*TtT Day.*?</p>',
        '', html, flags=re.DOTALL,
    )
    # Remove empty <div class="step-header mb-6"><h4...></h4></div> (no real content)
    # These happen when a short section title like "Files" gets wrapped but has no body
    # We keep them — they serve as visual section breaks
    return html.strip()


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    with open(SYLLABUS) as f:
        syllabus = json.load(f)

    labs = syllabus.get("01", {}).get("labs", [])

    for lab in labs:
        before = len(lab["content"])
        old = lab["content"]

        # Order matters:
        # 1. Keyword bolding first (operates on text nodes)
        # 2. Step headers (wraps <p> blocks in <div> wrappers)
        # 3. Learning objectives callout (wraps existing objectives section)
        # 4. Final cleanup

        new = bold_keywords_in_text_nodes(old)
        new = wrap_step_headers(new)
        new = style_learning_objectives(new)
        new = final_cleanup(new)

        lab["content"] = new
        after = len(new)

        headers = new.count('<div class="step-header')
        has_obj_callout = 'border-primary/30 bg-primary/5' in new

        if before != after or headers:
            print(f"  {lab['id']}: {before} → {after} chars | {headers} step headers"
                  f"{' | objectives callout' if has_obj_callout else ''}")

    with open(SYLLABUS, "w") as f:
        json.dump(syllabus, f, indent=2, ensure_ascii=False)

    print("\nDone — typography overhaul applied to all Day 1 labs.")


if __name__ == "__main__":
    main()