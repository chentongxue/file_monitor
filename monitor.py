# coding=utf-8
import os
import time

import requests
from watchdog.events import FileSystemEventHandler
from observer import observer


class FileMonitorHandler(FileSystemEventHandler):
    def __init__(self, directory, suffix, keywords, bot_api, name, alert_cd=60):
        self.directory = directory
        self.keywords = keywords
        self.bot_api = bot_api
        self.alert_cd = alert_cd
        self.last_alert_time = 0
        self.suffix = suffix
        self.last_seeks = dict()
        self.init()
        self.name = name

    def init(self):
        for filename in os.listdir(self.directory):
            path = os.path.join(self.directory, filename)
            if os.path.isfile(path) and filename.endswith(self.suffix):
                with open(path) as f:
                    f.seek(0, os.SEEK_END)
                    self.last_seeks[filename] = f.tell()

    def send_alert_message(self, content):
        if self.last_alert_time + self.alert_cd > time.time():
            return

        headers = {
            'Content-Type': 'application/json',
        }
        params = {
            'msgtype': 'text',
            'text': {
                'content': content
            }
        }
        print content
        if self.bot_api:
            response = requests.post(self.bot_api, headers=headers, json=params)
            print response.json()
        self.last_alert_time = time.time()

    def on_modified(self, event):
        if event.is_directory:
            return
        if not event.src_path.endswith(self.suffix):
            return
        self.on_new_content(event.src_path)

    def on_new_content(self, file_path):
        filename = os.path.basename(file_path)

        with open(file_path) as f:
            f.seek(0, os.SEEK_END)
            last_seek = self.last_seeks.get(filename, 0)
            if f.tell() < last_seek:
                last_seek = 0
            f.seek(last_seek)
            new_content = f.read()
            self.scan_keywords(new_content, filename)
            self.last_seeks[filename] = f.tell()

    def scan_keywords(self, text, filename):
        errors = []
        for line in text.split('\n'):
            for keyword in self.keywords:
                if keyword in line:
                    file_path = os.path.join(self.directory, filename)
                    error_message = u'[%s][%s] 发生告警！错误日志[%s]' % (self.name, file_path, line)
                    errors.append(error_message)
        if errors:
            self.send_alert_message('\n'.join(errors))

    def run(self):
        observer.schedule(event_handler=self, path=self.directory)
