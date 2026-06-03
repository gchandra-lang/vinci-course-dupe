#!/usr/bin/env python3
"""
Lab 1 (Day 2) — Validate a patrol run folder layout (no robot).

Checks metadata.json, patrol_plan.json, sportmodestate.jsonl, and checkpoints/.

Usage:
  python course/day-02/lab-01/lab01_validate_run_folder.py fixtures/sample_run_pass
  python course/day-02/lab-01/lab01_validate_run_folder.py ./my_run --scenario ../lab-00/my_team_scenario.json
  python course/day-02/lab-01/lab01_validate_run_folder.py ./my_run --relax-images
  python course/day-02/lab-01/lab01_validate_run_folder.py fixtures/sample_run_incomplete
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

METADATA_REQUIRED = ("schema_version", "created_utc", "operator")
PLAN_REQUIRED = ("schema_version", "checkpoints", "legs")
LEG_TYPES = frozenset({"increment", "velocity", "dwell"})


class ValidationResult:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    @property
    def ok(self) -> bool:
        return not self.errors


def _load_json(path: Path, result: ValidationResult) -> dict[str, Any] | None:
    if not path.is_file():
        result.error(f"missing file: {path.name}")
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        result.error(f"{path.name}: invalid JSON ({e})")
        return None
    if not isinstance(data, dict):
        result.error(f"{path.name}: root must be a JSON object")
        return None
    return data


def _validate_jsonl(path: Path, result: ValidationResult, *, min_lines: int = 1) -> int:
    if not path.is_file():
        result.error(f"missing file: {path.name}")
        return 0
    lines = path.read_text(encoding="utf-8").splitlines()
    non_empty = [ln for ln in lines if ln.strip()]
    if len(non_empty) < min_lines:
        result.error(f"{path.name}: need at least {min_lines} JSON line(s), got {len(non_empty)}")
        return 0
    for i, ln in enumerate(non_empty, start=1):
        try:
            json.loads(ln)
        except json.JSONDecodeError as e:
            result.error(f"{path.name} line {i}: {e}")
    return len(non_empty)


def _checkpoint_ids(plan: dict[str, Any], result: ValidationResult) -> list[str]:
    cps = plan.get("checkpoints")
    if not isinstance(cps, list) or not cps:
        result.error("patrol_plan.json: checkpoints must be a non-empty list")
        return []
    ids: list[str] = []
    for i, cp in enumerate(cps):
        if not isinstance(cp, dict):
            result.error(f"patrol_plan checkpoints[{i}]: must be object")
            continue
        cid = cp.get("id")
        if not cid or not isinstance(cid, str):
            result.error(f"patrol_plan checkpoints[{i}]: missing string id")
            continue
        if cid in ids:
            result.error(f"patrol_plan: duplicate checkpoint id {cid!r}")
            continue
        ids.append(cid)
    return ids


def _validate_legs(plan: dict[str, Any], cp_ids: list[str], result: ValidationResult) -> None:
    legs = plan.get("legs")
    if legs is None:
        result.warn("patrol_plan.json: no legs array (OK for scaffold-only run)")
        return
    if not isinstance(legs, list):
        result.error("patrol_plan.json: legs must be a list")
        return
    for i, leg in enumerate(legs):
        if not isinstance(leg, dict):
            result.error(f"patrol_plan legs[{i}]: must be object")
            continue
        ltype = leg.get("type")
        if ltype not in LEG_TYPES:
            result.warn(f"patrol_plan legs[{i}]: unknown type {ltype!r}")
        to_cp = leg.get("to_checkpoint")
        if to_cp and to_cp not in cp_ids:
            result.error(f"patrol_plan legs[{i}]: to_checkpoint {to_cp!r} not in checkpoints")
        if ltype == "increment":
            for axis in ("dx", "dy", "dyaw"):
                if axis not in leg:
                    result.warn(f"patrol_plan legs[{i}]: increment leg missing {axis}")


def _validate_metadata(meta: dict[str, Any], result: ValidationResult) -> None:
    for key in METADATA_REQUIRED:
        if key not in meta:
            result.error(f"metadata.json: missing {key!r}")
    if "checkpoints" in meta:
        cps = meta["checkpoints"]
        if not isinstance(cps, list):
            result.error("metadata.json: checkpoints must be a list of ids")
        elif cps and not all(isinstance(x, str) for x in cps):
            result.error("metadata.json: checkpoints entries must be strings")


def _validate_checkpoints_dir(
    run_dir: Path,
    cp_ids: list[str],
    result: ValidationResult,
    *,
    relax_images: bool,
) -> None:
    ck_root = run_dir / "checkpoints"
    if not ck_root.is_dir():
        result.error("missing directory: checkpoints/")
        return
    for cid in cp_ids:
        cp_dir = ck_root / cid
        if not cp_dir.is_dir():
            result.error(f"checkpoints/{cid}/ directory missing")
            continue
        frame = cp_dir / "frame.jpg"
        if relax_images:
            if not frame.is_file():
                result.warn(f"checkpoints/{cid}/frame.jpg missing (--relax-images)")
            continue
        if not frame.is_file():
            result.error(f"checkpoints/{cid}/frame.jpg missing")
            continue
        if frame.stat().st_size < 100:
            result.error(f"checkpoints/{cid}/frame.jpg too small (corrupt?)")
        slice_path = cp_dir / "state_slice.jsonl"
        if slice_path.is_file():
            _validate_jsonl(slice_path, result, min_lines=1)


def _cross_check_scenario(
    scenario: dict[str, Any],
    cp_ids: list[str],
    result: ValidationResult,
) -> None:
    sc_cps = scenario.get("checkpoints")
    if not isinstance(sc_cps, list):
        return
    scenario_ids = [
        str(cp["id"]) for cp in sc_cps if isinstance(cp, dict) and cp.get("id")
    ]
    if not scenario_ids:
        return
    missing = [sid for sid in scenario_ids if sid not in cp_ids]
    if missing:
        result.warn(
            f"scenario checkpoints not in patrol_plan: {missing} "
            "(OK if plan is a subset for dry-run)"
        )


def validate_run_folder(
    run_dir: Path,
    *,
    scenario_path: Path | None = None,
    relax_images: bool = False,
) -> ValidationResult:
    result = ValidationResult()
    if not run_dir.is_dir():
        result.error(f"not a directory: {run_dir}")
        return result

    meta = _load_json(run_dir / "metadata.json", result)
    plan = _load_json(run_dir / "patrol_plan.json", result)

    cp_ids: list[str] = []

    if meta:
        _validate_metadata(meta, result)

    if plan:
        for key in PLAN_REQUIRED:
            if key not in plan:
                result.error(f"patrol_plan.json: missing {key!r}")
        cp_ids = _checkpoint_ids(plan, result)
        _validate_legs(plan, cp_ids, result)
        if meta and isinstance(meta.get("checkpoints"), list):
            meta_ids = meta["checkpoints"]
            if meta_ids and cp_ids and set(meta_ids) != set(cp_ids):
                result.warn(
                    "metadata checkpoints list differs from patrol_plan checkpoint ids"
                )

    _validate_jsonl(run_dir / "sportmodestate.jsonl", result, min_lines=1)

    if cp_ids:
        _validate_checkpoints_dir(run_dir, cp_ids, result, relax_images=relax_images)

    if scenario_path and scenario_path.is_file() and plan:
        scenario = _load_json(scenario_path, result)
        if scenario:
            _cross_check_scenario(scenario, cp_ids, result)

    legacy_frame = run_dir / "frame_001.jpg"
    if legacy_frame.is_file() and not (run_dir / "checkpoints").is_dir():
        result.warn(
            "Day 1-style bundle (frame_001.jpg at root) — migrate to checkpoints/ for Day 2"
        )

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "run_dir",
        type=Path,
        help="Run folder to validate (e.g. fixtures/sample_run_pass)",
    )
    parser.add_argument(
        "--scenario",
        type=Path,
        default=None,
        help="Optional Lab 0 scenario JSON for cross-check",
    )
    parser.add_argument(
        "--relax-images",
        action="store_true",
        help="Do not require checkpoints/*/frame.jpg (scaffold / JSON-only)",
    )
    args = parser.parse_args()

    run_dir = args.run_dir
    if not run_dir.is_absolute():
        run_dir = (Path.cwd() / run_dir).resolve()

    print(f"Lab 1 — validate run folder: {run_dir}")
    result = validate_run_folder(
        run_dir,
        scenario_path=args.scenario,
        relax_images=args.relax_images,
    )

    for w in result.warnings:
        print(f"  WARN  {w}")
    for e in result.errors:
        print(f"  FAIL  {e}")

    if result.errors:
        print("Summary: FAIL")
        return 1
    if result.warnings:
        print(f"Summary: PASS with {len(result.warnings)} warning(s)")
        return 0
    print("Summary: PASS — run folder valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
