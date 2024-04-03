#! python3
# -*- encoding: utf-8 -*-
'''
@File        :   variables.py
@Time        :   2023/04/13 16:16:07
@Author      :   Shiqi Duan 
@Description :   This file is used for storing some test variables
@Version     :   1.0
@Contact     :   shiqduan@qti.qualcomm.com
'''

import os

project_dir = os.getcwd()
config_dir = os.path.join(project_dir, 'config')
tests_dir  = os.path.join(project_dir, 'tests')

t32AppVersion = {
    'arm': 't32marm64'
}