import numpy as np
import numpy.matlib
from src.Model.SingleLineModel import *
from src.TrackCircuitElement.Line import Line, Turnout
from src.TrackCircuitElement.JumperWires import *


class MainModel(ElePack):
    def __init__(self, line_group, md):
        super().__init__(None, line_group.name_base)
        # u_list = [45, 37.5, 30, 22.5]
        u_list = [183, 164, 142, 115, 81.5, 68, 60.5, 48.6, 40.8]
        self.pwr_U = u_list[int(md.parameter['level'])-1]
        self.freq = md.parameter['freq']

        self.line_group = line_group
        self.jumper_dict = dict()
        self.init_model()
        # self.ele_set = set()
        self.equs = self.get_equs_kirchhoff()
        self.varbs = self.equs.get_varbs()
        self.varbs.config_varb_num()
        self.matrx, self.cons = self.config_matrix()

        self.equ = self.equs.equ_dict['线路组_线路3_地面_区段1_左调谐单元_1发送器_1电压源_方程']
        num = self.equs.equs.index(self.equ)
        self.cons[num] = self.pwr_U
        print(len(self.cons))

        for value in self.cons:
            # print(value)
            pass

        # 结果
        self.value_c = np.linalg.solve(self.matrx, self.cons)
        # print(self.value_c)

        # for posi in self.element['线路1'].node_dict.keys():
        #     if posi >= 0:
        #         num = self.element['线路1'].node_dict[posi].l_track['U2'].num
        #         value = abs(self.value_c[num])
        #         # print(value)

        self.set_varbs_value()

    def set_varbs_value(self):
        for varb in self.varbs.varb_set:
            varb.value = self.value_c[varb.num]
            varb.value_c = abs(self.value_c[varb.num])

    def config_matrix(self):
        length = len(self.equs)
        matrix_main = np.matlib.zeros((length, length), dtype=complex)
        constant = np.zeros(length, dtype=complex)

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
            equs.add_equations(self.get_equ_unit(line_model, self.freq))
            # print(len(equs))
            equs.add_equations(self.get_equ_kcl(line_model))
            # print(len(equs))
            equs.add_equations(self.get_equ_kvl(line_model))
            # print(len(equs))
        for jumper in self.jumper_dict.values():
            equs.add_equations(jumper.get_equs())
        return equs

    # 元器件方程
    @staticmethod
    def get_equ_unit(line_model, freq):
        equs = EquationGroup()
        ele_set = line_model.get_ele_set(ele_set=set())
        for ele in ele_set:
            for module in ele.md_list:
                equs.add_equations(module.get_equs(freq))
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
                equ.add_items(EquItem(vb, -1))
            equs.add_equation(equ)
        return equs
