# --coding: utf-8 --
import argparse
import ctypes
import os
import platform
import sys
import papagayongrcc
import LipsyncFrameQT
import logging
from utilities import init_logging

logger = logging.getLogger('papagayo')

try:
    import pyi_splash
except ImportError:
    pyi_splash = None


class ParentClass:
    def __init__(self):
        self.phonemeset = LipsyncFrameQT.LipsyncDoc.PhonemeSet()


def parse_cli():
    ARG_KEY_LOG_LEVEL = "log_level"

    parser = argparse.ArgumentParser(description="Papagayo-NG LipSync Tool")
    parser.add_argument("-i", dest="input_file_path",
                        help="The input file, either a supported Papagayo-NG Project or a sound file.", metavar="FILE")
    parser.add_argument("--cli", dest="use_cli", action="store_true", help="Set this to use CLI commands.")
    parser.add_argument("-o", dest="output_file",
                        help="The output file, should be one of these filetypes or a directory: {}".format(
                            LipsyncFrameQT.lipsync_extension_list + LipsyncFrameQT.export_file_types))
    parser.add_argument("--output-type", dest="output_type", help="Possible options: {}".format(
        "".join(" {},".format(o_type.upper()) for o_type in
                LipsyncFrameQT.lipsync_extension_list + LipsyncFrameQT.exporter_list)[:-1]))
    parser.add_argument("--language", dest="language", help="Choose the language for Alelo Export.")
    parser.add_argument("--mouth-images", dest="mouth_image_dir", help="The Directory containing the mouth Images.")
    parser.add_argument("--use-allosaurus", dest="allosaurus", action="store_true",
                        help="Set this to run Allosaurus on your input files.")
    parser.add_argument("--use-rhubarb", dest="rhubarb", action="store_true",
                        help="Set this to run Rhubarb on your input files.")
    parser.add_argument("--fps", dest="fps", help="Set FPS for Input.", metavar="INT")
    parser.add_argument("--log-level", "-l", dest=ARG_KEY_LOG_LEVEL, choices=logging._nameToLevel.keys(), help="Set logging level.", default=logging._levelToName[logging.WARNING])
    args = parser.parse_args()
    
    # update root logger log level
    try:
        log_level_name = getattr(args, ARG_KEY_LOG_LEVEL, None)
        logging.root.setLevel(logging._nameToLevel[log_level_name])
    except:
        logger.warn(f"unable to set log level to {log_level_name}; leave at {logging._nameToLevel[logging.root.getEffectiveLevel()]}")

    list_of_input_files = []
    langman = LipsyncFrameQT.LipsyncDoc.LanguageManager()
    langman.init_languages()
    ini_path = os.path.join(LipsyncFrameQT.utilities.get_app_data_path(), "settings.ini")
    config = LipsyncFrameQT.QtCore.QSettings(ini_path, LipsyncFrameQT.QtCore.QSettings.IniFormat)
    if not args.use_cli:
        config.setValue("audio_output", "new")
    else:
        config.setValue("audio_output", "old")
        if args.allosaurus:
            config.setValue("/VoiceRecognition/recognizer", "Allosaurus")
            config.setValue("/VoiceRecognition/run_voice_recognition", True)
        if args.rhubarb:
            config.setValue("/VoiceRecognition/recognizer", "Rhubarb")
            config.setValue("/VoiceRecognition/run_voice_recognition", True)
        if not args.allosaurus and not args.rhubarb:
            config.setValue("/VoiceRecognition/run_voice_recognition", False)
        if args.fps:
            config.setValue("LastFPS", args.fps)
        if args.mouth_image_dir:
            config.setValue("MouthDir", args.mouth_image_dir)
        if args.input_file_path:
            parent = ParentClass()
            if os.path.isdir(args.input_file_path):
                for (dirpath, dirnames, filenames) in os.walk(args.input_file_path):
                    list_of_input_files.extend(os.path.join(dirpath, filename) if filename.endswith(
                        LipsyncFrameQT.lipsync_extension_list + LipsyncFrameQT.audio_extension_list) else "" for filename in
                                               filenames)
                    break
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
                if args.output_type.upper() == "MOHO":
                    for voice in i.project_node.children:
                        if args.output_file:
                            if os.path.isdir(args.output_file):
                                voice_file_path = os.path.join(args.output_file, "{}.dat".format(voice.name))
                                voice.export(voice_file_path)
                            else:
                                voice.export(args.output_file)
                elif args.output_type.upper() == "ALELO":
                    for voice in i.project_node.children:
                        if args.output_file:
                            if os.path.isdir(args.output_file):
                                voice_file_path = os.path.join(args.output_file, "{}.txt".format(voice.name))
                                voice.export_alelo(voice_file_path, args.language, langman)
                            else:
                                voice.export_alelo(args.output_file, args.language, langman)
                elif args.output_type.upper() == "JSON":
                    for voice in i.project_node.children:
                        if args.output_file:
                            if os.path.isdir(args.output_file):
                                voice_file_path = os.path.join(args.output_file, "{}.json".format(voice.name))
                                voice.export_json(voice_file_path)
                            else:
                                voice.export_json(args.output_file)
                elif args.output_type.upper() == "IMAGES":
                    for voice in i.project_node.children:
                        if args.output_file:
                            if os.path.isdir(args.output_file):
                                voice.export_images(args.output_file, "")
                elif args.output_type.upper() == "PGO":
                    if args.output_file:
                        i.save(args.output_file)
                elif args.output_type.upper() == "PG2":
                    if args.output_file:
                        i.save2(args.output_file)

    return args.use_cli


if __name__ == "__main__":
    init_logging()

    if pyi_splash:
        pyi_splash.close()
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
