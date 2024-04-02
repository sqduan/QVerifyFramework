#! python3
# -*- encoding: utf-8 -*-
'''
@File        :   core.py
@Time        :   2023/04/11 10:49:27
@Author      :   Shiqi Duan 
@Description :   This file is used for...
@Version     :   1.0
@Contact     :   shiqduan@qti.qualcomm.com
'''

#----------------------------------------------------------------
# CPU core class
#----------------------------------------------------------------
class Core:
    """
    A class representing the core of a DUT.

    Attributes:
        type (str): The type of the core.
        width (int): The width of the core in bits.
        corner (str): The corner of the core.
        perfMode (str): The performance mode of the core.
        freq (float): The frequency of the core in GHz.
        pmic (str): The power management IC (PMIC) of the core.

    Methods:
        __init__(self, type: str, width: int, corner: str, perfMode: str,
                 freq: float, pmic: str):
            Initializes a new Core object with the specified core params
        __str__(self):
            Print info about core

        classmethod:
        create_object_from_json(cls, config: dict):
            A class method to create a Core object from a JSON config object.

    Usage:
        core = Core('Cortex-A78', 64, 'TT', 'high', 2.4, 'PMIC123')
        core = Core.create_object_from_json(coreConfig)
    """
    def __init__(self, type = "arm", width = 32, \
                 corner = "1.0_tt", perfMode = "norm",\
                 freq = 3, pmic = 0x0, pllCfg = 0xF, clkCfg = 0x0):
        self.type   = type
        self.width  = width
        self.corner = corner
        self.perfMode = perfMode
        self.freq   = freq
        self.pmic   = pmic
        self.pllCfg = pllCfg
        self.clkCfg = clkCfg
    
    def __str__(self) -> str:
        coreInfo = f"Core Info:\n"\
                   f"  Type: {self.type}\n"\
                   f"  Width: {self.width}\n"\
                   f"  Corner: {self.corner}\n"\
                   f"  PerfMode: {self.perfMode}\n"\
                   f"  Freq: {self.freq}\n"\
                   f"  PMIC: {self.pmic}\n"\
                   f"  pllCfg: {self.pllCfg}\n"\
                   f"  clkCfg: {self.clkCfg}\n"
        return coreInfo

    @classmethod
    def create_object_from_json(cls, config):
        # Create the Core object
        try:
            return Core(**config)
        except KeyError as ke:
            print(f"Wrong json config object,"\
                  f"no such key when create {cls.__name__}\n")
            return None
        except TypeError as te:
            print("Wrong type error when create {cls.__name__}\n")
            return None