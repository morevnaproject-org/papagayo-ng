import ctypes
import ctypes.util

lib_path = ctypes.util.find_library('openal')
if lib_path is None:
    lib_path = ctypes.util.find_library('openal32')
    if lib_path is None:
        raise ImportError('openal library not found')
lib = ctypes.CDLL(lib_path)

ALC_FALSE = 0
ALC_TRUE = 1
ALC_FREQUENCY = 0x1007
ALC_REFRESH = 0x1008
ALC_SYNC = 0x1009
ALC_MONO_SOURCES = 0x1010
ALC_STEREO_SOURCES = 0x1011
ALC_NO_ERROR = ALC_FALSE
ALC_INVALID_DEVICE = 0xA001
ALC_INVALID_CONTEXT = 0xA002
ALC_INVALID_ENUM = 0xA003
ALC_INVALID_VALUE = 0xA004
ALC_OUT_OF_MEMORY = 0xA005
ALC_DEFAULT_DEVICE_SPECIFIER = 0x1004
ALC_DEVICE_SPECIFIER = 0x1005
ALC_EXTENSIONS = 0x1006
ALC_MAJOR_VERSION = 0x1000
ALC_MINOR_VERSION = 0x1001
ALC_ATTRIBUTES_SIZE = 0x1002
ALC_ALL_ATTRIBUTES = 0x1003
ALC_CAPTURE_DEVICE_SPECIFIER = 0x310
ALC_CAPTURE_DEFAULT_DEVICE_SPECIFIER = 0x311
ALC_CAPTURE_SAMPLES = 0x312

errors = {}
for k, v in locals().items():
    if not isinstance(v, int) or not v: continue
    assert v not in errors
    errors[v] = k.replace('_', ' ').lower()

class ALCError(Exception):
    pass

def check_error(result, func, arguments):
    err = GetError(0)
    if err:
        raise ALCError, errors[err]
    return result

CreateContext = lib.alcCreateContext
CreateContext.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
CreateContext.restype = ctypes.c_void_p
CreateContext.errcheck = check_error

MakeContextCurrent = lib.alcMakeContextCurrent
MakeContextCurrent.argtypes = [ctypes.c_void_p]
MakeContextCurrent.restype = ctypes.c_uint8
MakeContextCurrent.errcheck = check_error

ProcessContext = lib.alcProcessContext
ProcessContext.argtypes = [ctypes.c_void_p]
ProcessContext.restype = None
ProcessContext.errcheck = check_error

SuspendContext = lib.alcSuspendContext
SuspendContext.argtypes = [ctypes.c_void_p]
SuspendContext.restype = None
SuspendContext.errcheck = check_error

DestroyContext = lib.alcDestroyContext
DestroyContext.argtypes = [ctypes.c_void_p]
DestroyContext.restype = None
DestroyContext.errcheck = check_error

GetCurrentContext = lib.alcGetCurrentContext
GetCurrentContext.argtypes = []
GetCurrentContext.restype = ctypes.c_void_p
GetCurrentContext.errcheck = check_error

GetContextsDevice = lib.alcGetContextsDevice
GetContextsDevice.argtypes = [ctypes.c_void_p]
GetContextsDevice.restype = ctypes.c_void_p
GetContextsDevice.errcheck = check_error

OpenDevice = lib.alcOpenDevice
OpenDevice.argtypes = [ctypes.c_char_p]
OpenDevice.restype = ctypes.c_void_p
OpenDevice.errcheck = check_error

CloseDevice = lib.alcCloseDevice
CloseDevice.argtypes = [ctypes.c_void_p]
CloseDevice.restype = ctypes.c_uint8
CloseDevice.errcheck = check_error

GetError = lib.alcGetError
GetError.argtypes = [ctypes.c_void_p]
GetError.restype = ctypes.c_int

IsExtensionPresent = lib.alcIsExtensionPresent
IsExtensionPresent.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
IsExtensionPresent.restype = ctypes.c_uint8
IsExtensionPresent.errcheck = check_error

GetProcAddress = lib.alcGetProcAddress
GetProcAddress.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
GetProcAddress.restype = ctypes.c_void_p
GetProcAddress.errcheck = check_error

GetEnumValue = lib.alcGetEnumValue
GetEnumValue.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
GetEnumValue.restype = ctypes.c_int
GetEnumValue.errcheck = check_error

GetString = lib.alcGetString
GetString.argtypes = [ctypes.c_void_p, ctypes.c_int]
GetString.restype = ctypes.c_char_p
GetString.errcheck = check_error

GetIntegerv = lib.alcGetIntegerv
GetIntegerv.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
GetIntegerv.restype = None
GetIntegerv.errcheck = check_error

CaptureOpenDevice = lib.alcCaptureOpenDevice
CaptureOpenDevice.argtypes = [ctypes.c_char_p, ctypes.c_uint, ctypes.c_int, ctypes.c_int]
CaptureOpenDevice.restype = ctypes.c_void_p
CaptureOpenDevice.errcheck = check_error

CaptureCloseDevice = lib.alcCaptureCloseDevice
CaptureCloseDevice.argtypes = [ctypes.c_void_p]
CaptureCloseDevice.restype = ctypes.c_uint8
CaptureCloseDevice.errcheck = check_error

CaptureStart = lib.alcCaptureStart
CaptureStart.argtypes = [ctypes.c_void_p]
CaptureStart.restype = None
CaptureStart.errcheck = check_error

CaptureStop = lib.alcCaptureStop
CaptureStop.argtypes = [ctypes.c_void_p]
CaptureStop.restype = None
CaptureStop.errcheck = check_error

CaptureSamples = lib.alcCaptureSamples
CaptureSamples.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int]
CaptureSamples.restype = None
CaptureSamples.errcheck = check_error
