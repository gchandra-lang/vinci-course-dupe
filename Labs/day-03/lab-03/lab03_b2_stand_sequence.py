#!/usr/bin/env python3
"""
Lab 3 — Day 1: B2 advanced stand sequence (low‑level joint control).

This script provides two options:
  0 – Run the multi‑stage stand sequence using low‑level joint control.
  1 – Switch the robot to AI mode (SelectMode("ai")) and exit.
      Use this to regain remote control after a low‑level program.

Usage:
  conda activate unitree_env
  python lab03_b2_stand_sequence.py eth0

Safety:
  - The stand sequence WILL move legs significantly.
  - Ensure clear space and instructor supervision.
"""

import sys
import time

from unitree_sdk2py.core.channel import ChannelPublisher, ChannelFactoryInitialize
from unitree_sdk2py.core.channel import ChannelSubscriber
from unitree_sdk2py.idl.default import unitree_go_msg_dds__LowCmd_
from unitree_sdk2py.idl.unitree_go.msg.dds_ import LowCmd_, LowState_
from unitree_sdk2py.utils.thread import RecurrentThread
import unitree_legged_const as b2
from unitree_sdk2py.comm.motion_switcher.motion_switcher_client import MotionSwitcherClient
from unitree_sdk2py.b2.sport.sport_client import SportClient
from unitree_sdk2py.utils.crc import CRC


class StandSequence:
    """Multi‑stage stand routine using low‑level joint position commands."""
    
    def __init__(self):
        # Joint P gain (stiffness) and D gain (damping)
        self.Kp = 1000.0
        self.Kd = 10.0

        self.low_cmd = unitree_go_msg_dds__LowCmd_()
        self.low_state = None

        # Target joint angles (radians) for 12 joints
        # Stage 1: semi‑squat (hips slightly spread)
        self.targetPos_1 = [
            0.0, 1.36, -2.65,   # FR_0, FR_1, FR_2
            0.0, 1.36, -2.65,   # FL_0, FL_1, FL_2
            -0.2, 1.36, -2.65,  # RR_0, RR_1, RR_2
            0.2, 1.36, -2.65    # RL_0, RL_1, RL_2
        ]
        # Stage 2: lower crouch (body down)
        self.targetPos_2 = [
            0.0, 0.67, -1.3,
            0.0, 0.67, -1.3,
            0.0, 1.0, -1.8,
            0.0, 1.0, -1.8,   
        ]
        # Stage 4: wider stance (hips further apart)
        self.targetPos_3 = [
            -0.5, 1.36, -2.65,
            0.5, 1.36, -2.65,
            -0.5, 1.36, -2.65,
            0.5, 1.36, -2.65
        ]

        self.startPos = [0.0] * 12
        # Durations (number of control cycles at 500 Hz)
        self.duration_1 = 500   # ~1.0 second
        self.duration_2 = 900   # ~1.8 seconds
        self.duration_3 = 1000  # ~2.0 seconds hold
        self.duration_4 = 900   # ~1.8 seconds

        self.percent_1 = 0.0
        self.percent_2 = 0.0
        self.percent_3 = 0.0
        self.percent_4 = 0.0

        self.firstRun = True
        self.lowCmdWriteThread = None
        self.crc = CRC()

    def init_low_cmd(self):
        """Initialise low‑level command structure."""
        self.low_cmd.head[0] = 0xFE
        self.low_cmd.head[1] = 0xEF
        self.low_cmd.level_flag = 0xFF
        self.low_cmd.gpio = 0
        for i in range(20):
            self.low_cmd.motor_cmd[i].mode = 0x01
            self.low_cmd.motor_cmd[i].q = b2.PosStopF
            self.low_cmd.motor_cmd[i].kp = 0
            self.low_cmd.motor_cmd[i].dq = b2.VelStopF
            self.low_cmd.motor_cmd[i].kd = 0
            self.low_cmd.motor_cmd[i].tau = 0

    def low_state_callback(self, msg: LowState_):
        self.low_state = msg

    def low_cmd_write(self):
        """Called every 2 ms (500 Hz) to send motor commands."""
        if self.firstRun and self.low_state is not None:
            for i in range(12):
                self.startPos[i] = self.low_state.motor_state[i].q
            self.firstRun = False

        # Stage 1: from start to targetPos_1
        if self.percent_1 < 1.0:
            self.percent_1 += 1.0 / self.duration_1
            self.percent_1 = min(self.percent_1, 1.0)
            for i in range(12):
                self.low_cmd.motor_cmd[i].q = (1 - self.percent_1) * self.startPos[i] + self.percent_1 * self.targetPos_1[i]
                self.low_cmd.motor_cmd[i].dq = 0
                self.low_cmd.motor_cmd[i].kp = self.Kp
                self.low_cmd.motor_cmd[i].kd = self.Kd
                self.low_cmd.motor_cmd[i].tau = 0

        # Stage 2: from targetPos_1 to targetPos_2
        elif self.percent_1 >= 1.0 and self.percent_2 < 1.0:
            self.percent_2 += 1.0 / self.duration_2
            self.percent_2 = min(self.percent_2, 1.0)
            for i in range(12):
                self.low_cmd.motor_cmd[i].q = (1 - self.percent_2) * self.targetPos_1[i] + self.percent_2 * self.targetPos_2[i]
                self.low_cmd.motor_cmd[i].dq = 0
                self.low_cmd.motor_cmd[i].kp = self.Kp
                self.low_cmd.motor_cmd[i].kd = self.Kd
                self.low_cmd.motor_cmd[i].tau = 0

        # Stage 3: hold targetPos_2
        elif self.percent_2 >= 1.0 and self.percent_3 < 1.0:
            self.percent_3 += 1.0 / self.duration_3
            self.percent_3 = min(self.percent_3, 1.0)
            for i in range(12):
                self.low_cmd.motor_cmd[i].q = self.targetPos_2[i]
                self.low_cmd.motor_cmd[i].dq = 0
                self.low_cmd.motor_cmd[i].kp = self.Kp
                self.low_cmd.motor_cmd[i].kd = self.Kd
                self.low_cmd.motor_cmd[i].tau = 0

        # Stage 4: from targetPos_2 to targetPos_3
        elif self.percent_3 >= 1.0 and self.percent_4 < 1.0:
            self.percent_4 += 1.0 / self.duration_4
            self.percent_4 = min(self.percent_4, 1.0)
            for i in range(12):
                self.low_cmd.motor_cmd[i].q = (1 - self.percent_4) * self.targetPos_2[i] + self.percent_4 * self.targetPos_3[i]
                self.low_cmd.motor_cmd[i].dq = 0
                self.low_cmd.motor_cmd[i].kp = self.Kp
                self.low_cmd.motor_cmd[i].kd = self.Kd
                self.low_cmd.motor_cmd[i].tau = 0

        self.low_cmd.crc = self.crc.Crc(self.low_cmd)
        self.lowcmd_publisher.Write(self.low_cmd)

    def run(self, interface: str):
        """Initialise DDS, release high‑level modes, and start the sequence."""
        print("Initialising DDS...")
        ChannelFactoryInitialize(0, interface)

        # Publishers & subscribers
        self.lowcmd_publisher = ChannelPublisher("rt/lowcmd", LowCmd_)
        self.lowcmd_publisher.Init()
        self.lowstate_subscriber = ChannelSubscriber("rt/lowstate", LowState_)
        self.lowstate_subscriber.Init(self.low_state_callback, 10)

        # Release any active high‑level motion mode (e.g., BalanceStand)
        print("Releasing high‑level motion modes...")
        sc = SportClient()
        sc.SetTimeout(5.0)
        sc.Init()
        msc = MotionSwitcherClient()
        msc.SetTimeout(5.0)
        msc.Init()
        status, result = msc.CheckMode()
        while result.get('name'):
            sc.StandDown()
            msc.ReleaseMode()
            time.sleep(1)
            status, result = msc.CheckMode()
            print("release")

        self.init_low_cmd()
        self.lowCmdWriteThread = RecurrentThread(interval=0.002, target=self.low_cmd_write)
        self.lowCmdWriteThread.Start()

        print("Stand sequence started – watch the robot move.")
        while True:
            if self.percent_4 >= 1.0:
                time.sleep(1)
                print("Sequence completed. Robot is in final stance.")
                break
            time.sleep(1)


