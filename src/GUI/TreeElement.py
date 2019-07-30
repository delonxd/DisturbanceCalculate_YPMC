from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from src.AbstractClass.ElePack import *
from src.GUI.TreeItemElement import *


# 元素树控件
class TreeElement(QTreeWidget):
    sendmsg = pyqtSignal(ElePack)

    def __init__(self, vessel):
        super().__init__()
        self.vessel = vessel

        # 名称
        self.setHeaderLabel(vessel.name)
        # 子元素初始化
        for key in vessel.keys():
            TreeItemElement(parent=self, vessel=vessel, key=key)

        # 设置水平滚动条
        header = self.header()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(False)

        # 单击发送容器对象
        self.clicked.connect(self.emit_vessel)

    def emit_vessel(self, index):
        item = self.currentItem()
        self.sendmsg.emit(item.vessel[item.key])

    def test_slot(self):
        count = self.topLevelItemCount()
        for index in range(count):
            item = self.topLevelItem(index)
            print(item.vessel.name)

    def refresh_text(self):
        self.setText(0, self.vessel.name)
        count = self.topLevelItemCount()
        for index in range(count):
            item = self.topLevelItem(index)
            item.refresh_text()


if __name__ == '__main__':
    from src.Model.TestModel import *
    import sys
    import time

    # 显示当前时间
    print(time.asctime(time.localtime()))

    # 载入测试模型
    md = TestModel()

    # 运行GUI
    app = QApplication(sys.argv)

    main = TreeElement(md.line_group)
    main.show()
    sys.exit(app.exec_())
