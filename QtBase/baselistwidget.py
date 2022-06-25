# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *


class BaseListWidget(QListWidget):
    '''解决QListWidget不支持监听鼠标移动事件问题'''

    def mouseMoveEvent(self, e) -> None:
        self.parent().mouseMoveEvent(e)