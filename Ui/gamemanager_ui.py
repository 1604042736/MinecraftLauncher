# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\王永健\PCG\MinecraftLauncher\Ui\gamemanager.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GameManager(object):
    def setupUi(self, GameManager):
        GameManager.setObjectName("GameManager")
        GameManager.resize(1000, 618)
        self.gridLayout = QtWidgets.QGridLayout(GameManager)
        self.gridLayout.setObjectName("gridLayout")
        self.lw_gamelist = QtWidgets.QListWidget(GameManager)
        self.lw_gamelist.setObjectName("lw_gamelist")
        self.gridLayout.addWidget(self.lw_gamelist, 0, 0, 1, 1)

        self.retranslateUi(GameManager)
        QtCore.QMetaObject.connectSlotsByName(GameManager)

    def retranslateUi(self, GameManager):
        _translate = QtCore.QCoreApplication.translate
        GameManager.setWindowTitle(_translate("GameManager", "游戏管理"))
