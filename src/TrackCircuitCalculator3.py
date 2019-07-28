import numpy.matlib
import pickle
import time
from src import ElectricParameter as pc
from matplotlib import pyplot as plt


with open('TCSR_2000A_data_lib.pkl', 'rb') as pk_f:
    TCSR_2000A = pickle.load(pk_f)

TCSR_2000A['Ccmp_z'] = pc.ParaMultiF(1700, 2000, 2300, 2600)
TCSR_2000A['Ccmp_z'].rlc_s = {
    1700: [10e-3, None, 25e-6],
    2000: [10e-3, None, 25e-6],
    2300: [10e-3, None, 25e-6],
    2600: [10e-3, None, 25e-6]}

# 钢轨阻抗
TCSR_2000A['Trk_z'] = pc.ParaMultiF(1700, 2000, 2300, 2600)
TCSR_2000A['Trk_z'].rlc_s = {
    1700: [1.177, 1.314e-3, None],
    2000: [1.306, 1.304e-3, None],
    2300: [1.435, 1.297e-3, None],
    2600: [1.558, 1.291e-3, None]}

TCSR_2000A['Rd'] = 10000
TCSR_2000A['Rsht_z'] = 10e-3

# 载频
FREQ = 2600

from src.SectionGroup import *
from src.Train import *
from src.Line import *
from src.LineGroup import *
from src.SingleLineModel import *


########################################################################################################################

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
            print(len(equs))
            equs.add_equations(self.get_equ_kcl(line_model))
            print(len(equs))
            equs.add_equations(self.get_equ_kvl(line_model))
            print(len(equs))
        return equs

    # # 元器件方程
    # @staticmethod
    # def get_equ_unit(ele_set, freq):
    #     equs = EquationGroup()
    #     for ele in ele_set:
    #         for module in ele.md_list:
    #             module.get_equs(freq)
    #             num = 1
    #             for equ in module.equs:
    #                 equ.name = module.name + '方程' + str(num)
    #                 equs.add_equation(equ)
    #                 num += 1
    #     return equs
    #
    # # KCL方程
    # @staticmethod
    # def get_equ_kcl(line):
    #     equs = EquationGroup()
    #     for num in range(len(line.posi_line)):
    #         node = line.node_dict[line.posi_line[num]]
    #         name = line.name + '_节点KCL方程' + str(num + 1)
    #         equ = Equation(name=name)
    #         for ele in node.element.values():
    #             vb = ele.md_list[-1].varb_dict[ele.md_list[-1].varb_name[-1]]
    #             equ.add_varb(vb, 1)
    #         if node.track[0] is not None:
    #             ele = node.track[0]
    #             vb = ele.md_list[-1].varb_dict[ele.md_list[-1].varb_name[-1]]
    #             equ.add_varb(vb, 1)
    #         if node.track[1] is not None:
    #             ele = node.track[1]
    #             vb = ele.md_list[-1].varb_dict[ele.md_list[-1].varb_name[1]]
    #             equ.add_varb(vb, 1)
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
    #         name = line.name + '_节点KVL方程' + str(num + 1)
    #         equ = Equation(name=name)
    #         if node.track[0] is not None:
    #             ele = node.track[0]
    #             vb = ele.md_list[-1].varb_dict[ele.md_list[-1].varb_name[-2]]
    #             equ.add_varb(vb, 1)
    #         if node.track[1] is not None:
    #             ele = node.track[1]
    #             vb = ele.md_list[-1].varb_dict[ele.md_list[-1].varb_name[0]]
    #             equ.add_varb(vb, -1)
    #         equs.add_equation(equ)
    #     return equs

    # 元器件方程
    @staticmethod
    def get_equ_unit(line_model, freq):
        equs = EquationGroup()
        ele_set = line_model.get_element(ele_set=set())
        for ele in ele_set:
            for module in ele.md_list:
                equs.add_equations(module.get_equs(freq))
            print(len(equs), ele.name)
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


########################################################################################################################

# # 获得钢轨上任意位置电压电流
# def get_rail_ui(line, value, posi, freq):
#     u_rail = 0
#     i_rail = 0
#     for ele in line['钢轨'].element.values():
#         if posi == ele.para['左端位置']:
#             u_rail = value[ele['等效电路']['U1'].num]
#             i_rail = value[ele['等效电路']['I1'].num]
#         elif posi == ele.para['右端位置']:
#             u_rail = value[ele['等效电路']['U2'].num]
#             i_rail = - value[ele['等效电路']['I2'].num]
#         elif ele.para['左端位置'] < posi < ele.para['右端位置']:
#             pi_temp = TCircuitRailPi('未定义', 'Pi等效',
#                                      l_posi=ele.para['左端位置'],
#                                      r_posi=ele.para['右端位置'],
#                                      z_trk=ele['等效电路'].z_trk,
#                                      rd=ele['等效电路'].rd)
#             u1 = value[ele['等效电路']['U1'].num]
#             i1 = value[ele['等效电路']['I1'].num]
#             u_rail, i_rail = pi_temp.getU2I2(u1, i1, freq)
#             i_rail = -i_rail
#     return u_rail, i_rail


