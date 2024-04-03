#! python3
# -*- encoding: utf-8 -*-
'''
@File        :   VerificationLibrary.py
@Time        :   2023/04/12 13:22:50
@Author      :   Shiqi Duan 
@Description :   This file is used for define standard verification behaviors
                 for SoC verification in robot framework
@Version     :   1.0
@Contact     :   shiqduan@qti.qualcomm.com
'''

from os import sys, path
import errno
import time
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from hardware.rumi          import *

from robot.api import logger
from robot.api.logger import info, debug, trace, console

class VerificationLibrary:
    
    ROBOT_LIBRARY_SCOPE = 'SUITE'

    def __init__(self) -> None:
        self._settings      = None
        self._testPlatforms = []
        self._rumis         = []

    ################################################################
    # RUMI operations:
    #     -- Reload image: Reload the RUMI image
    #     -- Reset RUMI  : Do RUMI reset
    #     -- Reset JTAG  : Do JTAG reset
    #     -- Quit RUMI   : Quit the RUMI
    ################################################################
    def reload_image(self, ip: str, port: int, timeout: int):
        """Reload RUMI image of specific RUMI server

        Args:
            ip(str)      : ip of the RUMI server
            port(int)    : port of the RUMI server
            timeout(int) : timeout value for connection
        """
        ret = 0
        rumi = RUMI(ip, port, timeout)
        rumi.send_command("RELOAD_IMAGE")
        return ret
    
    def reset_rumi(self, ip: str, port: int, timeout: int):
        """Reset specific

         Args:
            ip(str)      : ip of the RUMI server
            port(int)    : port of the RUMI server
            timeout(int) : timeout value for connection
        """
        ret = 0
        rumi = RUMI(ip, port, timeout)
        rumi.send_command("RESET_RUMI")
        return ret
    
    def reset_jtag(self, ip: str, port: int, timeout: int):
        """Reset JTAG on specific RUMI

         Args:
            ip(str)      : ip of the RUMI server
            port(int)    : port of the RUMI server
            timeout(int) : timeout value for connection
        """
        ret = 0
        rumi = RUMI(ip, port, timeout)
        rumi.send_command("RESET_JTAG")
        return ret
    
    def quit_rumi(self, ip: str, port: int, timeout: int):
        """Quit RUMI

         Args:
            ip(str)      : ip of the RUMI server
            port(int)    : port of the RUMI server
            timeout(int) : timeout value for connection
        """
        ret = 0
        rumi = RUMI(ip, port, timeout)
        rumi.send_command("QUIT_RUMI")
        return ret
    
    def rumi_initialization(self, rumiConfig):
        ret = 0
        try:
            self._rumis = create_rumi_list_json_file(rumiConfig)
        except Exception as e:
            ret = -errno.EAGAIN
            logger.error("Do test initialization failed!", html = False)
        return ret

    def test_initialization(self, settings):
        """Do test setting and test platform initialization work

        Args:
            settings (string): Test setting file name

        Returns:
            0: Test initialization success
            -EAGAIN: Test initialization failed, please refer to error log
        """
        ret = 0
        try:
            self._settings.read_settings_from_file(settings)
            self._rumis = create_rumi_list_json_file(self._settings.rumiListFile)
        except Exception as e:
            ret = -errno.EAGAIN
            logger.error("Do test initialization failed!", html = False)
        return ret

    def print_test_platform(self):
        for tp in self._testPlatforms:
            logger.debug(tp.name, html = False)

    def get_test_platform_by_name(self, name: str):
        tp = None
        for obj in self._testPlatforms:
            if obj.name == name:
                tp = obj
                break
        return tp

    """
        Interfaces to control trace32

        start_trace32_process(self, name: String)
            Start trace32 process according to the name of the platform

        end_trace32_process(self, name)
            End trace32 process
    """
    def start_trace32_process(self, name: str):
        """Start a trace32 process for given test platform

        Args:
            name (str): Name of the test platform

        Raises:
            Exception: Create trace32 process has exception

        Returns:
            0: success
            -EAGAIN: Failed to create trace32 process, please try again
        """
        ret = 0
        tp = None
        tp = self.get_test_platform_by_name(name)
        if not tp is None:
            ret = tp.create_trace32_process()
        else:
            ret = errno.EINVAL
            logger.error(f"Failed to find DUT with name {name}!", html = False)

        return ret

    def kill_trace32_process(self, name):
        ret = 0
        tp = None

        tp = self.get_test_platform_by_name(name)
        if not tp is None:
            ret = tp.kill_trace32_process()
        else:
            ret = errno.EINVAL
            logger.error(f"Failed to find {name}!", html = False)

        return ret

    def check_trace32_process_status(self, name):
        # if process not exist:

        # Process exist, but have error messages

        # Process normal
        pass

    def connect_trace32(self, name):
        ret = 0
        tp = None

        tp = self.get_test_platform_by_name(name)
        if tp is None:
            ret = errno.EINVAL
            logger.error(f"Failed to find DUT with name {name}!", html = False)
        else:
            ret = tp.trace32.connect()

        return ret

    def disconnect_trace32(self, name):
        ret = 0
        tp = None

        tp = self.get_test_platform_by_name(name)
        if tp is None:
            ret = errno.EINVAL
            logger.error(f"Failed to find DUT with name {name}!", html = False)
        else:
            tp.trace32.disconnect()

        return ret

    def check_connection(self, name):
        pass

    def power_on_trace32(self, name):
        pass

    def power_off_trace32(self, name):
        pass

    def reset_trace32(self, name):
        pass

    def read_term_and_compare(self, name, keywords: list):
        ret = 0
        matchAll = False
        tp = None

        tp = self.get_test_platform_by_name(name)
        if tp is None:
            ret = errno.EINVAL
            logger.error(f"Failed to find DUT with name {name}!", html = False)
        else:
            [ret, matchAll] = tp.trace32.read_term_and_compare(keywords)

        return [ret, matchAll]

    def wait_until_not_running(self, name, timeout = 300):
        ret = 0
        tp = None

        tp = self.get_test_platform_by_name(name)
        if tp is None:
            ret = errno.EINVAL
            logger.error(f"Failed to find DUT with name {name}!", html = False)
        else:
            ret = tp.trace32.wait_until_not_running(timeout)

        return ret

    def execute_trace32_command(self, name:str, command:str):
        ret = 0
        tp = None

        tp = self.get_test_platform_by_name(name)
        if tp is None:
            ret = errno.EINVAL
            logger.error(f"Failed to find DUT with name {name}!", html = False)
        else:
            [ret, responseBuffer] = tp.trace32.execute_command(command)

        return ret

    def execute_cmm_script(self, name:str, scriptPath:str):
        ret = 0
        tp = None

        tp = self.get_test_platform_by_name(name)
        if tp is None:
            ret = errno.EINVAL
            logger.error(f"Failed to find DUT with name {name}!", html = False)
        else:
            ret = tp.trace32.execute_cmm_script(scriptPath)

        return ret
        

    def get_trace32_view_message(self, name):
        str = ""
        return str

    """
        Interfaces to control dut
    """
    def power_on_dut(self, name):
        pass

    def power_off_dut(self, name):
        pass

    def reset_dut(self, name):
        pass

    def sleep_for_seconds(self, seconds: int):
        ret = 0
        time.sleep(seconds)
        return ret

    """
        Some common interfaces for process control
        start_process(self)
            Start a process with command and timespan
    """
    @classmethod
    def start_process(command, timespan):
        process = None
        return process