from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.ImpedanceParaType import ImpedanceMultiFreq
from src.AbstractClass.ElePack import *


# 参数树节点
class TreeItemParameter(QTreeWidgetItem):
    def __init__(self, parent, vessel, key):
        super().__init__(parent)
        self.vessel = vessel
        self.key = key
        self.add_tree_item()
        self.setExpanded(True)
        self.refresh_text()

    @property
    def value(self):
        if isinstance(self.vessel, ElePack):
            return self.vessel.get_property(self.key)
        elif isinstance(self.vessel, (dict, ImpedanceMultiFreq)):
            return self.vessel[self.key]
        else:
            return None

    # 添加子节点
    def add_tree_item(self):
        value = self.value
        if isinstance(value, (dict, ImpedanceMultiFreq)):
            for key in value.keys():
                TreeItemParameter(parent=self, vessel=value, key=key)

    # 刷新显示
    def refresh_text(self):
        value = self.value
        self.setText(0, str(self.key))
        if isinstance(value, (dict, ImpedanceMultiFreq)):
            pass
        else:
            self.setText(1, str(value))
        count = self.childCount()
        for index in range(count):
            item = self.child(index)
            item.refresh_text()
