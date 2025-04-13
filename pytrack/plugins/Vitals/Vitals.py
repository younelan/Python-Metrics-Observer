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

    def get_uptime(self):
        # try:
        #     with open("/proc/uptime", "r") as f:
        #         uptime = f.readline().split()[0]
        #     uptime = int(float(uptime))
        #     days = uptime // 86400
        #     hours = (uptime % 86400) // 3600
        #     minutes = (uptime % 3600) // 60
        #     seconds = uptime % 60
        #     return f"{days}d {hours}h {minutes}m {seconds}s"
        # except Exception as e:
        #     return str(e)

        try:
            uptime = open("/proc/uptime").read().split()[0]
        except FileNotFoundError:
            uptime = 0
        time_seconds = float(uptime)
        if time_seconds / 3600 < 24:
            time = "{:02}:{:02}:{:02}".format(int(time_seconds // 3600), int((time_seconds // 60) % 60), time_seconds % 60)
        else:
            time = "{:d} days {:02}:{:02}:{:02}".format(int(time_seconds // (3600 * 24)), int((time_seconds // 3600) % 24), int((time_seconds // 60) % 60), time_seconds % 60)
        load = round(os.getloadavg()[0], 2)
        return time, load

    def on_update(self):
        data = {
            "time": self.get_translation("Time"),
            "start": self.get_translation("Uptime"),
            "load": self.get_translation("Load")
        }
        time, load = self.get_uptime()
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
        output += "</div>"
        output += "<div class='widget' style='background-color:#ccc;height:100%;padding:10px;padding-top:150px;padding-bottom:150px;'><div style='color:#00a;'>Server</div><div style='color:brown'>Metrics</div><div style='color:green'>Observer</div></div>"
        output += "</div>"
        return output

