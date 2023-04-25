import imp
import os
import platform
import sys
import traceback
import appdirs
import logging

from PySide2 import QtCore, QtGui

original_colors = {"wave_fill_color": QtGui.QColor(162, 205, 242),
                   "wave_line_color": QtGui.QColor(30, 121, 198),
                   "frame_color": QtGui.QColor(192, 192, 192),
                   "frame_text_color": QtGui.QColor(64, 64, 64),
                   "playback_fill_color": QtGui.QColor(209, 102, 121),
                   "playback_line_color": QtGui.QColor(128, 0, 0),
                   "phrase_fill_color": QtGui.QColor(205, 242, 162),
                   "phrase_line_color": QtGui.QColor(121, 198, 30),
                   "word_fill_color": QtGui.QColor(242, 205, 162),
                   "word_line_color": QtGui.QColor(198, 121, 30),
                   "phoneme_fill_color": QtGui.QColor(231, 185, 210),
                   "phoneme_line_color": QtGui.QColor(173, 114, 146),
                   "bg_fill_color": QtGui.QColor(255, 255, 255)}


def main_is_frozen():
    return (hasattr(sys, "frozen") or  # new py2exe
            hasattr(sys, "importers") or  # old py2exe
            imp.is_frozen("__main__"))  # tools/freeze


def get_main_dir():
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        if sys._MEIPASS:
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.abspath(".")
    except Exception:
        base_path = os.path.abspath(".")
    return base_path


def get_app_data_path():
    app_name = "PapagayoNG"
    app_author = "Morevna Project"
    user_data_dir = appdirs.user_data_dir(app_name, app_author)
    # If user data dir does not exist yet we create it.
    author_dir = os.path.abspath(os.path.join(user_data_dir, os.pardir))
    if not os.path.exists(author_dir):
        os.mkdir(author_dir)
    if not os.path.exists(user_data_dir):
        os.mkdir(user_data_dir)
    ini_path = os.path.join(user_data_dir, "settings.ini")
    config = QtCore.QSettings(ini_path, QtCore.QSettings.IniFormat)
    config.setFallbacksEnabled(False)  # File only, not registry or or.
    config.setValue("appdata_dir", user_data_dir)

    return user_data_dir


def which(program):
    def is_exe(fpath):
        if os.name == 'nt':
            return os.path.isfile(fpath) or os.path.isfile("{}.exe".format(fpath)) or os.path.isfile(
                "{}.bat".format(fpath))
        else:
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        program = os.path.realpath(program)
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            exe_file = os.path.realpath(exe_file)
            if is_exe(exe_file):
                return exe_file

    return None


def ffmpeg_binaries_exists():
    if platform.system() in ["Windows", "Darwin"]:
        ffmpeg_binary = "ffmpeg.exe"
        ffprobe_binary = "ffprobe.exe"
        if platform.system() == "Darwin":
            ffmpeg_binary = "ffmpeg"
            ffprobe_binary = "ffprobe"
        ffmpeg_path = os.path.join(get_app_data_path(), ffmpeg_binary)
        ffprobe_path = os.path.join(get_app_data_path(), ffprobe_binary)
        if not os.path.exists(ffmpeg_path) or not os.path.exists(ffprobe_path):
            return False
        else:
            return True
    return False


def allosaurus_model_exists():
    allosaurus_model_path = os.path.join(get_app_data_path(), "allosaurus_model", "latest")
    if os.path.exists(allosaurus_model_path):
        if not os.listdir(allosaurus_model_path):
            return False
        else:
            return True
    else:
        return False


def rhubarb_binaries_exists():
    rhubarb_path = os.path.join(get_app_data_path(), "rhubarb/rhubarb.exe")
    if platform.system() == "Darwin":
        rhubarb_path = os.path.join(get_app_data_path(), "rhubarb/rhubarb")
    if os.path.exists(rhubarb_path):
        return True
    else:
        return False


_INIT_LOGGING_DONE = False
def init_logging():
    """Set up logging streams and format.
    """

    global _INIT_LOGGING_DONE
    if not _INIT_LOGGING_DONE:
        root_logger = logging.root

        root_formatter = logging.Formatter(fmt='{name}.{levelname}.{lineno}: {msg}', style='{')

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(root_formatter)

        root_logger.addHandler(stdout_handler)
        _INIT_LOGGING_DONE = True
        
    else:
        logging.info(f'init_logging already called; skip creation of duplicate handlers')


class ApplicationTranslator:
    def __init__(self):
        self.app = QtCore.QCoreApplication.instance()
        self.translator = QtCore.QTranslator()
        ini_path = os.path.join(get_app_data_path(), "settings.ini")
        config = QtCore.QSettings(ini_path, QtCore.QSettings.IniFormat)
        config.setFallbacksEnabled(False)  # File only, not registry or or.
        self.translator.load(config.value("language", "en_us"), os.path.join(get_main_dir(), "rsrc", "i18n"))
        self.app.installTranslator(self.translator)

    def translate(self, context, text):
        return self.app.translate(context, text)


class WorkerSignals(QtCore.QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress

    '''
    finished = QtCore.Signal()
    error = QtCore.Signal(tuple)
    result = QtCore.Signal(object)
    progress = QtCore.Signal(int)


class Worker(QtCore.QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @QtCore.Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done
