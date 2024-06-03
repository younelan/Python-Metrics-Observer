
import json
import sys
from os.path import dirname,abspath
import os

base_folder = dirname(dirname(dirname(abspath(__file__)) ))
sys.path.insert(0, base_folder)
from CollectSSH import CollectSSH

class NokiaCollector(CollectSSH):
        commandgroups = {
            'prelude': {
                'enable': {'command': 'enable', 'waitfor': 'user.*#'},
                'show': {'command': 'show', 'waitfor': 'user.*#'}
            },
            'info': {
                'mem': {'command': 'mem', 'waitfor': 'user.*#', 'category': 'Memory', 'format': 'single-column'},
                'cpu': {'command': 'cpu', 'waitfor': 'user.*#', 'category': 'CPU', 'format': 'single-column'},
                'dns': {'command': 'dns', 'waitfor': 'user.*#', 'category': 'DNS', 'format': 'single-column'},
                'interface': {'command': 'network interface all', 'waitfor': 'user.*#', 'format': 'ifconfig'},
                'sysinfo': {'command': 'sysinfo', 'waitfor': 'user.*#', 'category': 'System', 'format': 'single-column'},
                'swversion': {'command': 'swversion', 'waitfor': 'user.*#'},
                'ridump': {'command': 'ridump', 'waitfor': 'user.*#', 'category': 'ridump', 'format': 'single-column'},
                'sysmon': {'command': 'sysmon', 'waitfor': 'user.*#', 'format': 'hide'},
                'route': {'command': 'route', 'waitfor': 'user.*#', 'format': 'route'},
                'lan-dhcp-config': {
                    'command': 'lan ip dhcp',
                    'waitfor': 'user.*#',
                    'category': 'dhcpd',
                    'format': 'single-column',
                    'delimiter': ' ',
                    'replacements': {
                        'option lease': 'opt_lease',
                        'opt dns': 'opt_dns',
                        'opt router': 'opt_router',
                        'start': 'dhcp_start',
                        'end': 'dhcp_end',
                        'dev_cate Camera': 'dev_cate_Camera',
                        'dev_cate Phone': 'dev_cate_Phone',
                        'dev_cate STB': 'dev_cate_STB',
                        'dev_cate Computer': 'dev_cate_Computer',
                        'lan ip': 'lan ip'
                    }
                },
                'lan-dhcp-hosts': {'command': 'lan ip hosts', 'waitfor': 'user.*#'},
                'lan-stats': {'command': 'lan stats', 'waitfor': 'user.*#'},
                'arp': {'command': 'arp', 'waitfor': 'user.*#'}
            },
            'outro': {
                'exit': {'command': 'exit', 'waitfor': '[a-z]+#'},
                'logout': {'command': 'logout'}
            }
        }

