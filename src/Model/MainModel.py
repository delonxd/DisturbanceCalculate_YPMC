import numpy as np
import numpy.matlib
from src.Model.SingleLineModel import *
from src.TrackCircuitElement.Line import Line
from src.Module.OutsideElement import *
from src.Method import *

from numba import jit
import time


class MainModel(ElePack):
    def __init__(self, line_group, md):
        super().__init__(None, line_group.name_base)
        self.freq = md.parameter['freq']
        self.line_group = line_group
        self.equs = None
        self.varbs = None
        self.module_set = set()
        self.value_c = None
        self.init_model()

        # 获取方程
        self.equs = self.get_equs_kirchhoff()

        # # 化简运算
        # lines = list(self.element.values())
        # nodes_new = combine_node_group(lines)
        #
        # posi_shunt = md.parameter['分路位置']
        #
        # equs_simple = EquationGroup()
        # node_shunt = nodes_new[posi_shunt]
        # equs_simple.add_equations(node_shunt.equs)
        #
        # node_t = nodes_new.left_node(node_shunt)
        # if node_t is not None:
        #     equs_simple.add_equations(node_t.get_left_equs(nodes_new))
        #     for ele in node_shunt.l_track:
        #         equs_simple.add_equations(ele.equs)
        #
        # node_t = nodes_new.right_node(node_shunt)
        # if node_t is not None:
        #     equs_simple.add_equations(node_t.get_right_equs(nodes_new))
        #     for ele in node_shunt.r_track:
        #         equs_simple.add_equations(ele.equs)
        #
        # self.equs = equs_simple

        # self.equs.config_equ_num()
        # self.equs.config_varb_num()
        self.equs.creat_matrix()
        #
        # print(len(self.equs))
        self.equs.solve_matrix()

    # @jit
    def reload_coefficient(self, module_set):
        for module in module_set:
            # if isinstance(module, CapC):
            module.refresh_coeffs(self.freq.value)
            for equ in module.equs.equs:
                row = equ.num[self.equs]
                columns = equ.varbs_num_list[self.equs]
                self.equs.m_matrix[row, columns] = equ.coeff_list

    def init_model(self):
        for ele in self.line_group.values():
            if isinstance(ele, Line):
                self[ele.name_base] = SingleLineModel(self, ele)
        self.config_mutual()
        self.get_ele_set(ele_set=set())

    def config_mutual(self):
        if len(self.element) == 2:
            line1, line2 = list(self.element.values())
            set1 = set(line1.node_dict.keys())
            set2 = set(line2.node_dict.keys())
            node_set = list(set1.intersection(set2))
            node_set.sort()
            for posi in node_set[:-1]:
                line1.node_dict[posi].r_track.mutual_trk = line2.node_dict[posi].r_track
                line2.node_dict[posi].r_track.mutual_trk = line1.node_dict[posi].r_track

    # 获得基尔霍夫电压电流方程
    def get_equs_kirchhoff(self):
        equs = EquationGroup()
        for line_model in self.element.values():
            equs.add_equations(self.get_equ_unit(line_model, self.freq.value))
            equs.add_equations(self.get_equ_kcl(line_model))
            equs.add_equations(self.get_equ_kvl(line_model))
        return equs

    # 元器件方程
    # @staticmethod
    def get_equ_unit(self, line, freq):
        equs = EquationGroup()
        # ele_set = line.get_ele_set(ele_set=set())
        ele_set = line.ele_set
        for ele in ele_set:
            ele.init_equs(freq)
            node = line.node_dict[ele.posi_abs]

            equs.add_equations(ele.equs)
            self.module_set.add(ele)

            if not isinstance(ele, SubRailPi):
                node.equs.add_equations(ele.equs)

            # for module in ele.md_list:
            #     self.module_set.add(module)
            #     module.init_equs(freq)
            #     equs.add_equations(module.equs)
        return equs

    # KCL方程
    @staticmethod
    def get_equ_kcl(line):
        equs = EquationGroup()
        counter = 1
        for posi in line.posi_line:
            node = line.node_dict[posi]

            if node.node_type == 'connected':
                equ_name = line.name + '_节点KCL方程' + str(counter)
                equ = Equation(name=equ_name)
                for ele in node.element.values():
                    equ.add_coeff(varb=ele.md_list[-1].get_varb(-1))
                if node.l_track is not None:
                    equ.add_coeff(varb=node.l_track.get_varb(-1))
                if node.r_track is not None:
                    equ.add_coeff(varb=node.r_track.get_varb(1))
                equs.add_equation(equ)
                node.equs.add_equation(equ)
                counter += 1

            elif node.node_type == 'disconnected':

                # 左边钢轨
                if node.l_track is not None:
                    equ_name = line.name + '_节点KCL方程' + str(counter)
                    equ = Equation(name=equ_name)
                    equ.add_coeff(varb=node.l_track.get_varb(-1))
                    for ele in node.element.values():
                        u_track = node.l_track.get_varb(-2)
                        u_ele = ele.md_list[-1].get_varb(-2)
                        if u_track == u_ele:
                            equ.add_coeff(varb=ele.md_list[-1].get_varb(-1))
                    equs.add_equation(equ)
                    node.equs.add_equation(equ)
                    counter += 1

                # 右边钢轨
                if node.r_track is not None:
                    equ_name = line.name + '_节点KCL方程' + str(counter)
                    equ = Equation(name=equ_name)
                    equ.add_coeff(varb=node.r_track.get_varb(1))
                    for ele in node.element.values():
                        u_track = node.r_track.get_varb(0)
                        u_ele = ele.md_list[-1].get_varb(-2)
                        if u_track == u_ele:
                            equ.add_coeff(varb=ele.md_list[-1].get_varb(-1))
                    equs.add_equation(equ)
                    node.equs.add_equation(equ)
                    counter += 1
        return equs

    # KVL方程
    @staticmethod
    def get_equ_kvl(line):
        equs = EquationGroup()
        posi_line = line.posi_line[1:-1]
        for num in range(len(posi_line)):
            node = line.node_dict[posi_line[num]]
            if node.node_type == 'disconnected':
                continue
            equ_name = line.name + '_节点KVL方程' + str(num+1)
            equ = Equation(name=equ_name)
            if node.l_track is not None:
                equ.add_coeff(varb=node.l_track.get_varb(-2), value=1)
            if node.r_track is not None:
                equ.add_coeff(varb=node.r_track.get_varb(0), value=-1)
            equs.add_equation(equ)
            node.equs.add_equation(equ)
        return equs


if __name__ == '__main__':
    c1 = np.random

    pass