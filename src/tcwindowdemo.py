from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src import TrackCircuitCalculator3 as tcc
import sys
import time

class ElementTreeItem(QTreeWidgetItem):
    def __init__(self, parent=None, vessel=None):
        super().__init__(parent)
        self.vessel = vessel

    def add_tree_item(self):
        if hasattr(self.vessel, 'element'):
            for key, value in self.vessel.element.items():
                child = ElementTreeItem(self, value)
                child.setText(0, key)
                child.add_tree_item()

#
# class
#


class ElementTree(QTreeWidget):
    sendmsg = pyqtSignal(tcc.ElePack)
    def __init__(self, vessel):
        super().__init__()
        self.vessel = vessel
        self.setHeaderLabel('列表')

        root = ElementTreeItem(parent=self, vessel=self.vessel)
        root.add_tree_item()
        root.setText(0, root.vessel.name)

        self.clicked.connect(self.return_vessel)

    def return_vessel(self, index):
        item = self.currentItem()
        # child = QTreeWidgetItem(self)
        # child.setText(0, 'adads')
        print(item.vessel.name)
        self.sendmsg.emit(item.vessel)

    def refresh(self):
        pass

class Showlist(QTextEdit):
    def __init__(self):
        super().__init__()
        font = QFont('Time', 14)
        self.setFont(font)

    def print_name(self, vessel):
        self.setText('')
        if isinstance(vessel, (tcc.Section, tcc.TCSR, tcc.TcsrBA)):
            prop = vessel.get_property()
            for key, value in prop.items():
                self.append(key + ': ' + str(value))
        else:
            for item in vessel.__dict__.items():
                self.append(str(item))

class MainWin(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle('轨道电路传输计算Demo')
        hbox = QHBoxLayout()

        sg1 = tcc.SectionGroup(name_base='地面', posi=0, m_num=3, freq1=2600,
                           m_length=[480, 500, 320],
                           j_length=[29, 29, 29, 29],
                           m_type=['2000A', '2000A', '2000A'],
                           c_num=[6, 6, 5])

        sg2 = tcc.SectionGroup(name_base='地面', posi=0, m_num=2, freq1=1700,
                           m_length=[480, 200, 320],
                           j_length=[29, 29, 29, 29],
                           m_type=['2000A', '2000A', '2000A'],
                           c_num=[8, 6, 5])
        train1 = tcc.Train(parent_ins=None, name_base='列车1', posi_abs=0)
        # 生成线路
        l1 = tcc.Line(name_base='线路1', sec_group=sg1, train=train1)
        l2 = tcc.Line(name_base='线路2', sec_group=sg2)
        lg = tcc.LineGroup(l1, l2, name_base='线路组')

        tree = ElementTree(lg)
        window1 = Showlist()
        hbox.addWidget(tree)
        layout = QVBoxLayout()
        layout.addWidget(QLineEdit())
        layout.addWidget(window1)
        hbox.addLayout(layout)

        self.setLayout(hbox)

        tree.sendmsg.connect(window1.print_name)


if __name__ == '__main__':
    print(time.asctime(time.localtime()))
    app = QApplication(sys.argv)
    main = MainWin()
    main.show()
    sys.exit(app.exec_())
