"""Go2 Ethernet / robot LAN checks for SDK labs (Day 1 New-lab)."""

from __future__ import annotations

import os
import platform
import subprocess
from pathlib import Path

ROBOT_SUBNET_PREFIX = "192.168.123."
GO2_ONBOARD_IP = "192.168.123.161"
# Examples from docs / VMs — real NIC names vary (enx…, enp…, ens…)
EXAMPLE_INTERFACES = ("enp0s31f6", "ens33", "en6")
# argparse default in READMEs; not valid on every machine
DOC_DEFAULT_INTERFACE = "enp0s31f6"


def iface_exists(iface: str) -> bool:
    if not iface or iface == "lo":
        return False
    if Path(f"/sys/class/net/{iface}").exists():
        return True
    try:
        return (
            subprocess.run(
                ["ip", "link", "show", iface],
                capture_output=True,
                timeout=5,
            ).returncode
            == 0
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def iface_robot_ip(iface: str) -> str | None:
    """Return PC IPv4 on robot subnet for iface, or None."""
    if not iface_exists(iface):
        return None
    if platform.system() == "Darwin":
        try:
            out = subprocess.check_output(["ifconfig", iface], text=True, timeout=5)
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        for line in out.splitlines():
            if "inet " not in line or ROBOT_SUBNET_PREFIX not in line:
                continue
            parts = line.strip().split()
            if "inet" in parts:
                ip = parts[parts.index("inet") + 1]
                if ip.startswith(ROBOT_SUBNET_PREFIX):
                    return ip.split("%")[0]
        return None
    try:
        out = subprocess.check_output(
            ["ip", "-br", "addr", "show", iface],
            text=True,
            timeout=5,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return None
    for part in out.split():
        if part.startswith(ROBOT_SUBNET_PREFIX):
            return part.split("/")[0].split("%")[0]
    return None


def list_robot_lan_interfaces() -> list[tuple[str, str]]:
    """All local interfaces with an IPv4 on 192.168.123.0/24."""
    found: list[tuple[str, str]] = []
    if platform.system() == "Darwin":
        try:
            out = subprocess.check_output(["ifconfig"], text=True, timeout=8)
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return found
        current: str | None = None
        for line in out.splitlines():
            if line and not line.startswith("\t") and not line.startswith(" "):
                current = line.split(":")[0]
            if current and "inet " in line and ROBOT_SUBNET_PREFIX in line:
                parts = line.strip().split()
                if "inet" in parts:
                    ip = parts[parts.index("inet") + 1]
                    if ip.startswith(ROBOT_SUBNET_PREFIX):
                        found.append((current, ip.split("%")[0]))
        return found
    try:
        out = subprocess.check_output(["ip", "-br", "addr"], text=True, timeout=8)
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return found
    for line in out.splitlines():
        parts = line.split()
        if len(parts) < 3:
            continue
        name, ip_raw = parts[0], parts[2]
        if ip_raw.startswith(ROBOT_SUBNET_PREFIX):
            found.append((name, ip_raw.split("/")[0].split("%")[0]))
    return found


def ping_go2(host: str = GO2_ONBOARD_IP, count: int = 2) -> bool:
    try:
        r = subprocess.run(
            ["ping", "-c", str(count), "-W", "2", host],
            capture_output=True,
            timeout=15,
        )
        return r.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def resolve_go2_interface(
    requested: str | None = None,
    *,
    env_var: str = "GO2_INTERFACE",
) -> tuple[str, str | None]:
    """
    Pick the NIC for ChannelFactoryInitialize.

    Priority: env GO2_INTERFACE → explicit CLI arg → sole robot-LAN iface → doc default.
    Returns (iface, optional notice printed before checks).
    """
    env = os.environ.get(env_var, "").strip()
    if env:
        return env, None

    on_lan = list_robot_lan_interfaces()

    if requested:
        req = requested.strip()
        if iface_exists(req):
            return req, None
        if len(on_lan) == 1:
            name, ip = on_lan[0]
            return (
                name,
                f"Note: {req!r} is not on this PC — using {name} ({ip}/24).\n"
                f"  export {env_var}={name}",
            )
        return req, None

    if len(on_lan) == 1:
        name, ip = on_lan[0]
        return (
            name,
            f"Note: no interface argument — using {name} ({ip}/24) on the robot LAN.\n"
            f"  export {env_var}={name}",
        )

    if len(on_lan) > 1:
        names = ", ".join(f"{n} ({ip})" for n, ip in on_lan)
        return (
            DOC_DEFAULT_INTERFACE,
            f"Note: several robot-LAN interfaces ({names}).\n"
            f"  Pass one explicitly or export {env_var}=<nic>",
        )

    return DOC_DEFAULT_INTERFACE, None


def _format_iface_suggestions(requested: str) -> str:
    on_lan = list_robot_lan_interfaces()
    lines = [
        f"  Requested: {requested!r}",
        f"  Robot subnet: {ROBOT_SUBNET_PREFIX}0/24  ·  onboard ping: {GO2_ONBOARD_IP}",
        "  Doc examples (names vary by machine): "
        + ", ".join(EXAMPLE_INTERFACES),
    ]
    if on_lan:
        lines.append("  Interfaces on robot LAN on THIS PC:")
        for name, ip in on_lan:
            mark = "  ← try this" if name != requested else "  ← you passed this name"
            lines.append(f"    {name}  {ip}/24{mark}")
    else:
        lines.append(
            f"  No interface has {ROBOT_SUBNET_PREFIX}x — set static IP on the port "
            "wired to Go2 (e.g. 192.168.123.98/24)."
        )
    return "\n".join(lines)


def validate_go2_interface(
    iface: str,
    *,
    ping_robot: bool = True,
) -> tuple[bool, str]:
    """
    Pre-flight before ChannelFactoryInitialize(iface).

    Returns (True, "") or (False, multi-line error hint).
    """
    if os.environ.get("CYCLONEDDS_URI"):
        return (
            False,
            "CYCLONEDDS_URI is set — unset before SDK labs:\n"
            "  unset CYCLONEDDS_URI\n"
            "  Then pass your real NIC name (not the robot IP 192.168.123.161).",
        )

    if not iface_exists(iface):
        return (
            False,
            f"Interface {iface!r} does not exist on this machine.\n"
            + _format_iface_suggestions(iface)
            + "\n\n  Find yours: ip -br addr  |  look for 192.168.123.x on the Go2 cable.",
        )

    ip = iface_robot_ip(iface)
    if ip is None:
        state = ""
        try:
            out = subprocess.check_output(
                ["ip", "-br", "link", "show", iface],
                text=True,
                timeout=5,
            )
            state = out.strip().split()[1] if out.strip() else "?"
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            state = "?"
        return (
            False,
            f"Interface {iface!r} exists ({state}) but has no {ROBOT_SUBNET_PREFIX}x address.\n"
            "  Set a static IP on the Ethernet port cabled to the robot, e.g.:\n"
            "    sudo ip addr add 192.168.123.98/24 dev "
            f"{iface}\n"
            + _format_iface_suggestions(iface)
            + "\n\n  Wrong interface name is a common mistake — use the NIC that shows "
            "192.168.123.x, not a doc placeholder like enp0s31f6 or ens33 unless that "
            "is actually your link.",
        )

    if ping_robot and not ping_go2():
        return (
            False,
            f"{iface} has {ip}/24 but ping {GO2_ONBOARD_IP} failed.\n"
            "  Check: robot powered, cable to THIS NIC, only one robot on .161, firewall off.\n"
            + _format_iface_suggestions(iface),
        )

    return True, ""


def prepare_go2_interface(
    requested: str | None,
    *,
    ping_robot: bool = True,
) -> tuple[str | None, int]:
    """
    Resolve NIC, print notice, validate. Use before ChannelFactoryInitialize.

    Returns (iface, 0) on success; (None, 1) on failure (errors already printed).
    """
    iface, notice = resolve_go2_interface(requested)
    if notice:
        print(notice)
    ok, hint = validate_go2_interface(iface, ping_robot=ping_robot)
    if not ok:
        print("ERROR: network / interface\n" + hint)
        return None, 1
    return iface, 0


def dds_failure_hint(iface: str) -> str:
    """Extra text when rt/sportmodestate never arrives after init."""
    on_lan = list_robot_lan_interfaces()
    alt = [n for n, _ in on_lan if n != iface]
    lines = [
        "No DDS data on this interface — often the wrong NIC name or CYCLONEDDS_URI set.",
        _format_iface_suggestions(iface),
    ]
    if alt:
        lines.append(
            f"\n  Retry with another robot-LAN interface, e.g.:\n"
            f"    python …/lab03_listen_sportmodestate.py {alt[0]}"
        )
    lines.append(
        f"\n  Or run full check:\n"
        f"    python course/day-01/New-lab/lab-00/lab00_readiness.py {iface}"
    )
    return "\n".join(lines)
