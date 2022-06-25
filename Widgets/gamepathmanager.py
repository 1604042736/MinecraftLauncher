# -*- coding: utf-8 -*-
from Api.managegamepath import ManageGamePath
from Ui.gamepathmanager_ui import *
from QtBase.basewidget import *


class GamePathManager(BaseWidget, Ui_GamePathManager):
    '''游戏路径管理界面'''

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.mgp = ManageGamePath

        self.set_lw_path()

    def set_lw_path(self):
        self.lw_path.clear()
        cur_path = self.mgp.get_cur_path()
        for i in self.mgp.get_all_path():
            item = QListWidgetItem()
            item.setSizeHint(QSize(256, 64))
            widget = GamePathInfo(i, i == cur_path)
            widget.settocurpath.connect(self.settocurpath)
            widget.delpath.connect(self.delpath)
            self.lw_path.addItem(item)
            self.lw_path.setItemWidget(item, widget)

    def settocurpath(self, path):
        self.mgp.settocurpath(path)
        self.set_lw_path()

    def delpath(self, path):
        def ok():
            self.mgp.delpath(path)
            self.set_lw_path()
        self.warning_dialog("删除", "确定删除?", ok)

    @pyqtSlot(bool)
    def on_pb_add_clicked(self, _):
        path = QFileDialog.getExistingDirectory(self, '选择文件夹', '.')
        if path:
            self.mgp.addpath(path)
            self.set_lw_path()


class GamePathInfo(QWidget):
    '''游戏路径信息'''
    settocurpath = pyqtSignal(str)
    delpath = pyqtSignal(str)

    def __init__(self, gamepath, is_cur=False) -> None:
        super().__init__()
        self.gamepath = gamepath
        self.is_cur = is_cur  # 是否是当前路径(cur_path)

        self.hbox = QHBoxLayout()

        self.l_path = QLabel(self, text=self.gamepath)
        if self.is_cur:
            self.l_path.setStyleSheet('color:red;')
        self.hbox.addWidget(self.l_path)

        self.pb_settocur = QPushButton(self, text='设置成当前路径')
        if self.is_cur:
            self.pb_settocur.setEnabled(False)
        self.pb_settocur.clicked.connect(self.on_pb_settocur_clicked)
        self.hbox.addWidget(self.pb_settocur)

        self.pb_del = QPushButton(self)
        self.pb_del.setIcon(qta.icon('mdi.delete'))
        self.pb_del.clicked.connect(self.on_pb_del_clicked)
        self.hbox.addWidget(self.pb_del)

        self.setLayout(self.hbox)

    def on_pb_settocur_clicked(self):
        self.settocurpath.emit(self.gamepath)

    def on_pb_del_clicked(self):
        self.delpath.emit(self.gamepath)
