#!/usr/bin/env python3
"""
Lab 4 (Day 2) — Copy a patrol plan and apply leg tuning overrides.

No robot. Produces patrol_plan.tuned.json for lab04_field_trial.py / lab03.

Usage:
  python course/day-02/New-lab/lab-06/lab04_tune_plan.py \\
    ../lab-04/patrol_plan.cone_course.json \\
    --out course/day-02/New-lab/lab-04/patrol_plan.tuned.json

  python course/day-02/New-lab/lab-06/lab04_tune_plan.py \\
    ../lab-04/patrol_plan.cone_course.json --out ./patrol_plan.tuned.json \\
    --leg 0 --dx 0.35 --leg 1 --dyaw 0.7 --leg 2 --dx 0.25

  python course/day-02/New-lab/lab-06/lab04_tune_plan.py \\
    ../lab-04/patrol_plan.cone_course.json --out ./patrol_plan.tuned.json \\
    --from-notes tuning_notes.template.json
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

_REPO = Path(__file__).resolve().parents[4]
_DAY02 = _REPO / "course" / "day-02"
if str(_DAY02) not in sys.path:
    sys.path.insert(0, str(_DAY02))

from go2_patrol_helpers import load_patrol_plan  # noqa: E402

AXIS_FIELDS = frozenset({"dx", "dy", "dyaw", "vx", "vy", "duration_s"})


def _parse_set_specs(specs: list[str]) -> dict[int, dict[str, float]]:
    """Parse --set leg:field:value (field = dx, dy, dyaw, vx, ...)."""
    overrides: dict[int, dict[str, float]] = {}
    for spec in specs:
        parts = spec.split(":")
        if len(parts) != 3:
            print(f"WARN: skip --set {spec!r} (want leg:field:value)")
            continue
        idx, field, val_s = parts[0], parts[1], parts[2]
        if field not in AXIS_FIELDS:
            print(f"WARN: unknown field {field!r}")
            continue
        overrides.setdefault(int(idx), {})[field] = float(val_s)
    return overrides


def _parse_leg_overrides(argv: list[str]) -> dict[int, dict[str, float]]:
    """Parse repeated --leg N --dx V --dyaw V groups from argv tail."""
    overrides: dict[int, dict[str, float]] = {}
    i = 0
    while i < len(argv):
        if argv[i] == "--leg" and i + 1 < len(argv):
            idx = int(argv[i + 1])
            overrides.setdefault(idx, {})
            i += 2
            while i < len(argv) and argv[i] != "--leg":
                if argv[i] in AXIS_FIELDS and i + 1 < len(argv):
                    overrides[idx][argv[i]] = float(argv[i + 1])
                    i += 2
                else:
                    break
        else:
            i += 1
    return overrides


def _merge_overrides(
    *maps: dict[int, dict[str, float]],
) -> dict[int, dict[str, float]]:
    out: dict[int, dict[str, float]] = {}
    for m in maps:
        for idx, fields in m.items():
            out.setdefault(idx, {}).update(fields)
    return out


def apply_overrides(plan: dict[str, Any], overrides: dict[int, dict[str, float]]) -> list[str]:
    logs: list[str] = []
    legs = plan.get("legs") or []
    for idx, fields in overrides.items():
        if idx < 0 or idx >= len(legs) or not isinstance(legs[idx], dict):
            logs.append(f"WARN: skip leg index {idx}")
            continue
        for key, val in fields.items():
            old = legs[idx].get(key)
            legs[idx][key] = val
            logs.append(f"leg[{idx}].{key}: {old} → {val}")
    return logs


def apply_notes_file(plan: dict[str, Any], notes_path: Path) -> list[str]:
    data = json.loads(notes_path.read_text(encoding="utf-8"))
    logs: list[str] = []
    for ch in data.get("changes") or []:
        if not isinstance(ch, dict):
            continue
        idx = int(ch.get("leg_index", -1))
        field = str(ch.get("field", ""))
        if field not in AXIS_FIELDS:
            continue
        to_val = ch.get("to")
        if to_val is None:
            continue
        legs = plan.get("legs") or []
        if 0 <= idx < len(legs) and isinstance(legs[idx], dict):
            old = legs[idx].get(field)
            legs[idx][field] = float(to_val)
            reason = ch.get("reason", "")
            logs.append(f"leg[{idx}].{field}: {old} → {to_val} ({reason})")
    return logs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan_in", type=Path, help="Source patrol_plan.json")
    parser.add_argument("--out", type=Path, required=True, help="Output tuned plan")
    parser.add_argument(
        "--from-notes",
        type=Path,
        default=None,
        help="Apply changes[] from tuning_notes JSON",
    )
    parser.add_argument(
        "--set",
        action="append",
        default=[],
        metavar="LEG:FIELD:VALUE",
        help="Override one field, e.g. 1:dyaw:0.7",
    )
    args, rest = parser.parse_known_args()

    plan_path = args.plan_in.resolve()
    try:
        plan = load_patrol_plan(plan_path)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"ERROR: {e}")
        return 1

    tuned = copy.deepcopy(plan)
    tuned["description"] = (
        str(tuned.get("description", "")) + " (Lab 4 tuned)"
    ).strip()

    logs: list[str] = []
    if args.from_notes:
        logs.extend(apply_notes_file(tuned, args.from_notes.resolve()))
    overrides = _merge_overrides(
        _parse_set_specs(args.set),
        _parse_leg_overrides(rest),
    )
    logs.extend(apply_overrides(tuned, overrides))

    out = args.out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(tuned, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {out}")
    for line in logs:
        print(f"  {line}")
    if not logs:
        print("  (no overrides — copy only)")
    print("\nNext:")
    print(f"  python course/day-02/New-lab/lab-06/lab04_field_trial.py en6 --plan {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
