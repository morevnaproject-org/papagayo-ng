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

"""functions to take a German word and return a list of phonemes
"""
from unicode_hammer import latin1_to_ascii as hammer

import locale
input_encoding = locale.getdefaultlocale()[1] # standard system encoding??
# input_encoding = 'cp1252'
# input_encoding = 'utf-8'
# input_encoding = 'utf-16'
# input_encoding = 'latin-1'
# input_encoding = 'iso-8859-1'

def breakdownWord(word, recursive=False):
    word = word.lower()
    isvowel = dict.fromkeys('aeiouäöü').has_key
    phonemes = []
    simple_convert = {
        'f': 'F',
        'j': 'Y',
        'k': 'K',
        'l': 'L',
        'm': 'M',
        'p': 'P',
        'q': 'K',
        'r': 'R',  # use AH0 or ER0 for final letter in word ??
        u'\N{LATIN SMALL LETTER SHARP S}': 'S',
        't': 'T',
        'v': 'F',  # non-native loan-words, 'V'
        'w': 'V',
        'y': 'IH0', # actual pronunciation varies with word origin
    }
    easy_consonants = simple_convert.keys()
    pos = 0
    previous = ' '
    for letter in word:
        if letter == previous and not isvowel(letter):
            pass
        elif letter == 'a':
            if len(word) > pos+1 and word[pos+1] == 'i': # ai
                phonemes.append('AY0')
            elif len(word) > pos+1 and word[pos+1] == 'u': # au
                phonemes.append('AW0')
            elif previous == 'a':
                pass
            elif len(word) > pos+2 and word[pos+1] == word[pos+2] and not isvowel(word[pos+1]):
                phonemes.append('AH0')
            elif len(word) > pos+1 and word[pos+1] == u'\N{LATIN SMALL LETTER SHARP S}':
                phonemes.append('AH0')
            elif len(word) == pos+1 and not isvowel(previous):
                phonemes.append('AA0')
            else:
                phonemes.append('AA0')
        elif letter == u'\N{LATIN SMALL LETTER A WITH DIAERESIS}':
            if len(word) > pos+1 and word[pos+1] == 'u': # äu
                phonemes.append('OY0')
            elif len(word) > pos+2 and word[pos+1] == word[pos+2] and not isvowel(word[pos+1]):
                phonemes.append('EH0')
            elif len(word) > pos+1 and word[pos+1] == u'\N{LATIN SMALL LETTER SHARP S}':
                phonemes.append('EH0')
            elif len(word) == pos+1:
                phonemes.append('EY0')
            else:
                phonemes.append('EY0')
        elif letter == 'b':
            if len(word) == pos+1:
                phonemes.append('P')
            elif len(word) > pos+1 and word[pos+1] in ['s', 't']:
                phonemes.append('P')
            else:
                phonemes.append('B')
        elif letter == 'c':
            if previous == 's' and len(word) > pos+1 and word[pos+1] == 'h':
                phonemes.append('SH')
            elif len(word) > pos+1 and word[pos+1] == 'h':
                phonemes.append('HH')  # use 'K'??
            else:
                phonemes.append('K')
        elif letter == 'd':
            if len(word) == pos+1:
                phonemes.append('T')
            elif len(word) > pos+1 and word[pos+1] in ['s', 't']:
                phonemes.append('T')
            else:
                phonemes.append('D')
        elif letter == 'e':
            if previous == 'i':
                pass  # covered under 'i'
            elif len(word) == pos+2 and word[pos+1] in ['l', 'n', 'r']:  # -en, -er, -el
                phonemes.append('EH0')
            elif len(word) > pos+1 and word[pos+1] == 'i':  # ei
                phonemes.append('AY0')
            elif len(word) > pos+1 and word[pos+1] == 'u':  # eu
                phonemes.append('OY0')
            elif len(word) > pos+1 and word[pos+1] == 'e':  # ee
                phonemes.append('EY0')
            elif previous == 'e':
                pass
            elif len(word) > pos+2 and word[pos+1] == word[pos+2] and not isvowel(word[pos+1]):
                phonemes.append('EH0')
            elif len(word) > pos+1 and word[pos+1] == u'\N{LATIN SMALL LETTER SHARP S}':
                phonemes.append('EH0')
            elif len(word) == pos+1 and not isvowel(previous):
                phonemes.append('EH0')
            else:
                phonemes.append('EY0')
        elif letter == 'g':
            if previous == 'n':
                phonemes.append('NG')
            elif len(word) == pos+1 and previous == 'i':
                phonemes.append('HH')
            elif len(word) == pos+1:
                phonemes.append('K')
            elif len(word) > pos+1 and word[pos+1] in ['s', 't']:
                phonemes.append('K')
            else:
                phonemes.append('G')
        elif letter == 'h':
            if isvowel(previous):
                pass  # silent
            elif previous == 'c':
                pass  # covered under 'c'
            else:
                phonemes.append('HH')
        elif letter == 'i':
            if previous in ['a', 'e']:
                pass # covered under other vowel
            elif len(word) > pos+1 and word[pos+1] == 'e':  # ie
                phonemes.append('IY0')
            elif len(word) > pos+2 and word[pos+1] == word[pos+2] and not isvowel(word[pos+1]):
                phonemes.append('IH0')
            elif len(word) > pos+1 and word[pos+1] == u'\N{LATIN SMALL LETTER SHARP S}':
                phonemes.append('IH0')
            elif len(word) == pos+1 and not isvowel(previous):
                phonemes.append('IY0')  # also use IH0 here instead?
            elif pos == 0:
                phonemes.append('IH0')
            else:
                phonemes.append('IH0')  # also use IH0 here instead?
        elif letter == 'n':
            if len(word) > pos+1 and word[pos+1] == 'g':
                pass  # covered under 'g'
            else:
                phonemes.append('N')
        elif letter == 'o':
            if previous == 'o':
                pass
            elif len(word) == pos+1 and not isvowel(previous):
                phonemes.append('AO0')
            else:
                phonemes.append('AO0')  # somtimes o in on, not covered in CMU/USA
        elif letter ==  u'\N{LATIN SMALL LETTER O WITH DIAERESIS}':
            phonemes.append('ER0')
        elif letter == 's':
            if pos == 0 and len(word) > pos+1 and word[pos+1] in ['p', 't']:
                phonemes.append('SH')
            elif len(word) > pos+2 and word[pos+1] == 'c' and word[pos+2] == 'h':
                pass  # covered under 'c'
            elif pos == 0:
                phonemes.append('Z')  # at beginning of word
            elif len(word) == pos+1:
                phonemes.append('S')  # at end of word
            else:
                phonemes.append('S')  # default sound - or 'Z' ??
        elif letter == 'u':
            if previous in ['a', u'\N{LATIN SMALL LETTER A WITH DIAERESIS}', 'e']:
                pass
            elif previous == 'q':
                phonemes.append('V')
            elif len(word) > pos+2 and word[pos+1] == word[pos+2] and not isvowel(word[pos+1]):
                phonemes.append('UH0')
            elif len(word) > pos+1 and word[pos+1] == u'\N{LATIN SMALL LETTER SHARP S}':
                phonemes.append('UH0')
            elif len(word) == pos+1 and not isvowel(previous):
                phonemes.append('UW0')
            else:
                phonemes.append('UW0')
        elif letter ==  u'\N{LATIN SMALL LETTER U WITH DIAERESIS}':
            phonemes.append('UW0')
        elif letter == 'x':
            phonemes.append('K')
            phonemes.append('S')
        elif letter == 'z':
            phonemes.append('T')
            phonemes.append('S')
        elif letter in easy_consonants:
            phonemes.append(simple_convert[letter])
        elif letter == ' ':
            pass
        elif len(hammer(letter)) == 1:
            if not recursive:
                phon = breakdownWord(hammer(letter[0]), True)
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
    testwords = [ 'stift', 'korken', 'insel',
    'auto', 'noch', 'fein', 'sie', 'neun', 'quittung', 'es',
                        'sprechen', 'muß', 'gut', 'von', 'wir', 'hätte',
                        'läutet', 'können', 'grün',
                        'das', 'vater', 'wenn', 'weg', 'bitte', 'in', 'wider',
                        'rose', 'unter', 'hypnose', 'typisch', 'mayer',
                        'hässlich', 'käse', 'mögen', 'fünf', 'über',
                        'saal', 'see', 'boot', 'bad', 'kredit', 'motto',
                        'meñe', 'på', 'hänsyn'
                        ]
    for word in testwords:
        print word, breakdownWord(unicode(word, input_encoding))
