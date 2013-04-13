To work with the Papagayo source code, you need some special software installed. This software is not necessary to run the installer-based version of Papagayo, but you do need it if you want to use this source code package.

Python - the programming language that Papagayo is written in.
http://www.python.org/

wxPython - a cross-platform user interface library for Python, based on wxWidgets.
http://www.wxpython.org/

OpenAL - a cross platform audio library. This provides a more cross-platform way of providing audio playback capabilities and replaces an earlier version using pyaudio and before that a custom library produced by Lost Marble.
http://openal.org (OpenAL ships with OS X and should be easily available for most Linux Distributions)

wxGlade - a user interface builder for wxWidgets. This program is not strictly necessary, but is helpful if you want to modify the user interface of Papagayo.
http://wxglade.sourceforge.net/


Papagayo is written in Python, and requires no special tools to work with the source - a basic text editor is good enough. To run Papagayo, double-click the papagayo.py file, or run the following command:

python papagayo.py

-----------------------------

The Papagayo source package includes the following files:

readme.txt - this file
gpl.txt - the user license for Papagayo

papagayo.py - the main program file
phonemes.py - a list if phoneme sets available in Papagayo
phonemes_preston_blair.py - Preston Blair phoneme set (default)
phonemes_fleming_dobbs.py - Fleming & Dobbs phoneme set
LipsyncDoc.py - the document structure, including voices, phoneme breakdown, etc.
breakdowns/*.py - code to break down words using language specific pronunciations
LipsyncFrame.py - the main Papagayo window
WaveformView.py - the waveform view in the main window
MouthView.py - the mouth view in the main window
PronunciationDialog.py - a dialog to provide manual phoneme breakdown
AboutBox.py - about box


lipsync.wxg - a wxGlade file defining the user interface layout for Papagayo


rsrc/ - various resources for Papagayo, including button pictures, mouths, and language configuraion/data
rsrc/mouths/ - a folder containing the mouth pictures
rsrc/languages/ - a folder containing the configuration and data for different languages
papagayo.ico - Windows icons
papagayo.icns - MacOS X icons

setup.py - a script to build Papagayo as a standalone Windows application
setup_mac.py - a script to build Papagayo as a standalone MacOS X application

-----------------------------

Here are a couple tips for source code that you may want to modify:

By default, Papagayo uses the Preston Blair phoneme set. There is also Fleming & Dobbs phoneme set available. The phoneme sets are stored in the phonemes_*.py files. If you want to add a different set of phonemes, you can use existsing sets as examples. Also, take a look at the instructions in the phonemes.py file.

To add breakdowns for other languages create a new language configuration in rsrc/languages/<language> inside you need to place a configuration file (see italian for an example of how to configure a breakdown)  You will also need to create a breakdown class.  These live in breakdowns.  The naming convention is <language>_breakdown.py. Just examine one of the existing ones for how to make it work.  Make sure the function to call your breakdown processing is called breakdownWord.

Papagayo now only works with Moho, but support could be added for other animation software, 2D or 3D. To add support for other export formats, look in the LipsyncDoc.py file for the function LipsyncVoice:Export - this is where Papagayo exports switch data for Moho. You will also need to modify the file LipsyncFrame.py to add a user interface for exporting the new format.

-----------------------------

Copyright (C) 2005 Mike Clifton
Contact:
http://www.lostmarble.com

Modifications (C) 2010 Benjamin Lau
Contact:
http://code.google.com/p/papagayo/
