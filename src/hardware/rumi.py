#! python3
# -*- encoding: utf-8 -*-
'''
@File        :   rumi.py
@Time        :   2024/04/2 10:51:18
@Author      :   Shiqi Duan
@Description :   This file is for RUMI operation request, it will send
                 request to RUMI and wait until operation done
@Version     :   1.0
@Contact     :   shiqduan@qti.qualcomm.com
'''
import os
import socket
import json
import threading
from robot.api import logger

dataLength = 1024

RUMICommand = {
    "RELOAD_IMAGE": "reload\n",
    "RESET_RUMI":  "reset_rumi\n",
    "RESET_JTAG":  "reset_jtag\n",
    "QUIT_RUMI":   "quit\n"
}

def create_rumi_list_json_file(jsonFile):
    """ Create a list which contains RUMI info from the json file

    Args:
        jsonFile (str): Path of the json file which describes the RUMIs

    Returns:
        List: The list which holds the test platform objects
    """
    try:
        with open(jsonFile) as jf:
            rumiObjs = json.load(jf)

        rumiList = {}
        for obj in rumiObjs:
            rumi = RUMI.create_object_from_json(rumiObjs[obj])
            rumiList[obj] = rumi
    except FileNotFoundError:
        logger.error(os.path.basename(__file__) + \
            f': Test Platform File {jsonFile} not exists!', \
            html = False)
        rumiList = None
    except (ValueError, TypeError):
        logger.error(os.path.basename(__file__) + \
            f': Wrong type or value of json obj, please check!', \
            html = False)
        rumiList = None

    return rumiList

class RUMI:
    def __init__(self, ip = 'blr-s4b-q07558', port = 9999, timeout = 10) -> None:
        self.ip   = ip
        self.port = port
        self.addr = (self.ip, self.port)

        self.timeout = timeout
        self.thread_running = False
        
    def set_ip(self, ip):
        self.ip = ip
        self.addr = (self.ip, self.port)

    def set_port(self, port):
        self.port = port
        self.addr = (self.ip, self.port)
        
    def send_command(self, command, param = None):
        if not self.thread_running:
            self.thread_running = True
            actualCommand = RUMICommand[command]
            threading.Thread(target = self._send_command_thread,
                             args = (actualCommand, param)).start()
        else:
            logger.warn(f"A client thread is already running!", html = False)

    def _send_command_thread(self, command, param):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.settimeout(self.timeout)
                client.connect(self.addr)
                
                # Send the command
                full_command = command.encode()
                if param is not None:
                    full_command += b' ' + param.encode()  # Assuming param is a string
                client.sendall(full_command)

                response = client.recv(dataLength).decode()
        except socket.timeout:
            logger.error(f"Client request to RUMI server timeout!", html = False)
        except Exception as e:
            print("Error:", e)
        finally:
            self.thread_running = False
       
    @classmethod     
    def create_object_from_json(cls, config):
        try:
            # Get ip of the RUMI server
            ip = config['ip']
            
            # Get port of the RUMI server
            port = config['port']

            # Update the RUMI
            return cls(ip, port)
        except KeyError as ke:
            print(f"Wrong json config object,"\
                  f"no such key when create {cls.__name__}\n")
            return None
        except TypeError as te:
            print("Wrong type error when create {cls.__name__}\n")
            return None