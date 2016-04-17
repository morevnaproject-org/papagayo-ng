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

"""functions to take a Spanish word and return a list of phonemes
"""

import string, locale
input_encoding = locale.getdefaultlocale()[1] # standard system encoding??
# input_encoding = 'cp1252'  # default for IDLE, Tkinter
# input_encoding = 'latin-1'  # common in English GUIs
# input_encoding = 'iso-8859-1'  # common in English GUIs
# input_encoding = 'utf-8'  # common
from .unicode_hammer import latin1_to_ascii as hammer

def stressSpanishWord(breakdown_word):
    """takes a "word" in phonemes and adds primary stress if necessary
    """
    # add stress as necessary
    stressed = 0
    vowelcount = 0
    for phoneme in breakdown_word :
        if phoneme[-1] == '1' :
            stressed = 1
            break
        elif phoneme[-1] == '0' :
            vowelcount =vowelcount + 1
    if not stressed :
        if vowelcount == 1 :
            for n in range(len(breakdown_word)) :
                if breakdown_word[n][-1] == '0' :
                    breakdown_word[n] = breakdown_word[n][:-1] + '1'
                    break
        elif breakdown_word[-1][0] not in ['A','E','I','O','U','Y','N','S'] :
            for n in range(len(breakdown_word)-1, -1, -1) :
                if breakdown_word[n][-1] == '0' :
                    breakdown_word[n] = breakdown_word[n][:-1] + '1'
                    break
        else :
            tag = 0
            for n in range(len(breakdown_word)-1, -1, -1) :
                # print 'breakdown_word', breakdown_word, ', n : ', n
                if breakdown_word[n][-1] == '0' :
                    if tag :
                        breakdown_word[n] = breakdown_word[n][:-1] + '1'
                        break
                    else :
                        tag = 1
    return breakdown_word


unconditional_conversions = {
    'a':'AA0',
    '\N{LATIN SMALL LETTER A WITH ACUTE}':'AA1',
    'f':'F',
    'i':'IY0',
    '\N{LATIN SMALL LETTER I WITH ACUTE}':'IY1',
    'j':'HH',
    'k':'K',
    'm':'M',
    'q':'K',
    't':'T',
    'w':'V',
    'z':'S' }  # South American, Castilian Spanish uses ''TH'

