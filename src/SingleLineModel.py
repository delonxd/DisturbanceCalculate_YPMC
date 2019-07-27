from src.ElePack import *
from src.SubRailPi import *


class Node:
    def __init__(self, posi):
        self.posi = posi
        self.element = dict()
        self.track = [None, None]

class SingleLineModel(ElePack):
    def __init__(self, parent_ins, line):
        super().__init__(parent_ins, line.name_base)
        self.name = line.name
        self.line = line
        self['元件'] = ElePack(self, '元件')
        self['钢轨'] = ElePack(self, '钢轨')

        self.posi_line = None
        self.node_dict = dict()
        self.var_set = set()
        self.get_model_element()
        print(line.name)

    # 获得矩阵模型的元件
    def get_model_element(self):
        self.get_posi_line()
        self['元件'].element = self.choose_element(self.line.ele_set, self.posi_line)
        self['钢轨'].element = self.set_sub_rail(self.posi_line)
        self['钢轨'].set_ele_name(prefix='')
        self.set_node_dict()
        self.link_track_ele()
        self.var_set = self.get_varb(varb_set=set())

    # 获得钢轨分割点位置（参数：全局元件及位置、线路元件）
    def get_posi_line(self, ftype='元件'):
        posi_global = self.get_posi_fast(self.parent_ins.line_group.ele_set)
        posi_self_ele = self.get_posi_fast(self.line.ele_set)
        posi_rail = self.line.rail_group.posi_list
        if ftype == '元件':
            rg = [posi_self_ele[0], posi_self_ele[-1]]
            if posi_self_ele[0] < posi_rail[0] or posi_self_ele[-1] > posi_rail[-1]:
                raise KeyboardInterrupt('钢轨范围异常')
        elif ftype == '钢轨':
            rg = [posi_rail[0], posi_rail[-1]]
        self.posi_line = self.sort_posi_list(list(filter(lambda posit: rg[0] <= posit <= rg[-1], posi_global)))
        print(self.posi_line)
        return self.posi_line

    def set_sub_rail(self, posi_all):
        sub_rail_list = list()
        sub_rail_dict = dict()
        for num in range(len(posi_all) - 1):
            l_posi = posi_all[num]
            r_posi = posi_all[num+1]
            z_trk = None
            rd = None
            for ele in self.line.rail_group.rail_list:
                if l_posi >= ele.l_posi and r_posi <= ele.r_posi:
                    z_trk = ele.ztrk
                    rd = ele.rd
            sub_rail_dict['钢轨段'+str(num+1)] = SubRailPi(self.line, '钢轨段'+str(num+1),
                                                        l_posi=l_posi, r_posi=r_posi,
                                                        z_trk=z_trk, rd=rd)
            sub_rail_list.append(sub_rail_dict['钢轨段'+str(num+1)])

        return sub_rail_dict

    # 获得模型的节点
    def set_node_dict(self):
        self.node_dict.clear()
        for posi in self.posi_line:
            self.node_dict[posi] = Node(posi)
        for ele in self['元件'].values():
            self.node_dict[ele.posi_abs].element[ele.name] = ele
        for ele in self['钢轨'].values():
            self.node_dict[ele.l_posi].track[1] = ele
            self.node_dict[ele.r_posi].track[0] = ele

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

