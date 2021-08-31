# -*- mode: python -*-
import shutil
import os
import sys
standalone_exe = True
block_cipher = None
with_rhubarb = False

if sys.platform == "win32":
    import pyinstaller_versionfile
    pyinstaller_versionfile.create_versionfile_from_input_file(
    output_file="./file_version_info.txt",
    input_file="./version_information.txt")

a = Analysis(['papagayo-ng.py'],
             pathex=['./'],
             binaries=[],
             datas=[],
             hiddenimports=['PySide2.QtXml', 'PySide2.QtPrintSupport', 'numpy.random.common', 'numpy.random.bounded_integers', 'numpy.random.entropy', 'pkg_resources.py2_warn', 'audioread', 'pydub'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
# Avoid warning
for d in a.datas:
    if '_C.cp39-win_amd64.pyd' in d[0]:
        a.datas.remove(d)
        break

useless_libs = (
        "Qt3D",
        "QtDesigner",
        "QtQuick",
        "QtShader",
        "QtVirt",
        "QtSql",
        "QtData",
        "QtCharts",
        "QtLabs",
        "QtScxml",
        "QtMultimedia",
        "QtWebEngine",
        "Qt5WebEngineCore"
    )
for d in a.datas:
    if d[0].startswith(useless_libs):
        a.datas.remove(d)

if sys.platform == "win32":
    splash = Splash('./rsrc/splash.png',
                    binaries=a.binaries,
                    datas=a.datas)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
if not standalone_exe:
    exe = EXE(pyz,
              a.scripts,
              splash,
              a.zipfiles,
              exclude_binaries=True,
              name='papagayo-ng',
              icon='./papagayo-ng.ico',
              debug=False,
              bootloader_ignore_signals=False,
              strip=False,
              upx=False,
              upx_exclude="vcruntime140.dll, qwindows.dll",
              runtime_tmpdir=None,
              console=False )
    coll = COLLECT(
        exe,
        splash.binaries,
        a.binaries,
        a.datas,
        name='papagayo-ng',
        strip=False,
        upx=False,
        upx_exclude="vcruntime140.dll, qwindows.dll"
    )
else:
    spec_file = None
    if sys.platform == "win32":
        spec_file = "./file_version_info.txt"
    exe = EXE(pyz,
              a.scripts,
              splash,
              splash.binaries,
              a.binaries,
              a.zipfiles,
              a.datas,
              [],
              name='papagayo-ng',
              icon='./papagayo-ng.ico',
              version= spec_file,
              debug=False,
              bootloader_ignore_signals=False,
              strip=False,
              upx=False,
              upx_exclude="qwindows.dll, pyside2.abi3.dll, qtcore.pyd, qtgui.pyd, qtwidgets.pyd, qt5core.dll, qt5gui.dll, qt5svg.dll, qt5widgets.dll, qt5xml.dll",
              runtime_tmpdir=None,
              console=True )

installer_folder = "./installer_files"
if os.path.exists(installer_folder):
    shutil.rmtree(installer_folder)
os.mkdir(installer_folder)
if sys.platform == "win32":
    shutil.move("./dist/papagayo-ng.exe", os.path.join(installer_folder , "papagayo-ng.exe"))
else:
    shutil.move("./dist/papagayo-ng", os.path.join(installer_folder , "papagayo-ng"))
shutil.copytree("./breakdowns", os.path.join(installer_folder , "breakdowns"))
shutil.copytree("./phonemes", os.path.join(installer_folder , "phonemes"))
shutil.copytree("./rsrc", os.path.join(installer_folder , "rsrc"))
if with_rhubarb:
    shutil.copytree("./rhubarb", os.path.join(installer_folder , "rhubarb"))
shutil.copy("../papagayo-ng.nsi", os.path.join(installer_folder , "papagayo-ng.nsi"))
shutil.copy("./papagayo-ng.ico", os.path.join(installer_folder , "papagayo-ng.ico"))
shutil.copy("./ipa_cmu.json", os.path.join(installer_folder , "ipa_cmu.json"))
shutil.copy("./version_information.txt", os.path.join(installer_folder , "version_information.txt"))
shutil.copy("./about_markdown.html", os.path.join(installer_folder , "about_markdown.html"))