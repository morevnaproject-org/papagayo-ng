# -*- mode: python -*-
standalone_exe = True
block_cipher = None


a = Analysis(['papagayo-ng.py'],
             pathex=['./'],
             binaries=[],
             datas=[],
             hiddenimports=['PySide2.QtXml', 'PySide2.QtPrintSupport', 'numpy.random.common', 'numpy.random.bounded_integers', 'numpy.random.entropy', 'pkg_resources.py2_warn', 'audioread'],
             hookspath=[],
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
              upx=False,
              upx_exclude="vcruntime140.dll, qwindows.dll",
              runtime_tmpdir=None,
              console=False )
    coll = COLLECT(
        exe,
        a.binaries,
        a.datas,
        name='papagayo-ng',
        strip=False,
        upx=False,
        upx_exclude="vcruntime140.dll, qwindows.dll"
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
              upx=False,
              upx_exclude="vcruntime140.dll, qwindows.dll",
              runtime_tmpdir=None,
              console=False )