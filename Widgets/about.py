# -*- coding: utf-8 -*-
from QtBase.basewidget import *
from Ui.about_ui import *
import webbrowser


class About(BaseWidget, Ui_About):
    '''关于界面'''

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

    @pyqtSlot(bool)
    def on_pb_openurl1_clicked(self, _):
        webbrowser.open("https://bmclapidoc.bangbang93.com/")
