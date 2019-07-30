from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.AbstractClass.ElePack import *


# 元素树节点
class TreeItemElement(QTreeWidgetItem):
    def __init__(self, parent, vessel, key):
        super().__init__(parent)
        self.vessel = vessel
        self.key = key
        self.add_tree_item()
        self.refresh_text()
        self.setExpanded(True)

    # 添加子节点
    def add_tree_item(self):
        vessel = self.vessel[self.key]
        if hasattr(vessel, 'element'):
            for key, value in vessel.element.items():
                TreeItemElement(parent=self, vessel=vessel, key=key)

    # 刷新显示
    def refresh_text(self):
        self.setText(0, self.key)
        count = self.childCount()
        for index in range(count):
            item = self.child(index)
            item.refresh_text()