#!/usr/bin/env python3
"""
Post-process syllabus.json Day 1 lab content:
  1. Convert raw markdown tables (| ... |) embedded in <p> tags → semantic HTML tables
  2. Wrap warning callouts ("Do not...", "Never...") in amber alert boxes
  3. Highlight parenthetical constraints "(do not mix)", "(required)" in left-border banners
"""
import json
import re
from pathlib import Path

SYLLABUS = Path("/Users/glennjeffersonchandra/course-vinci/client/src/data/syllabus.json")


# ── 1. Markdown table → HTML table ──────────────────────────────────────────

def parse_markdown_table(text: str) -> str | None:
    """
    Given a text block containing pipe-delimited rows, return an HTML <table>
    with Tailwind styling.  Returns None if no valid table is detected.
    """
    lines = text.strip().split("\n")
    # Filter to lines that contain at least one pipe
    rows = [ln.strip() for ln in lines if "|" in ln]

    if len(rows) < 2:
        return None  # need at least header + separator

    # Normalise: strip leading/trailing pipes, split on pipe
    cells: list[list[str]] = []
    for row in rows:
        r = row.strip("|").strip()
        cells.append([c.strip() for c in r.split("|")])

    # Identify separator row (every cell matches ---* or :---*)
    sep_idx: int | None = None
    for i, row in enumerate(cells):
        if all(re.match(r"^:?[—\-]{1,}:?$", c) for c in row):
            sep_idx = i
            break

    if sep_idx is None:
        return None  # no separator — not a table

    header = cells[sep_idx - 1] if sep_idx > 0 else cells[0]
    body = cells[sep_idx + 1:]

    if not body:
        return None

    # Build HTML
    col_count = len(header)
    th_html = "".join(
        f'<th class="p-2.5 text-left font-semibold text-muted-foreground border-b border-border">{c}</th>'
        for c in header
    )

    tr_html = ""
    for ri, row in enumerate(body):
        # Pad row to header width if needed
        while len(row) < col_count:
            row.append("")
        td_html = "".join(
            f'<td class="p-2.5">{c}</td>' for c in row[:col_count]
        )
        row_class = "even:bg-muted/20 border-b border-border/50"
        tr_html += f'<tr class="{row_class}">{td_html}</tr>'

    return (
        f'<table class="w-full text-xs border-collapse mb-4">'
        f'<thead><tr class="bg-muted/40">{th_html}</tr></thead>'
        f'<tbody>{tr_html}</tbody>'
        f'</table>'
    )


def convert_tables_in_content(html: str) -> str:
    """Find every <p> block that looks like a markdown table and replace it.
    Loops until no more tables are found (handles edge cases where re.sub
    misses blocks due to overlapping match regions)."""

    prev = None
    while prev != html:
        prev = html

        def replace_table_block(m: re.Match) -> str:
            inner = m.group(1)
            table_html = parse_markdown_table(inner)
            if table_html:
                return table_html
            return m.group(0)

        # Match any <p> block (any class) that contains pipe-delimited rows
        # with a separator line (pattern: cells made of dashes/em-dashes)
        html = re.sub(
            r'<p\b[^>]*>((?:[^<]|\n)*?\|[^<]*?)</p>',
            replace_table_block,
            html,
            flags=re.DOTALL,
        )

    return html


# ── 2. Warning / alert callouts ─────────────────────────────────────────────

WARNING_PATTERNS = [
    # Starts with "Do not..." / "Never..."
    r'^Do not\b.*$',
    r'^Never\b.*$',
    # Contains the ChannelFactoryInitialize gotcha
    r'.*ChannelFactoryInitialize.*',
    # Contains safety-critical language
    r'.*is not([\s](a|the))?.*command.*motion.*',
]
WARNING_RE = re.compile("|".join(WARNING_PATTERNS), re.IGNORECASE)


