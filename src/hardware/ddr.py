#! python3
# -*- encoding: utf-8 -*-
'''
@File        :   ddr.py
@Time        :   2023/04/11 10:48:45
@Author      :   Shiqi Duan 
@Description :   This file is used for describe ddr module on DUT
@Version     :   1.0
@Contact     :   shiqduan@qti.qualcomm.com
'''
#----------------------------------------------------------------
# DDR class
#----------------------------------------------------------------
class DDR:
    """
    A class representing the DDR memory of a DUT.

    Attributes:
        type   (int):  The type of DDR memory.
        width  (int):
        topa   (int):
        size   (int):
        freq   (int):
        cfgPn  (int):

    Methods:
        __init__(self, type: str, width: int):
            Initializes a new DDR object with the specified type and width.

    Usage:
        ddr = DDR(0xA0, 0x1, 0x0, 0x3, 5, 0x80)
    """
    def __init__(self, type = 0xA0, width = 0x1, \
                 topa = 0x0, size = 0x3, freq = 5, cfgPn = 0x80):
        self.type   = type
        self.width  = width
        self.topa   = topa
        self.size   = size
        self.freq   = freq
        self.cfgPn = cfgPn
    
    def __str__(self) -> str:
        ddrInfo = f"DDR:\n"\
                  f"  Type: {self.type}\n"\
                  f"  width: {self.width}\n"\
                  f"  topa: {self.topa}\n"\
                  f"  size: {self.size}\n"\
                  f"  topa: {self.freq}\n"\
                  f"  size: {self.cfgPn}\n"
        return ddrInfo

    @classmethod
    def create_object_from_json(cls, config):
        # Create the DDR object
        try:
            return DDR(**config)
        except KeyError as ke:
            print(f"Wrong json config object,"\
                  f"no such key when create {cls.__name__}\n")
            return None
        except TypeError as te:
            print("Wrong type error when create {cls.__name__}\n")
            return None