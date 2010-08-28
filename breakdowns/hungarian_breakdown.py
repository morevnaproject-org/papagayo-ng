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
    phonemes = []
    simple_convert = {
    'b': 'B',
    u'\N{LATIN SMALL LETTER E WITH ACUTE}': 'EY0',
    'f': 'F',
    'h': 'HH',
    u'\N{LATIN SMALL LETTER I WITH ACUTE}': 'IY0',
    'k': 'K',
    'm': 'M',
    'n': 'N',
    u'\N{LATIN SMALL LETTER O WITH ACUTE}': 'OW0', # ER0 ? AO0 ?
    'p': 'P',
    'r': 'R',
    't': 'T',
    'u': 'UW0',
    u'\N{LATIN SMALL LETTER U WITH ACUTE}': 'UW0',
    u'\N{LATIN SMALL LETTER O WITH DIAERESIS}': 'ER0',
    u'\N{LATIN SMALL LETTER O WITH DOUBLE ACUTE}': 'ER0',
    u'\N{LATIN SMALL LETTER U WITH DIAERESIS}': 'UW0', # IH0?
    u'\N{LATIN SMALL LETTER U WITH DOUBLE ACUTE}': 'UW0',
    'v': 'V',
    'w': 'V',
    }
    easy_consonants = simple_convert.keys()
    pos = 0
    previous = ' '
    for letter in word:
        if letter =='a':
            if len(word) > pos+1 and word[pos+1] in ['i', 'j', 'y']:
                phonemes.append('OY0')
            elif len(word) > pos+2 and word[pos+1]  == 'l' and word[pos+2]  == 'y':
                phonemes.append('OY0')
            else:
                phonemes.append('AO0')
        elif letter == u'\N{LATIN SMALL LETTER A WITH ACUTE}':
            if len(word) > pos+1 and word[pos+1] in ['i', 'j', 'y']:
                phonemes.append('AY0')
            elif len(word) > pos+2 and word[pos+1]  == 'l' and word[pos+2]  == 'y':
                phonemes.append('AY0')
            else:
                phonemes.append('AA0')
        elif letter == 'c':
            if len(word) > pos+1 and word[pos+1] == 's':
                phonemes.append('CH')
            else:
                phonemes.append('T')
                phonemes.append('S')
        elif letter == 'd':
            if len(word) > pos+1 and word[pos+1] == 's':
                pass  # handle under 'z'
            else:
                phonemes.append('D')
        elif letter == 'e':
            if previous == 'e':
                pass
            elif len(word) > pos+1 and word[pos+1] == 'e':
                phonemes.append('EY0')
            elif len(word) > pos+2 and word[pos+1]  == 'l' and word[pos+2]  == 'y':
                phonemes.append('EY0')
            else:
                phonemes.append('EH0')
        elif letter == 'g':
            if len(word) > pos+1 and word[pos+1] == 'y':
                phonemes.append('JH')
            else:
                phonemes.append('G')
        elif letter == 'i':
            if previous in ['a', 'o', u'\N{LATIN SMALL LETTER A WITH ACUTE}']:
                pass
            else:
                phonemes.append('IH0')  # IY0?
        elif letter == 'j':
            if previous in ['a', 'o', u'\N{LATIN SMALL LETTER A WITH ACUTE}']:
                pass
            else:
                phonemes.append('Y')
        elif letter == 'l':
            if len(word) > pos+1 and word[pos+1] == 'y':
                pass  # handled under y - ly is close enough to just IY
            else:
                phonemes.append('L')
        elif letter == 'o':
            if len(word) > pos+1 and word[pos+1] in ['i', 'j', 'y']:
                phonemes.append('OY0')
            elif len(word) > pos+2 and word[pos+1]  == 'l' and word[pos+2]  == 'y':
                phonemes.append('OY0')
            else:
                phonemes.append('AO0')
        elif letter == 'q': # loan words
            phonemes.append('K')
            phonemes.append('W')
        elif letter == 's':
            if previous == 'c':
                pass
            elif len(word) > pos+2 and word[pos+1] == 's' and word[pos+2] == 'z': # ssz
                pass
            elif len(word) > pos+1 and word[pos+1] == 'z' and previous == 's': # ssz
                phonemes.append('S')
                phonemes.append('S')
            elif len(word) > pos+1 and word[pos+1] == 'z': # sz
                phonemes.append('S')
            else:
                phonemes.append('SH')
        elif letter == 'x':  # loan words only
            phonemes.append('K')
            phonemes.append('S')
        elif letter == 'y':
            if previous in ['a', 'o', u'\N{LATIN SMALL LETTER A WITH ACUTE}']:
                pass
            elif previous == 'g':
                pass  # handled under g
            elif previous == 't':
                phonemes.append('Y')
            elif previous == 'n':
                pass  # close enough to just n, although more like Spanish ñ
            else:
                phonemes.append('IY0')
        elif letter == 'z':
            if len(word) > pos+1 and word[pos+1] == 's' and previous == 'd':   # dzs
                phonemes.append('JH')
            elif previous == 'z' and len(word) > pos+1 and word[pos+1] == 's': # zzs
                phonemes.append('ZH')
                phonemes.append('ZH')
            elif len(word) > pos+1 and word[pos+1] == 's': # zs
                phonemes.append('ZH')
            elif len(word) > pos+2 and word[pos+1] == 'z' and word[pos+2] == 's': # probably zzs
                pass
            elif previous == 'd':   # dz
                phonemes.append('D')
                phonemes.append('S')
            elif previous == 's':
                pass  # handled under s
            elif previous == 'c':
                pass  # handled under c
            else:
                phonemes.append('Z')
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
    testwords = [ 'szabadon', 'ferenc', 'fricsay', 'szöllösy', 'kodály',
                        'székely', 'fonó', 'györgy', 'cziffra',
                        'csárdás', 'kocsis', 'jános', 'masony', 'solti',
                        'szell', 'szigeti', 'miklos', 'rozsa',
                        'szar', 'száe', 'veréb', 'véreb', 'csikós', 'csíkos',
                        'kor', 'kór', 'tok', 'tök', 'út', 'üt',
                        'kocka', 'leér', 'csap', 'cukor', 'ökör',
                        'magyarázni', 'tér',
                        'hat', 'hát',  'kell', 'kék',
                        'iroda', 'irógép', 'hol', 'hó',
                        'öt',
                        # u'\N{LATIN SMALL LETTER O WITH DOUBLE ACUTE}t',
                        'unalmas', 'úszni', 'ürügy',
                        # u'\N{LATIN SMALL LETTER O WITH DOUBLE ACUTE}rhajó',
                        'på', 'hänsyn'

                        ]
    for eachword in testwords:
        print eachword, ':', breakdownWord(unicode(eachword, input_encoding)), '--', breakdownWord(unicode(eachword, input_encoding))

