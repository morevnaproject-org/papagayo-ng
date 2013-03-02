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

from unicode_hammer import latin1_to_ascii as hammer

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
        u'\N{LATIN SMALL LETTER S WITH CARON}': 'SH',  # š
        u'\N{LATIN SMALL LETTER Z WITH CARON}': 'ZH',  # ž
        u'\N{LATIN CAPITAL LETTER S WITH CARON}': 'SH',  # Š
        u'\N{LATIN CAPITAL LETTER Z WITH CARON}': 'ZH',  # Ž
        # Cyrillic
        u'\N{CYRILLIC SMALL LETTER A}': 'AA0',
        u'\N{CYRILLIC SMALL LETTER BE}': 'B',
        u'\N{CYRILLIC SMALL LETTER VE}': 'V',
        u'\N{CYRILLIC SMALL LETTER CHE}': 'CH',
        u'\N{CYRILLIC SMALL LETTER DE}': 'D',
        u'\N{CYRILLIC SMALL LETTER E}': 'EH0',
        u'\N{CYRILLIC SMALL LETTER EF}': 'F',
        u'\N{CYRILLIC SMALL LETTER GHE}': 'G',
        u'\N{CYRILLIC SMALL LETTER I}': 'IY0',
        u'\N{CYRILLIC SMALL LETTER HA}': 'HH', #  'Y'?? 'K'??
        u'\N{CYRILLIC SMALL LETTER SHORT I}': 'IY0',
        u'\N{CYRILLIC SMALL LETTER KA}': 'K',
        u'\N{CYRILLIC SMALL LETTER EL}': 'L',
        u'\N{CYRILLIC SMALL LETTER EM}': 'M',
        u'\N{CYRILLIC SMALL LETTER EN}': 'N',
        u'\N{CYRILLIC SMALL LETTER O}': 'AO0',
        u'\N{CYRILLIC SMALL LETTER PE}': 'P',
        u'\N{CYRILLIC SMALL LETTER ER}': 'R',
        u'\N{CYRILLIC SMALL LETTER ES}': 'S',
        u'\N{CYRILLIC SMALL LETTER SHA}': 'SH',
        u'\N{CYRILLIC SMALL LETTER TE}': 'T',
        u'\N{CYRILLIC SMALL LETTER U}': 'UW0',
        u'\N{CYRILLIC SMALL LETTER HARD SIGN}': 'Y',
        u'\N{CYRILLIC SMALL LETTER SOFT SIGN}': 'Y',
        u'\N{CYRILLIC SMALL LETTER YERU}': 'IH0',
        u'\N{CYRILLIC SMALL LETTER ZHE}': 'ZH',
        u'\N{CYRILLIC SMALL LETTER ZE}': 'Z',

        u'\N{CYRILLIC CAPITAL LETTER A}': 'AA0',
        u'\N{CYRILLIC CAPITAL LETTER BE}': 'B',
        u'\N{CYRILLIC CAPITAL LETTER VE}': 'V',
        u'\N{CYRILLIC CAPITAL LETTER CHE}': 'CH',
        u'\N{CYRILLIC CAPITAL LETTER DE}': 'D',
        u'\N{CYRILLIC CAPITAL LETTER E}': 'EH0',
        u'\N{CYRILLIC CAPITAL LETTER EF}': 'F',
        u'\N{CYRILLIC CAPITAL LETTER GHE}': 'G',
        u'\N{CYRILLIC CAPITAL LETTER I}': 'IY0',
        u'\N{CYRILLIC CAPITAL LETTER HA}': 'HH', #  'Y'?? 'K'??
        u'\N{CYRILLIC CAPITAL LETTER SHORT I}': 'IY0',
        u'\N{CYRILLIC CAPITAL LETTER KA}': 'K',
        u'\N{CYRILLIC CAPITAL LETTER EL}': 'L',
        u'\N{CYRILLIC CAPITAL LETTER EM}': 'M',
        u'\N{CYRILLIC CAPITAL LETTER EN}': 'N',
        u'\N{CYRILLIC CAPITAL LETTER O}': 'AO0',
        u'\N{CYRILLIC CAPITAL LETTER PE}': 'P',
        u'\N{CYRILLIC CAPITAL LETTER ER}': 'R',
        u'\N{CYRILLIC CAPITAL LETTER ES}': 'S',
        u'\N{CYRILLIC CAPITAL LETTER SHA}': 'SH',
        u'\N{CYRILLIC CAPITAL LETTER TE}': 'T',
        u'\N{CYRILLIC CAPITAL LETTER U}': 'UW0',
        u'\N{CYRILLIC CAPITAL LETTER HARD SIGN}': 'Y',
        u'\N{CYRILLIC CAPITAL LETTER SOFT SIGN}': 'Y',
        u'\N{CYRILLIC CAPITAL LETTER YERU}': 'IH0',
        u'\N{CYRILLIC CAPITAL LETTER ZHE}': 'ZH',
        u'\N{CYRILLIC CAPITAL LETTER ZE}': 'Z',
    }
    easy_consonants = simple_convert.keys()
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
        elif letter in  ['e', u'\N{CYRILLIC SMALL LETTER IE}']:
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
        elif letter in [ u'\N{CYRILLIC CAPITAL LETTER SHCHA}', u'\N{CYRILLIC SMALL LETTER SHCHA}' ]:
            phonemes.append('SH')
            #phonemes.append('CH')
        elif letter in [ u'\N{CYRILLIC CAPITAL LETTER TSE}' , u'\N{CYRILLIC SMALL LETTER TSE}' ]:
            phonemes.append('T')
            phonemes.append('S')
        elif letter == u'\N{CYRILLIC CAPITAL LETTER YA}' or letter == u'\N{CYRILLIC SMALL LETTER YA}':
			if pos==0:
				phonemes.append('IY0')
			phonemes.append('AA1')
        elif letter == u'\N{CYRILLIC CAPITAL LETTER YU}' or letter == u'\N{CYRILLIC SMALL LETTER YU}':
			if pos==0:
				phonemes.append('Y')
			phonemes.append('UW0')
        elif letter in [u'\N{LATIN SMALL LETTER E WITH DIAERESIS}', u'\N{CYRILLIC SMALL LETTER IO}']:
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
    testwordsC = u"\N{CYRILLIC CAPITAL LETTER VE}"
    u"\N{CYRILLIC SMALL LETTER ES}"
    u"\N{CYRILLIC SMALL LETTER IE}"
    u" "
    u"\N{CYRILLIC SMALL LETTER EL}"
    u"\N{CYRILLIC SMALL LETTER YU}"
    u"\N{CYRILLIC SMALL LETTER DE}"
    u"\N{CYRILLIC SMALL LETTER I}"
    u" "
    u"\N{CYRILLIC SMALL LETTER ER}"
    u"\N{CYRILLIC SMALL LETTER O}"
    u"\N{CYRILLIC SMALL LETTER ZHE}"
    u"\N{CYRILLIC SMALL LETTER DE}"
    u"\N{CYRILLIC SMALL LETTER A}"
    u"\N{CYRILLIC SMALL LETTER YU}"
    u"\N{CYRILLIC SMALL LETTER TE}"
    u"\N{CYRILLIC SMALL LETTER ES}"
    u"\N{CYRILLIC SMALL LETTER YA}"
    u" "
    u"\N{CYRILLIC SMALL LETTER ES}"
    u"\N{CYRILLIC SMALL LETTER VE}"
    u"\N{CYRILLIC SMALL LETTER O}"
    u"\N{CYRILLIC SMALL LETTER BE}"
    u"\N{CYRILLIC SMALL LETTER O}"
    u"\N{CYRILLIC SMALL LETTER DE}"
    u"\N{CYRILLIC SMALL LETTER EN}"
    u"\N{CYRILLIC SMALL LETTER YERU}"
    u"\N{CYRILLIC SMALL LETTER EM}"
    u"\N{CYRILLIC SMALL LETTER I}"
    u" "
    u"\N{CYRILLIC SMALL LETTER I}"
    u" "
    u"\N{CYRILLIC SMALL LETTER ER}"
    u"\N{CYRILLIC SMALL LETTER A}"
    u"\N{CYRILLIC SMALL LETTER VE}"
    u"\N{CYRILLIC SMALL LETTER EN}"
    u"\N{CYRILLIC SMALL LETTER YERU}"
    u"\N{CYRILLIC SMALL LETTER EM}"
    u"\N{CYRILLIC SMALL LETTER I}"
    u" "
    u"\N{CYRILLIC SMALL LETTER VE}"
    u" "
    u"\N{CYRILLIC SMALL LETTER ES}"
    u"\N{CYRILLIC SMALL LETTER VE}"
    u"\N{CYRILLIC SMALL LETTER O}"
    u"\N{CYRILLIC SMALL LETTER IE}"
    u"\N{CYRILLIC SMALL LETTER EM}"
    u" "
    u"\N{CYRILLIC SMALL LETTER DE}"
    u"\N{CYRILLIC SMALL LETTER O}"
    u"\N{CYRILLIC SMALL LETTER ES}"
    u"\N{CYRILLIC SMALL LETTER TE}"
    u"\N{CYRILLIC SMALL LETTER O}"
    u"\N{CYRILLIC SMALL LETTER I}"
    u"\N{CYRILLIC SMALL LETTER EN}"
    u"\N{CYRILLIC SMALL LETTER ES}"
    u"\N{CYRILLIC SMALL LETTER TE}"
    u"\N{CYRILLIC SMALL LETTER VE}"
    u"\N{CYRILLIC SMALL LETTER IE}"
    u" "
    u"\N{CYRILLIC SMALL LETTER I}"
    u" "
    u"\N{CYRILLIC SMALL LETTER PE}"
    u"\N{CYRILLIC SMALL LETTER ER}"
    u"\N{CYRILLIC SMALL LETTER A}"
    u"\N{CYRILLIC SMALL LETTER VE}"
    u"\N{CYRILLIC SMALL LETTER A}"
    u"\N{CYRILLIC SMALL LETTER HA}"
    u" "
    u"\N{CYRILLIC CAPITAL LETTER O}"
    u"\N{CYRILLIC SMALL LETTER EN}"
    u"\N{CYRILLIC SMALL LETTER I}"
    u" "
    u"\N{CYRILLIC SMALL LETTER EN}"
    u"\N{CYRILLIC SMALL LETTER A}"
    u"\N{CYRILLIC SMALL LETTER DE}"
    u"\N{CYRILLIC SMALL LETTER IE}"
    u"\N{CYRILLIC SMALL LETTER EL}"
    u"\N{CYRILLIC SMALL LETTER IE}"
    u"\N{CYRILLIC SMALL LETTER EN}"
    u"\N{CYRILLIC SMALL LETTER YERU}"
    u" "
    u"\N{CYRILLIC SMALL LETTER ER}"
    u"\N{CYRILLIC SMALL LETTER A}"
    u"\N{CYRILLIC SMALL LETTER ZE}"
    u"\N{CYRILLIC SMALL LETTER U}"
    u"\N{CYRILLIC SMALL LETTER EM}"
    u"\N{CYRILLIC SMALL LETTER O}"
    u"\N{CYRILLIC SMALL LETTER EM}"
    u" "
    u"\N{CYRILLIC SMALL LETTER I}"
    u" "
    u"\N{CYRILLIC SMALL LETTER ES}"
    u"\N{CYRILLIC SMALL LETTER O}"
    u"\N{CYRILLIC SMALL LETTER VE}"
    u"\N{CYRILLIC SMALL LETTER IE}"
    u"\N{CYRILLIC SMALL LETTER ES}"
    u"\N{CYRILLIC SMALL LETTER TE}"
    u"\N{CYRILLIC SMALL LETTER SOFT SIGN}"
    u"\N{CYRILLIC SMALL LETTER YU}"
    u" "
    u"\N{CYRILLIC SMALL LETTER I}"
    u" "
    u"\N{CYRILLIC SMALL LETTER DE}"
    u"\N{CYRILLIC SMALL LETTER O}"
    u"\N{CYRILLIC SMALL LETTER EL}"
    u"\N{CYRILLIC SMALL LETTER ZHE}"
    u"\N{CYRILLIC SMALL LETTER EN}"
    u"\N{CYRILLIC SMALL LETTER YERU}"
    u" "
    u"\N{CYRILLIC SMALL LETTER PE}"
    u"\N{CYRILLIC SMALL LETTER O}"
    u"\N{CYRILLIC SMALL LETTER ES}"
    u"\N{CYRILLIC SMALL LETTER TE}"
    u"\N{CYRILLIC SMALL LETTER U}"
    u"\N{CYRILLIC SMALL LETTER PE}"
    u"\N{CYRILLIC SMALL LETTER A}"
    u"\N{CYRILLIC SMALL LETTER TE}"
    u"\N{CYRILLIC SMALL LETTER SOFT SIGN}"
    u" "
    u"\N{CYRILLIC SMALL LETTER VE}"
    u" "
    u"\N{CYRILLIC SMALL LETTER O}"
    u"\N{CYRILLIC SMALL LETTER TE}"
    u"\N{CYRILLIC SMALL LETTER EN}"
    u"\N{CYRILLIC SMALL LETTER O}"
    u"\N{CYRILLIC SMALL LETTER SHA}"
    u"\N{CYRILLIC SMALL LETTER IE}"
    u"\N{CYRILLIC SMALL LETTER EN}"
    u"\N{CYRILLIC SMALL LETTER I}"
    u"\N{CYRILLIC SMALL LETTER I}"
    u" "
    u"\N{CYRILLIC SMALL LETTER DE}"
    u"\N{CYRILLIC SMALL LETTER ER}"
    u"\N{CYRILLIC SMALL LETTER U}"
    u"\N{CYRILLIC SMALL LETTER GHE}"
    u" "
    u"\N{CYRILLIC SMALL LETTER DE}"
    u"\N{CYRILLIC SMALL LETTER ER}"
    u"\N{CYRILLIC SMALL LETTER U}"
    u"\N{CYRILLIC SMALL LETTER GHE}"
    u"\N{CYRILLIC SMALL LETTER A}"
    u" "
    u"\N{CYRILLIC SMALL LETTER VE}"
    u" "
    u"\N{CYRILLIC SMALL LETTER DE}"
    u"\N{CYRILLIC SMALL LETTER U}"
    u"\N{CYRILLIC SMALL LETTER HA}"
    u"\N{CYRILLIC SMALL LETTER IE}"
    u" "
    u"\N{CYRILLIC SMALL LETTER BE}"
    u"\N{CYRILLIC SMALL LETTER ER}"
    u"\N{CYRILLIC SMALL LETTER A}"
    u"\N{CYRILLIC SMALL LETTER TE}"
    u"\N{CYRILLIC SMALL LETTER ES}"
    u"\N{CYRILLIC SMALL LETTER TE}"
    u"\N{CYRILLIC SMALL LETTER VE}"
    u"\N{CYRILLIC SMALL LETTER A}".split()
    #~ for word in testwordsC:
        #~ print word, breakdownWord(unicode(word, input_encoding))
    #~ for word in testwords:
        #~ print word, breakdownWord(unicode(word, input_encoding))
