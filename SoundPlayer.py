import wave
import audioop
import sys
import traceback
import openal
import thread
import Singleton

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class SoundPlayer():
    __metaclass__ = Singleton
    
    def __init__(self):
        self.device = openal.Device()
        self.contextlistener = self.device.ContextListener()
        self.contextlistener.position = 0, 0, 0
        self.contextlistener.velocity = 0, 0, 0
        self.contextlistener.orientation = 0, 1, 0, 0, 0, 1
    
    def initialize(self, soundfile, parent):
        self.soundfile = soundfile
        self.isplaying = False
        self.time = 0 # current audio position in frames
        self.source = self.contextlistener.get_source()
        self.source.buffer = openal.Buffer(self.soundfile)
        self.source.looping = False
        self.source.gain = .5
        self.source.position = 3, 3, -3
        
        try:
            self.wave_reference = wave.open(self.soundfile)
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
        self.source.pause()
#        if self.source.state != openal._al.INITIAL:
#            try:
#                self.source.rewindy()
#            except:
#                traceback.print_exc()
#                print dir(self.source)
        self.source.play()
        try:
            if start > self.Duration():
                start = self.Duration()
            elif start < 0:
                start = 0
            self.source.sec_offset = start
        except:
            print start
            print length
            print self.source.sec_offset
            return        
        self.isplaying = True
        while self.source.state == openal._al.PLAYING and self.isplaying == True and self.source.sec_offset <= (start + length):
            self.time = self.source.sec_offset
        self.source.stop()
        self.isplaying = False
    
    def Play(self, arg):
        thread.start_new_thread(self._play, (0,self.Duration()))

    def PlaySegment(self, start, length, arg):
        thread.start_new_thread(self._play, (start,length))
