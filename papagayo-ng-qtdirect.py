#--coding: utf-8 --

from PySide import QtCore, QtGui, QtUiTools
import sys
import papagayongrcc


class MainWindow:
    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        self.main_window = self.load_ui_widget("./rsrc/papagayo-ng2.ui")

        self.loader = None
        self.ui_file = None
        self.ui = None

        # This adds our statuses to the statusbar
        self.mainframe_statusbar_fields = ["Papagayo-NG", "Stopped"]
        self.play_status = QtGui.QLabel()
        self.play_status.setText(self.mainframe_statusbar_fields[1])
        # An empty Label to add a separator
        self.sep_status = QtGui.QLabel()
        self.sep_status.setText(u"")
        self.main_window.statusbar.addPermanentWidget(self.sep_status)
        self.main_window.statusbar.addPermanentWidget(self.play_status)
        self.main_window.statusbar.showMessage(self.mainframe_statusbar_fields[0])
        # Connect Events
        self.main_window.action_play.triggered.connect(self.test_button_event)
        self.main_window.action_exit.triggered.connect(self.quit_application)

    def load_ui_widget(self, ui_filename, parent=None):
        self.loader = QtUiTools.QUiLoader()
        self.ui_file = QtCore.QFile(ui_filename)
        self.ui_file.open(QtCore.QFile.ReadOnly)
        self.ui = self.loader.load(self.ui_file, parent)
        self.ui_file.close()
        return self.ui

    def test_button_event(self):
        self.play_status.setText("Running")

    def quit_application(self):
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    papagayo_window = MainWindow()
    papagayo_window.main_window.show()
    sys.exit(papagayo_window.app.exec_())
