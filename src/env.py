import os
import json
from enum import Enum

# Project dir
projectDir  = os.getcwd()

configPath     = "config"
configPath = os.path.join(projectDir, configPath)

# RUMI configure folder
rumiConfigFolder = "rumi_config"
rumiConfigPath = os.path.join(configPath, rumiConfigFolder)
rumiListFile = "rumi.json"
rumiListFile = os.path.join(rumiConfigPath, rumiListFile)

# Framework configure file
settingsFile = "settings.json"
settingsFile = os.path.join(configPath, settingsFile)

# Constants and enum variables
CORE = Enum('CORE', ('APSS', 'RISCV', 'Q6'))