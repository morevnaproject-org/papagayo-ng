import json
import os
import string
import tempfile
from pathlib import Path
import time

import PySide2.QtCore as QtCore
import utilities

if utilities.get_app_data_path() not in os.environ['PATH']:
    os.environ['PATH'] += os.pathsep + utilities.get_app_data_path()
import pydub
from pydub.generators import WhiteNoise
from PySide2 import QtWidgets
from allosaurus.app import read_recognizer

from utilities import get_main_dir


class AutoRecognize:
    def __init__(self, sound_path):
        ini_path = os.path.join(utilities.get_app_data_path(), "settings.ini")
        self.settings = QtCore.QSettings(ini_path, QtCore.QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)  # File only, not registry or or.
        self.allo_model_path = Path(os.path.join(utilities.get_app_data_path(), "allosaurus_model"))
        self.temp_wave_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
        self.duration_for_one_second = 1
        app = QtWidgets.QApplication.instance()
        self.main_window = None
        self.threadpool = QtCore.QThreadPool.globalInstance()
        for widget in app.topLevelWidgets():
            if isinstance(widget, QtWidgets.QMainWindow):
                self.main_window = widget
        self.sound_length = 0
        self.analysis_finished = False
        self.test_decode_time()
        self.convert_to_wav(sound_path)

    def test_decode_time(self):
        five_second_sample = WhiteNoise().to_audio_segment(duration=5000)
        five_second_sample = five_second_sample.set_sample_width(2)
        five_second_sample = five_second_sample.set_frame_rate(16000)
        five_second_sample = five_second_sample.set_channels(1)
        five_second_sample_temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
        out_ = five_second_sample.export(five_second_sample_temp_file, format="wav", bitrate="256k")
        out_.close()

        try:
            model = read_recognizer("latest", self.allo_model_path)
        except TypeError:
            model = read_recognizer("latest")
        start_time = time.process_time()
        model.recognize(five_second_sample_temp_file, timestamp=True,
                        lang_id=self.settings.value("allo_lang_id", "eng"),
                        emit=float(self.settings.value("allo_emission", 1.0)))
        self.duration_for_one_second = (time.process_time() - start_time) / 5
        os.remove(five_second_sample_temp_file)

    def convert_to_wav(self, sound_path):
        pydubfile = pydub.AudioSegment.from_file(sound_path, format=os.path.splitext(sound_path)[1][1:])
        pydubfile = pydubfile.set_sample_width(2)
        pydubfile = pydubfile.set_frame_rate(16000)
        pydubfile = pydubfile.set_channels(1)
        half_second_silence = pydub.AudioSegment.silent(500)
        self.sound_length = pydubfile.duration_seconds
        pydubfile += half_second_silence
        out_ = pydubfile.export(self.temp_wave_file, format="wav", bitrate="256k")
        out_.close()

    def update_progress(self, progress_callback):
        expected_time_to_finish = self.sound_length * self.duration_for_one_second
        start_time = time.process_time()
        finish_time = start_time + expected_time_to_finish
        progress_multiplier = 100.0 / expected_time_to_finish
        while time.process_time() < finish_time:
            if self.analysis_finished:
                break
            QtCore.QCoreApplication.processEvents()
            current_progress = (time.process_time() - start_time) * progress_multiplier
            progress_callback.emit(current_progress)
        self.main_window.lip_sync_frame.status_progress.hide()

    def recognize_allosaurus(self):
        try:
            model = read_recognizer("latest", self.allo_model_path)
        except TypeError:
            model = read_recognizer("latest")
        worker = utilities.Worker(self.update_progress)
        self.main_window.lip_sync_frame.status_progress.show()
        self.main_window.lip_sync_frame.status_progress.setMaximum(100)
        worker.signals.progress.connect(self.main_window.lip_sync_frame.status_bar_progress)
        self.threadpool.start(worker)

        results = model.recognize(self.temp_wave_file, timestamp=True,
                                  lang_id=self.settings.value("allo_lang_id", "eng"),
                                  emit=float(self.settings.value("allo_emission", 1.0)))
        self.analysis_finished = True
        ipa_list = []

        if results:
            ipa_convert = json.load(open("ipa_cmu.json", encoding="utf8"))
            stress_symbols = [*string.digits, r"!", r"+", r"/", r"#", r"ː", r"ʰ"]
            time_list = []
            prev_start = 0
            for line in results.splitlines():
                start, dur, phone = line.split()
                phone = "".join(e for e in phone if e not in stress_symbols)
                if phone not in ipa_convert:
                    print("Missing conversion for: " + phone)
                    dlg = QtWidgets.QMessageBox()
                    dlg.setText("Missing conversion for: " + phone)
                    dlg.setWindowTitle("Missing Phoneme Conversion")
                    dlg.setWindowIcon(self.main_window.windowIcon())
                    dlg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    dlg.setDefaultButton(QtWidgets.QMessageBox.Ok)
                    dlg.setIcon(QtWidgets.QMessageBox.Information)
                    dlg.exec_()

                phone_dict = {"start": float(start), "duration": float(dur), "phoneme": ipa_convert.get(phone)}
                time_list.append(float(start) - prev_start)
                prev_start = float(start)
                ipa_list.append(phone_dict)
            peaks = self.get_level_peaks(time_list)
            return ipa_list, peaks, results
        else:
            return None

    def get_level_peaks(self, v):
        peaks = [0]

        i = 1
        while i < len(v) - 1:
            pos_left = i
            pos_right = i

            while v[pos_left] == v[i] and pos_left > 0:
                pos_left -= 1

            while v[pos_right] == v[i] and pos_right < len(v) - 1:
                pos_right += 1

            # is_lower_peak = v[pos_left] > v[i] and v[i] < v[pos_right]
            is_upper_peak = v[pos_left] < v[i] and v[i] > v[pos_right]

            if is_upper_peak:
                peaks.append(i)

            i = pos_right

        peaks.append(len(v))
        return peaks

    def __del__(self):
        os.remove(self.temp_wave_file)
