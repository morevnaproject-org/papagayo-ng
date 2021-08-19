import json
import os
import shutil
import sys
from functools import partial

from PySide2.QtCore import Qt, QSize, QRect
from PySide2.QtGui import QPixmap, QIcon, QPainter, QFont, QPen
from PySide2.QtWidgets import QWidget, QApplication, QGridLayout, QLabel, QScrollArea, QMainWindow, QComboBox, \
    QPushButton, QDialog, QMessageBox

import utilities

widget_size = [100, 100]


class SelectPhonemeDialog(QDialog):
    def __init__(self, parent=None, phoneme_set=None):
        super(SelectPhonemeDialog, self).__init__(parent)
        self.setWindowTitle("Select the Phonemeset you want to modify.")
        self.lbl = QLabel("Select the Phonemeset you want to modify.")
        self.phoneme_sets = phoneme_set
        self.combobox = QComboBox()
        self.grid = QGridLayout()
        self.grid.addWidget(self.lbl)
        self.grid.addWidget(self.combobox)
        self.setLayout(self.grid)
        self.select_button = QPushButton("Select")
        self.select_button.clicked.connect(self.set_selected)
        self.grid.addWidget(self.select_button)
        self.selection = "CMU_39"
        for key, value in self.phoneme_sets.items():
            self.combobox.addItem(key)
        self.combobox.currentIndexChanged.connect(partial(self.get_selection, self.combobox))

    def get_selection(self, event=None, index=None):
        print(index)
        print(event.currentText())
        self.selection = event.currentText()

    def set_selected(self, event=None):
        self.close()


default_images = {"CMU_39": r"9 - Hunanbean @ 100% (CMU39)", "fleming_dobbs": r"5 - Fleming and Dobbs",
                  "preston_blair": r"4 - Preston Blair", "rhubarb": r"8 - Rhubarb"}
image_types = (".jpg", ".png")


