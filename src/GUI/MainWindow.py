from src.GUI.ParameterTree import *
from src.GUI.ElementTree import *

from src.Model.TestModel import *

import sys
import time


class ShowText(QTextEdit):
    def __init__(self):
        super().__init__()
        font = QFont('Time', 14)
        self.setFont(font)

    def print_name(self, vessel):
        self.setText('')
        for item in vessel.__dict__.items():
            self.append(str(item))


class ModelWindow(QDialog):
    def __init__(self, model):
        super().__init__()
        self.resize(600, 480)
        self.setWindowTitle('矩阵模型窗口')

        self.model = model
        self.tree = ElementTree(self.model)
        # self.window1 = ShowText()
        self.window2 = ParameterTree()

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
        # button1.clicked.connect(self.modeling)



class MainWin(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1280, 900)
        self.setWindowTitle('轨道电路传输计算Demo')

        md = TestModel()
        self.line_group = md.line_group
        self.tree = ElementTree(self.line_group)
        # self.window1 = ShowText()
        self.window2 = ParameterTree()

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

    def modeling(self):
        self.model = MainModel(self.line_group)
        self.model_window = ModelWindow(self.model)

        print(len(self.model.equs))
        self.model_window.exec()


if __name__ == '__main__':
    print(time.asctime(time.localtime()))
    app = QApplication(sys.argv)
    main = MainWin()
    main.show()
    sys.exit(app.exec_())
