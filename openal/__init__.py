import ctypes
import weakref

from . import _al
from . import _alc
from . import _alut

_refs = {}
def call_on_del(obj, func, *args, **kwargs):
    x = max(_refs.iterkeys()) + 1 if _refs else 0
    _refs[x] = weakref.ref(obj, lambda ref: (_refs.pop(x), func(*args, **kwargs)))

def call_array_fill(atype, contents, func, *args):
    x = (atype * len(contents))()
    for k, v in enumerate(contents):
        x[k] = v
    func(*list(args)+[x])

def call_array(atype, count, func, *args):
    x = (atype * count)()
    func(*list(args)+[x])
    return [x[y] for y in xrange(count)]

class _NoSetAttr(object):
    def __setattr__(self, key, value):
        if key[0] != '_' and not hasattr(self, key):
            raise AttributeError(key)
        object.__setattr__(self, key, value)

class Device(_NoSetAttr):
    def __init__(self, name=None):
        #print repr(_alc.GetString(0, _alc.ALC_DEVICE_SPECIFIER))
        self._handle = _alc.OpenDevice(name)
        assert self._handle
        call_on_del(self, _alc.CloseDevice, self._handle)
    
    def ContextListener(self, *args, **kwargs):
        return ContextListener(self, *args, **kwargs)

class ContextListener(_NoSetAttr):
    def __init__(self, device, frequency=None, refresh=None, sync=None, mono_sources=None, stereo_sources=None):
        self._device = device
        self._handle = _alc.CreateContext(self._device._handle, None) # XXX
        assert self._handle
        _alc.MakeContextCurrent(self._handle)
        
        handle = self._handle
        call_on_del(self, lambda: (_alc.MakeContextCurrent(None), _alc.DestroyContext(handle)))
    
    def get_source(self):
        return Source(self)
    
    def process(self):
        _alc.ProcessContext(self._handle)
    def suspend(self):
        _alc.SuspendContext(self._handle)
    
    def enable(self, target):
        _al.Enable(self._handle, target)
    def disable(self, target):
        _al.Disable(self._handle, target)
    def is_enabled(self, target):
        return _al.IsEnabled(self._handle, target)
    
    device = property(
        lambda self: self._device,
    )
    
    doppler_factor = property(
        lambda self: _al.GetFloat(_al.DOPPLER_FACTOR),
        lambda self, v: _al.DopplerFactor(v),
        doc="Get/set doppler_factor. Default 1.0.",
    )
    speed_of_sound = property(
        lambda self: _al.GetFloat(_al.SPEED_OF_SOUND),
        lambda self, v: _al.SpeedOfSound(v),
        doc="Get/set speed_of_sound. Default 343.3.",
    )
    distance_model = property(
        lambda self: _al.GetInteger(_al.DISTANCE_MODEL),
        lambda self, v: _al.DistanceModel(v),
    )
    version = property(
        lambda self: _al.GetString(_al.VERSION),
    )
    renderer = property(
        lambda self: _al.GetString(_al.RENDERER),
    )
    vendor = property(
        lambda self: _al.GetString(_al.VENDOR),
    )
    extensions = property(
        lambda self: _al.GetString(_al.EXTENSIONS).split(' '),
    )
    
    position = property(
        lambda self: call_array(ctypes.c_float, 3, _al.GetListenerfv, _al.POSITION),
        lambda self, v: call_array_fill(ctypes.c_float, v, _al.Listenerfv, _al.POSITION),
    )
    velocity = property(
        lambda self: call_array(ctypes.c_float, 3, _al.GetListenerfv, _al.VELOCITY),
        lambda self, v: call_array_fill(ctypes.c_float, v, _al.Listenerfv, _al.VELOCITY),
    )
    gain = property(
        lambda self: call_array(ctypes.c_float, 1, _al.GetListenerf, _al.GAIN)[0],
        lambda self, v: _al.Listenerf(_al.GAIN, v),
    )
    
    orientation = property(
        lambda self: call_array(ctypes.c_float, 6, _al.GetListenerfv, _al.ORIENTATION),
        lambda self, v: call_array_fill(ctypes.c_float, v, _al.Listenerfv, _al.ORIENTATION),
        doc='forward, up',
    )

