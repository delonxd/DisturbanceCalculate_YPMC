from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.GUI.TreeParameter import *
from src.GUI.TreeElement import *
from src.GUI.WindowModel import *
from src.Model.TestModel import *

import sys
import time


# 主窗口
class WindowMain(QWidget):
    def __init__(self, line_group):
        super().__init__()
        self.resize(1280, 900)
        self.setWindowTitle('轨道电路传输计算Demo')

        self.line_group = line_group
        self.tree = TreeElement(self.line_group)
        # self.window1 = ShowText()
        self.window2 = TreeParameter()

        hbox = QHBoxLayout()
        hbox.addWidget(self.tree, 1)
        hbox.addWidget(self.window2, 3)

        # layout.addWidget(window1)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        button1 = QPushButton('建立模型')
        button2 = QPushButton('关闭')
        hbox2.addWidget(button1)
        hbox2.addWidget(button2)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)

        # self.tree.sendmsg.connect(self.window1.print_name)
        self.tree.sendmsg.connect(self.window2.show_dict)
        button1.clicked.connect(self.modeling)
        button2.clicked.connect(self.close)

    def modeling(self):
        self.model = MainModel(self.line_group)
        self.model_window = WindowModel(self.model)

        print(len(self.model.equs))
        self.model_window.exec()


if __name__ == '__main__':
    print(time.asctime(time.localtime()))
    app = QApplication(sys.argv)

    md = TestModel()

    main = WindowMain(md.lg)
    main.show()
    sys.exit(app.exec_())
