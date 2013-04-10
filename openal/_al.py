import ctypes
import ctypes.util

lib_path = ctypes.util.find_library('openal')
if lib_path is None:
    raise ImportError('openal library not found')
lib = ctypes.CDLL(lib_path)

NONE = 0
FALSE = 0
TRUE = 1
SOURCE_RELATIVE = 0x202
CONE_INNER_ANGLE = 0x1001
CONE_OUTER_ANGLE = 0x1002
PITCH = 0x1003
POSITION = 0x1004
DIRECTION = 0x1005
VELOCITY = 0x1006
LOOPING = 0x1007
BUFFER = 0x1009
GAIN = 0x100A
MIN_GAIN = 0x100D
MAX_GAIN = 0x100E
ORIENTATION = 0x100F
SOURCE_STATE = 0x1010
INITIAL = 0x1011
PLAYING = 0x1012
PAUSED = 0x1013
STOPPED = 0x1014
BUFFERS_QUEUED = 0x1015
BUFFERS_PROCESSED = 0x1016
SEC_OFFSET = 0x1024
SAMPLE_OFFSET = 0x1025
BYTE_OFFSET = 0x1026
SOURCE_TYPE = 0x1027
STATIC = 0x1028
STREAMING = 0x1029
UNDETERMINED = 0x1030
FORMAT_MONO8 = 0x1100
FORMAT_MONO16 = 0x1101
FORMAT_STEREO8 = 0x1102
FORMAT_STEREO16 = 0x1103
REFERENCE_DISTANCE = 0x1020
ROLLOFF_FACTOR = 0x1021
CONE_OUTER_GAIN = 0x1022
MAX_DISTANCE = 0x1023
FREQUENCY = 0x2001
BITS = 0x2002
CHANNELS = 0x2003
SIZE = 0x2004
UNUSED = 0x2010
PENDING = 0x2011
PROCESSED = 0x2012
NO_ERROR = FALSE
INVALID_NAME = 0xA001
INVALID_ENUM = 0xA002
INVALID_VALUE = 0xA003
INVALID_OPERATION = 0xA004
OUT_OF_MEMORY = 0xA005
VENDOR = 0xB001
VERSION = 0xB002
RENDERER = 0xB003
EXTENSIONS = 0xB004
DOPPLER_FACTOR = 0xC000
DOPPLER_VELOCITY = 0xC001
SPEED_OF_SOUND = 0xC003
DISTANCE_MODEL = 0xD000
INVERSE_DISTANCE = 0xD001
INVERSE_DISTANCE_CLAMPED = 0xD002
LINEAR_DISTANCE = 0xD003
LINEAR_DISTANCE_CLAMPED = 0xD004
EXPONENT_DISTANCE = 0xD005
EXPONENT_DISTANCE_CLAMPED = 0xD006

errors = {}
for k, v in locals().items():
    if not isinstance(v, int) or not v: continue
    assert v not in errors
    errors[v] = k.replace('_', ' ').lower()

class ALError(Exception):
    pass

def check_error(result, func, arguments):
    err = GetError()
    if err:
        raise ALError, errors[err]
    return result

Enable = lib.alEnable
Enable.argtypes = [ctypes.c_int]
Enable.restype = None
Enable.errcheck = check_error

Disable = lib.alDisable
Disable.argtypes = [ctypes.c_int]
Disable.restype = None
Disable.errcheck = check_error

IsEnabled = lib.alIsEnabled
IsEnabled.argtypes = [ctypes.c_int]
IsEnabled.restype = ctypes.c_uint8
IsEnabled.errcheck = check_error

GetString = lib.alGetString
GetString.argtypes = [ctypes.c_int]
GetString.restype = ctypes.c_char_p
GetString.errcheck = check_error

GetBooleanv = lib.alGetBooleanv
GetBooleanv.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_uint8)]
GetBooleanv.restype = None
GetBooleanv.errcheck = check_error

GetIntegerv = lib.alGetIntegerv
GetIntegerv.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
GetIntegerv.restype = None
GetIntegerv.errcheck = check_error

GetFloatv = lib.alGetFloatv
GetFloatv.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float)]
GetFloatv.restype = None
GetFloatv.errcheck = check_error

GetDoublev = lib.alGetDoublev
GetDoublev.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
GetDoublev.restype = None
GetDoublev.errcheck = check_error

GetBoolean = lib.alGetBoolean
GetBoolean.argtypes = [ctypes.c_int]
GetBoolean.restype = ctypes.c_uint8
GetBoolean.errcheck = check_error

GetInteger = lib.alGetInteger
GetInteger.argtypes = [ctypes.c_int]
GetInteger.restype = ctypes.c_int
GetInteger.errcheck = check_error

GetFloat = lib.alGetFloat
GetFloat.argtypes = [ctypes.c_int]
GetFloat.restype = ctypes.c_float
GetFloat.errcheck = check_error

