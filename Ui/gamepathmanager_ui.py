# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\王永健\PCG\MinecraftLauncher\Ui\gamepathmanager.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from QtBase.baselistwidget import BaseListWidget
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GamePathManager(object):
    def setupUi(self, GamePathManager):
        GamePathManager.setObjectName("GamePathManager")
        GamePathManager.resize(1000, 618)
        self.gridLayout = QtWidgets.QGridLayout(GamePathManager)
        self.gridLayout.setObjectName("gridLayout")
        self.pb_add = QtWidgets.QPushButton(GamePathManager)
        self.pb_add.setObjectName("pb_add")
        self.gridLayout.addWidget(self.pb_add, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.lw_path = BaseListWidget(GamePathManager)
        self.lw_path.setObjectName("lw_path")
        self.gridLayout.addWidget(self.lw_path, 0, 1, 2, 1)

        self.retranslateUi(GamePathManager)
        QtCore.QMetaObject.connectSlotsByName(GamePathManager)

    def retranslateUi(self, GamePathManager):
        _translate = QtCore.QCoreApplication.translate
        GamePathManager.setWindowTitle(_translate("GamePathManager", "游戏路径管理"))
        self.pb_add.setText(_translate("GamePathManager", "添加"))
