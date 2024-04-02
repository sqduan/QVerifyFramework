#! python3
# -*- encoding: utf-8 -*-
'''
@File        :   trace32.py
@Time        :   2023/04/11 10:49:50
@Author      :   Shiqi Duan 
@Description :   This file is used for describe the Trace32 debugger connected
                 to DUT
@Version     :   1.0
@Contact     :   shiqduan@qti.qualcomm.com
'''

import ctypes
import enum
import errno
import time

from apc import APC

from robot.api import logger
from robot.api.logger import info, debug, trace, console

class PracticeInterpreterState(enum.IntEnum): 
    UNKNOWN = -1
    NOT_RUNNING = 0 
    RUNNING = 1 
    DIALOG_OPEN = 2
class MessageLineState(enum.IntEnum): 
    ERROR = 2
    ERROR_INFO = 16

t32api = ctypes.cdll.LoadLibrary("src/hardware/t32api64.dll")

#----------------------------------------------------------------
# Trace32 class
#----------------------------------------------------------------
class Trace32:
    """
    A class representing the Trace32 debugger of a DUT.

    Attributes:
        apc     (APC): The APC UPS of the Trace32.
        ip      (str): The IP address of the Trace32.
        port    (int): The port number of the Trace32.

    Methods:
        __init__(self, apc: str, ip: str, port: int):
            Initializes a new Trace32 object with the specified APC,
            IP address, and port number.

    Usage:
        trace32 = Trace32(apc, '192.168.0.1', 20000)
    """
    def __init__(self, apc, ip, port, config, initCmm):
        self.apc = apc
        self.ip = ip
        self.port = port
        self.config = config
        self.initCmm = initCmm

    def __str__(self) -> str:
        trace32Info = f"Trace32:\n"\
                      f"  ip: {self.ip}\n"\
                      f"  port: {self.port}\n"\
                      f"  apc: {self.apc}\n"
        
        return trace32Info

    def connect(self):
        T32_DEV = 1
        ret = 0
        port = "%d" % (self.port)
        t32api.T32_Config(b"NODE=", b"localhost")
        t32api.T32_Config(b"PORT=", port.encode())
        t32api.T32_Config(b"PACKLEN=", b"1024")

        # Establish a connection to TRACE32
        rc = t32api.T32_Init()
        if rc != 0:
            logger.error(f"Init t32 failed!", html = False)
            return rc

        # Sometimes the first attempt to Attach fails but a second will
        # usually succeed. This often happens if the API has been left hanging
        # when the previous user didn't call T32_Exit() before quitting.
        for x in range(3):
            rc = t32api.T32_Attach(T32_DEV)
            if rc == 0:
                break
        if rc != 0:
            logger.error(f"Attach t32 failed!", html = False)
            t32api.T32_Exit()
        return rc

    def disconnect(self):
        t32api.T32_Exit()

    def ping(self):
        rc = t32api.T32_Ping()
        if rc != 0:
            logger.error(f"Ping t32 failed!", html = False)
        return rc

    def read_term_and_compare(self, keywords: set):
        """Read the TERM view, then check whether contains keywords,
           this command will store the TERM view contents to debug file
           and clear the view!

        Args:
            keywords (set): keywords string set which will be compared with
                             the TERM view contents
        """
        buffer = (ctypes.c_char * 4096)()
        matchAll = False
        rc = 0

        if not keywords:
            rc = -errno.EINVAL
            logger.error(f"Empty keywords lists!", html = False)
            return [rc, matchAll]

        rc = self.connect()
        if rc != 0:
            return [rc, matchAll]

        # Transfer keywords list to sets
        keywordsSet = set(keywords)

        # Now read the hardcopy of the TERM VIEW window of trace32
        command = b"TERM.HARDCOPY"
        buffer = (ctypes.c_char * 4096)()
        offset = ctypes.c_uint32(0)
        code = "T32_PRINT_CODE_ASCII"
        mess_len = ctypes.c_uint(0)

        lastContent = ""   
 
        mess_len.value = t32api.T32_GetWindowContent(command, ctypes.byref(buffer), 1024, offset.value, code)
        while mess_len.value > 0:
            # Get the buffer from the TERM view, now you can do some compare works
            content = ""
            for i in range (0, mess_len.value):
                content = content + buffer[i].decode("utf-8")

            currentContent = lastContent + content
            lastContent = content

            # Do compare work, remove the keyword in set if found
            for keyword in keywordsSet.copy():
                if keyword in currentContent:
                    keywordsSet.remove(keyword)

            offset.value = offset.value + mess_len.value
            mess_len.value = t32api.T32_GetWindowContent(command, ctypes.byref(buffer), 1024, offset.value, code)

        # Check if all the keywords have been found
        if not keywordsSet:
            matchAll = True

        self.disconnect()
        return [rc, matchAll]

    def wait_until_not_running(self, timeout = 300):
        """Wait until the trace32 is not running

        Args:
            timeout (int): Timeout for waiting trace32 break
        Returns:
            0:  Successful
            <0: Timeout 
        """
        rc = self.connect()
        if rc != 0:
            return rc

        start = time.time()

        # Wait until the break point hit
        pstate = ctypes.c_uint16(-1)
        while rc == 0 and not pstate.value == 2:
            rc = t32api.T32_GetState(ctypes.byref(pstate))
            if time.time() - start >= timeout:
                logger.error(f"Wait timeout!", html = False)
                self.disconnect()
                return -errno.ETIMEDOUT
            
            time.sleep(300/1000)
            rc = t32api.T32_GetState(ctypes.byref(pstate))

        self.disconnect()
        return 0

    #----------------------------------------------------------------
    # Below are some key functions for executing trace32 command & cmm
    #----------------------------------------------------------------
    def execute_command(self, command: str, args: list = [], bufferSize = 1024):
        """Execute a trace32 command

        Args:
            command (str): Command which will be executed
            args (list): Args are lists contains the arguments
            bufferSize (int): The size of response buffer

        Returns:
            0:  Command executed successfully
            <0: Failed to execut command
        """

        # To execute a command, we need to first connect to a trace32, then
        # execute specific command, after command finish, we need to disconnect
        rc = self.connect()
        if rc != 0:
            return rc

        # Organize the command
        for arg in args:
            command = command + ' ' + str(arg)

        # Execute the command and wait for 
        t32api.T32_Cmd(command)
        responseBuffer = ctypes.create_string_buffer(bufferSize)
        rc = t32api.T32_Cmd(command.encode(), responseBuffer, bufferSize)
        if rc != 0:
            logger.error(f"Command {command} execute error!", html = False)

        self.disconnect()

        return [rc, responseBuffer]

    def execute_cmm_script(self, scriptPath, delayTime = 500):
        """Execute cmm script and wait it to finish

        Args:
            scriptPath (str): Path to the cmm script
            delayTime  (int): Miliseconds to delay while executing cmm

        Returns:
            0: cmm script runs successfully 
        """
        rc = self.connect()
        if rc != 0:
            return rc

        # Start PRACTICE script
        t32api.T32_Cmd(b"CD.DO " + scriptPath.encode('utf-8'))

        # Wait until PRACTICE script is done
        state = ctypes.c_int(PracticeInterpreterState.UNKNOWN) 
        rc = 0
        while rc==0 and not state.value==PracticeInterpreterState.NOT_RUNNING: 
            rc = t32api.T32_GetPracticeState(ctypes.byref(state))
            time.sleep(delayTime/1000)

        # Get confirmation that everything worked 
        status = ctypes.c_uint16(-1)
        message = ctypes.create_string_buffer(256)
        rc = t32api.T32_GetMessage(ctypes.byref(message), ctypes.byref(status)) 
        if rc != 0 \
            or status.value == MessageLineState.ERROR \
            or status.value == MessageLineState.ERROR_INFO:
            rc = -errno.EAGAIN
            logger.error(f"Execute {scriptPath} error!", html = False)

        # Disconnect the trace32
        self.disconnect()
        return rc

    @classmethod
    def create_object_from_json(cls, config):
        # Create the Trace32 object
        try:
            apcConfig = config['apc']
            apc  = APC.create_object_from_json(apcConfig)
            ip   = config['ip']
            port = config['port']
            t32config = config['config']
            initCmm = config['initCmm']

            return Trace32(apc, ip, port, t32config, initCmm)
        except KeyError as ke:
            print(f"Wrong json config object,"\
                  f"no such key when create {cls.__name__}\n")
            return None
        except TypeError as te:
            print("Wrong type error when create {cls.__name__}\n")
            return None
