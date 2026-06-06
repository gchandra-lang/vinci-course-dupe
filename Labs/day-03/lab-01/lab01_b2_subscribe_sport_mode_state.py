#!/usr/bin/env python3
"""
Lab 1 — Day 1: Subscribe to B2 `SportModeState` and display robot status.

This script subscribes to the `rt/sportmodestate` topic and prints key fields
(mode, gait, position, velocity, body height). No motion is generated.

Usage:
  conda activate unitree_env
  python lab01_subscribe_sport_mode_state.py eth0

Safety:
  - No motion is commanded. Keep area clear anyway.
  - Ensure robot is on a stable surface.
"""

import sys
import time

from unitree_sdk2py.core.channel import ChannelFactoryInitialize, ChannelSubscriber
from unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_


def main() -> int:
    # Get interface from command line
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <networkInterface>")
        print(f"Example: python {sys.argv[0]} eth0")
        return 1
    interface = sys.argv[1]

    # Safety reminder
    print("\n*** SAFETY: No motion is commanded. Keep area clear anyway. ***\n")
    input("Press Enter to start subscribing...")

    # Initialise DDS
    print(f"Initialising DDS on interface: {interface}")
    ChannelFactoryInitialize(0, interface)

    # Create subscriber for SportModeState
    state_received = False

    def callback(msg: SportModeState_):
        nonlocal state_received
        state_received = True
        mode = msg.mode
        gait = msg.gait_type
        pos = msg.position        # [x, y, z]
        vel = msg.velocity        # [vx, vy, vz]
        yaw_speed = msg.yaw_speed
        height = msg.body_height

        # Print one line of data
        print(f"mode={mode} gait={gait} "
              f"pos=({pos[0]:5.2f},{pos[1]:5.2f}) "
              f"vel=({vel[0]:5.2f},{vel[1]:5.2f}) "
              f"yaw={yaw_speed:5.2f} height={height:5.2f}")

    sub = ChannelSubscriber("rt/sportmodestate", SportModeState_)
    sub.Init(callback, 10)

    print("Subscribed to rt/sportmodestate. Press Ctrl+C to stop.\n")

    start_time = time.time()
    try:
        while True:
            time.sleep(0.2)
            # Warn if no data after 5 seconds
            if not state_received and (time.time() - start_time) > 5:
                print("Warning: No SportModeState message yet. Check robot connection.")
                state_received = True  # Only warn once
    except KeyboardInterrupt:
        print("\nExiting.")

    return 0


if __name__ == "__main__":
    sys.exit(main())