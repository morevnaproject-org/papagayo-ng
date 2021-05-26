import audioop
import os
import platform
import traceback
import wave
from utilities import *
import sounddevice as sd
import time

from utilities import which

try:
    from pydub import AudioSegment
    from pydub.utils import make_chunks
except ImportError:
    AudioSegment = None

try:
    import thread
except ImportError:
    import _thread as thread


class SoundPlayer:
    def __init__(self, soundfile, parent):
        self.soundfile = soundfile
        self.isplaying = False
        self.time = 0  # current audio position in frames
        self.audio = sd
        self.pydubfile = None
        self.volume = 100

        if AudioSegment:
            if which("ffmpeg") is not None:
                AudioSegment.converter = which("ffmpeg")
            elif which("avconv") is not None:
                AudioSegment.converter = which("avconv")
            else:
                if platform.system() == "Windows":
                    AudioSegment.converter = os.path.join(get_main_dir(), "ffmpeg.exe")
                    #AudioSegment.converter = os.path.dirname(os.path.realpath(__file__)) + "\\ffmpeg.exe"
                else:
                    # TODO: Check if we have ffmpeg or avconv installed
                    AudioSegment.converter = "ffmpeg"

        try:
            if AudioSegment:
                print(self.soundfile)
                self.pydubfile = AudioSegment.from_file(self.soundfile, format=os.path.splitext(self.soundfile)[1][1:])
            else:
                self.wave_reference = wave.open(self.soundfile)

            self.isvalid = True

        except:
            traceback.print_exc()
            self.wave_reference = None
            self.isvalid = False
        if AudioSegment:
            self.pydubfile = self.pydubfile.set_sample_width(2)
            self.audio.default.samplerate = self.pydubfile.frame_rate * self.pydubfile.channels

        else:
            self.audio.default.samplerate = self.wave_reference.getframerate()

    def IsValid(self):
        return self.isvalid

    def Duration(self):
        if AudioSegment:
            return(self.pydubfile.duration_seconds)
        else:
            return float(self.wave_reference.getnframes()) / float(self.wave_reference.getframerate())

    def GetRMSAmplitude(self, time, sampleDur):
        if AudioSegment:
            return self.pydubfile[time*1000.0:(time+sampleDur)*1000.0].rms
        else:
            startframe = int(round(time * self.wave_reference.getframerate()))
            samplelen = int(round(sampleDur * self.wave_reference.getframerate()))
            self.wave_reference.setpos(startframe)
            frame = self.wave_reference.readframes(samplelen)
            width = self.wave_reference.getsampwidth()
            return audioop.rms(frame, width)

    def is_playing(self):
        return self.isplaying

    def set_cur_time(self, time):
        self.time = time

    def stop(self):
        self.isplaying = False

    def current_time(self):
        return self.time

    def set_volume(self, volume):
        self.volume = volume

    def _play(self, start, length):
        self.isplaying = True
        if AudioSegment:
            millisecondchunk = 50 / 1000.0
            playchunk = self.pydubfile[start*1000.0:(start+length)*1000.0] - (60 - (60 * (self.volume/100.0)))
            self.time = start
            self.audio.play(playchunk.get_array_of_samples(), blocking=False)

            # For some reason it does not like the separated chunks, so we play it non-
            # We might be able to use self.audio.get_stream().time to improve accuracy
            for chunks in make_chunks(playchunk, millisecondchunk*1000):
                self.time += millisecondchunk

                time.sleep(millisecondchunk)
                if not self.isplaying:
                    break
                if self.time >= start+length:
                    break
        else:
            startframe = int(round(start * self.wave_reference.getframerate()))
            samplelen = int(round(length * self.wave_reference.getframerate()))
            remaining = samplelen
            chunk = 1024
            try:
                self.wave_reference.setpos(startframe)
            except wave.Error:
                self.isplaying = False
                return

            if remaining >= 1024:
                data = audioop.mul(self.wave_reference.readframes(chunk),self.wave_reference.getsampwidth(), self.volume/100.0)
                remaining -= chunk
            else:
                data = audioop.mul(self.wave_reference.readframes(remaining),self.wave_reference.getsampwidth(), self.volume/100.0)
                remaining = 0

            # play stream
            self.audio.play(data.get_array_of_samples(), blocking=False)

            while len(data) > 0 and self.isplaying:

                time.sleep(float(self.wave_reference.getframerate()))
                self.time = float(self.wave_reference.tell()) / float(self.wave_reference.getframerate())
                if remaining >= 1024:
                    data = audioop.mul(self.wave_reference.readframes(chunk),self.wave_reference.getsampwidth(), self.volume/100.0)
                    remaining -= chunk
                else:
                    data = audioop.mul(self.wave_reference.readframes(remaining),self.wave_reference.getsampwidth(), self.volume/100.0)
                    remaining = 0

        self.audio.stop()
        self.isplaying = False

    def play(self, arg):
        thread.start_new_thread(self._play, (0, self.Duration()))

    def play_segment(self, start, length):
        if not self.isplaying:  # otherwise this get's kinda echo-y
            thread.start_new_thread(self._play, (start, length))
