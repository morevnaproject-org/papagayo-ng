WHAT IS PAPAGAYO :
==================
This program is used to syncronises animated lip movement to a sound track.


HOW PAPAGAYO IS USED :
======================
- One loads an audio file into the program.
- The text that is spoken in the audio file is then also input. 
- This text can be split into its separate phoneme (sylable sounds).
- Each sylable sound has a mouth shape associated with it.
- These mouth shapes can then be aligned and timed to frames/timestamp.
- The synchronised sequence and timing of "lips" can then be exported.

HOW PAPAGAYO CODED :
====================
Papagayo-NG is written in Python, with following modules :

### TODO : Verification of version 3.7 complience
Python - the programming language that Papagayo is written in.
https://www.python.org/

### TODO : Verification of version 4.0.3 complience (wxPhoenix)
wxPython - a cross-platform user interface library for Python, wxWidgets based.
https://www.wxpython.org/

### Depriciated because wxglade leaves messy unreadable and difficult to mainatin code !
wxGlade - a user interface builder for wxWidgets. This program is not strictly 
necessary, but is helpful if you want to modify the user interface of Papagayo.
http://wxglade.sourceforge.net/


PyAudio - cross-platform audio I/O library for python based on PortAudio
http://people.csail.mit.edu/hubert/pyaudio/
http://www.portaudio.com/





To run Papagayo-NG, double-click the papagayo-ng.py file, 
or run the following command:

python papagayo-ng.py





-----------------------------

The Papagayo-NG source package includes the following files:

readme.txt - this file
gpl.txt     - the user license for Papagayo-NG

papagayo-ng.py              - the main program file
AboutBox.py                 - about box

phonemes.py                 - a list if phoneme sets available in Papagayo-NG
phonemes_preston_blair.py   - Preston Blair phoneme set (default)
phonemes_fleming_dobbs.py   - Fleming & Dobbs phoneme set
breakdowns/*.py             - code to break down words using language specific pronunciations
PronunciationDialog.py      - a dialog to provide manual phoneme breakdown

LipsyncDoc.py               - the document structure, including voices, phoneme breakdown, etc.
LipsyncFrame.py             - the main Papagayo-NG window
WaveformView.py             - view handler for the audio waveform in the main window
MouthView.py                - view handler for the mouth in the main window


lipsync.wxg                 - a wxGlade file defining the user interface layout for Papagayo-NG
rsrc/                       - various resources for Papagayo-NG, including button pictures, mouths, and language configuration/data
rsrc/mouths/                - a folder containing the mouth pictures
rsrc/languages/             - a folder containing the configuration and data for different languages
papagayo-ng.ico             - Windows icons
papagayo-ng.icns            - MacOS X icons

setup.py                    - a script to build Papagayo-NG as a standalone Windows application
setup_mac.py                - a script to build Papagayo-NG as a standalone MacOS X application

-----------------------------

Here are a couple tips for source code that you may want to modify:

By default, Papagayo-NG uses the Preston Blair phoneme set. 
There is also Fleming & Dobbs phoneme set available. 
The phoneme sets are stored in the phonemes_*.py files. If you want to add a 
different set of phonemes, you can use existing sets as examples. Also, take a 
look at the instructions in the phonemes.py file.

To add breakdowns for other languages create a new language configuration 
in rsrc/languages/<language> inside you need to place a configuration file 
(see italian for an example of how to configure a breakdown)  
You will also need to create a breakdown class.  These live in breakdowns.  
The naming convention is <language>_breakdown.py. Just examine one of the 
existing ones for how to make it work.  Make sure the function to call your 
breakdown processing is called breakdownWord.

Papagayo-NG now only works with Moho, but support could be added for other 
animation software, 2D or 3D. To add support for other export formats, 
look in the LipsyncDoc.py file for the function LipsyncVoice:Export - this is 
where Papagayo-NG exports switch data for Moho. You will also need to modify 
the file LipsyncFrame.py to add a user interface for exporting the new format.

-----------------------------

Original Copyright (C) 2005 Mike Clifton
Contact:http://www.lostmarble.com

Modifications (C) 2010 Benjamin Lau
Contact:https://code.google.com/archive/p/papagayo/

Papagayo-NG (C) 2016
- Konstantin Dmitriev
- Stefan Murawski
- Azia Giles Abuara
#TODO: Add People currently working on Papagayo-NG
https://github.com/morevnaproject/papagayo-ng
