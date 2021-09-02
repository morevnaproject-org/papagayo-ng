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

import math
import shutil
import sys

import anytree
from anytree import NodeMixin, Node, RenderTree
import importlib
import json
import fnmatch

from anytree.exporter import DotExporter

import utilities

try:
    import auto_recognition
except ModuleNotFoundError:
    auto_recognition = None
import os

from Rhubarb import Rhubarb, RhubarbTimeoutException

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import PySide2.QtCore as QtCore

import utilities
from PronunciationDialogQT import PronunciationDialog, show_pronunciation_dialog

ini_path = os.path.join(utilities.get_app_data_path(), "settings.ini")
config = QtCore.QSettings(ini_path, QtCore.QSettings.IniFormat)

if config.value("audio_output", "old") == "old":
    import SoundPlayer as SoundPlayer
else:
    if sys.platform == "win32":
        import SoundPlayerNew as SoundPlayer
    elif sys.platform == "darwin":
        import SoundPlayerOSX as SoundPlayer
    else:
        import SoundPlayer as SoundPlayer

strip_symbols = '.,!?;-/()"'
strip_symbols += '\N{INVERTED QUESTION MARK}'
strip_symbols += "'"


###############################################################

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
            in_file = open(path, 'r')
        except FileNotFoundError:
            print("Unable to open phoneme dictionary!:{}".format(path))
            return
        new_cmu_version = False
        if in_file.readline().startswith(";;; # CMUdict"):
            new_cmu_version = True
        # process dictionary entries
        for line in in_file.readlines():
            if not new_cmu_version:
                if line[0] == '#':
                    continue  # skip comments in the dictionary
            else:
                if line.startswith(";;;"):
                    continue
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
        in_file.close()
        in_file = None

    def load_language(self, language_config, force=False):
        if self.current_language == language_config["label"] and not force:
            return
        self.current_language = language_config["label"]

        if "dictionaries" in language_config:
            for dictionary in language_config["dictionaries"]:
                self.load_dictionary(os.path.join(utilities.get_main_dir(),
                                                  language_config["location"],
                                                  language_config["dictionaries"][dictionary]))

    def language_details(self, dirname, names):
        if "language.ini" in names:
            config = configparser.ConfigParser()
            config.read(os.path.join(dirname, "language.ini"))
            label = config.get("configuration", "label")
            ltype = config.get("configuration", "type")
            details = {"label": label, "type": ltype, "location": dirname}
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
        for path, dirs, files in os.walk(os.path.join(utilities.get_main_dir(), "rsrc", "languages")):
            if "language.ini" in files:
                self.language_details(path, files)


