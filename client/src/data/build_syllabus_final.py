#!/usr/bin/env python3
"""
[PROGRESS AUDIT] Final Merge: Combine all 7 days into syllabus.json
Day 01 → preserved as-is from existing syllabus.json
Days 02–04 → from build_syllabus.py (DAY02, DAY03, DAY04)
Days 05–07 → from build_syllabus_v2.py (DAY05, DAY06, DAY07)

Triple-Pass Integrity Check:
PASS 1 — Every slide has title, thesis, board_type, board_data, bottom_band
PASS 2 — Every day has day, title, eyebrow, thesis, rules[], pacing[], slides[], labs[]
PASS 3 — Count all slides, labs, pacing entries, and rules across all 7 days
"""
import json, os, sys

OUT = os.path.join(os.path.dirname(__file__), "syllabus.json")

# Import structures from the two build scripts
from build_syllabus import DAY02, DAY03, DAY04
from build_syllabus_v2 import DAY05, DAY06, DAY07

def load_day01():
    with open(OUT) as f:
        existing = json.load(f)
    return existing["01"]

def integrity_check_day(day_data, day_id):
    """Triple-pass integrity check for a single day."""
    errors = []

    # PASS 1: Slide-level checks
    for i, slide in enumerate(day_data["slides"]):
        for field in ["title", "thesis", "board_type", "board_data", "bottom_band"]:
            if field not in slide:
                errors.append(f"Day {day_id} Slide {i+1}: missing '{field}'")
            elif not slide[field]:
                errors.append(f"Day {day_id} Slide {i+1}: empty '{field}'")

        board_type = slide.get("board_type", "")
        if board_type not in ["table", "grid", "list", "math"]:
            errors.append(f"Day {day_id} Slide {i+1}: invalid board_type '{board_type}'")

        # Check board_data matches board_type
        bd = slide.get("board_data", {})
        if board_type == "table":
            if "headers" not in bd or "rows" not in bd:
                errors.append(f"Day {day_id} Slide {i+1}: table missing headers or rows")
            elif not isinstance(bd["headers"], list) or not isinstance(bd["rows"], list):
                errors.append(f"Day {day_id} Slide {i+1}: headers/rows must be lists")
        elif board_type == "grid":
            if not isinstance(bd, list):
                errors.append(f"Day {day_id} Slide {i+1}: grid board_data must be a list")
            for j, item in enumerate(bd):
                if not isinstance(item, dict) or "label" not in item or "value" not in item:
                    errors.append(f"Day {day_id} Slide {i+1} grid item {j}: missing label or value")
        elif board_type == "list":
            if not isinstance(bd, list):
                errors.append(f"Day {day_id} Slide {i+1}: list board_data must be a list")
            for j, item in enumerate(bd):
                if not isinstance(item, str) or len(item) < 10:
                    errors.append(f"Day {day_id} Slide {i+1} list item {j}: too short or not a string")
        elif board_type == "math":
            if "equation" not in bd or "steps" not in bd:
                errors.append(f"Day {day_id} Slide {i+1}: math missing equation or steps")

    # PASS 2: Day-level structure checks
    for field in ["day", "title", "eyebrow", "thesis", "rules", "pacing", "slides", "labs"]:
        if field not in day_data:
            errors.append(f"Day {day_id}: missing day-level field '{field}'")
        elif field in ["rules", "pacing", "slides", "labs"] and not isinstance(day_data[field], list):
            errors.append(f"Day {day_id}: '{field}' must be a list")
        elif field == "slides" and len(day_data[field]) == 0:
            errors.append(f"Day {day_id}: no slides defined")

    # Lab checks
    for i, lab in enumerate(day_data.get("labs", [])):
        for field in ["id", "title", "content"]:
            if field not in lab:
                errors.append(f"Day {day_id} Lab {lab.get('id', i)}: missing '{field}'")

    return errors

def print_audit_header(day_id, pct):
    """Print monospace progress audit header."""
    print(f"[PROGRESS AUDIT] Compiling Day Identifier: {day_id} of 07 | Total Task Completion: {pct:.2f}%")

