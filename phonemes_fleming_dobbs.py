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




# This file contains a mapping between the CMU phoneme set to the phoneme set
# as found in the book:
# Fleming, Bill, and Darris Dobbs. Animating Facial Features and Expressions. 
#    Rockland, Mass.: Charles River Media, 1999. 

# The phonemeset is defined in the two tables below. The first table contains
# the basic list of phonemes to use in your animation. The second table 
# contains a mapping from the CMU phonemes to the phonemes in the first table.

phoneme_set = [
	'MBP',
	'NLTDR',
	'FV',
	'TH', # TH DH
	'GK',
	'SH', # SH ZH CH J
	'O', # Y OY UE W UH ER
	'EHSZ', # IH EY EH E EE AH AY  AW AE AN H S Z
	'AA', # AA AD OW UW AR
	'IY', # IY IE
	'rest' # not really a phoneme - this is used in-between phrases when the mouth is at rest
]

# Phoneme conversion dictionary: CMU on the left to Preston Blair on the right
phoneme_conversion = {
	'AA0': 'AA', # odd     AA D
	'AA1': 'AA',
	'AA2': 'AA',
	'AE0': 'EHSZ', # at	AE T
	'AE1': 'EHSZ',
	'AE2': 'EHSZ',
	'AH0': 'AA', # hut	HH AH T
	'AH1': 'AA',
	'AH2': 'AA',
	'AO0': 'O', # ought	AO T
	'AO1': 'O',
	'AO2': 'O',
	'AW0': 'O', # cow	K AW
	'AW1': 'O',
	'AW2': 'O',
	'AY0': 'O', # hide	HH AY D
	'AY1': 'O',
	'AY2': 'O',
	'B': 'MBP', # be	B IY
	'CH': 'SH', # cheese	CH IY Z
	'D': 'NLTDR', # dee	D IY
	'DH': 'TH', # thee	DH IY
	'EH0': 'EHSZ', # Ed	EH D
	'EH1': 'EHSZ',
	'EH2': 'EHSZ',
	'ER0': 'O', # hurt	HH ER T
	'ER1': 'O',
	'ER2': 'O',
	'EY0': 'EHSZ', # ate	EY T
	'EY1': 'EHSZ',
	'EY2': 'EHSZ',
	'F': 'FV', # fee	F IY
	'G': 'GK', # green	G R IY N
	'HH': 'EHSZ', # he	HH IY
	'IH0': 'IY', # it	IH T
	'IH1': 'IY',
	'IH2': 'IY',
	'IY0': 'IY', # eat	IY T
	'IY1': 'IY',
	'IY2': 'IY',
	'JH': 'SH', # gee	JH IY
	'K': 'GK', # key	K IY
	'L': 'NLTDR', # lee	L IY
	'M': 'MBP', # me	M IY
	'N': 'NLTDR', # knee	N IY
	'NG': 'NLTDR', # ping	P IH NG
	'OW0': 'O', # oat	OW T
	'OW1': 'O',
	'OW2': 'O',
	'OY0': 'O', # toy	T OY
	'OY1': 'O',
	'OY2': 'O',
	'P': 'MBP', # pee	P IY
	'R': 'NLTDR', # read	R IY D
	'S': 'EHSZ', # sea	S IY
	'SH': 'SH', # she	SH IY
	'T': 'NLTDR', # tea	T IY
	'TH': 'TH', # theta	TH EY T AH
	'UH0': 'O', # hood	HH UH D
	'UH1': 'O',
	'UH2': 'O',
	'UW0': 'O', # two	T UW
	'UW1': 'O',
	'UW2': 'O',
	'V': 'FV', # vee	V IY
	'W': 'FV', # we	W IY
	'Y': 'O', # yield	Y IY L D
	'Z': 'EHSZ', # zee	Z IY
	'ZH': 'SH', # seizure	S IY ZH ER
	# The following phonemes are not part of the CMU phoneme set, but are meant to fix bugs in the CMU dictionary
	'E21': 'EHSZ' # E21 is used in ENGINEER
}
