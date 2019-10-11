import numpy as np
import numpy.matlib
from src.Model.SingleLineModel import *
from src.TrackCircuitElement.Line import Line, Turnout
from src.TrackCircuitElement.JumperWires import *
from src.Module.OutsideElement import *

from numba import jit
import time


class MainModel(ElePack):
    def __init__(self, line_group, md):
        super().__init__(None, line_group.name_base)
        # u_list = [45, 37.5, 30, 22.5]
        u_list = [183, 164, 142, 115, 81.5, 68, 60.5, 48.6, 40.8]
        self.pwr_U = u_list[int(md.parameter['level'])-1]
        self.freq = md.parameter['freq']

        self.line_group = line_group
        self.equs = None
        self.varbs = None
        self.module_set = set()
        self.value_c = None

        self.jumper_dict = dict()

        self.init_model()

        self.equs = self.get_equs_kirchhoff()
        self.equs.config_equ_num()
        self.equs.config_varb_num()
        self.equs.creat_matrix()

        self.equ = self.equs.equ_dict['线路组_线路3_地面_区段1_左调谐单元_1发送器_1电压源_方程']
        self.equs.constant[self.equ.num[self.equs]] = self.pwr_U

        self.equs.solve_matrix()

    # @jit
    def reload_coefficient(self, module_set):
        # print(len(module_set))
        count = 0
        for module in module_set:
            # if isinstance(module, CapC):
            module.refresh_coeffs(self.freq.value)
            for equ in module.equs.equs:
                # row = equ.num[self.equs]
                # columns = equ.varbs_num_list[self.equs]
                # self.equs.m_matrix[row, columns] = equ.coeff_list
                # for item in equ.items.items():
                #     column = item[0].num[self.equs]
                #     value = item[1]
                #     self.equs.m_matrix[row, column] = value
                #     count += 1
                pass
        # print(count)

    def init_model(self):
        for ele in self.line_group.values():
            if isinstance(ele, Line):
                self[ele.name_base] = SingleLineModel(self, ele)
            if isinstance(ele, Turnout):
                for jumper in ele.jumper_list:
                    self.jumper_dict[jumper.name_base] = jumper
        # self.config_mutual()
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
            # print(len(equs))
            equs.add_equations(self.get_equ_kcl(line_model))
            # print(len(equs))
            equs.add_equations(self.get_equ_kvl(line_model))
            # print(len(equs))
        for jumper in self.jumper_dict.values():
            equs.add_equations(jumper.get_equs())
        return equs

    # 元器件方程
    # @staticmethod
    def get_equ_unit(self, line_model, freq):
        equs = EquationGroup()
        ele_set = line_model.get_ele_set(ele_set=set())
        for ele in ele_set:
            for module in ele.md_list:
                self.module_set.add(module)
                module.init_equs(freq)
                equs.add_equations(module.equs)
        return equs

    # # 元器件方程
    # # @staticmethod
    # def get_equ_unit(self, line_model, freq):
    #     equs = EquationGroup()
    #     ele_set = line_model.get_ele_set(ele_set=set())
    #     for ele in ele_set:
    #         for module in ele.md_list:
    #             self.module_set.add(module)
    #             equs.add_equations(module.get_equs(freq))
    #     return equs

    # KCL方程
    @staticmethod
    def get_equ_kcl(line):
        equs = EquationGroup()
        for num in range(len(line.posi_line)):
            node = line.node_dict[line.posi_line[num]]
            name = line.name + '_节点KCL方程' + str(num+1)
            equ = Equation(name=name)
            for ele in node.element.values():
                vb = ele.md_list[-1].get_varb(-1)
                equ.varb_list.append(vb)
                equ.coeff_list.append(1)
                # equ.update_items({vb: 1})
            if node.l_track is not None:
                vb = node.l_track.get_varb(-1)
                equ.varb_list.append(vb)
                equ.coeff_list.append(1)
                # equ.update_items({vb: 1})
            if node.r_track is not None:
                vb = node.r_track.get_varb(1)
                equ.varb_list.append(vb)
                equ.coeff_list.append(1)
                # equ.update_items({vb: 1})
            equs.add_equation(equ)
        return equs

    # KVL方程
    @staticmethod
    def get_equ_kvl(line):
        equs = EquationGroup()
        posi_line = line.posi_line[1:-1]
        for num in range(len(posi_line)):
            node = line.node_dict[posi_line[num]]
            name = line.name + '_节点KVL方程' + str(num+1)
            equ = Equation(name=name)
            if node.l_track is not None:
                vb = node.l_track.get_varb(-2)
                equ.varb_list.append(vb)
                equ.coeff_list.append(1)
                # equ.update_items({vb: 1})
            if node.r_track is not None:
                vb = node.r_track.get_varb(0)
                equ.varb_list.append(vb)
                equ.coeff_list.append(-1)
                # equ.update_items({vb: -1})
            equs.add_equation(equ)
        return equs


    # # KCL方程
    # @staticmethod
    # def get_equ_kcl(line):
    #     equs = EquationGroup()
    #     for num in range(len(line.posi_line)):
    #         node = line.node_dict[line.posi_line[num]]
    #         name = line.name + '_节点KCL方程' + str(num+1)
    #         equ = Equation(name=name)
    #         for ele in node.element.values():
    #             vb = ele.md_list[-1].get_varb(-1)
    #             equ.add_items(EquItem(vb, 1))
    #         if node.l_track is not None:
    #             vb = node.l_track.get_varb(-1)
    #             equ.add_items(EquItem(vb, 1))
    #         if node.r_track is not None:
    #             vb = node.r_track.get_varb(1)
    #             equ.add_items(EquItem(vb, 1))
    #         equs.add_equation(equ)
    #     return equs
    #
    # # KVL方程
    # @staticmethod
    # def get_equ_kvl(line):
    #     equs = EquationGroup()
    #     posi_line = line.posi_line[1:-1]
    #     for num in range(len(posi_line)):
    #         node = line.node_dict[posi_line[num]]
    #         name = line.name + '_节点KVL方程' + str(num+1)
    #         equ = Equation(name=name)
    #         if node.l_track is not None:
    #             vb = node.l_track.get_varb(-2)
    #             equ.add_items(EquItem(vb, 1))
    #         if node.r_track is not None:
    #             vb = node.r_track.get_varb(0)
    #             equ.add_items(EquItem(vb, -1))
    #         equs.add_equation(equ)
    #     return equs


if __name__ == '__main__':
    c1 = np.random

    pass