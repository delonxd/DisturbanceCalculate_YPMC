from src.AbstractClass.ElePack import *


class LineGroup(ElePack):
    def __init__(self, *lines, name_base=''):
        super().__init__(None, name_base)
        for line in lines:
            line.parent_ins = self
            # self.element[line.name_base] = line
            self.add_child(line.name_base, line)
        self.refresh()

    def refresh(self):
        self.get_ele_set(ele_set=set())
        self.set_ele_name(prefix='')
