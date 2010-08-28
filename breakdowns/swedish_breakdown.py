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

"""functions to take a Swedish word and return a list of phonemes
"""
from unicode_hammer import latin1_to_ascii as hammer

import locale
input_encoding = locale.getdefaultlocale()[1] # standard system encoding??
# input_encoding = 'cp1252'
# input_encoding = 'utf-8'
# input_encoding = 'utf-16'
# input_encoding = 'latin-1'
# input_encoding = 'iso-8859-1'

def suffixen(word):
    suffix = False
    suffix_pronunciation = {
        u"erna": ["AE0", "R", "N", "AH0"],
        u"ernas": ["AE0", "R", "N", "AH0", "S"],
        u"erner": ["AE0", "R", "N", "AE0", "R"],
        u"age": ["AH0", "SH"],
        u"ege": ["EH0", "SH"],
        u"tion": ["CH", "UH0", "N"],
        u"fon": ["F", "AO0", "N"],
        u"for": ["F", "AO0", "R"]
    }
    suffixes = suffix_pronunciation.keys()
    for each_suffix in suffixes:
        if word.endswith(each_suffix) and len(word) > len(each_suffix):
            word = word[:-len(each_suffix)]
            suffix = suffix_pronunciation[each_suffix]
            break
    if not suffix:
        if word.endswith(u"er") and len(word) > 4:
            suffix = ["AE0", "R"]
            word = word[:-2]
    return word, suffix


def prefixen(word):
    prefix = False
    prefix_pronunciation = {
        u"an": ["AH0", "N"],
        u"anti": ["AH0", "N", "T", "IY0"],
        u"av": ["AH0", "V"],
        u"be": ["B", "EH0"],
        u"er": ["AE0", "R"],
        u"efter": ["EH0", "F", "T", "AE0", "R"],
        u'f\N{LATIN SMALL LETTER O WITH DIAERESIS}re': ["F", "ER0", "R", "EH0"],   # före
        u'f\N{LATIN SMALL LETTER O WITH DIAERESIS}r': ["F", "ER0", "R"],  # "för"
        u"fram": ["F", "R", "AH0", "M"],
        u"fr\N{LATIN SMALL LETTER A WITH RING ABOVE}": ["F", "R", "AO0", "N"],
        u"ill": ["IY0", "L"],
        # u"miss": ["M IY0 S"],
        u'p\N{LATIN SMALL LETTER A WITH RING ABOVE}': ["P", "AO0"],  # "på"
        u"re": ["R", "EH0"],
        u"upp": ["UW0", "P"],
        u"ut": ["UW0", "T"],
        u'\N{LATIN SMALL LETTER A WITH RING ABOVE}ter': ["AO0", "T", "AE0", "R"],  # "åter"
        u'\N{LATIN SMALL LETTER O WITH DIAERESIS}ver': ["ER0", "V", "AE0", "R"],  # "över"
        u"ad": ["AH0", "D"],
        u"dis": ["D", "IY0", "S"],
        u"fri": ["F", "R", "IY0"],
        u"fast": ["F", "AH0", "S", "T"],
        u"bio": ["B", "IY0", "UH0"],
        u"inter": ["IY0", "N", "T", "EH0", "R"],
        u"kron": ["K", "R", "UH0", "N"],
        u"samman": ["S", "AH0", "M", "AH0", "N"],
        u"s\N{LATIN SMALL LETTER O WITH DIAERESIS}nder": ["S", "ER0", "N", "D", "EH0", "R"],
        u"super": ["S", "UW0", "P", "EH0", "R"],
        u"kom": ["K", "AO0", "M"],
        u"korr": ["K", "AO0", "R"],
        u"koll": ["K", "AO0", "L"],
        u"astro": ["AH0", "S", "T", "R", "AO0"],
        u"auto": ["AH0", "UW0", "T", "AO0"],
        u"mono": ["M", "AO0", "N", "AO0"],
        u"poly": ["P", "AO0", "L", "UW0"],
        u"post": ["P", "AO0", "S", "T"],
    }
    prefixes = prefix_pronunciation.keys()
    prefixes.sort()
    for each_prefix in prefixes:
        if len(word) >= len(each_prefix)+2 and word.startswith(each_prefix):
            # if each_prefix[-1] in ['a', 'e', 'i', 'o', 'u', 'j', 'ÿ', ý']:
            word = word[len(each_prefix):]
            prefix = prefix_pronunciation[each_prefix]
            break
    #  "hän" but not "häng"
    if not prefix:
        if len(word) >= 5 and word.startswith(u'h\N{LATIN SMALL LETTER A WITH DIAERESIS}n') and not word.startswith(u'h\N{LATIN SMALL LETTER A WITH DIAERESIS}ng'):
            prefix = ['HH", "EH0", "N']  # u'h\N{LATIN SMALL LETTER A WITH DIAERESIS}n'
            word = word[3:]
        # "in" but not "ing"
        elif len(word) >= 4 and word.startswith(u'in') and not word.startswith(u'ing'):
            prefix = ["IY0", "N"]  #  u'i\N{LATIN SMALL LETTER A WITH DIAERESIS}n'
            word = word[2:]
        elif  word.startswith(u"sam"):
            prefix = ["S", "AH0", "M"]
            word = word[3:]
        elif  word.startswith(u"o"):
            prefix = ["UH0"]
            word = word[1:]
    return prefix, word

