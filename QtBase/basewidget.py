from PyQt5.QtWidgets import *
from QtBase.basewindow import *
import QtBase as g  # 用__init__.py存储全局信息


class BaseWidget(QWidget):
    '''
    在QWidget的基础上添加了一些功能
    作为其他窗体的基类
    '''

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.basewindow = None  # 如果窗口显示了这个变量不会为None
        self.dialog = None  # 对话框
        self._dialog = None  # 承载对话框,覆盖整个窗口

    def show(self, mode='none') -> None:
        '''通过BaseWindow显示'''
        if (mode == 'none'  # 不是立即显示
                        and g.mainwindow != None  # 有主窗口
                        and self is not g.mainwindow  # 这个窗口不是主窗口
                        and g.mainwindow.basewindow != None  # 已经主窗口显示了
                        and g.mainwindow.basewindow.isVisible()
                ):
            if self.basewindow:
                self.basewindow.close()
            g.mainwindow.catch_widget(self)
            return
        if mode == 'super':  # 用原来的方法show
            super().show()
            return
        self.basewindow = BaseWindow(self)
        self.on_show_ready()
        self.basewindow.show()

    def close(self) -> bool:
        '''重写close以释放被捕获的窗口'''
        if g.mainwindow and self is not g.mainwindow:
            g.mainwindow.release_widget(self)
        super().close()

    def on_show_ready(self):
        '''调用show之后BaseWindow准备好了(针对当前窗口)'''
        if g.mainwindow != None:
            g.mainwindow.on_any_window_show_ready(self)

    def resizeEvent(self, a0) -> None:
        if self._dialog != None:
            self._dialog.resize(self.width(), self.height())
        if self.dialog != None:
            self.dialog.resize(int(self.width()/2), int(self.height()/2))
            w, h = self.dialog.width(), self.dialog.height()
            self.dialog.move(int((self.width()-w)/2), int((self.height()-h)/2))

    def warning_dialog(self, title, message, ok_connect):
        '''警告对话框'''
        self._dialog = QWidget(self)
        self._dialog.setGeometry(0, 0, self.width(), self.height())

        self.dialog = QWidget(self._dialog)
        self.dialog.setObjectName('dialog')

        self.dialog.resize(int(self.width()/2), int(self.height()/2))
        w, h = self.dialog.width(), self.dialog.height()
        self.dialog.move(int((self.width()-w)/2), int((self.height()-h)/2))
        
        self.dialog.setStyleSheet(
            'QWidget#dialog{border:1px solid rgb(0,0,0);}')

        vbox = QVBoxLayout()

        l_title = QLabel(self.dialog, text=title)
        l_message = QLabel(self.dialog, text=message)

        pb_ok = QPushButton(self.dialog, text='确定')
        pb_ok.clicked.connect(self.dialog.close)
        pb_ok.clicked.connect(self._dialog.close)
        pb_ok.clicked.connect(ok_connect)
        pb_cancel = QPushButton(self.dialog, text='取消')
        pb_cancel.clicked.connect(self.dialog.close)
        pb_cancel.clicked.connect(self._dialog.close)

        vbox.addWidget(l_title)
        vbox.addWidget(l_message)
        vbox.addWidget(pb_ok)
        vbox.addWidget(pb_cancel)

        self.dialog.setLayout(vbox)
        self._dialog.show()
        self.dialog.show()
