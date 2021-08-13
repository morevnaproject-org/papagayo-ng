# --coding: utf-8 --
import argparse
import ctypes
import platform
import sys
import os
import papagayongrcc
import LipsyncFrameQT


class ParentClass:
    def __init__(self):
        self.phonemeset = LipsyncFrameQT.PhonemeSet()


def parse_cli():
    parser = argparse.ArgumentParser(description="Papagayo-NG LipSync Tool")
    parser.add_argument("-i", dest="input_file_path",
                        help="The input file, either a supported Papagayo-NG Project or a sound file.", metavar="FILE")
    parser.add_argument("--cli", dest="use_cli", action="store_true", help="Set this to disable the GUI.")
    args = parser.parse_args()
    list_of_input_files = []
    if args.input_file_path:
        parent = ParentClass()
        if os.path.isdir(args.input_file_path):
            for (dirpath, dirnames, filenames) in os.walk(args.input_file_path):
                list_of_input_files.extend(os.path.join(dirpath, filename) if filename.endswith(
                    LipsyncFrameQT.lipsync_extension_list + LipsyncFrameQT.audio_extension_list) else "" for filename in
                                           filenames)
        else:
            if args.input_file_path.endswith(
                    LipsyncFrameQT.lipsync_extension_list + LipsyncFrameQT.audio_extension_list):
                list_of_input_files.append(args.input_file_path)
        list_of_input_files = filter(None, list_of_input_files)
        print("Input Files:")
        list_of_doc_objects = []
        for i in list_of_input_files:
            print(i)
            new_doc = LipsyncFrameQT.open_file_no_gui(i, parent)
            list_of_doc_objects.append(new_doc)

        for i in list_of_doc_objects:
            print(i)
    return args.use_cli


if __name__ == "__main__":
    use_cli = parse_cli()
    if not use_cli:
        if platform.system() == "Windows":
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            process_array = (ctypes.c_uint8 * 1)()
            num_processes = kernel32.GetConsoleProcessList(process_array, 1)
            if num_processes < 3:
                ctypes.WinDLL('user32').ShowWindow(kernel32.GetConsoleWindow(), 0)
        papagayo_window = LipsyncFrameQT.LipsyncFrame()
        papagayo_window.main_window.show()
        sys.exit(papagayo_window.app.exec_())
