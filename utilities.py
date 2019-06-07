import imp
import os
import sys


def main_is_frozen():
    return (hasattr(sys, "frozen") or  # new py2exe
            hasattr(sys, "importers") or  # old py2exe
            imp.is_frozen("__main__"))  # tools/freeze


def get_main_dir():
    if main_is_frozen():
        return os.path.abspath(os.path.dirname(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def which(program):
    def is_exe(fpath):
        if os.name == 'nt':
            return os.path.isfile(fpath) or os.path.isfile("{}.exe".format(fpath)) or os.path.isfile("{}.bat".format(fpath))
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
