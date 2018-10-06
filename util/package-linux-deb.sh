#!/bin/sh
#
# Copyright (c) 2012-2013 Konstantin Dmitriev
#
# How to build:
# mount -o bind /mnt/data/zelgadis/projects/owncloud/papagayo /mnt/data/buildroots/pencil-buildroot.i386/mnt/
# linux32 chroot /mnt/data/buildroots/pencil-buildroot.i386/
# apt-get install --force-yes -y rpm alien
# cd /mnt
# bash util/package-linux.sh
# exit
# umount /mnt/data/buildroots/pencil-buildroot.i386/mnt/

set -e

if [[ `whoami` != "root" ]]; then
	echo "ERROR: You must be root to run this command."
	exit 1
fi

if ! ( which dpkg-buildpackage ); then
  apt-get install dpkg-dev
fi

export EMAIL='contact@morevnaproject.org'
export VERSION='1.4.2'
export RELEASE='1'
export SCRIPTDIR=$(cd `dirname $0`; pwd)
export SOURCEDIR=`dirname "${SCRIPTDIR}"`

DEB_DIST=/tmp/dist-deb/papagayo-ng-${VERSION}
[ -d "${DEB_DIST}" ] && rm -rf ${DEB_DIST}
mkdir -p ${DEB_DIST}


mkdir -p ${DEB_DIST}/opt/papagayo-ng
cp -rf ${SOURCEDIR}/*.py ${DEB_DIST}/opt/papagayo-ng
cp -rf ${SOURCEDIR}/*.txt ${DEB_DIST}/opt/papagayo-ng
cp -rf ${SOURCEDIR}/breakdowns ${DEB_DIST}/opt/papagayo-ng
cp -rf ${SOURCEDIR}/rsrc ${DEB_DIST}/opt/papagayo-ng 

# icons 
mkdir -p ${DEB_DIST}/usr/share/icons/hicolor
cp ${DEB_DIST}/opt/papagayo-ng/rsrc/papagayo-ng.png ${DEB_DIST}/usr/share/icons/hicolor/
mkdir -p ${DEB_DIST}/opt/papagayo-ng/share/pixmaps
cp ${DEB_DIST}/opt/papagayo-ng/rsrc/papagayo-ng.png ${DEB_DIST}/opt/papagayo-ng/share/pixmaps/

# exec
mkdir -p ${DEB_DIST}/usr/bin
cat > ${DEB_DIST}/usr/bin/papagayo-ng << EOF
#!/bin/sh

python /opt/papagayo-ng/papagayo-ng.py \${1+"\$@"} 2>&1
EOF
chmod a+x ${DEB_DIST}/usr/bin/papagayo-ng

# desktop
mkdir -p ${DEB_DIST}/usr/share/applications
cat > ${DEB_DIST}/usr/share/applications/papagayo-ng.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=Papagayo-NG 
Comment=Lipsync tool
Exec=papagayo-ng
Icon=papagayo-ng.png
Terminal=false
Type=Application
Categories=Graphics;Application;
MimeType=application/x-papagayo;
X-Desktop-File-Install-Version=0.15
EOF

mkdir -p ${DEB_DIST}/usr/share/mime/packages
cat > ${DEB_DIST}/usr/share/mime/packages/papagayo.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
    <mime-type type="application/x-papagayo">
        <comment xml:lang="en">Papagayo-NG Project</comment>
        <glob pattern="*.pgo" />
    	<icon name="papagayo-ng"/>
  </mime-type>
</mime-info>
EOF

mkdir -p ${DEB_DIST}/debian
	echo "9" > ${DEB_DIST}/debian/compat
	
	cat > ${DEB_DIST}/debian/control << EOF
Source: papagayo-ng
Section: graphics
Priority: extra
Maintainer: Konstantin Dmitiev <contact@morevnaproject.org

Package: papagayo-ng
Provides: papagayo
Architecture: all
Depends: python-pyaudio, python-wxgtk3.0
Description: Lip-sync animation software
 Papagayo is a lip-syncing program designed to help you line up phonemes (mouth shapes) with the actual recorded sound of actors speaking. Papagayo makes it easy to lip sync animated characters by making the process very simple - just type in the words being spoken (or copy/paste them from the animation's script), then drag the words on top of the sound's waveform until they line up with the proper sounds.
EOF
	
	cat > ${DEB_DIST}/debian/copyright << EOF
Format: http://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: papagayo-ng
Source: https://github.com/morevnaproject/papagayo-ng/

Files: *
Copyright: 2005           Mike Clifton
           2010           Benjamin Lau
           2016-2018      Konstantin Dmitriev
           2017           Azia Giles Abuara
           2017-2018      Stefan Murawski
License: GPL-2
Comment: see list of all contributors in file README
EOF
	
	cat > ${DEB_DIST}/debian/changelog << EOF
papagayo-ng (${VERSION}-${RELEASE}) unstable; urgency=medium

  * Custom Debian package form morevnaproject.org.

 -- Konstantin Dmitriev <contact@morevnaproject.org>  Sat, 06 Oct 2018 16:22:23 +1100

EOF
	
	cat > ${DEB_DIST}/debian/postinst << EOF
#!/bin/bash
if [ -x /usr/bin/update-mime-database ]; then
  update-mime-database /usr/share/mime
fi
if [ -x /usr/bin/update-desktop-database ]; then
  update-desktop-database
fi
EOF
	chmod a+x ${DEB_DIST}/debian/postinst
	
	cat > ${DEB_DIST}/debian/postrm << EOF
#!/bin/bash
if [ -x /usr/bin/update-mime-database ]; then
  update-mime-database /usr/share/mime
fi
if [ -x /usr/bin/update-desktop-database ]; then
  update-desktop-database
fi
EOF
	chmod a+x ${DEB_DIST}/debian/postrm

	cat > ${DEB_DIST}/debian/rules << EOF
#!/usr/bin/make -f
# debian/rules for alien

PACKAGE=\$(shell dh_listpackages)

build:
	dh_testdir

clean:
	dh_testdir
	dh_testroot
	dh_clean -d

binary-indep: build

binary-arch: build
	dh_testdir
	dh_testroot
	dh_prep
	dh_installdirs

	dh_installdocs
	dh_installchangelogs

# Copy the packages's files.
	find . -maxdepth 1 -mindepth 1 -not -name debian -print0 | \
		xargs -0 -r -i cp -a {} debian/\$(PACKAGE)

#
# If you need to move files around in debian/\$(PACKAGE) or do some
# binary patching, do it here
#


# This has been known to break on some wacky binaries.
#	dh_strip
	dh_compress
#	dh_fixperms
	dh_makeshlibs
	dh_installdeb
	-dh_shlibdeps
	dh_gencontrol
	dh_md5sums
#	dh_builddeb

binary: binary-indep binary-arch
.PHONY: build clean binary-indep binary-arch binary
EOF
	
cd ${DEB_DIST}
dpkg-buildpackage -d || true
chmod -R a+rX debian/papagayo-ng
dpkg-deb -Zgzip -b debian/papagayo-ng
mv debian/papagayo-ng.deb ${SCRIPTDIR}/papagayo-ng_${VERSION}-${RELEASE}_all.deb

#optionally, generate rpm
cd ${SCRIPTDIR}
alien -k --scripts -r ${SCRIPTDIR}/papagayo-ng_${VERSION}-${RELEASE}_all.deb || true
[ ! -d papagayo-ng-${VERSION} ] || rm -rf papagayo-ng-${VERSION}
