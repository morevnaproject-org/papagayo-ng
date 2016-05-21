#!/usr/local/bin/python
# -*- coding: cp1252 -*-

# this language module is written to be part of
# Papagayo-ng, a lip-sync tool for use with several different animation suites
# Original Copyright (C) 2005 Mike Clifton
#
# this module Copyright (C) 2005 Myles Strous
# Contact information at http://www-personal.monash.edu.au/~myless/catnap/index.html
#
# Portuguese breakdown by Anderson Prado (AndeOn), andeons.com
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

"""functions to take an Portuguese word and return a list of phonemes
"""

import locale

from unicode_hammer import latin1_to_ascii as hammer

input_encoding = locale.getdefaultlocale()[1]  # standard system encoding??
# input_encoding = 'cp1252'
# input_encoding = 'utf-8'
# input_encoding = 'utf-16'
# input_encoding = 'latin-1'
# input_encoding = 'iso-8859-1'


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Vowels and accented vowels
# � � � � � � i � � � �
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

setvowels = u'aeiou' + \
            u'\N{LATIN SMALL LETTER A WITH ACUTE}\N{LATIN SMALL LETTER A WITH GRAVE}\N{LATIN SMALL LETTER A WITH CIRCUMFLEX}\N{LATIN SMALL LETTER A WITH TILDE}' + \
            u'\N{LATIN SMALL LETTER E WITH ACUTE}\N{LATIN SMALL LETTER E WITH CIRCUMFLEX}' + \
            u'\N{LATIN SMALL LETTER I WITH ACUTE}\N{LATIN SMALL LETTER I WITH CIRCUMFLEX}' + \
            u'\N{LATIN SMALL LETTER O WITH ACUTE}\N{LATIN SMALL LETTER O WITH CIRCUMFLEX}\N{LATIN SMALL LETTER O WITH TILDE}' + \
            u'\N{LATIN SMALL LETTER U WITH ACUTE}'


