import json
import signal
import subprocess
import os

RHUBARB_PATH = './rhubarb/rhubarb'


class RhubarbTimeoutException(Exception):
    def __init__(self):
        super().__init__()


class Rhubarb:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.process = None

    def _signal_handler(self, signum, frame):
        print('Rhubarb не отвечает более 30 секунд')
        raise RhubarbTimeoutException()

    def _read_log(self):
        signal.signal(signal.SIGALRM, self._signal_handler)
        signal.alarm(30)
        log = self.process.stderr.readline().decode('utf-8').strip()
        signal.alarm(0)
        return log

    def _read_result(self):
        signal.signal(signal.SIGALRM, self._signal_handler)
        signal.alarm(1)
        line = ''
        result = ''
        while line != '}':
            line = self.process.stdout.readline().decode('utf-8').strip()
            result += line
        signal.alarm(0)
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
            print(log_formatted['log']['message'])
            if log_formatted['log']['message'] == 'Application terminating normally.':
                result_is_ready = True
