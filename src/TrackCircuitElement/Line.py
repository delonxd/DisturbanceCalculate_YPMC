from src.TrackCircuitElement.Rail import *
from src.TrackCircuitElement.JumperWires import *


# 线路
class Line(ElePack):
    def __init__(self, name_base, parameter, parent_ins=None,
                 sec_group=None, rail_group=None, train=None):
        super().__init__(parent_ins, name_base)
        self.parameter = parameter
        self.posi_abs = 0
        if rail_group is not None:
            self.rail_group = rail_group
            self.rail_group.set_parent_line(self)
        else:
            self.rail_group = RailGroup(parent_ins=self, name_base='钢轨',
                                        parameter=self.parameter)
        if sec_group is not None:
            self.add_child(sec_group.name_base, sec_group)
            sec_group.parent_ins = self
        if train is not None:
            self.add_child(train.name_base, train)
            train.parent_ins = self

    # def add_element(self, name, instance):
    #     self.element[name] = instance
    #     instance.parent_ins = self

    def refresh(self):
        self.get_ele_set(ele_set=set())
        self.set_ele_name(prefix='')


class Turnout(Line):
    def __init__(self, name_base, parameter, main_line, posi1, posi2,
                 parent_ins=None, sec_group=None, rail_group=None, train=None):
        super().__init__(name_base, parameter,
                         parent_ins=parent_ins, sec_group=sec_group,
                         rail_group=rail_group, train=train)
        self.main_line = main_line
        self.posi1 = posi1
        self.posi2 = posi2
        self.jumper_interval = 20
        self.jumper_list = []
        self.add_jumpers()

    def add_jumpers(self):
        posi_list = self.get_jumper_posi()
        m_line = self.main_line
        turnout = self
        for num in range(len(posi_list)):
            posi = posi_list[num]
            name_base = '跳线' + str(num+1)
            jumper = JumperWireConnection(name_base, m_line, turnout, posi)
            self.jumper_list.append(jumper)

    def get_jumper_posi(self,):
        interval = self.jumper_interval
        p1 = self.posi1
        p2 = self.posi2
        if p1 < p2:
            posi_list = list(np.arange(p1, p2, interval))
        else:
            posi_list = list(np.arange(p1, p2, -interval))
        return posi_list
