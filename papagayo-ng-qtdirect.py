from PySide import QtCore, QtGui, QtUiTools
import papagayongrcc


def loadUiWidget(uifilename, parent=None):
    loader = QtUiTools.QUiLoader()
    uifile = QtCore.QFile(uifilename)
    uifile.open(QtCore.QFile.ReadOnly)
    ui = loader.load(uifile, parent)
    uifile.close()
    return ui


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = loadUiWidget("./rsrc/papagayo-ng2.ui")
    MainWindow.show()
    sys.exit(app.exec_())