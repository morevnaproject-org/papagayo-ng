#--coding: utf-8 --

import sys
import LipsyncFrameQT
import papagayongrcc


if __name__ == "__main__":
    papagayo_window = LipsyncFrameQT.LipsyncFrame()
    papagayo_window.main_window.show()
    sys.exit(papagayo_window.app.exec_())
