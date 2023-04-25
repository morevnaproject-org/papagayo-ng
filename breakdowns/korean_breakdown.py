#!/usr/local/bin/python
# -*- coding: cp1252 -*-

# this language module is written to be part of
# Papagayo-NG, a lip-sync tool for use with several different animation suites
# Original Copyright (C) 2005 Mike Clifton
#
# this module Copyright (C) 2023 Owen Gallagher
# Contact information at github.com/ogallagher, owenjpgallagher@outlook.com
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

"""functions to take a Korean word (한국어 hangugeo 단어 daneo) and return a list of phonemes
"""

from breakdowns.unicode_hammer import latin1_to_ascii as hammer
import locale
import re
import logging

logger = logging.getLogger('korean-breakdown')

input_encoding = locale.getdefaultlocale()[1]  # standard system encoding??
# input_encoding = 'cp1252'
# input_encoding = 'utf-8'
# input_encoding = 'utf-16'
# input_encoding = 'latin-1'
# input_encoding = 'iso-8859-1'

# uppercase jamo chars represent jamo that will later be updated depending on context of surrounding
# jamo combinations
HAN_CHO = [
	'g', 'gg', 'n', 'd', 'dd', 'L', 'm', 'b',
	'bb', 'S', 'SS', '', 'J', 'JJ', 'ch', 'k',
	't', 'p', 'h'
]
"""Syllable start jamo. Unicode order ascending.
"""
HAN_JUNG = [
	'a', 'ae', 'ya', 'yae', 'eo', 'e', 'yeo', 'ye',
	'o', 'wa', 'wae', 'oe', 'yo', 'u', 'weo', 'we',
	'wi', 'yu', 'eu', 'ui', 'i'
]
"""Syllable middle jamo. Unicode order ascending.
"""
HAN_JONG = [
	'', 'G', 'gG', 'Gs', 'n', 'nj', 'nh', 'D',
	'L', 'lG', 'lm', 'lb', 'lS', 'lt', 'lp', 'lh',
	'm', 'B', 'BS', 'S', 'SS', 'ng', 'J', 'ch',
	'k', 't', 'p', 'h'
]
"""Syllable end jamo. Unicode order ascending.
"""

HAN_CODE_FIRST = 44032
HAN_CODE_LAST = 55203

def han_to_latin(han: str):
    """Generate latin phonetic (romaja) spelling from hangeul 한글 string.

    This may not work for unicodes larger than 4 bytes.
    Derived from [github.com/kawoou/jquery-korean-pron](https://github.com/kawoou/jquery-korean-pron)
    and translated from [github.com/ogallagher/han_url](https://github.com/ogallagher/han_url).
    """

    out: str = ''
    """Converted latin characters string."""

    code: int
    """Current character code."""
    offset: int
    """Offset is distance between start character 가 and current character."""
    cho: int
    """First jamo"""
    jung: int
    """Middle jamo"""
    jong: int
    """End jamo"""

    # break munja syllables into jamo phonetic elements (letters). then map each jamo to a standard phonetic romanization.
    for char in han:
        code = ord(char)

        if HAN_CODE_FIRST <= code <= HAN_CODE_LAST:
            # is hangul syllable between ga and hih(hit)
            offset = code - HAN_CODE_FIRST
            jong = int(offset % 28)
            jung = int((offset - jong) / 28 % 21)
            cho = int((offset - jong) / 28 / 21)

            jamos = HAN_CHO[cho] + HAN_JUNG[jung] + HAN_JONG[jong]
            logger.debug(f'{char} syllable to jamos {jamos}')

            out += jamos
        else:
            # is something else; leave unchanged
            out += char
    # end for chars

    # update phonetic spelling for special combinations
    combo_replacements = {
        # leave end g<vowel> unchanged
        r'G([aeoiuyw])': lambda m: f'g{m.group(1)}',
        # convert end g<consonant> to k
        r'G': 'k',
        # leave end b<vowel|bn> unchanged
        r'B([aeoiuywbn])': lambda m: f'b{m.group(1)}',
        # convert end ㅂ<consonant> to p
        r'B': 'p',
        # leave end d<vowel|dn> unchanged
        r'D([aeoiuywdn])': lambda m: f'd{m.group(1)}',
        # convert end d<consonant> to t
        r'D': 't',
        # convert <vowel>rl<vowel> to r
        r'(?<=[aeoiuyw])L(?=[aeoiuyw])': 'r',
        # convert remaining r to l
        r'L': 'l',
        # alias weo as wo
        r'weo': 'wo',
        # convert <vowel|s>s<vowel|s> to s
        r'S(?=[aeoiuywsS])': 's',
        # convert <vowel|j>j<vowel|j> to j
        r'J(?=[aeoiuywjJ])': 'j',
        # convert remaining s,j,ss<consonant> to t
        r'[SJ]|(?:([sS][sS])([^aeoiuyw]))': lambda m: f't{m.group(2)}' if m.group(2) is not None else 't',
        # convert shi and sshi
        r'si': 'shi'
    }
    """Map combinations expressed as regular expressions to replacement strings or methods.
    """

    for pattern, replacement in combo_replacements.items():
        out = re.sub(pattern=pattern, repl=replacement, string=out)
    
    return out
# end def

