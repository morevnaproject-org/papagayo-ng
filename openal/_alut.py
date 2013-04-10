import ctypes
import ctypes.util

lib_path = ctypes.util.find_library('alut')
if lib_path is None:
    raise ImportError('alut library not found')
lib = ctypes.CDLL(lib_path)

ERROR_NO_ERROR = 0
ERROR_OUT_OF_MEMORY = 0x200
ERROR_INVALID_ENUM = 0x201
ERROR_INVALID_VALUE = 0x202
ERROR_INVALID_OPERATION = 0x203
ERROR_NO_CURRENT_CONTEXT = 0x204
ERROR_AL_ERROR_ON_ENTRY = 0x205
ERROR_ALC_ERROR_ON_ENTRY = 0x206
ERROR_OPEN_DEVICE = 0x207
ERROR_CLOSE_DEVICE = 0x208
ERROR_CREATE_CONTEXT = 0x209
ERROR_MAKE_CONTEXT_CURRENT = 0x20A
ERROR_DESTROY_CONTEXT = 0x20B
ERROR_GEN_BUFFERS = 0x20C
ERROR_BUFFER_DATA = 0x20D
ERROR_IO_ERROR = 0x20E
ERROR_UNSUPPORTED_FILE_TYPE = 0x20F
ERROR_UNSUPPORTED_FILE_SUBTYPE = 0x210
ERROR_CORRUPT_OR_TRUNCATED_DATA = 0x211
WAVEFORM_SINE = 0x100
WAVEFORM_SQUARE = 0x101
WAVEFORM_SAWTOOTH = 0x102
WAVEFORM_WHITENOISE = 0x103
WAVEFORM_IMPULSE = 0x104
LOADER_BUFFER = 0x300
LOADER_MEMORY = 0x301

errors = {}
for k, v in locals().items():
    if not isinstance(v, int) or not v: continue
    assert v not in errors
    k = k.replace('_', ' ').lower()
    if not k.startswith('error '): continue
    errors[v] = k[len('error '):]

class ALUTError(Exception):
    pass

def check_error(result, func, arguments):
    err = GetError()
    if err:
        raise ALUTError, errors[err]
    return result

Init = lib.alutInit
Init.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_char_p)]
Init.restype = ctypes.c_uint8
Init.errcheck = check_error

InitWithoutContext = lib.alutInitWithoutContext
InitWithoutContext.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_char_p)]
InitWithoutContext.restype = ctypes.c_uint8
InitWithoutContext.errcheck = check_error

Exit = lib.alutExit
Exit.argtypes = []
Exit.restype = ctypes.c_uint8
Exit.errcheck = check_error

GetError = lib.alutGetError
GetError.argtypes = []
GetError.restype = ctypes.c_int

GetErrorString = lib.alutGetErrorString
GetErrorString.argtypes = [ctypes.c_int]
GetErrorString.restype = ctypes.c_char_p
GetErrorString.errcheck = check_error

CreateBufferFromFile = lib.alutCreateBufferFromFile
CreateBufferFromFile.argtypes = [ctypes.c_char_p]
CreateBufferFromFile.restype = ctypes.c_uint
CreateBufferFromFile.errcheck = check_error

CreateBufferFromFileImage = lib.alutCreateBufferFromFileImage
CreateBufferFromFileImage.argtypes = [ctypes.c_void_p, ctypes.c_int]
CreateBufferFromFileImage.restype = ctypes.c_uint
CreateBufferFromFileImage.errcheck = check_error

CreateBufferHelloWorld = lib.alutCreateBufferHelloWorld
CreateBufferHelloWorld.argtypes = []
CreateBufferHelloWorld.restype = ctypes.c_uint
CreateBufferHelloWorld.errcheck = check_error

CreateBufferWaveform = lib.alutCreateBufferWaveform
CreateBufferWaveform.argtypes = [ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.c_float]
CreateBufferWaveform.restype = ctypes.c_uint
CreateBufferWaveform.errcheck = check_error

LoadMemoryFromFile = lib.alutLoadMemoryFromFile
LoadMemoryFromFile.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_float)]
LoadMemoryFromFile.restype = ctypes.c_void_p
LoadMemoryFromFile.errcheck = check_error

LoadMemoryFromFileImage = lib.alutLoadMemoryFromFileImage
LoadMemoryFromFileImage.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_float)]
LoadMemoryFromFileImage.restype = ctypes.c_void_p
LoadMemoryFromFileImage.errcheck = check_error

LoadMemoryHelloWorld = lib.alutLoadMemoryHelloWorld
LoadMemoryHelloWorld.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_float)]
LoadMemoryHelloWorld.restype = ctypes.c_void_p
LoadMemoryHelloWorld.errcheck = check_error

LoadMemoryWaveform = lib.alutLoadMemoryWaveform
LoadMemoryWaveform.argtypes = [ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_float)]
LoadMemoryWaveform.restype = ctypes.c_void_p
LoadMemoryWaveform.errcheck = check_error

GetMIMETypes = lib.alutGetMIMETypes
GetMIMETypes.argtypes = [ctypes.c_int]
GetMIMETypes.restype = ctypes.c_char_p
GetMIMETypes.errcheck = check_error

GetMajorVersion = lib.alutGetMajorVersion
GetMajorVersion.argtypes = []
GetMajorVersion.restype = ctypes.c_int
GetMajorVersion.errcheck = check_error

GetMinorVersion = lib.alutGetMinorVersion
GetMinorVersion.argtypes = []
GetMinorVersion.restype = ctypes.c_int
GetMinorVersion.errcheck = check_error

Sleep = lib.alutSleep
Sleep.argtypes = [ctypes.c_float]
Sleep.restype = ctypes.c_uint8
Sleep.errcheck = check_error
