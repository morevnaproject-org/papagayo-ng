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

"""functions to take an Finnish word and return a list of phonemes
"""

from unicode_hammer import latin1_to_ascii as hammer

import locale, re
input_encoding = locale.getdefaultlocale()[1] # standard system encoding??
# input_encoding = 'cp1252'
# input_encoding = 'utf-8'
# input_encoding = 'utf-16'
# input_encoding = 'latin-1'
# input_encoding = 'iso-8859-1'

def breakdownWord(word, recursive=False):
    word = word.lower()
    # isvowel = dict.fromkeys('aeiouáéíóúàèìòùâêîôû').has_key
    phonemes = []
    simple_convert = {
        'd': 'D',
        'h': 'HH',
        'j': 'Y',
        'k': 'K',
        'l': 'L',
        'm': 'M',
        'p': 'P',
        'r': 'R',
        's': 'S',
        't': 'T',
        'v': 'V',
        # in foreign and borrowed words and names
        u'\N{LATIN SMALL LETTER S WITH CARON}': 'SH',  # š
        u'\N{LATIN SMALL LETTER Z WITH CARON}': 'ZH',  # ž
        u'\N{LATIN SMALL LETTER A WITH ACUTE}': 'AA0', # ??? # á
        u'\N{LATIN SMALL LETTER A WITH GRAVE}': 'AA0',  # à
        u'\N{LATIN SMALL LETTER AE}': 'AE0',  # æ - Norwegian / Danish
        'b': 'B',
        'c': 'K',  # S ???
        u'\N{LATIN SMALL LETTER C WITH CEDILLA}': 'SH',  # ç - French, etc
        u'\N{LATIN SMALL LETTER C WITH CARON}': 'S',  # ??? - Northern Sámi
        u'\N{LATIN SMALL LETTER D WITH STROKE}': 'D',  # ??? - Northern Sámi
        u'\N{LATIN SMALL LETTER ETH}': 'DH',  # ð - Icelandic
        u'\N{LATIN SMALL LETTER E WITH ACUTE}': 'EY0',  # é
        u'\N{LATIN SMALL LETTER E WITH DIAERESIS}': 'EH0',  # ??? # ë - scientific names
        'f': 'F',
        u'\N{LATIN SMALL LETTER G WITH STROKE}': 'G',  # ??? - other Sámi
        u'\N{LATIN SMALL LETTER G WITH BREVE}': 'G',  # ??? - other Sámi
        u'\N{LATIN SMALL LETTER N WITH TILDE}': 'N Y',  # ñ - Spanish
        u'\N{LATIN SMALL LETTER ENG}': 'N',  #  - Northern Sámi
        u'\N{LATIN SMALL LETTER O WITH STROKE}': 'ER0',  # ??? # ø - Norwegian / Danish
        u'\N{LATIN SMALL LETTER O WITH TILDE}': 'ER0',  # ??? # õ - Estonian
        'q': 'K',
        u'\N{LATIN SMALL LETTER SHARP S}': 'S',  # ß - German
        u'\N{LATIN SMALL LETTER T WITH STROKE}': 'T',  #  - Northern Sámi
        u'\N{LATIN SMALL LETTER THORN}': 'TH',  # Þ - Icelandic
        u'\N{LATIN SMALL LETTER O WITH DIAERESIS}': 'ER0', # ??? # ü - German / Estonian
        'w': 'V',
        'z': 'Z'

    }
    easy_consonants = simple_convert.keys()
    pos = 0
    previous = ' '
    for letter in word:
        #~ if letter == previous:
            #~ pass
        if letter == 'a':
            if len(word) > pos+1 and word[pos+1] in ['i', 'u', ]:
                pass  # handled under following letter
            else:
                phonemes.append('AA0')
        elif letter == 'e':
            if len(word) > pos+1 and word[pos+1] in ['i',]:
                pass  # handled under following letter
            elif previous == 'i':  # ie
                phonemes.append('IY0')  # ???
            else:
                phonemes.append('EH0')
        elif letter == 'i':
            prev_match_i = {
                'a': 'AY0',  # ai
                'e': 'EY0',  # ei
                'o': 'OY0',  # oi
                'u': 'UW0',  # ui
                'y': 'IY0'  # yi
                # u'\N{LATIN SMALL LETTER A WITH DIAERESIS}': ä ???
                # u'\N{LATIN SMALL LETTER O WITH DIAERESIS}': öi ???
            }
            if previous in prev_match_i:
                phonemes.append(prev_match_i[previous])
            else:
                phonemes.append('IH0')
        elif letter == 'o':
            if len(word) > pos+1 and word[pos+1] in ['i', 'u']:
                pass  # handled under following letter
            elif previous == 'u':  # uo
                phonemes.append('OW0')  # ???
            else:
                phonemes.append('OY0')
        elif letter == 'u':
            prev_match_u = {
                'a': 'AW0',  # au
                'o': 'OW0'  # AO??? # ou
                # eu ???
                # iu ???
            }
            if len(word) > pos+1 and word[pos+1] in ['i',]:
                pass  # handled under following letter
            elif previous in prev_match_u:
                phonemes.append(prev_match_u[previous])
            else:
                phonemes.append('UH0')
        elif letter == 'y':
            # äy ???
            # öy ???
            if len(word) > pos+1 and word[pos+1] in ['i',]:
                pass  # handled under following letter
            else:
                phonemes.append('UW0')  # ???
        elif letter == u'\N{LATIN SMALL LETTER A WITH DIAERESIS}':  # ä
            phonemes.append('AE0')
        elif letter == u'\N{LATIN SMALL LETTER O WITH DIAERESIS}':  # ö
            # yö ???
            phonemes.append('ER0')  # ???
        elif letter == 'g':
            if previous == 'n':
                phonemes.append('NG')
            else:
                phonemes.append('G')
        elif letter == 'n':
            if len(word) > pos+1 and word[pos+1] == 'g':
                pass # handled under g
            else:
                phonemes.append('N')
        elif letter in simple_convert:
            phonemes.append(simple_convert[letter])
        elif len(hammer(letter)) == 1:
            if not recursive:
                phon = breakdownWord(hammer(letter), True)
                if phon:
                    phonemes.append(phon[0])
        #~ else:
            #~ print "not handled", letter, word
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
    teststring = "Kaikki ihmiset syntyvät vapaina ja tasavertaisina arvoltaan ja oikeuksiltaan. Heille on annettu järki ja omatunto, ja heidän on toimittava toisiaan kohtaan veljeyden hengessä"
    splitter = re.compile('\W+', re.UNICODE)
    testwords = splitter.split(teststring)
    testwords.append('på')
    for word in testwords:
        print word, breakdownWord(unicode(word, input_encoding))