#~ def breakdownSwedishSyllablePhonetic(word, recursive=False):
    #~ temp_phonemes = breakdownSwedishSyllable(word, recursive, phonetic=True)
    #~ return temp_phonemes

def breakdownSwedishSyllable(word, recursive=False, phonetic=False):
    word = word.lower()
    # isvowel = dict.fromkeys('aeiou').has_key
    phonemes = []
    simple_convert = {
#    u'\N{LATIN SMALL LETTER A WITH ACUTE}': 'AH0',
    u'\N{LATIN SMALL LETTER E WITH ACUTE}': 'EY0',
#    u'\N{LATIN SMALL LETTER I WITH ACUTE}': 'IY0',
#    u'\N{LATIN SMALL LETTER O WITH ACUTE}': 'UH0',
#    u'\N{LATIN SMALL LETTER O WITH ACUTE}': 'UW0',
#    u'\N{LATIN SMALL LETTER Y WITH ACUTE}': 'ER0',
    'a' : 'AH0',  # not exact - AO0 ??
    'b': 'B',
    'f': 'F',
    'm': 'M',
    'o': 'UH0',  # compromise, actually UW0 or AA0 (not), sometimes AO0
    'q': 'K',
    'v': 'V',
    'w': 'V',
    'z': 'S',
    u'\N{LATIN SMALL LETTER A WITH RING ABOVE}': 'AO0',  # not exact
    u'\N{LATIN SMALL LETTER O WITH DIAERESIS}':  'ER0',
    }
    easy_consonants = simple_convert.keys()
    pos = 0
    previous = ' '
    for letter in word:
        if letter == 'c':
            if len(word) > pos+1 and word[pos+1] == 'c':
                pass # cc, handle on next case
            elif previous == 'c' and len(word) > pos+1 and word[pos+1] in ['e', 'i', 'y', u'\N{LATIN SMALL LETTER A WITH DIAERESIS}', u'\N{LATIN SMALL LETTER O WITH DIAERESIS}']:
                phonemes.append('K')
                phonemes.append('S')
            elif len(word) > pos+1 and word[pos+1] in ['e', 'i', 'y', u'\N{LATIN SMALL LETTER A WITH DIAERESIS}', u'\N{LATIN SMALL LETTER O WITH DIAERESIS}']:
                phonemes.append('S')
            elif len(word) > pos+1 and word[pos+1] == 'h':
                phonemes.append('SH')
                #~ if previous == 's':
                    #~ phonemes.append('SH')
                #~ else:
                    #~ phonemes.append('CH')  # sometimes 'K' as in English 'chorus', but no rule
            else: #  elif len(word) > pos+1 and word[pos+1] in ['a', 'o', 'u', u'\N{LATIN SMALL LETTER A WITH RING ABOVE}']:
                phonemes.append('K')
        elif letter == 'd':
            if pos == 0 and len(word) > pos+1 and word[pos+1] == 'j':  # dj at beginning of word
                pass  # same as j alone
            else:
                phonemes.append('D')
        elif letter == 'e':
            if phonetic:
                phonemes.append('EH0')
            elif len(word) == pos+2 and word[pos+1] == 'r':  # ends in er
                phonemes.append('AE0')
            else:
                phonemes.append('EH0')  # sometimes 'IY0', sometimes 'EY0'
        elif letter == 'g':
            if previous in ['l', 'r']:
                phonemes.append('Y')
            elif len(word) > pos+2 and word[pos+1] == 'i' and word[pos+2] == u'\N{LATIN SMALL LETTER O WITH DIAERESIS}':
                phonemes.append('SH')
            elif len(word) > pos+1 and word[pos+1] == 'n' and previous in ['a', 'o', 'u', 'e', 'i', 'y', u'\N{LATIN SMALL LETTER A WITH DIAERESIS}', u'\N{LATIN SMALL LETTER O WITH DIAERESIS}']:
                phonemes.append('NG')
            elif previous == 'n':  # ng
                phonemes.append('NG')
            elif len(word) > pos+1 and word[pos+1] == 'j':  # gj
                pass  # same as 'j' alone
            elif len(word) == pos+2 and word[pos+1] == 'e':  # ends in 'ge' - French loan-word such as garage ?
                phonemes.append('SH')
            elif pos==0 and len(word) > pos+1 and word[pos+1] in ['e', 'i', 'y', u'\N{LATIN SMALL LETTER A WITH DIAERESIS}', u'\N{LATIN SMALL LETTER O WITH DIAERESIS}']:
            # ??? if e is unstressed (how to tell?), pronounce as 'G'
                phonemes.append('Y')
            elif pos==0 and len(word) > pos+1 and word[pos+1] in ['a', 'o', 'u', u'\N{LATIN SMALL LETTER A WITH RING ABOVE}']:
                phonemes.append('G')
            elif previous == 'g':
                pass
            else:  # elif len(word) > pos+1 and word[pos+1] in ['a', 'o', 'u', u'\N{LATIN SMALL LETTER A WITH RING ABOVE}']:
                phonemes.append('G')
        elif letter == 'h':
            if previous == 'c':
                pass # handled under c
            elif len(word) > pos+1 and word[pos+1] == 'j':
                pass  # same as 'j' alone
            elif pos == 1 and previous == 's':  # probably a foreign loan-word
                phonemes.append('SH')
            else:
                phonemes.append('HH')
        elif letter == 'i':
            if previous == 'g' and len(word) > pos+1 and word[pos+1] == u'\N{LATIN SMALL LETTER O WITH DIAERESIS}':
                pass
            elif previous == 's' and len(word) > pos+1 and word[pos+1] == 'o': # sio e.g mission
                phonemes.append('UH0')
            else:
                phonemes.append('IY0')  # sometimes 'IH0'
        elif letter == 'k': # needs to be handled before j to handle skj sound
            if pos == 0 and word in [u'kefir', u'kex', u'kille', u'kis', u'kissa', u'kisse']:
                phonemes.append('K')
            elif pos == 0 and len(word) > pos+1 and word[pos+1] in ['e', 'i', 'y', u'\N{LATIN SMALL LETTER A WITH DIAERESIS}', u'\N{LATIN SMALL LETTER O WITH DIAERESIS}']:
                phonemes.append('CH')
            elif word == unicode('människa', input_encoding):
                phonemes.append('SH')
            elif word == unicode('människor', input_encoding):
                phonemes.append('SH')
            elif len(word) == pos+1 and previous == 's': # ends in SK
                phonemes.append('S')
                phonemes.append('K')
            elif len(word) > pos+1 and word[pos+1] == 'j':
                # phonemes.append('SH')
                phonemes.append('CH')  # more Finnish-Swedish than Swedish ???
            elif len(word) == pos+1 and previous == 'c':
                pass
            elif previous == 's' and len(word) > pos+1 and word[pos+1] in ['a', 'o', 'u', u'\N{LATIN SMALL LETTER A WITH RING ABOVE}']:
                phonemes.append('S')
                phonemes.append('K')
            elif previous == 's' and pos == 1: # sk at beginning of word
                phonemes.append('SH')
            else: #  elif len(word) > pos+1 and word[pos+1] in ['a', 'o', 'u',  u'\N{LATIN SMALL LETTER A WITH RING ABOVE}']
                phonemes.append('K')
        elif letter == 't': # needs to be handled before j to handle stj sound
            if previous == 's' and len(word) > pos+1 and word[pos+1] == 'j':
                phonemes.append('SH')
            if previous == 't' and len(word) == pos+1:
                pass
            elif len(word) > pos+1 and word[pos+1] == 'j':  # tj
                pass # handled under j
            else:
                phonemes.append('T')
        elif letter == 'j':
            if previous == 's':
                phonemes.append('SH')
            elif previous == 't':
                if word[pos-2] == 's':  # stj, handled under 't'
                    pass
                else:
                    phonemes.append('CH')
            elif previous == 'k':
                pass  # handled under k
            else:
                phonemes.append('Y')
        elif letter == 'l':
            if len(word) > pos+1 and word[pos+1] == 'j':
                pass  # same as 'j' alone
            else:
                phonemes.append('L')
        elif letter == 'n':
            if len(word) > pos+1 and word[pos+1] == 'g': # ng
                pass  # handled under 'g'
            elif len(word) > pos+1 and word[pos+1] == 'k': # ng
                phonemes.append('NG')
            else:
                phonemes.append('N')
        elif letter == 'p':
            if previous == 'p':
                pass
            else:
                phonemes.append('P')
        elif letter == 'r':
            if len(word) > pos+1 and word[pos+1] == 's':
                pass  # handled under s
            else:
                phonemes.append('R')
        elif letter == 's':
            if len(word) > pos+2 and word[pos+1] == 'c' and word[pos+2] == 'h':
                pass  # handled under 'c'
            elif len(word) > pos+2 and word[pos+1] == 't' and word[pos+2] == 'j':
                pass  # handled under 't'
            elif len(word) > pos+1 and word[pos+1] == 'k':
                pass  # handled under 'k'
            elif len(word) > pos+1 and word[pos+1] == 'j':
                pass # handled under 'j'
            elif len(word) > pos+1 and word[pos+1] == 's':
                pass
            elif len(word) > pos+1 and word[pos+1] == 'i' and len(word) > pos+2 and word[pos+2] == 'o': ## might need more breakdown
                phonemes.append('SH')
            elif pos == 0 and len(word) > pos+1 and word[pos+1] == 'h':
                pass  # handled under 'h'
            elif previous == 'r':
                phonemes.append('SH')  # not entirely accurate, use HH ??
            else:
                phonemes.append('S')
        elif letter == 'u':
            if previous == 'q':
                phonemes.append('V')
            else:
                phonemes.append('UW0')  # inaccurate, no accurate CMU equiivalent
        elif letter == 'x':
            phonemes.append('K')
            phonemes.append('S')
        elif letter == 'y':
            if word in [u'yoga', u'yoghurt']:
                phonemes.append('Y')
            elif word == u'fyrtio':
                phonemes.append('ER0')
            else:
                phonemes.append('UW0')    # not exact
        elif letter == u'\N{LATIN SMALL LETTER A WITH DIAERESIS}':
            if phonetic:
                phonemes.append('AE0')
            elif len(word) > pos+1 and word[pos+1] == 'r':
                phonemes.append('AE0')  # not exact, and skips exceptions---
            else:
                phonemes.append('EH0')  # not exact, and skips exceptions
        elif letter in easy_consonants:
            phonemes.append(simple_convert[letter])
        elif letter == " ":
            pass
        elif len(hammer(letter)) == 1:
            if not recursive:
                phon = " ".join(breakdownSwedishSyllable(hammer(letter), True, phonetic))
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

