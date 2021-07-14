# -*- coding: ISO-8859-1 -*-

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
import os

from PySide2 import QtCore, QtWidgets, QtGui

import utilities
from MouthViewQT import MouthView
from math import sqrt


class PronunciationDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, phoneme_set=None):
        super(PronunciationDialog, self).__init__(None)

        self.setWindowTitle("Unknown Word")
        self.word_label = QtWidgets.QLabel("Break down the word:", self)
        self.word_label.setAlignment(QtCore.Qt.AlignCenter)
        self.box = QtWidgets.QVBoxLayout()
        self.phoneme_grid = QtWidgets.QGridLayout()
        self.decide_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.confirm_button = QtWidgets.QPushButton("OK")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.stop_button = self.decide_box.addButton("Stop", QtWidgets.QDialogButtonBox.RejectRole)

        self.phoneme_ctrl = QtWidgets.QLineEdit()
        self.mouth_view = MouthView()
        for widget in QtWidgets.QApplication.instance().topLevelWidgets():
            if isinstance(widget, QtWidgets.QMainWindow):
                self.main_window = widget
        self.mouth_view.current_mouth = self.main_window.mouth_choice.currentText()
        self.mouth_view.set_document(self.main_window.lip_sync_frame.doc)

        self.gave_ok = False
        self.stop_decode = False
        self.curr_x = 0
        self.curr_y = 0
        self.max_x = round(sqrt(len(phoneme_set)))  # This way the grid should always be as square as possible

        self.box.addWidget(self.word_label)
        self.box.addWidget(self.mouth_view)
        self.box.addLayout(self.phoneme_grid)
        self.box.addWidget(self.phoneme_ctrl)
        self.box.addWidget(self.decide_box)

        phoneme_ids = {}
        self.phoneme_buttons = {}

        for phoneme in phoneme_set:
            if phoneme != "rest":
                self.phoneme_buttons[phoneme] = QtWidgets.QPushButton(phoneme, self)
                self.phoneme_buttons[phoneme].clicked.connect(self.on_phoneme_click)
                self.phoneme_buttons[phoneme].enterEvent = self.hover_phoneme
                self.phoneme_grid.addWidget(self.phoneme_buttons[phoneme], self.curr_y, self.curr_x)
                self.curr_x += 1
                if self.curr_x >= self.max_x:
                    self.curr_x = 0
                    self.curr_y += 1

        self.decide_box.accepted.connect(self.on_accept)
        self.decide_box.rejected.connect(self.on_reject)
        self.stop_button.clicked.connect(self.on_abort)

        self.setLayout(self.box)
        self.setModal(True)
        self.setWindowIcon(QtGui.QIcon(os.path.join(utilities.get_main_dir(), "rsrc", "window_icon.bmp")))
        self.show()

    def hover_phoneme(self, event=None):
        for phoneme in self.phoneme_buttons:
            if self.phoneme_buttons[phoneme].underMouse():
                self.mouth_view.set_phoneme_picture(phoneme)

    def add_phoneme(self, phoneme):
        text = "{} {}".format(self.phoneme_ctrl.text().strip(), phoneme)
        self.phoneme_ctrl.setText(text.strip())

    def on_phoneme_click(self, event=None):
        phoneme = self.sender().text()
        text = "{} {}".format(self.phoneme_ctrl.text().strip(), phoneme)
        self.phoneme_ctrl.setText(text.strip())

    def on_accept(self):
        self.gave_ok = True
        self.accept()
        # self.close()

    def on_reject(self):
        self.gave_ok = False
        self.reject()
        # self.close()

    def on_abort(self):
        self.gave_ok = False
        self.stop_decode = True
        self.reject()

# end of class PronunciationDialog
