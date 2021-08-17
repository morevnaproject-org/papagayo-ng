import json
import os
import sys
from functools import partial

from PySide2.QtCore import Qt, QSize, SIGNAL
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtWidgets import QWidget, QApplication, QGridLayout, QLabel, QScrollArea, QMainWindow, QCheckBox, \
    QComboBox, QFrame, QPushButton

import utilities

widget_size = [100, 100]


class PhonemeHelper(QMainWindow):
    def __init__(self):
        super(PhonemeHelper, self).__init__()
        self.image_grid = QGridLayout()
        self.scroll_area = QScrollArea(self)
        self.scroll_view = QWidget(self)

        self.set = []
        self.conversion = {}
        self.image_dir = os.path.join(utilities.get_main_dir(), "rsrc", "mouths", r"9 - Hunanbean @ 100% (CMU39)")
        self.rhubarb_dir = os.path.join(utilities.get_main_dir(), "rsrc", "mouths", r"8 - Rhubarb")
        self.load_phoneme_data()
        self.list_of_cmu_image_labels = []
        self.list_of_rhubarb_labels = []
        self.rhubarb_dict = {}
        #self.list_of_cmu_image_labels.append("")  # Empty Item at the beginning
        self.list_of_cmu_texts = []
        self.list_of_rhubarb_texts = []
        for key, value in self.conversion.items():
            image_path = os.path.join(self.image_dir, "{}.png".format(key))
            if os.path.exists(image_path):
                self.list_of_cmu_texts.append(key)
                lbl = QLabel()
                label_text = f"<html><img src='{image_path}' width={widget_size[0]} height={widget_size[1]}></html><br><center> Phoneme:'{key}'</center>"
                #lbl.setFrameShape(QFrame.Panel)
                #lbl.setLineWidth(1)
                lbl.setText(label_text)
                lbl.setScaledContents(True)
                #lbl.setMinimumSize(*widget_size)
                lbl.setMaximumSize(widget_size[0], widget_size[1] + 50)
                self.list_of_cmu_image_labels.append(lbl)
        #self.list_of_rhubarb_labels.append("")  # Empty Item at the beginning
        for key in self.set:
            image_path = os.path.join(self.rhubarb_dir, "{}.png".format(key))
            if os.path.exists(image_path):
                self.list_of_rhubarb_texts.append(key)
                pixmap = QPixmap(image_path)
                r_icon = QIcon()
                r_icon.addPixmap(pixmap)
                lbl = QLabel()
                label_text = f"<html><img src='{image_path}' width={widget_size[0]} height={widget_size[1]}></html><br><center>{key}</center>"
                lbl.setText(label_text)
                lbl.setMinimumSize(*widget_size)

                self.list_of_rhubarb_labels.append(r_icon)
        num_columns = len(self.list_of_rhubarb_labels)
        num_rows = len(self.list_of_cmu_image_labels)

        self.list_of_widgets = []
        for row, lbl in enumerate(self.list_of_cmu_image_labels):
            self.image_grid.addWidget(lbl, row, 0, alignment=Qt.AlignCenter)
            combobox = QComboBox()
            for r_label in self.list_of_rhubarb_labels:
                combobox.addItem(r_label, "")
            combobox.setIconSize(QSize(*widget_size))
            combobox.setMinimumSize(widget_size[0], lbl.height())
            combobox.currentIndexChanged.connect(partial(self.get_phoneme_widgets, combobox))
            #self.connect(combobox, SIGNAL("currentIndexChanged()"), partial(self.get_phoneme_widgets, "changed"))
            self.image_grid.addWidget(combobox, row, 1, alignment=Qt.AlignCenter)
            cmu_phoneme = lbl.text().split("Phoneme:")[1].split("</center>")[0].strip("'")
            self.rhubarb_dict[combobox] = cmu_phoneme
            self.list_of_widgets.append((lbl, combobox))

        self.scroll_area.setMinimumSize((widget_size[0] * 2) + self.scroll_area.verticalScrollBar().width(), 800)
        self.scroll_view = QWidget(self)
        self.scroll_view.setLayout(self.image_grid)
        self.scroll_area.setWidget(self.scroll_view)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        self.image_grid.addWidget(self.save_button)

        self.setCentralWidget(self.scroll_area)

    def save_settings(self):
        conversion_dict = {}
        export_json = {}
        for c_box in self.scroll_view.children():
            if isinstance(c_box, QComboBox):
                cmu_phoneme = self.rhubarb_dict[c_box]
                rhubarb_phoneme = self.set[c_box.currentIndex()]
                conversion_dict[cmu_phoneme] = rhubarb_phoneme
        export_json["phoneme_set" ] = self.set
        export_json["phoneme_conversion"] = conversion_dict
        out_file_path = os.path.join(utilities.get_main_dir(), "phonemes", "test_set.json")
        out_file = open(out_file_path, "w")
        json.dump(export_json, out_file, indent=True)
        out_file.close()

    def load_phoneme_data(self):
        with open(os.path.join(utilities.get_main_dir(), "./phonemes/rhubarb.json"), "r") as loaded_file:
            json_data = json.load(loaded_file)
            self.set = json_data["phoneme_set"]
            self.conversion = json_data["phoneme_conversion"]

    def set_phoneme_widgets(self):
        for c_box in self.scroll_view.children():
            if isinstance(c_box, QComboBox):
                cmu_phoneme = self.rhubarb_dict[c_box]
                try:
                    rhubarb_index = self.set.index(self.conversion.get(cmu_phoneme, "rest"))
                except ValueError:
                    rhubarb_index = self.set.index("rest")
                c_box.setCurrentIndex(rhubarb_index)

    def get_phoneme_widgets(self, event=None, blubb=None):
        print("Selected")
        print(event)
        selected_phoneme = self.set[event.currentIndex()]
        print(selected_phoneme)
        cmu_phoneme = self.rhubarb_dict[event]
        print(f"CMU: {cmu_phoneme} changed to Rhubarb: {selected_phoneme}")
        #for c_box in self.scroll_view.children():
        #    if isinstance(c_box, QComboBox):
        #        selected_phoneme = self.set[c_box.currentIndex()]
        #        print(selected_phoneme)

    def show_and_raise(self):
        self.show()
        self.raise_()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    phoneme_helper = PhonemeHelper()
    phoneme_helper.show_and_raise()
    phoneme_helper.set_phoneme_widgets()

    sys.exit(app.exec_())
