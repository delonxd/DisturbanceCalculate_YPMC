from src.ElePack import *


class LineGroup(ElePack):
    def __init__(self, *lines, name_base=''):
        super().__init__(None, name_base)
        self.ele_set = set()
        for line in lines:
            line.parent_ins = self
            self.element[line.name_base] = line
            self.ele_set.update(line.ele_set)
        self.set_ele_name(prefix='')
