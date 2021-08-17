import json
import os
import sys

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QApplication, QGridLayout, QLabel, QScrollArea, QMainWindow, QCheckBox

import utilities

widget_size = [100, 100]


class PhonemeHelper(QMainWindow):
    def __init__(self):
        super(PhonemeHelper, self).__init__()
        self.image_grid = QGridLayout()
        self.scroll_area = QScrollArea(self)
        self.scroll_view = QWidget(self)

        self.set = {}
        self.conversion = {}
        self.image_dir = os.path.join(utilities.get_main_dir(), "rsrc", "mouths", r"9 - Hunanbean @ 100% (CMU39)")
        self.rhubarb_dir = os.path.join(utilities.get_main_dir(), "rsrc", "mouths", r"8 - Rhubarb")
        self.load_phoneme_data()
        self.list_of_cmu_image_labels = []
        self.list_of_rhubarb_labels = []
        self.list_of_cmu_image_labels.append("")  # Empty Item at the beginning
        self.list_of_cmu_texts = []
        self.list_of_rhubarb_texts = []
        for key, value in self.conversion.items():
            image_path = os.path.join(self.image_dir, "{}.png".format(key))
            if os.path.exists(image_path):
                self.list_of_cmu_texts.append(key)
                lbl = QLabel()
                label_text = f"<html><img src='{image_path}' width={widget_size[0]} height={widget_size[1]}></html><br><center>{key}</center>"
                lbl.setText(label_text)
                lbl.setMinimumSize(*widget_size)
                self.list_of_cmu_image_labels.append(lbl)
        self.list_of_rhubarb_labels.append("")  # Empty Item at the beginning
        for key in self.set:
            image_path = os.path.join(self.rhubarb_dir, "{}.png".format(key))
            if os.path.exists(image_path):
                self.list_of_rhubarb_texts.append(key)
                lbl = QLabel()
                label_text = f"<html><img src='{image_path}' width={widget_size[0]} height={widget_size[1]}></html><br><center>{key}</center>"
                lbl.setText(label_text)
                lbl.setMinimumSize(*widget_size)
                self.list_of_rhubarb_labels.append(lbl)
        num_columns = len(self.list_of_rhubarb_labels)
        num_rows = len(self.list_of_cmu_image_labels)

        self.list_of_widgets = []
        for row in range(num_rows):
            for column in range(num_columns):
                temp_widget = None
                if row == 0 and column != 0:
                    temp_widget = self.image_grid.addWidget(self.list_of_rhubarb_labels[column], row, column,
                                                            alignment=Qt.AlignCenter)
                elif column == 0 and row != 0:
                    temp_widget = self.image_grid.addWidget(self.list_of_cmu_image_labels[row], row, column,
                                                            alignment=Qt.AlignCenter)

                elif column != 0 and row != 0:
                    checkbox_label = "{}|{}".format(self.list_of_rhubarb_texts[column - 1],
                                                    self.list_of_cmu_texts[row - 1])
                    new_checkbox = QCheckBox(checkbox_label)
                    new_checkbox.setMinimumSize(*widget_size)
                    temp_widget = self.image_grid.addWidget(new_checkbox, row, column, alignment=Qt.AlignCenter)
                self.list_of_widgets.append(temp_widget)
                print("row:{} - column:{}".format(row, column))
                print(self.image_grid.itemAtPosition(row, column))
        self.scroll_area.setMinimumSize((widget_size[0] * (num_columns)) + self.scroll_area.verticalScrollBar().width(),
                                        800)
        self.scroll_view = QWidget(self)
        self.scroll_view.setLayout(self.image_grid)
        self.scroll_area.setWidget(self.scroll_view)

        self.setCentralWidget(self.scroll_area)

    def load_phoneme_data(self):
        with open(os.path.join(utilities.get_main_dir(), "./phonemes/rhubarb.json"), "r") as loaded_file:
            json_data = json.load(loaded_file)
            self.set = json_data["phoneme_set"]
            self.conversion = json_data["phoneme_conversion"]

    def show_and_raise(self):
        self.show()
        self.raise_()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    phoneme_helper = PhonemeHelper()
    phoneme_helper.show_and_raise()

    sys.exit(app.exec_())
