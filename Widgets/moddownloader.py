# -*- coding: utf-8 -*-
from Api.mod import Mod
from QtBase.basewidget import *
from Ui.moddownloader_ui import *
from Widgets.moddetail import ModDetail
from Widgets.threadmanager import ThreadManager


class ModDownloader(BaseWidget, Ui_ModDownloader):
    '''模组下载界面'''
    SetLwResult = pyqtSignal(list)

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.pb_search.clicked.connect(self.search_mod)

        self.SetLwResult.connect(self.set_lw_result)

    @ThreadManager.asthread('加载Mod', show=False)
    def search_mod(self, _):
        name = self.le_name.text()
        search_result_list = Mod.search_mod(name)
        self.SetLwResult.emit(search_result_list)

    def set_lw_result(self, search_result_list):
        self.lw_result.clear()
        for i in search_result_list:
            item = QListWidgetItem()
            item.setSizeHint(QSize(256, 100))
            widget = ModInfo(i)
            self.lw_result.addItem(item)
            self.lw_result.setItemWidget(item, widget)


class ModInfo(QWidget):
    def __init__(self, info, parent=None) -> None:
        super().__init__(parent)
        self.info = info

        self.vbox = QVBoxLayout()

        self.l_name = QLabel(self, text=info['name'])
        self.l_name.setStyleSheet('font-weight: bold;')
        self.l_describe = QLabel(self, text=info['describe'])
        self.l_describe.setWordWrap(True)
        self.l_describe.setAlignment(QtCore.Qt.AlignTop)

        self.vbox.addWidget(self.l_name)
        self.vbox.addWidget(self.l_describe)

        self.setLayout(self.vbox)

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        self.moddetail = ModDetail(self.info)
        self.moddetail.show()
