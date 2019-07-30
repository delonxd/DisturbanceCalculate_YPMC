from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.GUI.TreeParameter import *
from src.GUI.TreeElement import *
from src.Model.TestModel import *


# 模型窗口
class WindowModel(QDialog):
    def __init__(self, model):
        super().__init__()
        self.resize(1024, 768)
        self.setWindowTitle('矩阵模型窗口')

        self.model = model
        self.tree = TreeElement(self.model)
        # self.window1 = ShowText()
        self.window2 = TreeParameter()

        hbox = QHBoxLayout()
        hbox.addWidget(self.tree, 1)
        hbox.addWidget(self.window2, 3)

        # layout.addWidget(window1)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        button1 = QPushButton('计算')
        button2 = QPushButton('关闭')
        hbox2.addWidget(button1)
        hbox2.addWidget(button2)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)

        # self.tree.sendmsg.connect(self.window1.print_name)
        self.tree.sendmsg.connect(self.window2.show_dict)
        button1.clicked.connect(self.tree.test_slot)
        button2.clicked.connect(self.close)