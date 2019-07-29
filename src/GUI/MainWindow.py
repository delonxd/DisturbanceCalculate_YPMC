from src.GUI.ParameterTree import *
from src.GUI.ElementTree import *

from src.Model.TestModel import *
# from src.ImpedanceParaType import ImpedanceMultiFreq
# from src.AbstractClass.ElePack import *

import sys
import time

# class ParameterTreeItem(QTreeWidgetItem):
#     def __init__(self, parent, vessel, key):
#         super().__init__(parent)
#         self.vessel = vessel
#         self.key = key
#         self.init_child()
#         self.setExpanded(True)
#         # for child in self.takeChildren():
#         #     self.removeChild(child)
#
#     @property
#     def value(self):
#         if isinstance(self.vessel, ElePack):
#             return self.vessel.get_property(self.key)
#         elif isinstance(self.vessel, (dict, ImpedanceMultiFreq)):
#             return self.vessel[self.key]
#         else:
#             return None
#
#     # @value.setter
#     # def value(self, text):
#     #     if isinstance(self.vessel, ElePack):
#     #         self.vessel.set_property(self.key, text)
#     #     # elif isinstance(self.vessel, (dict, tcc.pc.ParaMultiF)):
#     #     #     if self.vessel[self.key] = value
#     #     pass
#
#     def init_child(self):
#         value = self.value
#         self.setText(0, str(self.key))
#         if isinstance(value, (dict, ImpedanceMultiFreq)):
#             for key in value.keys():
#                 ParameterTreeItem(parent=self, vessel=value, key=key)
#         else:
#             self.setText(1, str(value))
#
#
# class ParameterTree(QTreeWidget):
#     def __init__(self):
#         super().__init__()
#         self.element = None
#         self.setColumnCount(2)
#         self.setHeaderLabels(['参数名', '值'])
#
#         header = self.header()
#         header.setSectionResizeMode(QHeaderView.ResizeToContents)
#         header.setStretchLastSection(False)
#         # self.show_dict()
#
#         # 当前编辑器
#         self.current_editor = (None, None)
#         # 双击开启编辑器
#         self.itemDoubleClicked.connect(self.open_editor)
#         # 目标改变关闭编辑器
#         self.itemSelectionChanged.connect(self.close_editor)
#
#     def show_dict(self, vessel):
#         self.clear()
#         for key in vessel.prop_table.keys():
#             ParameterTreeItem(parent=self, vessel=vessel, key=key)
#
#     # 激活编辑器
#     def open_editor(self, item, column):
#         if column == 1:
#             self.current_editor = (item, column)
#             self.openPersistentEditor(item, column)
#
#     # 关闭编辑器
#     def close_editor(self):
#         item, column = self.current_editor
#         if not (item, column) == (None, None):
#             key = item.key
#             vessel = item.vessel
#             text = item.text(1)
#             self.closePersistentEditor(item, column=column)
#             value_t = item.text(1)
#             flag = vessel.set_property(key, value_t)
#             if flag is False:
#                 item.setText(1, text)
#         self.current_editor = (None, None)
#
#     # 回车关闭编辑器
#     def keyPressEvent(self, event):
#         if event.key() == 16777220:
#             self.close_editor()
#

# class ElementTreeItem(QTreeWidgetItem):
#     def __init__(self, parent=None, vessel=None):
#         super().__init__(parent)
#         self.vessel = vessel
#         self.add_tree_item()
#
#     def add_tree_item(self):
#         if hasattr(self.vessel, 'element'):
#             for key, value in self.vessel.element.items():
#                 child = ElementTreeItem(self, value)
#                 child.setText(0, key)
#
#
# class ElementTree(QTreeWidget):
#     sendmsg = pyqtSignal(ElePack)
#
#     def __init__(self, vessel):
#         super().__init__()
#         self.vessel = vessel
#         self.setHeaderLabel('列表')
#
#         # 子元素初始化
#         root = ElementTreeItem(parent=self, vessel=self.vessel)
#         root.setText(0, root.vessel.name)
#
#         # 设置水平滚动条
#         header = self.header()
#         header.setSectionResizeMode(QHeaderView.ResizeToContents)
#         header.setStretchLastSection(False)
#
#         # self.setMouseTracking(True)
#         # self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
#         # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
#         # self.setSectionResizeMode
#         # self.setExpandsOnDoubleClick(False)
#
#         # 单击发送容器对象
#         self.clicked.connect(self.emit_vessel)
#
#     def emit_vessel(self, index):
#         item = self.currentItem()
#         self.sendmsg.emit(item.vessel)


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
