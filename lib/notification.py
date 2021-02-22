# -*- coding: utf-8 -*-

"""
Description: windows notification file

"""

# => IMPORTS
from win10toast import ToastNotifier


class Notification(object):
    def __init__(self):
        self.toaster = ToastNotifier()
        self.icon_path = './res/move.ico'

    def show_notification(self, title, description, threaded=True, duration=3):

        # => SHOW NOTIFICATION
        self.toaster.show_toast(
            title=title,
            msg=description,
            threaded=threaded,
            icon_path=self.icon_path,
            duration=duration
        )

