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

"""functions to take a Hungarian word and return a list of phonemes
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
    isvowel = dict.fromkeys(u'aeiou\N{LATIN SMALL LETTER DOTLESS I}'
u'\N{LATIN SMALL LETTER O WITH DIAERESIS}\N{LATIN SMALL LETTER U WITH DIAERESIS}'
u'\N{LATIN SMALL LETTER A WITH CIRCUMFLEX}\N{LATIN SMALL LETTER U WITH CIRCUMFLEX}').has_key
    phonemes = []
    simple_convert = {
    'b': 'B',
    'c': 'JH',
    u'\N{LATIN SMALL LETTER C WITH CEDILLA}': 'CH',
    'd': 'D',
    'f': 'F',
    'g': 'G',
    'h': 'HH',
    u'\N{LATIN SMALL LETTER DOTLESS I}': 'AH0',
    'i': 'IY0',
    'j': 'ZH',
    'k': 'K',
    'l': 'L',
    'm': 'M',
    'n': 'N',
    u'\N{LATIN SMALL LETTER O WITH DIAERESIS}': 'ER0',
    'p': 'P',
    'r': 'R',
    's': 'S',
    u'\N{LATIN SMALL LETTER S WITH CEDILLA}': 'SH',
    't': 'T',
    u'\N{LATIN SMALL LETTER U WITH DIAERESIS}': 'UW0', # IH0?
    'w': 'V',  # loan-words
    'z': 'Z',
    }
    easy_consonants = simple_convert.keys()
    pos = 0
    previous = ' '
    for letter in word:
        if letter == 'a':
            if len(word) > pos+1 and word[pos+1] == 'y':
                phonemes.append('AY0')
            else:
                phonemes.append('AA0')
        elif letter == u'\N{LATIN SMALL LETTER A WITH CIRCUMFLEX}':
            if previous in ['g', 'k', 'l']:
                phonemes.append('IY0')
                phonemes.append('AA0')
            else:
                phonemes.append('AA0')
        elif letter == 'e':
            if len(word) > pos+1 and word[pos+1] == 'y':
                phonemes.append('EY0')
            else:
                phonemes.append('EH0')
        elif letter == u'\N{LATIN SMALL LETTER G WITH BREVE}':
            pass
            #~ if len(word) > pos+1 and word[pos+1] in ['e', 'i',
                            #~ u'\N{LATIN SMALL LETTER O WITH DIAERESIS}',
                            #~ u'\N{LATIN SMALL LETTER U WITH DIAERESIS}']:
                #~ phonemes.append('Y')
            #~ else:
                #~ pass
        #~ elif letter == 'g':
            #~ if len(word) > pos+1 and word[pos+1] in ['e', 'i',
                            #~ u'\N{LATIN SMALL LETTER O WITH DIAERESIS}',
                            #~ u'\N{LATIN SMALL LETTER U WITH DIAERESIS}']:
                #~ phonemes.append('L')
                #~ phonemes.append('Y')
            #~ else:
                #~ phonemes.append('L')
        #~ elif letter == 'l':
            #~ if len(word) > pos+1 and word[pos+1] in ['e', 'i',
                            #~ u'\N{LATIN SMALL LETTER O WITH DIAERESIS}',
                            #~ u'\N{LATIN SMALL LETTER U WITH DIAERESIS}']:
                #~ phonemes.append('L')
                #~ phonemes.append('Y')
            #~ else:
                #~ phonemes.append('L')
        elif letter =='n':
            if len(word) > pos+1 and word[pos+1] == 'b':
                phonemes.append('M')
            else:
                phonemes.append('N')
        elif letter == 'o':
            if len(word) > pos+1 and word[pos+1] == 'y':
                phonemes.append('OY0')
            else:
                phonemes.append('OW0')
        elif letter == 'q':  # loan-words
            phonemes.append('K')
        elif letter == u'\N{LATIN SMALL LETTER U WITH CIRCUMFLEX}':
            if previous in ['g', 'k', 'l']:
                phonemes.append('IY0')
                phonemes.append('UW0')
            else:
                phonemes.append('UW0')
        elif letter == 'u':
            if len(word) > pos+1 and word[pos+1] == 'y':
                phonemes.append('IY0')
            else:
                phonemes.append('UH0')
        elif letter == 'v':
            if isvowel(previous):
                phonemes.append('W')
            else:
                phonemes.append('V')
        elif letter == 'x':  # loan-words
            phonemes.append('K')
            phonemes.append('S')
        elif letter == 'y':
            if previous in ['a', 'e', 'o', 'u', u'\N{LATIN SMALL LETTER O WITH DIAERESIS}']:
                pass
            else:
                phonemes.append('Y')
        elif letter in easy_consonants:
            phonemes.append(simple_convert[letter])
        elif letter == " ":
            pass
        elif len(hammer(letter)) == 1:
            # print "hammer"
            if not recursive:
                phon = " ".join(breakdownWord(hammer(letter), True))
                if phon:
                    phonemes.append(phon.split()[0])
        #~ else:
            #~ print "not handled", letter, word
        pos += 1
        previous = letter
    # return phonemes
    temp_phonemes = []
    previous_phoneme = " "
    for phoneme in phonemes:
        if phoneme != previous_phoneme:
            temp_phonemes.append(phoneme)
        previous_phoneme = phoneme
    return temp_phonemes



if __name__ == "__main__":
    testwords = [ 'merhaba', 'Iyi', 'geceler', 'allaha',
                        'ismarladik', 'güle', 'evet', 'hayir',
                        'lütfen', 'anlamiyorum', 'afiyet', 'olsun',
                        'saatler', 'elinize', 'ithal', 'Mithat', 'meshut',
                        'cem', 'Ahmet', 'rehber', 'müphem', 'ithal',
                        'på', 'hänsyn'
                        ]
    for eachword in testwords:
        print eachword, ':', breakdownWord(unicode(eachword, input_encoding)), '--', breakdownWord(unicode(eachword, input_encoding))

