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

"""functions to take a Norwegian word and return a list of phonemes
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
    isvowel = dict.fromkeys(u'aeiouy\N{LATIN SMALL LETTER A WITH RING ABOVE}\N{LATIN SMALL LETTER AE}\N{LATIN SMALL LETTER O WITH STROKE}').has_key
    phonemes = []
    simple_convert = {
    'b': 'B',
    'c': 'S',
    'f': 'F',
    'm': 'M',
    'p': 'P',
    'r': 'R',
    't': 'T',
    'v': 'V',
    'w': 'V',
    'z': 'S',
    }
    short_vowels = {
        u'a': 'AA0',
        u'e': 'EH0',
        u'i': 'IH0',
        u'o': 'UH0',
        u'u': 'UH0',
        u'y': 'IH0',
        u'\N{LATIN SMALL LETTER AE}': 'AE0',
        u'\N{LATIN SMALL LETTER O WITH STROKE}': 'AH0',
        u'\N{LATIN SMALL LETTER A WITH RING ABOVE}': 'AA0'
    }
    long_vowels = {
        u'a': 'AA0',
        u'e': 'EY0',
        u'i': 'IY0',
        u'o': 'OW0',
        u'u': 'UW0',
        u'y': 'IY0',
        u'\N{LATIN SMALL LETTER AE}': 'AE0',
        u'\N{LATIN SMALL LETTER O WITH STROKE}': 'ER0',
        u'\N{LATIN SMALL LETTER A WITH RING ABOVE}': 'AO0'
    }
    easy_consonants = simple_convert.keys()
    pos = 0
    previous = ' '
    for letter in word:
        if isvowel(letter):
            if len(word) == pos+3 and word[pos+1] == 'r' and word[pos+1] == 'd':
                phonemes.append(long_vowels[letter])
            elif letter == 'a'and len(word) > pos+1 and word[pos+1] == 'i':
                    phonemes.append('AY0')
            elif letter == 'a'and len(word) > pos+1 and word[pos+1] == 'u':
                    phonemes.append('AW0')
            elif letter == 'e'and len(word) > pos+1 and word[pos+1] == 'i':
                    phonemes.append('AY0')
            elif letter == 'e'and len(word) > pos+1 and word[pos+1] == 'r':
                    phonemes.append('AE0')
            elif letter == 'o'and len(word) > pos+1 and word[pos+1] == 'i':
                    phonemes.append('OY0')
            elif letter == 'o'and len(word) > pos+1 and word[pos+1] == 'i':
                    phonemes.append('UW0')
                    phonemes.append('IY0')
            elif letter == u'\N{LATIN SMALL LETTER O WITH STROKE}'and len(word) > pos+1 and word[pos+1] == 'y':
                    phonemes.append('OW0')
                    phonemes.append('IY0')
            elif len(word) == pos+2 and word[pos+1] == 'm':
                phonemes.append(short_vowels[letter])
            elif len(word) > pos+2 and word[pos+1] == word[pos+2] and not isvowel(word[pos+1]):
                phonemes.append(short_vowels[letter])
            elif len(word) == pos+3 and word[pos+1] == 'r' and word[pos+2] == 'd':
                phonemes.append(long_vowels[letter])
            elif len(word) > pos+2 and word[pos+1] != word[pos+2] and not isvowel(word[pos+1]):
                phonemes.append(long_vowels[letter])
            else:
                phonemes.append(long_vowels[letter])
        elif letter == 'd':
            if len(word) == pos+1 and previous == 'r': # ends in d, e.g. jord
                pass
            elif len(word) == pos+1 and isvowel(previous): # ends in long vowel then d, e.g. god
                pass
            elif previous in ['l', 'n']:  # holde, land
                pass
            else:
                phonemes.append('D')
        elif letter == 'g':
            if len(word) > pos+1 and word[pos+1] == 'j':   # gjær
                pass  # handled as a normal j
            elif len(word) == pos+1 and previous == 'i': # ærlig
                pass  # silent at end of word
            elif previous == 'n':
                pass  # handled under n
            elif len(word) > pos+1 and word[pos+1] in ['i', 'y']:
                phonemes.append('Y')
            elif len(word) > pos+2 and word[pos+1] == 'e' and word[pos+2] == 'i':
                phonemes.append('Y')
            else:
                phonemes.append('G')
        elif letter == 'h':
            if len(word) > pos+1 and word[pos+1] == 'j':   # hjem
                pass  # handled as a normal j
            if len(word) > pos+1 and word[pos+1] == 'v':   # hver
                pass  # handled as a normal v
            else:
                phonemes.append('HH')
        elif letter == 'j':
            if previous == 'k':
                pass  # handled under k
            elif previous == 's':
                pass  # handled under s
            else:
                phonemes.append('Y')
        elif letter == 'k':
            if previous == 's' and len(word) > pos+1 and word[pos+1] in [u'j', u'i', u'y', u'\N{LATIN SMALL LETTER O WITH STROKE}']:
                phonemes.append('SH')  # sjkære, ski, skøyter
            elif previous == 's':
                phonemes.append('S')
                phonemes.append('K')
            elif len(word) > pos+1 and word[pos+1] in [u'i', u'y']:  # kirke, kyss
                phonemes.append('HH')
            elif len(word) > pos+1 and word[pos+1] == 'j': # kjønn
                phonemes.append('HH')
            else:
                phonemes.append('K')  # kaffe
        elif letter == 'l':
            if len(word) > pos+1 and word[pos+1] == 'j':   # ljug
                pass  # handled as a normal j
            else:
                phonemes.append('L')
        elif letter == 'n':
            if len(word) > pos+1 and word[pos+1] == 'g': # fang
                phonemes.append('NG')
            else:
                phonemes.append('N')  # ni
        elif letter == 'q':  # foreign language loan-words?
            phonemes.append('K')
            phonemes.append('UW0')
        elif letter == 's':
            if previous == 'r':
                phonemes.append('SH') # Eastern Norway - norsk, person, for sent
            elif len(word) > pos+1 and word[pos+1] == 'k':
                pass  # handled under k
            elif len(word) > pos+1 and word[pos+1] == 'j': # sjø
                phonemes.append('SH')
            elif len(word) > pos+1 and word[pos+1] == 'l':
                phonemes.append('SH') # informal usage
            else:
                phonemes.append('S')  # syv
        elif letter == 'x':
            phonemes.append('K')
            phonemes.append('S')
        elif letter in easy_consonants:
            phonemes.append(simple_convert[letter])
        elif letter == " ":
            pass
        elif len(hammer(letter)) == 1:
            # print "hammer"
            if not recursive:
                phon = " ".join(breakdownWord(hammer(letter), True))
                if phon:
                    phonemes.append(phon)
        #~ else:
            #~ print "not handled", letter, word
        pos += 1
        previous = letter
    temp_phonemes = []
    previous_phoneme = " "
    for phoneme in phonemes:
        if phoneme != previous_phoneme:
            temp_phonemes.append(phoneme)
        previous_phoneme = phoneme
    return temp_phonemes



if __name__ == "__main__":
    testwords = [ 'natt', 'rar', 'hai', 'tau', 'by', 'du', 'menn', 'lettes', 'tre', 'nei', 'fire',
                        'gal', 'hatt', 'titt', 'bi', 'ja', 'kaffe', 'kjønn', 'lys', 'min', 'ni', 'fang', 'godt',
                        'to', 'koie', 'purre', 'råd', 'syv', 'sjø', 'tusen', 'gutt', 'ku', 'uimotståelig',
                        'vits', 'mygg', 'ny', 'lærd', 'tær', 'trøtt', 'kø', 'gøy', 'grått', 'båt',
                        'hjem', 'rom', 'hver', 'kirke', 'kyss', 'gjær', 'ljug', 'gi', 'begynne', 'geit',
                        'kart', 'ærlig', 'barn', 'skjære', 'ski', 'skøyter', 'norsk', 'person', 'forsent',
                        'slå','Oslo', 'jord', 'god', 'holde', 'land', 'huset', 'sølv',
                        'êtres', 'français', 'égaux'
                        ]
    for eachword in testwords:
        print eachword, ':', breakdownWord(unicode(eachword, input_encoding)), '--', breakdownWord(unicode(eachword, input_encoding))