def main():
    print("=" * 72)
    print("[PROGRESS AUDIT] FINAL MERGE — Triple-Pass Compilation")
    print("=" * 72)

    # Load Day 01
    print_audit_header("01", 100 * 1/7)
    day01 = load_day01()
    print(f"  Day 01: {len(day01['slides'])} slides, {len(day01['labs'])} labs, {len(day01['pacing'])} pacing entries, {len(day01['rules'])} rules")

    # Days 02-07
    days = {
        "02": DAY02,
        "03": DAY03,
        "04": DAY04,
        "05": DAY05,
        "06": DAY06,
        "07": DAY07,
    }

    all_errors = []
    all_errors.extend(integrity_check_day(day01, "01"))

    for day_id in sorted([d for d in days if d != "01"]):
        pct = 100 * (int(day_id)) / 7
        print_audit_header(day_id, pct)
        day_data = days[day_id]

        # Count
        n_slides = len(day_data["slides"])
        n_labs = len(day_data["labs"])
        n_pacing = len(day_data["pacing"])
        n_rules = len(day_data["rules"])

        # Count board types
        board_counts = {}
        for s in day_data["slides"]:
            bt = s.get("board_type", "unknown")
            board_counts[bt] = board_counts.get(bt, 0) + 1

        # Count total table cells, grid items, list items
        total_table_cells = 0
        total_grid_items = 0
        total_list_items = 0
        total_math_steps = 0
        for s in day_data["slides"]:
            bd = s.get("board_data", {})
            bt = s.get("board_type", "")
            if bt == "table":
                h = len(bd.get("headers", []))
                r = len(bd.get("rows", []))
                total_table_cells += h * r
            elif bt == "grid":
                total_grid_items += len(bd) if isinstance(bd, list) else 0
            elif bt == "list":
                total_list_items += len(bd) if isinstance(bd, list) else 0
            elif bt == "math":
                total_math_steps += len(bd.get("steps", [])) if isinstance(bd.get("steps", []), list) else 0

        print(f"  Slides: {n_slides} ({', '.join(f'{k}:{v}' for k,v in sorted(board_counts.items()))})")
        print(f"  Labs: {n_labs} | Pacing: {n_pacing} | Rules: {n_rules}")
        print(f"  Content: {total_table_cells} cells, {total_grid_items} grid items, {total_list_items} list items, {total_math_steps} math steps")

        # Integrity check
        errors = integrity_check_day(day_data, day_id)
        if errors:
            all_errors.extend(errors)
            for e in errors:
                print(f"  ⚠️  {e}")
        else:
            print(f"  ✅ All integrity checks passed")

    # Build final syllabus
    syllabus = {"01": day01}
    for day_id in ["02", "03", "04", "05", "06", "07"]:
        syllabus[day_id] = days[day_id]

    # Grand totals
    total_slides = sum(len(syllabus[d]["slides"]) for d in syllabus)
    total_labs = sum(len(syllabus[d]["labs"]) for d in syllabus)
    total_pacing = sum(len(syllabus[d]["pacing"]) for d in syllabus)
    total_rules = sum(len(syllabus[d]["rules"]) for d in syllabus)

    print("=" * 72)
    print(f"[PROGRESS AUDIT] GRAND TOTALS")
    print(f"  Total Slides: {total_slides} (Day 01: {len(day01['slides'])}, Days 02-07: {total_slides - len(day01['slides'])})")
    print(f"  Total Labs: {total_labs}")
    print(f"  Total Pacing Entries: {total_pacing}")
    print(f"  Total Rules: {total_rules}")
    print("=" * 72)

    if all_errors:
        print(f"\n⚠️  {len(all_errors)} INTEGRITY ERRORS FOUND:")
        for e in all_errors:
            print(f"  - {e}")
        print("\nAborting write due to integrity errors.")
        sys.exit(1)

    # Write final JSON
    with open(OUT, "w") as f:
        json.dump(syllabus, f, indent=2, ensure_ascii=False)

    file_size = os.path.getsize(OUT)
    print(f"\n✅ syllabus.json written: {file_size:,} bytes")
    print(f"✅ All {total_slides} slides across 7 days pass triple-pass integrity check.")
    print(f"[PROGRESS AUDIT] Total Task Completion: 100.00%")
    print("[PROGRESS AUDIT] Triple-Pass Compilation — COMPLETE")

if __name__ == "__main__":
    main()