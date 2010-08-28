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

"""functions to take a Dutch word and return a list of phonemes
"""

from unicode_hammer import latin1_to_ascii as hammer

import locale, re
input_encoding = locale.getdefaultlocale()[1] # standard system encoding??
# input_encoding = 'cp1252'
# input_encoding = 'utf-8'
# input_encoding = 'utf-16'
# input_encoding = 'latin-1'
# input_encoding = 'iso-8859-1'


def suffixen(word):
    suffix = False
    # if word.endswith('je'):
        # suffix = ['Y', 'AH0']
    if re.compile("[^aeiou]e$").search(word):
        suffix = ['EH0']  # AH0 ???
        word = word[:-1]
    elif word.endswith('isch'):
        suffix = ['IY0', 'S']
        word = word[:-4]
    elif word.endswith('ig'):
        suffix = ['AH0']
        word = word[:-2]
    elif word.endswith('lijk'):
        suffix = ['L', 'AH0', 'K']
        word = word[:-4]
    return word, suffix
# er, en, ee ??

def prefixen(word):
    isvowel = dict.fromkeys('aeiou').has_key
    prefix = False
    prefix_pronunciation = {
        'ge': ['HH', 'AH0'],  # HH EH0 ???
        'be': ['B', 'AH0'],  # B EH0 ???
        'er': ['EH0', 'R'],
        'her': ['HH', 'EH0', 'R'],
        'ver': ['F', 'EH0', 'R'],
        'ont': ['AW0', 'N', 'T'],
        'aan' : ['AA0', 'N'],
        'af': ['AH0', 'F'],
        'bij': ['B', 'AY0'],
        u'b\N{LATIN SMALL LETTER Y WITH ACUTE}': ['B', 'AY0'],  # bý
        u'b\N{LATIN SMALL LETTER Y WITH DIAERESIS}': ['B', 'AY0'],  # bÿ
        'hard': ['HH', 'AH0', 'R', 'D'],
        'los': ['L', 'AO0', 'S'],
        'mee': ['M', 'EY0'],
        'om': ['AO0', 'M'],
        'onder': ['AO0', 'N', 'D', 'EH0', 'R'],
        'op': ['AO0', 'P'],
        'over': ['AO0', 'F', 'EH0', 'R'],
        'plat': ['P', 'L', 'AH0', 'T'],
        'tegen': ['T', 'EY0'],
        'toe': ['T', 'UW0'],
        'uit': ['UH0', 'T'],
        'vast': ['F', 'AH0', 'S', 'T'],
        'weg': ['V', 'EY0', 'G'],
        }
    for each_prefix in prefix_pronunciation.keys():
        if len(word) > len(each_prefix)+2 and word.startswith(each_prefix):
            # if each_prefix[-1] in ['a', 'e', 'i', 'o', 'u', 'j', 'ÿ', ý']:
            word = word[len(each_prefix):]
            prefix = prefix_pronunciation[each_prefix]
            break
    return prefix, word

def stressWord(phonemes):
    index = 0
    for phoneme in phonemes:
        if phoneme.endswith('0'):
            phonemes[index] = phonemes[index][:-1] + '1'
            break
        index += 1
    return phonemes

def breakdownWord(word):
    sc = getSyllableCount(word)
    suffix, prefix = False, False
    if sc > 1:
        word, suffix = suffixen(word)
        prefix, word = prefixen(word)
    phonemes = syllablesToPhonemes(wordToSyllables(word))
    phonemes = stressWord(phonemes)
    if suffix:
        phonemes.extend(suffix)
    if prefix:
        prefix.extend(phonemes)
        phonemes = prefix
    # return " ".join(phonemes)
    return phonemes


def getSyllableCount(word):
    isvowel = dict.fromkeys('aeiou').has_key
    istrema = dict.fromkeys('äëïöü').has_key
    previous_letter = ' '
    syllable_count = 0
    vowel_count = 0
    for letter in word:
        if isvowel(letter):
            vowel_count = vowel_count + 1
        if vowel_count == 3: # 3-vowel dipthongs
            syllable_count += 1
            vowel_count = 1
        if isvowel(letter) and not isvowel(previous_letter):
            syllable_count += 1
        if istrema(letter):
            syllable_count += 1
        previous_letter = letter
    return syllable_count

