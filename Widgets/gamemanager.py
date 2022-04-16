import json
import globals as g
from Api.game import Game
from Api.launchgame import LaunchGame
from QtBase.basewidget import *
from Ui.gamemanager_ui import *
import globals as g
import os


class GameManager(BaseWidget, Ui_GameManager):
    '''游戏管理器'''

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.set_lw_gamelist()

    def set_lw_gamelist(self):
        self.lw_gamelist.clear()
        for i in os.listdir(g.config['cur_gamepath']+'\\versions'):
            if not os.path.exists(f'{g.config["cur_gamepath"]}\\versions\\{i}\\config.json'):
                g.logapi.info(f'忽略没有配置的版本{i}')
                continue
            item = QListWidgetItem()
            item.setSizeHint(QSize(256, 64))
            widget = GameInfo(i)
            widget.delgame.connect(self.delgame)
            self.lw_gamelist.addItem(item)
            self.lw_gamelist.setItemWidget(item, widget)

    def delgame(self, name):
        reply = QMessageBox.warning(
            self, "删除", "确定删除?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            Game.del_game(name)
            self.set_lw_gamelist()


class GameInfo(QWidget):
    '''游戏信息'''
    delgame = pyqtSignal(str)

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

        # 导入配置文件
        self.config = json.load(
            open(f'{g.config["cur_gamepath"]}\\versions\\{name}\\config.json'))

        self.hbox = QHBoxLayout()

        self.l_name = QLabel(self, text=name)
        self.hbox.addWidget(self.l_name)

        if self.config['forge_version']:
            self.pb_reinstall_forge = QPushButton(self, text='重新安装Forge')
            self.pb_reinstall_forge.clicked.connect(
                self.on_pb_reinstall_forge_clicked)
            self.hbox.addWidget(self.pb_reinstall_forge)

        self.pb_redownload_lib = QPushButton(self, text='重新安装libraries')
        self.pb_redownload_lib.clicked.connect(
            self.on_pb_redownload_lib_clicked)
        self.hbox.addWidget(self.pb_redownload_lib)

        self.pb_redownload_asset = QPushButton(self, text='重新安装asset')
        self.pb_redownload_asset.clicked.connect(
            self.on_pb_redownload_asset_clicked)
        self.hbox.addWidget(self.pb_redownload_asset)

        self.pb_del = QPushButton(self, text='删除')
        self.pb_del.clicked.connect(self.on_pb_del_clicked)
        self.hbox.addWidget(self.pb_del)

        self.setLayout(self.hbox)

    def on_pb_del_clicked(self):
        self.delgame.emit(self.name)

    def on_pb_reinstall_forge_clicked(self):
        Game.install_forge(
            self.name, self.config['version'], self.config['forge_version'])

    def on_pb_redownload_lib_clicked(self):
        g.dmr.add_task(f'重新下载lib', LaunchGame(
            self.name, True).analysis_libraries(True))

    def on_pb_redownload_asset_clicked(self):
        g.dmr.add_task(f'重新下载asset', LaunchGame(
            self.name, True).analysis_assets(True))
