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

"""functions to take an Russian word and return a list of phonemes
"""

from .unicode_hammer import latin1_to_ascii as hammer

import locale, re

output_encoding = 'utf-16'

input_encoding = locale.getdefaultlocale()[1] # standard system encoding??
# input_encoding = 'cp1252'
# input_encoding = 'utf-8'
# input_encoding = 'utf-16'
# input_encoding = 'koi8-r'  # cyrillic
# input_encoding = 'latin-1'
# input_encoding = 'iso-8859-1'

def breakdownWord(word, recursive=False):
    word = word.lower()
    phonemes = []
    simple_convert = {
        'a': 'AA0',
        'b': 'B',
        'd': 'D',
        'f': 'F',
        'h': 'HH',
        'i': 'IY0',
        'j': 'IY0',
        'k': 'K',
        'l': 'L',
        'm': 'M',
        'n': 'N',
        'o': 'AO0',
        'p': 'P',
        'r': 'R',
        't': 'T',
        'u': 'UW0',
        'v': 'V',
        'x': 'HH',  # use 'Y' ?? 'K'??
        '\N{LATIN SMALL LETTER S WITH CARON}': 'SH',  # š
        '\N{LATIN SMALL LETTER Z WITH CARON}': 'ZH',  # ž
        '\N{LATIN CAPITAL LETTER S WITH CARON}': 'SH',  # Š
        '\N{LATIN CAPITAL LETTER Z WITH CARON}': 'ZH',  # Ž
        # Cyrillic
        '\N{CYRILLIC SMALL LETTER A}': 'AA0',
        '\N{CYRILLIC SMALL LETTER BE}': 'B',
        '\N{CYRILLIC SMALL LETTER VE}': 'V',
        '\N{CYRILLIC SMALL LETTER CHE}': 'CH',
        '\N{CYRILLIC SMALL LETTER DE}': 'D',
        '\N{CYRILLIC SMALL LETTER E}': 'EH0',
        '\N{CYRILLIC SMALL LETTER EF}': 'F',
        '\N{CYRILLIC SMALL LETTER GHE}': 'G',
        '\N{CYRILLIC SMALL LETTER I}': 'IY0',
        '\N{CYRILLIC SMALL LETTER HA}': 'HH', #  'Y'?? 'K'??
        '\N{CYRILLIC SMALL LETTER SHORT I}': 'IY0',
        '\N{CYRILLIC SMALL LETTER KA}': 'K',
        '\N{CYRILLIC SMALL LETTER EL}': 'L',
        '\N{CYRILLIC SMALL LETTER EM}': 'M',
        '\N{CYRILLIC SMALL LETTER EN}': 'N',
        '\N{CYRILLIC SMALL LETTER O}': 'AO0',
        '\N{CYRILLIC SMALL LETTER PE}': 'P',
        '\N{CYRILLIC SMALL LETTER ER}': 'R',
        '\N{CYRILLIC SMALL LETTER ES}': 'S',
        '\N{CYRILLIC SMALL LETTER SHA}': 'SH',
        '\N{CYRILLIC SMALL LETTER TE}': 'T',
        '\N{CYRILLIC SMALL LETTER U}': 'UW0',
        '\N{CYRILLIC SMALL LETTER HARD SIGN}': '',
        '\N{CYRILLIC SMALL LETTER SOFT SIGN}': '',
        '\N{CYRILLIC SMALL LETTER YERU}': 'IH0',
        '\N{CYRILLIC SMALL LETTER ZHE}': 'ZH',
        '\N{CYRILLIC SMALL LETTER ZE}': 'Z',

        '\N{CYRILLIC CAPITAL LETTER A}': 'AA0',
        '\N{CYRILLIC CAPITAL LETTER BE}': 'B',
        '\N{CYRILLIC CAPITAL LETTER VE}': 'V',
        '\N{CYRILLIC CAPITAL LETTER CHE}': 'CH',
        '\N{CYRILLIC CAPITAL LETTER DE}': 'D',
        '\N{CYRILLIC CAPITAL LETTER E}': 'EH0',
        '\N{CYRILLIC CAPITAL LETTER EF}': 'F',
        '\N{CYRILLIC CAPITAL LETTER GHE}': 'G',
        '\N{CYRILLIC CAPITAL LETTER I}': 'IY0',
        '\N{CYRILLIC CAPITAL LETTER HA}': 'HH', #  'Y'?? 'K'??
        '\N{CYRILLIC CAPITAL LETTER SHORT I}': 'IY0',
        '\N{CYRILLIC CAPITAL LETTER KA}': 'K',
        '\N{CYRILLIC CAPITAL LETTER EL}': 'L',
        '\N{CYRILLIC CAPITAL LETTER EM}': 'M',
        '\N{CYRILLIC CAPITAL LETTER EN}': 'N',
        '\N{CYRILLIC CAPITAL LETTER O}': 'AO0',
        '\N{CYRILLIC CAPITAL LETTER PE}': 'P',
        '\N{CYRILLIC CAPITAL LETTER ER}': 'R',
        '\N{CYRILLIC CAPITAL LETTER ES}': 'S',
        '\N{CYRILLIC CAPITAL LETTER SHA}': 'SH',
        '\N{CYRILLIC CAPITAL LETTER TE}': 'T',
        '\N{CYRILLIC CAPITAL LETTER U}': 'UW0',
        '\N{CYRILLIC CAPITAL LETTER HARD SIGN}': '',
        '\N{CYRILLIC CAPITAL LETTER SOFT SIGN}': '',
        '\N{CYRILLIC CAPITAL LETTER YERU}': 'IH0',
        '\N{CYRILLIC CAPITAL LETTER ZHE}': 'ZH',
        '\N{CYRILLIC CAPITAL LETTER ZE}': 'Z',
    }
    easy_consonants = list(simple_convert.keys())
    pos = 0
    previous = ' '
    for letter in word:
        # if letter == previous and not isvowel(letter):  # double consonants
        #     pass
        if letter == 'c':
            if previous == 's' and len(word) > pos+1 and word[pos+1] == 'h':
                phonemes.append('SH')  # as in
                phonemes.append('CH')  #       freSH CHeese
            elif len(word) > pos+1 and word[pos+1] == 'h':
                phonemes.append('CH')
            else:
                phonemes.append('T')
                phonemes.append('S')
        elif letter == 'b' and len(word) == pos+1:
            phonemes.append('P')
        elif letter == 'd' and len(word) == pos+1:
            phonemes.append('T')
        elif letter in  ['e', '\N{CYRILLIC SMALL LETTER IE}']:
            if pos == 0:
                phonemes.append('Y')
                phonemes.append('EH0')
            if len(word) > pos+1 and word[pos+1] in ['h', '^']:
                phonemes.append('EH0')
            else:
                phonemes.append('EH0')
        elif letter =='^':
            pass
        elif letter == 'g':
            if len(word) == pos+1:
                phonemes.append('K')
            elif previous in ['e', 'o'] and len(word) == pos+2 and word[pos+1] == 'o':
                phonemes.append('V')  # possessive endings -ogo and -ego
            else:
                phonemes.append('G')
        elif letter == 'h':
            pass
        elif letter == 's':
            if len(word) > pos+1 and word[pos+1] == 'h':
                phonemes.append('SH')
            else:
                phonemes.append('S')
        elif letter == 'v' and len(word) == pos+1:
            phonemes.append('F')
        elif letter == 'y':
            if len(word) > pos+1 and word[pos+1] == 'a':
                phonemes.append('Y')
            else:
                phonemes.append('IH0')
        elif letter == 'z':
            if len(word) > pos+1 and word[pos+1] == 'h':
                if len(word) == pos+2:
                    phonemes.append('SH')
                else:
                    phonemes.append('ZH')
            else:
                if len(word) == pos+1:
                    phonemes.append('S')
                else:
                    phonemes.append('Z')
        elif letter in [ '\N{CYRILLIC CAPITAL LETTER SHCHA}', '\N{CYRILLIC SMALL LETTER SHCHA}' ]:
            phonemes.append('SH')
            #phonemes.append('CH')
        elif letter in [ '\N{CYRILLIC CAPITAL LETTER TSE}' , '\N{CYRILLIC SMALL LETTER TSE}' ]:
            phonemes.append('T')
            phonemes.append('S')
        elif letter == '\N{CYRILLIC CAPITAL LETTER YA}' or letter == '\N{CYRILLIC SMALL LETTER YA}':
            if pos==0:
                phonemes.append('IY0')
            phonemes.append('AA1')
        elif letter == '\N{CYRILLIC CAPITAL LETTER YU}' or letter == '\N{CYRILLIC SMALL LETTER YU}':
            if pos==0:
                phonemes.append('Y')
            phonemes.append('UW0')
        elif letter in ['\N{LATIN SMALL LETTER E WITH DIAERESIS}', '\N{CYRILLIC SMALL LETTER IO}']:
            if pos==0:
                phonemes.append('Y')
            phonemes.append('AO0')
        elif letter in easy_consonants:
            phonemes.append(simple_convert[letter])
        elif letter == ' ':
            pass
        elif len(hammer(letter)) == 1:
            if not recursive:
                phon = breakdownWord(hammer(letter), True)
                if phon:
                    phonemes.append(phon)
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
    testwords = "égaux Vse ljudi roždajutsya svobodnymi i ravnymi v svoem dostoinstve i pravah Oni nadeleny razumom i sovest'ju i dolžny postupat' v otnošenii drug druga v duhe bratstva".split()
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