class LipSyncObject(NodeMixin):
    '''
    This should be a general class for all LipSync Objects
    '''

    def __init__(self, parent=None, children=None, object_type="voice", text="", start_frame=0, end_frame=0, name="",
                 tags=None, num_children=0, sound_duration=0, fps=24):
        self.parent = parent
        ini_path = os.path.join(utilities.get_app_data_path(), "settings.ini")
        self.config = QtCore.QSettings(ini_path, QtCore.QSettings.IniFormat)
        self.config.setFallbacksEnabled(False)  # File only, not registry or or.
        if children:
            self.children = children
        self.object_type = object_type
        self.name = name
        self.text = text
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.tags = tags if tags else []
        self.num_children = num_children
        self.move_button = None
        if self.parent:
            self.sound_duration = self.root.sound_duration
        else:
            self.sound_duration = sound_duration
        self.fps = fps
        self.last_returned_frame = "rest"

    def get_min_size(self):
        # An object should be at least be able to contain all it's phonemes since only 1 phoneme per frame is allowed.
        if self.object_type == "phoneme":
            num_of_phonemes = 1
        else:
            num_of_phonemes = 0
            for descendant in self.descendants:
                if descendant.object_type == "phoneme":
                    num_of_phonemes += 1
        return num_of_phonemes

    def get_left_sibling(self):
        return anytree.util.leftsibling(self)

    def get_right_sibling(self):
        return anytree.util.rightsibling(self)

    def get_parent(self):
        if self.object_type != "phrase":
            return self.parent
        else:
            return None

    def get_frame_size(self):
        if self.object_type == "phoneme":
            return 1
        else:
            return self.end_frame - self.start_frame

    def has_shrink_room(self):
        if self.object_type == "phoneme":
            return False
        else:
            if self.get_min_size() >= self.get_frame_size():
                return False
            else:
                return True

    def has_left_sibling(self):
        try:
            left_sibling = bool(self.get_left_sibling())
        except AttributeError:
            left_sibling = False
        return left_sibling

    def has_right_sibling(self):
        try:
            right_sibling = bool(self.get_right_sibling())
        except AttributeError:
            right_sibling = False
        return right_sibling

    def get_left_max(self):
        if self.has_left_sibling():
            temp = self.get_left_sibling()
            if not temp.object_type == "phoneme":
                left_most_pos = temp.end_frame
            else:
                left_most_pos = temp.end_frame + 1
        else:
            left_most_pos = self.parent.start_frame
        return left_most_pos

    def get_right_max(self):
        if self.has_right_sibling():
            right_most_pos = self.get_right_sibling().start_frame
        else:
            if self.parent.object_type == "voice":
                right_most_pos = self.root.sound_duration
            elif self.parent.object_type == "project":
                right_most_pos = self.root.sound_duration
            else:
                try:
                    right_most_pos = self.parent.end_frame
                except AttributeError:
                    right_most_pos = self.root.sound_duration
        return right_most_pos

    def get_phoneme_at_frame(self, frame):
        for descendant in self.descendants:
            if descendant.object_type == "phoneme":
                if descendant.start_frame == frame:
                    self.last_returned_frame = descendant.text
                    return descendant.text

        if not self.config.value("RepeatLastPhoneme", True):
            return "rest"
        else:
            return self.last_returned_frame

    def reposition_to_left(self):
        if self.has_left_sibling():
            if self.object_type == "phoneme":
                self.start_frame = self.get_left_sibling().start_frame + 1
            else:
                self.start_frame = self.get_left_sibling().end_frame
                self.end_frame = self.start_frame + self.get_min_size()
                for child in self.children:
                    child.reposition_to_left()
        else:
            if self.object_type == "phoneme":
                self.start_frame = self.parent.start_frame
            else:
                self.start_frame = self.parent.name.node.start_frame
                self.end_frame = self.start_frame + self.get_min_size()
                for child in self.children:
                    child.reposition_to_left()

    def reposition_descendants(self, did_resize=False, x_diff=0):
        if did_resize:
            for child in self.children:
                child.reposition_to_left()
        else:
            for child in self.descendants:
                child.start_frame += x_diff
                child.end_frame += x_diff
                child.move_button.after_reposition()

    def reposition_descendants2(self, did_resize=False, x_diff=0):
        if did_resize:
            if self.object_type == "word":
                for position, child in enumerate(self.children):
                    child.start_frame = round(self.start_frame +
                                              ((self.get_frame_size() / self.get_min_size()) * position))
                    child.move_button.after_reposition()
                #self.wfv_parent.doc.dirty = True
            elif self.object_type == "phrase":
                extra_space = self.get_frame_size() - self.get_min_size()
                for child in self.children:
                    if child.has_left_sibling():
                        child.start_frame = child.get_left_sibling().end_frame
                        child.end_frame = child.start_frame + child.get_min_size()
                    else:
                        child.start_frame = self.start_frame
                        child.end_frame = child.start_frame + child.get_min_size()
                last_position = -1
                moved_child = False
                while extra_space > 0:
                    if last_position == len(self.children) - 1:
                        last_position = -1
                    if not moved_child:
                        last_position = -1
                    moved_child = False
                    for position, child in enumerate(self.children):
                        if child.has_left_sibling():
                            if child.start_frame < child.get_left_sibling().end_frame:
                                child.start_frame += 1
                                child.end_frame += 1
                            else:
                                if extra_space and not moved_child and (position > last_position):
                                    child.end_frame += 1
                                    extra_space -= 1
                                    moved_child = True
                                    last_position = position
                        else:
                            if extra_space and not moved_child and (position > last_position):
                                child.end_frame += 1
                                extra_space -= 1
                                moved_child = True
                                last_position = position
                    if not moved_child and extra_space == 0:
                        break
                for child in self.children:
                    child.move_button.after_reposition()
                    child.reposition_descendants2(True, 0)
                #self.wfv_parent.doc.dirty = True
        else:
            for child in self.descendants:
                child.start_frame += x_diff
                child.end_frame += x_diff
                child.move_button.after_reposition()
            #self.wfv_parent.doc.dirty = True

    def open(self, in_file):
        self.name = in_file.readline().strip()
        temp_text = in_file.readline().strip()
        self.text = temp_text.replace('|', '\n')
        num_phrases = int(in_file.readline())
        for p in range(num_phrases):
            self.num_children += 1
            phrase = LipSyncObject(object_type="phrase", parent=self)
            phrase.text = in_file.readline().strip()
            phrase.start_frame = int(in_file.readline())
            phrase.end_frame = int(in_file.readline())
            num_words = int(in_file.readline())
            for w in range(num_words):
                self.num_children += 1
                word = LipSyncObject(object_type="word", parent=phrase)
                word_line = in_file.readline().split()
                word.text = word_line[0]
                word.start_frame = int(word_line[1])
                word.end_frame = int(word_line[2])
                num_phonemes = int(word_line[3])
                for p2 in range(num_phonemes):
                    self.num_children += 1
                    phoneme = LipSyncObject(object_type="phoneme", parent=word)
                    phoneme_line = in_file.readline().split()
                    phoneme.start_frame = phoneme.end_frame = int(phoneme_line[0])
                    phoneme.text = phoneme_line[1]

    def save(self, out_file):
        out_file.write("\t{}\n".format(self.name))
        temp_text = self.text.replace('\n', '|')
        out_file.write("\t{}\n".format(temp_text))
        out_file.write("\t{:d}\n".format(len(self.children)))
        for phrase in self.children:
            out_file.write("\t\t{}\n".format(phrase.text))
            out_file.write("\t\t{:d}\n".format(phrase.start_frame))
            out_file.write("\t\t{:d}\n".format(phrase.end_frame))
            out_file.write("\t\t{:d}\n".format(len(phrase.children)))
            for word in phrase.children:
                out_file.write(
                    "\t\t\t{} {:d} {:d} {:d}\n".format(word.text, word.start_frame, word.end_frame, len(word.children)))
                for phoneme in word.children:
                    out_file.write("\t\t\t\t{:d} {}\n".format(phoneme.start_frame, phoneme.text))

    def run_breakdown(self, frame_duration, parent_window, language, languagemanager, phonemeset):
        if self.object_type == "voice":
            # First we delete all children
            self.children = []
            # make sure there is a space after all punctuation marks
            repeat_loop = True
            while repeat_loop:
                repeat_loop = False
                for i in range(len(self.text) - 1):
                    if (self.text[i] in ".,!?;-/()") and (not self.text[i + 1].isspace()):
                        self.text = "{} {}".format(self.text[:i + 1], self.text[i + 1:])
                        repeat_loop = True
                        break
            # break text into phrases
            # self.phrases = []
            for line in self.text.splitlines():
                if len(line) == 0:
                    continue
                phrase = LipSyncObject(object_type="phrase", parent=self)
                phrase.text = line
                # self.children.append(phrase)
            # now break down the phrases
            for phrase in self.children:
                return_value = phrase.run_breakdown(frame_duration, parent_window, language, languagemanager, phonemeset)
                if return_value == -1:
                    return -1
            # for first-guess frame alignment, count how many phonemes we have
            phoneme_count = 0
            for phrase in self.children:
                for word in phrase.children:
                    if len(word.children) == 0:  # deal with unknown words
                        phoneme_count += 4
                    for phoneme in word.children:
                        phoneme_count += 1
            # now divide up the total time by phonemes
            if frame_duration > 0 and phoneme_count > 0:
                frames_per_phoneme = int(float(frame_duration) / float(phoneme_count))
                if frames_per_phoneme < 1:
                    frames_per_phoneme = 1
            else:
                frames_per_phoneme = 1
            # finally, assign frames based on phoneme durations
            cur_frame = 0
            for phrase in self.children:
                for word in phrase.children:
                    for phoneme in word.children:
                        phoneme.start_frame = phoneme.end_frame = cur_frame
                        cur_frame += frames_per_phoneme
                    if len(word.children) == 0:  # deal with unknown words
                        word.start_frame = cur_frame
                        word.end_frame = cur_frame + 3
                        cur_frame += 4
                    else:
                        word.start_frame = word.children[0].start_frame
                        word.end_frame = word.children[-1].end_frame + frames_per_phoneme - 1
                phrase.start_frame = phrase.children[0].start_frame
                phrase.end_frame = phrase.children[-1].end_frame
        elif self.object_type == "phrase":
            # self.words = []
            for w in self.text.split():
                if len(w) == 0:
                    continue
                word = LipSyncObject(object_type="word", parent=self)
                word.text = w
                # self.words.append(word)
            for word in self.children:
                result = word.run_breakdown(frame_duration, parent_window, language, languagemanager, phonemeset)
                if result == -1:
                    return -1
        elif self.object_type == "word":
            # self.phonemes = []
            try:
                text = self.text.strip(strip_symbols)
                details = languagemanager.language_table[language]
                if details["type"] == "breakdown":
                    breakdown = importlib.import_module(details["breakdown_class"])
                    pronunciation_raw = breakdown.breakdown_word(text)
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
                        pronunciation_phoneme = pronunciation_raw[i].rstrip("0123456789")
                        pronunciation.append(phonemeset.conversion[pronunciation_phoneme])
                    except KeyError:
                        print(("Unknown phoneme:", pronunciation_raw[i], "in word:", text))

                for p in pronunciation:
                    if len(p) == 0:
                        continue
                    phoneme = LipSyncObject(object_type="phoneme", parent=self)
                    phoneme.text = p
                    # self.phonemes.append(phoneme)
            except KeyError:
                # this word was not found in the phoneme dictionary
                # TODO: This now depends on QT, make it neutral!
                return_value = show_pronunciation_dialog(parent_window, phonemeset.set, self.text)
                if return_value == -1:
                    return -1
                elif not return_value:
                    pass
                else:
                    conversion_map_to_cmu = {v: k for k, v in parent_window.doc.parent.phonemeset.conversion.items()}
                    phonemes_as_list = []
                    for p in return_value:
                        phoneme = LipSyncObject(object_type="phoneme", parent=self)
                        phoneme.text = p
                        phoneme_as_cmu = conversion_map_to_cmu.get(p, "rest")
                        phonemes_as_list.append(phoneme_as_cmu)
                    languagemanager.raw_dictionary[self.text.upper()] = phonemes_as_list

    ###

    def export(self, path):

        out_file = open(path, 'w')
        out_file.write("MohoSwitch1\n")
        phoneme = ""
        if len(self.children) > 0:
            start_frame = self.children[0].start_frame
            end_frame = self.children[-1].end_frame
            if start_frame != 0:
                phoneme = "rest"
                out_file.write("{:d} {}\n".format(1, phoneme))
        else:
            start_frame = 0
            end_frame = 1
        last_phoneme = self.leaves[0]
        for phoneme in self.leaves:
            if last_phoneme.text != phoneme.text:
                if phoneme.text == "rest":
                    # export an extra "rest" phoneme at the end of a pause between words or phrases
                    out_file.write("{:d} {}\n".format(phoneme.start_frame, phoneme.text))
            last_phoneme = phoneme
            out_file.write("{:d} {}\n".format(phoneme.start_frame + 1, phoneme.text))
        out_file.write("{:d} {}\n".format(end_frame + 2, "rest"))
        out_file.close()

    def export_images(self, path, currentmouth):
        if not self.config.value("MouthDir"):
            print("Use normal procedure.\n")
            phonemedict = {}
            for files in os.listdir(os.path.join(utilities.get_main_dir(), "rsrc", "mouths", currentmouth)):
                phonemedict[os.path.splitext(files)[0]] = os.path.splitext(files)[1]
            for phoneme in self.leaves:
                try:
                    shutil.copy(os.path.join(utilities.get_main_dir(), "rsrc", "mouths", currentmouth) + "/" +
                                phoneme.text + phonemedict[phoneme.text],
                                path + str(phoneme.start_frame).rjust(6, '0') +
                                phoneme.text + phonemedict[phoneme.text])
                except KeyError:
                    print("Phoneme \'{0}\' does not exist in chosen directory.".format(phoneme.text))

        else:
            print("Use this dir: {}\n".format(self.config.value("MouthDir")))
            phonemedict = {}
            for files in os.listdir(self.config.value("MouthDir")):
                phonemedict[os.path.splitext(files)[0]] = os.path.splitext(files)[1]
            for phoneme in self.leaves:
                try:
                    shutil.copy(
                        "{}/{}{}".format(self.config.value("MouthDir"), phoneme.text, phonemedict[phoneme.text]),
                        "{}{}{}{}".format(path, str(phoneme.start_frame).rjust(6, "0"), phoneme.text,
                                          phonemedict[phoneme.text]))
                except KeyError:
                    print("Phoneme \'{0}\' does not exist in chosen directory.".format(phoneme.text))

    def export_alelo(self, path, language, languagemanager):
        out_file = open(path, 'w')
        for phrase in self.children:
            for word in phrase.children:
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
                for phoneme in word.children:
                    #                   print phoneme.text
                    if first:
                        first = False
                    else:
                        try:
                            out_file.write("{:d} {:d} {}\n".format(last_phoneme.start_frame, phoneme.start_frame - 1,
                                                                   languagemanager.export_conversion[
                                                                       last_phoneme_text]))
                        except KeyError:
                            pass
                    if phoneme.text.lower() == "sil":
                        position += 1
                        out_file.write("{:d} {:d} sil\n".format(phoneme.start_frame, phoneme.start_frame))
                        continue
                    position += 1
                    last_phoneme_text = pronunciation[position]
                    last_phoneme = phoneme
                try:
                    out_file.write("{:d} {:d} {}\n".format(last_phoneme.start_frame, word.end_frame,
                                                           languagemanager.export_conversion[last_phoneme_text]))
                except KeyError:
                    pass
        out_file.close()

    def export_json(self, path):
        if len(self.children) > 0:
            start_frame = self.children[0].start_frame
            end_frame = self.children[-1].end_frame
        else:  # No phrases means no data, so do nothing
            return
        json_data = {"name": self.name, "start_frame": start_frame, "end_frame": end_frame,
                     "text": self.text, "num_children": self.num_children, "fps": self.fps}
        list_of_phrases = []
        list_of_used_phonemes = []
        for phr_id, phrase in enumerate(self.children):
            dict_phrase = {"id": phr_id, "text": phrase.text, "start_frame": phrase.start_frame,
                           "end_frame": phrase.end_frame, "tags": phrase.tags}
            list_of_words = []
            for wor_id, word in enumerate(phrase.children):
                dict_word = {"id": wor_id, "text": word.text, "start_frame": word.start_frame,
                             "end_frame": word.end_frame, "tags": word.tags + phrase.tags}
                list_of_phonemes = []
                for pho_id, phoneme in enumerate(word.children):
                    dict_phoneme = {"id": pho_id, "text": phoneme.text, "frame": phoneme.start_frame,
                                    "tags": phoneme.tags + word.tags + phrase.tags}
                    list_of_phonemes.append(dict_phoneme)
                    if phoneme.text not in list_of_used_phonemes:
                        list_of_used_phonemes.append(phoneme.text)
                dict_word["phonemes"] = list_of_phonemes
                list_of_words.append(dict_word)
            dict_phrase["words"] = list_of_words
            list_of_phrases.append(dict_phrase)
        json_data["phrases"] = list_of_phrases
        json_data["used_phonemes"] = list_of_used_phonemes
        file_path = open(path, "w")
        json.dump(json_data, file_path, indent=True)
        file_path.close()

    ###

    def __str__(self):
        if self.is_root:
            out_string = "LipSync{}:{}|{}|start_frame:{}|end_frame:{}|Children:{}".format(
                self.object_type.capitalize(),
                self.name, self.text,
                self.start_frame,
                self.end_frame, self.children)
        else:
            out_string = "LipSync{}:{}|{}|start_frame:{}|end_frame:{}|Parent:{}|Children:{}".format(
                self.object_type.capitalize(),
                self.name, self.text,
                self.start_frame,
                self.end_frame, self.parent.name or self.parent.text, self.children)
        return out_string

    def __repr__(self):
        return self.__str__()