def splitWord(word):
    if word == u"idka":
        return [u"idka"]
    pieces = [word]
    splitflags = ['kk', 'kb', 'bk', 'dk', 'gk', 'pk',
                        'pg', 'bg', 'kg', 'mg', 'vg', 'sg', 'tg',
                        'pb', 'pd', 'dt', 'td', 'tk']
    for splitflag in splitflags:
        if splitflag in word:
            chunks = word.split(splitflag, 1)
            pieces = [chunks[0] + splitflag[:-1], splitflag[-1:] + chunks[1]]
            break
    if len(pieces) > 1:
        tempPieces = []
        for piece in pieces:
            splitpiece = splitWord(piece)
            for tinypiece in splitpiece:
                tempPieces.append(tinypiece)
        return tempPieces
    else:
        return pieces

def breakdownWord(word, phonetic=False):
    specialcase_words = {
        u"mage" : ["M", "AH0", "G", "EH0"],
        u"krage": ["K", "R", "AH0", "G", "EH0"],
        u"hage": ["HH", "AH0", "G", "EH0"],
        u"stege": ["S", "T", "EH0", "G", "EH0"],
        u"och": ["AO0", "K"],
        u"som": ["S", "AO0", "M"],
        u"dom": ["D", "AO0", "M"],
        u"djonk": ["D", "Y", "AO0", "NG", "K"],
        u"jour": ["SH", "UH0", "R"],
        u"projekt": ["P", "R", "AO0", "SH", "EH0", "K", "T"],
        u"champagne": ["SH", "AH0", "M", "P", "AH0", "N", "Y"],
        u"komik": ["K", "UH0", "M", "IY0", "K"],
        u"komisk": ["K UH0 M IY0 S K"],
        u"komiker": ["K", "UH0", "M", "IY0", "CH", "EH0", "R"],
    }
    if word in specialcase_words.keys():
        return specialcase_words[word]
    phonemes = []
    word = word.lower()
    suffix = False
    prefix, word = prefixen(word)
    word, suffix = suffixen(word)
    morphemes = splitWord(word)
    # print prefix, morphemes
    for morpheme in morphemes:
        recursive = False
        morpheme_phonemes = breakdownSwedishSyllable(morpheme, recursive, phonetic)
        phonemes.extend(morpheme_phonemes)
    if prefix:
        prefix.extend(phonemes)
        phonemes = prefix
    if suffix:
        phonemes.extend(suffix)
    # return " ".join(phonemes)
    # return phonemes
    temp_phonemes = []
    previous_phoneme = " "
    for phoneme in phonemes:
        if phoneme != previous_phoneme:
            temp_phonemes.append(phoneme)
        previous_phoneme = phoneme
    return temp_phonemes

