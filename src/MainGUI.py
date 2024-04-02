import os
import sys
import json
from functools import partial

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from robot.api import logger

################################################################
# APP initialization, environment paths read and configuration
# file import
################################################################
sys.path.insert(1, 'src/hardware')
import env
import rumi
import test_platform

# Get RUMI info from rumi config json
rumis = rumi.create_rumi_list_json_file(env.rumiListFile)

# Read configuration from framework_config.json
try:
    with open(env.frameworkConfigFile, 'r') as config_file:
        config_data = json.load(config_file)
except FileNotFoundError:
    print("FileNotFound! No default config json file")
    
default2NodeRumi = config_data.get("default_2node_rumi")
default3NodeRumi = config_data.get("default_3node_rumi")
currentRumi = default2NodeRumi    # Record current rumi

def OpenRumiConfigFolder():
    # Open folder dialog and get selected directory
    directory = filedialog.askdirectory(initialdir=env.rumiConfigPath)
    
    if directory:
        # Clear existing listbox items
        listbox.delete(0, tk.END)
        
        # List subfolders in the selected directory
        subfolders = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
        
        print(subfolders)
        
        # Add subfolder names to the listbox
        for subfolder in subfolders:
            listbox.insert(tk.END, subfolder)
        
        # Display current config path in the text box
        config_path_text.delete(1.0, tk.END)  # Clear previous text
        config_path_text.insert(tk.END, directory)
        
def UpdateRumiConfig(text_widget):
    # Get selected item from listbox
    selected_item = listbox.curselection()
    if selected_item:
        # Get folder name from listbox
        folder_name = listbox.get(selected_item)

        # Update text widget with selected folder name
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, folder_name)
        currentRumi = str(text_widget.get("1.0", "end"))

        # Updating current RUMI configure files

def SelectRUMIType():
    selected_rumi = rumi_type_select.get()
    if selected_rumi == "2node":
        currentRumi = str(twoNodeRumi_text.get("1.0", "end"))
        twoNodeRumi_text.config(state=tk.NORMAL)
        threeNodeRumi_text.config(state=tk.DISABLED)
    elif selected_rumi == "3node":
        currentRumi = str(threeNodeRumi_text.get("1.0", "end"))
        twoNodeRumi_text.config(state=tk.DISABLED)
        threeNodeRumi_text.config(state=tk.NORMAL)
        
def StartupT32(coreType = env.CORE.APSS):
    if coreType == env.CORE.APSS:
        # Start up APSS T32
        test_platform.create_APSS_T32_process(1)
        
    elif coreType == env.CORE.RISCV:
        print("Hello: RISCV")
    elif coreType == env.CORE.Q6:
        print("Hello: Q6")

def SendRUMICommand(rumi, command, param = None):
    if not rumis:
        logger.error(f"RUMI list is empty!", html = False)
        return -1

    rumis[rumi].send_command(command, param)
    
    return 0

################################################################
# APP GUI construction, weiget create
################################################################
# Create APP window
root = tk.Tk()
root.title("Config File Explorer")
root.geometry("640x480")

# Create button to open folder dialog
RUMI_config_folder_choose_button = tk.Button(root, text="Select RUMI config",
                                             command=OpenRumiConfigFolder)

# Create select bar for RUMI selection
rumi_type_select = ttk.Combobox(root, values=["2node", "3node"])
rumi_type_select.set("2node")  # Set default value to "2node"
rumi_type_select.bind("<<ComboboxSelected>>", lambda event: SelectRUMIType())

# Create text box to show default 2node RUMI
twoNodeRumi_text = tk.Text(root, height=1, width=20)
twoNodeRumi_text.insert(tk.END, default2NodeRumi)

# Create button to update env.twoNodeRumi_text
update_button_2node = tk.Button(root, text="Update 2node", command=lambda: UpdateRumiConfig(twoNodeRumi_text))

# Create text box to show env.default3NodeRumi
threeNodeRumi_text = tk.Text(root, height=1, width=20)
threeNodeRumi_text.insert(tk.END, default3NodeRumi)

# Create button to update env.threeNodeRumi_text
update_button_3node = tk.Button(root, text="Update 3node", command=lambda: UpdateRumiConfig(threeNodeRumi_text))

# Create text box to show current config path
config_path_text = tk.Text(root, height=1, width=50)
config_path_text.insert(tk.END, env.rumiConfigPath)  # Show default path initially

# Create listbox to display subfolders
listbox = tk.Listbox(root)

# List subfolders in the default directory and add them to the listbox
subfolders_default = [name for name in os.listdir(env.rumiConfigPath) if os.path.isdir(os.path.join(env.rumiConfigPath, name))]
for subfolder in subfolders_default:
    listbox.insert(tk.END, subfolder)
    
start_apss_button = tk.Button(root, text="APSS T32 Start",
    command = partial(StartupT32, env.CORE.APSS))
start_riscv_button = tk.Button(root, text="TMEL T32 Start",
    command = partial(StartupT32, env.CORE.RISCV))
start_q6_button = tk.Button(root, text="Q6 T32 Start",
    command = partial(StartupT32, env.CORE.Q6))

flush_image_button = tk.Button(root, text="Flush RUMI Image",
    command = partial(SendRUMICommand, currentRumi, "FLUSH_IMAGE"))
rumi_reset_button = tk.Button(root, text="Reset RUMI",
    command = partial(SendRUMICommand, currentRumi, "RESET_RUMI"))
jtag_reset_button = tk.Button(root, text="Reset JTAG",
    command = partial(SendRUMICommand, currentRumi, "RESET_JTAG"))
rumi_quit_button = tk.Button(root, text="Quit RUMI",
    command = partial(SendRUMICommand, currentRumi, "RUMI_QUIT"))

################################################################
# APP GUI construction, weiget placement
################################################################
config_path_text.grid(row = 1, column = 2, sticky = tk.S + tk.N
    + tk.W)
RUMI_config_folder_choose_button.grid(row = 1, column = 0, sticky = tk.S + tk.N
    + tk.W)
rumi_type_select.grid(row = 2, column = 0, pady = 10)
twoNodeRumi_text.grid(row = 3, column = 0, pady = 10)
update_button_2node.place(in_=twoNodeRumi_text, relx=1.0, x=20, rely=0, y=0)

threeNodeRumi_text.grid(row = 4, column = 0, pady = 10)
update_button_3node.place(in_=threeNodeRumi_text, relx=1.0, x=20, rely=0, y=0)

listbox.grid(row = 5, column = 0, pady = 10)
start_apss_button.grid(row = 6, column = 0, pady = 10)
start_riscv_button.grid(row = 6, column = 1, pady = 10)
start_q6_button.grid(row = 6, column = 2, pady = 10)

flush_image_button.grid(row = 7, column = 1, pady = 10)
rumi_reset_button.grid(row = 7, column = 2, pady = 10)
jtag_reset_button.grid(row = 8, column = 1, pady = 10)
rumi_quit_button.grid(row = 8, column = 2, pady = 10)

# Run the Tkinter event loop
root.mainloop()
