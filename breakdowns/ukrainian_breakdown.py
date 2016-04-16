#!/usr/local/bin/python
# -*- coding: cp1252 -*-

# this language module is written to be part of
# Papagayo, a lip-sync tool for use with Lost Marble's Moho
#
# Papagayo is Copyright (C) 2005 Mike Clifton
# Contact information at http://www.lostmarble.com
#
# this module Copyright (C) 2005 Myles Strous
# Contact information at http://www-personal.monash.edu.au/~myless/catnap/index.html
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

"""functions to take an Ukrainian word and return a list of phonemes
"""

from .unicode_hammer import latin1_to_ascii as hammer

import locale, re

output_encoding = 'utf-16'

input_encoding = locale.getdefaultlocale()[1] # standard system encoding??
# input_encoding = 'cp1252'
# input_encoding = 'utf-8'  # unicode
# input_encoding = 'utf-16'  # unicode
# input_encoding = 'koi8-r'  # cyrillic
# input_encoding = 'utf-32' # unicode
# input_encoding = 'latin-1'
# input_encoding = 'iso-8859-1'

def breakdownWord(word, recursive=False):
    word = word.lower()
    phonemes = []
    vowels = [
        'a', 'A',
        'e', 'E',
        'i', 'I',
        'o', 'O',
        'u', 'U',
        '\N{CYRILLIC SMALL LETTER A}',  # looks like normal a
        # u'\N{CYRILLIC SMALL LETTER IE}',  # looks like normal e
        '\N{CYRILLIC SMALL LETTER UKRAINIAN IE}', # looks something like small Euro symbol with one cross-piece
        '\N{CYRILLIC SMALL LETTER BYELORUSSIAN-UKRAINIAN I}',  # looks like normal i
        # u'\N{CYRILLIC SMALL LETTER YI}',  # i with diaresis
        '\N{CYRILLIC SMALL LETTER I}',  # looks like small backwards capital N
        '\N{CYRILLIC SMALL LETTER SHORT I}',  # looks like small backwards capital N with tilde
        '\N{CYRILLIC SMALL LETTER O}',  # looks like normal o
        '\N{CYRILLIC SMALL LETTER U}',  # looks like normal y
        '\N{CYRILLIC CAPITAL LETTER A}',  # looks like normal A
        # u'\N{CYRILLIC CAPITAL LETTER IE}',  # looks like normal E
        '\N{CYRILLIC CAPITAL LETTER UKRAINIAN IE}', # looks something like Euro symbol with one cross-piece
        '\N{CYRILLIC CAPITAL LETTER BYELORUSSIAN-UKRAINIAN I}',  # looks like normal I
        # u'\N{CYRILLIC CAPITAL LETTER YI}',  # I with diaresis
        '\N{CYRILLIC CAPITAL LETTER I}',  # looks like backwards capital N
        '\N{CYRILLIC CAPITAL LETTER SHORT I}',  # looks like backwards capital N with tilde
        '\N{CYRILLIC CAPITAL LETTER O}',  # looks like normal O
        '\N{CYRILLIC CAPITAL LETTER U}',  # looks like normal Y
    ]
    simple_convert = {
        'a': 'AA0',
        'b': 'B',
        'v': 'V',
        'g': 'G',
        'd': 'D',
        'e': 'EH0',
        'j': 'Y',
        'y': 'IH0',
        'k': 'K',
        'l': 'L',
        'm': 'M',
        'n': 'N',
        'o': 'AO0',
        'p': 'P',
        'r': 'R',
        't': 'T',
        'f': 'F',
        'x': 'HH',  # use 'Y' ?? 'K'??
        '\N{LATIN SMALL LETTER S WITH CARON}': 'SH',  # š
        '\N{LATIN SMALL LETTER Z WITH CARON}': 'ZH',  # ž
        '\N{LATIN CAPITAL LETTER S WITH CARON}': 'SH',  # Š
        '\N{LATIN CAPITAL LETTER Z WITH CARON}': 'ZH',  # Ž
        # Cyrillic
        '\N{CYRILLIC SMALL LETTER A}': 'AA0',
        '\N{CYRILLIC SMALL LETTER BE}': 'B',
        '\N{CYRILLIC SMALL LETTER VE}': 'V',
        '\N{CYRILLIC SMALL LETTER GHE}': 'G',
        '\N{CYRILLIC SMALL LETTER GHE WITH UPTURN}': 'G',
        '\N{CYRILLIC SMALL LETTER DE}': 'D',
        '\N{CYRILLIC SMALL LETTER IE}': 'EH0',
        '\N{CYRILLIC SMALL LETTER BYELORUSSIAN-UKRAINIAN I}': 'IH0',
        '\N{CYRILLIC SMALL LETTER ZHE}': 'ZH',
        '\N{CYRILLIC SMALL LETTER ZE}': 'Z',
        '\N{CYRILLIC SMALL LETTER SHORT I}': 'IY0', # 'Y' ?
        '\N{CYRILLIC SMALL LETTER I}': 'IY0',
        '\N{CYRILLIC SMALL LETTER KA}': 'K',
        '\N{CYRILLIC SMALL LETTER EL}': 'L',
        '\N{CYRILLIC SMALL LETTER EM}': 'M',
        '\N{CYRILLIC SMALL LETTER EN}': 'N',
        '\N{CYRILLIC SMALL LETTER O}': 'AO0',
        '\N{CYRILLIC SMALL LETTER PE}': 'P',
        '\N{CYRILLIC SMALL LETTER ER}': 'R',
        '\N{CYRILLIC SMALL LETTER ES}': 'S',
        '\N{CYRILLIC SMALL LETTER TE}': 'T',
        '\N{CYRILLIC SMALL LETTER U}': 'UH0',
        '\N{CYRILLIC SMALL LETTER EF}': 'F',
        '\N{CYRILLIC SMALL LETTER HA}': 'HH', #  'Y'?? 'K'??
        '\N{CYRILLIC SMALL LETTER CHE}': 'CH',
        '\N{CYRILLIC SMALL LETTER SHA}': 'SH',
        '\N{CYRILLIC SMALL LETTER SHCHA}': 'SH',
        # u'\N{CYRILLIC SMALL LETTER SOFT SIGN}': 'Y',

        '\N{CYRILLIC CAPITAL LETTER A}': 'AA0',
        '\N{CYRILLIC CAPITAL LETTER BE}': 'B',
        '\N{CYRILLIC CAPITAL LETTER VE}': 'V',
        '\N{CYRILLIC CAPITAL LETTER GHE}': 'G',
        '\N{CYRILLIC CAPITAL LETTER GHE WITH UPTURN}': 'G',
        '\N{CYRILLIC CAPITAL LETTER DE}': 'D',
        '\N{CYRILLIC CAPITAL LETTER IE}': 'EH0',
        '\N{CYRILLIC CAPITAL LETTER BYELORUSSIAN-UKRAINIAN I}': 'IH0',
        '\N{CYRILLIC CAPITAL LETTER ZHE}': 'ZH',
        '\N{CYRILLIC CAPITAL LETTER ZE}': 'Z',
        '\N{CYRILLIC CAPITAL LETTER SHORT I}': 'IY0', # 'Y' ?
        '\N{CYRILLIC CAPITAL LETTER I}': 'IY0',
        '\N{CYRILLIC CAPITAL LETTER KA}': 'K',
        '\N{CYRILLIC CAPITAL LETTER EL}': 'L',
        '\N{CYRILLIC CAPITAL LETTER EM}': 'M',
        '\N{CYRILLIC CAPITAL LETTER EN}': 'N',
        '\N{CYRILLIC CAPITAL LETTER O}': 'AO0',
        '\N{CYRILLIC CAPITAL LETTER PE}': 'P',
        '\N{CYRILLIC CAPITAL LETTER ER}': 'R',
        '\N{CYRILLIC CAPITAL LETTER ES}': 'S',
        '\N{CYRILLIC CAPITAL LETTER TE}': 'T',
        '\N{CYRILLIC CAPITAL LETTER U}': 'UH0',
        '\N{CYRILLIC CAPITAL LETTER EF}': 'F',
        '\N{CYRILLIC CAPITAL LETTER HA}': 'HH', #  'Y'?? 'K'??
        '\N{CYRILLIC CAPITAL LETTER CHE}': 'CH',
        '\N{CYRILLIC CAPITAL LETTER SHA}': 'SH',
        '\N{CYRILLIC CAPITAL LETTER SHCHA}': 'SH',
        # u'\N{CYRILLIC CAPITAL LETTER SOFT SIGN}': 'Y',
    }
    easy_consonants = list(simple_convert.keys())
    pos = 0
    previous = ' '
    for letter in word:
        # if letter == previous and not isvowel(letter):  # double consonants
        #     pass
        if letter == 'c':
            if len(word) > pos+1 and word[pos+1] == 'h':
                phonemes.append('CH')
            else:
                pass
        elif letter == 'i':
            if previous == 'j':
                phonemes.append('IY0')
            else:
                phonemes.append('IH0')
        elif letter == 'h':
            if letter == 'h':
                if previous in ['z', 's', 'c']:
                    pass
                else:
                    phonemes.append('HH')
        elif letter == 's':
            if len(word) > pos+1 and word[pos+1] == 'h':
                phonemes.append('SH')
            else:
                phonemes.append('S')
        elif letter == 'u':
            if previous == 'j':
                phonemes.append('UW0')
            else:
                phonemes.append('UH0')
        elif letter == 'z':
            if len(word) > pos+1 and word[pos+1] == 'h':
                phonemes.append('ZH')
            else:
                phonemes.append('Z')
        elif letter == '\N{CYRILLIC SMALL LETTER SHCHA}':
            phonemes.append('SH')
            phonemes.append('CH')
        elif letter == '\N{CYRILLIC SMALL LETTER TSE}':
            phonemes.append('T')
            phonemes.append('S')
        elif letter == '\N{CYRILLIC SMALL LETTER YA}':
            phonemes.append('Y')
            phonemes.append('AO0') # not if unstressed - drop this line ?
        elif letter == '\N{CYRILLIC SMALL LETTER YU}':
            phonemes.append('Y')
            phonemes.append('UW0')
        elif letter == '\N{CYRILLIC SMALL LETTER YI}':
            phonemes.append('Y')
            phonemes.append('IY0')
        elif letter == '\N{CYRILLIC SMALL LETTER UKRAINIAN IE}':
            phonemes.append('Y')
            phonemes.append('EH0')
        elif letter == '\N{CYRILLIC CAPITAL LETTER SHCHA}':
            phonemes.append('SH')
            phonemes.append('CH')
        elif letter == '\N{CYRILLIC CAPITAL LETTER TSE}':
            phonemes.append('T')
            phonemes.append('S')
        elif letter == '\N{CYRILLIC CAPITAL LETTER YU}':
            if previous in vowels or previous == "'" or pos == 0:
                phonemes.append('Y')
                phonemes.append('UW0')
            else:
                phonemes.append('UH0')
        elif letter == '\N{CYRILLIC CAPITAL LETTER YA}':
            if previous in vowels or previous == "'" or pos == 0:
                phonemes.append('Y')
                phonemes.append('AO0') # not if unstressed - drop this line ?
            else:
                phonemes.append('AA0')
        elif letter == '\N{CYRILLIC CAPITAL LETTER YI}':
            phonemes.append('Y')
            phonemes.append('IY0')
        elif letter == '\N{CYRILLIC CAPITAL LETTER UKRAINIAN IE}':
            phonemes.append('Y')
            phonemes.append('EH0')
        elif letter in easy_consonants:
            phonemes.append(simple_convert[letter])
        elif letter == ' ':
            pass
        elif len(hammer(letter)) == 1:
            if not recursive:
                phon = breakdownWord(hammer(letter), True)
                if phon:
                    phonemes.append(phon[0])
        #~ else:
            #~ print "not handled", letter.encode(output_encoding), word.encode(output_encoding)
        pos += 1
        previous = letter
    # return " ".join(phonemes)
    # return phonemes
    temp_phonemes = []
    previous_phoneme = " "
    for phoneme in phonemes:
        if phoneme != previous_phoneme:
            temp_phonemes.append(phoneme)
        previous_phoneme = phoneme
    return temp_phonemes


