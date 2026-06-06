#!/usr/bin/env python3
"""
Lab 2 — Day 1: Interactive B2 motion menu (supervised movement).

This script provides a simple numbered menu to command basic B2 motions:
  - Stand up (BalanceStand)
  - Sit down (StandDown)
  - Emergency stop (StopMove)
  - Move forward a short distance (Move)
  - Recovery stand (RecoveryStand)
  - Move to a target position (MoveToPos) – automatically stands first

All commands are executed via the SportClient. No programming required —
just select a number from the menu.

Usage:
  conda activate unitree_env
  python lab02_b2_motion_menu.py eth0

Safety:
  - Motion is ENABLED. Ensure clear floor space (3m x 3m minimum).
  - No one stands in front of the robot while moving.
  - Keep hands away from legs.
  - Instructor must supervise all movements.
"""

import sys
import time

from unitree_sdk2py.b2.sport.sport_client import SportClient
from unitree_sdk2py.core.channel import ChannelFactoryInitialize


def main() -> int:
    # Get interface from command line (like original b2_sport_client.py)
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <networkInterface>")
        print(f"Example: python {sys.argv[0]} eth0")
        return 1
    interface = sys.argv[1]

    # Safety banner
    print("\n" + "=" * 60)
    print("   B2 MOTION MENU (SUPERVISED MOVEMENT)")
    print("=" * 60)
    print("WARNING: Robot WILL move when you select a command.")
    print("Ensure: floor clear, no obstacles, instructor present.")
    print("        Keep hands away from legs.")
    print("        Press Ctrl+C to exit menu at any time.\n")
    input("Press Enter to continue...")

    # Initialise DDS and sport client
    ChannelFactoryInitialize(0, interface)
    sport_client = SportClient()
    sport_client.SetTimeout(10.0)
    sport_client.Init()

    # Main interactive loop
    while True:
        print("\n" + "-" * 40)
        print("MENU (type the number and press Enter):")
        print("  1. Stand up (BalanceStand)")
        print("  2. Sit down (StandDown)")
        print("  3. Emergency stop (StopMove)")
        print("  4. Move forward (Move 0.5 m)")
        print("  5. Recovery stand (RecoveryStand – from damp)")
        print("  6. Move to position (MoveToPos: forward 0.5m, left 0.2m)")
        print("  7. Gait Switch")
        print("  0. Exit menu")
        choice = input("Your choice: ").strip()

        if choice == "0":
            print("Exiting menu. Robot remains in current state.")
            break
        elif choice == "1":
            print("Command: BalanceStand()")
            ret = sport_client.BalanceStand()
            print(f"Return code: {ret} (0 = success)")
        elif choice == "2":
            print("Command: StandDown()")
            ret = sport_client.StandDown()
            print(f"Return code: {ret}")
        elif choice == "3":
            print("Command: StopMove()")
            ret = sport_client.StopMove()
            print(f"Return code: {ret}")
        elif choice == "4":
            print("Command: Move(0.5, 0.0, 0.0) → forward 0.5 meters")
            ret = sport_client.Move(0.5, 0.0, 0.0)
            print(f"Return code: {ret}")
        elif choice == "5":
            print("Command: RecoveryStand()")
            ret = sport_client.RecoveryStand()
            print(f"Return code: {ret}")
        elif choice == "6":
            print("MoveToPos example: ensuring robot stands first...")
            sport_client.BalanceStand()
            time.sleep(2)
            print("Executing MoveToPos(0.5, 0.2, 0.0) → 0.5m forward, 0.2m left")
            ret = sport_client.ClassicWalk(True)
            ret = sport_client.MoveToPos(0.5, 0.2, 0.0)
            print(f"Return code: {ret} (0 = success)")
        elif choice == "7":
            print("Command: SwitchGait()")
            ret = sport_client.SwitchGait(2)
            print(f"Return code: {ret}")
        else:
            print("Invalid choice. Please enter 0–6.")
            continue

        # Brief pause after command
        time.sleep(0.5)

    return 0


if __name__ == "__main__":
    sys.exit(main())