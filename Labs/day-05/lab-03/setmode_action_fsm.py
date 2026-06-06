#!/usr/bin/env python3
"""
G1 locomotion examples, get and set FSM ID to switch modes.

Usage:
  python3 loco_fsm_modes.py enp0s31f6
"""

import time
import sys
from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize
from unitree_sdk2py.idl.default import unitree_go_msg_dds__SportModeState_
from unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_
from unitree_sdk2py.g1.loco.g1_loco_client import LocoClient
import math
from dataclasses import dataclass

@dataclass
class TestOption:
    name: str
    id: int

option_list = [
    TestOption(name="Set mode: Zero Torque (CAUTION: robot relaxes all joints / falls instantly.)", id=0),
    TestOption(name="Set mode: Damping", id=1),
    TestOption(name="Test action: shake hand", id=2),
    TestOption(name="Get FSM ID", id=3),
    TestOption(name="Set FSM ID", id=4),
]

class UserInterface:
    def __init__(self):
        self.test_option_ = None

    def convert_to_int(self, input_str):
        try:
            return int(input_str)
        except ValueError:
            return None

    def terminal_handle(self):
        input_str = input("Enter id or name: \n")

        if input_str == "list":
            self.test_option_.name = None
            self.test_option_.id = None
            for option in option_list:
                print(f"{option.name}, id: {option.id}")
            return

        for option in option_list:
            if input_str == option.name or self.convert_to_int(input_str) == option.id:
                self.test_option_.name = option.name
                self.test_option_.id = option.id
                print(f"Test: {self.test_option_.name}, test_id: {self.test_option_.id}")
                return

        print("No matching test option found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} networkInterface")
        sys.exit(-1)

    print("WARNING: Please ensure there are no obstacles around the robot while running this example.")
    input("Press Enter to continue...")

    ChannelFactoryInitialize(0, sys.argv[1])

    test_option = TestOption(name=None, id=None) 
    user_interface = UserInterface()
    user_interface.test_option_ = test_option

    sport_client = LocoClient()  
    sport_client.SetTimeout(10.0)
    sport_client.Init()

    print("Input \"list\" to list all test option ...")
    while True:
        user_interface.terminal_handle()

        print(f"Updated Test Option: Name = {test_option.name}, ID = {test_option.id}")

        if test_option.id == 0:
            sport_client.ZeroTorque()
        elif test_option.id == 1:
            sport_client.Damp()
        elif test_option.id == 2:
            sport_client.ShakeHand()
        elif test_option.id == 3:
            id = sport_client.GetFsmId()
            print("GetFsmId:", id)
        elif test_option.id == 4:
            print("0 = Zero Torque (CAUTION: robot relaxes all joints / falls instantly.)")
            print("1 = Damping")
            print("4 = Preparation")
            print("802 = Run")
            user_input = input("Enter FSM ID: ")
            id = int(user_input)
            sport_client.SetFsmId(id)

        time.sleep(1)
