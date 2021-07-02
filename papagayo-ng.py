#--coding: utf-8 --
import platform
import sys
import LipsyncFrameQT
import papagayongrcc
import ctypes

if __name__ == "__main__":
    if platform.system() == "Windows":
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        process_array = (ctypes.c_uint8 * 1)()
        num_processes = kernel32.GetConsoleProcessList(process_array, 1)
        if num_processes < 3:
            ctypes.WinDLL('user32').ShowWindow(kernel32.GetConsoleWindow(), 0)
    papagayo_window = LipsyncFrameQT.LipsyncFrame()
    papagayo_window.main_window.show()
    sys.exit(papagayo_window.app.exec_())
