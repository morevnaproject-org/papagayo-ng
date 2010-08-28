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

from unicode_hammer import latin1_to_ascii as hammer

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
        u'\N{CYRILLIC SMALL LETTER A}',  # looks like normal a
        # u'\N{CYRILLIC SMALL LETTER IE}',  # looks like normal e
        u'\N{CYRILLIC SMALL LETTER UKRAINIAN IE}', # looks something like small Euro symbol with one cross-piece
        u'\N{CYRILLIC SMALL LETTER BYELORUSSIAN-UKRAINIAN I}',  # looks like normal i
        # u'\N{CYRILLIC SMALL LETTER YI}',  # i with diaresis
        u'\N{CYRILLIC SMALL LETTER I}',  # looks like small backwards capital N
        u'\N{CYRILLIC SMALL LETTER SHORT I}',  # looks like small backwards capital N with tilde
        u'\N{CYRILLIC SMALL LETTER O}',  # looks like normal o
        u'\N{CYRILLIC SMALL LETTER U}',  # looks like normal y
        u'\N{CYRILLIC CAPITAL LETTER A}',  # looks like normal A
        # u'\N{CYRILLIC CAPITAL LETTER IE}',  # looks like normal E
        u'\N{CYRILLIC CAPITAL LETTER UKRAINIAN IE}', # looks something like Euro symbol with one cross-piece
        u'\N{CYRILLIC CAPITAL LETTER BYELORUSSIAN-UKRAINIAN I}',  # looks like normal I
        # u'\N{CYRILLIC CAPITAL LETTER YI}',  # I with diaresis
        u'\N{CYRILLIC CAPITAL LETTER I}',  # looks like backwards capital N
        u'\N{CYRILLIC CAPITAL LETTER SHORT I}',  # looks like backwards capital N with tilde
        u'\N{CYRILLIC CAPITAL LETTER O}',  # looks like normal O
        u'\N{CYRILLIC CAPITAL LETTER U}',  # looks like normal Y
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
        u'\N{LATIN SMALL LETTER S WITH CARON}': 'SH',  # š
        u'\N{LATIN SMALL LETTER Z WITH CARON}': 'ZH',  # ž
        u'\N{LATIN CAPITAL LETTER S WITH CARON}': 'SH',  # Š
        u'\N{LATIN CAPITAL LETTER Z WITH CARON}': 'ZH',  # Ž
        # Cyrillic
        u'\N{CYRILLIC SMALL LETTER A}': 'AA0',
        u'\N{CYRILLIC SMALL LETTER BE}': 'B',
        u'\N{CYRILLIC SMALL LETTER VE}': 'V',
        u'\N{CYRILLIC SMALL LETTER GHE}': 'G',
        u'\N{CYRILLIC SMALL LETTER GHE WITH UPTURN}': 'G',
        u'\N{CYRILLIC SMALL LETTER DE}': 'D',
        u'\N{CYRILLIC SMALL LETTER IE}': 'EH0',
        u'\N{CYRILLIC SMALL LETTER BYELORUSSIAN-UKRAINIAN I}': 'IH0',
        u'\N{CYRILLIC SMALL LETTER ZHE}': 'ZH',
        u'\N{CYRILLIC SMALL LETTER ZE}': 'Z',
        u'\N{CYRILLIC SMALL LETTER SHORT I}': 'IY0', # 'Y' ?
        u'\N{CYRILLIC SMALL LETTER I}': 'IY0',
        u'\N{CYRILLIC SMALL LETTER KA}': 'K',
        u'\N{CYRILLIC SMALL LETTER EL}': 'L',
        u'\N{CYRILLIC SMALL LETTER EM}': 'M',
        u'\N{CYRILLIC SMALL LETTER EN}': 'N',
        u'\N{CYRILLIC SMALL LETTER O}': 'AO0',
        u'\N{CYRILLIC SMALL LETTER PE}': 'P',
        u'\N{CYRILLIC SMALL LETTER ER}': 'R',
        u'\N{CYRILLIC SMALL LETTER ES}': 'S',
        u'\N{CYRILLIC SMALL LETTER TE}': 'T',
        u'\N{CYRILLIC SMALL LETTER U}': 'UH0',
        u'\N{CYRILLIC SMALL LETTER EF}': 'F',
        u'\N{CYRILLIC SMALL LETTER HA}': 'HH', #  'Y'?? 'K'??
        u'\N{CYRILLIC SMALL LETTER CHE}': 'CH',
        u'\N{CYRILLIC SMALL LETTER SHA}': 'SH',
        u'\N{CYRILLIC SMALL LETTER SHCHA}': 'SH',
        # u'\N{CYRILLIC SMALL LETTER SOFT SIGN}': 'Y',

        u'\N{CYRILLIC CAPITAL LETTER A}': 'AA0',
        u'\N{CYRILLIC CAPITAL LETTER BE}': 'B',
        u'\N{CYRILLIC CAPITAL LETTER VE}': 'V',
        u'\N{CYRILLIC CAPITAL LETTER GHE}': 'G',
        u'\N{CYRILLIC CAPITAL LETTER GHE WITH UPTURN}': 'G',
        u'\N{CYRILLIC CAPITAL LETTER DE}': 'D',
        u'\N{CYRILLIC CAPITAL LETTER IE}': 'EH0',
        u'\N{CYRILLIC CAPITAL LETTER BYELORUSSIAN-UKRAINIAN I}': 'IH0',
        u'\N{CYRILLIC CAPITAL LETTER ZHE}': 'ZH',
        u'\N{CYRILLIC CAPITAL LETTER ZE}': 'Z',
        u'\N{CYRILLIC CAPITAL LETTER SHORT I}': 'IY0', # 'Y' ?
        u'\N{CYRILLIC CAPITAL LETTER I}': 'IY0',
        u'\N{CYRILLIC CAPITAL LETTER KA}': 'K',
        u'\N{CYRILLIC CAPITAL LETTER EL}': 'L',
        u'\N{CYRILLIC CAPITAL LETTER EM}': 'M',
        u'\N{CYRILLIC CAPITAL LETTER EN}': 'N',
        u'\N{CYRILLIC CAPITAL LETTER O}': 'AO0',
        u'\N{CYRILLIC CAPITAL LETTER PE}': 'P',
        u'\N{CYRILLIC CAPITAL LETTER ER}': 'R',
        u'\N{CYRILLIC CAPITAL LETTER ES}': 'S',
        u'\N{CYRILLIC CAPITAL LETTER TE}': 'T',
        u'\N{CYRILLIC CAPITAL LETTER U}': 'UH0',
        u'\N{CYRILLIC CAPITAL LETTER EF}': 'F',
        u'\N{CYRILLIC CAPITAL LETTER HA}': 'HH', #  'Y'?? 'K'??
        u'\N{CYRILLIC CAPITAL LETTER CHE}': 'CH',
        u'\N{CYRILLIC CAPITAL LETTER SHA}': 'SH',
        u'\N{CYRILLIC CAPITAL LETTER SHCHA}': 'SH',
        # u'\N{CYRILLIC CAPITAL LETTER SOFT SIGN}': 'Y',
    }
    easy_consonants = simple_convert.keys()
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
        elif letter == u'\N{CYRILLIC SMALL LETTER SHCHA}':
            phonemes.append('SH')
            phonemes.append('CH')
        elif letter == u'\N{CYRILLIC SMALL LETTER TSE}':
            phonemes.append('T')
            phonemes.append('S')
        elif letter == u'\N{CYRILLIC SMALL LETTER YA}':
            phonemes.append('Y')
            phonemes.append('AO0') # not if unstressed - drop this line ?
        elif letter == u'\N{CYRILLIC SMALL LETTER YU}':
            phonemes.append('Y')
            phonemes.append('UW0')
        elif letter == u'\N{CYRILLIC SMALL LETTER YI}':
            phonemes.append('Y')
            phonemes.append('IY0')
        elif letter == u'\N{CYRILLIC SMALL LETTER UKRAINIAN IE}':
            phonemes.append('Y')
            phonemes.append('EH0')
        elif letter == u'\N{CYRILLIC CAPITAL LETTER SHCHA}':
            phonemes.append('SH')
            phonemes.append('CH')
        elif letter == u'\N{CYRILLIC CAPITAL LETTER TSE}':
            phonemes.append('T')
            phonemes.append('S')
        elif letter == u'\N{CYRILLIC CAPITAL LETTER YU}':
            if previous in vowels or previous == "'" or pos == 0:
                phonemes.append('Y')
                phonemes.append('UW0')
            else:
                phonemes.append('UH0')
        elif letter == u'\N{CYRILLIC CAPITAL LETTER YA}':
            if previous in vowels or previous == "'" or pos == 0:
                phonemes.append('Y')
                phonemes.append('AO0') # not if unstressed - drop this line ?
            else:
                phonemes.append('AA0')
        elif letter == u'\N{CYRILLIC CAPITAL LETTER YI}':
            phonemes.append('Y')
            phonemes.append('IY0')
        elif letter == u'\N{CYRILLIC CAPITAL LETTER UKRAINIAN IE}':
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
