# Papagayo-NG, a lip-sync tool for use with several different animation suites
# Original Copyright (C) 2005 Mike Clifton
# Contact information at http://www.lostmarble.com
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

#import os
import shutil
import codecs
import importlib

try:
    import configparser
except ImportError:
    import ConfigParser as configparser
# import wx

from utilities import *
from PronunciationDialogQT import PronunciationDialog
import SoundPlayer
import traceback
#import sys
#import breakdowns

strip_symbols = '.,!?;-/()"'
strip_symbols += '\N{INVERTED QUESTION MARK}'


###############################################################

class LipsyncPhoneme:
    def __init__(self):
        self.text = ""
        self.frame = 0
        self.is_phoneme = True


###############################################################

class LipsyncWord:
    def __init__(self):
        self.text = ""
        self.start_frame = 0
        self.end_frame = 0
        self.phonemes = []
        self.is_phoneme = False

    def run_breakdown(self, parentWindow, language, languagemanager, phonemeset):
        self.phonemes = []
        try:
            text = self.text.strip(strip_symbols)
            details = languagemanager.language_table[language]
            if details["type"] == "breakdown":
                #exec ("import %s as breakdown" % details["breakdown_class"])
                breakdown = importlib.import_module(details["breakdown_class"])
                pronunciation_raw = breakdown.breakdownWord(text)
            elif details["type"] == "dictionary":
                if languagemanager.current_language != language:
                    languagemanager.load_language(details)
                    languagemanager.current_language = language
                if details["case"] == "upper":
                    pronunciation_raw = languagemanager.raw_dictionary[text.upper()]
                elif details["case"] == "lower":
                    pronunciation_raw = languagemanager.raw_dictionary[text.lower()]
                else:
                    pronunciation_raw = languagemanager.raw_dictionary[text]
            else:
                pronunciation_raw = phonemeDictionary[text.upper()]

            pronunciation = []
            for i in range(len(pronunciation_raw)):
                try:
                    pronunciation.append(phonemeset.conversion[pronunciation_raw[i]])
                except:
                    print(("Unknown phoneme:", pronunciation_raw[i], "in word:", text))

            for p in pronunciation:
                if len(p) == 0:
                    continue
                phoneme = LipsyncPhoneme()
                phoneme.text = p
                self.phonemes.append(phoneme)
        except KeyError:
            # this word was not found in the phoneme dictionary
            # TODO: This now depends on QT, make it neutral!
            dlg = PronunciationDialog(parentWindow, phonemeset.set)
            dlg.word_label.setText(dlg.word_label.text() + ' ' + self.text)
            dlg.exec_()
            if dlg.gave_ok:
                for p in dlg.phoneme_ctrl.text().split():
                    if len(p) == 0:
                        continue
                    phoneme = LipsyncPhoneme()
                    phoneme.text = p
                    self.phonemes.append(phoneme)
            dlg.destroy()

    def reposition_phoneme(self, phoneme):
        id = 0
        for i in range(len(self.phonemes)):
            if phoneme is self.phonemes[i]:
                id = i
        if (id > 0) and (phoneme.frame < self.phonemes[id - 1].frame + 1):
            phoneme.frame = self.phonemes[id - 1].frame + 1
        if (id < len(self.phonemes) - 1) and (phoneme.frame > self.phonemes[id + 1].frame - 1):
            phoneme.frame = self.phonemes[id + 1].frame - 1
        if phoneme.frame < self.start_frame:
            phoneme.frame = self.start_frame
        if phoneme.frame > self.end_frame:
            phoneme.frame = self.end_frame


###############################################################

