#! python3
# -*- encoding: utf-8 -*-
'''
@File        :   settings.py
@Time        :   2023/04/12 13:35:19
@Author      :   Shiqi Duan 
@Description :   This is a Setting class which stores the setting options in
                 verification framework
@Version     :   1.0
@Contact     :   shiqduan@qti.qualcomm.com
'''

from os import sys, path
import errno
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import json

from .variables import *

from robot.api import logger

class Settings():
    def __init__(self, arguments = None) -> None:
        self.module                 = ""
        self.compile                = False
        self.testPlatformConfigFile = ""
        self.rumiListFile           = ""
        self.suite                  = ""
        self.logdir                 = ""
        self.t32_timeout            = 300
        self.case_timeout           = 1200

        if arguments is not None:
            self.settingFile = os.path.join(config_dir, arguments.setting)
            self._parse_args()

    def _parse_args(self):
        return self.read_settings_from_file(self.settingFile)
        
    def read_settings_from_file(self, settingsFile):
        ret = 0
        try:
            with open(settingsFile) as sf:
                setting = json.load(sf)
            self.module  = setting['module']
            self.compile = setting['compile']
            self.testPlatformConfigFile = os.path.join(config_dir, setting['test_platform_config'])
            self.suite = os.path.join(tests_dir, setting['module'], setting['suite'])
            self.logdir = setting['logdir']
            self.t32_timeout = setting['t32_timeout']
            self.case_timeout = setting['case_timeout']
        except FileNotFoundError:
            ret = errno.ENOENT
            logger.error(f'Oppps, Setting file {settingsFile} not exits!', html = False)
        except (ValueError, TypeError):
            ret = errno.EINVAL
            logger.error("Decode json in setting file failed!", html = False)
        return ret