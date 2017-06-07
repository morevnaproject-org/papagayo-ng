#!/usr/local/bin/python
# -*- coding: cp1252 -*-

# this language module is written to be part of
# Papagayo-NG, a lip-sync tool for use with several different animation suites
# Original Copyright (C) 2005 Mike Clifton
#
# this module Copyright (C) 2016 Azia Giles Abuara
# Contact information at aziacomics-com.webs.com, aziagiles@gmail.com
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

'''
***TUTORIAL IN USING THIS MODULE
-Spell any word as they are pronounced rather than how they are really spelled. Do this with respect to the english
alphabet in mind i.e a-z,sh,ch. In summary play just with this 28 sounds to spell your words i.e
                     a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,ch,sh
***E.g:
'laugh' will be spelled as 'laf', 'the' as 'de', 'say' as 'seh','nation' as 'nehshon', 'chalk' as 'cholk', 'chlorine' as 'klorin'
'genius' as 'jinius', 'pharmacy' as 'famaci', 'cough' as 'cof', 'ghetto' as 'gheto' etc

***Objective: The idea behind this module is to help you breakdown any other language or dialect with respect to english
'''

"""functions to take any Word in Any Language or Dialect and return a list of phonemes
"""
from breakdowns.unicode_hammer import latin1_to_ascii as hammer

import locale
input_encoding = locale.getdefaultlocale()[1] # standard system encoding??
# input_encoding = 'cp1252'
# input_encoding = 'utf-8'
# input_encoding = 'utf-16'
# input_encoding = 'latin-1'
# input_encoding = 'iso-8859-1'

# lists containing different accented vowels
accented_a = [u'\N{LATIN SMALL LETTER A WITH ACUTE}', u'\N{LATIN SMALL LETTER A WITH GRAVE}', u'\N{LATIN SMALL LETTER A WITH CIRCUMFLEX}', u'\N{LATIN SMALL LETTER A WITH TILDE}', u'\N{LATIN SMALL LETTER A WITH DIAERESIS}', u'\N{LATIN SMALL LETTER A WITH RING ABOVE}', u'\N{LATIN SMALL LETTER AE}']
accented_e = [u'\N{LATIN SMALL LETTER E WITH CIRCUMFLEX}', u'\N{LATIN SMALL LETTER E WITH DIAERESIS}', u'\N{LATIN SMALL LETTER E WITH GRAVE}', u'\N{LATIN SMALL LETTER E WITH ACUTE}', u'\N{LATIN SMALL LIGATURE OE}']
accented_i = [u'\N{LATIN SMALL LETTER I WITH ACUTE}', u'\N{LATIN SMALL LETTER I WITH CIRCUMFLEX}', u'\N{LATIN SMALL LETTER I WITH GRAVE}', u'\N{LATIN SMALL LETTER I WITH DIAERESIS}']
accented_o = [u'\N{LATIN SMALL LETTER O WITH CIRCUMFLEX}', u'\N{LATIN SMALL LETTER O WITH DIAERESIS}', u'\N{LATIN SMALL LETTER O WITH STROKE}',u'\N{LATIN SMALL LETTER O WITH GRAVE}',u'\N{LATIN SMALL LETTER O WITH ACUTE}',u'\N{LATIN SMALL LETTER O WITH TILDE}']
accented_u = [u'\N{LATIN SMALL LETTER U WITH ACUTE}', u'\N{LATIN SMALL LETTER U WITH GRAVE}',u'\N{LATIN SMALL LETTER U WITH CIRCUMFLEX}',u'\N{LATIN SMALL LETTER U WITH DIAERESIS}']

def breakdownWord(word, recursive=False):
    word = word.lower()
    isvowel = dict.fromkeys('aàáâãäåæeèéêëiìíîïoòóôõöøœuùúûü').has_key
    phonemes = []
    simple_convert = {
        'b': 'B',
        'd': 'D',
        'f': 'F',
        'g': 'G',
        'j': 'JH',
        'k': 'K',
        'l': 'L',
        'm': 'M',
        'n': 'N',
        'p': 'P',
        'q': 'K',
        'r': 'R',
        's': 'S',  
        't': 'T',
        'v': 'V',  
        'w': 'W',
        'y': 'Y',
        'z': 'Z',
        u'\N{LATIN SMALL LETTER C WITH CEDILLA}':'S' #  ç
    }
    easy_consonants = simple_convert.keys()
    pos = 0
    previous = ' '
    for letter in word:
        if letter in ['a',accented_a]:            # a
                phonemes.append('AE0')
        elif letter in ['e',accented_e]:          # e
               phonemes.append('EH0')      
        elif letter in ['i',accented_i]:          # i
                phonemes.append('IH0')
        elif letter in ['o',accented_o]:          # o
                phonemes.append('AO0')
        elif letter in ['u',accented_u]:          # u
                phonemes.append('UW0')
                 
        elif letter == 'c':
            if len(word) > pos+1 and word[pos+1] == 'h': # ch 
                phonemes.append('CH')
            elif len(word) > pos+1 and word[pos+1] in ['e','i','y',accented_e,accented_i]: #ce, ci
                phonemes.append('S')
            elif len(word) > pos+1 and word[pos+1] in ['a','o','r','u',accented_a,accented_o,accented_u]:    # ca, co, cu, cr
                phonemes.append('K')
            else:
                phonemes.append('K')
        elif  letter == 'h':     
            if previous in ['c','s']:  
                pass 
            else:
                phonemes.append('HH')    # h      
        elif letter == 's':     
            if len(word) > pos+1 and word[pos+1] == 'h':  
                phonemes.append('SH')   # sh
            else:
                phonemes.append('S')    # s
        elif letter == 'x':             # x
            if pos+1==len(word):
               phonemes.append('Z')
            else:
               phonemes.append('K')
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
        temp_phonemes.append(phoneme)
        previous_phoneme = phoneme
    return temp_phonemes

if __name__ == "__main__":
    testwords = ['y','gooooool','chalk','ghetto','laf','fada','yam','enegi','taxi', 'abi', 
    'don', 'fufu', 'achu', 'jelof', 'seh', 'sah', 'fo','wahala', 'massa','shame',
                        'contrih', 'camer', 'naija', 'ah', 'whosaiye', 'pikin',
                        'babalaro', 'witch', 'doh',
                        'di', 'sabi', 'sef', 'hambok', 'makala', 'accra', 'chop',
                        'njama', 'mimbo', 'plat', 'motor', 'vex',
                        'happi', 'joli', 'tiff', 'piss', 'akra',
                        'eru', 'ndolo', 'munah', 'ndole', 'benskin', 'yi',
                        'krouhkrouh', 'wan', 'kosh'
                        ]
    for word in testwords:
        print(word, breakdownWord(unicode(word, input_encoding)))
