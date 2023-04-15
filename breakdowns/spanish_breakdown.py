#!/usr/local/bin/python
# -*- coding: cp1252 -*-

# this language module is written to be part of
# Papagayo-NG, a lip-sync tool for use with several different animation suites
# Original Copyright (C) 2005 Mike Clifton
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

import locale

input_encoding = locale.getdefaultlocale()[1]  # standard system encoding??
# input_encoding = 'cp1252'  # default for IDLE, Tkinter
# input_encoding = 'latin-1'  # common in English GUIs
# input_encoding = 'iso-8859-1'  # common in English GUIs
# input_encoding = 'utf-8'  # common
from breakdowns.unicode_hammer import latin1_to_ascii as hammer


def stressSpanishWord(breakdown_word):
    """takes a "word" in phonemes and adds primary stress if necessary
    """
    # add stress as necessary
    stressed = 0
    vowelcount = 0
    for phoneme in breakdown_word:
        if phoneme[-1] == '1':
            stressed = 1
            break
        elif phoneme[-1] == '0':
            vowelcount += 1
    if not stressed:
        if vowelcount == 1:
            for n in range(len(breakdown_word)):
                if breakdown_word[n][-1] == '0':
                    breakdown_word[n] = breakdown_word[n][:-1] + '1'
                    break
        elif breakdown_word[-1][0] not in ['A', 'E', 'I', 'O', 'U', 'Y', 'N', 'S']:
            for n in range(len(breakdown_word) - 1, -1, -1):
                if breakdown_word[n][-1] == '0':
                    breakdown_word[n] = breakdown_word[n][:-1] + '1'
                    break
        else:
            tag = 0
            for n in range(len(breakdown_word) - 1, -1, -1):
                # print 'breakdown_word', breakdown_word, ', n : ', n
                if breakdown_word[n][-1] == '0':
                    if tag:
                        breakdown_word[n] = breakdown_word[n][:-1] + '1'
                        break
                    else:
                        tag = 1
    return breakdown_word


unconditional_conversions = {
    u'a': 'AA0',
    u'\N{LATIN SMALL LETTER A WITH ACUTE}': 'AA1',
    u'f': 'F',
    u'i': 'IY0',
    u'\N{LATIN SMALL LETTER I WITH ACUTE}': 'IY1',
    u'j': 'HH',
    u'k': 'K',
    u'm': 'M',
    u'q': 'K',
    u't': 'T',
    u'w': 'V',
    u'z': 'S'}  # South American, Castilian Spanish uses ''TH'


