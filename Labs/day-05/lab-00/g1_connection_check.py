#!/usr/bin/env python3
"""
G1 connection quickstart — run all checks we hit during bring-up (no guesswork).

Checks (in order):
  1. SDK + CYCLONEDDS_HOME
  2. PC wired IP on 192.168.123.0/24
  3. Ping locomotion + dev PC
  4. Local multicast on robot subnet (optional)
  5. DDS rt/lowstate
  6. Motion mode CheckMode (expect 'ai')
  7. Loco FSM id (must not be 1 for high-level motion)
  8. Optional: WaveHand RPC (--try-wave)

Usage:
  conda activate unitree_env
  export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
  unset CYCLONEDDS_URI
  python scripts/g1_connection_check.py
  python scripts/g1_connection_check.py --interface enp0s31f6
  python scripts/g1_connection_check.py --try-wave   # robot must be clear; FSM != 1
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import socket
import struct
import subprocess
import sys
import time


ROBOT_SUBNET_PREFIX = "192.168.123."
PING_HOSTS = ("192.168.123.161", "192.168.123.164")
MCAST_GROUP = "239.255.0.250"
MCAST_PORT = 7401


class Step:
    def __init__(self, name: str, passed: bool, detail: str, hint: str = ""):
        self.name = name
        self.passed = passed
        self.detail = detail
        self.hint = hint


def _print_step(i: int, s: Step) -> None:
    mark = "PASS" if s.passed else "FAIL"
    print(f"\n[{i}] {s.name}: {mark}")
    print(f"    {s.detail}")
    if s.hint and not s.passed:
        print(f"    → {s.hint}")
    elif s.hint and s.passed and "optional" in s.hint.lower():
        print(f"    ({s.hint})")


def _ping(host: str, count: int = 2) -> bool:
    try:
        r = subprocess.run(
            ["ping", "-c", str(count), "-W", "2", host],
            capture_output=True,
            timeout=15,
        )
        return r.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _iface_ipv4(iface: str) -> str | None:
    if platform.system() == "Darwin":
        try:
            out = subprocess.check_output(["ifconfig", iface], text=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None
        for line in out.splitlines():
            if "inet " not in line or ROBOT_SUBNET_PREFIX not in line:
                continue
            parts = line.strip().split()
            if "inet" in parts:
                ip = parts[parts.index("inet") + 1]
                if ip.startswith(ROBOT_SUBNET_PREFIX):
                    return ip
        return None
    try:
        out = subprocess.check_output(["ip", "-br", "addr", "show", iface], text=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    for part in out.split():
        if part.startswith(ROBOT_SUBNET_PREFIX):
            return part.split("/")[0]
    return None


def _multicast_loopback(bind_ip: str) -> bool:
    try:
        rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        rx.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        rx.bind(("", MCAST_PORT))
        mreq = struct.pack(
            "4s4s", socket.inet_aton(MCAST_GROUP), socket.inet_aton(bind_ip)
        )
        rx.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        rx.settimeout(2.0)
        tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        tx.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack("b", 1))
        tx.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(bind_ip))
        tx.sendto(b"ping", (MCAST_GROUP, MCAST_PORT))
        rx.recvfrom(256)
        return True
    except OSError:
        return False
    finally:
        try:
            rx.close()
            tx.close()
        except Exception:
            pass


def check_sdk_env() -> Step:
    home = os.environ.get("CYCLONEDDS_HOME", "")
    if not home:
        return Step(
            "SDK environment",
            False,
            "CYCLONEDDS_HOME is not set",
            "Run: export CYCLONEDDS_HOME=\"$HOME/cyclonedds/install\" "
            "(or ./scripts/setup_unitree_sdk.sh)",
        )
    if not os.path.isdir(home):
        return Step(
            "SDK environment",
            False,
            f"CYCLONEDDS_HOME path missing: {home}",
            "Run: ./scripts/setup_unitree_sdk.sh",
        )
    try:
        import unitree_sdk2py  # noqa: F401
    except ImportError as e:
        return Step(
            "SDK environment",
            False,
            str(e),
            "Run: ./scripts/setup_unitree_sdk.sh",
        )
    if os.environ.get("CYCLONEDDS_URI"):
        return Step(
            "SDK environment",
            True,
            f"unitree_sdk2py OK; CYCLONEDDS_HOME={home}; "
            "warning: CYCLONEDDS_URI is set — may conflict with --interface",
            "Run: unset CYCLONEDDS_URI before robot examples",
        )
    return Step(
        "SDK environment",
        True,
        f"unitree_sdk2py OK; CYCLONEDDS_HOME={home}",
    )


def check_pc_ip(iface: str) -> tuple[Step, str | None]:
    ip = _iface_ipv4(iface)
    if ip is None:
        return (
            Step(
                "PC Ethernet IP",
                False,
                f"No {ROBOT_SUBNET_PREFIX}x on interface '{iface}'",
                "Set manual IP e.g. 192.168.123.51/24 on the port wired to the robot",
            ),
            None,
        )
    return (
        Step("PC Ethernet IP", True, f"{iface} → {ip}/24"),
        ip,
    )


def check_ping() -> Step:
    lines = []
    ok = True
    for h in PING_HOSTS:
        p = _ping(h)
        lines.append(f"{h}: {'ok' if p else 'timeout'}")
        ok = ok and p
    return Step(
        "Ping robot",
        ok,
        "; ".join(lines),
        "Power robot, check cable/switch, static IP on PC",
    )


def check_multicast(bind_ip: str) -> Step:
    ok = _multicast_loopback(bind_ip)
    return Step(
        "PC multicast (local)",
        ok,
        "loopback multicast OK" if ok else "could not send/receive multicast on PC",
        "optional if robot DDS works; check firewall",
    )


def check_dds_lowstate(iface: str) -> Step:
    from unitree_sdk2py.core.channel import ChannelFactoryInitialize, ChannelSubscriber
    from unitree_sdk2py.idl.unitree_hg.msg.dds_ import LowState_

    try:
        ChannelFactoryInitialize(0, iface)
    except Exception as e:
        return Step(
            "DDS lowstate",
            False,
            f"ChannelFactoryInitialize failed: {e}",
            f"unset CYCLONEDDS_URI; use interface {iface}",
        )

    got: list[int] = []

    def handler(msg) -> None:
        got.append(int(msg.tick))

    sub = ChannelSubscriber("rt/lowstate", LowState_)
    sub.Init(handler, 10)
    deadline = time.time() + 8.0
    while time.time() < deadline and not got:
        time.sleep(0.1)

    if not got:
        return Step(
            "DDS lowstate",
            False,
            "no messages on rt/lowstate (8s)",
            "Robot on? SelectMode('ai')? tcpdump 239.255.0.1 on "
            f"{iface}? See docs/G1-FIELD-GUIDE.md",
        )
    return Step(
        "DDS lowstate",
        True,
        f"received lowstate (tick={got[0]}, …)",
    )


def check_motion_mode(iface: str) -> Step:
    from unitree_sdk2py.core.channel import ChannelFactoryInitialize
    from unitree_sdk2py.comm.motion_switcher.motion_switcher_client import (
        MotionSwitcherClient,
    )

    ChannelFactoryInitialize(0, iface)
    msc = MotionSwitcherClient()
    msc.SetTimeout(10.0)
    msc.Init()
    code, result = msc.CheckMode()
    if code != 0 or not result:
        return Step(
            "Motion mode (CheckMode)",
            False,
            f"code={code} result={result}",
            "DDS RPC issue or robot service down",
        )
    name = result.get("name", "")
    ok = name == "ai"
    return Step(
        "Motion mode (CheckMode)",
        ok,
        f"name={name!r} (full: {result})",
        "" if ok else "SelectMode('ai') from PC or stand robot; see G1 Field Guide",
    )


def check_fsm(iface: str) -> tuple[Step, int | None]:
    from unitree_sdk2py.core.channel import ChannelFactoryInitialize
    from unitree_sdk2py.g1.loco.g1_loco_client import LocoClient
    from unitree_sdk2py.g1.loco.g1_loco_api import ROBOT_API_ID_LOCO_GET_FSM_ID

    ChannelFactoryInitialize(0, iface)
    c = LocoClient()
    c.SetTimeout(10.0)
    c.Init()
    code, data = c._Call(ROBOT_API_ID_LOCO_GET_FSM_ID, "{}")
    if code != 0 or not data:
        return (
            Step("Loco FSM id", False, f"read failed code={code}", "Check DDS / sport service"),
            None,
        )
    fsm = json.loads(data).get("data")
    if fsm == 1:
        return (
            Step(
                "Loco FSM id",
                False,
                "FSM=1 (DAMP) — high-level wave/walk will not move the robot",
                "Stand robot (feet on floor) or SetFsmId(500/706); do not call Damp() before wave",
            ),
            fsm,
        )
    return (
        Step(
            "Loco FSM id",
            True,
            f"FSM={fsm} (not damp) — OK for g1_loco_client_example.py",
        ),
        fsm,
    )


def check_wave(iface: str) -> Step:
    from unitree_sdk2py.core.channel import ChannelFactoryInitialize
    from unitree_sdk2py.g1.loco.g1_loco_client import LocoClient

    ChannelFactoryInitialize(0, iface)
    c = LocoClient()
    c.SetTimeout(10.0)
    c.Init()
    code = c.SetTaskId(0)
    if code != 0:
        return Step(
            "WaveHand RPC",
            False,
            f"SetTaskId(0) returned code={code}",
            "FSM damp? debug mode? See G1 Field Guide",
        )
    return Step(
        "WaveHand RPC",
        True,
        "SetTaskId(0) code=0 — watch robot for wave (~5s)",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--interface",
        default=os.environ.get("G1_INTERFACE", "enp0s31f6"),
        help="Ethernet interface to robot (default: enp0s31f6)",
    )
    parser.add_argument(
        "--skip-multicast",
        action="store_true",
        help="Skip local PC multicast loopback test",
    )
    parser.add_argument(
        "--try-wave",
        action="store_true",
        help="Send WaveHand after checks (clear space; FSM must not be 1)",
    )
    args = parser.parse_args()
    iface = args.interface

    print("G1 connection quickstart")
    print(f"  interface: {iface}")
    print("  See docs/G1-FIELD-GUIDE.md for details")

    steps: list[Step] = []
    n = 0

    n += 1
    steps.append(check_sdk_env())
    if not steps[-1].passed:
        for i, s in enumerate(steps, start=1):
            _print_step(i, s)
        print("\nSummary: FAIL — fix SDK install first (./scripts/setup_unitree_sdk.sh)")
        return 1

    n += 1
    step_ip, bind_ip = check_pc_ip(iface)
    steps.append(step_ip)
    if not step_ip.passed:
        for i, s in enumerate(steps, start=1):
            _print_step(i, s)
        print("\nSummary: FAIL — fix PC IP on wired interface")
        return 1

    n += 1
    steps.append(check_ping())
    if not steps[-1].passed:
        for i, s in enumerate(steps, start=1):
            _print_step(i, s)
        print("\nSummary: FAIL — fix L3 before DDS")
        return 1

    if not args.skip_multicast and bind_ip:
        n += 1
        steps.append(check_multicast(bind_ip))

    n += 1
    steps.append(check_dds_lowstate(iface))
    dds_ok = steps[-1].passed

    fsm: int | None = None
    if dds_ok:
        n += 1
        steps.append(check_motion_mode(iface))
        n += 1
        fsm_step, fsm = check_fsm(iface)
        steps.append(fsm_step)
    else:
        steps.append(
            Step(
                "Motion mode / FSM",
                False,
                "skipped (DDS lowstate failed)",
                "Fix DDS first",
            )
        )

    if args.try_wave and dds_ok and fsm is not None and fsm != 1:
        n += 1
        steps.append(check_wave(iface))
        time.sleep(2)

    # Print all steps with stable numbering
    for i, s in enumerate(steps, start=1):
        _print_step(i, s)

    must_pass = {"SDK environment", "PC Ethernet IP", "Ping robot", "DDS lowstate"}
    failed = [s.name for s in steps if s.name in must_pass and not s.passed]

    print()
    if failed:
        print(f"Summary: FAIL — fix: {', '.join(failed)}")
        print("  Doc: docs/G1-FIELD-GUIDE.md")
        return 1

    fsm_step = next((s for s in steps if s.name == "Loco FSM id"), None)
    if fsm_step and not fsm_step.passed:
        if "FSM=1" in fsm_step.detail or "DAMP" in fsm_step.detail:
            print("Summary: PARTIAL — network + DDS OK, but FSM=1 (damp).")
            print("  High-level examples need FSM ≠ 1. See G1 Field Guide §7.")
        else:
            print("Summary: PARTIAL — network + DDS OK; could not read FSM / motion mode.")
            print(f"  Detail: {fsm_step.detail}")
        print(f"  Next: ./scripts/run_g1_highlevel.sh {iface} loco  (after robot is standing)")
        return 2

    motion_step = next((s for s in steps if s.name == "Motion mode (CheckMode)"), None)
    if motion_step and not motion_step.passed:
        print("Summary: PARTIAL — DDS OK; CheckMode failed (sport service?).")
        print(f"  Detail: {motion_step.detail}")
        return 2

    print("Summary: PASS — ready for high-level SDK")
    print(f"  Next: ./scripts/run_g1_highlevel.sh {iface} loco")
    print("        (try: wave hand1 — do NOT run damp first)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
