#-----------------------------------------------------------------------------
# Copyright (c) 2014-2018, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

import os
from PyInstaller.utils.hooks import collect_data_files, get_qmake_path
from PyInstaller.utils.hooks.qt import Qt5LibraryInfo
import PyInstaller.compat as compat


hiddenimports = ['PySide2.QtCore',
                 'PySide2.QtGui',
                 'PySide2.QtNetwork',
                 'PySide2.QtWebChannel',
                 'PySide2.QtWebEngineCore',
                 ]

if compat.is_win:
    pyside2_library_info = Qt5LibraryInfo('PySide2')
    pyside2_dir = pyside2_library_info.location['DataPath']
    binaries = [(os.path.join(pyside2_dir, 'QtWebEngineProcess.exe'), '.')]
    resources_dir = os.path.join(pyside2_dir, 'resources')
    datas = [(os.path.join(resources_dir, 'icudtl.dat'), '.'),
             (os.path.join(resources_dir, 'qtwebengine_resources.pak'), '.')]
    
else:
    # Find the additional files necessary for QtWebEngine.
    datas = (collect_data_files('PySide2', True, os.path.join('Qt', 'resources')) +
             collect_data_files('PySide2', True, os.path.join('Qt', 'translations')) +
             [x for x in collect_data_files('PySide2', False, os.path.join('Qt', 'bin'))
              if x[0].endswith('QtWebEngineProcess.exe')])

    # Note that for QtWebEngineProcess to be able to find icudtl.dat the bundle_identifier
    # must be set to 'org.qt-project.Qt.QtWebEngineCore'. This can be done by passing
    # bundle_identifier='org.qt-project.Qt.QtWebEngineCore' to the BUNDLE command in
    # the .spec file. FIXME: This is not ideal and a better solution is required.
    qmake = get_qmake_path('5')
    if qmake:
        libdir = compat.exec_command(qmake, "-query", "QT_INSTALL_LIBS").strip()

        if compat.is_darwin:
            binaries = [
                (os.path.join(libdir, 'QtWebEngineCore.framework', 'Versions', '5',
                              'Helpers', 'QtWebEngineProcess.app', 'Contents', 'MacOS', 'QtWebEngineProcess'),
                 os.path.join('QtWebEngineProcess.app', 'Contents', 'MacOS'))
            ]

            resources_dir = os.path.join(libdir, 'QtWebEngineCore.framework', 'Versions', '5', 'Resources')
            datas += [
                (os.path.join(resources_dir, 'icudtl.dat'), '.'),
                (os.path.join(resources_dir, 'qtwebengine_resources.pak'), '.'),
                # The distributed Info.plist has LSUIElement set to true, which prevents the
                # icon from appearing in the dock.
                (os.path.join(libdir, 'QtWebEngineCore.framework', 'Versions', '5',
                              'Helpers', 'QtWebEngineProcess.app', 'Contents', 'Info.plist'),
                 os.path.join('QtWebEngineProcess.app', 'Contents'))
            ]
