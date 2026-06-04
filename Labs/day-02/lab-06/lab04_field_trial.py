#!/usr/bin/env python3
"""
Lab 4 (Day 2) — Field trial: tuned plan + Lab 3 patrol run + field_test.md report.

Usage:
  # 1) Tune plan (no robot)
  python course/day-02/lab-06/lab04_tune_plan.py \\
    ../lab-04/patrol_plan.cone_course.json --out course/day-02/lab-04/patrol_plan.tuned.json \\
    --leg 1 --dyaw 0.7 --leg 2 --dx 0.25

  # 2) Field trial run
  python course/day-02/lab-06/lab04_field_trial.py en6 -y \\
    --plan course/day-02/lab-04/patrol_plan.tuned.json \\
    --baseline-run run_20260526T132200Z \\
    --cp-results cp_A:pass,cp_B:partial,cp_C:pass \\
    --notes "Increased dyaw; reduced final dx before wall"
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_REPO = Path(__file__).resolve().parents[3]
_LAB04 = Path(__file__).resolve().parent
_LAB03 = _LAB04.parent / "lab-03" / "lab03_patrol_runner.py"
_VALIDATOR = _LAB04.parent / "lab-01" / "lab01_validate_run_folder.py"
_TEMPLATE = _LAB04 / "field_test.template.md"
_DEFAULT_PLAN = _LAB04 / "patrol_plan.tuned.json"


def _parse_cp_results(s: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in s.split(","):
        part = part.strip()
        if ":" not in part:
            continue
        cp, status = part.split(":", 1)
        out[cp.strip()] = status.strip().lower()
    return out


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _write_field_test(
    out_path: Path,
    *,
    operator: str,
    interface: str,
    baseline_run: Path | None,
    trial_run: Path,
    plan_path: Path,
    cp_results: dict[str, str],
    notes: str,
    validator_ok: bool,
    patrol_exit: int,
) -> None:
    baseline_meta = _load_json(baseline_run / "metadata.json") if baseline_run else None
    trial_meta = _load_json(trial_run / "metadata.json")

    lines = [
        "# Field test report — Day 2 Lab 4",
        "",
        f"**Generated:** {datetime.now(timezone.utc).isoformat()}",
        f"**Operator:** {operator}",
        f"**Interface:** {interface}",
        "",
        "## Run folders",
        "",
        "| Run | Path | Plan |",
        "|-----|------|------|",
    ]
    if baseline_run:
        lines.append(
            f"| Baseline | `{baseline_run}` | "
            f"{(baseline_meta or {}).get('plan_file', '?')} |"
        )
    lines.append(f"| Field trial | `{trial_run}` | `{plan_path.name}` |")
    lines.append("")
    lines.append("## Checkpoint results")
    lines.append("")
    lines.append("| Checkpoint | Result | Capture |")
    lines.append("|------------|--------|---------|")
    captures = (trial_meta or {}).get("captures") or {}
    for cp, status in cp_results.items():
        cap = "pass" if cp in captures else "missing"
        lines.append(f"| {cp} | {status} | {cap} |")
    if not cp_results:
        lines.append("| *(none recorded)* | | |")
    lines.append("")
    lines.append("## Operator notes")
    lines.append("")
    lines.append(notes if notes else "_(none)_")
    lines.append("")
    lines.append("## Automated checks")
    lines.append("")
    lines.append(f"- Patrol runner exit code: **{patrol_exit}**")
    lines.append(
        f"- Validator: **{'PASS' if validator_ok else 'FAIL or skipped'}**"
    )
    lines.append("")
    lines.append("## Tuning reference")
    lines.append("")
    lines.append(f"Plan file: `{plan_path.resolve()}`")
    if trial_meta:
        lines.append(f"- CheckMode: `{trial_meta.get('check_mode', {})}`")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        "See also [`field_test.template.md`](field_test.template.md) for manual sign-off."
    )
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("interface", nargs="?", default=os.environ.get("GO2_INTERFACE", "enp0s31f6"))
    parser.add_argument(
        "--plan",
        type=Path,
        default=_DEFAULT_PLAN,
        help="Tuned patrol_plan.json (create with lab04_tune_plan.py)",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Field-trial run folder (default: run_field_<UTC>)",
    )
    parser.add_argument(
        "--baseline-run",
        type=Path,
        default=None,
        help="Previous Lab 3 run folder for comparison in report",
    )
    parser.add_argument(
        "--cp-results",
        default="cp_A:pass,cp_B:pass,cp_C:pass",
        help="Comma list cp_ID:pass|partial|fail (your observation)",
    )
    parser.add_argument("--notes", default="", help="Free-text tuning / field observations")
    parser.add_argument("--operator", default=os.environ.get("USER", "operator"))
    parser.add_argument("--dry-run", action="store_true", help="Print plan only; no robot")
    parser.add_argument("--skip-patrol", action="store_true", help="Write report only (no robot)")
    parser.add_argument("-y", "--yes", action="store_true")
    args = parser.parse_args()

    if not os.environ.get("CYCLONEDDS_HOME"):
        print("ERROR: CYCLONEDDS_HOME is not set.")
        return 1

    plan_path = args.plan.resolve()
    if not plan_path.is_file():
        print(f"ERROR: plan not found: {plan_path}")
        print("  Create with lab04_tune_plan.py first.")
        return 1

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = (args.out_dir or Path(f"run_field_{ts}")).resolve()

    print(f"Interface: {args.interface}")
    print(f"Plan:      {plan_path}")
    print(f"Run dir:   {run_dir}")

    if args.dry_run:
        print("[dry-run] Would run lab03_patrol_runner.py then write field_test.md")
        print(f"  cp-results: {args.cp_results}")
        return 0

    if args.skip_patrol:
        if not run_dir.is_dir():
            print(f"ERROR: --skip-patrol needs existing run dir: {run_dir}")
            return 1
        patrol_exit = 0
        validator_ok = False
    else:
        if not _LAB03.is_file():
            print(f"ERROR: missing {_LAB03}")
            return 1
        cmd = [
            sys.executable,
            str(_LAB03),
            args.interface,
            "--plan",
            str(plan_path),
            "--out-dir",
            str(run_dir),
            "--validate",
        ]
        if args.yes:
            cmd.append("-y")
        print("\n=== Lab 3 patrol (field trial) ===")
        print(" ".join(cmd))
        r = subprocess.run(cmd, cwd=_REPO, check=False)
        patrol_exit = r.returncode

        validator_ok = False
        if _VALIDATOR.is_file() and run_dir.is_dir():
            vr = subprocess.run(
                [sys.executable, str(_VALIDATOR), str(run_dir)],
                cwd=_REPO,
                check=False,
            )
            validator_ok = vr.returncode == 0

    field_test_path = run_dir / "field_test.md"
    if run_dir.is_dir():
        _write_field_test(
            field_test_path,
            operator=args.operator,
            interface=args.interface,
            baseline_run=args.baseline_run.resolve() if args.baseline_run else None,
            trial_run=run_dir,
            plan_path=plan_path,
            cp_results=_parse_cp_results(args.cp_results),
            notes=args.notes,
            validator_ok=validator_ok,
            patrol_exit=patrol_exit,
        )

    if patrol_exit != 0:
        print("Summary: FAIL — patrol runner error")
        return patrol_exit

    print()
    print("Summary: PASS — Lab 4 field trial complete")
    print(f"  Run folder: {run_dir}")
    print(f"  Report:     {field_test_path}")
    print("  Next: Lab 5 mini-project")
    return 0


if __name__ == "__main__":
    sys.exit(main())
