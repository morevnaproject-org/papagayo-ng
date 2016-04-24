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
# you use for animating. By default, the animation phoneme set is the Preston
# Blair phoneme set, as found in the book:
# "Cartoon Animation", by Preston Blair, page 186.

# The phonemeset is defined in the two tables below. The first table contains
# the basic list of phonemes to use in your animation. The second table 
# contains a mapping from the CMU phonemes to the phonemes in the first table.

# Preston Blair phoneme set:
# AI O E U etc L WQ MBP FV
# etc=CDGKNRSThYZ

phoneme_set = [
    'AI',
    'O',
    'E',
    'U',
    'etc', # this covers Preston Blair's CDGKNRSThYZ mouth shape
    'L',
    'WQ',
    'MBP',
    'FV',
    'rest' # not really a phoneme - this is used in-between phrases when the mouth is at rest
]

# Phoneme conversion dictionary: CMU on the left to Preston Blair on the right
phoneme_conversion = {
    'AA0': 'AI', # odd     AA D
    'AA1': 'AI',
    'AA2': 'AI',
    'AE0': 'AI', # at   AE T
    'AE1': 'AI',
    'AE2': 'AI',
    'AH0': 'AI', # hut  HH AH T
    'AH1': 'AI',
    'AH2': 'AI',
    'AO0': 'O', # ought AO T
    'AO1': 'O',
    'AO2': 'O',
    'AW0': 'O', # cow   K AW
    'AW1': 'O',
    'AW2': 'O',
    'AY0': 'AI', # hide HH AY D
    'AY1': 'AI',
    'AY2': 'AI',
    'B': 'MBP', # be    B IY
    'CH': 'etc', # cheese   CH IY Z
    'D': 'etc', # dee   D IY
    'DH': 'etc', # thee DH IY
    'EH0': 'E', # Ed    EH D
    'EH1': 'E',
    'EH2': 'E',
    'ER0': 'E', # hurt  HH ER T
    'ER1': 'E',
    'ER2': 'E',
    'EY0': 'E', # ate   EY T
    'EY1': 'E',
    'EY2': 'E',
    'F': 'FV', # fee    F IY
    'G': 'etc', # green G R IY N
    'HH': 'etc', # he   HH IY
    'IH0': 'AI', # it   IH T
    'IH1': 'AI',
    'IH2': 'AI',
    'IY0': 'E', # eat   IY T
    'IY1': 'E',
    'IY2': 'E',
    'JH': 'etc', # gee  JH IY
    'K': 'etc', # key   K IY
    'L': 'L', # lee L IY
    'M': 'MBP', # me    M IY
    'N': 'L', # knee  N IY
    'NG': 'L', # ping P IH NG
    'OW0': 'O', # oat   OW T
    'OW1': 'O',
    'OW2': 'O',
    'OY0': 'WQ', # toy  T OY
    'OY1': 'WQ',
    'OY2': 'WQ',
    'P': 'MBP', # pee   P IY
    'R': 'etc', # read  R IY D
    'S': 'etc', # sea   S IY
    'SH': 'etc', # she  SH IY
    'T': 'etc', # tea   T IY
    'TH': 'etc', # theta    TH EY T AH
    'UH0': 'U', # hood  HH UH D
    'UH1': 'U',
    'UH2': 'U',
    'UW0': 'U', # two   T UW
    'UW1': 'U',
    'UW2': 'U',
    'V': 'FV', # vee    V IY
    'W': 'WQ', # we W IY
    'Y': 'etc', # yield Y IY L D
    'Z': 'etc', # zee   Z IY
    'ZH': 'etc', # seizure  S IY ZH ER
    # The following phonemes are not part of the CMU phoneme set, but are meant to fix bugs in the CMU dictionary
    'E21': 'E' # E21 is used in ENGINEER
}
