#!/usr/bin/env python3
"""
Lab 0 — Go2 environment, SDK layout, and optional on-robot readiness.

No motion commands. Use this script for Lab 0 deliverables.

Usage (from repo root):
  conda activate unitree_env
  export CYCLONEDDS_HOME="$HOME/cyclonedds/install"

  # A. Machine only (no robot)
  python course/day-01/New-lab/lab-00/lab00_readiness.py

  # B. Robot on, wired to Go2
  python course/day-01/New-lab/lab-00/lab00_readiness.py en6
  python course/day-01/New-lab/lab-00/lab00_readiness.py en6 --skip-multicast

Also runs scripts/verify_install.py import checks unless --skip-verify.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPTS_DIR = REPO_ROOT / "scripts"
VENDOR_SDK = REPO_ROOT / "vendor" / "unitree_sdk2_python"

GO2_EXAMPLE_PATHS = (
    "example/go2/high_level/go2_sport_client.py",
    "example/go2/front_camera/camera_opencv.py",
    "example/obstacles_avoid/obstacles_avoid_switch.py",
    "unitree_sdk2py/go2/sport/sport_client.py",
)


def _ok(msg: str) -> None:
    print(f"  PASS  {msg}")


def _fail(msg: str) -> None:
    print(f"  FAIL  {msg}")


def check_cyclonedds_home() -> bool:
    home = os.environ.get("CYCLONEDDS_HOME")
    if not home:
        _fail("CYCLONEDDS_HOME is not set")
        print("        export CYCLONEDDS_HOME=\"$HOME/cyclonedds/install\"")
        return False
    if not Path(home).is_dir():
        _fail(f"CYCLONEDDS_HOME path missing: {home}")
        return False
    _ok(f"CYCLONEDDS_HOME={home}")
    return True


def check_cyclonedds_uri() -> bool:
    if os.environ.get("CYCLONEDDS_URI"):
        print("  WARN  CYCLONEDDS_URI is set — unset before robot labs:")
        print("        unset CYCLONEDDS_URI")
        return True
    _ok("CYCLONEDDS_URI unset")
    return True


def check_vendor_tree() -> bool:
    ok = True
    if not VENDOR_SDK.is_dir():
        _fail(f"SDK not cloned: {VENDOR_SDK}")
        print("        cd vendor && git clone https://github.com/unitreerobotics/unitree_sdk2_python.git")
        return False
    _ok(f"vendor SDK: {VENDOR_SDK}")
    for rel in GO2_EXAMPLE_PATHS:
        path = VENDOR_SDK / rel
        if path.is_file():
            _ok(rel)
        else:
            _fail(f"missing: {rel}")
            ok = False
    return ok


def check_go2_imports() -> bool:
    ok = True
    try:
        import cyclonedds  # noqa: F401

        _ok(f"cyclonedds {getattr(cyclonedds, '__version__', '?')}")
    except ImportError as e:
        _fail(f"cyclonedds: {e}")
        ok = False

    try:
        import unitree_sdk2py

        _ok(f"unitree_sdk2py ({unitree_sdk2py.__file__})")
    except ImportError as e:
        _fail(f"unitree_sdk2py: {e}")
        return False

    try:
        from unitree_sdk2py.idl.unitree_go.msg.dds_ import LowState_, SportModeState_

        _ = (LowState_, SportModeState_)
        _ok("idl.unitree_go (SportModeState_, LowState_)")
    except ImportError as e:
        _fail(f"unitree_go IDL: {e}")
        ok = False

    try:
        from unitree_sdk2py.idl.unitree_hg.msg.dds_ import LowState_ as HgLowState_

        _ = HgLowState_
        _ok("idl.unitree_hg importable (G1 only — do not use on Go2)")
    except ImportError:
        print("  WARN  unitree_hg not found (OK if SDK variant omits HG)")

    try:
        from unitree_sdk2py.go2.sport.sport_client import SportClient

        _ = SportClient
        _ok("go2.sport.SportClient")
    except ImportError as e:
        _fail(f"SportClient: {e}")
        ok = False

    return ok


def run_verify_install() -> bool:
    script = SCRIPTS_DIR / "verify_install.py"
    if not script.is_file():
        _fail(f"verify_install.py not found: {script}")
        return False
    print("\n=== scripts/verify_install.py ===")
    r = subprocess.run(
        [sys.executable, str(script)],
        cwd=REPO_ROOT,
        check=False,
    )
    return r.returncode == 0


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


def print_stack_reminder() -> None:
    print(
        """
=== Go2 Python stack (Lab 0) ===

  course/day-01/New-lab/lab-*.py
           │
           ▼
  unitree_sdk2py
    ├── core.channel      ChannelFactoryInitialize, pub/sub
    ├── go2.sport         SportClient (high-level locomotion)
    ├── go2.obstacles_avoid, video, vui, robot_state
    └── idl.unitree_go    SportModeState_, LowState_, …
           │
           ▼
  CycloneDDS 0.10.x       CYCLONEDDS_HOME

Topics (subscribe):  rt/sportmodestate, rt/lowstate
RPC (Lab 2+):        SportClient → sport service

Onboard (typical):   192.168.123.161  |  PC: 192.168.123.x/24
"""
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "interface",
        nargs="?",
        default=None,
        help="Ethernet NIC to Go2 (e.g. en6). Omit for machine-only checks.",
    )
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="Skip scripts/verify_install.py",
    )
    parser.add_argument(
        "--skip-multicast",
        action="store_true",
        help="Pass --skip-multicast to go2_connection_check.py",
    )
    args = parser.parse_args()

    print("Lab 0 — Go2 readiness")
    print(f"  repo: {REPO_ROOT}")

    failed = False

    print("\n=== Environment ===")
    failed |= not check_cyclonedds_home()
    check_cyclonedds_uri()

    print("\n=== Vendor tree ===")
    failed |= not check_vendor_tree()

    print("\n=== Go2 Python imports ===")
    failed |= not check_go2_imports()

    if not args.skip_verify:
        if not run_verify_install():
            failed = True

    print_stack_reminder()

    if failed:
        print("Summary: FAIL — fix install (./scripts/setup_unitree_sdk.sh)")
        return 1

    if args.interface is None:
        print("Summary: PASS — machine ready (no robot checks)")
        print("  Next: wire Go2, then re-run:")
        print("        python course/day-01/New-lab/lab-00/lab00_readiness.py en6")
        return 0

    code = run_go2_connection_check(args.interface, args.skip_multicast)
    if code == 0:
        print("\nLab 0 complete — proceed to Lab 1")
    elif code == 2:
        print("\nLab 0 PARTIAL — DDS OK; review CheckMode in log, then Lab 1")
    else:
        print("\nLab 0 FAIL — see docs/GO2-FIELD-GUIDE.md")
    return code


if __name__ == "__main__":
    sys.exit(main())