def switch_to_ai_mode(interface: str) -> None:
    """Initialise DDS and switch the robot to AI mode (remote control ready)."""
    print("Initialising DDS...")
    ChannelFactoryInitialize(0, interface)
    msc = MotionSwitcherClient()
    msc.SetTimeout(5.0)
    msc.Init()
    print("Switching to AI mode...")
    code, _ = msc.SelectMode("ai")
    if code == 0:
        print("Success. The robot should now respond to the remote controller.")
    else:
        print(f"Failed to switch mode. Return code: {code}")


def main() -> int:
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <networkInterface>")
        print(f"Example: python {sys.argv[0]} eth0")
        return 1
    interface = sys.argv[1]

    # Safety banner
    print("\n" + "=" * 60)
    print("   B2 CONTROL MODE SELECTOR")
    print("=" * 60)
    print("WARNING: Option 0 will move the robot significantly.")
    print("Ensure: floor clear, no obstacles, instructor present.\n")

    # Menu
    print("Choose an action:")
    print("  0 – Run LOW‑LEVEL stand sequence (robot will move)")
    print("  1 – Switch to AI mode (regain remote control) and exit")
    print("  2 – Exit without any action")
    choice = input("Your choice (0, 1, or 2): ").strip()

    if choice == "0":
        print("\n" + "=" * 60)
        print("   B2 ADVANCED STAND SEQUENCE (LOW‑LEVEL CONTROL)")
        print("=" * 60)
        print("WARNING: Robot will move legs through a multi‑stage stand.")
        print("Keep hands and objects away from the robot.")
        print("Press Ctrl+C to stop the program (robot may fall).\n")
        input("Press Enter to start the stand sequence...")
        sequence = StandSequence()
        sequence.run(interface)
    elif choice == "1":
        switch_to_ai_mode(interface)
    elif choice == "2":
        print("Exiting without any action.")
        return 0
    else:
        print("Invalid choice. Exiting.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())