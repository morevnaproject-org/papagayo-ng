# This file was created automatically by SWIG.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _lm

def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "this"):
        if isinstance(value, class_type):
            self.__dict__[name] = value.this
            if hasattr(value,"thisown"): self.__dict__["thisown"] = value.thisown
            del value.thisown
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name) or (name == "thisown"):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0
del types


try:
    from weakref import proxy as weakref_proxy
except:
    weakref_proxy = lambda x: x


LM_FIXED_BITS = _lm.LM_FIXED_BITS
class rgb_color(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, rgb_color, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, rgb_color, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ rgb_color instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    __swig_setmethods__["r"] = _lm.rgb_color_r_set
    __swig_getmethods__["r"] = _lm.rgb_color_r_get
    if _newclass:r = property(_lm.rgb_color_r_get, _lm.rgb_color_r_set)
    __swig_setmethods__["g"] = _lm.rgb_color_g_set
    __swig_getmethods__["g"] = _lm.rgb_color_g_get
    if _newclass:g = property(_lm.rgb_color_g_get, _lm.rgb_color_g_set)
    __swig_setmethods__["b"] = _lm.rgb_color_b_set
    __swig_getmethods__["b"] = _lm.rgb_color_b_get
    if _newclass:b = property(_lm.rgb_color_b_get, _lm.rgb_color_b_set)
    __swig_setmethods__["a"] = _lm.rgb_color_a_set
    __swig_getmethods__["a"] = _lm.rgb_color_a_get
    if _newclass:a = property(_lm.rgb_color_a_get, _lm.rgb_color_a_set)
    def __init__(self, *args):
        _swig_setattr(self, rgb_color, 'this', _lm.new_rgb_color(*args))
        _swig_setattr(self, rgb_color, 'thisown', 1)
    def __del__(self, destroy=_lm.delete_rgb_color):
        try:
            if self.thisown: destroy(self)
        except: pass


class rgb_colorPtr(rgb_color):
    def __init__(self, this):
        _swig_setattr(self, rgb_color, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, rgb_color, 'thisown', 0)
        _swig_setattr(self, rgb_color,self.__class__,rgb_color)
_lm.rgb_color_swigregister(rgb_colorPtr)

class hsv_color(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, hsv_color, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, hsv_color, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ hsv_color instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    __swig_setmethods__["h"] = _lm.hsv_color_h_set
    __swig_getmethods__["h"] = _lm.hsv_color_h_get
    if _newclass:h = property(_lm.hsv_color_h_get, _lm.hsv_color_h_set)
    __swig_setmethods__["s"] = _lm.hsv_color_s_set
    __swig_getmethods__["s"] = _lm.hsv_color_s_get
    if _newclass:s = property(_lm.hsv_color_s_get, _lm.hsv_color_s_set)
    __swig_setmethods__["v"] = _lm.hsv_color_v_set
    __swig_getmethods__["v"] = _lm.hsv_color_v_get
    if _newclass:v = property(_lm.hsv_color_v_get, _lm.hsv_color_v_set)
    __swig_setmethods__["a"] = _lm.hsv_color_a_set
    __swig_getmethods__["a"] = _lm.hsv_color_a_get
    if _newclass:a = property(_lm.hsv_color_a_get, _lm.hsv_color_a_set)
    def __init__(self, *args):
        _swig_setattr(self, hsv_color, 'this', _lm.new_hsv_color(*args))
        _swig_setattr(self, hsv_color, 'thisown', 1)
    def __del__(self, destroy=_lm.delete_hsv_color):
        try:
            if self.thisown: destroy(self)
        except: pass


class hsv_colorPtr(hsv_color):
    def __init__(self, this):
        _swig_setattr(self, hsv_color, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, hsv_color, 'thisown', 0)
        _swig_setattr(self, hsv_color,self.__class__,hsv_color)
_lm.hsv_color_swigregister(hsv_colorPtr)


LM_InitAudio = _lm.LM_InitAudio

LM_ExitAudio = _lm.LM_ExitAudio
class LM_SoundPlayer(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, LM_SoundPlayer, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, LM_SoundPlayer, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ LM_SoundPlayer instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, LM_SoundPlayer, 'this', _lm.new_LM_SoundPlayer(*args))
        _swig_setattr(self, LM_SoundPlayer, 'thisown', 1)
    def __del__(self, destroy=_lm.delete_LM_SoundPlayer):
        try:
            if self.thisown: destroy(self)
        except: pass

    def IsValid(*args): return _lm.LM_SoundPlayer_IsValid(*args)
    def Duration(*args): return _lm.LM_SoundPlayer_Duration(*args)
    def Play(*args): return _lm.LM_SoundPlayer_Play(*args)
    def Stop(*args): return _lm.LM_SoundPlayer_Stop(*args)
    def IsPlaying(*args): return _lm.LM_SoundPlayer_IsPlaying(*args)
    def CurrentTime(*args): return _lm.LM_SoundPlayer_CurrentTime(*args)
    def SetCurTime(*args): return _lm.LM_SoundPlayer_SetCurTime(*args)
    def SetRateMultiplier(*args): return _lm.LM_SoundPlayer_SetRateMultiplier(*args)
    def PlaySegment(*args): return _lm.LM_SoundPlayer_PlaySegment(*args)
    def GetAmplitude(*args): return _lm.LM_SoundPlayer_GetAmplitude(*args)
    def GetRMSAmplitude(*args): return _lm.LM_SoundPlayer_GetRMSAmplitude(*args)
    def GetMaxAmplitude(*args): return _lm.LM_SoundPlayer_GetMaxAmplitude(*args)

class LM_SoundPlayerPtr(LM_SoundPlayer):
    def __init__(self, this):
        _swig_setattr(self, LM_SoundPlayer, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, LM_SoundPlayer, 'thisown', 0)
        _swig_setattr(self, LM_SoundPlayer,self.__class__,LM_SoundPlayer)
_lm.LM_SoundPlayer_swigregister(LM_SoundPlayerPtr)

import sys
import os
import imp
import math
import wx
import __main__

__appDir = None

def main_is_frozen():
    return hasattr(sys, "frozen")
    #return (hasattr(sys, "frozen") # new py2exe
    #    or hasattr(sys, "importers") # old py2exe
    #    or imp.is_frozen("__main__")) # tools/freeze

def AppDir():
    global __appDir
    if __appDir is not None:
        return __appDir
    if main_is_frozen():
        if "__WXMAC__" in wx.PlatformInfo:
            __appDir = os.path.dirname(os.path.abspath(__main__.__file__ + "/../../.."))
        else:
            __appDir = os.path.dirname(sys.executable)
    else:
        __appDir = os.path.dirname(os.path.abspath(__main__.__file__))
    return __appDir
    #return os.path.dirname(sys.argv[0])

def Round(a):
    if a > 0:
        return math.floor(a + 0.5)
    else:
        return -math.floor(0.5 - a)

def RsrcBMP(path):
    return wx.Bitmap(os.path.join(AppDir(), "rsrc/%s" % path), wx.BITMAP_TYPE_ANY)