class PhonemeHelper(QMainWindow):
    def __init__(self):
        super(PhonemeHelper, self).__init__()
        self.image_grid = QGridLayout()
        self.scroll_area = QScrollArea(self)
        self.scroll_view = QWidget(self)
        self.phoneme_sets = {}
        self.input_icons = {}
        self.combo_box_dict = {}
        self.get_list_of_phoneme_sets()
        self.current_phoneme_set = {}
        phoneme_selection = SelectPhonemeDialog(phoneme_set=self.phoneme_sets)
        phoneme_selection.setModal(True)
        phoneme_selection.exec_()
        if phoneme_selection.selection:
            self.current_phoneme_set[phoneme_selection.selection] = self.phoneme_sets.pop(phoneme_selection.selection)
        temp_image_set = default_images.get([key for key in self.current_phoneme_set][0], "")
        self.setWindowTitle("Adjust Phonemes for {} Conversions.".format(phoneme_selection.selection))
        if temp_image_set:
            self.input_dir = os.path.join(utilities.get_main_dir(), "rsrc", "mouths", temp_image_set)
        self.output_dirs = []
        self.list_of_output_labels = []
        for p_set in self.phoneme_sets:
            temp_image_set = default_images.get(p_set)
            if temp_image_set:
                temp_path = os.path.join(utilities.get_main_dir(), "rsrc", "mouths", temp_image_set)
                self.output_dirs.append(temp_path)
                output_dict = {"name": p_set, "images": self.create_labels(self.get_images_from_path(temp_path))}
                self.list_of_output_labels.append(output_dict)

        self.input_icons["name"] = [key for key in self.current_phoneme_set][0]
        self.input_icons["images"] = self.create_icons(self.get_images_from_path(self.input_dir))

        self.create_combo_widgets(self.input_icons, self.list_of_output_labels)

        self.set = []
        self.conversion = {}

        self.list_of_cmu_image_labels = []
        self.list_of_rhubarb_labels = []
        self.rhubarb_dict = {}
        self.list_of_cmu_texts = []
        self.list_of_rhubarb_texts = []

        num_columns = len(self.input_icons)
        num_rows = len(self.list_of_cmu_image_labels)
        print(len(self.phoneme_sets))

        self.scroll_area.setMinimumSize(int((widget_size[0] * (len(self.phoneme_sets) * 2)) +
                                        self.scroll_area.verticalScrollBar().width() * 1.6), 800)
        self.scroll_view = QWidget(self)
        self.scroll_view.setLayout(self.image_grid)
        self.scroll_area.setWidget(self.scroll_view)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        self.image_grid.addWidget(self.save_button)

        self.setCentralWidget(self.scroll_area)

    def create_combo_widgets(self, input_data, output_list):
        list_of_widgets = []
        for output_set in output_list:
            output_name = output_set["name"]
            output_data = output_set["images"]
            output_layout = QGridLayout()
            set_label = QLabel(output_name)
            self.image_grid.addWidget(set_label, 0, output_list.index(output_set), Qt.AlignCenter)
            self.image_grid.addLayout(output_layout, 1, output_list.index(output_set), Qt.AlignTop)
            for row, lbl_name in enumerate(output_data):
                lbl = output_data[lbl_name]
                output_layout.addWidget(lbl, row, 0, alignment=Qt.AlignCenter)
                combobox = QComboBox()
                for icon_name in input_data["images"]:
                    icon = input_data["images"][icon_name]
                    combobox.addItem(icon, "")
                combobox.setIconSize(QSize(*widget_size))
                combobox.setMinimumSize(widget_size[0], lbl.height())
                output_layout.addWidget(combobox, row, 1, alignment=Qt.AlignCenter)
                phoneme_label = lbl.text().split("Phoneme:<br>")[1].split("</center>")[0].strip("'")
                output_phoneme_id = f"{output_name}#{phoneme_label}"
                self.combo_box_dict[combobox] = output_phoneme_id

    def create_labels(self, in_path):
        output_labels = {}
        for key in in_path:
            if os.path.exists(in_path[key]):
                lbl = QLabel()
                label_text = f"<html><img src='{in_path[key]}' width={widget_size[0]} height={widget_size[1]}></html><br><center> Phoneme:<br>'{key}'</center>"
                lbl.setText(label_text)
                lbl.setScaledContents(True)
                lbl.setMaximumSize(widget_size[0], widget_size[1] + 50)
                output_labels[key] = lbl
        return output_labels

    def create_icons(self, in_path):
        input_icons = {}
        for key in in_path:
            if os.path.exists(in_path[key]):
                key = os.path.basename(in_path[key]).split(".")[0]
                pixmap = QPixmap(in_path[key])
                # add Text to Picture
                painter = QPainter()
                painter.begin(pixmap)

                painter.setPen(QPen(Qt.white))
                font = QFont("Arial")
                font.setPointSizeF(30)
                font.setBold(True)
                font.setHintingPreference(QFont.PreferNoHinting)
                painter.setFont(font)
                painter.drawText(pixmap.rect(), Qt.AlignHCenter | Qt.AlignBottom, key)

                painter.setPen(QPen(Qt.black))
                font = QFont("Arial")
                font.setPointSizeF(30)
                font.setBold(False)
                font.setHintingPreference(QFont.PreferNoHinting)
                painter.setFont(font)
                painter.drawText(pixmap.rect(), Qt.AlignHCenter | Qt.AlignBottom, key)
                painter.end()

                r_icon = QIcon()
                r_icon.addPixmap(pixmap)
                input_icons[key] = r_icon
        return input_icons

    def get_images_from_path(self, in_path):
        image_dict = {}
        for image in os.listdir(in_path):
            if image.endswith(image_types):
                image_dict[image.split(".")[0]] = os.path.join(in_path, image)
        return image_dict

    def get_list_of_phoneme_sets(self):
        for phoneme_set in os.listdir(os.path.join(utilities.get_main_dir(), "phonemes")):
            if phoneme_set.endswith(".json"):
                with open(os.path.join(utilities.get_main_dir(), "phonemes", phoneme_set), "r") as loaded_file:
                    json_data = json.load(loaded_file)
                    file_name = phoneme_set.split(".")[0]
                    self.phoneme_sets[file_name] = json_data

    def save_settings(self):
        # Move old set to backup
        backup_path = os.path.join(utilities.get_main_dir(), "phonemes", "backup")
        if not os.path.exists(backup_path):
            os.mkdir(backup_path)
        dest_set = list(self.current_phoneme_set.keys())[0]
        old_path = os.path.join(utilities.get_main_dir(), "phonemes", "{}.json".format(dest_set))
        backup_file_path = os.path.join(backup_path, "{}.json".format(dest_set))
        shutil.move(old_path, backup_file_path)
        # Now Save the new file to the old path
        export_json = {}
        for c_box in self.scroll_view.children():
            if isinstance(c_box, QComboBox):
                phoneme_info = self.combo_box_dict[c_box]
                p_set, phoneme = phoneme_info.split("#")
                whish_conversion_name = "{}_phoneme_conversion".format(p_set.lower())
                phoneme_string = self.current_phoneme_set[dest_set]["phoneme_set"][c_box.currentIndex()]
                if whish_conversion_name not in export_json:
                    export_json[whish_conversion_name] = {}
                export_json[whish_conversion_name][phoneme] = phoneme_string

        export_json["phoneme_set"] = self.current_phoneme_set[dest_set]["phoneme_set"]
        out_file_path = os.path.join(utilities.get_main_dir(), "phonemes", "{}.json".format(dest_set))
        out_file = open(out_file_path, "w")
        json.dump(export_json, out_file, indent=True)
        out_file.close()
        save_finished = QMessageBox()
        save_finished.setText("Saving finished.")
        save_finished.setWindowTitle("Saving finished.")
        save_finished.exec_()

    def set_phoneme_widgets(self):
        for c_box in self.scroll_view.children():
            if isinstance(c_box, QComboBox):
                phoneme_info = self.combo_box_dict[c_box]
                p_set, phoneme = phoneme_info.split("#")
                dest_set = list(self.current_phoneme_set.keys())[0]
                whish_conversion_name = "{}_phoneme_conversion".format(p_set.lower())
                if p_set == "CMU_39":
                    whish_conversion_name = "phoneme_conversion"
                whish_conversion = self.current_phoneme_set[dest_set].get(whish_conversion_name, None)
                if whish_conversion:
                    try:
                        c_index = self.current_phoneme_set[dest_set]["phoneme_set"].index(whish_conversion[phoneme])
                    except (ValueError, KeyError):
                        c_index = len(self.current_phoneme_set[dest_set]["phoneme_set"][-1])
                    c_box.setCurrentIndex(c_index)
                else:
                    print("Does not yet exists.")
                    print(whish_conversion_name)

    def show_and_raise(self):
        self.show()
        self.raise_()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    phoneme_helper = PhonemeHelper()
    phoneme_helper.show_and_raise()
    phoneme_helper.set_phoneme_widgets()

    sys.exit(app.exec_())
