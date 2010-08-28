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

"""functions to take an Italian word and return a list of phonemes
"""
from unicode_hammer import latin1_to_ascii as hammer

import locale, re
input_encoding = locale.getdefaultlocale()[1] # standard system encoding??
# input_encoding = 'cp1252'
# input_encoding = 'utf-8'
# input_encoding = 'utf-16'
# input_encoding = 'latin-1'
# input_encoding = 'iso-8859-1'

vowels = u'aeiou' + \
u'\N{LATIN SMALL LETTER A WITH ACUTE}\N{LATIN SMALL LETTER A WITH GRAVE}\N{LATIN SMALL LETTER A WITH CIRCUMFLEX}' +\
u'\N{LATIN SMALL LETTER E WITH ACUTE}\N{LATIN SMALL LETTER E WITH GRAVE}\N{LATIN SMALL LETTER E WITH CIRCUMFLEX}' +\
u'\N{LATIN SMALL LETTER I WITH ACUTE}\N{LATIN SMALL LETTER I WITH GRAVE}\N{LATIN SMALL LETTER I WITH CIRCUMFLEX}' +\
u'\N{LATIN SMALL LETTER O WITH ACUTE}\N{LATIN SMALL LETTER O WITH GRAVE}\N{LATIN SMALL LETTER O WITH CIRCUMFLEX}' +\
u'\N{LATIN SMALL LETTER U WITH ACUTE}\N{LATIN SMALL LETTER U WITH GRAVE}\N{LATIN SMALL LETTER U WITH CIRCUMFLEX}'

# print vowels.encode('cp1252')