def breakdownSwedishWordPhonetic(word):
    phonetic = True
    CMUversion = breakdownWord(word, phonetic)
    return CMUversion

if __name__ == "__main__":
    testwords = [ 'hänsyn', 'hänseende', 'hängiva',
                        'friktioner', 'friktion', 'er', 'som', 'dom', 'musikalisk', 'missionär', 'kurage', 'övergav', 'inkomma', 'bank', 'mission',
                        'kom', 'min', 'pojke', 'så', 'går', 'vi', 'bort', 'till', 'mormor', 'och', 'snor', 'hennes', 'plånbok', 'ur', 'kommoden',
                        'kåm', 'min', 'påjke', 'så', 'går', 'vi', 'bårt', 'till', 'mormor', 'och', 'snor', 'hennes', 'plånbok', 'ur', 'kåmmoden',
                        'verkligt', 'fräscha', 'färger', 'på', 'tapeterna', 'här',
                        'värkligt', 'frescha', 'färgär', 'på', 'tapetärna', 'här',
                        'sjutton', 'Svenska', 'tala', 'glas', 'bröd', 'cafe', 'cykel',
                        'dag', 'heta', 'nej', 'fredag', 'gata', 'gå', 'gissa',
                        'höst', 'huvudvärk', 'kniv', 'springa', 'timme',
                        'ja', 'kaffe', 'kärlek', 'lördag', 'måndag', 'natt',
                        'stol', 'moln', 'kopp', 'ost', 'pris', 'ringa',
                        'sommar', 'te', 'ut', 'under', 'vår', 'vinter',
                        'till exempel', 'dyr', 'mycket', 'zoo', 'språk',
                        'ålder', 'bära', 'vän', 'röd', 'köra', 'sönder',
                        'gäst', 'gjorde', 'hjälpa', 'ljus', 'check',
                        'kilo', 'kjol', 'tjugo', 'chock', 'garage', 'mars',
                        'schampoo', 'sju', 'skinn', 'skjorta', 'stjarna',
                        'många', 'regn', 'bank',
                        'sherry', 'shah', 'ta', 'katt', 'ko',
                        'hon', 'hus', 'brunn', 'båt', 'sång', 'se', 'fett',
                        'fil', 'in', 'sy', 'sytt', 'träd', 'lätt', 'söt',
                        'röst',
                        'häckklippning', 'askkopp', 'sakkunnig', 'rockkrage', 'ekkärl',
                        'snabbkylning', 'kråkbär', 'piller',
                        'djur', 'vädja', 'djonk',
                        'gevär', 'nagel',
                        'vagn', 'piggna',
                        "kurage",
                        'och', 'idka',
                        'kälke', 'angå', 'skol', 'idé',
                        'motion', 'berättar', 'glädje', 'rasism', 'gråta', 'falla', 'hammare',
                        'prinsessa', 'chockera',
                        'människa', 'människor',
                        'kefir', 'kex', 'kille', 'kis', 'kissa', 'kisse',
                        'yago', 'yoghurt', 'fyrtio',
                        'mage', 'krage', 'hage', 'stege', 'jour', 'projekt', 'champagne',
                        "komik", "komisk", "komiker",
                        'biokemi', 'biogeografi'
                        # fake words to test 100% code coverage
                        'intel', 'ants', 'sampan', 'eccles', 'gnocci', 'regiön', 'region', 'luge', 'quick', 'queasy',
                        'nerfon', 'binfor', 'överland', 'återland', 'efterland', 'éèêïòóõ', 'bistjon',
                        'meñe', 'êtres', 'français', 'égaux'
                        ]
    for eachword in testwords:
        print eachword, ':', breakdownWord(unicode(eachword, input_encoding)), '--', breakdownSwedishWordPhonetic(unicode(eachword, input_encoding))