GetDouble = lib.alGetDouble
GetDouble.argtypes = [ctypes.c_int]
GetDouble.restype = ctypes.c_double
GetDouble.errcheck = check_error

GetError = lib.alGetError
GetError.argtypes = []
GetError.restype = ctypes.c_int

IsExtensionPresent = lib.alIsExtensionPresent
IsExtensionPresent.argtypes = [ctypes.c_char_p]
IsExtensionPresent.restype = ctypes.c_uint8
IsExtensionPresent.errcheck = check_error

GetProcAddress = lib.alGetProcAddress
GetProcAddress.argtypes = [ctypes.c_char_p]
GetProcAddress.restype = ctypes.c_void_p
GetProcAddress.errcheck = check_error

GetEnumValue = lib.alGetEnumValue
GetEnumValue.argtypes = [ctypes.c_char_p]
GetEnumValue.restype = ctypes.c_int
GetEnumValue.errcheck = check_error

Listenerf = lib.alListenerf
Listenerf.argtypes = [ctypes.c_int, ctypes.c_float]
Listenerf.restype = None
Listenerf.errcheck = check_error

Listener3f = lib.alListener3f
Listener3f.argtypes = [ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.c_float]
Listener3f.restype = None
Listener3f.errcheck = check_error

Listenerfv = lib.alListenerfv
Listenerfv.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float)]
Listenerfv.restype = None
Listenerfv.errcheck = check_error

Listeneri = lib.alListeneri
Listeneri.argtypes = [ctypes.c_int, ctypes.c_int]
Listeneri.restype = None
Listeneri.errcheck = check_error

Listener3i = lib.alListener3i
Listener3i.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
Listener3i.restype = None
Listener3i.errcheck = check_error

Listeneriv = lib.alListeneriv
Listeneriv.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
Listeneriv.restype = None
Listeneriv.errcheck = check_error

GetListenerf = lib.alGetListenerf
GetListenerf.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float)]
GetListenerf.restype = None
GetListenerf.errcheck = check_error

GetListener3f = lib.alGetListener3f
GetListener3f.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)]
GetListener3f.restype = None
GetListener3f.errcheck = check_error

GetListenerfv = lib.alGetListenerfv
GetListenerfv.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float)]
GetListenerfv.restype = None
GetListenerfv.errcheck = check_error

GetListeneri = lib.alGetListeneri
GetListeneri.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
GetListeneri.restype = None
GetListeneri.errcheck = check_error

GetListener3i = lib.alGetListener3i
GetListener3i.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
GetListener3i.restype = None
GetListener3i.errcheck = check_error

GetListeneriv = lib.alGetListeneriv
GetListeneriv.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
GetListeneriv.restype = None
GetListeneriv.errcheck = check_error

GenSources = lib.alGenSources
GenSources.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_uint)]
GenSources.restype = None
GenSources.errcheck = check_error

DeleteSources = lib.alDeleteSources
DeleteSources.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_uint)]
DeleteSources.restype = None
DeleteSources.errcheck = check_error

IsSource = lib.alIsSource
IsSource.argtypes = [ctypes.c_uint]
IsSource.restype = ctypes.c_uint8
IsSource.errcheck = check_error

Sourcef = lib.alSourcef
Sourcef.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.c_float]
Sourcef.restype = None
Sourcef.errcheck = check_error

Source3f = lib.alSource3f
Source3f.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.c_float]
Source3f.restype = None
Source3f.errcheck = check_error

Sourcefv = lib.alSourcefv
Sourcefv.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_float)]
Sourcefv.restype = None
Sourcefv.errcheck = check_error

Sourcei = lib.alSourcei
Sourcei.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.c_int]
Sourcei.restype = None
Sourcei.errcheck = check_error

Source3i = lib.alSource3i
Source3i.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
Source3i.restype = None
Source3i.errcheck = check_error

Sourceiv = lib.alSourceiv
Sourceiv.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
Sourceiv.restype = None
Sourceiv.errcheck = check_error

GetSourcef = lib.alGetSourcef
GetSourcef.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_float)]
GetSourcef.restype = None
GetSourcef.errcheck = check_error

GetSource3f = lib.alGetSource3f
GetSource3f.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)]
GetSource3f.restype = None
GetSource3f.errcheck = check_error

GetSourcefv = lib.alGetSourcefv
GetSourcefv.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_float)]
GetSourcefv.restype = None
GetSourcefv.errcheck = check_error

GetSourcei = lib.alGetSourcei
GetSourcei.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
GetSourcei.restype = None
GetSourcei.errcheck = check_error

GetSource3i = lib.alGetSource3i
GetSource3i.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
GetSource3i.restype = None
GetSource3i.errcheck = check_error

GetSourceiv = lib.alGetSourceiv
GetSourceiv.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
GetSourceiv.restype = None
GetSourceiv.errcheck = check_error