def show_ele(vessel, para=''):
    if isinstance(vessel, (list, set)):
        list_t = list()
        for ele in vessel:
            if para == '':
                list_t.append(ele.__repr__())
            else:
                list_t.append(ele.__dict__[para].__repr__())
        list_t.sort()
        for ele in list_t:
            print(ele)
    elif isinstance(vessel, (dict, ElePack)):
        keys = sorted(list(vessel.keys()))
        for key in keys:
            if para == '':
                print(key, ':', vessel[key])
            else:
                print(vessel[key].__dict__[para])


#######################################################################################################################

if __name__ == '__main__':
    # print(time.asctime(time.localtime()))
    # # 载频
    # # 钢轨初始化
    # r1 = Rail(upper_ins=None, name_base='主串钢轨', trk_num=1,
    #           posi=[-np.inf, np.inf],
    #           ztrk=[TCSR_2000A['Trk_z']],
    #           rd=[TCSR_2000A['Rd']])

    # 轨道电路初始化
    sg1 = SectionGroup(name_base='地面', posi=0, m_num=1, freq1=2600,
                       m_length=[509, 389, 320],
                       j_length=[29, 29, 29, 29],
                       m_type=['2000A', '2000A', '2000A'],
                       c_num=[6, 6, 5],
                       parameter=TCSR_2000A)

    sg2 = SectionGroup(name_base='地面', posi=0, m_num=2, freq1=1700,
                       m_length=[480, 200, 320],
                       j_length=[29, 29, 29, 29],
                       m_type=['2000A', '2000A', '2000A'],
                       c_num=[8, 6, 5],
                       parameter=TCSR_2000A)

    train1 = Train(name_base='列车1', posi_abs=0, parameter=TCSR_2000A)

    # 生成线路
    l1 = Line(name_base='线路1', sec_group=sg1, train=train1,
              parameter=TCSR_2000A)
    l2 = Line(name_base='线路2', sec_group=sg2,
              parameter=TCSR_2000A)
    lg = LineGroup(l1, name_base='线路组')

    # 建立模型
    model = MainModel(lg)

    a = 1
    pass
    # output = []
    # for i in range(0, 600, 1):
    #     set_posi_abs(train1, i)
    #     l1.set_sub_rail(ele_all=ele_all)
    #     # l2.set_sub_rail(ele_all=ele_all)
    #     # 生成矩阵
    #     # m1 = Matrix(l1, l2, freq=FREQ)
    #     m1 = Matrix(l1, freq=FREQ)
    #     b = np.zeros(m1.length, dtype=complex)
    #     # b[m1.equ_dict['主串_区段1_电压源方程1'].num] = 100
    #     b[m1.equ_dict['主串_区段1_TCSR1_1发送器_1电压源方程1'].num] = 181
    #
    #     # 结果
    #     value_c = np.linalg.solve(m1.matrx, b)
    #     # del m1
    #
    #     if l1.node_dict[i].track[0] is not None:
    #         data = abs(value_c[l1.node_dict[i].track[0]['I2'].num])
    #     else:
    #         data = 0
    #
    #     # l2.node_dict[i].track[0]['I2']
    #     # x = abs(value_c[train1['分路电阻1']['阻抗']['I'].num])
    #     # x = np.angle(value_c[rc1['区段1']['TCSR2']['发送接收器']['采样电阻']['U'].num])/np.pi*180
    #     # print(x)
    #     output.append(data)

    # # 后处理
    # U_list = []
    # I_list = []
    # for i in range(2500):
    #     U,I = get_rail_ui(l1, value_c, i, FREQ)
    #     if U:
    #         U_list.append(abs(U))
    #         I_list.append(abs(I))

    # a = sp.Matrix(m1.matrx)
    # 画图
    # plt.title("Matplotlib demo")
    # plt.xlabel("x axis caption")
    # plt.ylabel("y axis caption")
    # plt.plot(output)
    # print(time.asctime(time.localtime()))
    # plt.show()

    pass
