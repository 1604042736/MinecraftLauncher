# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\王永健\PCG\MinecraftLauncher\Ui\welcome.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from QtBase.baselistwidget import BaseListWidget
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Welcome(object):
    def setupUi(self, Welcome):
        Welcome.setObjectName("Welcome")
        Welcome.resize(1000, 618)
        self.gridLayout = QtWidgets.QGridLayout(Welcome)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(Welcome)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lw_func = BaseListWidget(self.groupBox)
        self.lw_func.setObjectName("lw_func")
        self.gridLayout_2.addWidget(self.lw_func, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Welcome)
        QtCore.QMetaObject.connectSlotsByName(Welcome)

    def retranslateUi(self, Welcome):
        _translate = QtCore.QCoreApplication.translate
        Welcome.setWindowTitle(_translate("Welcome", "欢迎"))
        self.groupBox.setTitle(_translate("Welcome", "所有功能"))
