import wave
import audioop
import sys
import traceback
import pyaudio
import os, platform
from pydub import AudioSegment


try:
    import thread
except ImportError:
    import _thread as thread

class SoundPlayer():
    def __init__(self, soundfile, parent):
        self.soundfile = soundfile
        self.isplaying = False
        self.time = 0 # current audio position in frames
        self.audio = pyaudio.PyAudio()
        if platform.system() == "Windows":
            AudioSegment.converter = os.path.dirname(os.path.realpath(__file__)) + "\\ffmpeg.exe"
        else:
            pass #might do something different for linux or so here

        try:
            tempsound = AudioSegment.from_file(self.soundfile, format = os.path.splitext(self.soundfile)[1][1:])
            tempsound.export(os.path.dirname(os.path.realpath(__file__)) +"\\temp.wav", format = "wav")
            self.wave_reference = wave.open(os.path.dirname(os.path.realpath(__file__)) + "\\temp.wav")
            self.isvalid = True
        
        #try:
            #self.wave_reference = wave.open(self.soundfile)
            #self.isvalid = True
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
        return audioop.rms(frame,width)

    def IsPlaying(self):
        return self.isplaying

    def SetCurTime(self, time):
        self.time = time

    def Stop(self):
        self.isplaying = False

    def CurrentTime(self):
        return self.time

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
        stream = self.audio.open(format =
          self.audio.get_format_from_width(self.wave_reference.getsampwidth()),
          channels = self.wave_reference.getnchannels(),
          rate = self.wave_reference.getframerate(),
          output = True)
        # read data
        
        if remaining >= 1024:
            data = self.wave_reference.readframes(chunk)
            remaining -= chunk
        else:
            data = self.wave_reference.readframes(remaining)
            remaining = 0
        
        # play stream
        while data != '' and self.isplaying==True:
            stream.write(data)
            self.time = float(self.wave_reference.tell()) / float(self.wave_reference.getframerate())
            if remaining >= 1024:
                data = self.wave_reference.readframes(chunk)
                remaining -= chunk
            else:
                data = self.wave_reference.readframes(remaining)
                remaining = 0
            
        stream.close()
        self.isplaying = False
    
    def Play(self, arg):
        thread.start_new_thread(self._play, (0,self.Duration()))

    def PlaySegment(self, start, length, arg):
        thread.start_new_thread(self._play, (start,length))
