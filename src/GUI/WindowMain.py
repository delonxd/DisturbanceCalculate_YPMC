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
    def __init__(self, line_group, md):
        super().__init__()
        self.resize(1280, 900)
        self.setWindowTitle('轨道电路传输计算Demo')

        self.line_group = line_group
        self.md = md

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
        self.model = MainModel(self.line_group, self.md)
        self.model_window = WindowModel(self.model)

        print(len(self.model.equs))
        self.model_window.exec()


if __name__ == '__main__':
    print(time.asctime(time.localtime()))
    app = QApplication(sys.argv)

    #读取参数
    df = pd.read_excel('../Input/襄阳动车所输入参数_有道岔版.xlsx', header=None)

    sec_num = 1
    num = 2
    output = 8 * [0]
    row = 2 * num + 2
    freq = df.loc[row, 3]
    length = df.loc[row, 4]
    turnout_num = df.loc[row, 5]
    turnout_list = []
    if turnout_num > 0:
        p1 = length - df.loc[row, 6]
        p2 = length - df.loc[row, 7]
        turnout_list.append((p1, p2))
    if turnout_num == 2:
        p1 = length - df.loc[row, 9]
        p2 = length - df.loc[row, 10]
        turnout_list.append((p1, p2))

    c_num = df.loc[row, 19]
    level = df.loc[row, 20]
    cab_len = df.loc[row, 14]

    md = TestModel(freq=freq,
                   length=length,
                   c_num=c_num,
                   level=level,
                   rd=10000,
                   r_cable=43,
                   cab_len=cab_len,
                   turnout_list=turnout_list)

    main = WindowMain(md.lg, md)
    main.show()
    sys.exit(app.exec_())
