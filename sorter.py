#! python.exe
# -*- coding: utf-8 -*-

"""
Description: Main program file

"""

# => IMPORTS
import sys

# => LIB IMPORTS
from lib import func
from lib import notification as ntf
from lib import system_tray as st

# => 3-RD PARTY MODULES
from PySide2 import QtWidgets, QtGui

ICON_PATH = 'res/move.png'


# => MAIN FUNCTION
def main():
    # => SETUP
    func.setup()

    # => CREATE QT APP
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    tray_icon = st.SystemTrayIcon(QtGui.QIcon(ICON_PATH), w)
    tray_icon.show()

    # => GUI
    func.start()

    data = func.get_config()

    # => IF NOT SET
    if not bool(int(data[' GLOBAL ']['set'])):

        # => SETUP ALL - UNPACK DATA
        prefixes, paths = func.set_all()

        # => SEND ALL DATA
        func.set_sorting_sections(prefixes)
        func.set_sorting_paths(paths)

    else:
        func.help_msg()

    func.create_prefixes_txt()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
