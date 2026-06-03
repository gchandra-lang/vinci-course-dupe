#!/usr/bin/env python3
"""Build Day 1 labs from New-lab/ into syllabus.json with proper text sanitization."""

import json
import re
from pathlib import Path

NEW_LAB = Path("/Users/glennjeffersonchandra/course-vinci/New-lab")
SYLLABUS = Path("/Users/glennjeffersonchandra/course-vinci/client/src/data/syllabus.json")

# ── Text sanitizer: strip raw markdown formatting ──
def sanitize(text: str) -> str:
    """Remove raw markdown: **bold**, `code`, -- dashes, stray # headers, etc."""
    # Remove top-level markdown header lines (## Title)
    text = re.sub(r"^#{1,4}\s+", "", text, flags=re.MULTILINE)
    # Remove bold/italic markers (**text** → text, *text* → text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    # Remove any remaining stray ** markers (unbalanced pairs, trailing, etc.)
    text = re.sub(r"\*\*", "", text)
    # Remove inline code backticks
    text = re.sub(r"`([^`]+)`", r"\1", text)
    # Remove stray em-dash indicators
    text = text.replace("--", "—")
    # Remove leading em-dash on a line followed by optional whitespace
    text = re.sub(r"^—\s*", "", text, flags=re.MULTILINE)
    # Normalise triple dashes
    text = text.replace("---", "")
    # Remove standalone horizontal-rule lines (—- or —)
    text = re.sub(r"^\s*—{1,3}\s*$", "", text, flags=re.MULTILINE)
    # Collapse multiple blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Remove leading/trailing blank lines
    text = text.strip()
    return text


def parse_metadata(readme: str) -> dict[str, str]:
    """Extract metadata key-value pairs from the top of a README."""
    meta: dict[str, str] = {}
    lines = readme.splitlines()
    for line in lines[:15]:
        line = line.strip()
        # Match patterns like: **Duration:** ~45–60 min
        m = re.match(r"\*{0,2}(Duration|Robot required|Robot motion|Motion|Prerequisites|PDF coverage|TtT Day)\*{0,2}:\s*(.+)", line, re.IGNORECASE)
        if m:
            key = m.group(1).strip()
            val = sanitize(m.group(2).strip())
            meta[key] = val
        # Also match "**TtT Day 1 · 10:45 ROS block**"
        m2 = re.match(r"TtT Day.*?:\s*(.+)", sanitize(line))
        if m2:
            meta.setdefault("Track", m2.group(1).strip())
    return meta


def render_metadata_html(meta: dict[str, str]) -> str:
    """Render metadata as a clean key-value grid."""
    if not meta:
        return ""
    rows = []
    for k, v in meta.items():
        if k == "TtT Day":
            rows.append(f'<div class="flex gap-2"><span class="font-semibold text-foreground">Track:</span><span>{v}</span></div>')
        else:
            rows.append(f'<div class="flex gap-2"><span class="font-semibold text-foreground">{k}:</span><span>{v}</span></div>')
    return f'<div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5 text-xs mb-4 p-3 bg-muted/30 border border-border/60 rounded-lg">{"".join(rows)}</div>'


def extract_learning_objectives(readme: str) -> str:
    """Extract the numbered learning objectives section."""
    lines = readme.splitlines()
    started = False
    items: list[str] = []
    for line in lines:
        s = line.strip()
        if re.match(r"^#{1,4}\s*Learning objectives", s, re.IGNORECASE):
            started = True
            continue
        if started:
            if re.match(r"^#{1,4}\s", s):
                break
            m = re.match(r"^\d+\.[\s]*(.+)", s)
            if m:
                items.append(sanitize(m.group(1)))
    if not items:
        return ""
    return '<ul class="list-decimal pl-5 space-y-1 text-xs text-muted-foreground leading-relaxed mb-4">' + "".join(f"<li>{it}</li>" for it in items) + "</ul>"


def extract_after_heading(readme: str, heading: str) -> str:
    """Extract text under a specific heading until the next heading or ---."""
    lines = readme.splitlines()
    started = False
    buf: list[str] = []
    for line in lines:
        s = line.strip()
        if re.match(rf"^#{1,4}\s*{re.escape(heading)}", s, re.IGNORECASE):
            started = True
            continue
        if started:
            if re.match(r"^#{1,4}\s", s) or s == "---":
                break
            buf.append(s)
    return "\n".join(buf).strip()