def wrap_warnings_in_content(html: str) -> str:
    """Wrap <p> blocks matching warning patterns in amber alert boxes."""

    def maybe_alert(m: re.Match) -> str:
        inner = m.group(1)
        # Check if any line of the inner text matches warning patterns
        if WARNING_RE.search(inner):
            # Clean up the text — remove leading labels like "⚠ Warning:"
            cleaned = re.sub(r'^⚠?\s*Warning:?\s*', '', inner, flags=re.IGNORECASE)
            return (
                f'<div class="border border-amber-500/40 bg-amber-500/10 rounded-lg p-3 mb-4">'
                f'<span class="font-semibold text-amber-600 dark:text-amber-400 text-xs uppercase tracking-wide">⚠ Important</span>'
                f'<p class="text-xs text-foreground leading-relaxed mt-1">{cleaned}</p>'
                f'</div>'
            )
        return m.group(0)

    return re.sub(
        r'<p class="text-xs text-muted-foreground leading-relaxed mb-3">((?:[^<]|\n)*?)</p>',
        maybe_alert,
        html,
        flags=re.DOTALL,
    )


# ── 3. Parenthetical constraint micro-banners ────────────────────────────────

CONSTRAINT_PATTERNS = [
    r'(\(do not mix[^)]*\))',
    r'(\(required[^)]*\))',
    r'(\(mandatory[^)]*\))',
    r'(\(not optional[^)]*\))',
]
CONSTRAINT_RE = re.compile("|".join(CONSTRAINT_PATTERNS), re.IGNORECASE)


def highlight_constraints_in_content(html: str) -> str:
    """Wrap paragraphs containing key parenthetical constraints in left-border banners."""

    def maybe_banner(m: re.Match) -> str:
        inner = m.group(1)
        if CONSTRAINT_RE.search(inner):
            # Render as a styled micro-banner instead of a plain <p>
            return (
                f'<div class="border-l-2 border-primary pl-3 py-1 mb-3 text-xs text-foreground italic">'
                f'{inner}'
                f'</div>'
            )
        return m.group(0)

    return re.sub(
        r'<p class="text-xs text-muted-foreground leading-relaxed mb-3">((?:[^<]|\n)*?)</p>',
        maybe_banner,
        html,
        flags=re.DOTALL,
    )


# ── 4. Final cleanup ────────────────────────────────────────────────────────

def final_cleanup(html: str) -> str:
    """Remove stray artifacts and collapse whitespace."""
    # Remove any remaining stray ** markers
    html = re.sub(r"\*\*", "", html)
    # Remove standalone horizontal-rule em-dash lines inside <p> tags
    html = re.sub(r"<p[^>]*>\s*—{1,3}\s*</p>", "", html)
    # Collapse 3+ consecutive newlines
    html = re.sub(r"\n{3,}", "\n", html)
    return html.strip()


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    with open(SYLLABUS) as f:
        syllabus = json.load(f)

    labs = syllabus.get("01", {}).get("labs", [])
    total_tables = 0
    total_warnings = 0
    total_banners = 0

    for lab in labs:
        before = len(lab["content"])
        old = lab["content"]

        # Apply transforms in order:
        # 1. Tables first (removes <p> wrappers)
        # 2. Warnings (wraps remaining <p> blocks)
        # 3. Constraint banners (wraps remaining <p> blocks)
        new = convert_tables_in_content(old)
        tables_converted = old.count('<p class="text-xs') - new.count('<p class="text-xs')  # approximate

        old2 = new
        new = wrap_warnings_in_content(new)
        warnings_added = new.count('⚠ Important') - old2.count('⚠ Important')

        old3 = new
        new = highlight_constraints_in_content(new)
        banners_added = new.count('border-l-2 border-primary') - old3.count('border-l-2 border-primary')

        new = final_cleanup(new)

        lab["content"] = new
        after = len(new)

        table_count = new.count("<table")
        warning_count = new.count("⚠ Important")
        banner_count = new.count("border-l-2 border-primary")

        total_tables += table_count
        total_warnings += warning_count
        total_banners += banner_count

        if table_count or warning_count or banner_count:
            print(f"  {lab['id']}: {before} → {after} chars | {table_count} tables, {warning_count} warnings, {banner_count} banners")

    # Write back
    with open(SYLLABUS, "w") as f:
        json.dump(syllabus, f, indent=2, ensure_ascii=False)

    print(f"\nTotals: {total_tables} tables, {total_warnings} warnings, {total_banners} constraint banners")


if __name__ == "__main__":
    main()