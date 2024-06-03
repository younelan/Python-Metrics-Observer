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
    config['vars'] = {
      "footerfg": "#b69bd7",
      "footerbg": "#415479",
      "pagebg": "#8598c3",
      "pagefg": "black",
      "contentbefore": "",
      "contentafter": "",
      "footer": "(c) 2024 Pytrack Metrics Observer",   
      "sitename": "Pytrack Metrics Observer",
      "pagebefore": "",
      "pageafter": "",
      "contentbefore": "",
      "contentafter": "",
      "pagestyle": "",
      "logoimg": "res/servercontrol.gif",
      "menubg": "#142C50",
      "menufg": "white",
      "title": "Pytrack Metrics Observer",
      "footerfg": "#b69bd7",
      "footerbg": "#415479",
      "styles": "",
      };

    config['paths'] = {
        'base': os.path.dirname(os.path.abspath(__file__)),
        'data': os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"),
        'plugins': os.path.join(os.path.dirname(os.path.abspath(__file__)), "plugins"),
    }
    config_file_path = os.path.join(os.path.dirname(__file__), "data", "config.json")
    styles_file_path = os.path.join(os.path.dirname(__file__), "templates", "styles.css")

    if os.path.exists(styles_file_path):
        with open(styles_file_path, 'r') as file:
           config['vars']['pagestyle']="<style>" + "".join(file.readlines()) + "</style>"

    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as file:
            json_config = json.load(file)
            for key, value in json_config.items():
                config[key] = value
    return config