def breakdownWord(word,  recursive=False):
    word = word.lower()
    isvowel = dict.fromkeys(vowels).has_key
    phonemes = []
    simple_convert = {
        'b': 'B',
        'd': 'D',
        'f': 'F',
        'j': 'IY0',  # actual pronunciation varies with word origin
        'k': 'K',  # actual pronunciation varies with word origin
        'l': 'L',
        'm': 'M',
        'p': 'P',
        'q': 'K',
        'r': 'R',
        't': 'T',
        'v': 'V',
        'w': 'W',  # actual pronunciation varies with word origin
        'x': 'K S',  # actual pronunciation varies with word origin
        'y': 'IY0',  # actual pronunciation varies with word origin
    }
    easy_consonants = simple_convert.keys()
    pos = 0
    previous = ' '
    for letter in word:
        # if letter == previous and not isvowel(letter):  # double consonants
        #     pass
        if  letter in [u'a', u'\N{LATIN SMALL LETTER A WITH ACUTE}', u'\N{LATIN SMALL LETTER A WITH GRAVE}', u'\N{LATIN SMALL LETTER A WITH CIRCUMFLEX}']:
            phonemes.append('AA0')
        elif letter == 'c':
            if previous == 's':
                # ['e', 'i', 'é', 'í', 'è', 'ì', 'ê', 'î']
                if len(word) > pos+1 and word[pos+1] in ['e', 'i', u'\N{LATIN SMALL LETTER E WITH ACUTE}', u'\N{LATIN SMALL LETTER I WITH ACUTE}', u'\N{LATIN SMALL LETTER E WITH GRAVE}', u'\N{LATIN SMALL LETTER I WITH GRAVE}', u'\N{LATIN SMALL LETTER E WITH CIRCUMFLEX}', u'\N{LATIN SMALL LETTER I WITH CIRCUMFLEX}']:
                    phonemes.append('SH')
                else:
                    phonemes.append('S')
                    phonemes.append('K')
            elif len(word) > pos+1 and word[pos+1] in ['e', 'i', u'\N{LATIN SMALL LETTER E WITH ACUTE}', u'\N{LATIN SMALL LETTER I WITH ACUTE}', u'\N{LATIN SMALL LETTER E WITH GRAVE}', u'\N{LATIN SMALL LETTER I WITH GRAVE}', u'\N{LATIN SMALL LETTER E WITH CIRCUMFLEX}', u'\N{LATIN SMALL LETTER I WITH CIRCUMFLEX}']:
                phonemes.append('CH')
            else:
                phonemes.append('K')
        elif letter in ['e', u'\N{LATIN SMALL LETTER E WITH CIRCUMFLEX}']:
            phonemes.append('EH0')  # long is "EY0"
        elif letter == u'\N{LATIN SMALL LETTER E WITH ACUTE}':
            phonemes.append('EY0')
        elif letter == u'\N{LATIN SMALL LETTER E WITH GRAVE}':
            phonemes.append('EH0')
        elif letter == 'g':
            if len(word) > pos+1 and word[pos+1] in ['e', u'\N{LATIN SMALL LETTER E WITH ACUTE}', u'\N{LATIN SMALL LETTER E WITH GRAVE}', u'\N{LATIN SMALL LETTER E WITH CIRCUMFLEX}']:
                phonemes.append('JH')
            elif len(word) > pos+1 and word[pos+1] in ['i', u'\N{LATIN SMALL LETTER I WITH ACUTE}', u'\N{LATIN SMALL LETTER I WITH GRAVE}', u'\N{LATIN SMALL LETTER I WITH CIRCUMFLEX}']:
                pass # handled under 'i'
            elif len(word) > pos+1 and word[pos+1] == 'h':
                phonemes.append('G')
            elif len(word) > pos+1 and word[pos+1] == 'l':
                pass # handled nuder 'l'
            elif len(word) > pos+1 and word[pos+1] == 'n':
                pass # handled under 'n'
            elif len(word) > pos+1 and word[pos+1] == 'u':
                phonemes.append('G')
                phonemes.append('W')
            else:
                phonemes.append('G')
        elif letter == 'h':
                pass
        elif letter in ['i', u'\N{LATIN SMALL LETTER I WITH ACUTE}', u'\N{LATIN SMALL LETTER I WITH GRAVE}', u'\N{LATIN SMALL LETTER I WITH CIRCUMFLEX}']:
            if previous == 'c' and len(word) > pos+1 and isvowel(word[pos+1]):
                pass
            elif previous == 'g':
                if len(word) > pos+1 and word[pos+1] in ['a', 'o', 'u', u'\N{LATIN SMALL LETTER A WITH ACUTE}', u'\N{LATIN SMALL LETTER A WITH GRAVE}', u'\N{LATIN SMALL LETTER A WITH CIRCUMFLEX}', u'\N{LATIN SMALL LETTER O WITH ACUTE}', u'\N{LATIN SMALL LETTER O WITH GRAVE}', u'\N{LATIN SMALL LETTER O WITH CIRCUMFLEX}', u'\N{LATIN SMALL LETTER U WITH ACUTE}', u'\N{LATIN SMALL LETTER U WITH GRAVE}', u'\N{LATIN SMALL LETTER U WITH CIRCUMFLEX}']:  # or isvowel(word[pos+1]) ??
                    phonemes.append('JH')
                else:
                    phonemes.append('G')
                    phonemes.append('IY0')
            else:
                phonemes.append('IY0')
        elif letter == 'l':
            if previous == 'g':
                # ['e', 'i', 'é', 'í', 'è', 'ì', 'ê', 'î']
                if len(word) > pos+1 and word[pos+1] in ['e', 'i', u'\N{LATIN SMALL LETTER E WITH ACUTE}', u'\N{LATIN SMALL LETTER I WITH ACUTE}', u'\N{LATIN SMALL LETTER E WITH GRAVE}', u'\N{LATIN SMALL LETTER I WITH GRAVE}', u'\N{LATIN SMALL LETTER E WITH CIRCUMFLEX}', u'\N{LATIN SMALL LETTER I WITH CIRCUMFLEX}']:
                    phonemes.append('L')
                    phonemes.append('IY0')
                else:
                    phonemes.append('L')
                    phonemes.append('G')
            else:
                phonemes.append('L')
        elif letter == 'n':
            if previous == 'g':
                if len(word) > pos+1 and isvowel(word[pos+1]):
                    phonemes.append('N')
                    phonemes.append('Y')
                else:
                    phonemes.append('G')
                    phonemes.append('N')
            else:
                phonemes.append('N')
        elif letter in ['o', u'\N{LATIN SMALL LETTER O WITH ACUTE}', u'\N{LATIN SMALL LETTER O WITH GRAVE}', u'\N{LATIN SMALL LETTER O WITH CIRCUMFLEX}']:
            phonemes.append('OW0')  # when closed, when open as 'AO0' ?
        elif letter == 's':
            if len(word) > pos+1 and word[pos+1] == 'c':
                pass  # handled under c
            elif isvowel(previous) and len(word) > pos+1 and isvowel(word[pos+1]):
                phonemes.append('Z')
            elif pos == 0:
                if len(word) > pos+1 and isvowel(word[pos+1]):
                    phonemes.append('S')
                elif len(word) > pos+1 and word[pos+1] in ['c', 'f', 'p', 'q', 's', 't']:
                    phonemes.append('S')
            elif len(word) > pos+1 and word[pos+1] in ['b', 'd', 'g', 'l', 'm', 'n', 'r', 'v']:
                phonemes.append('Z')
            else:
                phonemes.append('S')
        elif letter in ['u', u'\N{LATIN SMALL LETTER U WITH ACUTE}', u'\N{LATIN SMALL LETTER U WITH GRAVE}', u'\N{LATIN SMALL LETTER U WITH CIRCUMFLEX}']:
            if previous == 'q':
                phonemes.append('W')
            elif previous == 'g':
                pass  # handled under 'g'
            else:
                phonemes.append('UW0')
        elif letter == 'z':
            if pos == 0:
                phonemes.append('Z')
            elif previous == 'z':
                phonemes.append('T')
                phonemes.append('S')
            elif len(word) > pos+1 and word[pos+1] == 'z':
                pass
            else:
                phonemes.append('Z')
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
            #~ print "not handled", letter, word
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
    testwords = ['gli', 'pietà', 'guarda',
                        'casa', 'padre', 'grande', 'tanto',
                        'busta', 'Berlinguer', 'Bertinotti', 'bambola', 'bambino',
                        'cinque', 'cenci', 'focassia', 'ciao', 'fece',
                        'ricavare', 'cavolo', 'come', 'facoltà', 'culto',
                        'domenica', 'andare', 'commanda', 'diavolo',
                        'mettere', 'meteorologica', 'mele', 'finire',
                        'finto', 'raffinato', 'Ruffino', 'fondametale',
                        'gelato', 'formaggio', 'genio', 'finge', 'Giovanni', 'gengive',
                        'gamba', 'gufo', 'gobbo', 'raccolgo', 'ragazzo',
                        'gli', 'figlio', 'raccogliere', 'aglio', 'Ventimiglia',
                        'gnocchi', 'vigna', 'cigno', 'castagna', 'stagnare',
                        'hai', 'ghenga', 'abbachio', 'chiasso', 'ghiera',
                        'timone', 'partire', 'Primo', 'spaghetti', 'fili',
                        'lungo', 'Fillungo', 'falò', 'lui', 'lei',
                        'milione', 'mamma', 'Sambuca', 'Mussolini', 'militare',
                        'nano', 'nonno', 'mano', 'autunno', 'mondo', 'monte',
                        'potere', 'posta', 'appoggiare', 'aprodere', 'colto',
                        'pudore', 'troppo', 'Paolo', 'proprio', 'provare',
                        'quello', 'qui', 'quaglione', 'quaglia', 'qualunque',
                        'Roma', 'traspassare', 'camorra', 'parlare', 'ruderi', 'marroni',
                        'sapere', 'sasso', 'vaso', 'Tasso', 'posso', 'Varese',
                        'tutto', 'fonte', 'tela', 'Torino', 'elefanti',
                        'strutto', 'muto', 'Ubaldo', 'Ugi', 'Udine', 'furgone',
                        'velo', 'veloce', 'trovare', 'tivu', 'vergine', 'vinto',
                        'zabaglione', 'zero', 'zoologica', 'mazzo', 'nozzi', 'ragazza',
                        'tutta', 'tuta',
                        'Giovanni', 'Giuseppe', 'Gianna',
                        'cioè', 'città', 'ramarro',
                        'på', 'hänsyn'
                        ]
    for word in testwords:
        print word, breakdownWord(unicode(word, input_encoding))
