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

export EMAIL='ksee.zelgadis@gmail.com'
export VERSION='1.4.2'
export RELEASE='5'
export SCRIPTDIR=$(cd `dirname $0`; pwd)
export SOURCEDIR=`dirname "$SCRIPTDIR"`

cat > /tmp/papagayo.spec << EOS
%define _unpackaged_files_terminate_build 0

Name:           papagayo
Version:        $VERSION
Release:        $RELEASE
Summary: 	Lipsync tool.
Group: 		Applications/Multimedia
License:        GPL
URL:            http://github.com/morevnaproject/papagayo
BuildArch:	noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	pyaudio wxPython


%description
Papagayo is a lip-syncing program designed to help you line up phonemes (mouth shapes) with the actual recorded sound of actors speaking. Papagayo makes it easy to lip sync animated characters by making the process very simple - just type in the words being spoken (or copy/paste them from the animation's script), then drag the words on top of the sound's waveform until they line up with the proper sounds. 

%prep


%build

%install
rm -rf \$RPM_BUILD_ROOT

cd $SOURCEDIR
mkdir -p \$RPM_BUILD_ROOT/opt/papagayo
cp -rf *.py \$RPM_BUILD_ROOT/opt/papagayo
cp -rf *.txt \$RPM_BUILD_ROOT/opt/papagayo
cp -rf breakdowns \$RPM_BUILD_ROOT/opt/papagayo
cp -rf rsrc \$RPM_BUILD_ROOT/opt/papagayo

mkdir -p \$RPM_BUILD_ROOT/usr/bin
cat > \$RPM_BUILD_ROOT/usr/bin/papagayo << EOF
#!/bin/sh

python /opt/papagayo/papagayo.py \\\${1+"\\\$@"} 2>&1
EOF
chmod a+x \$RPM_BUILD_ROOT/usr/bin/papagayo

mkdir -p \$RPM_BUILD_ROOT/usr/share/applications
cat > \$RPM_BUILD_ROOT/usr/share/applications/papagayo.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=Papagayo 
Comment=Lipsync tool
Exec=papagayo
Icon=papagayo.png
Terminal=false
Type=Application
Categories=Graphics;Application;
MimeType=application/x-papagayo;
X-Desktop-File-Install-Version=0.15
EOF

mkdir -p \$RPM_BUILD_ROOT/usr/share/mime/packages
cat > \$RPM_BUILD_ROOT/usr/share/mime/packages/papagayo.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
    <mime-type type="application/x-papagayo">
        <comment xml:lang="en">Papagayo Project</comment>
        <glob pattern="*.pgo" />
    	<icon name="papagayo"/>
  </mime-type>
</mime-info>
EOF

mkdir -p \$RPM_BUILD_ROOT/usr/share/pixmaps
mv \$RPM_BUILD_ROOT/opt/papagayo/rsrc/papagayo.png \$RPM_BUILD_ROOT/usr/share/pixmaps/papagayo.png

%check
exit 0

%clean
rm -rf \$RPM_BUILD_ROOT

%post
if [ -x /usr/bin/update-mime-database ]; then
  update-mime-database /usr/share/mime
fi
if [ -x /usr/bin/update-desktop-database ]; then
  update-desktop-database
fi

%postun
if [ -x /usr/bin/update-mime-database ]; then
  update-mime-database /usr/share/mime
fi
if [ -x /usr/bin/update-desktop-database ]; then
  update-desktop-database
fi

%files
%defattr(-,root,root,-)
/opt/papagayo/*
/usr/bin/*
/usr/share/*

%changelog
* Wed Feb 24 2013 Konstantin Dmitriev <ksee.zelgadis@gmail.com> - 0.5-1
- Initial release

EOS
	
	rpmbuild -bb --target noarch /tmp/papagayo.spec
	rm /tmp/papagayo.spec
	cp /root/rpmbuild/RPMS/noarch/papagayo-${VERSION}-${RELEASE}.noarch.rpm .
    alien -k --scripts papagayo-${VERSION}-${RELEASE}.noarch.rpm
    rm -rf papagayo-${VERSION}
