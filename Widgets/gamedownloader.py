# -*- coding: utf-8 -*-
from QtBase.basewidget import *
from Ui.gamedownloader_ui import *
from Api.game import Game
import globals as g
from Widgets.threadmanager import *


class GameDownloader(BaseWidget, Ui_GameDownloader):
    '''游戏下载器'''

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.download_content = {  # 下载内容
            "version": "",
            "forge": "",
            "optifine": "",
            "liteloader": ""
        }
        self.set_cb_version()

    @pyqtSlot(str)
    def on_le_name_textChanged(self, text):
        if text:
            self.pb_download.setEnabled(True)
        else:
            self.pb_download.setEnabled(False)

    @ThreadManager.asthread('加载游戏版本', show=False)
    def set_cb_version(self):
        self.cb_version.clear()
        self.cb_version.addItem('')
        for i in Game.get_versions():
            self.cb_version.addItem(i)

    @ThreadManager.asthread('加载Forge', show=False)
    def set_cb_forge(self):
        version = self.cb_version.currentText()
        self.cb_forge.clear()
        self.cb_forge.addItem('')
        for i in Game.get_forge(version):
            self.cb_forge.addItem(i)

    @ThreadManager.asthread('加载Optifine', show=False)
    def set_cb_optifine(self):
        version = self.cb_version.currentText()
        self.cb_optifine.clear()
        self.cb_optifine.addItem('')
        for i in Game.get_optifine(version):
            self.cb_optifine.addItem(i)

    @ThreadManager.asthread('加载liteloader', show=False)
    def set_cb_liteloader(self):
        version = self.cb_version.currentText()
        self.cb_liteloader.clear()
        self.cb_liteloader.addItem('')
        for i in Game.get_liteloader(version):
            self.cb_liteloader.addItem(i)

    def set_le_name(self):
        text = []
        for key, val in self.download_content.items():
            if not val:
                continue
            if key == 'version':
                text.append(val)
            else:
                text.append(f'{key}{val}')
        self.le_name.setText('-'.join(text))

    @pyqtSlot(str)
    def on_cb_version_currentTextChanged(self, text):
        if text:
            self.set_cb_forge()
            self.set_cb_optifine()
            self.set_cb_liteloader()
            self.download_content['version'] = text
            self.set_le_name()

    @pyqtSlot(str)
    def on_cb_forge_currentTextChanged(self, text):
        if text:
            self.download_content['forge'] = text
            self.set_le_name()

    @pyqtSlot(str)
    def on_cb_optifine_currentTextChanged(self, text):
        if text:
            self.download_content['optifine'] = text
            self.set_le_name()

    @pyqtSlot(str)
    def on_cb_liteloader_currentTextChanged(self, text):
        if text:
            self.download_content['liteloader'] = text
            self.set_le_name()

    @pyqtSlot(bool)
    def on_pb_download_clicked(self, _):
        name = self.le_name.text()
        iter = Game.download_version(
            name, self.download_content['version'], self.download_content['forge'])
        g.dmr.add_task(f'下载{name}', iter)
