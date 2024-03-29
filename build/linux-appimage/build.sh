#!/bin/sh

# https://github.com/AppImage/AppImageKit/wiki/Bundling-Python-apps

SCRIPTPATH=$(cd `dirname "$0"`; pwd)
SOURCES_DIR="${SCRIPTPATH}/../../app_image_build/"

#PYTHON_APPIMAGE_URL="https://github.com/niess/python-appimage/releases/download/python3.10/python3.10.0-cp310-cp310-manylinux2010_x86_64.AppImage"
PYTHON_APPIMAGE_URL="https://github.com/niess/python-appimage/releases/download/python3.9/python3.9.6-cp39-cp39-manylinux2014_x86_64.AppImage"
PYTHON_APPIMAGE_FILENAME=`basename "${PYTHON_APPIMAGE_URL}"`

# Detect package management system.
YUM=$(which yum 2>/dev/null)
APT_GET=$(which apt-get 2>/dev/null)

echo "Installing required build tools."
# libffi is required by cffi python package, which in turn is required by sounddevice
if [[ ! -z $YUM ]]; then
    sudo yum install -y gcc libffi-devel
elif [[ ! -z $APT_GET ]]; then
    sudo apt-get install -y build-essential libffi-dev
fi


[ -d "${SCRIPTPATH}/build" ] || mkdir -p "${SCRIPTPATH}/build"
cd "${SCRIPTPATH}/build"
wget "${PYTHON_APPIMAGE_URL}"
chmod +x "${PYTHON_APPIMAGE_FILENAME}"
"./${PYTHON_APPIMAGE_FILENAME}" --appimage-extract

#export PATH="$(pwd)/squashfs-root/usr/bin:$PATH"
./squashfs-root/AppRun -m pip install torch==1.9.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
./squashfs-root/AppRun -m pip install -r "${SOURCES_DIR}requirements.txt"
#./squashfs-root/AppRun -m pip install $(grep -ivE "allosaurus" "${SOURCES_DIR}requirements.txt")
rm squashfs-root/opt/python3.9/lib/python3.9/site-packages/PySide2/Qt/lib/libQt5WebEngineCore.so.5
rm -rf ./squashfs-root/opt/python3.9/lib/python3.9/site-packages/torch/test


#find "${SOURCES_DIR}" -type f -not -iname '*/not-from-here/*' -exec cp -rf '{}' '/dest/{}' ';'
rsync -av --progress "${SOURCES_DIR}" "squashfs-root/opt/papagayo-ng" --exclude build

cp "${SCRIPTPATH}/files/papagayo-ng" squashfs-root/usr/bin/
rm squashfs-root/usr/share/applications/*.desktop
rm squashfs-root/*.desktop
cp "${SCRIPTPATH}/files/papagayo-ng.desktop" squashfs-root/usr/share/applications/
cp "${SCRIPTPATH}/files/papagayo-ng.desktop" squashfs-root/
cp "${SOURCES_DIR}/rsrc/papagayo-ng.png" squashfs-root/
rm squashfs-root/usr/share/metainfo/*

# Change AppRun so that it launches papagayo-ng
sed -i -e 's|/opt/python3.9/bin/python3.9|/usr/bin/papagayo-ng|g' ./squashfs-root/AppRun

# Convert back into an AppImage
wget -c https://github.com/$(wget -q https://github.com/probonopd/go-appimage/releases -O - | grep "appimagetool-.*-x86_64.AppImage" | head -n 1 | cut -d '"' -f 2)
chmod +x appimagetool-*.AppImage
#
# The following line does not work quite yet due to https://github.com/probonopd/go-appimage/issues/30
# ./appimagetool-*-x86_64.AppImage deploy squashfs-root/usr/share/applications/taguette.desktop
./appimagetool-*-x86_64.AppImage squashfs-root/ # Replace "1" with the actual version/build number
mv Papagayo_NG-*-x86_64.AppImage ../
cd ..
rm -rf build