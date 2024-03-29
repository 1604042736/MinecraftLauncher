# -*- coding: utf-8 -*-
from QtBase.basewidget import *
from Ui.setting_ui import *
import globals as g
import os


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

    @pyqtSlot(bool)
    def on_pb_dellog_clicked(self, _):
        for i in os.listdir('Logs'):
            try:
                os.remove(os.path.join('Logs', i))
            except:
                pass

    @pyqtSlot(bool)
    def on_pb_openlogfolder_clicked(self, _):
        os.startfile('Logs')
