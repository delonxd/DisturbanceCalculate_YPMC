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


class MainWin(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1280, 900)
        self.setWindowTitle('轨道电路传输计算Demo')

        md = TestModel()

        tree = ElementTree(md.line_group)
        window1 = ShowText()
        window2 = ParameterTree()

        hbox = QHBoxLayout()
        hbox.addWidget(tree, 1)
        hbox.addWidget(window2, 3)

        # layout.addWidget(window1)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(QPushButton('计算'))
        hbox2.addWidget(QPushButton('关闭'))

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)

        tree.sendmsg.connect(window1.print_name)
        tree.sendmsg.connect(window2.show_dict)


if __name__ == '__main__':
    print(time.asctime(time.localtime()))
    app = QApplication(sys.argv)
    main = MainWin()
    main.show()
    sys.exit(app.exec_())