def breakdown_word(input_word, recursive=False):
    """breaks down a word into phonemes
    """
    # word = input_word.decode(input_encoding)  # decode input into Python default internal format (utf-16) from the GUI input format
    word = input_word
    word = word.lower()
    previous = u''
    word_index = 0
    word_breakdown = []
    for letter in word:
        if letter == u'b':
            if word_index == 0 or previous in [u'm', u'n']:
                word_breakdown.append('B')
            else:
                word_breakdown.append('V')
        elif letter == u'c':
            if word_index < len(word) - 1 and word[word_index + 1] == u'h':
                word_breakdown.append('CH')
            elif previous == u'c':
                word_breakdown.append('S')
            elif word_index < len(word) - 1 and word[word_index + 1] == u's':
                pass
            elif word_index < len(word) - 1 and word[word_index + 1] in [u'e', u'i']:
                # should this be SH before 'e', S before 'i' ??
                word_breakdown.append('S')  # South American, Castilian Spanish uses 'TH'
            else:
                word_breakdown.append('K')
        elif letter == u'd':
            if word_index == 0 or previous in [u'l', u'n']:
                word_breakdown.append('D')
            else:
                word_breakdown.append('DH')
        elif letter == u'e':
            if word_index == len(word) - 1 or word[word_index + 1] in [u'a', u'e', u'i', u'o', u'u']:
                word_breakdown.append('EY0')
            else:
                word_breakdown.append('EH0')
        elif letter == u'\N{LATIN SMALL LETTER E WITH ACUTE}':
            if word_index == len(word) - 1 or word[word_index + 1] in [u'a', u'e', u'i', u'o', u'u']:
                word_breakdown.append('EY1')
            else:
                word_breakdown.append('EH1')
        elif letter == u'g':
            if word_index < len(word) - 1 and word[word_index + 1] == u'\N{LATIN SMALL LETTER U WITH DIAERESIS}':
                word_breakdown.append('V')
            elif word_index < len(word) - 1 and word[word_index + 1] in [u'e', u'i']:
                word_breakdown.append('HH')
            else:
                word_breakdown.append('G')
        elif letter == u'h':
            pass
        elif letter == u'l':
            if word_index < len(word) - 1 and word[word_index + 1] == u'l':
                pass
            elif previous == u'l':
                word_breakdown.append('Y')
            else:
                word_breakdown.append('L')
        elif letter == u'n':
            if word_index < len(word) - 1 and word[word_index + 1] == u'v':
                word_breakdown.append('M')
            else:
                word_breakdown.append('N')
        elif letter == u'\N{LATIN SMALL LETTER N WITH TILDE}':
            word_breakdown.append('N')
            word_breakdown.append('Y')
        elif letter == u'o':
            if word_index < len(word) - 1 and word[word_index + 1] not in [u'a', u'e', u'i', u'o',
                                                                           u'u']:  # last bit necessary ?
                word_breakdown.append('AO0')
            else:
                word_breakdown.append('OW0')
        elif letter == u'\N{LATIN SMALL LETTER O WITH ACUTE}':
            if word_index < len(word) - 1 and word[word_index + 1] not in [u'a', u'e', u'i', u'o',
                                                                           u'u']:  # last bit necessary ?
                word_breakdown.append('AO1')
            else:
                word_breakdown.append('OW1')
        elif letter == u'p':
            if word_index == len(word) - 1:
                pass
            else:
                word_breakdown.append('P')
        elif letter == u'r':
            if previous == u'r':
                pass
            elif word_index < len(word) - 1 and word[word_index + 1] == u'r':
                word_breakdown.append('R')  # RR - trilled a lot
            else:
                word_breakdown.append('R')  # only a little trilled
        elif letter == u's':
            if word_index < len(word) - 1 and word[word_index + 1] in [u'd', u'g', u'l', u'm', u'n']:
                word_breakdown.append('Z')
            else:
                word_breakdown.append('S')
        elif letter == u'u':
            if previous == u'q':
                pass
            elif previous == u'g' and word_index < len(word) - 1 and word[word_index + 1] in [u'u', u'i']:
                pass
            else:
                word_breakdown.append('UW0')
        elif letter == u'\N{LATIN SMALL LETTER U WITH ACUTE}':
            if previous == u'q':
                pass
            elif previous == u'g' and word_index < len(word) - 1 and word[word_index + 1] in [u'u', u'i']:
                pass
            else:
                word_breakdown.append('UW1')
        elif letter == u'v':
            if word_index == 0 or previous in [u'm', u'n']:
                word_breakdown.append('B')
            else:
                word_breakdown.append('V')
        elif letter == u'x':
            if previous in [u'a', u'e', u'i', u'o', u'u'] and word_index < len(word) - 1 and word[word_index + 1] in [
                u'a', u'e', u'i', u'o', u'u']:
                word_breakdown.append('K')
                word_breakdown.append('S')
            else:
                word_breakdown.append('S')
        elif letter == u'y':
            if len(word) == 1:
                word_breakdown.append('IY1')
            elif word_index == len(word) - 1:
                word_breakdown.append('IY0')
            else:
                word_breakdown.append('Y')
        elif letter in unconditional_conversions.keys():
            word_breakdown.append(unconditional_conversions[letter])
        elif len(hammer(letter)) == 1:
            if not recursive:
                phon = word_breakdown(hammer(letter), True)
                if phon:
                    word_breakdown.append(phon[0])
        previous = letter
        word_index += 1
    word_breakdown = stressSpanishWord(word_breakdown)
    # return breakdown_word
    temp_phonemes = []
    previous_phoneme = " "
    for phoneme in word_breakdown:
        if phoneme != previous_phoneme:
            temp_phonemes.append(phoneme)
        previous_phoneme = phoneme
    return temp_phonemes


if __name__ == '__main__':
    # test the function
    from yaml import load, Loader
    with open('test/rsrc/breakdown_examples_spanish.yml', 'r') as file:
        breakdown_examples = load(file, Loader)
        test_words = breakdown_examples['words']

    for eachword in test_words:
        print(eachword, breakdown_word(eachword), " ".join(breakdown_word(eachword)))
