from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.ImpedanceParaType import ImpedanceMultiFreq
from src.AbstractClass.ElePack import *
from src.GUI.TreeItemParameter import *


# 参数树控件
class TreeParameter(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.element = None
        self.setColumnCount(2)
        self.setHeaderLabels(['参数名', '值'])
        self.vessel = None

        header = self.header()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(False)
        # self.show_dict()

        # 当前编辑器
        self.current_editor = (None, None, None)
        # 双击开启编辑器
        self.itemDoubleClicked.connect(self.open_editor)
        # 目标改变关闭编辑器
        self.itemSelectionChanged.connect(self.close_editor)

        # self.findItems()

    def show_dict(self, vessel):
        self.clear()
        self.vessel = vessel
        for key in vessel.prop_table.keys():
            TreeItemParameter(parent=self, vessel=vessel, key=key)

    # 激活编辑器
    def open_editor(self, item, column):
        if column == 1:
            self.current_editor = (item, column, item.text(1))
            self.openPersistentEditor(item, column)

    # 关闭编辑器
    def close_editor(self):
        item, column, text = self.current_editor
        if not (item, column, text) == (None, None, None):
            self.closePersistentEditor(item, column=column)
            value_t = item.text(1)
            try:
                flag = item.vessel.set_property(item.key, value_t)
                if flag:
                    self.refresh_text()
                else:
                    item.setText(1, text)
            except Exception as reason:
                print(reason)
                item.setText(1, text)
        self.current_editor = (None, None, None)

    # 回车关闭编辑器
    def keyPressEvent(self, event):
        print(event.key())
        if event.key() == 16777220:
            self.close_editor()

    # 刷新显示
    def refresh_text(self):
        count = self.topLevelItemCount()
        for index in range(count):
            item = self.topLevelItem(index)
            item.refresh_text()



