"""Shared helpers for Day 1 ROS 2 + unitree_ros2 labs (ROS-Basic track)."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
HUMBLE_SETUP = Path("/opt/ros/humble/setup.bash")
CYCLONEDDS_INSTALL = "cyclonedds_ws/install/setup.bash"
EXAMPLE_INSTALL = "example/install/setup.bash"
UNITREE_PKGS = ("unitree_api", "unitree_go", "unitree_ros2_example")


@dataclass
class UnitreeRos2Candidate:
    label: str
    path: Path
    exists: bool
    built: bool
    has_git: bool


def unitree_ros2_candidates() -> list[UnitreeRos2Candidate]:
    """Known install locations: in-repo clone and ~/unitree_ros2."""
    env = os.environ.get("UNITREE_ROS2", "").strip()
    paths: list[tuple[str, Path]] = []
    if env:
        paths.append((f"UNITREE_ROS2 env ({env})", Path(env).expanduser()))
    paths.append(("in-repo", REPO_ROOT / "unitree_ros2"))
    paths.append(("home", Path.home() / "unitree_ros2"))

    seen: set[Path] = set()
    out: list[UnitreeRos2Candidate] = []
    for label, p in paths:
        resolved = p.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        cyclone = resolved / CYCLONEDDS_INSTALL
        out.append(
            UnitreeRos2Candidate(
                label=label,
                path=resolved,
                exists=resolved.is_dir(),
                built=cyclone.is_file(),
                has_git=(resolved / ".git").is_dir(),
            )
        )
    return out


def resolve_unitree_ros2(*, prefer_built: bool = True) -> Path | None:
    """
    Pick unitree_ros2 workspace root.

    Order: valid UNITREE_ROS2 env → built in-repo → built in home → first existing dir.
    """
    candidates = unitree_ros2_candidates()
    if prefer_built:
        for c in candidates:
            if c.built:
                return c.path
    for c in candidates:
        if c.exists:
            return c.path
    return None


def humble_available() -> bool:
    return HUMBLE_SETUP.is_file()


def resolve_ros_python() -> Path:
    """
    Interpreter for rclpy nodes. Must match ROS Humble (Python 3.10 on Ubuntu 22.04).

    Conda/base ``python3`` is often 3.11+ and breaks rclpy even after sourcing humble.
    """
    candidates = (
        Path("/usr/bin/python3.10"),
        Path("/usr/bin/python3"),
    )
    for exe in candidates:
        if not exe.is_file():
            continue
        proc = subprocess.run(
            [
                str(exe),
                "-c",
                "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode == 0 and proc.stdout.strip() == "3.10":
            return exe
    return Path("python3")


def source_shell_snippet(unitree_ros2: Path | None) -> str:
    lines = ["source /opt/ros/humble/setup.bash"]
    if unitree_ros2 and (unitree_ros2 / CYCLONEDDS_INSTALL).is_file():
        lines.append(f"source {unitree_ros2 / CYCLONEDDS_INSTALL}")
        ex = unitree_ros2 / EXAMPLE_INSTALL
        if ex.is_file():
            lines.append(f"source {ex}")
    return "\n".join(lines)


def run_in_ros_env(
    unitree_ros2: Path | None,
    command: str,
    *,
    timeout_s: float = 60.0,
) -> subprocess.CompletedProcess[str]:
    script = source_shell_snippet(unitree_ros2)
    script += f"\n{command}"
    return subprocess.run(
        ["bash", "-lc", script],
        capture_output=True,
        text=True,
        timeout=timeout_s,
        check=False,
    )


def list_unitree_packages(unitree_ros2: Path | None) -> tuple[bool, list[str], str]:
    proc = run_in_ros_env(unitree_ros2, "ros2 pkg list")
    if proc.returncode != 0:
        return False, [], (proc.stderr or proc.stdout or "ros2 pkg list failed").strip()
    pkgs = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
    return True, pkgs, ""


def missing_unitree_packages(unitree_ros2: Path | None) -> list[str]:
    ok, pkgs, _ = list_unitree_packages(unitree_ros2)
    if not ok:
        return list(UNITREE_PKGS)
    found = set(pkgs)
    return [p for p in UNITREE_PKGS if p not in found]
