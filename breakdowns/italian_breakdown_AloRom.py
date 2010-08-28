#!/usr/local/bin/python
# -*- coding: cp1252 -*-

# this language module is written to be part of
# Papagayo, a lip-sync tool for use with Lost Marble's Moho
#
# Papagayo is Copyright (C) 2005 Mike Clifton
# Contact information at http://www.lostmarble.com
#
# this module Copyright (C) 2006 Nicola Jelmorini
# Contact information at http://blenderedintorni.blogspot.com/
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

from unicode_hammer import latin1_to_ascii as hammer

import locale
input_encoding = locale.getdefaultlocale()[1] # standard system encoding??
# input_encoding = 'cp1252'
# input_encoding = 'utf-8'
# input_encoding = 'utf-16'
# input_encoding = 'latin-1'
# input_encoding = 'iso-8859-1'



import string

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# aggiungere qui tutte le vocali con stress=0
# a e o u
# aggiungere qui tutte le lettere accentate con lo stress=1
# à é è ò ù
# aggiungere qui le consonanti che non modificano formulazione
# b d f k m n p q s t v w x y z
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
unconditional_conversions = {
    u'a':'AA0',
    u'\N{LATIN SMALL LETTER A WITH GRAVE}':'AA1',
    u'b':'B',
    u'd':'D',
    u'e':'IH0',
    u'\N{LATIN SMALL LETTER E WITH ACUTE}':'IH1',
    u'\N{LATIN SMALL LETTER E WITH GRAVE}':'IH1',
    u'f':'F',
    u'k':'K',
    u'm':'M',
    u'n':'N',
    u'o':'OW0',
    u'\N{LATIN SMALL LETTER O WITH GRAVE}':'OW1',
    u'p':'P',
    u'q':'K',
    u'r':'R',
    u's':'S',
    u't':'T',
    u'u':'UH0',
    u'\N{LATIN SMALL LETTER U WITH GRAVE}':'UH1',
    u'v':'V',
    u'w':'V',
    u'x':'EH0',
    u'y':'EH0',
    u'z':'Z' }


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# aggiungere qui tutte le combinazioni che modificano la formulazione di base (vedi sopra)
# lettera "c": COno - CIlindro - CHIesa - CAsa - CUrato - CEna - perCIÒ - calCIO - vaCAnza - perCHÉ
# lettera "g": GIOco - GAstro - fiGLIo - GLArona - GHIaccio - GIUrato - GLObale
# lettera "h": HO - HAi - CHE - CHIuso - anCHE
# lettera "j": Jelmorini - BanJo
# lettera "l": fiGLIo
# lettera "i,ì,í": per combinazioni con "c", "g", "l"
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# breaks down a word into phonemes
def breakdownWord(input_word, recursive=False):
    word = input_word
    word = word.lower()  # trasformando tutte le parole in minuscolo si diminuiscono le combinazioni da gestire
    previous = u''
    word_index = 0
    breakdown_word = []
    for letter in word :
        if letter == u'c' :
            #ci
            if word_index < len(word) and word[word_index+1]==u'i' :
                breakdown_word.append('EH0')
            #ce
            elif word_index < len(word) and word[word_index+1]==u'e' :
                breakdown_word.append('EH0')
            #cci
            elif word_index < len(word)-1 and word[word_index+1]==u'c' and word[word_index+2]==u'i' :
                breakdown_word.append('EH0')
            else :
                breakdown_word.append('K')
        elif letter == u'g' :
        	#gi
            if word_index < len(word) and word[word_index+1]==u'i' :
                breakdown_word.append('JH')
            #gli
            elif word_index < len(word)-1 and word[word_index+1]==u'l' and word[word_index+2]==u'i' :
                breakdown_word.append('JH')
            else :
                breakdown_word.append('G')
        elif letter == u'i' :
            #ci, #gi
            if previous == u'c' or previous == u'g' :
                previous = letter
                word_index = word_index + 1
                continue
            else :
                breakdown_word.append('EH0')
        elif letter == u'\N{LATIN SMALL LETTER I WITH ACUTE}' :
            #cí, #gí
            if previous == u'c' or previous == u'g' :
                previous = letter
                word_index = word_index + 1
                continue
            else :
                breakdown_word.append('EH1')
        elif letter == u'\N{LATIN SMALL LETTER I WITH GRAVE}' :
            #cì, #gì
            if previous == u'c' or previous == u'g' :
                previous = letter
                word_index = word_index + 1
                continue
            else :
                breakdown_word.append('EH1')
        elif letter == u'h' :
            #ch
            if previous == u'c':
                previous = letter
                word_index = word_index + 1
                continue
            else :
                breakdown_word.append('HH')
        elif letter == u'j' :
            if word_index > 0 and word_index <len(word) :
                breakdown_word.append('JH')
            else :
                breakdown_word.append('EH0')
        elif letter == u'l' :
            #gli
            if word_index < len(word) and previous == u'g' and word[word_index+1] == u'i' :
                previous = letter
                word_index = word_index + 1
                continue
            else :
                breakdown_word.append('L')
        elif letter in unconditional_conversions.keys():
            breakdown_word.append(unconditional_conversions[letter])
        elif letter == " ":
            pass
        elif len(hammer(letter)) == 1:
            # print "hammer"
            if not recursive:
                phon = " ".join(breakdownWord(hammer(letter), True))
                if phon:
                    breakdown_word.append(phon.split()[0])
        #~ else:
            #~ print "not handled", letter, word
        previous = letter
        word_index = word_index + 1
    return breakdown_word


if __name__ == '__main__' :
    # test the function
    test_words = ['ciccia','fiGLIo','Salve','sa','amici', 'italiano', 'padre', 'Selezioni',
                  'settimana', 'Gli', 'migliore', 'Jelmorini', 'Nicola', 'umani','de', 'la',
                  'in', 'L''America', 'latina', 'y', 'zucchero','probabilmente','patacca',
                  'COno', 'CIlindro', 'CHIesa', 'CAsa', 'CUrato', 'CEna' ,'calCIO','vaCAnza',
                  'GIOco', 'GAstro', 'GiGLIo', 'GLArona', 'GHIaccio', 'GIUrato', 'GLObale',
                  'HO', 'HAi', 'CHE', 'CHIuso', 'anCHE','BanJo','marGIne',
                  'RAdio', 'ROnco', 'RUbino', 'REsto', 'ramaRRo', 'cROsta', 'på', 'hänsyn']
    for word in test_words:
        print word," --> ", breakdownWord(unicode(word, input_encoding))