def wordToSyllables(word):
    word = word.lower()
    isvowel = dict.fromkeys('aeiou').has_key
    istrema = dict.fromkeys('äëïöü').has_key
    syllable_count = getSyllableCount(word)
    syllables = [[]]
    previous_letter = ' '
    syllable_end_flag = False
    pos = 0
    syllable_check = 1
    vowel_count = 0
    for letter in word:
        # vowels automatically continue a syllable, except for 3-vowel diphthongs
        if isvowel(letter):
            vowel_count = vowel_count + 1
            if vowel_count == 2 and word[pos] == word[pos-1]:  # second vowel in mooi
                syllables[-1].append(letter) # second "o" in mooi continues the syllable
            elif vowel_count == 2 and len(word) > pos+1 and word[pos] == word[pos+1]: # riool
                syllables.append([letter]) # start a new syllable on the second vowel
                vowel_count = 1
            elif vowel_count == 3:
                syllables.append([letter]) # start a new syllable on the third vowel
                vowel_count = 1
            else:
                syllables[-1].append(letter)  # just a vowel
        # except for vowels with a trema (looks like German Umlaut, but different meaning), which start a new syllable
        elif istrema(letter):
            syllables.append([letter])
            syllable_check += 1
            vowel_count = 0
        # if this is a consonant, the previous letter is a vowel and the next letter is a vowel, start a new syllable
        elif len(word) > pos+1 and isvowel(previous_letter) and isvowel(word[pos+1]) and syllable_check < syllable_count:
            syllables.append([letter])
            syllable_check += 1
            vowel_count = 0
        # if this is a consonant, and the previous letter was a consonant, and the letter before that was a vowel, start a new syllable
        elif not isvowel(previous_letter) and len(syllables[-1]) > 1 and isvowel(syllables[-1][-2]) and syllable_check < syllable_count:
            syllables.append([letter])
            syllable_check += 1
            vowel_count = 0
        else:
            syllables[-1].append(letter)
            vowel_count = 0
        previous_letter = letter
        pos += 1
    return syllables

