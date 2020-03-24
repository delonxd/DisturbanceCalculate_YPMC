from src.AbstractClass.ElePack import *
from src.Module.SubRail import *
from src.Module.BreakPoint import *
from src.TrackCircuitElement.Train import *

class NodeGroup:
    def __init__(self):
        # self.parent_line = parent_line
        self.node_dict = dict()
        self.group_type = None

    @property
    def posi_list(self):
        posi_list = list(self.node_dict.keys())
        posi_list.sort()
        return posi_list

    @property
    def posi_set(self):
        posi_set = set(self.node_dict.keys())
        return posi_set

    def left_node(self, node):
        posi_list = self.posi_list
        index_num = posi_list.index(node.posi) - 1
        if index_num >= 0:
            return self.node_dict[posi_list[index_num]]
        else:
            return None

    def right_node(self, node):
        posi_list = self.posi_list
        index_num = posi_list.index(node.posi) + 1
        if index_num < len(posi_list):
            return self.node_dict[posi_list[index_num]]
        else:
            return None

    def get_equs(self):
        equs = EquationGroup()
        counter = 0
        for posi in self.posi_list:
            node = self.node_dict[posi]
            equs.add_equations(node.equs)
            if counter == 0:
                counter += 1
                continue
            for ele in node.l_track:
                equs.add_equations(ele.equs)

        return equs

    def __len__(self):
        return len(self.node_dict)

    def __getitem__(self, key):
        return self.node_dict[key]

    def __setitem__(self, key, value):
        self.node_dict[key] = value

    def values(self):
        return self.node_dict.values()

    def keys(self):
        return self.node_dict.keys()

    def items(self):
        return self.node_dict.items()

    def clear(self):
        self.node_dict.clear()

class Node:
    def __init__(self, posi):
        self.node_type = 'connected'
        # self.node_type = 'disconnected'
        self.posi = posi
        self.element = dict()
        self.l_track = None
        self.r_track = None
        self.equs = EquationGroup()

    @property
    def track(self):
        track = [self.l_track, self.r_track]
        return track

    @track.setter
    def track(self, value):
        self.l_track = value[0]
        self.r_track = value[1]

    def get_left_equs(self, node_group):
        if self.r_track is []:
            raise KeyboardInterrupt('空值错误：节点右侧没有钢轨')

        varbs1 = []
        varbs2 = []
        for ele in self.r_track:
            varbs1.append(ele.get_varb(1))
            varbs2.append(ele.get_varb(0))

        equs = EquationGroup()
        equs.add_equations(self.equs)
        for ele in self.l_track:
            equs.add_equations(ele.equs)

        node_left = node_group.left_node(self)
        if node_left is not None:
            equs.add_equations(node_left.get_left_equs(node_group))

        equ_name = str(self.posi) + '左侧'
        equs_new = equs.simplify_equs(varbs1, varbs2, equ_name)

        return equs_new

    def get_right_equs(self, node_group):
        if self.l_track is []:
            raise KeyboardInterrupt('空值错误：节点右侧没有钢轨')

        varbs1 = []
        varbs2 = []
        for ele in self.l_track:
            varbs1.append(ele.get_varb(-1))
            varbs2.append(ele.get_varb(-2))

        equs = EquationGroup()
        equs.add_equations(self.equs)
        for ele in self.r_track:
            equs.add_equations(ele.equs)

        node_right = node_group.right_node(self)
        if node_right is not None:
            equs.add_equations(node_right.get_right_equs(node_group))

        equ_name = str(self.posi) + '右侧'
        equs_new = equs.simplify_equs(varbs1, varbs2, equ_name)

        return equs_new

class SingleLineModel(ElePack):
    def __init__(self, parent_ins, line):
        super().__init__(parent_ins, line.name_base)
        self.name = line.name
        self.line = line
        self['元件'] = ElePack(self, '元件')
        self['钢轨'] = ElePack(self, '钢轨')
        self.ftype = '元件'
        self.posi_line = []
        # self.node_dict = dict()
        self.node_dict = NodeGroup()
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
        flag = self.line.parameter['节点选取模式']

        if flag == '元件':
            if posi_ele[0] < posi_rail[0] or posi_ele[-1] > posi_rail[-1]:
                raise KeyboardInterrupt('钢轨范围异常')
            else:
                rg = [posi_ele[0], posi_ele[-1]]
        elif flag == '钢轨':
            rg = [posi_rail[0], posi_rail[-1]]
        elif flag == '特殊':
            rg = [posi_global[0], posi_global[-1]]
        else:
            raise KeyboardInterrupt('节点设置错误')

        # if self.ftype == '元件':
        #     if posi_ele[0] < posi_rail[0] or posi_ele[-1] > posi_rail[-1]:
        #         raise KeyboardInterrupt('钢轨范围异常')
        #     else:
        #         rg = [posi_ele[0], posi_ele[-1]]
        # elif self.ftype == '钢轨':
        #     rg = [posi_rail[0], posi_rail[-1]]
        #
        # # rg = [posi_global[0], posi_global[-1]]

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
            if isinstance(ele, BreakPoint):
                self.node_dict[ele.posi_abs].node_type = 'disconnected'
            else:
                self.node_dict[ele.posi_abs].element[ele.name] = ele
        for ele in self['钢轨'].values():
            self.node_dict[ele.l_posi].r_track = ele
            self.node_dict[ele.r_posi].l_track = ele

    # 设备和钢轨相连
    def link_track_ele(self):
        for node in self.node_dict.values():
            if node.node_type == 'connected':
                for ele in node.element.values():
                    if node.track[1] is not None:
                        self.equal_varb([ele.md_list[-1], -2], [node.track[1].md_list[0], 0])
                    else:
                        self.equal_varb([ele.md_list[-1], -2], [node.track[0].md_list[0], 2])
            elif node.node_type == 'disconnected':
                for ele in node.element.values():
                    if isinstance(ele.parent_ins, Train):
                        if node.track[1] is not None:
                            self.equal_varb([ele.md_list[-1], -2], [node.track[1].md_list[0], 0])
                        else:
                            self.equal_varb([ele.md_list[-1], -2], [node.track[0].md_list[0], 2])
                    else:
                        if ele.posi_rlt <= 0:
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
