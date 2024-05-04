
import json
import sys
from os.path import dirname,abspath
import os

base_folder = dirname(dirname(dirname(abspath(__file__)) ))
sys.path.insert(0, base_folder)
from CollectSSH import CollectSSH

class LinuxCollector(CollectSSH):
        commandgroups = {
            'prelude': {
            },
            'info': {

    'cpu': {'command': "grep 'cpu ' /proc/stat", 'waitfor': '.*#', 'category': 'CPU', 'format': 'single-column'},
    'memory_total': {'command': "grep MemTotal /proc/meminfo", 'waitfor': '.*#', 'category': 'Memory', 'format': 'single-column'},
    'memory_free': {'command': "grep MemFree /proc/meminfo", 'waitfor': '.*#', 'category': 'Memory', 'format': 'single-column'},
    'memory_used': {'command': "grep -E '^MemTotal|^MemFree|^Buffers|^Cached' /proc/meminfo", 'waitfor': '.*#', 'category': 'Memory', 'format': 'single-column'},
    'swap_total': {'command': "grep SwapTotal /proc/meminfo", 'waitfor': '.*#', 'category': 'Swap', 'format': 'single-column'},
    'swap_free': {'command': "grep SwapFree /proc/meminfo", 'waitfor': '.*#', 'category': 'Swap', 'format': 'single-column'},
    'disk_usage': {'command': "df -h /", 'waitfor': '.*#', 'category': 'Disk', 'format': 'single-column'},
    'load_average': {'command': "cat /proc/loadavg", 'waitfor': '.*#', 'category': 'Load', 'format': 'single-column'},
    'network_interface': {'command': "ifconfig -a", 'waitfor': '.*#', 'format': 'ifconfig'},
    'network_connections_established': {'command': "ss -t -a -n state established", 'waitfor': '.*#', 'category': 'Network', 'format': 'single-column'},
    'network_connections_time_wait': {'command': "ss -t -a -n state time-wait", 'waitfor': '.*#', 'category': 'Network', 'format': 'single-column'},
    'network_connections_closed': {'command': "ss -t -a -n state closed", 'waitfor': '.*#', 'category': 'Network', 'format': 'single-column'},
    'processes_running': {'command': "ps -e --no-headers", 'waitfor': '.*#', 'category': 'Processes', 'format': 'single-column'},
    'uptime': {'command': "uptime", 'waitfor': '.*#', 'category': 'System', 'format': 'single-column'},
    'users_logged_in': {'command': "who", 'waitfor': '.*#', 'category': 'Users', 'format': 'single-column'},
    'system_version': {'command': "uname -a", 'waitfor': '.*#', 'category': 'System', 'format': 'single-column'},
    'system_architecture': {'command': "uname -m", 'waitfor': '.*#', 'category': 'System', 'format': 'single-column'},
    'kernel_version': {'command': "uname -r", 'waitfor': '.*#', 'category': 'System', 'format': 'single-column'},
    'available_memory': {'command': "grep MemAvailable /proc/meminfo", 'waitfor': '.*#', 'category': 'Memory', 'format': 'single-column'},
    'total_processes': {'command': "ps -e", 'waitfor': '.*#', 'category': 'Processes', 'format': 'single-column'},
    'tcp_connections': {'command': "cat /proc/net/tcp* /proc/net/tcp6*", 'waitfor': '.*#', 'category': 'Network', 'format': 'single-column'},
    'udp_connections': {'command': "cat /proc/net/udp* /proc/net/udp6*", 'waitfor': '.*#', 'category': 'Network', 'format': 'single-column'},
    'total_users': {'command': "awk -F: '$3 >= 1000 && $1 != \"nobody\"' /etc/passwd", 'waitfor': '.*#', 'category': 'Users', 'format': 'single-column'},
    'logged_in_users': {'command': "who | awk '{print $1}' | sort | uniq", 'waitfor': '.*#', 'category': 'Users', 'format': 'single-column'},
    'last_boot_time': {'command': "who -b", 'waitfor': '.*#', 'category': 'System', 'format': 'single-column'},
    'kernel_info': {'command': "cat /proc/version", 'waitfor': '.*#', 'category': 'System', 'format': 'single-column'},
    'system_uptime': {'command': "uptime -s", 'waitfor': '.*#', 'category': 'System', 'format': 'single-column'},
    'total_memory': {'command': "grep MemTotal /proc/meminfo", 'waitfor': '.*#', 'category': 'Memory', 'format': 'single-column'},
    'total_swap': {'command': "grep SwapTotal /proc/meminfo", 'waitfor': '.*#', 'category': 'Swap', 'format': 'single-column'}



            },
            'outro': {
                'exit': {'command': 'exit', 'waitfor': '[a-z]+#'},
            }
        }

