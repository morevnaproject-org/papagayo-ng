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

# setup_mac.py
# To run: python setup_mac.py py2app
from distutils.core import setup
import glob
import py2app

py2app_options = dict(
	# This is a shortcut that will place MyApplication.icns
	# in the Contents/Resources folder of the application bundle,
	# and make sure the CFBundleIcon plist key is set appropriately.
	iconfile="papagayo.icns",
),

setup(
	app = ["papagayo.py"],
	options = {"py2app": {
		"iconfile": "papagayo.icns",
	}},
	name = "Papagayo",
	version = "1.1"
)
