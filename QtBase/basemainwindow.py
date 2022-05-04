from QtBase.basewidget import *
import QtBase as g
import qtawesome as qta


class BaseMainWindow(QStackedWidget, BaseWidget):
    '''对软件中的窗口进行管理'''

    def __init__(self) -> None:
        super().__init__()
        self.resize(1000, 618)

        self.caughtwidgets = []  # 被捕获的窗口

        self.currentChanged.connect(self.on_self_currentChanged)

        g.mainwindow = self

    def ready(self):
        '''当一切准备好后...'''

    def on_any_window_show_ready(self, win):
        '''调用show之后BaseWindow准备好了(针对任何一个窗口)'''

    def resizeEvent(self, a0) -> None:
        self.resize(self.width(), self.height())

    def on_self_currentChanged(self, _):
        if self.count():
            self.pb_sepwin.show()
        else:
            self.pb_sepwin.hide()

        if self.count() > 1:
            self.pb_back.show()
        else:
            self.pb_back.hide()

        if self.basewindow:
            self.basewindow.resize_other_widget()  # 防止按钮show或hide之后没有及时更新

    def on_pb_back_clicked(self, _):
        widget = self.currentWidget()
        self.release_widget(widget)

    def on_pb_sepwin_clicked(self, _):
        widget = self.currentWidget()
        self.release_widget(widget)
        widget.show('imm')

    def on_show_ready(self):
        bw = self.basewindow
        self.pb_back = QPushButton(bw.title)
        self.pb_back.resize(bw.TH, bw.TH)
        self.pb_back.setObjectName('pb_back')
        self.pb_back.setIcon(qta.icon('fa.arrow-left'))
        self.pb_back.hide()
        bw.add_leftwidget(self.pb_back, 0)

        bw.remove_rightwidget(bw.parentwin_button)

        self.pb_sepwin = QPushButton(bw.title)
        self.pb_sepwin.resize(bw.TH, bw.TH)
        self.pb_sepwin.setObjectName('pb_sepwin')
        self.pb_sepwin.setIcon(qta.icon('fa.external-link'))
        self.pb_sepwin.hide()
        bw.add_rightwidget(self.pb_sepwin)

        self.pb_back.clicked.connect(self.on_pb_back_clicked)
        self.pb_sepwin.clicked.connect(self.on_pb_sepwin_clicked)

        super().on_show_ready()

    def catch_widget(self, widget):
        '''捕获调用show的窗体'''
        self.caughtwidgets.append(widget)
        self.addWidget(widget)
        self.setCurrentIndex(self.count()-1)

    def release_widget(self, widget):
        '''释放窗口'''
        self.removeWidget(widget)
        self.caughtwidgets.remove(widget)
