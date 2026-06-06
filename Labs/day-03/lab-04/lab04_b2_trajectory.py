#!/usr/bin/env python3
"""
Lab 4 — Day 2: B2 trajectory following (autonomous path with turns).

This script provides a menu to:
  0 – Display robot state (position, velocity, height, gait) once.
  1 – Run a pre‑defined trajectory: stand up, enable classic walk,
      then execute a sequence of forward, turn right, sideways move,
      turn left (using PathPoint objects and TrajectoryFollow).
  2 – Exit.

The trajectory uses the exact path points from the original example.
No low‑level joint control – uses high‑level SportClient.

Usage:
  conda activate unitree_env
  python lab04_b2_trajectory.py eth0

Safety:
  - The trajectory WILL move the robot forward, turn, and move sideways.
  - Ensure clear floor space (at least 1.5 m in front and sideways).
  - Instructor must supervise.
"""

import sys
import time
from unitree_sdk2py.core.channel import ChannelFactoryInitialize, ChannelSubscriber
from unitree_sdk2py.b2.sport.sport_client import SportClient, PathPoint
from unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_


# ---------- Helper: pad trajectory to 30 points ----------
def pad_to_30_points(points: list) -> list:
    """Pad a list of PathPoint (2..30) to exactly 30 points by repeating the last point."""
    if len(points) > 30:
        print(f"Warning: {len(points)} points provided, truncating to first 30.")
        points = points[:30]
    elif len(points) < 2:
        raise ValueError("At least 2 path points required.")
    if len(points) == 30:
        return points
    padded = points[:]
    last_pt = points[-1]
    while len(padded) < 30:
        padded.append(PathPoint(
            timeFromStart=last_pt.timeFromStart,
            x=last_pt.x, y=last_pt.y, yaw=last_pt.yaw,
            vx=0.0, vy=0.0, vyaw=0.0
        ))
    return padded


# ---------- Display state once ----------
def display_state_once():
    """Subscribe briefly, print one state, then unsubscribe."""
    print("\n--- Getting robot state (waiting for message) ---")
    state_received = False

    def callback(msg: SportModeState_):
        nonlocal state_received
        if not state_received:
            mode = msg.mode
            gait = msg.gait_type
            pos = msg.position
            vel = msg.velocity
            yaw_speed = msg.yaw_speed
            height = msg.body_height
            print(f"mode={mode} gait={gait} "
                  f"pos=({pos[0]:5.2f},{pos[1]:5.2f}) "
                  f"vel=({vel[0]:5.2f},{vel[1]:5.2f}) "
                  f"yaw={yaw_speed:5.2f} height={height:5.2f}")
            state_received = True

    sub = ChannelSubscriber("rt/sportmodestate", SportModeState_)
    sub.Init(callback, 10)
    timeout = 5
    start = time.time()
    while not state_received and (time.time() - start) < timeout:
        time.sleep(0.1)
    if not state_received:
        print("No state received. Check robot connection.")


# ---------- Run the defined trajectory ----------
def run_trajectory(sport_client):
    """Make robot walk a sequence: forward, turn right, move leftward, turn left."""
    print("\n--- Running trajectory (forward + turn + sideways + turn) ---")
    # Ensure robot is ready
    print("Standing up...")
    sport_client.RecoveryStand()
    time.sleep(3)
    sport_client.ClassicWalk(True)
    time.sleep(0.5)

    # Define path points (exactly as in the original trajectory-v3.py)
    # Remarks are added to explain each segment
    raw_points = [
        # Point 0: start at (x=0, y=0.2), facing forward (yaw=0), all velocities zero
        PathPoint(0, 0, 0.2, 0, 0, 0, 0),

        # Point 1: move forward to x=0.5 (stay at y=0.2) in 5 seconds.
        # vx = 0.25 m/s (but note: 0.5 m / 5 s = 0.1 m/s; the high vx may cause overshoot)
        PathPoint(5, 0.5, 0.2, 0, 0.25, 0, 0),   # move forward

        # Point 2: turn 90° to the right side (yaw from 0 to 1.5708 rad) in 5 seconds.
        # Positive yaw = turn left in Unitree convention, so this actually turns left.
        # To turn right, vyaw should be negative.
        PathPoint(10, 0.5, 0, 1.5708, 0, 0, 0.1),  # turn (intended as right)

        # Point 3: move leftward (negative y) from y=0 to y=0.5 in 5 seconds.
        # vy = -0.1 m/s means moving towards negative y direction.
        PathPoint(15, 0.5, 0.5, 1.5708, 0, -0.1, 0),  # move leftward

        # Point 4: turn 90° to the left side (yaw from 1.5708 back to 0) in 5 seconds.
        # vyaw negative reduces yaw, which is a right turn.
        PathPoint(20.0, 0.5, 0.5, 0.0, 0, 0, -0.1)   # turn back
    ]

    # Pad to 30 points as required by the SDK
    trajectory = pad_to_30_points(raw_points)
    print(f"Trajectory has {len(trajectory)} points (padded).")
    ret = sport_client.TrajectoryFollow(trajectory)
    if ret != 0:
        print(f"Error: TrajectoryFollow returned {ret}")
    else:
        print("Trajectory executing... waiting 20 seconds for completion.")
        time.sleep(23.0)
        print("Trajectory finished.")

    # Disable classic walk (return to normal mode)
    sport_client.ClassicWalk(False)
    print("Robot stopped. Returning to menu.")

def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <networkInterface>")
        print(f"Example: python {sys.argv[0]} eth0")
        return 1
    interface = sys.argv[1]

    # Safety banner
    print("\n" + "=" * 60)
    print("   B2 TRAJECTORY FOLLOWING (AUTONOMOUS PATH)")
    print("=" * 60)
    print("WARNING: Option 1 will move the robot forward, turn, and move sideways.")
    print("Ensure: floor clear (1.5 m front and sides), no obstacles, instructor present.\n")
    input("Press Enter to continue...")

    # Initialise DDS once (shared for all actions)
    print(f"Initialising DDS on interface: {interface}")
    ChannelFactoryInitialize(0, interface)

    # Create sport client (used for trajectory)
    sport_client = SportClient()
    sport_client.SetTimeout(10.0)
    sport_client.Init()

    # Main menu loop
    while True:
        print("\n" + "=" * 40)
        print("  B2 CONTROL MENU")
        print("=" * 40)
        print("0 - Display sport mode state (once)")
        print("1 - Run trajectory (forward + turn + sideways + turn)")
        print("2 - Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "0":
            display_state_once()
        elif choice == "1":
            run_trajectory(sport_client)
        elif choice == "2":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please enter 0, 1, or 2.")

    return 0


if __name__ == "__main__":
    sys.exit(main())