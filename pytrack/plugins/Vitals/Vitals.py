import os,sys
from os.path import dirname, abspath
base_folder = dirname(dirname(abspath(__file__)) )
sys.path.insert(0, base_folder)
from datetime import datetime
import platform
import subprocess
import psutil
import time

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
        """
        Gets the system uptime using the psutil library.
        Returns a tuple containing the formatted uptime string and the 1-minute load average.
        """
        try:
            boot_time_timestamp = psutil.boot_time()
            boot_time = datetime.datetime.fromtimestamp(boot_time_timestamp)
            now = datetime.datetime.now()
            uptime_seconds = int((now - boot_time).total_seconds())

            if uptime_seconds / 3600 < 24:
                time = "{:02}:{:02}:{:02}".format(int(uptime_seconds // 3600), int((uptime_seconds // 60) % 60), int(uptime_seconds % 60))
            else:
                time = "{:d} days {:02}:{:02}:{:02}".format(int(uptime_seconds // (3600 * 24)), int((uptime_seconds // 3600) % 24), int((uptime_seconds // 60) % 60), int(uptime_seconds % 60))

            load = round(psutil.getloadavg()[0], 2)  # psutil also provides load averages
            return time, load
        except Exception as e:
            print(f"Error getting uptime using psutil: {e}")
            return "N/A", "N/A"
    
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
        """
        Gets the system memory information using the psutil library.
        Returns a dictionary containing memory statistics.
        """
        try:
            virtual_memory = psutil.virtual_memory()
            swap_memory = psutil.swap_memory()
            stats = {
                "MemTotal": virtual_memory.total,
                "MemFree": virtual_memory.available,
                "MemUsed": virtual_memory.used,
                "MemPercent": virtual_memory.percent,
                "SwapTotal": swap_memory.total,
                "SwapFree": swap_memory.free,
                "SwapUsed": swap_memory.used,
                "SwapPercent": swap_memory.percent,
            }
            print(stats)
            return stats
        except Exception as e:
            print(f"Error getting memory info using psutil: {e}")
            return {}
    
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

