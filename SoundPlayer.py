import audioop
import os
import platform
import traceback
import wave
from utilities import *
import pyaudio

from utilities import which

import subprocess
import tempfile

try:
    import thread
except ImportError:
    import _thread as thread

class SoundPlayer:
    def __init__(self, soundfile, parent):
        self.soundfile = soundfile
        self.isplaying = False
        self.time = 0  # current audio position in frames
        self.audio = pyaudio.PyAudio()
        self.volume = 100

        if which("ffmpeg") is not None:
            self.converter = which("ffmpeg")
        elif which("avconv") is not None:
            self.converter = which("avconv")
        else:
            if platform.system() == "Windows":
                self.converter = os.path.join(get_main_dir(), "ffmpeg.exe")
            else:
                # TODO: Check if we have ffmpeg or avconv installed
                self.converter = "ffmpeg"

        try:
            format = os.path.splitext(self.soundfile)[1][1:]

            wave_file = self.soundfile

            if format != "wav":
                wave_file = tempfile._get_default_tempdir() + "/" + next(tempfile._get_candidate_names()) + ".wav"
                subprocess.call([self.converter, '-i', self.soundfile, wave_file])

            self.wave_reference = wave.open(wave_file)

            self.isvalid = True

        except:
            traceback.print_exc()
            self.wave_reference = None
            self.isvalid = False

    def IsValid(self):
        return self.isvalid

    def Duration(self):
        return float(self.wave_reference.getnframes()) / float(self.wave_reference.getframerate())

    def GetRMSAmplitude(self, time, sampleDur):
        startframe = int(round(time * self.wave_reference.getframerate()))
        samplelen = int(round(sampleDur * self.wave_reference.getframerate()))
        self.wave_reference.setpos(startframe)
        frame = self.wave_reference.readframes(samplelen)
        width = self.wave_reference.getsampwidth()
        return audioop.rms(frame, width)

    def IsPlaying(self):
        return self.isplaying

    def SetCurTime(self, time):
        self.time = time

    def Stop(self):
        self.isplaying = False

    def CurrentTime(self):
        return self.time

    def SetVolume(self, volume):
        self.volume = volume

    def _play(self, start, length):
        self.isplaying = True

        startframe = int(round(start * self.wave_reference.getframerate()))
        samplelen = int(round(length * self.wave_reference.getframerate()))
        remaining = samplelen
        chunk = 1024
        try:
            self.wave_reference.setpos(startframe)
        except wave.Error:
            self.isplaying = False
            return
        stream = self.audio.open(format=
                                 self.audio.get_format_from_width(self.wave_reference.getsampwidth()),
                                 channels=self.wave_reference.getnchannels(),
                                 rate=self.wave_reference.getframerate(),
                                 output=True)
        # read data

        if remaining >= 1024:
            data = audioop.mul(self.wave_reference.readframes(chunk),self.wave_reference.getsampwidth(), self.volume/100.0)
            remaining -= chunk
        else:
            data = audioop.mul(self.wave_reference.readframes(remaining),self.wave_reference.getsampwidth(), self.volume/100.0)
            remaining = 0

        # play stream
        while len(data) > 0 and self.isplaying:
            stream.write(data)
            self.time = float(self.wave_reference.tell()) / float(self.wave_reference.getframerate())
            if remaining >= 1024:
                data = audioop.mul(self.wave_reference.readframes(chunk),self.wave_reference.getsampwidth(), self.volume/100.0)
                remaining -= chunk
            else:
                data = audioop.mul(self.wave_reference.readframes(remaining),self.wave_reference.getsampwidth(), self.volume/100.0)
                remaining = 0

        stream.close()
        self.isplaying = False

    def Play(self, arg):
        thread.start_new_thread(self._play, (0, self.Duration()))

    def PlaySegment(self, start, length, arg):
        if not self.isplaying:  # otherwise this get's kinda echo-y
            thread.start_new_thread(self._play, (start, length))