def build_lab(
    lab_id: str,
    title: str,
    readme_path: Path,
    code_files: list[dict],
) -> dict:
    """Build a sanitized lab entry."""
    readme = readme_path.read_text() if readme_path.exists() else ""
    meta = parse_metadata(readme)

    # Build clean content
    parts: list[str] = []

    # 1. Metadata grid
    meta_html = render_metadata_html(meta)
    if meta_html:
        parts.append(meta_html)

    # 2. Learning objectives
    obj_html = extract_learning_objectives(readme)
    if obj_html:
        parts.append('<div class="font-serif italic text-foreground text-xs mb-2">Learning Objectives:</div>')
        parts.append(obj_html)

    # 3. What you will learn / Overview (first paragraph after metadata)
    # Strip out the intro heading line and get the actual text
    cleaned = sanitize(readme)
    # Remove the first heading line
    cleaned = re.sub(r"^.*?\n", "", cleaned, count=1)
    # Extract the overview — text before the first remaining ## heading
    overview_parts: list[str] = []
    for line in cleaned.splitlines():
        s = line.strip()
        if re.match(r"^#{1,4}\s", s) or s == "---":
            break
        if s:
            overview_parts.append(s)
        elif overview_parts and overview_parts[-1] != "":
            overview_parts.append("")

    overview = "\n".join(overview_parts).strip()
    # Build a set of metadata field names to skip duplicate lines in overview
    meta_field_names = {k.lower() for k in meta.keys()}
    if overview:
        # Wrap in paragraphs
        paras = overview.split("\n\n")
        for p in paras:
            p = p.strip()
            if not p or p.startswith("<"):
                continue
            # Skip paragraphs that are just duplicate metadata key-value pairs
            # e.g. "Duration: ~45 min" or "Robot required: Optional"
            first_word = p.split(":")[0].strip().lower()
            if first_word in meta_field_names:
                continue
            # Skip learning objectives heading / items — already rendered separately
            if re.match(r"^(Learning objectives?|By the end of)", p, re.IGNORECASE):
                continue
            # Skip numbered list items that look like learning objectives
            if re.match(r"^\d+\.\s", p.strip().split("\n")[0]):
                continue
            # Skip raw em-dash divider lines
            if re.match(r"^—{1,3}$", p.strip()):
                continue
            # Skip lines that look like the original markdown metadata prefix
            # e.g. "TtT Day 1 · 10:45 ROS block"
            if re.match(r"^TtT Day\b", p, re.IGNORECASE):
                continue
            parts.append(f'<p class="text-xs text-muted-foreground leading-relaxed mb-3">{sanitize(p)}</p>')

    # 4. Instructions / Steps
    steps = extract_after_heading(readme, "Steps") or extract_after_heading(readme, "Hands-on") or extract_after_heading(readme, "Hands-on checklist")
    if steps:
        parts.append('<div class="font-serif italic text-foreground text-xs mt-3 mb-2">Instructions:</div>')
        parts.append(f'<div class="text-xs text-muted-foreground leading-relaxed space-y-2">{sanitize(steps)}</div>')

    # 5. Deliverable
    deliverable = extract_after_heading(readme, "Deliverable")
    if deliverable:
        parts.append('<div class="font-serif italic text-foreground text-xs mt-3 mb-1">Deliverable:</div>')
        parts.append(f'<p class="text-xs text-muted-foreground leading-relaxed">{sanitize(deliverable)}</p>')

    content = "\n".join(parts)
    # Ensure it's all on one logical "line" for JSON — or just keep the embedded HTML
    # Compact excessive whitespace
    content = re.sub(r"\n{2,}", "\n", content).strip()

    # Post-process: convert raw markdown tables, warnings, constraints
    content = post_process_content(content)

    return {
        "id": lab_id,
        "title": title,
        "content": content,
        "code_files": code_files,
    }


# ── Post-processing transforms (applied to final HTML content) ──────────────────

