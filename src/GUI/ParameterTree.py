from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from src.ImpedanceParaType import ImpedanceMultiFreq
from src.AbstractClass.ElePack import *


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
        if isinstance(self.vessel, ElePack):
            return self.vessel.get_property(self.key)
        elif isinstance(self.vessel, (dict, ImpedanceMultiFreq)):
            return self.vessel[self.key]
        else:
            return None

    def init_child(self):
        value = self.value
        self.setText(0, str(self.key))
        if isinstance(value, (dict, ImpedanceMultiFreq)):
            for key in value.keys():
                ParameterTreeItem(parent=self, vessel=value, key=key)
        else:
            self.setText(1, str(value))


class ParameterTree(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.element = None
        self.setColumnCount(2)
        self.setHeaderLabels(['参数名', '值'])

        header = self.header()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(False)
        # self.show_dict()

        # 当前编辑器
        self.current_editor = (None, None)
        # 双击开启编辑器
        self.itemDoubleClicked.connect(self.open_editor)
        # 目标改变关闭编辑器
        self.itemSelectionChanged.connect(self.close_editor)

    def show_dict(self, vessel):
        self.clear()
        for key in vessel.prop_table.keys():
            ParameterTreeItem(parent=self, vessel=vessel, key=key)

    # 激活编辑器
    def open_editor(self, item, column):
        if column == 1:
            self.current_editor = (item, column)
            self.openPersistentEditor(item, column)

    # 关闭编辑器
    def close_editor(self):
        item, column = self.current_editor
        if not (item, column) == (None, None):
            key = item.key
            vessel = item.vessel
            text = item.text(1)
            self.closePersistentEditor(item, column=column)
            value_t = item.text(1)
            flag = vessel.set_property(key, value_t)
            if flag is False:
                item.setText(1, text)
        self.current_editor = (None, None)

    # 回车关闭编辑器
    def keyPressEvent(self, event):
        if event.key() == 16777220:
            self.close_editor()