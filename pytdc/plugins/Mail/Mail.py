import json
import sys
import subprocess
from os.path import dirname,abspath
import os

base_folder = dirname(dirname(abspath(__file__)) )
sys.path.insert(0, base_folder)
from Plugin import Plugin

class Mail(Plugin):
    def show_page(self, params):
        page = params.get('page', 'viewqueue')
        action = params.get('action', 'viewqueue')
        output = ""
        if action == 'start':
            output = self.start()
        elif action == 'stop':
            output = self.stop()
        elif action == 'pause':
            output = self.pause()
        elif action == 'unpause':
            output = self.unpause()
        else:
            if page == "mailsummary":
                output = self.show_queue_summary()
            else:
                output = self.show_queue()
        return output

    def get_menus(self):
        return {
            "mail": {
                "text": "Mail Server",
                "weight": 1,
                "children": {
                    "queuestats": {"plugin": "mail", "page": "queuestats", "text": "Graphs"},
                    "viewqueue": {"plugin": "mail", "page": "viewqueue", "text": "View Queue"},
                    "mailsummary": {"plugin": "mail", "page": "mailsummary", "text": "Mail Summary"}
                }
            }
        }

    def on_command(self, options):
        action = options.get('a')
        if action == "pause":
            self.pause()
        elif action == "unpause":
            self.unpause()
        elif action == "start":
            self.start()
        elif action == "stop":
            self.stop()
        else:
            print(f"Unknown Action - mail::{action}")

    def get_queue(self):
        queue = self.run_command('postqueue -j')
        return queue

    def get_fake_queue(self):
        raw_queue = '''{"queue_name": "deferred", "queue_id": "454C01C1504", "arrival_time": 1710007169, "message_size": 1572, "sender": "nabil@elandaloussi.net",  "recipients": [{"address": "anouar.zyne@sawab.ma", "delay_reason": "Host or domain name not found. Name service error for name=sawab.ma type=MX: Host not found, try again"}]}
        {"queue_name": "deferred", "queue_id": "454C01C1504", "arrival_time": 1710007169, "message_size": 1572, "sender": "nabil@elandaloussi.net",  "recipients": [{"address": "anouar.zyne@sawab.ma", "delay_reason": "Host or domain name not found. Name service error for name=sawab.ma type=MX: Host not found, try again"}]}
        {"queue_name": "active", "queue_id": "D2AB8164F6C", "arrival_time": 1598566172, "message_size": 509, "sender": "test@root.ca", "recipients": [{"address": "genie@test.com", "delay_reason": "SASL authentication failed; server alert.alteeve.com[65.39.153.73] said: 535 5.7.8 Error: authentication failed: PDYxOTk0MjM0MjQ0OTc0NjcuMTU5ODU2NzI3NUBhbGVydC5hbHRlZXZlLmNvbT4="}]}
        {"queue_name": "deferred", "queue_id": "148C27A1", "arrival_time": 1598567179, "message_size": 506, "sender": "test@root.ca", "recipients": [{"address": "bob@test.com", "delay_reason": "SASL authentication failed; server alert.alteeve.com[65.39.153.73] said: 535 5.7.8 Error: authentication failed: PDMwMDU5MjIxODIxODEyOTQuMTU5ODU2NzE3OEBhbGVydC5hbHRlZXZlLmNvbT4="}]}
        {"queue_name": "deferred", "queue_id": "BA21318B727", "arrival_time": 1598567440, "message_size": 509, "sender": "test@root.ca", "recipients": [{"address": "alfred@test.com", "delay_reason": "SASL authentication failed; server alert.alteeve.com[65.39.153.73] said: 535 5.7.8 Error: authentication failed: PDQyOTA5MTAzODIxMzg5NDQuMTU5ODU2NzQ0MEBhbGVydC5hbHRlZXZlLmNvbT4="}]}'''
        return raw_queue

    def show_queue_summary(self):
        raw_queue = self.get_queue()
        # Implementation...
        pass

    def show_queue(self):
        raw_queue = self.get_queue()
        # Implementation...
        pass

    def view_message(self, msg_id):
        # Implementation...
        pass

    def on_update(self):
        status = []
        # Implementation...
        pass

    def start(self):
        result = subprocess.run(['sudo', 'systemctl', 'start', 'postfix'], capture_output=True, text=True)
        if result.returncode == 0:
            return "started"
        else:
            return f"Error starting Postfix: {result.stderr}"

    def stop(self):
        result = subprocess.run(['sudo', 'systemctl', 'stop', 'postfix'], capture_output=True, text=True)
        if result.returncode == 0:
            return "stopped"
        else:
            return f"Error stopping Postfix: {result.stderr}"

    def pause(self):
        # Implementation...
        pass

    def unpause(self):
        # Implementation...
        pass

    def show_widget(self, widget):
        if not widget: 
            widget = 'postfix_status'
        if widget == "postfix_status":
            return self.postfix_status()
        else:
            return ""

    def postfix_status(self):
        basedir = os.path.dirname(os.path.abspath(__file__))
        start = self.get_translation("Start")
        service = self.get_translation("Service")
        mail = self.get_translation("Mail Delivery")
        stop = self.get_translation("Stop")
        stopped = self.get_translation("Stopped")
        started = self.get_translation("Started")
        enable = self.get_translation("Pause")
        disable = self.get_translation("Unpause")
        size = self.get_translation("Queue Size")
        approximate = self.get_translation("Approximately")
        output = "<h2 class='widgetheader'>" + self.get_translation("Postfix State")+ "</h2>"
        status = self.run_command(os.path.join(basedir, 'bin/postfixstatus'))
        
        if status == "started":
            output += service + " <span class='connected'>" + started + "</span> ( <a href='./?page=mail&action=stop'>" + stop + "</a>) | "
        else:
            output += service + " <span class='disconnected'>" + stopped + "</span> ( <a href='./?page=mail&action=start'>" + start + "</a>) | "
            
        output += "<br>"
        defer_transports = self.run_command(['postconf', '-h', 'defer_transports'])
        if defer_transports == "smtp":
            output += mail + " <span class='disconnected'>" + stopped + "</span> ( <a href='./?page=mail&action=unpause'>" + disable + "</a>)"
        else:
            output += mail + " <span class='connected'>" + started + "</span> ( <a href='./?page=mail&action=pause'>" + enable + "</a>)<p>"
        
        mailcount = self.mailcount()
        output += size + ": </b>" + str(mailcount) + "<font size=-3>(" + approximate + ")</font>"
        
        return output

    def mailcount(self):
        mailqueue = self.run_command([ 'postqueue', '-p'])
        print (mailqueue)
        if mailqueue != None:
            count = len(mailqueue.split('@'))
        else:
            count = 0
        return count

