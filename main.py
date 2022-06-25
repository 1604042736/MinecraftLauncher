# -*- coding: utf-8 -*-
# pipreqs . --encoding utf-8 --force

import sys
import json
from Widgets.mainwindow import *
import globals as g


def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()

    app.setStyleSheet('''
QGroupBox{
    font-size: 13px;
    font-weight: bold;
    border:4px solid white;
    border-radius:10px;
    background-color:white;
}
QScrollArea{
    border:none;
}
QListWidget{
    border:none;
}
QListWidget::Item:hover{
    background-color:rgb(240,240,240);
}
QListWidget::Item:selected{
    background-color:rgb(230,230,230);
}
QListWidget QPushButton{
    border:1px solid rgb(0,0,0);
}
QListWidget QPushButton:hover{
    background-color:rgb(200,200,200);
}
QListWidget QLabel{
    font-size:13px;
}
''')
    app.exec()
    json.dump(g.config, open('config.json', encoding='utf-8', mode='w'))
    sys.exit()


if __name__ == '__main__':
    main()
