import numpy as np
import numpy.matlib
from src.Model.SingleLineModel import *


class MainModel(ElePack):
    def __init__(self, line_group):
        super().__init__(None, line_group.name_base)
        self.line_group = line_group
        self.init_model()
        self.ele_set = set()
        self.equs = self.get_equs_kirchhoff()
        self.varbs = self.equs.get_varbs()
        self.varbs.config_varb_num()
        self.matrx, self.cons = self.config_matrix()

    def config_matrix(self):
        length = len(self.equs)
        matrix_main = np.matlib.zeros((length, length), dtype=complex)
        constant = [0] * length

        self.equs.sort_by_name()
        equ_list = self.equs.equs
        for row in range(length):
            equ = equ_list[row]
            for item in equ.items:
                column = item.varb.num
                value = item.coefficient
                matrix_main[row, column] = value
            constant[row] = equ.constant
        return matrix_main, constant

    def init_model(self):
        for line in self.line_group.values():
            self[line.name_base] = SingleLineModel(self, line)
        self.config_mutual()
        self.get_ele_set()

    def get_ele_set(self):
        ele_set = self.get_element(ele_set=set())
        self.ele_set = ele_set
        return ele_set

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
            equs.add_equations(self.get_equ_unit(line_model, 1700))
            # print(len(equs))
            equs.add_equations(self.get_equ_kcl(line_model))
            # print(len(equs))
            equs.add_equations(self.get_equ_kvl(line_model))
            # print(len(equs))
        return equs

    # 元器件方程
    @staticmethod
    def get_equ_unit(line_model, freq):
        equs = EquationGroup()
        ele_set = line_model.get_element(ele_set=set())
        for ele in ele_set:
            for module in ele.md_list:
                equs.add_equations(module.get_equs(freq))
            # print(len(equs), ele.name)
        return equs

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
                equ.add_items(EquItem(vb, 1))
            if node.l_track is not None:
                vb = node.l_track.get_varb(-1)
                equ.add_items(EquItem(vb, 1))
            if node.r_track is not None:
                vb = node.r_track.get_varb(1)
                equ.add_items(EquItem(vb, 1))
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
                equ.add_items(EquItem(vb, 1))
            if node.r_track is not None:
                vb = node.r_track.get_varb(0)
                equ.add_items(EquItem(vb, 1))
            equs.add_equation(equ)
        return equs