if __name__ == "__main__":
    testwords = "på hänsyn Vsi ljudy narodžujut'sja vil'nymy i rivnymy u svojij hidnosti ta pravax. Vony nadileni rozumom i sovistju i povynni dijaty u vidnošenni odyn do odnoho v dusi braterstva.".split()
    testwordsC = "\N{CYRILLIC CAPITAL LETTER VE}"
    "\N{CYRILLIC SMALL LETTER ES}"
    "\N{CYRILLIC SMALL LETTER IE}"
    " "
    "\N{CYRILLIC SMALL LETTER EL}"
    "\N{CYRILLIC SMALL LETTER YU}"
    "\N{CYRILLIC SMALL LETTER DE}"
    "\N{CYRILLIC SMALL LETTER I}"
    " "
    "\N{CYRILLIC SMALL LETTER ER}"
    "\N{CYRILLIC SMALL LETTER O}"
    "\N{CYRILLIC SMALL LETTER ZHE}"
    "\N{CYRILLIC SMALL LETTER DE}"
    "\N{CYRILLIC SMALL LETTER A}"
    "\N{CYRILLIC SMALL LETTER YU}"
    "\N{CYRILLIC SMALL LETTER TE}"
    "\N{CYRILLIC SMALL LETTER ES}"
    "\N{CYRILLIC SMALL LETTER YA}"
    " "
    "\N{CYRILLIC SMALL LETTER ES}"
    "\N{CYRILLIC SMALL LETTER VE}"
    "\N{CYRILLIC SMALL LETTER O}"
    "\N{CYRILLIC SMALL LETTER BE}"
    "\N{CYRILLIC SMALL LETTER O}"
    "\N{CYRILLIC SMALL LETTER DE}"
    "\N{CYRILLIC SMALL LETTER EN}"
    "\N{CYRILLIC SMALL LETTER YERU}"
    "\N{CYRILLIC SMALL LETTER EM}"
    "\N{CYRILLIC SMALL LETTER I}"
    " "
    "\N{CYRILLIC SMALL LETTER I}"
    " "
    "\N{CYRILLIC SMALL LETTER ER}"
    "\N{CYRILLIC SMALL LETTER A}"
    "\N{CYRILLIC SMALL LETTER VE}"
    "\N{CYRILLIC SMALL LETTER EN}"
    "\N{CYRILLIC SMALL LETTER YERU}"
    "\N{CYRILLIC SMALL LETTER EM}"
    "\N{CYRILLIC SMALL LETTER I}"
    " "
    "\N{CYRILLIC SMALL LETTER VE}"
    " "
    "\N{CYRILLIC SMALL LETTER ES}"
    "\N{CYRILLIC SMALL LETTER VE}"
    "\N{CYRILLIC SMALL LETTER O}"
    "\N{CYRILLIC SMALL LETTER IE}"
    "\N{CYRILLIC SMALL LETTER EM}"
    " "
    "\N{CYRILLIC SMALL LETTER DE}"
    "\N{CYRILLIC SMALL LETTER O}"
    "\N{CYRILLIC SMALL LETTER ES}"
    "\N{CYRILLIC SMALL LETTER TE}"
    "\N{CYRILLIC SMALL LETTER O}"
    "\N{CYRILLIC SMALL LETTER I}"
    "\N{CYRILLIC SMALL LETTER EN}"
    "\N{CYRILLIC SMALL LETTER ES}"
    "\N{CYRILLIC SMALL LETTER TE}"
    "\N{CYRILLIC SMALL LETTER VE}"
    "\N{CYRILLIC SMALL LETTER IE}"
    " "
    "\N{CYRILLIC SMALL LETTER I}"
    " "
    "\N{CYRILLIC SMALL LETTER PE}"
    "\N{CYRILLIC SMALL LETTER ER}"
    "\N{CYRILLIC SMALL LETTER A}"
    "\N{CYRILLIC SMALL LETTER VE}"
    "\N{CYRILLIC SMALL LETTER A}"
    "\N{CYRILLIC SMALL LETTER HA}"
    " "
    "\N{CYRILLIC CAPITAL LETTER O}"
    "\N{CYRILLIC SMALL LETTER EN}"
    "\N{CYRILLIC SMALL LETTER I}"
    " "
    "\N{CYRILLIC SMALL LETTER EN}"
    "\N{CYRILLIC SMALL LETTER A}"
    "\N{CYRILLIC SMALL LETTER DE}"
    "\N{CYRILLIC SMALL LETTER IE}"
    "\N{CYRILLIC SMALL LETTER EL}"
    "\N{CYRILLIC SMALL LETTER IE}"
    "\N{CYRILLIC SMALL LETTER EN}"
    "\N{CYRILLIC SMALL LETTER YERU}"
    " "
    "\N{CYRILLIC SMALL LETTER ER}"
    "\N{CYRILLIC SMALL LETTER A}"
    "\N{CYRILLIC SMALL LETTER ZE}"
    "\N{CYRILLIC SMALL LETTER U}"
    "\N{CYRILLIC SMALL LETTER EM}"
    "\N{CYRILLIC SMALL LETTER O}"
    "\N{CYRILLIC SMALL LETTER EM}"
    " "
    "\N{CYRILLIC SMALL LETTER I}"
    " "
    "\N{CYRILLIC SMALL LETTER ES}"
    "\N{CYRILLIC SMALL LETTER O}"
    "\N{CYRILLIC SMALL LETTER VE}"
    "\N{CYRILLIC SMALL LETTER IE}"
    "\N{CYRILLIC SMALL LETTER ES}"
    "\N{CYRILLIC SMALL LETTER TE}"
    "\N{CYRILLIC SMALL LETTER SOFT SIGN}"
    "\N{CYRILLIC SMALL LETTER YU}"
    " "
    "\N{CYRILLIC SMALL LETTER I}"
    " "
    "\N{CYRILLIC SMALL LETTER DE}"
    "\N{CYRILLIC SMALL LETTER O}"
    "\N{CYRILLIC SMALL LETTER EL}"
    "\N{CYRILLIC SMALL LETTER ZHE}"
    "\N{CYRILLIC SMALL LETTER EN}"
    "\N{CYRILLIC SMALL LETTER YERU}"
    " "
    "\N{CYRILLIC SMALL LETTER PE}"
    "\N{CYRILLIC SMALL LETTER O}"
    "\N{CYRILLIC SMALL LETTER ES}"
    "\N{CYRILLIC SMALL LETTER TE}"
    "\N{CYRILLIC SMALL LETTER U}"
    "\N{CYRILLIC SMALL LETTER PE}"
    "\N{CYRILLIC SMALL LETTER A}"
    "\N{CYRILLIC SMALL LETTER TE}"
    "\N{CYRILLIC SMALL LETTER SOFT SIGN}"
    " "
    "\N{CYRILLIC SMALL LETTER VE}"
    " "
    "\N{CYRILLIC SMALL LETTER O}"
    "\N{CYRILLIC SMALL LETTER TE}"
    "\N{CYRILLIC SMALL LETTER EN}"
    "\N{CYRILLIC SMALL LETTER O}"
    "\N{CYRILLIC SMALL LETTER SHA}"
    "\N{CYRILLIC SMALL LETTER IE}"
    "\N{CYRILLIC SMALL LETTER EN}"
    "\N{CYRILLIC SMALL LETTER I}"
    "\N{CYRILLIC SMALL LETTER I}"
    " "
    "\N{CYRILLIC SMALL LETTER DE}"
    "\N{CYRILLIC SMALL LETTER ER}"
    "\N{CYRILLIC SMALL LETTER U}"
    "\N{CYRILLIC SMALL LETTER GHE}"
    " "
    "\N{CYRILLIC SMALL LETTER DE}"
    "\N{CYRILLIC SMALL LETTER ER}"
    "\N{CYRILLIC SMALL LETTER U}"
    "\N{CYRILLIC SMALL LETTER GHE}"
    "\N{CYRILLIC SMALL LETTER A}"
    " "
    "\N{CYRILLIC SMALL LETTER VE}"
    " "
    "\N{CYRILLIC SMALL LETTER DE}"
    "\N{CYRILLIC SMALL LETTER U}"
    "\N{CYRILLIC SMALL LETTER HA}"
    "\N{CYRILLIC SMALL LETTER IE}"
    " "
    "\N{CYRILLIC SMALL LETTER BE}"
    "\N{CYRILLIC SMALL LETTER ER}"
    "\N{CYRILLIC SMALL LETTER A}"
    "\N{CYRILLIC SMALL LETTER TE}"
    "\N{CYRILLIC SMALL LETTER ES}"
    "\N{CYRILLIC SMALL LETTER TE}"
    "\N{CYRILLIC SMALL LETTER VE}"
    "\N{CYRILLIC SMALL LETTER A}".split()
    #~ for word in testwordsC:
        #~ print word, breakdownWord(unicode(word, input_encoding))
    #~ for word in testwords:
        #~ print word, breakdownWord(unicode(word, input_encoding))
