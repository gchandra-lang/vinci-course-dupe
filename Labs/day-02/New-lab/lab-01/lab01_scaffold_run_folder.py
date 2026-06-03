#!/usr/bin/env python3
"""
Lab 1 (Day 2) — Create an empty patrol run folder from a Lab 0 scenario file.

No robot. Writes metadata.json, patrol_plan.json, empty sportmodestate.jsonl,
and checkpoints/<id>/ placeholders (no images until Lab 3 capture).

Usage:
  python course/day-02/New-lab/lab-01/lab01_scaffold_run_folder.py ../lab-00/my_team_scenario.json
  python course/day-02/New-lab/lab-01/lab01_scaffold_run_folder.py ../lab-00/my_team_scenario.json --out-dir ./run_dry_01
  python course/day-02/New-lab/lab-01/lab01_scaffold_run_folder.py ../lab-00/patrol_scenario.template.json --increment-dx 0.4
"""

from __future__ import annotations

import argparse
import json
import socket
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

def _load_scenario(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("scenario root must be object")
    cps = data.get("checkpoints")
    if not isinstance(cps, list) or len(cps) < 2:
        raise ValueError("scenario needs at least 2 checkpoints")
    return data


def _build_plan(
    scenario: dict[str, Any],
    *,
    increment_dx: float,
) -> dict[str, Any]:
    cps_in = scenario["checkpoints"]
    checkpoints: list[dict[str, Any]] = []
    for cp in cps_in:
        if not isinstance(cp, dict) or not cp.get("id"):
            continue
        checkpoints.append(
            {
                "id": str(cp["id"]),
                "label": str(cp.get("label", cp["id"])),
                "dwell_s": 2.0,
            }
        )
    if len(checkpoints) < 2:
        raise ValueError("could not read 2+ checkpoint ids from scenario")

    legs: list[dict[str, Any]] = []
    for i in range(1, len(checkpoints)):
        legs.append(
            {
                "type": "increment",
                "dx": increment_dx,
                "dy": 0.0,
                "dyaw": 0.0,
                "to_checkpoint": checkpoints[i]["id"],
                "notes": "Scaffold leg — tune before Lab 2 hardware",
            }
        )

    return {
        "schema_version": 1,
        "description": f"Scaffold from scenario {scenario.get('team_name', '')}".strip(),
        "checkpoints": checkpoints,
        "legs": legs,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "scenario",
        type=Path,
        help="Lab 0 patrol scenario JSON",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Output run directory (default: run_<UTC>)",
    )
    parser.add_argument(
        "--increment-dx",
        type=float,
        default=0.4,
        help="Default dx for increment legs between checkpoints",
    )
    parser.add_argument(
        "--operator",
        default=None,
        help="Override operator (default: scenario operator)",
    )
    args = parser.parse_args()

    scenario_path = args.scenario.resolve()
    if not scenario_path.is_file():
        print(f"ERROR: scenario not found: {scenario_path}")
        return 1

    try:
        scenario = _load_scenario(scenario_path)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"ERROR: {e}")
        return 1

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = args.out_dir or Path(f"run_{ts}")
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=False)

    plan = _build_plan(scenario, increment_dx=args.increment_dx)
    cp_ids = [cp["id"] for cp in plan["checkpoints"]]

    operator = args.operator or str(scenario.get("operator", "operator"))
    metadata: dict[str, Any] = {
        "schema_version": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "operator": operator,
        "team_name": scenario.get("team_name", ""),
        "robot_id": "go2-01",
        "host": socket.gethostname(),
        "interface": None,
        "lab": "day-02-lab-01-scaffold",
        "scenario_file": str(scenario_path.name),
        "checkpoints": cp_ids,
        "artifacts": {
            "patrol_plan": "patrol_plan.json",
            "sportmodestate_log": "sportmodestate.jsonl",
        },
        "notes": "Scaffold run — add images in Lab 3; validate with lab01_validate_run_folder.py",
    }

    (out_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )
    (out_dir / "patrol_plan.json").write_text(
        json.dumps(plan, indent=2) + "\n",
        encoding="utf-8",
    )
    (out_dir / "sportmodestate.jsonl").write_text(
        json.dumps(
            {
                "t": 0.0,
                "mode": 0,
                "note": "placeholder — replace during patrol or copy from Day 1 log",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    ck_root = out_dir / "checkpoints"
    ck_root.mkdir()
    for cid in cp_ids:
        cp_dir = ck_root / cid
        cp_dir.mkdir()
        (cp_dir / "README.txt").write_text(
            "Lab 3 will write frame.jpg here after capture.\n",
            encoding="utf-8",
        )

    print(f"Created scaffold run: {out_dir}")
    print("  metadata.json, patrol_plan.json, sportmodestate.jsonl (placeholder)")
    print(f"  checkpoints/ ({len(cp_ids)} dirs)")
    print()
    print("Validate (expect warnings until images exist):")
    print(f"  python course/day-02/New-lab/lab-01/lab01_validate_run_folder.py {out_dir} --relax-images")
    return 0


if __name__ == "__main__":
    sys.exit(main())
