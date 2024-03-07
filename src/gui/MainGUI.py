import tkinter as tk
from tkinter import filedialog
import os
import json

# Get the RUMI configure file folder
currentPath = os.path.dirname(__file__)
configPath     = "../../config"
configPath = os.path.join(currentPath, configPath)

rumiConfigFolder = "rumi_config"
rumiConfigPath = os.path.join(configPath, rumiConfigFolder)

# Read configuration from framework_config.json
framework_config_file = "framework_config.json"
framework_config_file = os.path.join(configPath, framework_config_file)
try:
    with open(framework_config_file, 'r') as config_file:
        config_data = json.load(config_file)
except FileNotFoundError:
    print("FileNotFound! No default config json file")
    
default_2node_rumi = config_data.get("default_2node_rumi")
default_3node_rumi = config_data.get("default_3node_rumi")

def OpenRumiConfigFolder():
    # Open folder dialog and get selected directory
    directory = filedialog.askdirectory(initialdir=rumiConfigPath)
    
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

# Create Tkinter window
root = tk.Tk()
root.title("Config File Explorer")

# Create button to open folder dialog
open_button = tk.Button(root, text="Open Folder", command=OpenRumiConfigFolder)
open_button.pack(pady=10)

# Create text box to show default_2node_rumi
default_2node_rumi_text = tk.Text(root, height=1, width=20)
default_2node_rumi_text.insert(tk.END, default_2node_rumi)
default_2node_rumi_text.pack(pady=5)

# Create text box to show default_3node_rumi
default_3node_rumi_text = tk.Text(root, height=1, width=20)
default_3node_rumi_text.insert(tk.END, default_3node_rumi)
default_3node_rumi_text.pack(pady=5)

# Create text box to show current config path
config_path_text = tk.Text(root, height=1, width=50)
config_path_text.insert(tk.END, rumiConfigPath)  # Show default path initially
config_path_text.pack(pady=5)

# Create listbox to display subfolders
listbox = tk.Listbox(root)
listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# List subfolders in the default directory and add them to the listbox
subfolders_default = [name for name in os.listdir(rumiConfigPath) if os.path.isdir(os.path.join(rumiConfigPath, name))]
for subfolder in subfolders_default:
    listbox.insert(tk.END, subfolder)


# Run the Tkinter event loop
root.mainloop()
