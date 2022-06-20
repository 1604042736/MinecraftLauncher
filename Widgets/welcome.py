from importlib import import_module
from QtBase.baselistwidget import BaseListWidget
from Ui.welcome_ui import *
from QtBase.basewidget import *
import Widgets.gamepathmanager
import Widgets.gamedownloader
import Widgets.gamelauncher
import Widgets.setting
import Widgets.gamemanager
import Widgets.about


class Welcome(BaseWidget, Ui_Welcome):
    '''欢迎界面'''

    func_dict = {  # 功能
        "游戏路径管理": {
            "import_path": Widgets.gamepathmanager,
            "main_class": "GamePathManager",
            "describe": "对游戏的路径进行管理(添加,删除,修改)"
        },
        "游戏下载": {
            "import_path": Widgets.gamedownloader,
            "main_class": "GameDownloader",
            "describe": "下载与游戏有关的东西(游戏本体,Forge,Optifin,Liteloader)"
        },
        "游戏启动": {
            "import_path": Widgets.gamelauncher,
            "main_class": "GameLauncer",
            "describe": "启动游戏"
        },
        "设置": {
            "import_path": Widgets.setting,
            "main_class": "Setting",
            "describe": "设置"
        },
        "游戏管理": {
            "import_path": Widgets.gamemanager,
            "main_class": "GameManager",
            "describe": "对游戏进行管理"
        },
        "关于": {
            "import_path": Widgets.about,
            "main_class": "About",
            "describe": "跟软件有关的信息"
        }
    }

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.set_lw_func()

    def set_lw_func(self):
        '''设置功能列表'''
        self.lw_func.clear()
        for key, val in self.func_dict.items():
            item = QListWidgetItem()
            item.setSizeHint(QSize(256, 64))
            widget = FuncInfo(val['import_path'],
                              val['main_class'], key+':'+val['describe'])
            self.lw_func.addItem(item)
            self.lw_func.setItemWidget(item, widget)


class FuncInfo(QWidget):
    '''功能信息'''

    def __init__(self, import_path, main_class, describe) -> None:
        '''
        import_path:导入的路径,可以用__import__导入
        main_class:主类
        describe:描述
        '''
        super().__init__()
        self.import_path = import_path
        self.main_class = main_class

        self.hbox = QHBoxLayout()

        self.l_describe = QLabel(self, text=describe)

        self.pb_start = QPushButton(self, text='启动')
        self.pb_start.clicked.connect(self.on_pb_start_clicked)

        self.hbox.addWidget(self.l_describe)
        self.hbox.addWidget(self.pb_start)

        self.setLayout(self.hbox)

    def on_pb_start_clicked(self):
        if isinstance(self.import_path, str):
            module = import_module(self.import_path)  # 导入包
        else:
            module = self.import_path
        main_class = module.__dict__[self.main_class]()  # 获取主类
        if isinstance(main_class, BaseWidget):  # 是个窗口
            self.instance = main_class
            self.instance.show()
        else:
            ...
