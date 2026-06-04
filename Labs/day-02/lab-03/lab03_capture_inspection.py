#!/usr/bin/env python3
"""
Lab 3 — Capture a front-camera frame and inspection data bundle (no sport motion).

Creates a directory with:
  metadata.json          — session, CheckMode, paths
  frame_001.jpg          — front camera (VideoClient)
  sportmodestate.jsonl   — optional short state log

Usage:
  conda activate unitree_env
  export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
  unset CYCLONEDDS_URI
  python course/day-02/lab-03/lab03_capture_inspection.py en6
  python course/day-02/lab-03/lab03_capture_inspection.py en6 --out-dir ./my_checkpoint
  python course/day-02/lab-03/lab03_capture_inspection.py en6 --gui
  python course/day-02/lab-03/lab03_capture_inspection.py en6 --operator "Team A" --state-log-sec 10
"""

from __future__ import annotations

import argparse
import json
import os
import socket
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from unitree_sdk2py.comm.motion_switcher.motion_switcher_client import (
    MotionSwitcherClient,
)
from unitree_sdk2py.core.channel import ChannelFactoryInitialize, ChannelSubscriber
from unitree_sdk2py.go2.video.video_client import VideoClient
from unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_


def _init_dds(iface: str) -> None:
    if os.environ.get("CYCLONEDDS_URI"):
        print("Warning: CYCLONEDDS_URI is set; unset it for interface-only init.")
        ChannelFactoryInitialize(0)
    else:
        ChannelFactoryInitialize(0, iface)


def _check_mode() -> dict[str, Any]:
    msc = MotionSwitcherClient()
    msc.SetTimeout(10.0)
    msc.Init()
    code, result = msc.CheckMode()
    name = ""
    if isinstance(result, dict):
        name = str(result.get("name", ""))
    return {"code": code, "result": result, "name": name}


def _capture_frame(
    client: VideoClient,
    max_wait_s: float,
) -> tuple[int, np.ndarray | None]:
    deadline = time.time() + max_wait_s
    last_code = -1
    while time.time() < deadline:
        last_code, data = client.GetImageSample()
        if last_code != 0 or not data:
            time.sleep(0.05)
            continue
        image_data = np.frombuffer(bytes(data), dtype=np.uint8)
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        if image is not None and image.size > 0:
            return 0, image
        time.sleep(0.05)
    return last_code, None


def _log_sportmodestate(out_path: Path, duration_s: float, rate_hz: float) -> int:
    records: list[dict[str, Any]] = []
    min_interval = 1.0 / rate_hz if rate_hz > 0 else 0.0
    last_write = 0.0
    start = time.time()

    def handler(msg: SportModeState_) -> None:
        nonlocal last_write
        now = time.time()
        if now - start > duration_s:
            return
        if records and now - last_write < min_interval:
            return
        last_write = now
        records.append(
            {
                "t": round(now, 3),
                "mode": int(msg.mode),
                "gait_type": int(msg.gait_type),
                "error_code": int(msg.error_code),
                "body_height": float(msg.body_height),
                "velocity": [float(msg.velocity[i]) for i in range(3)],
            }
        )

    sub = ChannelSubscriber("rt/sportmodestate", SportModeState_)
    sub.Init(handler, 10)
    while time.time() - start < duration_s:
        time.sleep(0.05)

    with out_path.open("w", encoding="utf-8") as fp:
        for row in records:
            fp.write(json.dumps(row) + "\n")
    return len(records)


def _preview_until_save(image: np.ndarray, out_path: Path) -> bool:
    print("GUI: s=save frame, ESC=quit without overwrite")
    cv2.imshow("lab03_front_camera", image)
    while True:
        key = cv2.waitKey(20) & 0xFF
        if key == 27:
            cv2.destroyWindow("lab03_front_camera")
            return False
        if key in (ord("s"), ord("S")):
            cv2.imwrite(str(out_path), image)
            cv2.destroyWindow("lab03_front_camera")
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "interface",
        nargs="?",
        default=os.environ.get("GO2_INTERFACE", "enp0s31f6"),
        help="Ethernet interface to robot",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Output directory (default: inspection_capture_<UTC>)",
    )
    parser.add_argument(
        "--operator",
        default=os.environ.get("USER", "operator"),
        help="Operator name for metadata",
    )
    parser.add_argument(
        "--robot-id",
        default="go2-01",
        help="Robot label for metadata",
    )
    parser.add_argument(
        "--state-log-sec",
        type=float,
        default=5.0,
        help="Seconds of sportmodestate JSONL (0=skip)",
    )
    parser.add_argument(
        "--state-log-hz",
        type=float,
        default=2.0,
        help="Max lines per second in sportmodestate log",
    )
    parser.add_argument(
        "--camera-wait",
        type=float,
        default=15.0,
        help="Max seconds to wait for a valid frame",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Show OpenCV window (press s to save, ESC to cancel)",
    )
    parser.add_argument(
        "--probe-json",
        type=Path,
        default=None,
        help="Merge lab03_platform_probe.py JSON into metadata (run probe first)",
    )
    args = parser.parse_args()

    if not os.environ.get("CYCLONEDDS_HOME"):
        print("ERROR: CYCLONEDDS_HOME is not set. See Lab 0.")
        return 1

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = args.out_dir or Path(f"inspection_capture_{ts}")
    out_dir.mkdir(parents=True, exist_ok=True)

    frame_path = out_dir / "frame_001.jpg"
    state_path = out_dir / "sportmodestate.jsonl"
    meta_path = out_dir / "metadata.json"

    print(f"Interface: {args.interface}")
    print(f"Output:    {out_dir.resolve()}")
    _init_dds(args.interface)

    mode_info = _check_mode()
    print(f"CheckMode: code={mode_info['code']} name={mode_info['name']!r}")

    video = VideoClient()
    video.SetTimeout(3.0)
    video.Init()

    print(f"Capturing front camera (max {args.camera_wait}s)...")
    code, image = _capture_frame(video, args.camera_wait)
    if image is None:
        print(f"FAIL: no valid frame (last GetImageSample code={code})")
        print("  Robot powered? Video service up? Try --camera-wait 30")
        return 1

    h, w = image.shape[:2]
    print(f"Frame: {w}x{h}")

    if args.gui:
        if not _preview_until_save(image, frame_path):
            print("GUI cancelled — no frame saved.")
            return 1
    else:
        cv2.imwrite(str(frame_path), image)

    print(f"Saved {frame_path}")

    n_state = 0
    if args.state_log_sec > 0:
        print(f"Logging sportmodestate {args.state_log_sec}s...")
        n_state = _log_sportmodestate(state_path, args.state_log_sec, args.state_log_hz)
        print(f"Saved {state_path} ({n_state} lines)")

    metadata: dict[str, Any] = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "operator": args.operator,
        "robot_id": args.robot_id,
        "host": socket.gethostname(),
        "interface": args.interface,
        "check_mode": mode_info,
        "artifacts": {
            "frame": frame_path.name,
            "sportmodestate_log": state_path.name if n_state else None,
        },
        "frame_size": {"width": w, "height": h},
        "notes": "Lab 3 inspection checkpoint — review image for scene/obstacles/lighting",
    }
    if args.probe_json and args.probe_json.is_file():
        metadata["platform_probe"] = json.loads(
            args.probe_json.read_text(encoding="utf-8")
        )
        print(f"Merged platform probe from {args.probe_json}")
    meta_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {meta_path}")

    print()
    print("Summary: PASS — inspection bundle ready")
    print(f"  ls {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