class LipsyncPhrase:
    def __init__(self):
        self.text = ""
        self.start_frame = 0
        self.end_frame = 0
        self.words = []
        self.is_phoneme = False

    def run_breakdown(self, parentWindow, language, languagemanager, phonemeset):
        self.words = []
        for w in self.text.split():
            if len(w) == 0:
                continue
            word = LipsyncWord()
            word.text = w
            self.words.append(word)
        for word in self.words:
            word.run_breakdown(parentWindow, language, languagemanager, phonemeset)

    def reposition_word(self, word):
        id = 0
        for i in range(len(self.words)):
            if word is self.words[i]:
                id = i
        if (id > 0) and (word.start_frame < self.words[id - 1].end_frame + 1):
            word.start_frame = self.words[id - 1].end_frame + 1
            if word.end_frame < word.start_frame + 1:
                word.end_frame = word.start_frame + 1
        if (id < len(self.words) - 1) and (word.end_frame > self.words[id + 1].start_frame - 1):
            word.end_frame = self.words[id + 1].start_frame - 1
            if word.start_frame > word.end_frame - 1:
                word.start_frame = word.end_frame - 1
        if word.start_frame < self.start_frame:
            word.start_frame = self.start_frame
        if word.end_frame > self.end_frame:
            word.end_frame = self.end_frame
        if word.end_frame < word.start_frame:
            word.end_frame = word.start_frame
        frameDuration = word.end_frame - word.start_frame + 1
        phonemeCount = len(word.phonemes)
        # now divide up the total time by phonemes
        if frameDuration > 0 and phonemeCount > 0:
            framesPerPhoneme = float(frameDuration) / float(phonemeCount)
            if framesPerPhoneme < 1:
                framesPerPhoneme = 1
        else:
            framesPerPhoneme = 1
        # finally, assign frames based on phoneme durations
        curFrame = word.start_frame
        for phoneme in word.phonemes:
            phoneme.frame = int(round(curFrame))
            curFrame += framesPerPhoneme
        for phoneme in word.phonemes:
            word.reposition_phoneme(phoneme)


###############################################################