ROMAJA_TO_PHONEME = {
    'g': 'G',
    'gg': 'G',
    'n': 'N',
    'd': 'D',
    'dd': 'D',
    'l': 'L',
    'r': 'R',
    'm': 'M',
    'b': 'B',
    'bb': 'B',
    's': 'S',
    'ss': 'S',
    'sh': 'SH',
    'ssh': 'SH',
    'j': 'JH',
    'jj': 'JH',
    'ch': 'CH',
    'k': 'K',
    't': 'T',
    'p': 'P',
    'h': 'HH',

    'a': 'AA0',
    'ae': 'AE0',
    'y': 'Y',
    'eo': 'AO0',
    'e': 'EH0',
    'o': 'AO0',
    'w': 'W',
    'u': 'UW0',
    'eu': 'UW0',
    'ui': 'IH0',
    'i': 'IY0',

    'nh': 'N',
    'lg': 'L',
    'lm': 'M',
    'lt': 'T',
    'lp': 'P',
    'lh': 'L',
    'ng': 'NG',
    'hd': 'T'
}
"""Map a romaja phonetic string to a phoneme.
"""

# sort romaja_to_phoneme key length descending
romaja_keys = list(ROMAJA_TO_PHONEME.keys())
romaja_keys.sort(key=(lambda k: len(k)), reverse=True)
ROMAJA_TO_PHONEME = {
    romaja_key: ROMAJA_TO_PHONEME[romaja_key]
    for romaja_key in romaja_keys
}

def consume_romaja_phoneme(romaja_word, char_idx):
    """Convert the next block of available romaja characters into a phoneme.
    
    Args:
        romaja_word: The entire romaja word.
        har_idx: Char index from where to start the substring to convert into a single phoneme.

    Returns:
        Tuple[str, int]: The consumed phoneme(s) and a new char_idx value for where to start the next phoneme.
        The phoneme is None if unable to convert.
    """

    phoneme: str = None
    char_idx_next: int = char_idx

    # generate phoneme
    for romaja_key in ROMAJA_TO_PHONEME.keys():
        if romaja_key == romaja_word[char_idx:char_idx+len(romaja_key)]:
            logger.debug(f'found romaja key {romaja_key} at {char_idx}')
            phoneme = ROMAJA_TO_PHONEME[romaja_key]
            char_idx_next += len(romaja_key)
            
            return phoneme, char_idx_next
        # else:
        #     logger.debug(f'(no match on {romaja_key} {char_idx}:{char_idx+len(romaja_key)} {romaja_word[char_idx:char_idx+len(romaja_key)]})')
    # end for romaja keys

    # no phoneme found
    return None, char_idx + 1
# end def

def breakdown_word(input_word, recursive=False):
    """Breaks down a korean word into phonemes.

    The full available phoneme set that is used seems to be CMU-39, but with an extra suffix on
    vowels to indicate stressed syllables, being 0 (no stress) or 1 (stress).
    """

    romaja = han_to_latin(input_word)
    word_idx = 0
    phonemes = []
    while word_idx < len(romaja):
        phoneme, word_idx_next = consume_romaja_phoneme(romaja_word=romaja, char_idx=word_idx)

        if phoneme is not None:
            phonemes.append(phoneme)
            word_idx = word_idx_next

        else:
            letter_hammer = hammer(romaja[word_idx])
            if len(letter_hammer) == 1:
                if not recursive:
                    phon = breakdown_word(letter_hammer, recursive=True)
                    if phon:
                        phonemes.append(phon[0])
                # end if not recurse
            # end if hammer

            word_idx += 1
        # end else
    # end for letters

    # should we remove duplicates?
    remove_duplicates = False

    if remove_duplicates:
        phonemes_uq = []
        phoneme_prev = ' '
        for phoneme in phonemes:
            if phoneme != phoneme_prev:
                phonemes_uq.append(phoneme)
            phoneme_prev = phoneme
        # end for phonemes

        phonemes = phonemes_uq
    # end if remove duplicates

    return phonemes
# end def

if __name__ == '__main__':
    # tests
    from typing import *
    import traceback
    from utilities import init_logging
    init_logging()
    logging.root.setLevel(logging.DEBUG)
    logger.info(f'test korean phoneme breakdown examples')

    from yaml import load, Loader
    with open('test/rsrc/breakdown_examples_korean.yml', 'r') as file:
        tests: Dict[str, Union[str, List[Dict[str, str]]]] = load(file, Loader)

    fails = []
    
    for test_phrase in tests['phrases']:
        words_han = test_phrase['han'].split(' ')
        words_latin = test_phrase['latin'].split(' ')
        phonemes = test_phrase['phonemes']
        words_latin_generated = []
        phonemes_latin_generated = []

        for t in range(len(words_han)):
            try:
                # test han to latin
                test_han = words_han[t]
                test_latin = han_to_latin(test_han)
                words_latin_generated.append(test_latin)
                logger.debug(f'{test_han} phonetic romanization {test_latin}')

                # fail on wrong romaja
                assert test_latin == words_latin[t]

                # test full breakdown
                test_phonemes = ' '.join(breakdown_word(test_han))
                logger.info(f'{test_han} phoneme breakdown = {test_phonemes}')

                # fail on wrong phonemes
                assert test_phonemes == phonemes[t]
            
            except AssertionError:
                logger.error(f'test failure at "{test_phrase}": {words_han[t]}')
                fails.append(traceback.format_exc())
        # end for words
        
        logger.info(f'{" ".join(words_han)} => {" ".join(words_latin_generated)}')
    # end for phrases

    if len(fails) == 0:
        logger.info(f'** all korean breakdown tests passed **')
    else:
        logger.error(
            f'some korean breakdown tests failed:\n' +
            "\n".join(f'- {fail}' for fail in fails)
        )
# end main
