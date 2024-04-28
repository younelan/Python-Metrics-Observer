import paramiko
import re
import time
import logging
import sys
from Plugin import Plugin 


class CollectSSH(Plugin):
    def __init__(self, sshconfig):
        super().__init__()
        self.connection = None
        self.sshconfig = sshconfig
        self.shell = None
        self.error = ""
        self.collections = []
        self.logger = logging.getLogger(__name__)

    def set_config(self, sshconfig):
        self.sshconfig = sshconfig

    def connect(self):
        try:
            self.connection = paramiko.SSHClient()
            if self.sshconfig.get('auto_add_policy', False):
                self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            else:
                self.connection.set_missing_host_key_policy(paramiko.RejectPolicy())
            self.connection.connect(self.sshconfig['host'], self.sshconfig['port'], self.sshconfig['user'], self.sshconfig['pass'])
            self.logger.info("SSH connection established")
            self.shell = self.connection.invoke_shell()
            time.sleep(1)  # Wait for shell to open
            self.poll()  # Consume initial shell output
            return True
        except paramiko.AuthenticationException:
            self.error = "SSH authentication failed"
            self.logger.error("SSH authentication failed")
            return False
        except paramiko.SSHException:
            self.error = "SSH connection failed"
            self.logger.error("SSH connection failed")
            return False
        except Exception as e:
            self.error = f"SSH connection error: {e}"
            self.logger.error(f"SSH connection error: {e}")
            return False

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def status(self):
        return bool(self.connection)

    def get_error(self):
        return self.error

    def poll(self):
        if not self.connection or not self.shell:
            self.error = "No connection or shell established"
            return False
        try:
            data = ""
            while self.shell.recv_ready():
                data += self.shell.recv(4096).decode()
            return data
        except Exception as e:
            self.error = f"Error while polling: {e}"
            self.logger.error(f"Error while polling: {e}")
            return False

    def send(self, text):
        if not self.connection or not self.shell:
            self.error = "No connection or shell established"
            return False
        try:
            self.shell.send(text + "\n")
            return True
        except Exception as e:
            self.error = f"Error while sending data: {e}"
            self.logger.error(f"Error while sending data: {e}")
            return False

    def collect(self, commandgroups=None):
        if not commandgroups:
            commandgroups = self.commandgroups
        retval = {}
        try:
            if self.connect():
                for groupidx, commands in commandgroups.items():
                    retval[groupidx] = {}
                    for commandidx, command in commands.items():
                        self.send(command['command'])
                        if 'waitfor' in command:
                            result = self.wait_for(command['waitfor'])
                            result['format'] = command.get('format', 'text')
                            result['delimeter'] = command.get('delimeter', ':')
                            result['category'] = command.get('category', 'default')
                            result['replacements'] = command.get('replacements', {})
                            retval[groupidx][commandidx] = result
                self.disconnect()
        except Exception as e:
            self.error = f"Error while collecting data: {e}"
            self.logger.error(f"Error while collecting data: {e}")
        return retval

    def wait_for(self, regex, timeout=5):
        if not self.connection or not self.shell:
            self.error = "No connection or shell established"
            return {'data': None, 'success': False}
        try:
            end_time = time.time() + timeout
            data = ""
            while time.time() < end_time:
                if self.shell.recv_ready():
                    buffer = self.shell.recv(4096).decode()
                    data += buffer
                    if re.search(regex, data):
                        return {'data': data, 'success': True}
                time.sleep(0.1)
            self.error = "Timeout occurred while waiting for regex match"
            return {'data': data, 'success': False}
        except Exception as e:
            self.error = f"Error while waiting for regex match: {e}"
            self.logger.error(f"Error while waiting for regex match: {e}")
            return {'data': data, 'success': False}

