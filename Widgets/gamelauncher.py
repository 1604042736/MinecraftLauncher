# -*- coding: utf-8 -*-
import os
from Api.launchgame import LaunchGame
from QtBase.basewidget import *
from Ui.gamelauncher_ui import *
import globals as g


class GameLauncer(BaseWidget, Ui_GameLauncher):
    '''游戏启动器'''

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.set_cb_curversion()
        self.le_playername.setText(g.config['player_name'])

    def set_cb_curversion(self):
        self.cb_curversion.clear()
        cur_version = g.config['cur_version']
        if cur_version:
            self.cb_curversion.addItem(cur_version)
        version_path = os.path.join(g.config['cur_gamepath'], 'versions')
        if not os.path.exists(version_path):
            return
        for i in os.listdir(version_path):
            if i != cur_version:
                self.cb_curversion.addItem(i)

    @pyqtSlot(bool)
    def on_pb_startgame_clicked(self, _):
        g.config['player_name'] = self.le_playername.text()
        name = self.cb_curversion.currentText()
        g.config['cur_version'] = name

        g.dmr.add_task(f'启动{name}', LaunchGame(name).launch(g.config['javapath'], g.config['player_name'],
                                                            g.config['width'], g.config['height'], g.config['maxmem'], g.config['minmem']))

    def on_t_finish(self):
        self.pb_startgame.setEnabled(True)
        self.pb_startgame.setText('开始游戏')


class LaunchGameThread(QThread):
    '''游戏启动线程'''
    finish = pyqtSignal()  # 结束

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

    def run(self):
        name = self.name
        LaunchGame(name).launch(g.config['javapath'], g.config['player_name'],
                                g.config['width'], g.config['height'], g.config['maxmem'], g.config['minmem'])
        self.finish.emit()
