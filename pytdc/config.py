#!/usr/bin/env python3

import os
import json
import sys

# Add the project root directory to sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def get_config():
    config = {
        'connection-name': "The Internet",
        'ping-address': "4.4.4.4",
        'ping-subnets': {},
        'lang': 'en'
    }

    config['paths'] = {
        'base': os.path.dirname(os.path.abspath(__file__)),
        'data': os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"),
        'plugins': os.path.join(os.path.dirname(os.path.abspath(__file__)), "plugins"),
    }
    config_file_path = os.path.join(os.path.dirname(__file__), "data", "config.json")

    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as file:
            json_config = json.load(file)
            for key, value in json_config.items():
                config[key] = value
    return config

