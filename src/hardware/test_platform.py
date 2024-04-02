#! python3
# -*- encoding: utf-8 -*-
'''
@File        :   test_platform.py
@Time        :   2023/04/03 11:09:07
@Author      :   Shiqi Duan 
@Description :   This is the class file used to describe the test platform, it
                 includes several subclasses describe the hardwares on the
                 platform.
@Version     :   1.0
@Contact     :   shiqduan@qti.qualcomm.com
'''

import sys
import json
import os
import errno
from os import path

from dut     import DUT
from trace32 import Trace32
from utils.subprocess_control import subprocess_start

from robot.api import logger

def create_test_platforms_from_json_file(jsonFile):
    """ Create test platforms from the json file

    Args:
        jsonFile (str): Path of the json file which describes the test platforms

    Returns:
        List: The list which holds the test platform objects
    """
    try:
        with open(jsonFile) as jf:
            testPlatformObjs = json.load(jf)

        testPlatforms = []
        for obj in testPlatformObjs['test_platforms']:
            platform = TestPlatform.create_object_from_json(obj)
            testPlatforms.append(platform)
    except FileNotFoundError:
        logger.error(os.path.basename(__file__) + \
            f': Test Platform File {jsonFile} not exists!', \
            html = False)
        testPlatforms = None
    except (ValueError, TypeError):
        logger.error(os.path.basename(__file__) + \
            f': Wrong type or value of json obj, please check!', \
            html = False)
        testPlatforms = None

    return testPlatforms

#----------------------------------------------------------------
# Test Platform Class
#----------------------------------------------------------------
class TestPlatform:
    """
    A class representing test platform, a test platform contains two parts:
    device under test (DUT) and a trace32 debugger.

    Attributes:
        name              : Name of the testplatform
        dut (DUT)         : Device under test
        trace32 (Trace32) : The Trace32 debugger connected to the DUT.
    
    Methods:
        __init__(self, dut: DUT, t32: Trace32):
            Initializes a new test platform object with specified DUT and
            Trace32 objects.
        __str__(self):
            Print info about test platform
        
        classmethod:
        create_object_from_json(cls, config: dict):
            factory method which will create test platform from json config obj
    """
    def __init__(self, name, dut: DUT, trace32: Trace32) -> None:
        self.name    = name
        self.dut     = dut
        self.trace32 = trace32
        self.APSST32Process  = None
        self.Q6T32Process    = None
        self.RISCVT32Process = None
    
    def __str__(self) -> str:
        dutInfo     = f"{self.dut}"
        trace32Info = f"{self.trace32}"
        return dutInfo + trace32Info

    def get_trace32_command(self):
        t32app   = trace32App[self.dut.core.type]
        config   = self.trace32.config
        initCmm  = self.trace32.initCmm

        corner   = self.dut.core.corner
        perfMode = self.dut.core.perfMode
        cpuFreq  = self.dut.core.freq
        pmicCfg  = self.dut.core.pmic
        pllCfg   = self.dut.core.pllCfg
        clkCfg   = self.dut.core.clkCfg

        ddrType  = self.dut.ddr.type
        ddrWidth = self.dut.ddr.width
        ddrTopa  = self.dut.ddr.topa
        ddrSize  = self.dut.ddr.size
        ddrFreq  = self.dut.ddr.freq
        ddrCfgPn = self.dut.ddr.cfgPn

        if self.dut.project == 'miami':
            command = [t32app, '-c', config, '-s', initCmm, corner, \
                        perfMode, cpuFreq, pmicCfg, ddrType, pllCfg, clkCfg, \
                        ddrWidth, ddrTopa, ddrSize, ddrFreq, ddrCfgPn]
        elif self.dut.project == 'alder':
            command = [t32app, '-c', config, '-s', initCmm, corner, \
                        perfMode, cpuFreq, pmicCfg, ddrType, pllCfg, clkCfg, \
                        ddrFreq]
        return list(map(str, command))

    def create_trace32_process(self):
        ret = 0
        if not self.t32Process is None:
            logger.error(os.path.basename(__file__) + \
                f': The trace32 process of {self.name} has been started!', \
                html = False)
            ret = -errno.EEXIST
        else:
            # First organize the trace32 process command
            timeLimit = 2
            command = self.get_trace32_command()

            # Then start the trace32 process command
            [self.t32Process, outs, errs] = subprocess_start(command, timeLimit)
            if self.t32Process is None:
                logger.error(os.path.basename(__file__) + \
                    f': Wrong type or value of json obj, please check!', \
                    html = False)
                ret = -errno.EAGAIN

        return ret
    
    def create_APSS_T32_process(T32App, configFile, initCMM):
        """ Directly startup APSS T32 process based on the config file and init CMM

        Args:
            T32APP (str): Path of the APSS T32
            configFile (str): Path of the Trace32 config file
            initCMM(str): Path of the init cmm script

        Returns:
            Start success or not
        """
        

    def kill_trace32_process(self, coreType):
        ret = 0
        
        if self.t32Process is None:
            logger.error(os.path.basename(__file__) + \
                f': The trace32 process has already been closed!', \
                html = False)
            ret = -errno.EALREADY
        else:
            self.t32Process.kill()
        return ret

    @classmethod
    def create_object_from_json(cls, config):
        try:
            name = config['name']

            # Create the DUT object
            dutConfig = config['dut']
            dut = DUT.create_object_from_json(dutConfig)

            trace32Config = config['trace32']
            trace32 = Trace32.create_object_from_json(trace32Config)        

            return TestPlatform(name, dut, trace32)           
        except KeyError as ke:
            print(f"Wrong json config object,"\
                  f"no such key when create {cls.__name__}\n")
            return None
        except TypeError as te:
            print(f"Wrong type error when create {cls.__name__}\n")
            return None
