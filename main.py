# pyinstaller -F main.py -n MinecraftLauncher -w --distpath ./
# pipreqs . --encoding utf-8 --force

import sys
import json
from Widgets.mainwindow import *
import globals as g
from qt_material import apply_stylesheet


def main():
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme=g.config["theme"])
    mainwindow = MainWindow()
    mainwindow.show()
    mainwindow.ready()
    app.exec()
    json.dump(g.config, open('config.json', encoding='utf-8', mode='w'))
    sys.exit()


if __name__ == '__main__':
    main()
