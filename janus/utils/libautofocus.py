from ctypes import cdll
import ctypes


class init_options(ctypes.Structure):
    _fields_ = [("tangoVimbaCamera", ctypes.c_char_p),
                ("tangoFocusAxis", ctypes.c_char_p)]


class focus_options(ctypes.Structure):
    _fields_ = [("signalTreshold", ctypes.c_float),
                ("goalTreshold", ctypes.c_float),
                ("delayFrames", ctypes.c_int32)]


done_callback_type = ctypes.CFUNCTYPE(None)
error_callback_type = ctypes.CFUNCTYPE(None, ctypes.c_int32, ctypes.c_char_p, ctypes.c_void_p)


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@singleton
class LibAutofocusImporter:

    def wrap_function(self, lib, name, arg_types, ret_types):
        fct = lib.__getattr__(name)
        fct.argtypes = arg_types
        fct.restype = ret_types
        return fct

    def libaf_error_callback(self, error_code, error_message, object):
        print("libaf error callback '{}', '{}', '{}'".format(error_code, error_message, object))

    def __init__(self):
        lib = cdll.LoadLibrary('../cmake-build-debug/libautofocus.so')
        self.init = self.wrap_function(lib, "InitializeAutofocus", [init_options], ctypes.c_void_p)
        self.start_focus = self.wrap_function(lib, "StartAutofocus", [ctypes.c_void_p, focus_options], None)
        self.stop_focus = self.wrap_function(lib, "StopAutofocus", [ctypes.c_void_p], None)
        self.set_focus_callback = self.wrap_function(lib, "SetFocusDoneCallback", [ctypes.c_void_p], done_callback_type)
        self.is_focus_running = self.wrap_function(lib, "IsFocusRunning", [ctypes.c_void_p], ctypes.c_bool)
        self.shutdown = self.wrap_function(lib, "Shutdown", [ctypes.c_void_p], None)
        set_libaf_error_cb = self.wrap_function(lib, "SetErrorCallback", [error_callback_type], None)

        errorCb = error_callback_type(self.libaf_error_callback)
        self.errorCb = errorCb
        set_libaf_error_cb(errorCb)


class LibAutofocusWrapper:
    def __init__(self):
        self.afObject = None
        self.cbRefHelper = None
        self.af = LibAutofocusImporter()

    def __del__(self):
        if self.afObject:
            self.Shutdown()
        pass

    def Init(self, vimbaCamera, focusAxis):
        if self.afObject:
            print("libaf already initialized")
            return
        options = init_options()
        options.tangoVimbaCamera = vimbaCamera.encode('utf-8')
        options.tangoFocusAxis = focusAxis.encode('utf-8')
        self.afObject = self.af.init(options)
        pass

    def SetFocusFinishedCallback(self, cb):
        if not self.afObject:
            print("libaf not initialized")
            return
        if cb:
            c_callback = done_callback_type(cb)
            self.cbRefHelper = c_callback
            self.af.set_focus_callback(self.afObject, c_callback)
        else:
            self.af.set_focus_callback(self.afObject, None)
            self.cbRefHelper = None

    def IsFocusRunning(self):
        if not self.afObject:
            print("libaf not initialized")
            return
        isRunning = self.af.is_focus_running(self.afObject)
        return isRunning

    def StartFocus(self, signalTreshold, goalTreshold, delayFrames):
        if not self.afObject:
            print("libaf not initialized")
            return
        options = focus_options()
        options.signalTreshold = signalTreshold
        options.goalTreshold = goalTreshold
        options.delayFrames = delayFrames
        self.af.start_focus(self.afObject, options)

    def StopFocus(self):
        if not self.afObject:
            print("libaf not initialized")
            return
        self.af.stop_focus(self.afObject)
        pass

    def Shutdown(self):
        if not self.afObject:
            print("libaf not initialized")
            return
        self.af.shutdown(self.afObject)
        self.afObject = None
