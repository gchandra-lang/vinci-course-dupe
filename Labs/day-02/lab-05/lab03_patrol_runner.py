#!/usr/bin/env python3
"""
Lab 3 (Day 2) — Patrol + per-checkpoint camera capture + run folder.

Combines Lab 2 motion with Lab 1 VideoClient capture. Writes a full Day 2 run tree.

Usage:
  python course/day-02/lab-05/lab03_patrol_runner.py en6 --dry-run
  python course/day-02/lab-05/lab03_patrol_runner.py en6
  python course/day-02/lab-05/lab03_patrol_runner.py en6 --plan ../lab-04/patrol_plan.cone_course.json
  python course/day-02/lab-05/lab03_patrol_runner.py en6 --out-dir ./run_team_a -y --validate
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

_REPO = Path(__file__).resolve().parents[3]
_DAY02 = Path(__file__).resolve().parents[1]
_DAY01 = _DAY02.parent / "day-01"
for _p in (_DAY01, _DAY02):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from go2_motion_helpers import visible_stand_prep  # noqa: E402
from go2_patrol_helpers import (  # noqa: E402
    PatrolStateLogger,
    capture_checkpoint,
    check_mode,
    checkpoint_ids,
    clamp_plan_to_limits,
    enable_avoid,
    init_run_directory,
    load_patrol_plan,
    load_scenario_limits,
    release_avoid,
    run_patrol_legs,
    write_run_metadata,
)

from unitree_sdk2py.core.channel import ChannelFactoryInitialize, ChannelSubscriber
from unitree_sdk2py.go2.obstacles_avoid.obstacles_avoid_client import (
    ObstaclesAvoidClient,
)
from unitree_sdk2py.go2.sport.sport_client import SportClient
from unitree_sdk2py.go2.video.video_client import VideoClient
from unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_

LAB03 = Path(__file__).resolve().parent
DEFAULT_PLAN = _DAY02 / "lab-02" / "patrol_plan.cone_course.json"
VALIDATOR = _DAY02 / "lab-01" / "lab01_validate_run_folder.py"


def _init_dds(iface: str) -> None:
    if os.environ.get("CYCLONEDDS_URI"):
        print("Warning: CYCLONEDDS_URI is set; unset it for interface-only init.")
        ChannelFactoryInitialize(0)
    else:
        ChannelFactoryInitialize(0, iface)


def _wait_sportmodestate(timeout_s: float = 8.0) -> bool:
    got: list[int] = []

    def handler(msg: SportModeState_) -> None:
        got.append(1)

    sub = ChannelSubscriber("rt/sportmodestate", SportModeState_)
    sub.Init(handler, 10)
    deadline = time.time() + timeout_s
    while time.time() < deadline and not got:
        time.sleep(0.05)
    return bool(got)


def _confirm() -> bool:
    print()
    print("WARNING: Robot will STAND UP, patrol, and capture at checkpoints.")
    print("  - Cleared course; spotter required.")
    try:
        return input("Type yes to continue: ").strip().lower() in ("yes", "y")
    except EOFError:
        print("No TTY — use a real terminal or --dry-run")
        return False


def _dry_run(plan: dict[str, Any], run_dir: Path, cp_ids: list[str]) -> None:
    print(f"[dry-run] Run folder: {run_dir}")
    print("[dry-run] StandUp → BalanceStand → log sportmodestate → avoid on")
    print(f"[dry-run] Capture cp_A at {run_dir}/checkpoints/cp_A/frame.jpg")
    for i, leg in enumerate(plan.get("legs") or [], start=1):
        if not isinstance(leg, dict):
            continue
        to_cp = leg.get("to_checkpoint", "?")
        print(f"[dry-run] leg {i} ({leg.get('type')}) → dwell → capture {to_cp}")
    print("[dry-run] stop → metadata.json → validate")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("interface", nargs="?", default=os.environ.get("GO2_INTERFACE", "enp0s31f6"))
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--scenario", type=Path, default=None)
    parser.add_argument("--out-dir", type=Path, default=None)
    parser.add_argument("--operator", default=os.environ.get("USER", "operator"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-stand", action="store_true")
    parser.add_argument("--stand-up-wait", type=float, default=5.0)
    parser.add_argument("--leg-wait", type=float, default=5.0)
    parser.add_argument("--leg-pulses", type=int, default=3)
    parser.add_argument("--leg-hz", type=float, default=2.0)
    parser.add_argument("--stream-increment", action="store_true")
    parser.add_argument("--default-dwell", type=float, default=2.0)
    parser.add_argument("--camera-wait", type=float, default=15.0)
    parser.add_argument("--state-log-hz", type=float, default=5.0)
    parser.add_argument("--no-capture", action="store_true", help="Patrol only (no VideoClient)")
    parser.add_argument("--validate", action="store_true", help="Run lab01_validate_run_folder.py after")
    parser.add_argument("-y", "--yes", action="store_true")
    args = parser.parse_args()

    if not os.environ.get("CYCLONEDDS_HOME"):
        print("ERROR: CYCLONEDDS_HOME is not set.")
        return 1

    plan_path = args.plan.resolve()
    if not plan_path.is_file():
        print(f"ERROR: plan not found: {plan_path}")
        return 1

    try:
        plan = load_patrol_plan(plan_path)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"ERROR: {e}")
        return 1

    limits = load_scenario_limits(args.scenario.resolve() if args.scenario else None)
    for msg in clamp_plan_to_limits(plan, limits):
        print(f"WARN: {msg}")

    cp_ids = checkpoint_ids(plan)
    if not cp_ids:
        print("ERROR: plan has no checkpoint ids")
        return 1

    print(f"Interface: {args.interface}")
    print(f"Plan:      {plan_path}")

    if args.dry_run:
        preview = args.out_dir or Path("run_<UTC>")
        _dry_run(plan, preview.resolve() if args.out_dir else preview, cp_ids)
        return 0

    run_dir = init_run_directory(args.out_dir, plan_path=plan_path)
    print(f"Run dir:   {run_dir}")

    if not args.yes and not _confirm():
        print("Aborted.")
        return 1

    _init_dds(args.interface)
    if not _wait_sportmodestate():
        print("FAIL: no rt/sportmodestate")
        return 1

    mode_info = check_mode()
    print(f"CheckMode: code={mode_info['code']} name={mode_info['name']!r}")

    sport = SportClient()
    sport.SetTimeout(10.0)
    sport.Init()

    avoid = ObstaclesAvoidClient()
    avoid.SetTimeout(3.0)
    avoid.Init()

    video: VideoClient | None = None
    if not args.no_capture:
        video = VideoClient()
        video.SetTimeout(3.0)
        video.Init()

    state_log = PatrolStateLogger(run_dir / "sportmodestate.jsonl", rate_hz=args.state_log_hz)
    captures: dict[str, str] = {}
    capture_fail = False

    def _capture(cp_id: str, label: str) -> None:
        nonlocal capture_fail
        if args.no_capture or video is None:
            print(f"  [skip capture] {cp_id}")
            return
        print(f"  Capture {cp_id} ({label})")
        if not capture_checkpoint(
            video,
            run_dir,
            cp_id,
            camera_wait_s=args.camera_wait,
            state_logger=state_log,
        ):
            capture_fail = True
        else:
            captures[cp_id] = f"checkpoints/{cp_id}/frame.jpg"

    step = 1

    def nxt(msg: str) -> None:
        nonlocal step
        print(f"[{step}] {msg}")
        step += 1

    try:
        nxt("Visible stand prep")
        visible_stand_prep(sport, skip=args.skip_stand, stand_up_wait_s=args.stand_up_wait)

        nxt("Start sportmodestate log")
        state_log.start()
        print(f"  Logging → {run_dir / 'sportmodestate.jsonl'}")

        nxt("Capture start checkpoint")
        start_cp = cp_ids[0]
        _capture(start_cp, "before patrol")

        nxt("Enable obstacle avoidance")
        if not enable_avoid(avoid):
            print("FAIL: avoid switch")
            return 1

        nxt("UseRemoteCommandFromApi(True)")
        avoid.UseRemoteCommandFromApi(True)
        time.sleep(0.5)

        def after_cp(cp_id: str, leg_i: int) -> None:
            _capture(cp_id, f"after leg {leg_i}")

        run_patrol_legs(
            avoid,
            plan,
            leg_pulses=args.leg_pulses,
            pulse_hz=args.leg_hz,
            settle_s=args.leg_wait,
            stream=args.stream_increment,
            stream_hz=args.leg_hz,
            default_dwell=args.default_dwell,
            on_after_checkpoint=after_cp,
            log_step=nxt,
        )

        nxt("Stop and release avoid")
        release_avoid(avoid, sport)

    except KeyboardInterrupt:
        print("\nInterrupt — stopping...")
        release_avoid(avoid, sport)
        state_log.stop()
        return 130

    n_lines = state_log.stop()
    print(f"  sportmodestate.jsonl: {n_lines} lines")

    meta_path = write_run_metadata(
        run_dir,
        operator=args.operator,
        interface=args.interface,
        plan_path=plan_path,
        checkpoint_list=cp_ids,
        check_mode_info=mode_info,
        captures=captures,
    )
    print(f"  Wrote {meta_path}")

    if args.validate and VALIDATOR.is_file():
        print("\n=== validate run folder ===")
        r = subprocess.run(
            [sys.executable, str(VALIDATOR), str(run_dir)],
            cwd=_REPO,
            check=False,
        )
        if r.returncode != 0:
            print("WARN: validator reported issues (missing frames?)")
        elif capture_fail:
            print("WARN: one or more captures failed — folder may be incomplete")
        else:
            print("Validator: PASS")
    elif capture_fail:
        print("Summary: PARTIAL — patrol done, some captures failed")
        return 2

    print()
    print("Summary: PASS — Lab 3 patrol run folder ready")
    print(f"  ls {run_dir}")
    print(f"  python course/day-02/lab-01/lab01_validate_run_folder.py {run_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