def parse_markdown_table(text: str) -> str | None:
    """Convert a pipe-delimited text block into a styled HTML <table>."""
    lines = text.strip().split("\n")
    rows = [ln.strip() for ln in lines if "|" in ln]
    if len(rows) < 2:
        return None
    cells = [[c.strip() for c in r.strip("|").strip().split("|")] for r in rows]
    sep_idx = next((i for i, row in enumerate(cells) if all(re.match(r"^:?[—\-]{1,}:?$", c) for c in row)), None)
    if sep_idx is None:
        return None
    header = cells[sep_idx - 1] if sep_idx > 0 else cells[0]
    body = cells[sep_idx + 1:]
    if not body:
        return None
    col_count = len(header)
    th_html = "".join(
        f'<th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">{c}</th>'
        for c in header
    )
    tr_html = ""
    for row in body:
        while len(row) < col_count:
            row.append("")
        td_html = "".join(f'<td class="p-2.5">{c}</td>' for c in row[:col_count])
        tr_html += f'<tr class="even:bg-muted/20 border-b border-border/50">{td_html}</tr>'
    return (
        f'<table class="w-full text-xs border-collapse mb-4">'
        f'<thead><tr class="bg-muted/40">{th_html}</tr></thead>'
        f'<tbody>{tr_html}</tbody>'
        f'</table>'
    )


def post_process_content(html: str) -> str:
    """Apply table conversion, warning wrapping, and constraint highlighting to content."""

    # 1. Convert markdown tables inside <p> tags
    def replace_table(m: re.Match) -> str:
        inner = m.group(1)
        t = parse_markdown_table(inner)
        return t if t else m.group(0)

    html = re.sub(
        r'<p class="text-xs text-muted-foreground leading-relaxed mb-3">((?:[^<]|\n)*?\|[^<]*?)</p>',
        replace_table, html, flags=re.DOTALL,
    )

    # 2. Wrap warning callouts in amber alert boxes
    WARNING_RE = re.compile(
        r'^(Do not\b.*|Never\b.*|.*ChannelFactoryInitialize.*|.*is not(?:\s(?:a|the))?\s.*command.*motion.*)$',
        re.IGNORECASE,
    )

    def maybe_alert(m: re.Match) -> str:
        inner = m.group(1)
        if WARNING_RE.search(inner):
            cleaned = re.sub(r'^⚠?\s*Warning:?\s*', '', inner, flags=re.IGNORECASE)
            return (
                f'<div class="border border-amber-500/40 bg-amber-500/10 rounded-lg p-3 mb-4">'
                f'<span class="font-semibold text-amber-600 dark:text-amber-400 text-xs uppercase tracking-wide">⚠ Important</span>'
                f'<p class="text-xs text-foreground leading-relaxed mt-1">{cleaned}</p>'
                f'</div>'
            )
        return m.group(0)

    html = re.sub(
        r'<p class="text-xs text-muted-foreground leading-relaxed mb-3">((?:[^<]|\n)*?)</p>',
        maybe_alert, html, flags=re.DOTALL,
    )

    # 3. Highlight parenthetical constraints as left-border banners
    CONSTRAINT_RE = re.compile(
        r'(\(do not mix[^)]*\)|\(required[^)]*\)|\(mandatory[^)]*\)|\(not optional[^)]*\))',
        re.IGNORECASE,
    )

    def maybe_banner(m: re.Match) -> str:
        inner = m.group(1)
        if CONSTRAINT_RE.search(inner):
            return (
                f'<div class="border-l-2 border-primary pl-3 py-1 mb-3 text-xs text-foreground italic">'
                f'{inner}'
                f'</div>'
            )
        return m.group(0)

    html = re.sub(
        r'<p class="text-xs text-muted-foreground leading-relaxed mb-3">((?:[^<]|\n)*?)</p>',
        maybe_banner, html, flags=re.DOTALL,
    )

    # 4. Final cleanup
    html = re.sub(r"\*\*", "", html)
    html = re.sub(r"\n{3,}", "\n", html)
    return html.strip()


def read_code_file(path: Path) -> dict:
    """Read a code file into the code_files structure."""
    return {
        "name": path.name,
        "code": path.read_text(),
    }


