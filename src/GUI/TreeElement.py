from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from src.AbstractClass.ElePack import *
from src.GUI.TreeItemElement import *
from src.TrackCircuitElement.Section import *


# 元素树控件
class TreeElement(QTreeWidget):
    sendmsg = pyqtSignal(ElePack)

    def __init__(self, vessel):
        super().__init__()
        self.vessel = vessel
        # 子元素初始化
        # for key in vessel.keys():
        for key, _ in vessel.items_by_posi():
            item = TreeItemElement(parent=self, vessel=vessel, key=key)
            self.addTopLevelItem(item)

        self.refresh_text()

        # 设置水平滚动条
        header = self.header()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(False)

        # 单击发送容器对象
        self.clicked.connect(self.on_tree_clicked)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.generate_menu)

    def generate_menu(self, pos):
        # QItemSelection
        # QItemSelectionModel
        item = self.selectionModel().selection().indexes()
        item = self.currentItem()

        screen_pos = self.mapToGlobal(pos)
        y = screen_pos.y()
        screen_pos.setY(y + 23)
        menu = QMenu()
        action1 = menu.addAction('添加')
        action2 = menu.addAction('删除')
        action3 = menu.addAction('编辑')
        action4 = menu.addAction('添加电容')

        action = menu.exec(screen_pos)
        if action == action4:
            parent_ins = item.vessel[item.key]
            if isinstance(parent_ins, Section):
                name = '新增电容'
                if name not in parent_ins.keys():
                    posi = 233.7
                    new_c = CapC(parent_ins=parent_ins, name_base=name,
                                 posi=posi, z=parent_ins.parameter['Ccmp_z'])
                    new_c.set_posi_abs(0)
                    parent_ins[name] = new_c
                    values = parent_ins.values_by_posi()
                    index = values.index(new_c)
                    new_item = TreeItemElement(parent=None, vessel=parent_ins, key=name)
                    item.insertChild(index, new_item)
                    print(item.parent().vessel)
                    # item.parent().refresh_text()
                    self.refresh_text()
                    self.vessel.refresh()
        elif action == action2:
            element = item.vessel[item.key]
            element.parent_ins.element.pop(element.name_base)



        # self.topLevelItem(item)
        # a = item[0].row()
        # print(item, item.vessel[item.key])
        pass




    def on_tree_clicked(self, index):
        item = self.currentItem()
        self.sendmsg.emit(item.vessel[item.key])

    def test_slot(self):
        count = self.topLevelItemCount()
        for index in range(count):
            item = self.topLevelItem(index)
            print(item.vessel.name)

    def refresh_text(self):
        # 名称
        self.setHeaderLabel(self.vessel.name)
        count = self.topLevelItemCount()
        for index in range(count):
            item = self.topLevelItem(index)
            item.refresh_text()

    # 回车关闭编辑器
    def keyPressEvent(self, event):
        print(event.key())
        if event.key() == 16777220:
            self.close_editor()


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

    main = TreeElement(md.lg)
    main.show()
    sys.exit(app.exec_())
