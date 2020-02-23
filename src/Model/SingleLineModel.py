from src.AbstractClass.ElePack import *
from src.Module.SubRail import *


class Node:
    def __init__(self, posi):
        self.posi = posi
        self.element = dict()
        self.l_track = None
        self.r_track = None

    @property
    def track(self):
        track = [self.l_track, self.r_track]
        return track

    @track.setter
    def track(self, value):
        self.l_track = value[0]
        self.r_track = value[1]


class SingleLineModel(ElePack):
    def __init__(self, parent_ins, line):
        super().__init__(parent_ins, line.name_base)
        self.name = line.name
        self.line = line
        self['元件'] = ElePack(self, '元件')
        self['钢轨'] = ElePack(self, '钢轨')
        self.ftype = '元件'
        self.posi_line = []
        self.node_dict = dict()
        # self.var_set = set()
        self.config_model()

    @property
    def posi_global(self):
        line_group = self.parent_ins.line_group
        posi_global = line_group.get_posi_fast(line_group.ele_set)
        posi_special = self.parent_ins.line_group.special_point
        posi_global.extend(posi_special)
        posi_global = self.sort_posi_list(posi_global)
        return posi_global

    @property
    def posi_ele(self):
        line = self.line
        posi_ele = line.get_posi_fast(line.ele_set)
        return posi_ele

    @property
    def posi_rail(self):
        posi_rail = self.line.rail_group.posi_list
        return posi_rail

    # 获得矩阵模型的元件
    def config_model(self):
        self.get_posi_line()
        self.config_ele()
        self.config_track()
        self.config_node_dict()
        self.link_track_ele()
        # self.var_set = self.get_varb(varb_set=set())

    # 获得钢轨段节点列表
    def get_posi_line(self):
        posi_global = self.posi_global
        posi_ele = self.posi_ele
        posi_rail = self.posi_rail
        if self.ftype == '元件':
            if posi_ele[0] < posi_rail[0] or posi_ele[-1] > posi_rail[-1]:
                raise KeyboardInterrupt('钢轨范围异常')
            else:
                rg = [posi_ele[0], posi_ele[-1]]
        elif self.ftype == '钢轨':
            rg = [posi_rail[0], posi_rail[-1]]
        posi_line = self.sort_posi_list(list(filter(lambda posit: rg[0] <= posit <= rg[-1], posi_global)))
        self.posi_line = posi_line
        return posi_line

    # 设置元件
    def config_ele(self):
        self['元件'].element = self.choose_element(self.line.ele_set, self.posi_line)

    # 设置钢轨段
    def config_track(self):
        posi_list = self.posi_line
        # ele_list = list()
        ele_dict = dict()
        rail_list = self.line.rail_group.rail_list
        for num in range(len(posi_list) - 1):
            l_posi, r_posi = posi_list[num], posi_list[num + 1]
            for rail in rail_list:
                if rail.l_posi <= l_posi and r_posi <= rail.r_posi:
                    z_trk, rd = rail.ztrk, rail.rd
                    name = '钢轨段' + str(num+1)
                    ele_dict[name] = SubRailPi(parent_ins=self.line, name_base=name,
                                               l_posi=l_posi, r_posi=r_posi,
                                               z_trk=z_trk, rd=rd)
                    # ele_list.append(ele_dict['钢轨段'+str(num+1)])
                    break
        self['钢轨'].element = ele_dict
        self['钢轨'].set_ele_name(prefix='')

    # 获得模型的节点
    def config_node_dict(self):
        self.node_dict.clear()
        for posi in self.posi_line:
            self.node_dict[posi] = Node(posi)
        for ele in self['元件'].values():
            self.node_dict[ele.posi_abs].element[ele.name] = ele
        for ele in self['钢轨'].values():
            self.node_dict[ele.l_posi].r_track = ele
            self.node_dict[ele.r_posi].l_track = ele

    # 设备和钢轨相连
    def link_track_ele(self):
        for node in self.node_dict.values():
            for ele in node.element.values():
                if node.track[1] is not None:
                    self.equal_varb([ele.md_list[-1], -2], [node.track[1].md_list[0], 0])
                else:
                    self.equal_varb([ele.md_list[-1], -2], [node.track[0].md_list[0], 2])

    # 按位置筛选元件
    @staticmethod
    def choose_element(ele_set, posi_abs):
        ele_dict = dict()
        for ele in ele_set:
            if ele.posi_abs in posi_abs:
                ele_dict[ele.name] = ele
        return ele_dict
