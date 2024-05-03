import os,sys
from os.path import dirname, abspath
base_folder = dirname(dirname(abspath(__file__)) )
sys.path.insert(0, base_folder)
from datetime import datetime

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
            time = "{:02}:{:02}:{:02}".format(int(time_seconds // 3600), int((time_seconds // 60) % 60), time_seconds % 60)
        else:
            time = "{:d} days {:02}:{:02}:{:02}".format(int(time_seconds // (3600 * 24)), int((time_seconds // 3600) % 24), int((time_seconds // 60) % 60), time_seconds % 60)
        load = round(os.getloadavg()[0], 2)

        data = {
            "time": self.get_translation("Time"),
            "start": self.get_translation("Uptime"),
            "load": self.get_translation("Load")
        }
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        status = {
            "time": current_time,
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
        output = ""
        output += "<table class='memtable'>"
        for key, value in vars.items():
            output += f"<tr><td class='memkey'>{self.get_translation(value)}</td>"
            val = int((stats[key] if key in stats else 0) / 1024)
            output += f"<td class='memvalue'>{val} MB</td></tr>"
        output += "</table>"
        return output

    def show_page(self, app):
        config = self.config
        uptime = self.data.get("uptime","")
        mem_info = self.show_memory()
        output = ""
        logoimg = config.get("logo","")
        output += "<div class='widget'>";
        output += self.controller.show_widget("network", "ping_status")
        output += "</div><div class=widget>";
        output += self.controller.show_widget("mail", "postfix_status")
        vital = self.get_translation("Server Vital Signs")
        output += f"<h2 class='widgetheader'>{vital}</h2><p>{uptime}<p>"
        output += f"<p>{mem_info}<p>"
        output += "<div class='widget'><img align=absmiddle src='res/images/TowerLogo.png' width=200 height=auto></div>"
        output += "</div>"
        output += "</div>"
        return output

