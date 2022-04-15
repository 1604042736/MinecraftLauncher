from QtBase.basemainwindow import *
from Widgets.threadmanager import ThreadManager
from Widgets.welcome import *
import globals as g
import qtawesome as qta


class MainWindow(BaseMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('我的世界启动器')

    def ready(self):
        self.welcome = Welcome()
        self.welcome.show()
        g.dmr = ThreadManager()

    def on_any_window_show_ready(self, win):
        bw = win.basewindow

        if win is not self:
            win.pb_home = QPushButton(bw.title)
            win.pb_home.resize(bw.TH, bw.TH)
            win.pb_home.setObjectName('pb_home')
            win.pb_home.setIcon(qta.icon('fa.home'))
            win.pb_home.clicked.connect(lambda: self.show())
            bw.add_rightwidget(win.pb_home)

        win.pb_dm = QPushButton(bw.title)
        win.pb_dm.resize(bw.TH, bw.TH)
        win.pb_dm.setObjectName('pb_dm')
        win.pb_dm.setIcon(qta.icon('fa.list-alt'))
        win.pb_dm.clicked.connect(lambda: g.dmr.show())
        bw.add_rightwidget(win.pb_dm)
