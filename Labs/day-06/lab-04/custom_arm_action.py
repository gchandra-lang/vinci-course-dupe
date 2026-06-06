#!/usr/bin/env python3
"""
G1 custom arm action example.

Usage:
  python3 custom_arm_action.py enp0s31f6
"""

import time
import sys

from unitree_sdk2py.core.channel import ChannelPublisher, ChannelFactoryInitialize
from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize
from unitree_sdk2py.idl.default import unitree_hg_msg_dds__LowCmd_
from unitree_sdk2py.idl.default import unitree_hg_msg_dds__LowState_
from unitree_sdk2py.idl.unitree_hg.msg.dds_ import LowCmd_
from unitree_sdk2py.idl.unitree_hg.msg.dds_ import LowState_
from unitree_sdk2py.utils.crc import CRC
from unitree_sdk2py.utils.thread import RecurrentThread
from unitree_sdk2py.comm.motion_switcher.motion_switcher_client import MotionSwitcherClient

import numpy as np

kPi = 3.141592654
kPi_2 = 1.57079632

class G1JointIndex:
    # Left leg
    LeftHipPitch = 0
    LeftHipRoll = 1
    LeftHipYaw = 2
    LeftKnee = 3
    LeftAnklePitch = 4
    LeftAnkleB = 4
    LeftAnkleRoll = 5
    LeftAnkleA = 5

    # Right leg
    RightHipPitch = 6
    RightHipRoll = 7
    RightHipYaw = 8
    RightKnee = 9
    RightAnklePitch = 10
    RightAnkleB = 10
    RightAnkleRoll = 11
    RightAnkleA = 11

    WaistYaw = 12
    WaistRoll = 13        # NOTE: INVALID for g1 23dof/29dof with waist locked
    WaistA = 13           # NOTE: INVALID for g1 23dof/29dof with waist locked
    WaistPitch = 14       # NOTE: INVALID for g1 23dof/29dof with waist locked
    WaistB = 14           # NOTE: INVALID for g1 23dof/29dof with waist locked

    # Left arm
    LeftShoulderPitch = 15
    LeftShoulderRoll = 16
    LeftShoulderYaw = 17
    LeftElbow = 18
    LeftWristRoll = 19
    LeftWristPitch = 20   # NOTE: INVALID for g1 23dof
    LeftWristYaw = 21     # NOTE: INVALID for g1 23dof

    # Right arm
    RightShoulderPitch = 22
    RightShoulderRoll = 23
    RightShoulderYaw = 24
    RightElbow = 25
    RightWristRoll = 26
    RightWristPitch = 27  # NOTE: INVALID for g1 23dof
    RightWristYaw = 28    # NOTE: INVALID for g1 23dof

    kNotUsedJoint = 29 # NOTE: Weight