def breakdownWord(word, recursive=False):
    word = word.lower()
    isvowel = dict.fromkeys(setvowels).has_key
    phonemes = []
    simple_convert = {
        'b': 'B',
        'd': 'D',
        'f': 'F',
        'j': 'ZH',
        'k': 'K',
        'l': 'L',
        'm': 'M',
        'n': 'N',
        'p': 'P',
        'q': 'K',
        'r': 'R',
        't': 'T',
        'v': 'V',
        'w': 'W',
        'y': 'IY0',
        'z': 'Z',
        u'\N{LATIN SMALL LETTER C WITH CEDILLA}': 'S',  # �
    }

    easy_consonants = simple_convert.keys()
    pos = 0
    previous = ' '
    for letter in word:
        # if letter == previous and not isvowel(letter):  # double consonants
        #     pass
        # A
        if letter in ['a', u'\N{LATIN SMALL LETTER A WITH ACUTE}', u'\N{LATIN SMALL LETTER A WITH GRAVE}',
                      u'\N{LATIN SMALL LETTER A WITH CIRCUMFLEX}']:
            phonemes.append('AA0')
        elif letter == u'\N{LATIN SMALL LETTER A WITH TILDE}':
            phonemes.append('AE0')
            # E
        elif letter in ['e', u'\N{LATIN SMALL LETTER E WITH CIRCUMFLEX}']:
            phonemes.append('EY0')
        elif letter == u'\N{LATIN SMALL LETTER E WITH ACUTE}':
            phonemes.append('EH0')
            # I
        elif letter in ['i', u'\N{LATIN SMALL LETTER I WITH ACUTE}', u'\N{LATIN SMALL LETTER I WITH CIRCUMFLEX}']:
            phonemes.append('IY0')
            # O
        elif letter in ['o', u'\N{LATIN SMALL LETTER O WITH CIRCUMFLEX}']:
            phonemes.append('OW0')
        elif letter == u'\N{LATIN SMALL LETTER O WITH ACUTE}':
            phonemes.append('OY0')
        elif letter == u'\N{LATIN SMALL LETTER O WITH TILDE}':
            phonemes.append('AW0')
            # U
        elif letter in ['u', u'\N{LATIN SMALL LETTER U WITH ACUTE}']:
            # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            # Special rule to digraphs consonant:
            # qu and gu (followed by e or i):  aquilo, quest�o, quilo, querida, guerra, �guia
            # ?need fix exceptions when vowel u is pronounced : cinquenta, frequente, tranquilo, lingui�a, aguentar
            # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            if previous == 'q':  # digraph consonant Qu
                # ['e', 'i', '�', '�', '�', '�']
                if len(word) > pos + 1 and word[pos + 1] in ['e', 'i', u'\N{LATIN SMALL LETTER E WITH ACUTE}',
                                                             u'\N{LATIN SMALL LETTER I WITH ACUTE}',
                                                             u'\N{LATIN SMALL LETTER E WITH CIRCUMFLEX}',
                                                             u'\N{LATIN SMALL LETTER I WITH CIRCUMFLEX}']:
                    phonemes.append('K')
                else:
                    phonemes.append('UW0')
            elif previous == 'g':  # digraph consonant Gu
                # ['e', 'i', '�', '�', '�', '�']
                if len(word) > pos + 1 and word[pos + 1] in ['e', 'i', u'\N{LATIN SMALL LETTER E WITH ACUTE}',
                                                             u'\N{LATIN SMALL LETTER I WITH ACUTE}',
                                                             u'\N{LATIN SMALL LETTER E WITH CIRCUMFLEX}',
                                                             u'\N{LATIN SMALL LETTER I WITH CIRCUMFLEX}']:
                    phonemes.append('G')
                else:
                    phonemes.append('UW0')
            else:
                phonemes.append('UW0')
            # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            # consonants with combinations
            # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            # C
        elif letter == 'c':
            if previous == 's':  # digraph consonant sC #asCender
                # ['e', 'i', '�', '�', '�', '�']
                if len(word) > pos + 1 and word[pos + 1] in ['e', 'i', u'\N{LATIN SMALL LETTER E WITH ACUTE}',
                                                             u'\N{LATIN SMALL LETTER I WITH ACUTE}',
                                                             u'\N{LATIN SMALL LETTER E WITH CIRCUMFLEX}',
                                                             u'\N{LATIN SMALL LETTER I WITH CIRCUMFLEX}']:
                    phonemes.append('S')
                else:
                    phonemes.append('S')
                    phonemes.append('K')
            if previous == 'x':  # digraph consonant xC #exCelente
                # ['e', 'i', '�', '�', '�', '�']
                if len(word) > pos + 1 and word[pos + 1] in ['e', 'i', u'\N{LATIN SMALL LETTER E WITH ACUTE}',
                                                             u'\N{LATIN SMALL LETTER I WITH ACUTE}',
                                                             u'\N{LATIN SMALL LETTER E WITH CIRCUMFLEX}',
                                                             u'\N{LATIN SMALL LETTER I WITH CIRCUMFLEX}']:
                    phonemes.append('S')
                else:
                    phonemes.append('S')
                    phonemes.append('K')
            # ce #ci
            elif len(word) > pos + 1 and word[pos + 1] in ['e', 'i', u'\N{LATIN SMALL LETTER E WITH ACUTE}',
                                                           u'\N{LATIN SMALL LETTER I WITH ACUTE}',
                                                           u'\N{LATIN SMALL LETTER E WITH CIRCUMFLEX}',
                                                           u'\N{LATIN SMALL LETTER I WITH CIRCUMFLEX}']:
                phonemes.append('S')
            else:
                phonemes.append('K')
                # G
        elif letter == 'g':
            # ge #gi
            if len(word) > pos + 1 and word[pos + 1] in ['e', 'i', u'\N{LATIN SMALL LETTER E WITH ACUTE}',
                                                         u'\N{LATIN SMALL LETTER I WITH ACUTE}',
                                                         u'\N{LATIN SMALL LETTER E WITH CIRCUMFLEX}',
                                                         u'\N{LATIN SMALL LETTER I WITH CIRCUMFLEX}']:
                phonemes.append('ZH')
            else:
                phonemes.append('G')

        # H
        elif letter == 'h':  # silent letter
            if previous == 'n':
                phonemes.append('N')  # digraph consonant Nh
            else:
                pass

        # M
        elif letter == 'm':
            # ['i', 'o', 'u', '�', '�', '�', '�', '�', �]
            if previous in ['i', 'o', 'u', u'\N{LATIN SMALL LETTER I WITH ACUTE}',
                            u'\N{LATIN SMALL LETTER O WITH ACUTE}', u'\N{LATIN SMALL LETTER U WITH ACUTE}',
                            u'\N{LATIN SMALL LETTER I WITH CIRCUMFLEX}', u'\N{LATIN SMALL LETTER O WITH CIRCUMFLEX}',
                            u'\N{LATIN SMALL LETTER O WITH TILDE}'] and word[-1] == ('m') or len(
                word) > pos + 1 and not isvowel(word[pos + 1]):
                pass  # digraphs vowel am em im om um
            else:
                phonemes.append('M')

        # N
        elif letter == 'n':
            if len(word) > pos + 1 and word[pos + 1] == 'h':
                pass  # Nh handled under #H
            elif isvowel(previous) and word[-1] == ('n') or len(word) > pos + 1 and not isvowel(word[pos + 1]):
                pass  # digraphs vowel an en in on un
            else:
                phonemes.append('N')
        # S
        elif letter == 's':
            if len(word) > pos + 1 and word[pos + 1] == 'c':
                pass  # sC handled under #C
            elif isvowel(previous) and len(word) > pos + 1 and isvowel(
                    word[pos + 1]):  # check if have vowel before and after S #caSa
                phonemes.append('Z')
            else:
                phonemes.append('S')
        # X
        elif letter == 'x':
            if len(word) > pos + 1 and word[pos + 1] == 'c':
                pass  # xC handled under #C
            else:
                phonemes.append('SH')  # There are some exceptions where X have phoneme "KS" like t�xi = T A K S I
            #
        elif letter in easy_consonants:
            phonemes.append(simple_convert[letter])
        elif letter == ' ':
            pass
        elif len(hammer(letter)) == 1:
            if not recursive:
                phon = breakdownWord(hammer(letter), True)
                if phon:
                    phonemes.append(phon[0])
                    # ~ else:
                    # ~ print "not handled", letter, word
        pos += 1
        previous = letter
    # return phonemes
    # return " ".join(phonemes)
    temp_phonemes = []
    previous_phoneme = " "
    for phoneme in phonemes:
        if phoneme != previous_phoneme:
            temp_phonemes.append(phoneme)
        previous_phoneme = phoneme
    return temp_phonemes


if __name__ == "__main__":
    testwords = ['casa', 'agilidade', 'guarda',
                 'telhado', 'marinheiro', 'chave', 'passo', 'carro',
                 'guerra', 'guia', 'queijo', 'quiabo',
                 'crescer', 'des�o', 'exce��o', 'zero',
                 'al�a', 'xaxim',
                 'gorila', 'escada', 'mec�nico'
                 ]
    for word in testwords:
        print word, breakdownWord(unicode(word, input_encoding))
