# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\王永健\PCG\MinecraftLauncher\Ui\setting.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Setting(object):
    def setupUi(self, Setting):
        Setting.setObjectName("Setting")
        Setting.resize(1000, 618)
        self.gridLayout = QtWidgets.QGridLayout(Setting)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(Setting)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 980, 598))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(
            self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)
        self.le_javapath = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.le_javapath.setObjectName("le_javapath")
        self.gridLayout_2.addWidget(self.le_javapath, 2, 1, 1, 2)
        self.sb_width = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        self.sb_width.setMaximum(2000)
        self.sb_width.setObjectName("sb_width")
        self.gridLayout_2.addWidget(self.sb_width, 0, 1, 1, 2)
        self.sb_height = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        self.sb_height.setMinimum(0)
        self.sb_height.setMaximum(2000)
        self.sb_height.setObjectName("sb_height")
        self.gridLayout_2.addWidget(self.sb_height, 1, 1, 1, 2)
        self.pb_openlogfolder = QtWidgets.QPushButton(
            self.scrollAreaWidgetContents)
        self.pb_openlogfolder.setObjectName("pb_openlogfolder")
        self.gridLayout_2.addWidget(self.pb_openlogfolder, 5, 2, 1, 1)
        self.sb_minmem = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        self.sb_minmem.setMaximum(8192)
        self.sb_minmem.setObjectName("sb_minmem")
        self.gridLayout_2.addWidget(self.sb_minmem, 4, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.sb_maxmem = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        self.sb_maxmem.setMaximum(8192)
        self.sb_maxmem.setObjectName("sb_maxmem")
        self.gridLayout_2.addWidget(self.sb_maxmem, 3, 1, 1, 2)
        self.pb_dellog = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pb_dellog.setObjectName("pb_dellog")
        self.gridLayout_2.addWidget(self.pb_dellog, 5, 0, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 4, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 1, 1, 1)

        self.retranslateUi(Setting)
        QtCore.QMetaObject.connectSlotsByName(Setting)

    def retranslateUi(self, Setting):
        _translate = QtCore.QCoreApplication.translate
        Setting.setWindowTitle(_translate("Setting", "设置"))
        self.label_4.setText(_translate("Setting", "最大内存"))
        self.pb_openlogfolder.setText(_translate("Setting", "打开日志文件夹"))
        self.label_2.setText(_translate("Setting", "游戏窗口宽度"))
        self.label.setText(_translate("Setting", "游戏窗口高度"))
        self.label_3.setText(_translate("Setting", "java路径"))
        self.pb_dellog.setText(_translate("Setting", "清除日志"))
        self.label_5.setText(_translate("Setting", "最小内存"))
