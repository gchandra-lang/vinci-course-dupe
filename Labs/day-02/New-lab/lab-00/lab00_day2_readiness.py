#!/usr/bin/env python3
"""
Lab 0 (Day 2) — Day 1 recap, patrol imports, optional robot check, scenario validation.

No motion commands.

Usage (from repo root):
  conda activate unitree_env
  export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
  unset CYCLONEDDS_URI

  python course/day-02/New-lab/lab-00/lab00_day2_readiness.py
  python course/day-02/New-lab/lab-00/lab00_day2_readiness.py en6
  python course/day-02/New-lab/lab-00/lab00_day2_readiness.py --validate-scenario my_team_scenario.json
  python course/day-02/New-lab/lab-00/lab00_day2_readiness.py --write-scenario my_team_scenario.json
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPTS_DIR = REPO_ROOT / "scripts"
VENDOR_SDK = REPO_ROOT / "vendor" / "unitree_sdk2_python"
DAY01 = REPO_ROOT / "course" / "day-01"
DAY01_NEW = DAY01 / "New-lab"
DAY02 = REPO_ROOT / "course" / "day-02"
DAY02_NEW = DAY02 / "New-lab"
DAY02_LAB00 = Path(__file__).resolve().parent
SCENARIO_TEMPLATE = DAY02_LAB00 / "patrol_scenario.template.json"

DAY1_NEW_REQUIRED = (
    "lab-00/lab00_readiness.py",
    "lab-01/lab01_ros_readiness.py",
    "lab-03/lab03_listen_sportmodestate.py",
    "lab-04/lab04_sport_readonly.py",
    "lab-05/lab05_safe_posture.py",
    "ros_basic_helpers.py",
)
DAY1_MAIN_REQUIRED = ("go2_motion_helpers.py",)

DAY2_PREREQ = (
    "lab-02/lab04_obstacle_avoid_intro.py",
    "lab-03/lab03_capture_inspection.py",
)

DAY2_VENDOR_PATHS = (
    "example/obstacles_avoid/obstacles_avoid_move.py",
    "example/obstacles_avoid/obstacles_avoid_switch.py",
    "example/go2/front_camera/camera_opencv.py",
    "unitree_sdk2py/go2/obstacles_avoid/obstacles_avoid_client.py",
)

SCENARIO_REQUIRED_TOP = (
    "schema_version",
    "team_name",
    "operator",
    "arena",
    "checkpoints",
    "motion_limits",
    "abort_rules",
    "deliverables",
)


def _ok(msg: str) -> None:
    print(f"  PASS  {msg}")


def _fail(msg: str) -> None:
    print(f"  FAIL  {msg}")


def _warn(msg: str) -> None:
    print(f"  WARN  {msg}")


def check_environment() -> bool:
    ok = True
    home = os.environ.get("CYCLONEDDS_HOME")
    if not home or not Path(home).is_dir():
        _fail("CYCLONEDDS_HOME missing or not a directory")
        ok = False
    else:
        _ok(f"CYCLONEDDS_HOME={home}")

    if os.environ.get("CYCLONEDDS_URI"):
        _warn("CYCLONEDDS_URI is set — unset before robot labs")
    else:
        _ok("CYCLONEDDS_URI unset")
    return ok


def check_day1_artifacts() -> bool:
    ok = True
    if not DAY01_NEW.is_dir():
        _fail(f"Day 1 New-lab missing: {DAY01_NEW}")
        return False
    for rel in DAY1_NEW_REQUIRED:
        path = DAY01_NEW / rel
        if path.is_file():
            _ok(f"day-01/New-lab/{rel}")
        else:
            _fail(f"missing day-01/New-lab/{rel}")
            ok = False
    for rel in DAY1_MAIN_REQUIRED:
        path = DAY01 / rel
        if path.is_file():
            _ok(f"day-01/{rel}")
        else:
            _fail(f"missing day-01/{rel}")
            ok = False
    return ok


def check_day2_early_labs() -> bool:
    """Labs 2–3 on Day 2 (avoid + capture) — complete before patrol labs 4+."""
    ok = True
    for rel in DAY2_PREREQ:
        path = DAY02_NEW / rel
        if path.is_file():
            _ok(f"day-02/New-lab/{rel}")
        else:
            _fail(f"missing day-02/New-lab/{rel}")
            ok = False
    return ok


def check_patrol_imports() -> bool:
    ok = True
    try:
        from unitree_sdk2py.go2.obstacles_avoid.obstacles_avoid_client import (
            ObstaclesAvoidClient,
        )

        _ = ObstaclesAvoidClient
        _ok("ObstaclesAvoidClient")
    except ImportError as e:
        _fail(f"ObstaclesAvoidClient: {e}")
        ok = False

    try:
        from unitree_sdk2py.go2.video.video_client import VideoClient

        _ = VideoClient
        _ok("VideoClient (checkpoint capture)")
    except ImportError as e:
        _fail(f"VideoClient: {e}")
        ok = False

    try:
        from unitree_sdk2py.comm.motion_switcher.motion_switcher_client import (
            MotionSwitcherClient,
        )

        _ = MotionSwitcherClient
        _ok("MotionSwitcherClient")
    except ImportError as e:
        _fail(f"MotionSwitcherClient: {e}")
        ok = False

    return ok


def check_vendor_patrol_examples() -> bool:
    ok = True
    if not VENDOR_SDK.is_dir():
        _fail(f"vendor SDK missing: {VENDOR_SDK}")
        return False
    _ok(f"vendor SDK: {VENDOR_SDK}")
    for rel in DAY2_VENDOR_PATHS:
        path = VENDOR_SDK / rel
        if path.is_file():
            _ok(rel)
        else:
            _fail(f"missing: {rel}")
            ok = False
    return ok


def validate_scenario(path: Path) -> bool:
    if not path.is_file():
        _fail(f"scenario file not found: {path}")
        return False

    try:
        data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        _fail(f"invalid JSON: {e}")
        return False

    ok = True
    for key in SCENARIO_REQUIRED_TOP:
        if key not in data:
            _fail(f"scenario missing key: {key}")
            ok = False

    cps = data.get("checkpoints")
    if not isinstance(cps, list) or len(cps) < 2:
        _fail("checkpoints must be a list with at least 2 entries")
        ok = False
    else:
        for i, cp in enumerate(cps):
            if not isinstance(cp, dict) or not cp.get("id"):
                _fail(f"checkpoint[{i}] needs id")
                ok = False

    limits = data.get("motion_limits")
    if isinstance(limits, dict):
        vx = limits.get("max_forward_vx_mps")
        dx = limits.get("max_increment_dx_m")
        if vx is not None and float(vx) > 0.35:
            _warn(f"max_forward_vx_mps={vx} — instructor cap is usually 0.25")
        if dx is not None and float(dx) > 0.8:
            _warn(f"max_increment_dx_m={dx} — keep small for class patrol")
    else:
        _fail("motion_limits must be an object")
        ok = False

    if ok:
        _ok(f"scenario valid: {path.name} ({len(cps)} checkpoints)")
    return ok


def write_scenario(dest: Path) -> bool:
    if not SCENARIO_TEMPLATE.is_file():
        _fail(f"template missing: {SCENARIO_TEMPLATE}")
        return False
    if dest.exists():
        _fail(f"refusing to overwrite: {dest}")
        return False
    shutil.copy2(SCENARIO_TEMPLATE, dest)
    _ok(f"wrote {dest}")
    print("  Edit team_name, operator, checkpoints, and motion_limits before Lab 2.")
    return True


def run_go2_connection_check(iface: str, skip_multicast: bool) -> int:
    script = SCRIPTS_DIR / "go2_connection_check.py"
    if not script.is_file():
        _fail(f"go2_connection_check.py not found: {script}")
        return 1
    cmd = [sys.executable, str(script), "--interface", iface]
    if skip_multicast:
        cmd.append("--skip-multicast")
    print(f"\n=== scripts/go2_connection_check.py ({iface}) ===")
    return subprocess.run(cmd, cwd=REPO_ROOT, check=False).returncode


def print_inspection_pipeline() -> None:
    print(
        """
