# initialize.py
import os
import sys

# Get the absolute path of the parent directory of the base module
current_dir = os.path.abspath(os.path.dirname(__file__))

# Add the parent directory to sys.path
#sys.path.insert(0, parent_dir)
sys.path.insert(0, current_dir)

import Plugin.Plugin
import PluginController.PluginController