class LipsyncVoice:
    def __init__(self, name="Voice"):
        self.name = name
        self.text = ""
        self.phrases = []

    def run_breakdown(self, frameDuration, parentWindow, language, languagemanager, phonemeset):
        # make sure there is a space after all punctuation marks
        repeatLoop = True
        while repeatLoop:
            repeatLoop = False
            for i in range(len(self.text) - 1):
                if (self.text[i] in ".,!?;-/()") and (not self.text[i + 1].isspace()):
                    self.text = self.text[:i + 1] + ' ' + self.text[i + 1:]
                    repeatLoop = True
                    break
        # break text into phrases
        self.phrases = []
        for line in self.text.splitlines():
            if len(line) == 0:
                continue
            phrase = LipsyncPhrase()
            phrase.text = line
            self.phrases.append(phrase)
        # now break down the phrases
        for phrase in self.phrases:
            phrase.run_breakdown(parentWindow, language, languagemanager, phonemeset)
        # for first-guess frame alignment, count how many phonemes we have
        phonemeCount = 0
        for phrase in self.phrases:
            for word in phrase.words:
                if len(word.phonemes) == 0:  # deal with unknown words
                    phonemeCount += 4
                for phoneme in word.phonemes:
                    phonemeCount += 1
        # now divide up the total time by phonemes
        if frameDuration > 0 and phonemeCount > 0:
            framesPerPhoneme = int(float(frameDuration) / float(phonemeCount))
            if framesPerPhoneme < 1:
                framesPerPhoneme = 1
        else:
            framesPerPhoneme = 1
        # finally, assign frames based on phoneme durations
        curFrame = 0
        for phrase in self.phrases:
            for word in phrase.words:
                for phoneme in word.phonemes:
                    phoneme.frame = curFrame
                    curFrame += framesPerPhoneme
                if len(word.phonemes) == 0:  # deal with unknown words
                    word.start_frame = curFrame
                    word.end_frame = curFrame + 3
                    curFrame += 4
                else:
                    word.start_frame = word.phonemes[0].frame
                    word.end_frame = word.phonemes[-1].frame + framesPerPhoneme - 1
            phrase.start_frame = phrase.words[0].start_frame
            phrase.end_frame = phrase.words[-1].end_frame

    def reposition_phrase(self, phrase, lastFrame):
        id = 0
        for i in range(len(self.phrases)):
            if phrase is self.phrases[i]:
                id = i
        if (id > 0) and (phrase.start_frame < self.phrases[id - 1].end_frame + 1):
            phrase.start_frame = self.phrases[id - 1].end_frame + 1
            if phrase.end_frame < phrase.start_frame + 1:
                phrase.end_frame = phrase.start_frame + 1
        if (id < len(self.phrases) - 1) and (phrase.end_frame > self.phrases[id + 1].start_frame - 1):
            phrase.end_frame = self.phrases[id + 1].start_frame - 1
            if phrase.start_frame > phrase.end_frame - 1:
                phrase.start_frame = phrase.end_frame - 1
        if phrase.start_frame < 0:
            phrase.start_frame = 0
        if phrase.end_frame > lastFrame:
            phrase.end_frame = lastFrame
        if phrase.start_frame > phrase.end_frame - 1:
            phrase.start_frame = phrase.end_frame - 1
        # for first-guess frame alignment, count how many phonemes we have
        frameDuration = phrase.end_frame - phrase.start_frame + 1
        phonemeCount = 0
        for word in phrase.words:
            if len(word.phonemes) == 0:  # deal with unknown words
                phonemeCount += 4
            for phoneme in word.phonemes:
                phonemeCount += 1
        # now divide up the total time by phonemes
        if frameDuration > 0 and phonemeCount > 0:
            framesPerPhoneme = float(frameDuration) / float(phonemeCount)
            if framesPerPhoneme < 1:
                framesPerPhoneme = 1
        else:
            framesPerPhoneme = 1
        # finally, assign frames based on phoneme durations
        curFrame = phrase.start_frame
        for word in phrase.words:
            for phoneme in word.phonemes:
                phoneme.frame = int(round(curFrame))
                curFrame += framesPerPhoneme
            if len(word.phonemes) == 0:  # deal with unknown words
                word.start_frame = curFrame
                word.end_frame = curFrame + 3
                curFrame += 4
            else:
                word.start_frame = word.phonemes[0].frame
                word.end_frame = word.phonemes[-1].frame + int(round(framesPerPhoneme)) - 1
            phrase.RepositionWord(word)

    def open(self, inFile):
        self.name = inFile.readline().strip()
        tempText = inFile.readline().strip()
        self.text = tempText.replace('|', '\n')
        numPhrases = int(inFile.readline())
        for p in range(numPhrases):
            phrase = LipsyncPhrase()
            phrase.text = inFile.readline().strip()
            phrase.start_frame = int(inFile.readline())
            phrase.end_frame = int(inFile.readline())
            numWords = int(inFile.readline())
            for w in range(numWords):
                word = LipsyncWord()
                wordLine = inFile.readline().split()
                word.text = wordLine[0]
                word.start_frame = int(wordLine[1])
                word.end_frame = int(wordLine[2])
                numPhonemes = int(wordLine[3])
                for p in range(numPhonemes):  # TODO: Might want to rename p to make it clearer
                    phoneme = LipsyncPhoneme()
                    phonemeLine = inFile.readline().split()
                    phoneme.frame = int(phonemeLine[0])
                    phoneme.text = phonemeLine[1]
                    word.phonemes.append(phoneme)
                phrase.words.append(word)
            self.phrases.append(phrase)

    def save(self, outFile):
        outFile.write("\t%s\n" % self.name)
        tempText = self.text.replace('\n', '|')
        outFile.write("\t%s\n" % tempText)
        outFile.write("\t%d\n" % len(self.phrases))
        for phrase in self.phrases:
            outFile.write("\t\t%s\n" % phrase.text)
            outFile.write("\t\t%d\n" % phrase.start_frame)
            outFile.write("\t\t%d\n" % phrase.end_frame)
            outFile.write("\t\t%d\n" % len(phrase.words))
            for word in phrase.words:
                outFile.write("\t\t\t%s %d %d %d\n" % (word.text, word.start_frame, word.endFrame, len(word.phonemes)))
                for phoneme in word.phonemes:
                    outFile.write("\t\t\t\t%d %s\n" % (phoneme.frame, phoneme.text))

    def get_phoneme_at_frame(self, frame):
        for phrase in self.phrases:
            if (frame <= phrase.end_frame) and (frame >= phrase.start_frame):
                # we found the phrase that contains this frame
                word = None
                for w in phrase.words:
                    if (frame <= w.end_frame) and (frame >= w.start_frame):
                        word = w  # the frame is inside this word
                        break
                if word is not None:
                    # we found the word that contains this frame
                    for i in range(len(word.phonemes) - 1, -1, -1):
                        if frame >= word.phonemes[i].frame:
                            return word.phonemes[i].text
                break
        return "rest"

    def export(self, path):

        outFile = open(path, 'w')
        outFile.write("MohoSwitch1\n")
        phoneme = ""
        if len(self.phrases) > 0:
            start_frame = self.phrases[0].start_frame
            end_frame = self.phrases[-1].end_frame
            if start_frame != 0:
                phoneme = "rest"
                outFile.write("%d %s\n" % (1, phoneme))
        else:
            start_frame = 0
            end_frame = 1

        for frame in range(start_frame, end_frame + 1):
            nextPhoneme = self.get_phoneme_at_frame(frame)
            if nextPhoneme != phoneme:
                if phoneme == "rest":
                    # export an extra "rest" phoneme at the end of a pause between words or phrases
                    outFile.write("%d %s\n" % (frame, phoneme))
                phoneme = nextPhoneme
                outFile.write("%d %s\n" % (frame + 1, phoneme))
        outFile.write("%d %s\n" % (end_frame + 2, "rest"))
        outFile.close()

    def export_images(self, path, currentmouth):
        # TODO: self.config still relies on wx!
        try:
            self.config
        except AttributeError:
            self.config = wx.Config("Papagayo-NG", "Lost Marble")
        phoneme = ""
        if len(self.phrases) > 0:
            start_frame = self.phrases[0].start_frame
            end_frame = self.phrases[-1].end_frame
        else:
            start_frame = 0
            end_frame = 1
        if not self.config.Read("MouthDir"):
            print("Use normal procedure.\n")
            phonemedict = {}
            for files in os.listdir(
                            os.path.join(os.path.dirname(os.path.abspath(__file__)), "rsrc/mouths/") + currentmouth):
                phonemedict[os.path.splitext(files)[0]] = os.path.splitext(files)[1]
            for frame in range(start_frame, end_frame + 1):
                phoneme = self.get_phoneme_at_frame(frame)
                try:
                    shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                             "rsrc/mouths/") + currentmouth + "/" + phoneme + phonemedict[phoneme],
                                path + str(frame).rjust(6, '0') + phoneme + phonemedict[phoneme])
                except KeyError:
                    print("Phoneme '" + phoneme + "' does not exist in chosen directory.")

        else:
            print("Use this dir:" + self.config.Read("MouthDir") + "\n")
            phonemedict = {}
            for files in os.listdir(self.config.Read("MouthDir")):
                phonemedict[os.path.splitext(files)[0]] = os.path.splitext(files)[1]
            for frame in range(start_frame, end_frame + 1):
                phoneme = self.get_phoneme_at_frame(frame)
                try:
                    shutil.copy(self.config.Read("MouthDir") + "/" + phoneme + phonemedict[phoneme],
                                path + str(frame).rjust(6, '0') + phoneme + phonemedict[phoneme])
                except KeyError:
                    print("Phoneme '" + phoneme + "' does not exist in chosen directory.")

    def export_alelo(self, path, language, languagemanager):
        outFile = open(path, 'w')
        for phrase in self.phrases:
            for word in phrase.words:
                text = word.text.strip(strip_symbols)
                details = languagemanager.language_table[language]
                if languagemanager.current_language != language:
                    languagemanager.LoadLanguage(details)
                    languagemanager.current_language = language
                if details["case"] == "upper":
                    pronunciation = languagemanager.raw_dictionary[text.upper()]
                elif details["case"] == "lower":
                    pronunciation = languagemanager.raw_dictionary[text.lower()]
                else:
                    pronunciation = languagemanager.raw_dictionary[text]
                first = True
                position = -1
                #               print word.text
                for phoneme in word.phonemes:
                    #                   print phoneme.text
                    if first:
                        first = False
                    else:
                        try:
                            outFile.write("%d %d %s\n" % (
                                lastPhoneme.frame, phoneme.frame - 1, languagemanager.export_conversion[lastPhoneme_text]))
                        except KeyError:
                            pass
                    if phoneme.text.lower() == "sil":
                        position += 1
                        outFile.write("%d %d sil\n" % (phoneme.frame, phoneme.frame))
                        continue
                    position += 1
                    lastPhoneme_text = pronunciation[position]
                    lastPhoneme = phoneme
                try:
                    outFile.write("%d %d %s\n" % (
                        lastPhoneme.frame, word.end_frame, languagemanager.export_conversion[lastPhoneme_text]))
                except KeyError:
                    pass
        outFile.close()