class Custom:
    def __init__(self):
        self.time_ = 0.0
        self.control_dt_ = 0.02  
        self.duration_ = 3.0   
        self.counter_ = 0
        self.weight = 0.
        self.weight_rate = 0.2
        self.kp = 60.
        self.kd = 1.5
        self.dq = 0.
        self.tau_ff = 0.
        self.mode_machine_ = 0
        self.low_cmd = unitree_hg_msg_dds__LowCmd_()  
        self.low_state = None 
        self.first_update_low_state = False
        self.crc = CRC()
        self.done = False

        self.target_pos = [
            0., kPi_2, 0., kPi_2, 0., 0., 0.,
            0., -kPi_2, 0., kPi_2, 0., 0., 0.,
            0, 0, 0
        ]

        self.arm_joints = [
          G1JointIndex.LeftShoulderPitch,  G1JointIndex.LeftShoulderRoll,
          G1JointIndex.LeftShoulderYaw,    G1JointIndex.LeftElbow,
          G1JointIndex.LeftWristRoll, G1JointIndex.LeftWristPitch,
          G1JointIndex.LeftWristYaw,
          G1JointIndex.RightShoulderPitch, G1JointIndex.RightShoulderRoll,
          G1JointIndex.RightShoulderYaw,   G1JointIndex.RightElbow,
          G1JointIndex.RightWristRoll, G1JointIndex.RightWristPitch,
          G1JointIndex.RightWristYaw,
          G1JointIndex.WaistYaw,
          G1JointIndex.WaistRoll,
          G1JointIndex.WaistPitch
        ]

    def Init(self):
        # create publisher #
        self.arm_sdk_publisher = ChannelPublisher("rt/arm_sdk", LowCmd_)
        self.arm_sdk_publisher.Init()

        # create subscriber # 
        self.lowstate_subscriber = ChannelSubscriber("rt/lowstate", LowState_)
        self.lowstate_subscriber.Init(self.LowStateHandler, 10)

    def Start(self):
        self.lowCmdWriteThreadPtr = RecurrentThread(
            interval=self.control_dt_, target=self.LowCmdWrite, name="control"
        )
        while self.first_update_low_state == False:
            time.sleep(1)

        if self.first_update_low_state == True:
            self.lowCmdWriteThreadPtr.Start()

    def LowStateHandler(self, msg: LowState_):
        self.low_state = msg

        if self.first_update_low_state == False:
            self.first_update_low_state = True
        
    # CUSTOM ARM ACTION
    def LowCmdWrite(self):
        self.time_ += self.control_dt_

        # Enable arm SDK control
        self.low_cmd.motor_cmd[G1JointIndex.kNotUsedJoint].q = 1.0

        # Build reference poses once
        if not hasattr(self, "_stand_q"):
            self._stand_q = {
                joint: self.low_state.motor_state[joint].q for joint in self.arm_joints
            }

            deg30 = 30.0 * kPi / 180.0
            deg60 = 60.0 * kPi / 180.0
            deg90 = 90.0 * kPi / 180.0

            # A-pose from standing: shoulder rolls +/-30 deg
            self._a_pose_q = dict(self._stand_q)
            self._a_pose_q[G1JointIndex.LeftShoulderRoll] = self._stand_q[G1JointIndex.LeftShoulderRoll] + deg30
            self._a_pose_q[G1JointIndex.RightShoulderRoll] = self._stand_q[G1JointIndex.RightShoulderRoll] - deg30

            # Waist yaw left +30 deg from A-pose
            self._yaw_left_q = dict(self._a_pose_q)
            self._yaw_left_q[G1JointIndex.WaistYaw] = self._a_pose_q[G1JointIndex.WaistYaw] + deg30

            # Waist yaw right 60 deg relative to left target
            self._yaw_right_q = dict(self._yaw_left_q)
            self._yaw_right_q[G1JointIndex.WaistYaw] = self._yaw_left_q[G1JointIndex.WaistYaw] - deg60

        kp = 40.0
        kd = 1.0

        def write_pose(pose):
            for joint in self.arm_joints:
                self.low_cmd.motor_cmd[joint].tau = 0.0
                self.low_cmd.motor_cmd[joint].q = pose[joint]
                self.low_cmd.motor_cmd[joint].dq = 0.0
                self.low_cmd.motor_cmd[joint].kp = kp
                self.low_cmd.motor_cmd[joint].kd = kd

        def blend_pose(start_pose, end_pose, r):
            for joint in self.arm_joints:
                q = (1.0 - r) * start_pose[joint] + r * end_pose[joint]
                self.low_cmd.motor_cmd[joint].tau = 0.0
                self.low_cmd.motor_cmd[joint].q = q
                self.low_cmd.motor_cmd[joint].dq = 0.0
                self.low_cmd.motor_cmd[joint].kp = kp
                self.low_cmd.motor_cmd[joint].kd = kd

        # Timeline (seconds)
        t1 = 2.0   # move to standing
        t2 = 4.0   # hold standing
        t3 = 6.0   # move to A-pose
        t4 = 10.0  # hold A-pose
        t5 = 11.0  # yaw left 30 in 1s
        t6 = 12.0  # hold 1s
        t7 = 14.0  # yaw right 60 in 2s
        t8 = 15.0  # hold 1s
        t9 = 17.0  # move back to standing
        t10 = 19.0 # hold standing
        t11 = 20.0 # release arm_sdk

        if self.time_ < t1:
            # Stage 1: current -> standing
            r = np.clip(self.time_ / (t1 - 0.0), 0.0, 1.0)
            start_pose = {joint: self.low_state.motor_state[joint].q for joint in self.arm_joints}
            blend_pose(start_pose, self._stand_q, r)

        elif self.time_ < t2:
            # Stage 2: hold standing
            write_pose(self._stand_q)

        elif self.time_ < t3:
            # Stage 3: standing -> A-pose
            r = np.clip((self.time_ - t2) / (t3 - t2), 0.0, 1.0)
            blend_pose(self._stand_q, self._a_pose_q, r)

        elif self.time_ < t4:
            # Stage 4: hold A-pose
            write_pose(self._a_pose_q)

        elif self.time_ < t5:
            # Stage 5: waist yaw left 30 deg in 1s
            r = np.clip((self.time_ - t4) / (t5 - t4), 0.0, 1.0)
            blend_pose(self._a_pose_q, self._yaw_left_q, r)

        elif self.time_ < t6:
            # Stage 6: hold left yaw
            write_pose(self._yaw_left_q)

        elif self.time_ < t7:
            # Stage 7: waist yaw right 60 deg in 2s
            r = np.clip((self.time_ - t6) / (t7 - t6), 0.0, 1.0)
            blend_pose(self._yaw_left_q, self._yaw_right_q, r)

        elif self.time_ < t8:
            # Stage 8: hold right yaw
            write_pose(self._yaw_right_q)

        elif self.time_ < t9:
            # Stage 9: return to standing
            r = np.clip((self.time_ - t8) / (t9 - t8), 0.0, 1.0)
            blend_pose(self._yaw_right_q, self._stand_q, r)

        elif self.time_ < t10:
            # Stage 10: hold standing
            write_pose(self._stand_q)

        elif self.time_ < t11:
            # Stage 11: release arm_sdk
            r = np.clip((self.time_ - t10) / (t11 - t10), 0.0, 1.0)
            self.low_cmd.motor_cmd[G1JointIndex.kNotUsedJoint].q = 1.0 - r
            write_pose(self._stand_q)

        else:
            self.done = True

        self.low_cmd.crc = self.crc.Crc(self.low_cmd)
        self.arm_sdk_publisher.Write(self.low_cmd)

if __name__ == '__main__':

    print("WARNING: Please ensure there are no obstacles around the robot while running this example.")
    input("Press Enter to continue...")

    if len(sys.argv)>1:
        ChannelFactoryInitialize(0, sys.argv[1])
    else:
        ChannelFactoryInitialize(0)

    custom = Custom()
    custom.Init()
    custom.Start()

    while True:        
        time.sleep(1)
        if custom.done: 
           print("Done!")
           sys.exit(-1)     
