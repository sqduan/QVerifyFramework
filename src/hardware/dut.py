#! python3
# -*- encoding: utf-8 -*-
'''
@File        :   dut.py
@Time        :   2023/04/11 10:51:18
@Author      :   Shiqi Duan 
@Description :   This file is used for...
@Version     :   1.0
@Contact     :   shiqduan@qti.qualcomm.com
'''

from apc  import APC
from ddr  import DDR
from core import Core

#----------------------------------------------------------------
# DUT class
#----------------------------------------------------------------
class DUT:
    """
    A class representing a Device Under Test (DUT).

    Attributes:
        basic       : Some basic info about the DUT.
        core (Core) : The core of the DUT.
        ddr (DDR)   : The DDR memory of the DUT.
        apc (APC)   : The APC of the DUT

    Methods:
        __init__(self, basic: Dict, core: Core, ddr: DDR, apc: TAPC):
            Initializes a new DUT object with the specified basic info
            and Core, DDR, and APC objects.
        __str__(self):
            Print DUT Info

        classmethod
        create_object_from_json(cls, config: dict):
            A class method to create a DUT object from a JSON config object.

    Usage:
        dut.create_object_from_json(config)
    """
    def __init__(self, basic, core: Core, ddr: DDR, apc: APC):
        # Init basic info
        self.name    = basic['name']
        self.type    = basic['type']
        self.project = basic['project']
        self.addr    = basic['addr']
        self.src     = basic['src']

        # Init core/ddr/apc and trace32
        self.core = core
        self.ddr  = ddr
        self.apc  = apc

    def __str__(self):
        basicInfo = f"DUT:\n"\
                    f"Basic Info:\n"\
                    f"  Name: {self.name}\n"\
                    f"  Type: {self.type}\n"\
                    f"  Project: {self.project}\n"\
                    f"  addr: {self.addr}\n"\
                    f"  src: {self.src}\n\n"
        coreInfo = f"{self.core}\n"
        ddrInfo  = f"{self.ddr}\n"
        apcInfo  = f"{self.apc}\n"
        return basicInfo + coreInfo + ddrInfo + apcInfo

    @classmethod
    def create_object_from_json(cls, config):
        try:
            # Get basic info about the DUT
            basicInfo = config['basic']

            # Create the Core object
            coreConfig = config['core']
            core = Core.create_object_from_json(coreConfig)

            # Create the DDR object
            ddrConfig = config['ddr']
            ddr = DDR.create_object_from_json(ddrConfig)

            apcConfig = config['apc']
            apc = APC.create_object_from_json(apcConfig)

            # Update the DUT object
            return cls(basicInfo, core, ddr, apc)
        except KeyError as ke:
            print(f"Wrong json config object,"\
                  f"no such key when create {cls.__name__}\n")
            return None
        except TypeError as te:
            print("Wrong type error when create {cls.__name__}\n")
            return None