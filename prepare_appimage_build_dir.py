import os
import shutil

PREPARE_FOR_PYINSTALLER = True


def main():
    source_dir = os.getcwd()
    new_dir = os.path.join(os.getcwd(), "app_image_build")
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    else:
        shutil.rmtree(new_dir)
        os.makedirs(new_dir)
    list_of_files = ["papagayo-ng.py", "Rhubarb.py", "AboutBoxQT.py",
                     "MouthViewQT.py", "utilities.py", "SettingsQT.py",
                     "PronunciationDialogQT.py", "SoundPlayerNew.py",
                     "SoundPlayerOSX.py", "SoundPlayerQT.py",
                     "WaveformViewRewrite.py", "papagayongrcc.py",
                     "LipsyncDoc.py", "LipsyncFrameQT.py",
                     "auto_recognition.py", "SoundPlayer.py", "gpl.txt",
                     "papagayo-ng.ico", "ipa_cmu.json", "version_information.txt",
                     "qt-icons.qrc", "readme.md", "about_markdown.html",
                     "rsrc/", "breakdowns/", "phonemes/", "requirements.txt"]

    if PREPARE_FOR_PYINSTALLER:
        list_of_files.append("nsis_extra_files/")
        list_of_files.append("papagayo-ng.spec")

    for file_name in list_of_files:
        if file_name.endswith(r"/"):
            shutil.copytree(os.path.join(source_dir, file_name), os.path.join(new_dir, file_name))
        else:
            shutil.copy(os.path.join(source_dir, file_name), os.path.join(new_dir, file_name))


if __name__ == "__main__":
    main()