=== Inspection pipeline (Day 2) ===

  ┌──────────┐   ┌──────────┐   ┌─────────────┐   ┌──────────┐   ┌─────────┐
  │ Sensors  │──►│ Log DDS  │──►│ Rules /     │──►│ Patrol   │──►│ Report  │
  │ camera,  │   │ JSONL +  │   │ scenario    │   │ avoid +  │   │ run     │
  │ state    │   │ images   │   │ card        │   │ capture  │   │ folder  │
  └──────────┘   └──────────┘   └─────────────┘   └──────────┘   └─────────┘

Day 1: single checkpoint + avoid intro
Day 2: multi-stop patrol + run folder (Labs 1–3)
"""
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "interface",
        nargs="?",
        default=None,
        help="Ethernet NIC (e.g. en6). Omit for machine-only checks.",
    )
    parser.add_argument(
        "--validate-scenario",
        metavar="PATH",
        default=None,
        help="Validate patrol scenario JSON and exit.",
    )
    parser.add_argument(
        "--write-scenario",
        metavar="PATH",
        default=None,
        help="Copy patrol_scenario.template.json to PATH.",
    )
    parser.add_argument(
        "--skip-multicast",
        action="store_true",
        help="Pass --skip-multicast to go2_connection_check.py",
    )
    args = parser.parse_args()

    if args.write_scenario:
        return 0 if write_scenario(Path(args.write_scenario)) else 1

    if args.validate_scenario:
        print("Lab 0 — scenario validation")
        return 0 if validate_scenario(Path(args.validate_scenario)) else 1

    print("Lab 0 (Day 2) — inspection readiness")
    print(f"  repo: {REPO_ROOT}")

    failed = False

    print("\n=== Environment ===")
    failed |= not check_environment()

    print("\n=== Day 1 artifacts (prerequisite) ===")
    failed |= not check_day1_artifacts()

    print("\n=== Day 2 lab scripts (avoid + capture) ===")
    failed |= not check_day2_early_labs()

    print("\n=== Day 2 patrol imports ===")
    failed |= not check_patrol_imports()

    print("\n=== Vendor patrol examples ===")
    failed |= not check_vendor_patrol_examples()

    print_inspection_pipeline()

    if failed:
        print("Summary: FAIL — fix environment or complete Day 1 labs")
        return 1

    print("Summary: PASS — Day 2 machine ready (no robot checks)")
    print("  Next:")
    print("    1. Copy scenario: python course/day-02/New-lab/lab-00/lab00_day2_readiness.py \\")
    print("         --write-scenario my_team_scenario.json")
    print("    2. Edit checkpoints and limits; validate:")
    print("         python course/day-02/New-lab/lab-00/lab00_day2_readiness.py \\")
    print("         --validate-scenario my_team_scenario.json")
    print("    3. Wire Go2 and re-run with interface:")
    print("         python course/day-02/New-lab/lab-00/lab00_day2_readiness.py en6")

    if args.interface is None:
        return 0

    code = run_go2_connection_check(args.interface, args.skip_multicast)
    if code == 0:
        print("\nLab 0 complete — proceed to Lab 1 (run folder schema)")
    elif code == 2:
        print("\nLab 0 PARTIAL — DDS OK; review CheckMode before patrol motion (Lab 2+)")
    else:
        print("\nLab 0 FAIL — see docs/GO2-FIELD-GUIDE.md")
    return code


if __name__ == "__main__":
    sys.exit(main())
