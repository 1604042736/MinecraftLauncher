from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import QtBase as g
import qtawesome as qta


class BaseWindow(QWidget):
    '''
    对窗口进行了一些处理
    BaseWidget显示时会使用这个类
    '''
    TH = 32  # TITLE_HEIGHT = 32  # 标题栏高度
    LL = 0  # LEFTLEN = 0  # 左边控件长度
    RL = 0  # RIGHTLEN = 0  # 右边控件长度

    def __init__(self, widget) -> None:
        super().__init__()
        self.widget = widget
        self.widget.setParent(self)
        self.widget.move(0, 0)
        self.resize(widget.width(), widget.height())

        self.set_title()
        self.set_connection()

        self.setWindowTitle(widget.windowTitle())

        QWidget.show(widget)  # 防止因为各种原因造成widget隐藏
        self.setMouseTracking(True)

    def set_title(self):
        '''实现一个标题栏'''

        self.rightWidgets = []  # 标题栏靠右的控件
        self.leftWidgets = []  # 标题栏靠左的控件

        self.title = QFrame(self)
        self.title.setObjectName('title')
        self.title.move(0, 0)
        self.title.hide()

        # 标题栏里的按钮
        self.parentwin_button = QPushButton(self.title)
        self.parentwin_button.resize(self.TH, self.TH)
        self.parentwin_button.setObjectName('parentwin_button')
        self.parentwin_button.setIcon(qta.icon('fa.mail-reply-all'))

        self.add_rightwidget(self.parentwin_button)

        self.title.raise_()

        self.title.setStyleSheet('''
QFrame{
    background-color:rgb(255,255,255);
}
QPushButton{
    border:none;
}
QPushButton:hover{
    background-color:rgb(200,200,200);
}
QPushButton#close_button:hover{
    background-color:rgb(255,0,0);
}
        ''')

    def mouseMoveEvent(self, a0) -> None:
        x, y = a0.x(), a0.y()
        inrange = self.title.x() <= x <= self.title.x()+self.title.width()  # 在标题栏范围内
        if y < 2 and inrange:
            self.title.show()
        elif y > self.TH or not inrange:
            self.title.hide()

    def set_connection(self):
        '''设置信号和槽'''
        self.parentwin_button.clicked.connect(self.on_parentwin_button_clicked)

    def on_parentwin_button_clicked(self):
        '''重新回归mainwindow'''
        if self is not g.mainwindow:
            self.widget.show()

    def resizeEvent(self, a0) -> None:
        self.widget.resize(self.width(), self.height())
        self.resize_other_widget()

    def resize_other_widget(self):
        '''设置其他控件大小'''
        title_width = sum([w.width() for w in self.rightWidgets if not w.isHidden()] +
                          [w.width() for w in self.leftWidgets if not w.isHidden()])
        self.title.resize(title_width, self.TH)
        self.title.move(int((self.width()-title_width)/2), 0)
        # 实时计算位置
        self.RL = 0
        for widget in self.rightWidgets:
            if widget.isHidden():
                continue
            self.RL += widget.width()
            widget.move(self.title.width()-self.RL, 0)
        self.LL = 0
        for widget in self.leftWidgets:
            if widget.isHidden():
                continue
            widget.move(self.LL, 0)
            self.LL += widget.width()

    def add_rightwidget(self, widget: QWidget, index=-1):
        '''往标题栏右侧添加控件'''
        if index < 0:
            index = len(self.rightWidgets)+index+1
        self.rightWidgets.insert(index, widget)
        widget.resize(widget.width(), self.TH)
        self.resize_other_widget()

    def remove_rightwidget(self, widget: QWidget):
        '''删除标题栏右侧的控件'''
        self.rightWidgets.remove(widget)
        widget.hide()  # 避免干扰
        self.resize_other_widget()

    def add_leftwidget(self, widget: QWidget, index=-1):
        '''往标题栏左侧添加控件'''
        if index < 0:
            index = len(self.rightWidgets)+index+1
        self.leftWidgets.insert(index, widget)
        widget.resize(widget.width(), self.TH)
        self.resize_other_widget()

    def remove_leftwidget(self, widget: QWidget):
        '''删除标题栏左侧的控件'''
        self.leftWidgets.remove(widget)
        widget.hide()  # 避免干扰
        self.resize_other_widget()

    def remove_widget(self, widget: QWidget):
        '''删除标题栏的控件'''
        try:
            self.remove_leftwidget(widget)
        except:
            self.remove_rightwidget(widget)
