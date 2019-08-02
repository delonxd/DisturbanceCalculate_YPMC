from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.AbstractClass.ElePack import *


# 元素树节点
class TreeItemElement(QTreeWidgetItem):
    def __init__(self, parent, vessel, key):
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.vessel = vessel
        self.key = key
        self.setExpanded(True)
        self.add_tree_item()
        self.refresh_text()

    # 添加子节点
    def add_tree_item(self):
        vessel = self.vessel[self.key]
        if vessel.flag_ele_unit is True:
            self.setExpanded(False)
        if hasattr(vessel, 'element'):
            # for key, value in vessel.element.items():
            for key, value in vessel.items_by_posi():
                TreeItemElement(parent=self, vessel=vessel, key=key)

    # 刷新显示
    def refresh_text(self):
        self.setText(0, self.key)
        count = self.childCount()
        for index in range(count):
            item = self.child(index)
            item.refresh_text()