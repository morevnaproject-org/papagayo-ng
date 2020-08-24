import json
import subprocess
import os
import threading
from PySide2.QtWidgets import QProgressDialog
from PySide2.QtCore import QCoreApplication
import sys

if sys.platform == "win32":
    RHUBARB_PATH = './rhubarb/rhubarb.exe'
else:
    RHUBARB_PATH = './rhubarb/rhubarb'


class RhubarbTimeoutException(Exception):
    def __init__(self):
        super().__init__()


class Rhubarb:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.process = None
        self.progress = 0
        self.progress_dialog = QProgressDialog("Processing by Rhubarb", "Cancel", 0, 100)
        self.progress_dialog.setWindowTitle("Progress")
        self.progress_dialog.setModal(True)
        self.progress_dialog.forceShow()

    def _signal_handler(self):
        print('Rhubarb did not respond for more than 30 seconds.')
        raise RhubarbTimeoutException()

    def _read_log(self):
        alarm = threading.Timer(30, self._signal_handler)
        alarm.start()
        log = self.process.stderr.readline().decode('utf-8').strip()
        self.progress = json.loads(log).get("value", 0) * 100
        alarm.cancel()
        return log

    def _read_result(self):
        alarm = threading.Timer(1, self._signal_handler)
        alarm.start()
        line = ''
        result = ''
        while line != '}':
            line = self.process.stdout.readline().decode('utf-8').strip()
            result += line
        alarm.cancel()
        return json.loads(result)

    def run(self):
        if not os.path.exists(RHUBARB_PATH):
            return None
        args = [RHUBARB_PATH, self.file_path, '--machineReadable', '-f', 'json']

        self.process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result_is_ready = False
        log = ''
        while True:
            if result_is_ready:
                result = self._read_result()
                return result['mouthCues']
            else:
                log = self._read_log()
                log_formatted = json.loads(log)
            self.progress_dialog.setValue(int(self.progress))
            QCoreApplication.processEvents()
            if log_formatted['type'] == 'success':
                result_is_ready = True
                self.progress_dialog.close()
            elif log_formatted['type'] == 'failure':
                self.progress_dialog.close()
                return None
