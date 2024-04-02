#! python3
# -*- encoding: utf-8 -*-
'''
@File        :   apc.py
@Time        :   2023/04/11 10:47:44
@Author      :   Shiqi Duan 
@Description :   This file is used for...
@Version     :   1.0
@Contact     :   shiqduan@qti.qualcomm.com
'''

from enum import Enum

class Power(Enum):
    """
    A Enum to indicate power status
    """
    OFF = 0
    ON  = 1

#----------------------------------------------------------------
# APC class
#----------------------------------------------------------------
class APC:
    """
    A class representing the APC UPS.

    Attributes:
        ip (str): IP address of APC.
        port (int): The port of the APC.

    Methods:
        __init__(self, ip: str, port: int):
            Initializes a new APC object with the specified ip and pprt.
        power_on(self):
            Turn on the APC
        power_off(self):
            Turn off the APC
        reset(self):
            Reset the APC (turn off then turn on)

    Usage:
        apc = APC('10.21.10.81', 5)
    """
    def __init__(self, ip = "0.0.0.0", port = 5, timeout = 300):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.status = Power.ON

    def __str__(self) -> str:
        apcInfo = f"APC:\n"\
                      f"  ip: {self.ip}\n"\
                      f"  port: {self.port}\n"
        return apcInfo

    def is_power_on(self) -> bool:
        """
        Currently we simply check the power status by a variable, it's better
        to get status through the APC command
        """
        return self.status == Power.ON

    def power_on(self):
        if self.is_power_on():
            return 0
        else:
            pass

    def power_off(self):
        if not self.is_power_on():
            return 0
        else:
            pass

    def reset(self):
        self.power_off()
        self.power_on()

    @classmethod
    def create_object_from_json(cls, config):
        # Create the DDR object
        try:
            return APC(**config)
        except KeyError as ke:
            print(f"Wrong json config object,"\
                  f"no such key when create {cls.__name__}\n")
            return None
        except TypeError as te:
            print("Wrong type error when create {cls.__name__}\n")
            return None