class LipsyncDoc:
    def __init__(self, langman: LanguageManager, parent):
        self._dirty = False
        ini_path = os.path.join(utilities.get_app_data_path(), "settings.ini")
        self.settings = QtCore.QSettings(ini_path, QtCore.QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)  # File only, not registry or or.
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
        self.project_node = LipSyncObject(name=self.name, object_type="project")

    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, value):
        self._dirty = value

    def __del__(self):
        # Properly close down the sound object
        if self.sound is not None:
            del self.sound

    def open_json(self, path):
        self._dirty = False
        self.path = os.path.normpath(path)
        self.name = os.path.basename(path)
        self.project_node.name = self.name
        self.sound = None
        self.voices = []
        self.current_voice = None
        file_data = open(self.path, "r")
        json_data = json.load(file_data)
        self.soundPath = json_data.get("sound_path", "")
        if not os.path.isabs(self.soundPath):
            self.soundPath = os.path.normpath("{}/{}".format(os.path.dirname(self.path), self.soundPath))
        self.fps = json_data["fps"]
        self.soundDuration = json_data["sound_duration"]
        self.project_node.sound_duration = self.soundDuration
        self.parent.phonemeset.selected_set = json_data.get("phoneme_set", "preston_blair")
        num_voices = json_data["num_voices"]
        for voice in json_data["voices"]:
            temp_voice = LipSyncObject(name=voice["name"], text=voice["text"], num_children=voice["num_children"],
                                       fps=self.fps, parent=self.project_node, object_type="voice",
                                       sound_duration=self.soundDuration)
            for phrase in voice["phrases"]:
                temp_phrase = LipSyncObject(text=phrase["text"], start_frame=phrase["start_frame"],
                                            end_frame=phrase["end_frame"], tags=phrase["tags"], fps=self.fps,
                                            object_type="phrase", parent=temp_voice, sound_duration=self.soundDuration)
                for word in phrase["words"]:
                    temp_word = LipSyncObject(text=word["text"], start_frame=word["start_frame"], fps=self.fps,
                                              end_frame=word["end_frame"], tags=word["tags"], object_type="word",
                                              parent=temp_phrase, sound_duration=self.soundDuration)
                    for phoneme in word["phonemes"]:
                        temp_phoneme = LipSyncObject(text=phoneme["text"], start_frame=phoneme["frame"],
                                                     end_frame=phoneme["frame"], tags=phoneme["tags"], fps=self.fps,
                                                     object_type="phoneme", parent=temp_word,
                                                     sound_duration=self.soundDuration)
            self.voices.append(temp_voice)
        file_data.close()
        self.open_audio(self.soundPath)
        if len(self.voices) > 0:
            self.current_voice = self.voices[0]

    def open(self, path):
        self._dirty = False
        self.path = os.path.normpath(path)
        self.name = os.path.basename(path)
        self.project_node.name = self.name
        self.sound = None
        self.voices = []
        self.current_voice = None
        in_file = open(self.path, 'r')
        in_file.readline()  # discard the header
        self.soundPath = in_file.readline().strip()
        if not os.path.isabs(self.soundPath):
            self.soundPath = os.path.normpath("{}/{}".format(os.path.dirname(self.path), self.soundPath))
        self.fps = int(in_file.readline())
        print(("self.path: {}".format(self.path)))
        self.soundDuration = int(in_file.readline())
        print(("self.soundDuration: {:d}".format(self.soundDuration)))
        self.project_node.sound_duration = self.soundDuration
        num_voices = int(in_file.readline())
        for i in range(num_voices):
            voice = LipSyncObject(object_type="voice", parent=self.project_node)
            voice.open(in_file)
            self.voices.append(voice)
        in_file.close()
        self.open_audio(self.soundPath)
        if len(self.voices) > 0:
            self.current_voice = self.voices[0]

    def open_audio(self, path):
        if not os.path.exists(path):
            return
        if self.sound is not None:
            del self.sound
            self.sound = None
        # self.soundPath = str(path.encode("utf-8"))
        self.soundPath = path  # .encode('latin-1', 'replace')
        self.sound = SoundPlayer.SoundPlayer(self.soundPath, self.parent)
        if self.sound.IsValid():
            print("valid sound")
            self.soundDuration = int(self.sound.Duration() * self.fps)
            print(("self.sound.Duration(): {:d}".format(int(self.sound.Duration()))))
            print(("frameRate: {:d}".format(int(self.fps))))
            print(("soundDuration1: {:d}".format(self.soundDuration)))
            if self.soundDuration < self.sound.Duration() * self.fps:
                self.soundDuration += 1
                print(("soundDuration2: {:d}".format(self.soundDuration)))
            self.project_node.sound_duration = self.soundDuration
        else:
            self.sound = None

    def open_from_dict(self, json_data):
        self._dirty = False
        # self.path = os.path.normpath(path)
        # self.name = os.path.basename(path)
        self.project_node.name = "Test_Copy"
        self.project_node.children = []
        self.sound = None
        self.voices = []
        self.current_voice = None
        self.soundPath = json_data.get("sound_path", "")
        if not os.path.isabs(self.soundPath):
            self.soundPath = os.path.normpath("{}/{}".format(os.path.dirname(self.path), self.soundPath))
        self.fps = json_data["fps"]
        self.soundDuration = json_data["sound_duration"]
        self.project_node.sound_duration = self.soundDuration
        self.parent.phonemeset.selected_set = json_data.get("phoneme_set", "preston_blair")
        num_voices = json_data["num_voices"]
        for voice in json_data["voices"]:
            temp_voice = LipSyncObject(name=voice["name"], text=voice["text"], num_children=voice["num_children"],
                                       fps=self.fps, parent=self.project_node, object_type="voice",
                                       sound_duration=self.soundDuration)
            for phrase in voice["phrases"]:
                temp_phrase = LipSyncObject(text=phrase["text"], start_frame=phrase["start_frame"],
                                            end_frame=phrase["end_frame"], tags=phrase["tags"], fps=self.fps,
                                            object_type="phrase", parent=temp_voice, sound_duration=self.soundDuration)
                for word in phrase["words"]:
                    temp_word = LipSyncObject(text=word["text"], start_frame=word["start_frame"], fps=self.fps,
                                              end_frame=word["end_frame"], tags=word["tags"], object_type="word",
                                              parent=temp_phrase, sound_duration=self.soundDuration)
                    for phoneme in word["phonemes"]:
                        temp_phoneme = LipSyncObject(text=phoneme["text"], start_frame=phoneme["frame"],
                                                     end_frame=phoneme["frame"], tags=phoneme["tags"], fps=self.fps,
                                                     object_type="phoneme", parent=temp_word,
                                                     sound_duration=self.soundDuration)
            self.voices.append(temp_voice)
        # file_data.close()
        self.open_audio(self.soundPath)
        if len(self.voices) > 0:
            self.current_voice = self.voices[0]

    def copy_to_dict(self, saved_sound_path=""):
        if not saved_sound_path:
            saved_sound_path = self.soundPath
        out_dict = {"version": 2, "sound_path": saved_sound_path, "fps": self.fps,
                    "sound_duration": self.soundDuration,
                    "num_voices": len(self.project_node.children),
                    "phoneme_set": self.parent.phonemeset.selected_set}
        list_of_voices = []
        for voi_id, voice in enumerate(self.project_node.children):
            start_frame = 0
            end_frame = 1
            if len(voice.children) > 0:
                start_frame = voice.children[0].start_frame
                end_frame = voice.children[-1].end_frame
            json_data = {"name": voice.name, "start_frame": start_frame, "end_frame": end_frame,
                         "text": voice.text, "num_children": len(voice.descendants)}
            list_of_phrases = []
            list_of_used_phonemes = []
            for phr_id, phrase in enumerate(voice.children):
                dict_phrase = {"id": phr_id, "text": phrase.text, "start_frame": phrase.start_frame,
                               "end_frame": phrase.end_frame, "tags": phrase.tags}
                list_of_words = []
                for wor_id, word in enumerate(phrase.children):
                    dict_word = {"id": wor_id, "text": word.text, "start_frame": word.start_frame,
                                 "end_frame": word.end_frame, "tags": word.tags}
                    list_of_phonemes = []
                    for pho_id, phoneme in enumerate(word.children):
                        dict_phoneme = {"id": pho_id, "text": phoneme.text,
                                        "frame": phoneme.start_frame, "tags": phoneme.tags}
                        list_of_phonemes.append(dict_phoneme)
                        if phoneme.text not in list_of_used_phonemes:
                            list_of_used_phonemes.append(phoneme.text)
                    dict_word["phonemes"] = list_of_phonemes
                    list_of_words.append(dict_word)
                dict_phrase["words"] = list_of_words
                list_of_phrases.append(dict_phrase)
            json_data["phrases"] = list_of_phrases
            json_data["used_phonemes"] = list_of_used_phonemes
            list_of_voices.append(json_data)
        out_dict["voices"] = list_of_voices
        return out_dict

    def save2(self, path):
        self.path = os.path.normpath(path)
        self.name = os.path.basename(path)
        self.project_node.name = self.name
        if os.path.dirname(self.path) == os.path.dirname(self.soundPath):
            saved_sound_path = os.path.basename(self.soundPath)
        else:
            saved_sound_path = self.soundPath
        out_json = self.copy_to_dict(saved_sound_path)
        file_path = open(self.path, "w")
        json.dump(out_json, file_path, indent=True)
        file_path.close()

    def save(self, path):
        self.path = os.path.normpath(path)
        self.name = os.path.basename(path)
        self.project_node.name = self.name
        if os.path.dirname(self.path) == os.path.dirname(self.soundPath):
            saved_sound_path = os.path.basename(self.soundPath)
        else:
            saved_sound_path = self.soundPath
        out_file = open(self.path, "w")
        out_file.write("lipsync version 1\n")
        out_file.write("{}\n".format(saved_sound_path))
        out_file.write("{:d}\n".format(self.fps))
        out_file.write("{:d}\n".format(self.soundDuration))
        out_file.write("{:d}\n".format(len(self.project_node.children)))
        for voice in self.project_node.children:
            voice.save(out_file)
        out_file.close()
        self._dirty = False

    def convert_to_phonemeset_old(self):
        # The base set is the CMU39 set, we will convert everything to that and from it to the desired one for now
        new_set = self.parent.main_window.phoneme_set.currentText()
        old_set = self.parent.phonemeset.selected_set
        if old_set != new_set:
            if old_set != "CMU_39":
                conversion_map_to_cmu = {v: k for k, v in self.parent.phonemeset.conversion.items()}
                for voice in self.project_node.children:
                    for phrase in voice.children:
                        for word in phrase.children:
                            for phoneme in word.children:
                                phoneme.text = conversion_map_to_cmu.get(phoneme.text, "rest")
            new_map = PhonemeSet()
            new_map.load(new_set)
            conversion_map_from_cmu = new_map.conversion
            for voice in self.project_node.children:
                for phrase in voice.children:
                    for word in phrase.children:
                        for phoneme in word.children:
                            phoneme.text = conversion_map_from_cmu.get(phoneme.text, "rest")
            self.dirty = True
            self.parent.phonemeset.selected_set = new_set
            self.parent.main_window.waveform_view.set_document(self, force=True, clear_scene=True)

    def convert_to_phonemeset(self):
        # The base set is the CMU39 set, we will convert everything to that and from it to the desired one for now
        new_set = self.parent.main_window.phoneme_set.currentText()
        old_set = self.parent.phonemeset.selected_set
        conversion_dict = {}
        if old_set != new_set:
            new_map = PhonemeSet()
            new_map.load(new_set)
            for conversion_name in new_map.alternate_conversions:
                if conversion_name.startswith(old_set.lower()):
                    print(conversion_name)
                    conversion_dict = new_map.alternate_conversions[conversion_name]
            if conversion_dict:
                print(conversion_dict)
                for voice in self.project_node.children:
                    for phrase in voice.children:
                        for word in phrase.children:
                            for phoneme in word.children:
                                phoneme.text = conversion_dict.get(phoneme.text, "rest")
                self.dirty = True
                self.parent.phonemeset.selected_set = new_set
                self.parent.main_window.waveform_view.set_document(self, force=True, clear_scene=True)
            # if old_set != "CMU_39":
            #     conversion_map_to_cmu = {v: k for k, v in self.parent.phonemeset.conversion.items()}
            #     for voice in self.project_node.children:
            #         for phrase in voice.children:
            #             for word in phrase.children:
            #                 for phoneme in word.children:
            #                     phoneme.text = conversion_map_to_cmu.get(phoneme.text, "rest")
            # new_map = PhonemeSet()
            # new_map.load(new_set)
            # conversion_map_from_cmu = new_map.conversion
            # for voice in self.project_node.children:
            #     for phrase in voice.children:
            #         for word in phrase.children:
            #             for phoneme in word.children:
            #                 phoneme.text = conversion_map_from_cmu.get(phoneme.text, "rest")
            # self.dirty = True
            # self.parent.phonemeset.selected_set = new_set
            # self.parent.main_window.waveform_view.set_document(self, force=True, clear_scene=True)

    def auto_recognize_phoneme(self, manual_invoke=False):
        if self.settings.value("/VoiceRecognition/run_voice_recognition", "true").lower() == "true" or manual_invoke:
            if auto_recognition:
                if self.settings.value("/VoiceRecognition/recognizer", "Allosaurus") == "Allosaurus":
                    allo_recognizer = auto_recognition.AutoRecognize(self.soundPath)
                    results, peaks, allo_output = allo_recognizer.recognize_allosaurus()
                    if results:
                        phonemes_as_text = ""
                        end_frame = math.floor(self.fps * (results[-1]["start"] + results[-1]["duration"] * 2))
                        phrase = LipSyncObject(object_type="phrase", parent=self.current_voice)
                        phrase.text = 'Auto detection Allosaurus'
                        phrase.start_frame = 0
                        phrase.end_frame = end_frame
                        for i in range(len(peaks) - 1):
                            peak_left = peaks[i]
                            peak_right = peaks[i + 1]

                            word_chunk = results[peak_left:peak_right]
                            word = LipSyncObject(object_type="word", parent=phrase)

                            word.text = "|".join(
                                letter["phoneme"] if letter["phoneme"] is not None else "rest" for letter in word_chunk)
                            word.start_frame = math.floor(self.fps * results[peak_left]["start"])
                            # word.end_frame = math.floor(self.fps * results[peak_right]["start"])
                            previous_frame_pos = math.floor(self.fps * results[peak_left]["start"]) - 1
                            for phoneme in word_chunk:
                                current_frame_pos = math.floor(self.fps * phoneme['start'])
                                if current_frame_pos == previous_frame_pos:
                                    current_frame_pos += 1
                                pg_phoneme = LipSyncObject(object_type="phoneme", parent=word)
                                pg_phoneme.start_frame = pg_phoneme.end_frame = current_frame_pos
                                previous_frame_pos = current_frame_pos
                                pg_phoneme.text = phoneme['phoneme'] if phoneme['phoneme'] is not None else 'rest'
                                # word.phonemes.append(pg_phoneme)
                                phonemes_as_text += pg_phoneme.text
                            phonemes_as_text += " "
                            word.end_frame = previous_frame_pos + 1
                            # phrase.words.append(word)
                        phonemes_as_text += "\n{}".format(str(allo_output))
                        try:
                            self.parent.main_window.text_edit.setText(phonemes_as_text)
                        except AttributeError:
                            pass
                        phrase.end_frame = phrase.children[-1].end_frame
                        # self.current_voice.phrases.append(phrase)
                        self.parent.phonemeset.selected_set = self.parent.phonemeset.load("CMU_39")
                        try:
                            current_index = self.parent.main_window.phoneme_set.findText(self.parent.phonemeset.selected_set)
                            self.parent.main_window.phoneme_set.setCurrentIndex(current_index)
                        except AttributeError:
                            pass
                elif self.settings.value("/VoiceRecognition/recognizer", "Allosaurus") == "Rhubarb":
                    try:
                        phonemes = Rhubarb(self.soundPath).run()
                        if not phonemes:
                            return
                        end_frame = math.floor(self.fps * phonemes[-1]['end'])
                        phrase = LipSyncObject(object_type="phrase", parent=self.current_voice)
                        phrase.text = 'Auto detection rhubarb'
                        phrase.start_frame = 0
                        phrase.end_frame = end_frame

                        word = LipSyncObject(object_type="word", parent=phrase)
                        word.text = 'rhubarb'
                        word.start_frame = 0
                        word.end_frame = end_frame

                        for phoneme in phonemes:
                            pg_phoneme = LipSyncObject(object_type="phoneme", parent=word)
                            pg_phoneme.start_frame = pg_phoneme.end_frame = math.floor(self.fps * phoneme['start'])
                            pg_phoneme.text = phoneme['value'] if phoneme['value'] != 'X' else 'rest'
                            # word.phonemes.append(pg_phoneme)

                        # phrase.words.append(word)
                        # self.current_voice.phrases.append(phrase)
                        self.parent.phonemeset.selected_set = self.parent.phonemeset.load("rhubarb")
                        current_index = self.parent.main_window.phoneme_set.findText(
                            self.parent.phonemeset.selected_set)
                        self.parent.main_window.phoneme_set.setCurrentIndex(current_index)

                    except RhubarbTimeoutException:
                        pass

    def __str__(self):
        out_string = "LipSyncDoc:{}|Objects:{}|Sound:{}|".format(self.name, self.project_node, self.soundPath)
        return out_string

    def __repr__(self):
        return self.__str__()


class PhonemeSet:
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        self.set = []
        self.conversion = {}
        self.alternatives = []
        self.alternate_conversions = {}
        for file in os.listdir(os.path.join(utilities.get_main_dir(), "phonemes")):
            if fnmatch.fnmatch(file, '*.json'):
                self.alternatives.append(file.split(".")[0])

        # Try to load Preston Blair as default as before, but fall back just in case
        self.selected_set = self.load("preston_blair")
        if not self.selected_set:
            self.load(self.alternatives[0])
            self.selected_set = self.alternatives[0]

    def load(self, name=''):
        if name in self.alternatives:
            with open(os.path.join(utilities.get_main_dir(), "./phonemes/{}.json".format(name)), "r") as loaded_file:
                json_data = json.load(loaded_file)
                self.set = json_data["phoneme_set"]
                if name.lower() != "cmu_39":
                    self.conversion = json_data.get("cmu_39_phoneme_conversion")
                else:
                    for phoneme in self.set:
                        self.conversion[phoneme] = phoneme
                for key in json_data:
                    if key != "phoneme_set":
                        self.alternate_conversions[key] = json_data[key]
                return name
        else:
            print(("Can't find phonemeset! ({})".format(name)))
            return False
