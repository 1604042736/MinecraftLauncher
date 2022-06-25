# -*- coding: utf-8 -*-
import webbrowser
from Api.mod import Mod
from QtBase.basewidget import *
from Ui.moddetail_ui import *
from Widgets.threadmanager import ThreadManager


class ModDetail(BaseWidget, Ui_ModDetail):
    '''模组详情界面'''
    SetLwModFiles = pyqtSignal(list)

    def __init__(self, mod_info) -> None:
        super().__init__()
        self.setupUi(self)
        self.mod_info = mod_info

        self.SetLwModFiles.connect(self.set_lw_modfiles)

        self.set_info()
        self.get_modfiles()

    def set_info(self):
        self.l_name.setText(self.mod_info['name'])
        self.l_name.setStyleSheet('font-weight: bold;')
        self.l_describe.setText(self.mod_info['describe'])
        self.l_describe.setWordWrap(True)
        self.l_describe.setAlignment(QtCore.Qt.AlignTop)

    @ThreadManager.asthread('加载Mod文件', show=False)
    def get_modfiles(self):
        self.lw_modfiles.clear()
        files = Mod.get_mod_files(self.mod_info)
        self.SetLwModFiles.emit(files)

    def set_lw_modfiles(self, files):
        self.lw_modfiles.clear()
        for i in files:
            item = QListWidgetItem()
            item.setSizeHint(QSize(256, 64))
            widget = ModFileInfo(i)
            self.lw_modfiles.addItem(item)
            self.lw_modfiles.setItemWidget(item, widget)

    @pyqtSlot(bool)
    def on_pb_mcmod_clicked(self, _):
        webbrowser.open(self.mod_info['mcmod_url'])

    @pyqtSlot(bool)
    def on_pb_curseforge_clicked(self, _):
        webbrowser.open(self.mod_info['curseforge_url'])


class ModFileInfo(QWidget):
    def __init__(self, info) -> None:
        super().__init__()
        self.info = info

        self.hbox = QHBoxLayout()

        self.l_name = QLabel(self, text=info['name'])
        self.pb_download = QPushButton(self, text='下载')
        self.pb_download.clicked.connect(self.download_mod_file)

        self.hbox.addWidget(self.l_name)
        self.hbox.addWidget(self.pb_download)

        self.setLayout(self.hbox)

    def download_mod_file(self):
        path = QFileDialog.getExistingDirectory(self, '选择文件夹', '.')
        if path:
            iter = Mod.download_mod_file(self.info, path)
            g.dmr.add_task(f'下载{self.info["name"]}', iter)
