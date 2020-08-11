# -*- mode: python -*-
standalone_exe = True
block_cipher = None


a = Analysis(['papagayo-ng.py'],
             pathex=['C:\\Users\\Stefan\\Documents\\StefanMain\\PycharmProjects\\new_papagayo\\papagayo-ng'],
             binaries=[],
             datas=[('./rsrc', './rsrc'), ('./breakdowns', './breakdowns'), ('./phonemes', './phonemes')],
             hiddenimports=['PySide2.QtXml', 'PySide2.QtPrintSupport', 'phonemes_preston_blair', 'phonemes_fleming_dobbs', 'phonemes_rhubarb', 'numpy.random.common', 'numpy.random.bounded_integers', 'numpy.random.entropy', 'pkg_resources.py2_warn'],
             hookspath=['./hooks'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
if not standalone_exe:
    exe = EXE(pyz,
              a.scripts,
              a.zipfiles,
              exclude_binaries=True,
              name='papagayo-ng',
              icon='./papagayo-ng.ico',
              debug=False,
              bootloader_ignore_signals=False,
              strip=False,
              upx=True,
              runtime_tmpdir=None,
              console=False )
    coll = COLLECT(
        exe,
        a.binaries,
        a.datas,
        name='papagayo-ng',
        strip=False,
        upx=True
    )
else:
    exe = EXE(pyz,
              a.scripts,
              a.binaries,
              a.zipfiles,
              a.datas,
              [],
              name='papagayo-ng',
              icon='./papagayo-ng.ico',
              debug=False,
              bootloader_ignore_signals=False,
              strip=False,
              upx=True,
              runtime_tmpdir=None,
              console=False )