###############################################################

class LipsyncDoc:
    def __init__(self, langman, parent):
        self.dirty = False
        self.name = "Untitled"
        self.path = None
        self.fps = 24
        self.soundDuration = 72
        self.soundPath = ""
        self.sound = None
        self.voices = []
        self.current_voice = None
        self.language_manager = langman
        self.parent = parent

    def __del__(self):
        # Properly close down the sound object
        if self.sound is not None:
            del self.sound

    def open(self, path):
        self.dirty = False
        self.path = os.path.normpath(path)
        self.name = os.path.basename(path)
        self.sound = None
        self.voices = []
        self.current_voice = None
        inFile = codecs.open(self.path, 'r', 'utf-8', 'replace')
        inFile.readline()  # discard the header
        self.soundPath = inFile.readline().strip()
        if not os.path.isabs(self.soundPath):
            self.soundPath = os.path.normpath(os.path.dirname(self.path) + '/' + self.soundPath)
        self.fps = int(inFile.readline())
        print(("self.path: %s" % self.path))
        self.soundDuration = int(inFile.readline())
        print(("self.soundDuration: %d" % self.soundDuration))
        numVoices = int(inFile.readline())
        for i in range(numVoices):
            voice = LipsyncVoice()
            voice.open(inFile)
            self.voices.append(voice)
        inFile.close()
        self.open_audio(self.soundPath)
        if len(self.voices) > 0:
            self.current_voice = self.voices[0]

    def open_audio(self, path):
        if self.sound is not None:
            del self.sound
            self.sound = None
        # self.soundPath = str(path.encode("utf-8"))
        self.soundPath = path  # .encode('latin-1', 'replace')
        self.sound = SoundPlayer.SoundPlayer(self.soundPath, self.parent)
        if self.sound.IsValid():
            print("valid sound")
            self.soundDuration = int(self.sound.Duration() * self.fps)
            print(("self.sound.Duration(): %d" % int(self.sound.Duration())))
            print(("frameRate: %d" % int(self.fps)))
            print(("soundDuration1: %d" % self.soundDuration))
            if self.soundDuration < self.sound.Duration() * self.fps:
                self.soundDuration += 1
                print(("soundDuration2: %d" % self.soundDuration))
        else:
            self.sound = None

    def save(self, path):
        self.path = os.path.normpath(path)
        self.name = os.path.basename(path)
        if os.path.dirname(self.path) == os.path.dirname(self.soundPath):
            savedSoundPath = os.path.basename(self.soundPath)
        else:
            savedSoundPath = self.soundPath
        outFile = codecs.open(self.path, 'w', 'utf-8', 'replace')
        outFile.write("lipsync version 1\n")
        outFile.write("%s\n" % savedSoundPath)
        outFile.write("%d\n" % self.fps)
        outFile.write("%d\n" % self.soundDuration)
        outFile.write("%d\n" % len(self.voices))
        for voice in self.voices:
            voice.save(outFile)
        outFile.close()
        self.dirty = False


