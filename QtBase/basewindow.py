from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ctypes.wintypes import *
from win32gui import *
from win32con import *
import QtBase as g
import qtawesome as qta


class BaseWindow(QWidget):
    '''
    对窗口进行了一些处理
    BaseWidget显示时会使用这个类
    '''
    TH = 32  # TITLE_HEIGHT = 32  # 标题栏高度
    TD = 4  # TOP_DISTANCE = 4  # 上边框距离
    BD = 4  # BOTTOM_DISTANCE = 4  # 下边框距离
    LD = 4  # LEFT_DISTANCE = 4  # 左边框距离
    RD = 4  # RIGHT_DISTANCE = 16  # 右边框距离
    LL = 0  # LEFTLEN = 0  # 左边控件长度
    RL = 0  # RIGHTLEN = 0  # 右边控件长度
    YS = 0  # YSHIFT = 0  # 偏移,最大化后不能用原来的坐标

    def __init__(self, widget) -> None:
        super().__init__()
        self.widget = widget
        self.widget.setParent(self)
        self.widget.move(0, 0)
        self.resize(widget.width(), widget.height())

        self.set_title()
        self.set_connection()
        self.set_windowstyle()

        self.setWindowTitle(widget.windowTitle())

        QWidget.show(widget)  # 防止因为各种原因造成widget隐藏

    def set_windowstyle(self):
        '''设置窗口样式'''
        self.setWindowFlag(Qt.FramelessWindowHint)  # 不设置会导致窗口大小不正确
        hwnd = self.winId()
        style = GetWindowLong(hwnd, GWL_STYLE)
        SetWindowLong(hwnd, GWL_STYLE, style | WS_MAXIMIZEBOX |
                      WS_THICKFRAME | WS_CAPTION)

    def set_title(self):
        '''实现一个标题栏'''

        self.rightWidgets = []  # 标题栏靠右的控件
        self.leftWidgets = []  # 标题栏靠左的控件

        self.title = QFrame(self)
        self.title.setObjectName('title')
        self.title.move(0, 0)
        self.title.hide()

        # 标题栏里的按钮
        self.close_button = QPushButton(self.title)
        self.close_button.resize(self.TH, self.TH)
        self.close_button.setObjectName('close_button')
        self.close_button.setIcon(qta.icon('fa.close'))

        self.maxnormal_button = QPushButton(self.title)
        self.maxnormal_button.resize(self.TH, self.TH)
        self.maxnormal_button.setObjectName('maxnormal_button')
        self.maxnormal_button.setIcon(qta.icon('fa5.window-maximize'))

        self.min_button = QPushButton(self.title)
        self.min_button.resize(self.TH, self.TH)
        self.min_button.setObjectName('min_button')
        self.min_button.setIcon(qta.icon('ei.minus'))

        self.parentwin_button = QPushButton(self.title)
        self.parentwin_button.resize(self.TH, self.TH)
        self.parentwin_button.setObjectName('parentwin_button')
        self.parentwin_button.setIcon(qta.icon('fa.mail-reply-all'))

        self.l_title = QLabel(self.title, text=self.widget.windowTitle())
        self.l_title.resize(128, self.TH)

        self.add_rightwidget(self.close_button)
        self.add_rightwidget(self.maxnormal_button)
        self.add_rightwidget(self.min_button)
        self.add_rightwidget(self.parentwin_button)
        self.add_leftwidget(self.l_title)

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

    def set_connection(self):
        '''设置信号和槽'''
        self.close_button.clicked.connect(self.on_close_button_clicked)
        self.maxnormal_button.clicked.connect(self.on_maxnormal_button_clicked)
        self.min_button.clicked.connect(self.on_min_button_clicked)
        self.parentwin_button.clicked.connect(self.on_parentwin_button_clicked)

    def on_close_button_clicked(self):
        self.close()

    def on_maxnormal_button_clicked(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def on_min_button_clicked(self):
        self.showMinimized()

    def on_parentwin_button_clicked(self):
        '''重新回归mainwindow'''
        if self is not g.mainwindow:
            self.widget.show()

    def setWindowTitle(self, a0: str) -> None:
        self.l_title.setText(a0)
        return super().setWindowTitle(a0)

    def showMaximized(self) -> None:
        self.maxnormal_button.setIcon(qta.icon('fa5.window-restore'))
        return super().showMaximized()

    def showNormal(self) -> None:
        self.maxnormal_button.setIcon(qta.icon('fa5.window-maximize'))
        return super().showNormal()

    def resizeEvent(self, a0) -> None:
        self.widget.resize(self.width(), self.height())
        self.title.resize(self.width(), self.TH)
        self.resize_other_widget()

    def resize_other_widget(self):
        '''设置其他控件大小'''
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

    def GET_X_LPARAM(self, param: int) -> int:
        return param & 0xffff

    def GET_Y_LPARAM(self, param: int) -> int:
        return param >> 16

    def moveEvent(self, a0) -> None:
        pos = a0.pos()
        try:
            if pos.x() < 0 and pos.y() < 0:  # 防止超出屏幕(一般发生在最大化的时侯)
                self.maxnormal_button.setIcon(qta.icon('fa5.window-restore'))
                # 桌面的宽高,也就是窗口最大化时的宽高
                width = QDesktopWidget().availableGeometry().width()
                height = QDesktopWidget().availableGeometry().height()
                # 得到偏移的大小
                x = 0-pos.x() if pos.x() < 0 else 0
                y = 0-pos.y() if pos.y() < 0 else 0
                self.YS = y
                # moveEvent比resizeEvent晚发出,所以不会影响
                self.widget.move(x, y)
                self.widget.resize(width, height)
                self.title.move(x, y)
                self.title.resize(width, self.TH)
                self.resize_other_widget()
            else:
                self.YS = 0
                self.title.move(0, 0)
                self.widget.move(0, 0)
                self.resizeEvent(None)
        except AttributeError:
            pass

    def nativeEvent(self, eventType, message):
        if self.parent():  # 作为子窗口时不处理
            return False, 0
        msg = MSG.from_address(message.__int__())
        if msg.message == WM_NCCALCSIZE:
            return True, 0
        elif msg.message == WM_NCHITTEST:
            xPos = self.GET_X_LPARAM(msg.lParam) - self.frameGeometry().x()
            yPos = self.GET_Y_LPARAM(msg.lParam) - self.frameGeometry().y()
            right = self.width()-self.RD
            bottom = self.height()-self.BD
            if self.title.isHidden():
                if yPos <= self.TD+self.YS:
                    self.title.show()
            else:  # 只有在标题栏显示时才能拖动
                if (self.TD < yPos < self.TH+self.YS and self.LD+self.LL < xPos < right-self.RL):  # 使标题栏上的按钮可点击
                    return True, HTCAPTION
                if yPos > self.TH+self.YS:  # 超出范围重新隐藏
                    self.title.hide()
            if xPos <= self.LD and yPos <= self.TD:
                return True, HTTOPLEFT
            elif xPos >= right and yPos <= self.TD:
                return True, HTTOPRIGHT
            elif yPos >= bottom and xPos <= self.LD:
                return True, HTBOTTOMLEFT
            elif yPos >= bottom and xPos >= right:
                return True, HTBOTTOMRIGHT
            elif yPos <= self.TD:
                return True, HTTOP
            elif xPos <= self.LD:
                return True, HTLEFT
            elif xPos >= right:
                return True, HTRIGHT
            elif yPos >= bottom:
                return True, HTBOTTOM
        return False, 0

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
