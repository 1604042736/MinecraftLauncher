# -*- coding: utf-8 -*-
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
        self.setMouseTracking(True)
        self.resize(1000, 618)

    def show(self, mode='none') -> None:
        '''通过BaseWindow显示'''
        self.set_all_mousetrack(self)
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

    def warning_dialog(self, title, message, ok_connect):
        '''警告对话框'''
        reply = QMessageBox.warning(
            self, title, message, QMessageBox.Ok | QMessageBox.Cancel)
        if reply == QMessageBox.Ok:
            ok_connect.emit()

    def set_all_mousetrack(self, w):
        '''将所有控件设置为鼠标跟踪'''
        children = w.findChildren(QWidget)
        for child in children:
            child.setMouseTracking(True)
            self.set_all_mousetrack(child)
