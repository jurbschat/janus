'''
Created on May 8, 2019

@author: janmeyer
'''

import sys
import logging
from PyQt5.QtCore import QObject, pyqtSignal

initialized = False
stderr_handler = None
stdout_handler = None
root_logger = None


def __init__():
    global initialized
    global stderr_handler
    global root_logger
    root_logger = logging.getLogger()
    root_logger.setLevel(0)
    if root_logger.hasHandlers():
        stderr_handler = root_logger.handlers[0]
    initialized = True


def Logger():
    global initialized
    global root_logger
    if (not "initialized" in globals() or not initialized):
        __init__()
    return root_logger


def StderrHandler():
    global initialized
    global stderr_handler
    if (not "initialized" in globals() or not initialized):
        __init__()
    if stderr_handler is None:
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.ERROR)
    return stderr_handler


def StdoutHandler():
    global stdout_handler
    if stdout_handler is None:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.INFO)
    return stdout_handler


def LogFormater():
    return logging.Formatter("%(asctime)-15s %(levelname)-8s %(message)s")


class LogHandler(QObject, logging.Handler):

    value_changed = pyqtSignal(object, name="valueChanged")

    def __init__(self, view_level=0):
        QObject.__init__(self)
        logging.Handler.__init__(self)
        self.view_level = view_level
        self.buffer = []
        self.text = ""
        self.setFormatter(LogFormater())

    def set_view_level(self, level):
        if level != self.view_level:
            self.view_level = level
            self._compile_text()

    def emit(self, record):
        """
        Emit a record.
        If a formatter is specified, it is used to format the record.
        The record is then written to the stream with a trailing newline.  If
        exception information is present, it is formatted using
        traceback.print_exception and appended to the stream.  If the stream
        has an 'encoding' attribute, it is used to determine how to do the
        output to the stream.
        """
        try:
            msg = self.format(record)
            level = record.levelno
            self.acquire()
            self.buffer.append((level, msg))
            if level >= self.view_level:
                self.text += msg + "\n"
            self.release()
            if level >= self.view_level:
                self.value_changed.emit(msg)
        except RecursionError:  # See issue 36272
            raise
        except Exception:
            self.handleError(record)

    def close(self):
        """
        Tidy up any resources used by the handler.
        """
        self.acquire()
        self.buffer = []
        self.text = ""
        self.release()
        logging.Handler.close(self)

    def _compile_text(self):
        self.acquire()
        self.text = ""
        for (level, msg) in self.buffer:
            if level >= self.view_level:
                self.text += msg + "\n"
        self.text = self.text[:-1]
        self.release()
        self.value_changed.emit(None)
