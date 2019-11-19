'''from ..core import Object
import os
from PyQt5.QtCore import QObject, pyqtSignal
from janus.utils.libautofocus import LibAutofocusWrapper, done_callback_type


class AutofocusController(QObject, Object):

    focus_done = pyqtSignal()

    def __init__(self, tangoVimba, tangoFoxusAxis):
        QObject.__init__(self)
        Object.__init__(self)
        self.libaf = LibAutofocusWrapper("../../../lib/libautofocus.so")
        self.libaf.Init(tangoVimba, tangoFoxusAxis)
        self.libaf.SetFocusFinishedCallback(self._focusDone)

    def __del__(self):
        self.libaf.Shutdown()
        pass

    def _focusDone(self):
        self.focus_done.emit();

    def start_autofocus(self, signalTreshold, goalTreshold, delayFrames):
        self.libaf.StartFocus(signalTreshold, goalTreshold, delayFrames)

    def stop_autofocus(self):
        self.libaf.StopFocus()

    def is_focusing(self):
        self.libaf.IsFocusRunning()
        pass'''
