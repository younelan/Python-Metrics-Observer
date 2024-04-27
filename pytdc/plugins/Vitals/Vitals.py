import os,sys
from os.path import dirname, abspath
base_folder = dirname(dirname(abspath(__file__)) )
sys.path.insert(0, base_folder)

from Plugin import Plugin

class Vitals(Plugin):
    def get_menus(self):
        return {
            "serverstats": {
                "text": "Server Stats",
                "weight": -2,
                "children": {
                    "vitals": {"plugin": "vitals", "page": "vitals", "text": "View Server Vitals"},
                }
            }
        }

    def on_update(self):
        uptime = open("/proc/uptime").read().split()[0]
        time_seconds = float(uptime)
        if time_seconds / 3600 < 24:
            time = "{:02}:{:02}:{:02}".format(int(time_seconds / 3600), int((time_seconds / 60) % 60), time_seconds % 60)
        else:
            time = "{:d} days {:02}:{:02}:{:02}".format(int(time_seconds / (3600 * 24)), int((time_seconds / 3600) % 24), int((time_seconds / 60) % 60), time_seconds % 60)
        load = round(os.getloadavg()[0], 2)
        data = {
            "time": self.get_translation("Time"),
            "start": self.get_translation("Uptime"),
            "load": self.get_translation("Load")
        }
        status = {
            "time": date('h:i:s'),
            "start": time,
            "load": load
        }
        data.update(status)
        uptime = ", ".join([f"{self.get_translation(key)}: {value}" for key, value in data.items()])
        status["uptime"] = uptime
        self.data = status
        return status

    def get_memory(self):
        stats = {}
        mem = open("/proc/meminfo").read().split("\n")
        for line in mem:
            if ":" in line:
                key, value = line.split(":")
                stats[key.strip()] = int(value.split()[0])
        return stats

    def show_memory(self):
        stats = self.get_memory()
        vars = {
            "MemTotal": "Total Memory",
            "MemFree": "Free Memory",
            "SwapTotal": "Total Swap",
            "SwapFree": "Available Swap"
        }
        output = "<style>.memtable {padding-left: 10px}.memitem {font-weight:bold;color:darkblue}.memkey {font-weight:bold;background-color: #CCC;padding-left: 10px;padding-right:10px}.memvalue {padding-left: 5px; padding-right: 5px;text-align:right}</style>"
        output += "<table class='memtable'>"
        for key, value in vars.items():
            output += f"<tr><td class='memkey'>{self.get_translation(value)}</td>"
            val = int((stats[key] if key in stats else 0) / 1024)
            output += f"<td class='memvalue'>{val} MB</td></tr>"
        output += "</table>"
        return output

    def show_page(self, app):
        config = self.config
        uptime = self.data["uptime"]
        mem_info = self.show_memory()
        output = "<style>.widgetheader { color:darkblue}.label {font-weight: bold;color: #055;}.left {display: inline-block;width:40%;float:left;valign:top;dbackground-color: yellow;border-right: 10px solid red;padding-right:5px;}.m.right {padding-left:5px;display: inline-block;width:40%;ebackground-color: cyan;valign: top;}.connlabel {font-size: 1.5 em;color:darkblue}.connip {font-size: 0.8em}.connected {color: green}.disconnected {color: brown}</style>"
        logoimg = config["logo"]
        output += "<div class='left'>"
        output += self.controller.show_widget("network", "ping_status")
        output += "<div align=center><img align=absmiddle src='images/TowerLogo.png' width=200 height=auto></div><p>"
        output += "</div><div class='right'>"
        output += "<p>"
        output += self.controller.show_widget("mail", "postfix_status")
        vital = self.get_translation("Server Vital Signs")
        output += f"<h2 class='widgetheader'>{vital}</h2><p>{uptime}<p>"
        output += f"<p>{mem_info}<p>"
        return output
