import subprocess
import json
import re
import os,sys
import xml.etree.ElementTree as ET

from os.path import dirname, abspath

base_folder = dirname(dirname(abspath(__file__)) )
sys.path.insert(0, base_folder)
from Plugin import Plugin

class Network(Plugin):
    style = """
    <style>
    </style>
    """

    def get_menus(self):
        return {
            "network": {
                "text": "Network",
                "children": {
                    'nethosts' : {"plugin": "network", "page": "hosts", "text": "Network Hosts"},
                    "router": {"plugin": "nokia2425", "page": "router", "text": "Router"}

                }
            }
        }

    def show_page(self, params):
        page = params.get('page', 'hosts')
        action = params.get('action', '')

        if page == 'hosts':
            return self.show_hosts()

    def show_hosts(self):
        hostfile = f"{self.config['paths']['data']}/hosts.json"
        with open(hostfile) as f:
            hosts = json.load(f)

        if not hosts:
            hosts = []

        fields = {
            "hostname": "Host Name",
            "ip": "IP Address",
            "mac_address": "Mac Address",
            "vendor": "Vendor"
        }

        output = f"<h2>{self.get_translation('Network Hosts')}</h2><table>"
        output += "<tr style='background-color: #ccc;font-weight:bold;padding: 5px;'>\n"
        for key, value in fields.items():
            output += f"<td style='padding-left:5px'>{self.get_translation(value)}</td>\n"
        output += "</tr>\n"

        for host in hosts['hosts']:
            output += "<tr>\n"
            for key, value in fields.items():
                output += f"<td style='padding-left:10px;'>{host[key]}</td>\n"
            output += "</tr>\n"

        output += "</table>"
        return output

    def on_update(self):
        addr = self.config.get("ping-address", "8.8.8.8")
        subnets = self.config.get("ping-subnets", False)

        if self.ping_addr(addr):
            status = {"status": "connected", "addr": addr}
        else:
            status = {"status": "disconnected", "addr": addr}

        self.data = status
        return status

    def on_long_update(self):
        subnets = self.config.get("ping-subnets", [])
        hosts = []
        hostfile = os.path.join(self.config['paths']['data'], "hosts.json")
        if subnets:
            hosts = self.map_subnets(subnets)['hosts']
        with open(hostfile, 'w') as f:
            json.dump({"hosts": hosts}, f)
        self.data['hosts'] = hosts
        return self.data
    
    def on_bad_long_update(self):
        subnets = self.config.get("ping-subnets", False)
        hosts = []

        if subnets:
            for subnet in subnets:
                hosts.extend(self.ping_subnets(subnet))
        try:
            hostfile = f"{self.config['paths']['data']}/hosts.json"
        except:
            hostfile = None
            print("-ERR: Data Folder not defined in config")
        if(hostfile):
            try:
                with open(hostfile, 'w') as f:
                    json.dump({"hosts": hosts}, f)
            except:
                print("-ERR: Could not write hosts.json")
            self.data['hosts'] = hosts
        return self.data

    def ping_status(self):
        addr = self.data.get('addr',"8.8.8.8")
        conn = self.config.get('connection-name',"Internet")
        connstate = self.get_translation("Connection State")
        output = "<h2 class='widgetheader'>" + self.get_translation("Ping Test") + "</h2>";
    
        output += "<span class='connlabel'>" + "<span class='connip'>%s</span>\n</span>: " % (conn);
        if  self.data.get('status',"") == "connected":
            output += " <span class='connected'>" + self.get_translation("Connected") + "</span> <span class='connip'>(%s)</span> " % (addr)
        else:
            output += "<span class='disconnected'>" + self.get_translation("No Response") + "</span> <span class='connip'>(%s)</span> "  % (addr)

        # output = f"<span class='connlabel'><h2>{connstate} <span class='connip'>({conn})</span></b></font></h2>"

        # output += f"{self.get_translation('Ping Test')}: "
        # if self.data.get('status',"") == "connected":
        #     output += f" <span class='connected'>{self.get_translation('Connected')}</span> <span class='connip'>({addr})</span> "
        # else:
        #     output += f"<span class='disconnected'>{self.get_translation('No Response')}</span> <span class='connip'>({addr})</span> "

        return output

    def show_widget(self, widget):
        print (widget)
        #widget = params.get('widget', 'ping_status')
        #widget=params
        if not widget:
            widget = "ping_status"
        ping_status=self.ping_status()
        #print("his %s gg" %ping_status) 
        #print  (ping_status)
        if widget.lower() == "ping_status":
            return ping_status
        else:
            return "hello"

    def ping_addr(self, addr, count=1):
        cmd = f"ping -c {count} {addr}"
        result = subprocess.run(cmd.split(), capture_output=True)

        if result.returncode == 0:
            return True
        else:
            return False

    def ping_subnets(self, net, count=1):
        hosts = []
        for i in range(1, 255):
            if self.ping_addr(f"{net}.{i}"):
                hosts.append(f"{net}.{i}")
        return hosts

    def get_nmap_hosts(self, input):
        up_hosts = []
        for line in input.split("\n"):
            if line.startswith("Status: Up"):
                match = re.search(r"\(([\w.-]+)\)$", line)
                if match:
                    up_hosts.append(match.group(1))
        return up_hosts

    def bad_map_subnets(self, nets):
        net_str = " ".join(nets)
        cmd = f"sudo nmap -sn -oX - {net_str}"
        raw_nmap = subprocess.run(cmd.split(), capture_output=True, text=True)
        nmap_output = raw_nmap.stdout
        return {"hosts": self.get_nmap_hosts(nmap_output)}
    
    def map_subnets(self,nets):
        net_str = " ".join(nets)
        cmd = f"sudo nmap -sn -oX - {net_str}"
        raw_nmap = subprocess.run(cmd.split(), capture_output=True)
        return {'hosts': parse_map(raw_nmap.stdout)}

# def parse_map(nmapOutput):
#     upHosts = []
#     xml = ET.fromstring(nmapOutput)
#     hosts = xml.findall('.//host[status/@state="up"]')
#     for host in hosts:
#         status = "up"
#         ipAddress = host.find('address[@addrtype="ipv4"]').attrib['addr']
#         hostname = host.find('hostnames/hostname').attrib.get('name', ipAddress)
#         macAddress = host.find('address[@addrtype="mac"]').attrib.get('addr', None)
#         vendor = host.find('os/osmatch').attrib.get('osclass_vendor', '')
#         upHosts.append({
#             "hostname": hostname,
#             "ip": ipAddress,
#             "mac_address": macAddress,
#             "vendor": vendor
#         })
#     return upHosts
def parse_map(nmapOutput):
    upHosts = []
    xml = ET.fromstring(nmapOutput)
    hosts = xml.findall('.//host')
    for host in hosts:
        status_elem = host.find('status')
        if status_elem is not None and status_elem.attrib.get('state') == "up":
            ipAddress = host.find('address[@addrtype="ipv4"]').attrib['addr']
            hostname_elem = host.find('hostnames/hostname')
            hostname = hostname_elem.attrib['name'] if hostname_elem is not None else ipAddress
            macAddress_elem = host.find('address[@addrtype="mac"]')
            macAddress = macAddress_elem.attrib['addr'] if macAddress_elem is not None else None
            vendor = host.find('os/osmatch').attrib['osclass_vendor'] if host.find('os/osmatch') is not None else ""
            upHosts.append({
                "hostname": hostname,
                "ip": ipAddress,
                "mac_address": macAddress,
                "vendor": vendor
            })
    return upHosts