class Source(_NoSetAttr):
    def __init__(self, cl):
        self._cl = cl
        self._buffer = None
        
        self._handle, = call_array(ctypes.c_uint, 1, _al.GenSources, 1)
        call_on_del(self, call_array_fill, ctypes.c_uint, [self._handle], _al.DeleteSources, 1)
    
    def queue_buffers(self, buffers):
        raise NotImplementedError
    def unqueue_buffers(self, buffers):
        raise NotImplementedError
    def play(self):
        _al.SourcePlay(self._handle)
    def pause(self):
        _al.SourcePause(self._handle)
    def stop(self):
        _al.SourceStop(self._handle)
    def rewindy(self):
        _al.SourceRewind(self._handle)
    
    position = property(
        lambda self: call_array(ctypes.c_float, 3, _al.GetSourcefv, self._handle, _al.POSITION),
        lambda self, v: call_array_fill(ctypes.c_float, v, _al.Sourcefv, self._handle, _al.POSITION),
    )
    velocity = property(
        lambda self: call_array(ctypes.c_float, 3, _al.GetSourcefv, self._handle, _al.VELOCITY),
        lambda self, v: call_array_fill(ctypes.c_float, v, _al.Sourcefv, self._handle, _al.VELOCITY),
    )
    gain = property(
        lambda self: call_array(ctypes.c_float, 1, _al.GetSourcef, self._handle, _al.GAIN)[0],
        lambda self, v: _al.Sourcef(self._handle, _al.GAIN, v),
    )
    
    relative = property(
        lambda self: call_array(ctypes.c_int, 1, _al.GetSourcei, self._handle, _al.SOURCE_RELATIVE)[0],
        lambda self, v: _al.Sourcei(self._handle, _al.SOURCE_RELATIVE, v),
    )
    type = property(
        lambda self: call_array(ctypes.c_int, 1, _al.GetSourcei, self._handle, _al.SOURCE_TYPE)[0],
        lambda self, v: _al.Sourcei(self._handle, _al.SOURCE_TYPE, v),
    )
    looping = property(
        lambda self: call_array(ctypes.c_int, 1, _al.GetSourcei, self._handle, _al.LOOPING)[0],
        lambda self, v: _al.Sourcei(self._handle, _al.LOOPING, v),
    )
    
    def _get_buffer(self):
        return self._buffer
    def _set_buffer(self, v):
        _al.Sourcei(self._handle, _al.BUFFER, _al.NONE if v is None else v._handle)
        self._buffer = v
    buffer = property(_get_buffer, _set_buffer)
    
    buffers_queued = property(
        lambda self: call_array(ctypes.c_int, 1, _al.GetSourcei, self._handle, _al.BUFFERS_QUEUED)[0],
    )
    buffers_processed = property(
        lambda self: call_array(ctypes.c_int, 1, _al.GetSourcei, self._handle, _al.BUFFERS_PROCESSED)[0],
    )
    min_gain = property(
        lambda self: call_array(ctypes.c_float, 1, _al.GetSourcef, self._handle, _al.MIN_GAIN)[0],
        lambda self, v: _al.Sourcef(self._handle, _al.MIN_GAIN, v),
    )
    reference_distance = property(
        lambda self: call_array(ctypes.c_float, 1, _al.GetSourcef, self._handle, _al.REFERENCE_DISTANCE)[0],
        lambda self, v: _al.Sourcef(self._handle, _al.REFERENCE_DISTANCE, v),
    )
    rolloff_factor = property(
        lambda self: call_array(ctypes.c_float, 1, _al.GetSourcef, self._handle, _al.ROLLOFF_FACTOR)[0],
        lambda self, v: _al.Sourcef(self._handle, _al.ROLLOFF_FACTOR, v),
    )
    max_distance = property(
        lambda self: call_array(ctypes.c_float, 1, _al.GetSourcef, self._handle, _al.MAX_DISTANCE)[0],
        lambda self, v: _al.Sourcef(self._handle, _al.MAX_DISTANCE, v),
    )
    pitch = property(
        lambda self: call_array(ctypes.c_float, 1, _al.GetSourcef, self._handle, _al.PITCH)[0],
        lambda self, v: _al.Sourcef(self._handle, _al.PITCH, v),
    )
    direction = property(
        lambda self: call_array(ctypes.c_float, 3, _al.GetSourcefv, self._handle, _al.DIRECTION),
        lambda self, v: call_array_fill(ctypes.c_float, v, _al.Sourcefv, self._handle, _al.DIRECTION),
    )
    cone_inner_angle = property(
        lambda self: call_array(ctypes.c_float, 1, _al.GetSourcef, self._handle, _al.CONE_INNER_ANGLE)[0],
        lambda self, v: _al.Sourcef(self._handle, _al.CONE_INNER_ANGLE, v),
    )
    cone_outer_angle = property(
        lambda self: call_array(ctypes.c_float, 1, _al.GetSourcef, self._handle, _al.CONE_OUTER_ANGLE)[0],
        lambda self, v: _al.Sourcef(self._handle, _al.CONE_OUTER_ANGLE, v),
    )
    sec_offset = property(
        lambda self: call_array(ctypes.c_float, 1, _al.GetSourcef, self._handle, _al.SEC_OFFSET)[0],
        lambda self, v: _al.Sourcef(self._handle, _al.SEC_OFFSET, v),
    )
    sample_offset = property(
        lambda self: call_array(ctypes.c_float, 1, _al.GetSourcef,self._handle, _al.SAMPLE_OFFSET)[0],
        lambda self, v: _al.Sourcef(self._handle, _al.SAMPLE_OFFSET, v),
    )
    byte_offset = property(
        lambda self: call_array(ctypes.c_float, 1, _al.GetSourcef, self._handle, _al.BYTE_OFFSET)[0],
        lambda self, v: _al.Sourcef(self._handle, _al.BYTE_OFFSET, v),
    )
    state = property(
        lambda self: call_array(ctypes.c_int, 1, _al.GetSourcei, self._handle, _al.SOURCE_STATE)[0],
        lambda self, v: _al.Sourcei(self._handle, _al.SOURCE_STATE, v),
    )