SourcePlayv = lib.alSourcePlayv
SourcePlayv.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_uint)]
SourcePlayv.restype = None
SourcePlayv.errcheck = check_error

SourceStopv = lib.alSourceStopv
SourceStopv.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_uint)]
SourceStopv.restype = None
SourceStopv.errcheck = check_error

SourceRewindv = lib.alSourceRewindv
SourceRewindv.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_uint)]
SourceRewindv.restype = None
SourceRewindv.errcheck = check_error

SourcePausev = lib.alSourcePausev
SourcePausev.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_uint)]
SourcePausev.restype = None
SourcePausev.errcheck = check_error

SourcePlay = lib.alSourcePlay
SourcePlay.argtypes = [ctypes.c_uint]
SourcePlay.restype = None
SourcePlay.errcheck = check_error

SourceStop = lib.alSourceStop
SourceStop.argtypes = [ctypes.c_uint]
SourceStop.restype = None
SourceStop.errcheck = check_error

SourceRewind = lib.alSourceRewind
SourceRewind.argtypes = [ctypes.c_uint]
SourceRewind.restype = None
SourceRewind.errcheck = check_error

SourcePause = lib.alSourcePause
SourcePause.argtypes = [ctypes.c_uint]
SourcePause.restype = None
SourcePause.errcheck = check_error

SourceQueueBuffers = lib.alSourceQueueBuffers
SourceQueueBuffers.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_uint)]
SourceQueueBuffers.restype = None
SourceQueueBuffers.errcheck = check_error

SourceUnqueueBuffers = lib.alSourceUnqueueBuffers
SourceUnqueueBuffers.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_uint)]
SourceUnqueueBuffers.restype = None
SourceUnqueueBuffers.errcheck = check_error

GenBuffers = lib.alGenBuffers
GenBuffers.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_uint)]
GenBuffers.restype = None
GenBuffers.errcheck = check_error

DeleteBuffers = lib.alDeleteBuffers
DeleteBuffers.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_uint)]
DeleteBuffers.restype = None
DeleteBuffers.errcheck = check_error

IsBuffer = lib.alIsBuffer
IsBuffer.argtypes = [ctypes.c_uint]
IsBuffer.restype = ctypes.c_uint8
IsBuffer.errcheck = check_error

BufferData = lib.alBufferData
BufferData.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
BufferData.restype = None
BufferData.errcheck = check_error

Bufferf = lib.alBufferf
Bufferf.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.c_float]
Bufferf.restype = None
Bufferf.errcheck = check_error

Buffer3f = lib.alBuffer3f
Buffer3f.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.c_float]
Buffer3f.restype = None
Buffer3f.errcheck = check_error

Bufferfv = lib.alBufferfv
Bufferfv.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_float)]
Bufferfv.restype = None
Bufferfv.errcheck = check_error

Bufferi = lib.alBufferi
Bufferi.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.c_int]
Bufferi.restype = None
Bufferi.errcheck = check_error

Buffer3i = lib.alBuffer3i
Buffer3i.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
Buffer3i.restype = None
Buffer3i.errcheck = check_error

Bufferiv = lib.alBufferiv
Bufferiv.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
Bufferiv.restype = None
Bufferiv.errcheck = check_error

GetBufferf = lib.alGetBufferf
GetBufferf.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_float)]
GetBufferf.restype = None
GetBufferf.errcheck = check_error

GetBuffer3f = lib.alGetBuffer3f
GetBuffer3f.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)]
GetBuffer3f.restype = None
GetBuffer3f.errcheck = check_error

GetBufferfv = lib.alGetBufferfv
GetBufferfv.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_float)]
GetBufferfv.restype = None
GetBufferfv.errcheck = check_error

GetBufferi = lib.alGetBufferi
GetBufferi.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
GetBufferi.restype = None
GetBufferi.errcheck = check_error

GetBuffer3i = lib.alGetBuffer3i
GetBuffer3i.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
GetBuffer3i.restype = None
GetBuffer3i.errcheck = check_error

GetBufferiv = lib.alGetBufferiv
GetBufferiv.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
GetBufferiv.restype = None
GetBufferiv.errcheck = check_error

DopplerFactor = lib.alDopplerFactor
DopplerFactor.argtypes = [ctypes.c_float]
DopplerFactor.restype = None
DopplerFactor.errcheck = check_error

DopplerVelocity = lib.alDopplerVelocity
DopplerVelocity.argtypes = [ctypes.c_float]
DopplerVelocity.restype = None
DopplerVelocity.errcheck = check_error

SpeedOfSound = lib.alSpeedOfSound
SpeedOfSound.argtypes = [ctypes.c_float]
SpeedOfSound.restype = None
SpeedOfSound.errcheck = check_error

DistanceModel = lib.alDistanceModel
DistanceModel.argtypes = [ctypes.c_int]
DistanceModel.restype = None
DistanceModel.errcheck = check_error
