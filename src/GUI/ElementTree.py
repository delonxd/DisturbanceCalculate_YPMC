from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


from src.AbstractClass.ElePack import *


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
    sendmsg = pyqtSignal(ElePack)

    def __init__(self, vessel):
        super().__init__()
        self.vessel = vessel
        self.setHeaderLabel('列表')

        # 子元素初始化
        root = ElementTreeItem(parent=self, vessel=self.vessel)
        root.setText(0, root.vessel.name)

        # 设置水平滚动条
        header = self.header()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(False)

        # self.setMouseTracking(True)
        # self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.setSectionResizeMode
        # self.setExpandsOnDoubleClick(False)

        # 单击发送容器对象
        self.clicked.connect(self.emit_vessel)

    def emit_vessel(self, index):
        item = self.currentItem()
        self.sendmsg.emit(item.vessel)
