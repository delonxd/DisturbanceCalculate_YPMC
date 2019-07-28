from src.Rail import *


# 线路
class Line(ElePack):
    def __init__(self, name_base, parameter, parent_ins=None,
                 sec_group=None, rail_group=None, train=None):
        super().__init__(parent_ins, name_base)
        self.parameter = parameter
        if rail_group is not None:
            self.rail_group = rail_group
            self.rail_group.set_parent_line(self)
        else:
            self.rail_group = RailGroup(parent_ins=self, name_base='钢轨',
                                        parameter=self.parameter)
        if sec_group is not None:
            self.add_element(sec_group.name_base, sec_group)
        if train is not None:
            self.add_element(train.name_base, train)

        self.ele_set = self.get_element(ele_set=set())
        self.set_ele_name(prefix='')

    def add_element(self, name, instance):
        self.element[name] = instance
        instance.parent_ins = self
