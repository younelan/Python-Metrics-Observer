import sys
import os
import json
from pprint import pprint
import re
from os.path import dirname, abspath

base_folder = dirname(dirname(abspath(__file__)) )
sys.path.insert(0, base_folder)
base_folder = dirname(__file__) 
sys.path.insert(0, base_folder)


from Plugin import Plugin
import LinuxCollector as lc

class Linux(Plugin):
    def __init__(self, config):
        super().__init__(config)
        self.style = """
        <style>
        </style>
        """

    def get_menus(self):
        return {
            "network": {
                "text": "Network",
                "children": {
                    "linux": {"plugin": "linux", "page": "info", "text": "Linux"},

                }
            }
        }

    def on_long_update(self):
        sshconfig = self.config["credentials"].get("linux", {})

        ssh = lc.LinuxCollector()
        ssh.set_ssh_config(sshconfig)

        if ssh.connect():
            collection = ssh.collect()
            print ("--collecting Linux")
            print (collection)
        else:
            collection = []
            self.debug(1, f"Connection failed. Error: {ssh.get_error()}\n")

        self.store(collection, "linux.json")
        ssh.disconnect()

    def show_page(self, params):
        page = params.get("page", "linux")
        action = params.get("action", "")
        match page:
            case "linux":
                return self.show_config()
            case _:
                return self.show_config()

    def show_config(self):
        retval = ""
        hostfile = f"{self.config['paths']['data']}/linux.json"
        routerconfig = json.loads(open(hostfile).read()) if os.path.exists(hostfile) else {}
        rows = {}
        if not routerconfig:
            return "<h1>Linux</h1><p>No data found, Make sure plugin is running</p>"
        for name, section in routerconfig.get("info", {}).items():
            if section.get("success", False):
                status = '<span class="connected">up</span>' 
            else:
                status = '<span class="disconnected">down</span>'
            data_type = section.get("format", "text")
            delimeter = section.get("delimeter", ":")
            category = section.get("category", "default")
            if data_type == "single-column":
                print('---' , name,data_type,delimeter,category)
                pos = 1
                lines = section.get("data", "").split("\n")
                if lines:
                    while pos < len(lines):
                        line = lines[pos].strip()
                        if delimeter in line:
                            split_row = line.split(delimeter, 1)
                            #print ('----',name,delimeter,split_row)
                            if category not in rows:
                                rows[category]={}
                            rows[category][split_row[0]]=split_row[1]
                            #rows.setdefault(category, {})[split_row[0]] = split_row[1]
                        pos += 1
                    
                    #print(rows)
            elif data_type == "ifconfig":
                ifconfig = self.parse_ifconfig_output(section.get("data", ""))
                tabledata = """
                <table class='ifconfig-table'>\n
                """
                headerrow = list(ifconfig.values())[0]
                tabledata += "<tr>"
                for iface, info in headerrow.items():
                    tabledata += f"<th class='ifconfig-column'>{iface}</th>\n"
                tabledata += "</tr>"
                for idx, row in ifconfig.items():
                    tabledata += "<tr>"
                    tabledata += f"<td class='config-category'>{idx}</td>"
                    for iface, info in row.items():
                        tabledata += f"<td class='ifconfig-column'>{info}</td>\n"
                    tabledata += "</tr>"
                tabledata += "</table>"
                retval += f"<h1>{name}</h1>\n{tabledata}"
            elif data_type == "hide":
                pass
            else:
                lines = section.get("data", "").split("\n")
                pos = 1
                retval += f"<h1>{name} {status}</h1><pre>\n"
                while pos < len(lines)-1:
                    line = lines[pos]
                    retval += f"{line}\n"
                    pos += 1
                retval += "</pre>"

        mixedtable = "<h1>System Information </h1>\n"
        if rows:
            #pprint(rows)
            #return retval
            mixedtable += "<table class='config-table'>"
            mixedtable += "<tr><th class='config-category config-column'>Category</th><th class='config-subcategory config-column'>Subcategory</th><th class='config-column config-value'>Value</th></tr>"

            for category, entries in rows.items():
                print ('+++', category)
                for configkey, configvalue in entries.items():
                    mixedtable += "<tr>"
                    mixedtable += f"<td class='config-category config-column'>{category}</td><td class='config-subcategory config-column'>{configkey}</td><td class='config-column config-value'>{configvalue}</td>"
                    mixedtable += "</tr>"
            
            mixedtable += "</table>"
        else:
            mixedtable += "No data found, Make sure plugin is running"
        retval = mixedtable + retval
        return retval

    def parse_ifconfig_output(self, output):
        lines = output.split("\n")
        ifaces = {}
        current_iface = None
        pos = 0
        while pos < len(lines)-1:
            line = lines[pos]
            pos += 1
            if not line.strip():
                continue
            matches = re.match(r"^([^\s]+)", line)
            if matches:
                current_iface = matches.group(1)
                ifaces[current_iface] = {}
            matches = re.match(r"^\s{2}([^:]+):\s*(.*)$", line)
            if matches:
                key = matches.group(1).strip()
                value = matches.group(2).strip()
                ifaces[current_iface][key] = value
        return ifaces

