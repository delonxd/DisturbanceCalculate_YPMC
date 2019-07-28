from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import src.TrackCircuitCalculator3 as tcc
import sys
import time


class ParameterTreeItem(QTreeWidgetItem):
    def __init__(self, parent, vessel, key):
        super().__init__(parent)
        self.vessel = vessel
        self.key = key
        self.init_child()
        self.setExpanded(True)
        # for child in self.takeChildren():
        #     self.removeChild(child)

    @property
    def value(self):
        if isinstance(self.vessel, tcc.ElePack):
            return self.vessel.get_property(self.key)
        elif isinstance(self.vessel, (dict, tcc.pc.ParaMultiF)):
            return self.vessel[self.key]
        else:
            return None

    @value.setter
    def value(self, text):
        if isinstance(self.vessel, tcc.ElePack):
            self.vessel.set_property(self.key, text)
        # elif isinstance(self.vessel, (dict, tcc.pc.ParaMultiF)):
        #     if self.vessel[self.key] = value
        pass

    def init_child(self):
        value = self.value
        self.setText(0, str(self.key))
        if isinstance(value, (dict, tcc.pc.ParaMultiF)):
            for key in value.keys():
                ParameterTreeItem(parent=self,vessel=value,key=key)
        else:
            self.setText(1, str(value))


class ParameterTree(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.element = None
        self.setColumnCount(2)
        self.setHeaderLabels(['参数名', '值'])
        # self.show_dict()

        self.current_editor = (None, None)

        self.itemDoubleClicked.connect(self.open_editor)
        self.itemSelectionChanged.connect(self.close_editor)
        self.itemSelectionChanged.connect(self.test_slot)

    def show_dict(self, vessel):
        self.clear()
        for key in vessel.prop_table.keys():
            ParameterTreeItem(parent=self, vessel=vessel, key=key)



    def open_editor(self, item, column):
        if column == 1:
            self.current_editor = (item, column)
            self.openPersistentEditor(item, column)

    def close_editor(self):
        item, column = self.current_editor
        if not (item, column) == (None, None):
            value = item.value
            text = item.text(1)
            self.closePersistentEditor(item, column)
            if isinstance(value, str):
                item.value = item.text(1)
            else:
                item.setText(1, text)
        self.current_editor = (None, None)

    def keyPressEvent(self, event):
        if event.key() == 16777220:
            self.close_editor()

    def test_slot(self):
        item = self.currentItem()
        # print(item.text(1))



class ElementTreeItem(QTreeWidgetItem):
    def __init__(self, parent=None, vessel=None):
        super().__init__(parent)
        self.vessel = vessel
        self.add_tree_item()

    def add_tree_item(self):
        if hasattr(self.vessel, 'element'):
            for key, value in self.vessel.element.items():
                child = ElementTreeItem(self, value)
                child.setText(0, key)


class ElementTree(QTreeWidget):
    sendmsg = pyqtSignal(tcc.ElePack)

    def __init__(self, vessel):
        super().__init__()
        self.vessel = vessel
        self.setHeaderLabel('列表')
        root = ElementTreeItem(parent=self, vessel=self.vessel)
        root.setText(0, root.vessel.name)

        # self.setMouseTracking(True)

        self.current_editor = (None, None)

        # self.setExpandsOnDoubleClick(False)

        self.clicked.connect(self.emit_vessel)

        self.itemDoubleClicked.connect(self.open_editor)
        self.itemSelectionChanged.connect(self.close_editor)

        # self.expanded.connect(self.test_slot)

    def emit_vessel(self, index):
        item = self.currentItem()
        self.sendmsg.emit(item.vessel)

    def open_editor(self, item, column):
        self.current_editor = (item, column)
        self.openPersistentEditor(item, column)

    def close_editor(self):
        item, column = self.current_editor
        if not (item, column) == (None, None):
            self.closePersistentEditor(item, column)
        self.current_editor = (None, None)

    def keyPressEvent(self, event):
        print(event.text())
        if event.key() == 16777220:
            self.close_editor()

    def test_slot(self, item):
        print(item)


    def refresh(self):
        pass


class ShowText(QTextEdit):
    def __init__(self):
        super().__init__()
        font = QFont('Time', 14)
        self.setFont(font)

    def print_name(self, vessel):
        self.setText('')
        # if isinstance(vessel, (tcc.Section, tcc.TCSR, tcc.TcsrBA)):
        #     prop = vessel.get_property()
        #     for key, value in prop.items():
        #         self.append(key + ': ' + str(value))
        # else:
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
                               c_num=[6, 6, 5],
                               parameter=tcc.TCSR_2000A)

        sg2 = tcc.SectionGroup(name_base='地面', posi=0, m_num=2, freq1=1700,
                               m_length=[480, 200, 320],
                               j_length=[29, 29, 29, 29],
                               m_type=['2000A', '2000A', '2000A'],
                               c_num=[8, 6, 5],
                               parameter=tcc.TCSR_2000A)
        train1 = tcc.Train(name_base='列车1', posi_abs=0, parameter=tcc.TCSR_2000A)
        # 生成线路
        l1 = tcc.Line(name_base='线路1', sec_group=sg1, train=train1,
                      parameter=tcc.TCSR_2000A)
        l2 = tcc.Line(name_base='线路2', sec_group=sg2,
                      parameter=tcc.TCSR_2000A)
        lg = tcc.LineGroup(l1, l2, name_base='线路组')

        tree = ElementTree(lg)
        window1 = ShowText()
        window2 = ParameterTree()
        hbox.addWidget(tree, 1)
        layout = QVBoxLayout()
        # layout.addWidget(window1)
        layout.addWidget(window2)

        hbox.addLayout(layout, 3)

        self.setLayout(hbox)

        tree.sendmsg.connect(window1.print_name)
        tree.sendmsg.connect(window2.show_dict)


if __name__ == '__main__':
    print(time.asctime(time.localtime()))
    app = QApplication(sys.argv)
    main = MainWin()
    main.show()
    sys.exit(app.exec_())
