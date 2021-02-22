# -*- coding: utf-8 -*-

"""
Description: system tray window

"""

# => 3-RD PARTY IMPORTS:
from PySide2 import QtWidgets, QtGui

# => IMPORTS
from lib import func
from lib import notification as ntf


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip(f'Project Sorter 1.0.0')

        # => SET MENU
        menu = QtWidgets.QMenu(parent)

        sort = menu.addAction('Sort projects')
        exit_p = menu.addAction('Exit')
        edit = menu.addAction('Edit')

        sort.triggered.connect(self.sort_projects)
        exit_p.triggered.connect(self.exit_program)
        edit.triggered.connect(self.edit)

        self.setContextMenu(menu)
        self.activated.connect(self.onTrayIconActivated)

        self.toaster = ntf.Notification()

    def onTrayIconActivated(self, reason):
        pass

    @staticmethod
    def exit_program():
        exit()

    @staticmethod
    def edit():

        # => EDIT THE PREFIXES OR PATHS
        # => GUI
        func.start()

        data = func.get_config()

        # => SETUP ALL - UNPACK DATA
        prefixes, paths = func.set_all()

        # => SEND ALL DATA
        func.set_sorting_sections(prefixes)
        func.set_sorting_paths(paths)

        func.create_prefixes_txt()

    def sort_projects(self):
        projects = func.get_dir_names()

        COUNT = 0
        ALL = len(projects)

        if len(projects) != 0:
            result = func.sort_projects_name(projects)

            for project in result:
                COUNT += func.move_project(project[1], project[0])

            # => SHOW NOTIFICATION
            self.toaster.show_notification(
                title=f"{COUNT} Projects Moved\n",
                description=f"{COUNT} of {ALL} projects has been moved to their correct directories",
                duration=6
            )