class Buffer(_NoSetAttr):
    def __init__(self, filename=None, data=None, rawdata=None):
        assert (filename is not None) + (data is not None) + (rawdata is not None) == 1
        
        if filename is not None:
            self._handle = _alut.CreateBufferFromFile(filename)
        elif data is not None:
            self._handle = _alut.CreateBufferFromFileImage(data, len(data))
        else:
            channels, bits, frequency, data2 = rawdata
            format = {
                (1, 8): _al.FORMAT_MONO8,
                (1, 16): _al.FORMAT_MONO16,
                (2, 8): _al.FORMAT_STEREO8,
                (2, 16): _al.FORMAT_STEREO16,
            }[channels, bits]
            self._handle, = call_array(ctypes.c_uint, 1, _al.GenBuffers, 1)
            _al.BufferData(self._handle, format, data2, len(data2), frequency)
        
        call_on_del(self, call_array_fill, ctypes.c_uint, [self._handle], _al.DeleteBuffers, 1)
    
    frequency = property(
        lambda self: call_array(ctypes.c_int, 1, _al.GetBufferi, self._handle, _al.FREQUENCY)[0],
    )
    size = property(
        lambda self: call_array(ctypes.c_int, 1, _al.GetBufferi, self._handle, _al.SIZE)[0],
    )
    bits = property(
        lambda self: call_array(ctypes.c_int, 1, _al.GetBufferi, self._handle, _al.BITS)[0],
    )
    channels = property(
        lambda self: call_array(ctypes.c_int, 1, _al.GetBufferi, self._handle, _al.CHANNELS)[0],
    )

_alut.InitWithoutContext(None, None)
