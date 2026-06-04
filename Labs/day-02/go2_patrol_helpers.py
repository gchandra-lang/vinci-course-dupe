"""Shared Go2 patrol helpers for Day 2 — avoid legs, plan loading, cleanup, capture."""

from __future__ import annotations

import json
import shutil
import socket
import time
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from unitree_sdk2py.comm.motion_switcher.motion_switcher_client import (
    MotionSwitcherClient,
)
from unitree_sdk2py.core.channel import ChannelSubscriber
from unitree_sdk2py.go2.obstacles_avoid.obstacles_avoid_client import (
    ObstaclesAvoidClient,
)
from unitree_sdk2py.go2.sport.sport_client import SportClient
from unitree_sdk2py.go2.video.video_client import VideoClient
from unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_

DEFAULT_MAX_VX = 0.25
DEFAULT_MAX_INCREMENT_DX = 0.5


def load_patrol_plan(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("patrol_plan root must be object")
    if "checkpoints" not in data or "legs" not in data:
        raise ValueError("patrol_plan missing checkpoints or legs")
    return data


def load_scenario_limits(path: Path | None) -> dict[str, float]:
    if path is None or not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    limits = data.get("motion_limits")
    if not isinstance(limits, dict):
        return {}
    out: dict[str, float] = {}
    for key in ("max_forward_vx_mps", "max_increment_dx_m", "max_increment_dy_m", "max_vyaw_rad_s"):
        if key in limits and limits[key] is not None:
            out[key] = float(limits[key])
    return out


def clamp_plan_to_limits(
    plan: dict[str, Any],
    limits: dict[str, float],
) -> list[str]:
    """Clamp leg speeds in-place; return warning messages."""
    warnings: list[str] = []
    max_dx = limits.get("max_increment_dx_m", DEFAULT_MAX_INCREMENT_DX)
    max_dy = limits.get("max_increment_dy_m", max_dx)
    max_vyaw = limits.get("max_vyaw_rad_s", 0.5)

    for i, leg in enumerate(plan.get("legs") or []):
        if not isinstance(leg, dict):
            continue
        if leg.get("type") == "increment":
            for axis, cap, name in (
                ("dx", max_dx, "dx"),
                ("dy", max_dy, "dy"),
                ("dyaw", max_vyaw, "dyaw"),
            ):
                if axis not in leg:
                    continue
                val = float(leg[axis])
                if abs(val) > cap:
                    warnings.append(
                        f"legs[{i}].{name} {val} clamped to {cap} (scenario limit)"
                    )
                    leg[axis] = cap if val > 0 else -cap
        elif leg.get("type") == "velocity":
            cap_vx = limits.get("max_forward_vx_mps", DEFAULT_MAX_VX)
            if "vx" in leg and abs(float(leg["vx"])) > cap_vx:
                warnings.append(f"legs[{i}].vx clamped to {cap_vx}")
                leg["vx"] = cap_vx if float(leg["vx"]) > 0 else -cap_vx
    return warnings


def enable_avoid(avoid: ObstaclesAvoidClient, timeout_s: float = 3.0) -> bool:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if avoid.SwitchSet(True) == 0:
            code, on = avoid.SwitchGet()
            if code == 0 and on:
                return True
        time.sleep(0.1)
    return False


def release_avoid(
    avoid: ObstaclesAvoidClient,
    sport: SportClient | None = None,
) -> None:
    for _ in range(15):
        avoid.Move(0.0, 0.0, 0.0)
        time.sleep(0.05)
    try:
        avoid.UseRemoteCommandFromApi(False)
    except Exception:
        pass
    time.sleep(0.3)
    avoid.SwitchSet(False)
    if sport is not None:
        sport.StopMove()


def run_increment_leg(
    avoid: ObstaclesAvoidClient,
    dx: float,
    dy: float,
    dyaw: float,
    *,
    pulses: int = 3,
    pulse_hz: float = 2.0,
    settle_s: float = 5.0,
    stream: bool = False,
    stream_duration_s: float = 8.0,
    stream_hz: float = 10.0,
) -> int:
    """
    Increment goal for one patrol leg.

    Default (recommended): send the increment goal a few times, then wait for motion
    to finish — avoids flooding MoveToIncrementPosition for the whole leg window.

    stream=True: legacy Lab 2 behaviour (repeat goal for stream_duration_s).
    """
    if stream:
        interval = 1.0 / stream_hz if stream_hz > 0 else 0.1
        end = time.time() + stream_duration_s
        n = 0
        while time.time() < end:
            avoid.MoveToIncrementPosition(dx, dy, dyaw)
            n += 1
            time.sleep(interval)
        print(
            f"  [stream] {n}× MoveToIncrementPosition({dx}, {dy}, {dyaw}) "
            f"over {stream_duration_s}s"
        )
        return n

    interval = 1.0 / pulse_hz if pulse_hz > 0 else 0.5
    n = max(1, pulses)
    for _ in range(n):
        avoid.MoveToIncrementPosition(dx, dy, dyaw)
        time.sleep(interval)
    print(
        f"  {n}× MoveToIncrementPosition({dx}, {dy}, {dyaw}), "
        f"then settle {settle_s}s"
    )
    time.sleep(settle_s)
    return n


def run_velocity_leg(
    avoid: ObstaclesAvoidClient,
    vx: float,
    vy: float,
    vyaw: float,
    duration_s: float,
    hz: float = 20.0,
) -> int:
    interval = 1.0 / hz if hz > 0 else 0.05
    end = time.time() + duration_s
    n = 0
    while time.time() < end:
        avoid.Move(vx, vy, vyaw)
        n += 1
        time.sleep(interval)
    print(f"  Sent {n} Move({vx}, {vy}, {vyaw}) over {duration_s}s")
    return n


def checkpoint_dwell(checkpoints: list[dict[str, Any]], cp_id: str, default_s: float) -> float:
    for cp in checkpoints:
        if isinstance(cp, dict) and cp.get("id") == cp_id:
            return float(cp.get("dwell_s", default_s))
    return default_s


def checkpoint_ids(plan: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for cp in plan.get("checkpoints") or []:
        if isinstance(cp, dict) and cp.get("id"):
            out.append(str(cp["id"]))
    return out


def check_mode() -> dict[str, Any]:
    msc = MotionSwitcherClient()
    msc.SetTimeout(10.0)
    msc.Init()
    code, result = msc.CheckMode()
    name = ""
    if isinstance(result, dict):
        name = str(result.get("name", ""))
    return {"code": code, "result": result, "name": name}


def init_run_directory(
    base: Path | None,
    *,
    plan_path: Path,
) -> Path:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = base or Path(f"run_{ts}")
    run_dir = run_dir.resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "checkpoints").mkdir(exist_ok=True)
    shutil.copy2(plan_path, run_dir / "patrol_plan.json")
    return run_dir


def write_run_metadata(
    run_dir: Path,
    *,
    operator: str,
    interface: str,
    plan_path: Path,
    checkpoint_list: list[str],
    check_mode_info: dict[str, Any],
    captures: dict[str, str],
    extra: dict[str, Any] | None = None,
) -> Path:
    meta: dict[str, Any] = {
        "schema_version": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "operator": operator,
        "robot_id": "go2-01",
        "host": socket.gethostname(),
        "interface": interface,
        "lab": "day-02-lab-03-patrol-runner",
        "plan_file": plan_path.name,
        "checkpoints": checkpoint_list,
        "check_mode": check_mode_info,
        "artifacts": {
            "patrol_plan": "patrol_plan.json",
            "sportmodestate_log": "sportmodestate.jsonl",
        },
        "captures": captures,
    }
    if extra:
        meta.update(extra)
    meta_path = run_dir / "metadata.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return meta_path


class PatrolStateLogger:
    """Append sportmodestate samples to JSONL during patrol."""

    def __init__(self, out_path: Path, rate_hz: float = 5.0) -> None:
        self.out_path = out_path
        self.rate_hz = rate_hz
        self._fp = None
        self._last_write = 0.0
        self._count = 0
        self._sub: ChannelSubscriber | None = None

    def _row(self, msg: SportModeState_) -> dict[str, Any]:
        return {
            "t": round(time.time(), 3),
            "mode": int(msg.mode),
            "gait_type": int(msg.gait_type),
            "error_code": int(msg.error_code),
            "body_height": float(msg.body_height),
            "velocity": [float(msg.velocity[i]) for i in range(3)],
        }

    def _handler(self, msg: SportModeState_) -> None:
        if self._fp is None:
            return
        now = time.time()
        min_interval = 1.0 / self.rate_hz if self.rate_hz > 0 else 0.0
        if self._count and now - self._last_write < min_interval:
            return
        self._last_write = now
        self._fp.write(json.dumps(self._row(msg)) + "\n")
        self._fp.flush()
        self._count += 1

    def start(self) -> None:
        self.out_path.parent.mkdir(parents=True, exist_ok=True)
        self._fp = self.out_path.open("w", encoding="utf-8")
        self._sub = ChannelSubscriber("rt/sportmodestate", SportModeState_)
        self._sub.Init(self._handler, 10)

    def stop(self) -> int:
        if self._sub is not None:
            self._sub = None
        if self._fp is not None:
            self._fp.close()
            self._fp = None
        return self._count

    def write_slice(self, cp_dir: Path, window_s: float = 1.0) -> int:
        """Copy recent tail of log into checkpoint state_slice.jsonl (best-effort)."""
        if not self.out_path.is_file():
            return 0
        lines = self.out_path.read_text(encoding="utf-8").splitlines()
        tail = lines[-max(1, int(window_s * self.rate_hz)) :]
        slice_path = cp_dir / "state_slice.jsonl"
        slice_path.write_text("\n".join(tail) + ("\n" if tail else ""), encoding="utf-8")
        return len(tail)


def capture_frame(
    video: VideoClient,
    out_path: Path,
    *,
    max_wait_s: float = 15.0,
) -> tuple[bool, int, int]:
    """Save front camera frame; returns ok, width, height."""
    import cv2
    import numpy as np

    deadline = time.time() + max_wait_s
    last_code = -1
    while time.time() < deadline:
        last_code, data = video.GetImageSample()
        if last_code != 0 or not data:
            time.sleep(0.05)
            continue
        image_data = np.frombuffer(bytes(data), dtype=np.uint8)
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        if image is not None and image.size > 0:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(out_path), image)
            h, w = image.shape[:2]
            return True, w, h
        time.sleep(0.05)
    print(f"  FAIL capture (last code={last_code})")
    return False, 0, 0


