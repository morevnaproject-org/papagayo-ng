
import os
import platform
import traceback

from utilities import *

import time

from PySide2.QtMultimedia import QMediaPlayer, QAudioProbe, QAudioBuffer
from PySide2.QtMultimedia import QAudioOutput
from PySide2.QtCore import QCoreApplication
from PySide2.QtCore import QUrl

from utilities import which

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
        self.probe = QAudioProbe()
        self.is_loaded = False
        self.volume = 100
        self.isplaying = False
        # File Loading is Asynchronous, so we need to be creative here, doesn't need to be duration but it works
        self.audio.durationChanged.connect(self.on_durationChanged)
        self.audio.setMedia(QUrl.fromLocalFile(soundfile))
        # It will hang here forever if we don't process the events.
        while not self.is_loaded:
            QCoreApplication.processEvents()
            time.sleep(0.1)

        self.isvalid = True
        self.probe.setSource(self.audio)
        self.probe.audioBufferProbed.connect(self.get_audio_buffer)

        #self.audio.play()

    def on_durationChanged(self, duration):
        print("Changed!")
        print(duration)
        self.is_loaded = True

    def get_audio_buffer(self, bufferdata):
        print(bufferdata)

    def IsValid(self):
        return self.isvalid

    def Duration(self):
        return self.audio.duration() / 1000.0

    def GetRMSAmplitude(self, time, sampleDur):
        return 1  # TODO: Somehow get the raw sampledata from QT here...

    def is_playing(self):
        return self.isplaying

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
        print("Playing Segment")
        if not self.isplaying:  # otherwise this get's kinda echo-y
            self.isplaying = True
            self.audio.setPosition(start * 1000.0)
            self.audio.play()
            thread.start_new_thread(self._wait_for_segment_end, (start, length))

    def _wait_for_segment_end(self, newstart, newlength):
        start = newstart * 1000.0
        length = newlength * 1000.0
        end = start + length
        print(start)
        print(length)
        print(end)
        while self.audio.position() < end:
            QCoreApplication.processEvents()
            print(self.audio.position())
            time.sleep(0.001)
        self.audio.stop()
        self.isplaying = False