def main():
    with open(SYLLABUS) as f:
        syllabus = json.load(f)

    # Build lab definitions from New-lab/
    labs = []

    # Lab 0
    labs.append(build_lab(
        "lab-00",
        "Lab 0 — Environment, Architecture & Readiness",
        NEW_LAB / "lab-00" / "README.md",
        [
            read_code_file(NEW_LAB / "lab-00" / "lab00_readiness.py"),
            read_code_file(NEW_LAB / "go2_network_helpers.py"),
        ],
    ))

    # Lab 1
    labs.append(build_lab(
        "lab-01",
        "Lab 1 — Go2, ROS 2 & unitree_ros2 Setup",
        NEW_LAB / "lab-01" / "README.md",
        [
            read_code_file(NEW_LAB / "lab-01" / "lab01_ros_readiness.py"),
            read_code_file(NEW_LAB / "ros_basic_helpers.py"),
        ],
    ))

    # Lab 2
    labs.append(build_lab(
        "lab-02",
        "Lab 2 — ROS 2 Pub/Sub (Talker / Listener)",
        NEW_LAB / "lab-02" / "README.md",
        [
            read_code_file(NEW_LAB / "lab-02" / "talker.py"),
            read_code_file(NEW_LAB / "lab-02" / "listener.py"),
            read_code_file(NEW_LAB / "lab-02" / "lab01_verify_pubsub.py"),
            read_code_file(NEW_LAB / "lab-02" / "run_lab.sh"),
        ],
    ))

    # Lab 3
    labs.append(build_lab(
        "lab-03",
        "Lab 3 — DDS Observation (rt/sportmodestate)",
        NEW_LAB / "lab-03" / "README.md",
        [
            read_code_file(NEW_LAB / "lab-03" / "lab03_listen_sportmodestate.py"),
            read_code_file(NEW_LAB / "go2_network_helpers.py"),
        ],
    ))

    # Lab 4
    labs.append(build_lab(
        "lab-04",
        "Lab 4 — SDK Sport RPC & Motion Modes (Read-Only)",
        NEW_LAB / "lab-04" / "README.md",
        [
            read_code_file(NEW_LAB / "lab-04" / "lab04_sport_readonly.py"),
            read_code_file(NEW_LAB / "go2_network_helpers.py"),
        ],
    ))

    # Lab 5
    labs.append(build_lab(
        "lab-05",
        "Lab 5 — Stand, Balance & Short Walk (SDK)",
        NEW_LAB / "lab-05" / "README.md",
        [
            read_code_file(NEW_LAB / "lab-05" / "lab05_safe_posture.py"),
        ],
    ))

    # Lab 6
    labs.append(build_lab(
        "lab-06",
        "Lab 6 — RViz2 & Go2 ROS 2 Data",
        NEW_LAB / "lab-06" / "README.md",
        [
            read_code_file(NEW_LAB / "lab-06" / "run_rviz.sh"),
        ],
    ))

    # Lab 7
    labs.append(build_lab(
        "lab-07",
        "Lab 7 — Optional Sport Showcase (SDK)",
        NEW_LAB / "lab-07" / "README.md",
        [
            read_code_file(NEW_LAB / "lab-07" / "lab07_showcase.py"),
        ],
    ))

    # Lab 8
    labs.append(build_lab(
        "lab-08",
        "Lab 8 — rqt (ROS 2 GUI Toolbox)",
        NEW_LAB / "lab-08" / "README.md",
        [
            read_code_file(NEW_LAB / "lab-08" / "lab08_check_rqt.py"),
            read_code_file(NEW_LAB / "lab-08" / "run_demo_topics.sh"),
        ],
    ))

    # Lab 9
    labs.append(build_lab(
        "lab-09",
        "Lab 9 — PlotJuggler (Time-Series Plots)",
        NEW_LAB / "lab-09" / "README.md",
        [
            read_code_file(NEW_LAB / "lab-09" / "lab09_check_plotjuggler.py"),
            read_code_file(NEW_LAB / "lab-09" / "plot_demo_publisher.py"),
            read_code_file(NEW_LAB / "lab-09" / "run_demo_plot.sh"),
        ],
    ))

    # Update syllabus
    if "01" not in syllabus:
        syllabus["01"] = {}
    syllabus["01"]["labs"] = labs

    # Write back
    with open(SYLLABUS, "w") as f:
        json.dump(syllabus, f, indent=2, ensure_ascii=False)

    print(f"Updated Day 1 with {len(labs)} labs")
    for lab in labs:
        codes = len(lab["code_files"])
        print(f"  {lab['id']}: {len(lab['content']):5d} chars content, {codes} code files")


if __name__ == "__main__":
    main()