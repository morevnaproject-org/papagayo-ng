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

from qtpy import QtCore, QtWidgets
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
        self.phoneme_ctrl = QtWidgets.QLineEdit()

        self.gave_ok = False
        self.curr_x = 0
        self.curr_y = 0
        self.max_x = round(sqrt(len(phoneme_set)))  # This way the grid should always be as square as possible

        self.box.addWidget(self.word_label)
        self.box.addLayout(self.phoneme_grid)
        self.box.addWidget(self.phoneme_ctrl)
        self.box.addWidget(self.decide_box)

        phoneme_ids = {}
        self.phoneme_buttons = {}

        for phoneme in phoneme_set:
            print(phoneme)
            if phoneme != "rest":
                phoneme_ids[phoneme] = QtWidgets.QPushButton(phoneme, self)
                phoneme_ids[phoneme].clicked.connect(self.on_phoneme_click)
                self.phoneme_grid.addWidget(phoneme_ids[phoneme], self.curr_y, self.curr_x)
                self.curr_x += 1
                if self.curr_x >= self.max_x:
                    self.curr_x = 0
                    self.curr_y += 1

        self.decide_box.accepted.connect(self.on_accept)
        self.decide_box.rejected.connect(self.on_reject)

        self.setLayout(self.box)
        self.setModal(True)
        self.show()

    def add_phoneme(self, phoneme):
        text = "%s %s" % (self.phoneme_ctrl.text().strip(), phoneme)
        self.phoneme_ctrl.setText(text.strip())

    def on_phoneme_click(self, event=None):
        print(self.sender().text())
        phoneme = self.sender().text()
        text = "%s %s" % (self.phoneme_ctrl.text().strip(), phoneme)
        self.phoneme_ctrl.setText(text.strip())

    def on_accept(self):
        self.gave_ok = True
        self.close()

    def on_reject(self):
        self.gave_ok = False
        self.close()

# end of class PronunciationDialog