from phonemes import *


class PhonemeSet:
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        self.set = []
        self.conversion = {}
        self.alternatives = phoneme_sets
        self.load(self.alternatives[0])

    def load(self, name=''):
        if name in self.alternatives:
            print("import phonemes_%s as phonemeset" % name)
            phonemeset = importlib.import_module("phonemes_%s" % name)
            # exec("import phonemes_%s as phonemeset" % name)
            # import phonemes_preston_blair as phonemeset
            self.set = phonemeset.phoneme_set
            self.conversion = phonemeset.phoneme_conversion
        else:
            print(("Can't find phonemeset! (%s)" % name))
            return


class LanguageManager:
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        self.language_table = {}
        self.phoneme_dictionary = {}
        self.raw_dictionary = {}
        self.current_language = ""

        self.export_conversion = {}
        self.init_languages()

    def load_dictionary(self, path):
        try:
            inFile = open(path, 'r')
        except:
            print(("Unable to open phoneme dictionary!:", path))
            return
        # process dictionary entries
        for line in inFile.readlines():
            if line[0] == '#':
                continue  # skip comments in the dictionary
            # strip out leading/trailing whitespace
            line.strip()
            line = line.rstrip('\r\n')

            # split into components
            entry = line.split()
            if len(entry) == 0:
                continue
            # check if this is a duplicate word (alternate transcriptions end with a number in parentheses) - if so, throw it out
            if entry[0].endswith(')'):
                continue
            # add this entry to the in-memory dictionary
            for i in range(len(entry)):
                if i == 0:
                    self.raw_dictionary[entry[0]] = []
                else:
                    rawentry = entry[i]
                    self.raw_dictionary[entry[0]].append(rawentry)
        inFile.close()
        inFile = None

    def load_language(self, language_config, force=False):
        if self.current_language == language_config["label"] and not force:
            return
        self.current_language = language_config["label"]

        if "dictionaries" in language_config:
            for dictionary in language_config["dictionaries"]:
                self.load_dictionary(
                    os.path.join(get_main_dir(), language_config["location"], language_config["dictionaries"][dictionary]))

    def language_details(self, dirname, names):
        if "language.ini" in names:
            config = configparser.ConfigParser()
            config.read(os.path.join(dirname, "language.ini"))
            label = config.get("configuration", "label")
            ltype = config.get("configuration", "type")
            details = {}
            details["label"] = label
            details["type"] = ltype
            details["location"] = dirname
            if ltype == "breakdown":
                details["breakdown_class"] = config.get("configuration", "breakdown_class")
                self.language_table[label] = details
            elif ltype == "dictionary":
                try:
                    details["case"] = config.get("configuration", "case")
                except:
                    details["case"] = "upper"
                details["dictionaries"] = {}

                if config.has_section('dictionaries'):
                    for key, value in config.items('dictionaries'):
                        details["dictionaries"][key] = value
                self.language_table[label] = details
            else:
                print("unknown type ignored language not added to table")

    def init_languages(self):
        if len(self.language_table) > 0:
            return
        for path, dirs, files in os.walk(os.path.join(get_main_dir(), "rsrc/languages")):
            if "language.ini" in files:
                self.language_details(path, files)
