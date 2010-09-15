# Papagayo, a lip-sync tool for use with Lost Marble's Moho
# Copyright (C) 2005 Mike Clifton
# Contact information at http://www.lostmarble.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# setup.py
# To run: python setup.py py2exe
# To display options: python setup.py py2exe --help
# To run in GUI mode: setup(windows=["app.py"])
# To run in command-line mode: setup(console=["app.py"])
from distutils.core import setup
import py2exe
import os
import sys

resources = [("",["papagayo.nsi","papagayo.ico","gpl.txt"])]
for root, dirs, files in os.walk('rsrc'):
	if ".svn" in root:
		continue
	dirdata = (root,[])
	for file in files:
		if "~" in file:
			continue
		dirdata[1].append(os.path.join(root,file))
	resources.append(dirdata)
		
for root, dirs, files in os.walk('dlls'):
	dirdata = ("",[])
	for file in files:
		dirdata[1].append(os.path.join(root,file))
	resources.append(dirdata)
	
setup(
	windows = [{
		"script": "papagayo.py",
		"icon_resources": [(1, "papagayo.ico")],
		}],
	options = {"py2exe": {
		"compressed": 1,
		"optimize": 2,
		"packages": ["encodings"]
	}},
	name = "Papagayo",
	version = "1.2",
	data_files = resources
)

os.system(r"C:\Program Files\NSIS\makensis.exe output\papagayo.nsi")