def breakdownWord(input_word,  recursive=False):
    """breaks down a word into phonemes
    """
    # word = input_word.decode(input_encoding)  # decode input into Python default internal format (utf-16) from the GUI input format
    word = input_word
    word = word.lower()
    previous = ''
    word_index = 0
    breakdown_word = []
    for letter in word :
        if letter == 'b' :
            if word_index == 0 or previous in ['m', 'n']:
                breakdown_word.append('B')
            else :
                breakdown_word.append('V')
        elif letter == 'c' :
            if word_index < len(word)-1 and word[word_index+1]=='h' :
                breakdown_word.append('CH')
            elif previous == 'c' :
                breakdown_word.append('S')
            elif word_index < len(word)-1 and word[word_index+1]=='s' :
                pass
            elif word_index < len(word)-1 and word[word_index+1] in ['e', 'i'] :
                # should this be SH before 'e', S before 'i' ??
                breakdown_word.append('S')  # South American, Castilian Spanish uses 'TH'
            else :
                breakdown_word.append('K')
        elif letter == 'd' :
            if word_index == 0 or previous in ['l', 'n']:
                breakdown_word.append('D')
            else :
                breakdown_word.append('DH')
        elif letter == 'e' :
            if word_index == len(word)-1 or word[word_index+1] in ['a','e','i','o','u'] :
                breakdown_word.append('EY0')
            else :
                breakdown_word.append('EH0')
        elif letter == '\N{LATIN SMALL LETTER E WITH ACUTE}' :
            if word_index == len(word)-1 or word[word_index+1] in ['a','e','i','o','u'] :
                breakdown_word.append('EY1')
            else :
                breakdown_word.append('EH1')
        elif letter == 'g' :
            if word_index < len(word)-1 and word[word_index+1] == '\N{LATIN SMALL LETTER U WITH DIAERESIS}':
                breakdown_word.append('V')
            elif word_index < len(word)-1 and word[word_index+1] in ['e', 'i'] :
                breakdown_word.append('HH')
            else :
                breakdown_word.append('G')
        elif letter == 'h' :
            pass
        elif letter == 'l' :
            if word_index < len(word)-1 and word[word_index+1] == 'l' :
                pass
            elif previous == 'l' :
                breakdown_word.append('Y')
            else :
                breakdown_word.append('L')
        elif letter == 'n' :
            if word_index < len(word)-1 and word[word_index+1] == 'v' :
                breakdown_word.append('M')
            else :
                breakdown_word.append('N')
        elif letter == '\N{LATIN SMALL LETTER N WITH TILDE}':
            breakdown_word.append('N')
            breakdown_word.append('Y')
        elif letter == 'o' :
            if word_index < len(word)-1 and word[word_index+1] not in ['a','e','i','o','u']:  # last bit necessary ?
                breakdown_word.append('AO0')
            else :
                breakdown_word.append('OW0')
        elif letter == '\N{LATIN SMALL LETTER O WITH ACUTE}':
            if word_index < len(word)-1 and word[word_index+1] not in ['a','e','i','o','u']:  # last bit necessary ?
                breakdown_word.append('AO1')
            else :
                breakdown_word.append('OW1')
        elif letter == 'p' :
            if word_index == len(word)-1 :
                pass
            else :
                breakdown_word.append('P')
        elif letter == 'r' :
            if previous == 'r' :
                pass
            elif word_index < len(word)-1 and word[word_index+1] == 'r' :
                breakdown_word.append('R') # RR - trilled a lot
            else :
                breakdown_word.append('R') # only a little trilled
        elif letter == 's' :
            if word_index < len(word)-1 and word[word_index+1] in ['d','g','l','m','n'] :
                breakdown_word.append('Z')
            else:
                breakdown_word.append('S')
        elif letter == 'u' :
            if previous == 'q' :
                pass
            elif previous == 'g' and word_index < len(word)-1 and word[word_index+1] in ['u','i'] :
                pass
            else :
                breakdown_word.append('UW0')
        elif letter == '\N{LATIN SMALL LETTER U WITH ACUTE}':
            if previous == 'q' :
                pass
            elif previous == 'g' and word_index < len(word)-1 and word[word_index+1] in ['u','i'] :
                pass
            else :
                breakdown_word.append('UW1')
        elif letter == 'v' :
            if word_index == 0 or previous in ['m', 'n']:
                breakdown_word.append('B')
            else :
                breakdown_word.append('V')
        elif letter == 'x' :
            if previous in ['a','e','i','o','u'] and word_index < len(word)-1 and word[word_index+1] in ['a','e','i','o','u'] :
                breakdown_word.append('K')
                breakdown_word.append('S')
            else :
                breakdown_word.append('S')
        elif letter == 'y' :
            if len(word) == 1 :
                breakdown_word.append('IY1')
            elif word_index == len(word)-1 :
                breakdown_word.append('IY0')
            else :
                breakdown_word.append('Y')
        elif letter in list(unconditional_conversions.keys()) :
            breakdown_word.append(unconditional_conversions[letter])
        elif len(hammer(letter)) == 1:
            if not recursive:
                phon = breakdownWord(hammer(letter), True)
                if phon:
                    breakdown_word.append(phon[0])
        previous = letter
        word_index = word_index + 1
    breakdown_word = stressSpanishWord(breakdown_word)
    # return breakdown_word
    temp_phonemes = []
    previous_phoneme = " "
    for phoneme in breakdown_word:
        if phoneme != previous_phoneme:
            temp_phonemes.append(phoneme)
        previous_phoneme = phoneme
    return temp_phonemes


if __name__ == '__main__' :
    # test the function
    test_words = ['Holas', 'amigos', 'si', 'español', 'padré', 'Selecciones', 'de', 'la', 'semana', 'Los', 'mejores', 'sitios', 'los', 'derechos', 'humanos', 'en', 'américa', 'latina', 'y', 'färger', 'på', 'hänsyn']
    for eachword in test_words:
        print(eachword, breakdownWord(str(eachword, input_encoding)), " ".join(breakdownWord(str(eachword, input_encoding))))

