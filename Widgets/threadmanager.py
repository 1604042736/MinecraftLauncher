from inspect import isgenerator
import logging

from QtBase.basewidget import *
from Ui.threadmanager_ui import *
import globals as g


class ThreadManager(BaseWidget, Ui_ThreadManager):
    '''线程管理'''
    thread_add_task = pyqtSignal(str, object, bool, tuple)  # 提供给线程用的接口

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.thread_add_task.connect(self.add_task)

    def add_task(self, name, iter,  show=True, args=()):
        '''添加任务'''
        # iter为生成器,可以达到实时更新进度的目的
        item = QListWidgetItem()
        item.setSizeHint(QSize(256, 64))
        widget = ThreadTaskInfo(item, name, iter, args)
        widget.finished.connect(self.finish_task)
        self.lw_task.addItem(item)
        self.lw_task.setItemWidget(item, widget)

        if show:
            self.show()

    def on_show_ready(self):
        super().on_show_ready()
        self.basewindow.remove_rightwidget(self.pb_dm)

    def finish_task(self, taskitem):
        '''结束任务'''
        self.lw_task.takeItem(self.lw_task.row(taskitem))

    @staticmethod
    def asthread(name, show=True):
        '''将函数通过线程的方式执行'''
        def wrap(func):
            def set_thread(*args):
                g.dmr.add_task(name, func, show, args)
            return set_thread
        return wrap


class ThreadTaskInfo(QWidget):
    '''线程任务信息'''
    finished = pyqtSignal(QListWidgetItem)  # 结束信号

    def __init__(self, item, name, iter, args) -> None:
        super().__init__()

        self.item = item
        self.name = name  # 名称
        self.iter = iter  # 下载函数的生成器
        self.args = args  # 函数参数

        self.hbox = QHBoxLayout()

        self.l_name = QLabel(self, text=self.name)
        self.hbox.addWidget(self.l_name)

        if isgenerator(iter):  # 是生成器就显示进度
            self.progressbar = QProgressBar(self)
            self.progressbar.setRange(0, 100)
            self.progressbar.setValue(0)
            self.hbox.addWidget(self.progressbar)

        self.pb_suspend = QPushButton(self, text='暂停')
        self.pb_suspend.setObjectName('pb_suspend')
        self.pb_suspend.clicked.connect(self.on_pb_suspend_clicked)
        self.hbox.addWidget(self.pb_suspend)

        self.pb_continue = QPushButton(self, text='继续')
        self.pb_continue.setObjectName('pb_continue')
        self.pb_continue.setEnabled(False)
        self.pb_continue.clicked.connect(self.on_pb_continue_clicked)
        self.hbox.addWidget(self.pb_continue)

        self.pb_cancel = QPushButton(self, text='取消')
        self.pb_cancel.setObjectName('pb_cancel')
        self.pb_cancel.clicked.connect(self.on_pb_cancel_clicked)
        self.hbox.addWidget(self.pb_cancel)

        self.setLayout(self.hbox)

        self.t = ThreadTask(self.iter, args)
        self.t.progressupdata.connect(self.on_t_progressupdata)
        self.t.finish.connect(self.on_t_finish)
        self.t.start()

    def on_pb_suspend_clicked(self):
        self.t.suspend = True
        self.pb_continue.setEnabled(True)
        self.pb_suspend.setEnabled(False)

    def on_pb_continue_clicked(self):
        self.t.suspend = False
        self.pb_continue.setEnabled(False)
        self.pb_suspend.setEnabled(True)

    def on_pb_cancel_clicked(self):
        self.t.quit()
        self.finished.emit(self.item)

    def on_t_progressupdata(self, progress):
        self.progressbar.setValue(progress)

    def on_t_finish(self):
        self.finished.emit(self.item)


class ThreadTask(QThread):
    '''线程任务'''
    progressupdata = pyqtSignal(int)  # 进度更新
    finish = pyqtSignal()  # 结束

    def __init__(self, iter, args) -> None:
        super().__init__()
        self.iter = iter
        self.suspend = False  # 是否暂停
        self.args = args  # 参数

    def run(self):
        if isgenerator(self.iter):
            for i in self.iter:
                while self.suspend:  # 如果暂停就一直等待
                    pass
                self.progressupdata.emit(i)  # 是生成器可以更新进度
        else:  # 不是生成器会导致无法暂停
            self.iter(*self.args)
        self.finish.emit()
