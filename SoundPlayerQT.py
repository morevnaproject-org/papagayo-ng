from PySide2 import QtWidgets

from utilities import *

import time

from PySide2.QtMultimedia import QMediaPlayer, QAudioFormat, QAudioBuffer, QAudioDecoder
from PySide2.QtMultimedia import QAudioOutput
from PySide2.QtCore import QCoreApplication
from PySide2.QtCore import QUrl

from utilities import which
from cffi import FFI

ffi = FFI()

import numpy as np

try:
    import thread
except ImportError:
    import _thread as thread


class SoundPlayer:
    def __init__(self, soundfile, parent):
        self.soundfile = soundfile
        self.isplaying = False
        self.time = 0  # current audio position in frames
        self.audio = QMediaPlayer()
        self.decoder = QAudioDecoder()
        self.is_loaded = False
        self.volume = 100
        self.isplaying = False
        self.decoded_audio = {}
        self.only_samples = []
        self.decoding_is_finished = False
        self.max_bits = 32768
        self.signed = False
        # File Loading is Asynchronous, so we need to be creative here, doesn't need to be duration but it works
        self.audio.durationChanged.connect(self.on_durationChanged)
        self.decoder.finished.connect(self.decode_finished_signal)
        self.audio.setMedia(QUrl.fromLocalFile(soundfile))
        self.decoder.setSourceFilename(soundfile)  # strangely inconsistent file-handling
        self.top_level_widget = None

        for widget in QtWidgets.QApplication.topLevelWidgets():
            if "lip_sync_frame" in dir(widget):
                self.top_level_widget = widget
        self.top_level_widget.lip_sync_frame.status_progress.show()
        self.top_level_widget.lip_sync_frame.status_progress.reset()
        self.top_level_widget.lip_sync_frame.status_progress.setMinimum(0)
        self.top_level_widget.lip_sync_frame.status_progress.setMaximum(0)
        # It will hang here forever if we don't process the events.
        while not self.is_loaded:
            QCoreApplication.processEvents()
            time.sleep(0.01)
        self.top_level_widget.lip_sync_frame.status_progress.setMaximum(self.decoder.duration())
        self.decode_audio(self.top_level_widget.lip_sync_frame.status_bar_progress)
        self.top_level_widget.lip_sync_frame.status_progress.hide()
        self.np_data = np.array(self.only_samples)
        if not self.signed:  # don't ask me why this fixes 8 bit samples...
            self.np_data = self.np_data - self.max_bits / 2
        print(len(self.only_samples))
        print(self.max_bits)
        self.isvalid = True

    def audioformat_to_datatype(self, audioformat):
        num_bits = audioformat.sampleSize()
        signed = audioformat.sampleType()
        self.max_bits = 2 ** int(num_bits)
        if signed == QAudioFormat.SampleType.UnSignedInt:
            self.signed = False
            return "uint{0}_t".format(str(num_bits))
        elif signed == QAudioFormat.SampleType.SignedInt:
            self.signed = True
            self.max_bits = int(self.max_bits / 2)
            return "int{0}_t".format(str(num_bits))

    def decode_audio(self, progress_callback):
        self.decoder.start()
        while not self.decoding_is_finished:
            QCoreApplication.processEvents()
            if self.decoder.bufferAvailable():
                tempdata = self.decoder.read()
                # We use the Pointer Address to get a cffi Pointer to the data (hopefully)
                cast_data = self.audioformat_to_datatype(tempdata.format())
                possible_data = ffi.cast("{1}[{0}]".format(tempdata.sampleCount(), cast_data),
                                         int(tempdata.constData()))
                self.only_samples.extend(possible_data)
                self.decoded_audio[self.decoder.position()] = [possible_data, len(possible_data), tempdata.byteCount(),
                                                               tempdata.format()]
            progress_callback(self.decoder.position())

    def decode_finished_signal(self):
        self.decoding_is_finished = True

    def on_durationChanged(self, duration):
        self.is_loaded = True

    def get_audio_buffer(self, bufferdata):
        print(bufferdata)

    def IsValid(self):
        return self.isvalid

    def Duration(self):
        return self.audio.duration() / 1000.0

    def GetRMSAmplitude(self, time_pos, sample_dur):
        # time_start = time_pos * (len(self.only_samples)/self.Duration())
        # time_end = (time_pos + sample_dur) * (len(self.only_samples)/self.Duration())
        # samples = self.only_samples[int(time_start):int(time_end)]
        time_start = time_pos * (len(self.np_data) / self.Duration())
        time_end = (time_pos + sample_dur) * (len(self.np_data) / self.Duration())
        samples = self.np_data[int(time_start):int(time_end)]

        if len(samples):
            return np.sqrt(np.mean(samples ** 2))
        else:
            return 1

    def is_playing(self):
        if self.audio.state() == QMediaPlayer.PlayingState:
            return True
        else:
            return False

    def set_cur_time(self, newtime):
        self.time = newtime * 1000.0
        self.audio.setPosition(self.time)

    def stop(self):
        self.isplaying = False
        self.audio.stop()

    def current_time(self):
        self.time = self.audio.position() / 1000.0
        return self.time

    def set_volume(self, newvolume):
        self.volume = newvolume
        self.audio.setVolume(self.volume)

    def play(self, arg):
        self.isplaying = True  # TODO: We should be able to replace isplaying with queries to self.audio.state()
        self.audio.play()

    def play_segment(self, start, length):
        if not self.is_playing():  # otherwise this gets kinda echo-y
            self.isplaying = True
            self.audio.setPosition(start * 1000.0)
            self.audio.play()
            thread.start_new_thread(self._wait_for_segment_end, (start, length))

    def _wait_for_segment_end(self, newstart, newlength):
        start = newstart * 1000.0
        length = newlength * 1000.0
        end = start + length
        while self.audio.position() < end:
            if not self.isplaying:
                return 0
            QCoreApplication.processEvents()
            time.sleep(0.001)
        self.audio.stop()
        self.isplaying = False
