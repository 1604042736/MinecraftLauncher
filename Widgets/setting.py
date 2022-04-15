import logging
from QtBase.basewidget import *
from Ui.setting_ui import *
import globals as g
from qt_material import *


class Setting(BaseWidget, Ui_Setting):
    '''设置界面'''

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.set_all()

    def set_all(self):
        '''设置所有'''
        self.sb_width.setValue(g.config['width'])
        self.sb_height.setValue(g.config['height'])
        self.le_javapath.setText(g.config['javapath'])
        self.sb_maxmem.setValue(g.config['maxmem'])
        self.sb_minmem.setValue(g.config['minmem'])
        theme = g.config['theme']
        self.cb_theme.clear()
        self.cb_theme.addItems(list_themes())
        self.cb_theme.setCurrentText(theme)

    def save_all(self):
        '''保存所有'''
        g.config['width'] = self.sb_width.value()
        g.config['height'] = self.sb_height.value()
        g.config['javapath'] = self.le_javapath.text()
        g.config['maxmem'] = self.sb_maxmem.value()
        g.config['minmem'] = self.sb_minmem.value()

    @pyqtSlot(int)
    def on_sb_width_valueChanged(self, _):
        g.config['width'] = self.sb_width.value()

    @pyqtSlot(int)
    def on_sb_height_valueChanged(self, _):
        g.config['height'] = self.sb_height.value()

    @pyqtSlot(str)
    def on_le_javapath_textChanged(self, _):
        g.config['javapath'] = self.le_javapath.text()

    @pyqtSlot(int)
    def on_sb_maxmem_valueChanged(self, _):
        g.config['maxmem'] = self.sb_maxmem.value()

    @pyqtSlot(int)
    def on_sb_minmem_valueChanged(self, _):
        g.config['minmem'] = self.sb_minmem.value()

    @pyqtSlot(str)
    def on_cb_theme_currentTextChanged(self, text):
        g.config['theme'] = text
        apply_stylesheet(qApp, theme=text)