def syllablesToPhonemes(syllables,  recursive=False):
    isvowel = dict.fromkeys('aeiou').has_key
    phonemes = []
    simple_convert = {
    'b': 'B',
    'd': 'D',
    'f': 'F',
    'h': 'HH',
    'j': 'Y',  # SH in some words borrowed from French
    'k': 'K',
    'l': 'L',
    'm': 'M',
    'n': 'N',
    'p': 'P',
    'r': 'R',
    's': 'S',
    't': 'T',
    'v': 'F', #  English F mixed with English V
    'w': 'V', # closer to soft English V than the English W - pronounced back in mouth, not with pursed lips
    'z': 'Z'
    }
    easy_consonants = simple_convert.keys()
    syllable_pos, letter_pos = 0,1
    pos = [1,1] # syllable 1, letter 1
    previous_letter = ' '
    for syllable in syllables:
        for letter in syllable:
            if letter == previous_letter and not isvowel(letter):  # double consonants
                pass
            # ===================== consonants ==========================
            elif letter == "b" and pos[syllable_pos] == len(syllables) and pos[letter_pos] == len(syllables[-1]):  # last letter in word
                phonemes.append("P")
            elif letter == "d" and pos[syllable_pos] == len(syllables) and pos[letter_pos] == len(syllables[-1]):  # last letter in word
                phonemes.append("T")
            elif letter == "n" and len(syllable) > pos[letter_pos] and syllable[letter_pos] == "g": # ng
                    pass # handled in next case
            elif letter == "g" and previous_letter == "n": # ng
                phonemes.append("NG")
            elif letter == 'g':
                phonemes.append("HH")  # not accurate, but the nearest phoneme in CMU? (use K instead? put in a G anyway?)
            # elif letter == 'c' and len(syllable) > pos[letter_pos]-1 and syllable[pos[letter_pos]] == 'h':
            elif letter == 'c' and len(syllable) > pos[letter_pos]+1 and syllable[pos[letter_pos]] == 'h':  # ch
                pass
            elif letter == 'h' and previous_letter == 'c': # ch
                phonemes.append("HH")  # not accurate, but the nearest phoneme in CMU? (use K instead? put in a G anyway?)
            elif letter == 't'and len(syllable) > pos[letter_pos] and syllable[pos[letter_pos]] == 'h': # th
                    pass # handled in next case
            elif letter == 'h' and previous_letter == 't': # th
                phonemes.append("TH")
            elif letter == 'j'and previous_letter == 'i':
                    pass # handled in vowels
            elif letter == 'w'and previous_letter == 'u':
                    pass # handled in vowels
            elif letter == 'x':  # rare, mostly borrowed words
                phonemes.append("K")
                phonemes.append("S")
            elif letter == 'q':  # rare, mostly borrowed words
                phonemes.append("K")
                phonemes.append("W")
            elif letter == 'c':
                if pos[letter_pos] < len(syllable) and syllable[pos[letter_pos]] in "ei":   # c     before e and i pronounce as s
                    phonemes.append("S")
                else:
                    phonemes.append("K")  # c     before a consonant, at the end of a word and before a, o, u pronounce as k;
            elif letter in easy_consonants:
                phonemes.append(simple_convert[letter])
            # =============== vowels ================
            # ------------ A -------------------------------
            elif letter == 'a': # short AH, long AA
                if pos[letter_pos] < len(syllable) and syllable[pos[letter_pos]] == 'a':  # double a
                    phonemes.append("AA0")
                elif previous_letter == 'a':  # double a handled by case above
                    pass
                elif pos[letter_pos] == len(syllable):  # long a reduced to single letter
                    phonemes.append("AA0")
                elif pos[letter_pos] < len(syllable) and syllable[pos[letter_pos]] == 'u': # au
                    phonemes.append("AW0")  # occasionally as UW0 in some words borrowed from French
                else:
                    phonemes.append('AH0')  # like English short u (cut, hut)
            # ------------ E -------------------------------
            elif letter == 'e': # e short EH long EY
                if pos[letter_pos] < len(syllable) and syllable[pos[letter_pos]] == 'e':  # double e
                    phonemes.append("EY0")
                elif previous_letter == 'e':  # double e handled by case above
                    pass
                elif previous_letter == 'i':  # ie handled at i stage
                    pass
                elif previous_letter == 'o':  # oe handled at o stage
                    pass
                elif pos[letter_pos] == len(syllable):  # long e reduced to single letter
                    phonemes.append("EY0")
                elif pos[letter_pos] < len(syllable) and syllable[pos[letter_pos]] == 'u': # eu
                    phonemes.append("ER0")  # less R than English equivalent, closer to French eu
                elif pos[letter_pos] < len(syllable) and syllable[pos[letter_pos]] == 'i': # ei
                    phonemes.append("AY0")
                else:
                    phonemes.append('EH0')  # closer to a (bad B AH D) than English short EH0 (bed = B EH D)
            # ------------ I -------------------------------
            elif letter == 'i': # i short IH long IY
                if pos[letter_pos] < len(syllable) and syllable[pos[letter_pos]] == 'i':  # double i
                    phonemes.append("IY0")
                elif previous_letter == 'u':  # ui handled at u stage
                    pass
                elif previous_letter == 'i':  # double i handled by case above
                    pass
                elif previous_letter == 'e': # ei handled at ei stage
                    pass
                # elif previous_letter == 'a': # !!!FIXME!!! handle aai, aaij
                #    pass
                elif pos[letter_pos] == len(syllable):  # long i reduced to single letter
                    phonemes.append("IY0")
                elif pos[letter_pos] < len(syllable) and syllable[pos[letter_pos]] == 'j': # ij
                    phonemes.append("AY0")
                elif pos[letter_pos] < len(syllable) and syllable[pos[letter_pos]] == 'u': # iu
                    phonemes.append("IY0")
                elif pos[letter_pos] < len(syllable) and syllable[pos[letter_pos]] == 'e': # ie
                    phonemes.append("IY0")
                # elif pos[letter_pos] < len(syllable) and syllable[pos[letter_pos]] == 'e': # ieuw !!!FIXME!!!  handle ieuw IY UW ???
                #    phonemes.append("IY0")
                else:
                    phonemes.append('IH0')
            # ------------ O -------------------------------
            elif letter == 'o': # o short AA long OW
                if pos[letter_pos] < len(syllable) and syllable[pos[letter_pos]] == 'o':  # double o
                    phonemes.append("OW0")
                elif previous_letter == 'o':  # double o handled by case above
                    pass
                elif pos[letter_pos] == len(syllable):  # long o reduced to single letter
                    phonemes.append("OW0")
                elif pos[letter_pos] < len(syllable) and syllable[pos[letter_pos]] == 'e': # oe
                    phonemes.append("UW0")
                elif pos[letter_pos] < len(syllable) and syllable[pos[letter_pos]] == 'u': # ou
                    phonemes.append("AW0")
                else:
                    phonemes.append('AO0')
            # ------------ U -------------------------------
            elif letter == 'u':
                if pos[letter_pos] < len(syllable) and syllable[pos[letter_pos]] == 'u':  # double u
                    phonemes.append("UW0")
                elif previous_letter == 'u':  # double u handled by case above
                    pass
                elif previous_letter == 'a':  # au handled at a stage
                    pass
                elif previous_letter == 'e':  # handled at e stage
                    pass
                elif previous_letter == 'i':
                    phonemes.append("UW0")
                elif previous_letter == 'o':  # handled at o stage
                    pass
                elif pos[letter_pos] == len(syllable):  # long u reduced to single letter
                    phonemes.append("UW0")
                elif pos[letter_pos] < len(syllable) and syllable[pos[letter_pos]] == 'w': # uw
                    phonemes.append("UW0")  # uw = EW in English DEW IY UW ???
                elif pos[letter_pos] < len(syllable) and syllable[pos[letter_pos]] == 'i': # ui
                    phonemes.append("UH0")  # - not accurate but the nearest phoneme in CMU? (use UW instead?)
                else:
                    phonemes.append('ER0')  # - not accurate but the nearest phoneme in CMU? (use AH instead?)
            # ------------ TREMA (looks like German Umlaut, but different meaning) -------------------------------
            elif letter == u'\N{LATIN SMALL LETTER A WITH DIAERESIS}':  # ä
                phonemes.append('AH0')  # like English short u (cut, hut)
            elif letter == u'\N{LATIN SMALL LETTER E WITH DIAERESIS}':  # ë
                phonemes.append('EH0')  # closer to a (bad B AH D) than English short EH0 (bed = B EH D)
            elif letter == u'\N{LATIN SMALL LETTER I WITH DIAERESIS}':  # ï
                phonemes.append('IH0')
            elif letter == u'\N{LATIN SMALL LETTER O WITH DIAERESIS}':  # ö
                phonemes.append('AO0')
            elif letter == u'\N{LATIN SMALL LETTER U WITH DIAERESIS}':  # ü
                phonemes.append('ER0')  # - not accurate but the nearest phoneme in CMU? (use AH instead?)
            elif letter == u'\N{LATIN SMALL LETTER Y WITH DIAERESIS}' or letter == u'\N{LATIN SMALL LETTER Y WITH ACUTE}':  # 'ÿ' or 'ý'
                # LATIN SMALL LETTER Y WITH DIAERESIS
                # LATIN SMALL LETTER Y WITH ACUTE
                phonemes.append("AY0")
            elif len(hammer(letter)) == 1:
                if not recursive:
                    phon = syllablesToPhonemes(hammer(letter), True)
                    if phon:
                        phonemes.append(phon[0])
            pos[letter_pos] += 1
            previous_letter = letter
        pos[syllable_pos] += 1
        pos[letter_pos] = 1
        previous_letter = ' '
    # return phonemes
    temp_phonemes = []
    previous_phoneme = " "
    for phoneme in phonemes:
        if phoneme != previous_phoneme:
            temp_phonemes.append(phoneme)
        previous_phoneme = phoneme
    return temp_phonemes

if __name__ == "__main__":
    testwords = ['Alle', 'bitte', 'all', 'alle', 'bed', 'kaud', 'hotel', 'kogel', 'licht', 'maand', 'niemand', 'tijd', 'vis', 'walvis',
                    'graag', 'gemeen', 'goed', 'ja', 'niet', 'jager', 'juist', 'regen', 'riool', 'raam', 'bad', 'gat', 'tassen',
                    'gaas', 'maand', 'varen', 'met', 'heg', 'meer', 'deeg', 'eten', 'gaten', 'muren',
                    'boot', 'boten', 'ogen', 'muur', 'fuut', 'duren', 'mooi', 'ce', 'ci', 'hec', 'på', 'hänsyn']
    for word in testwords:
        # print word, wordToSyllables(word), syllablesToPhonemes(wordToSyllables(word)), breakdownWord(word)
        print word, wordToSyllables(word), breakdownWord(unicode(word, input_encoding))