def capture_checkpoint(
    video: VideoClient,
    run_dir: Path,
    cp_id: str,
    *,
    camera_wait_s: float,
    state_logger: PatrolStateLogger | None = None,
) -> bool:
    cp_dir = run_dir / "checkpoints" / cp_id
    cp_dir.mkdir(parents=True, exist_ok=True)
    frame_path = cp_dir / "frame.jpg"
    ok, w, h = capture_frame(video, frame_path, max_wait_s=camera_wait_s)
    if ok:
        print(f"  Saved {frame_path} ({w}x{h})")
        if state_logger is not None:
            n = state_logger.write_slice(cp_dir, window_s=1.5)
            if n:
                print(f"  state_slice.jsonl ({n} lines)")
    return ok


def run_patrol_legs(
    avoid: ObstaclesAvoidClient,
    plan: dict[str, Any],
    *,
    leg_pulses: int = 3,
    pulse_hz: float = 2.0,
    settle_s: float = 5.0,
    stream: bool = False,
    stream_hz: float = 10.0,
    default_dwell: float = 2.0,
    on_after_checkpoint: Callable[[str, int], None] | None = None,
    log_step: Callable[[str], None] | None = None,
) -> None:
    """Execute all legs; optional callback after dwell at each to_checkpoint."""
    checkpoints: list[dict[str, Any]] = list(plan.get("checkpoints") or [])
    legs = [lg for lg in (plan.get("legs") or []) if isinstance(lg, dict)]

    for i, leg in enumerate(legs, start=1):
        ltype = str(leg.get("type", "increment"))
        to_cp = str(leg.get("to_checkpoint", f"leg{i}"))

        if log_step:
            log_step(f"Leg {i}: {ltype} → {to_cp}")

        if ltype == "increment":
            run_increment_leg(
                avoid,
                float(leg.get("dx", 0.0)),
                float(leg.get("dy", 0.0)),
                float(leg.get("dyaw", 0.0)),
                pulses=leg_pulses,
                pulse_hz=pulse_hz,
                settle_s=settle_s,
                stream=stream,
                stream_duration_s=settle_s,
                stream_hz=stream_hz,
            )
        elif ltype == "velocity":
            run_velocity_leg(
                avoid,
                float(leg.get("vx", 0.0)),
                float(leg.get("vy", 0.0)),
                float(leg.get("vyaw", 0.0)),
                float(leg.get("duration_s", settle_s)),
                stream_hz,
            )
        else:
            print(f"WARN: skip unknown leg type {ltype!r}")
            continue

        dwell = checkpoint_dwell(checkpoints, to_cp, default_dwell)
        if log_step:
            log_step(f"Dwell at {to_cp} ({dwell}s)")
        time.sleep(dwell)

        if on_after_checkpoint is not None:
            on_after_checkpoint(to_cp, i)
