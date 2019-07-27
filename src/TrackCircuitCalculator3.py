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

        for line in line_group.element.values():
            self[line.name_base] = SingleLineModel(self, line)
        self.set_line_mutual()
        # self.ele_set = get_element()
        self.equs_kirchhoff = self.get_equs_kirchhoff()

    def set_line_mutual(self):
        if len(self.element) == 2:
            lines = list(self.element.values())
            set1 = set(lines[0].node_dict.keys())
            set2 = set(lines[1].node_dict.keys())
            node_set = list(set1.intersection(set2))
            node_set.sort()
            for posi in node_set[:-1]:
                lines[0].node_dict[posi].track[1].mutual_trk = lines[1].node_dict[posi].track[1]
                lines[1].node_dict[posi].track[1].mutual_trk = lines[0].node_dict[posi].track[1]

    def get_equs_kirchhoff(self):
        equs = list()
        for line_model in self.element.values():
            # equs.extend(self.get_equ_unit(line_model, freq))
            equs.extend(self.get_equ_kcl(line_model))
            equs.extend(self.get_equ_kvl(line_model))
        return equs

    # 元器件方程
    @staticmethod
    def get_equ_unit(vessel, freq, equs):
        ele_set = vessel.get_element(ele_set=set())
        # equs = []
        for ele in ele_set:
            for module in ele.md_list:
                module.get_equs(freq)
                num = 1
                for equ in module.equs:
                    equ.name = module.name + '方程' + str(num)
                    equs.append(equ)
                    num += 1
        return equs

    # KCL方程
    @staticmethod
    def get_equ_kcl(line):
        equs = list()
        for num in range(len(line.posi_line)):
            node = line.node_dict[line.posi_line[num]]
            name = line.name + '_节点KCL方程' + str(num+1)
            equ = Equation(name=name)
            for ele in node.element.values():
                vb = ele.md_list[-1].varb_dict[ele.md_list[-1].varb_name[-1]]
                equ.add_varb(vb, 1)
            if node.track[0] is not None:
                ele = node.track[0]
                vb = ele.md_list[-1].varb_dict[ele.md_list[-1].varb_name[-1]]
                equ.add_varb(vb, 1)
            if node.track[1] is not None:
                ele = node.track[1]
                vb = ele.md_list[-1].varb_dict[ele.md_list[-1].varb_name[1]]
                equ.add_varb(vb, 1)
            equs.append(equ)
        return equs

    # KVL方程
    @staticmethod
    def get_equ_kvl(line):
        equs = list()
        posi_line = line.posi_line[1:-1]
        for num in range(len(posi_line)):
            node = line.node_dict[posi_line[num]]
            name = line.name + '_节点KVL方程' + str(num+1)
            equ = Equation(name=name)
            if node.track[0] is not None:
                ele = node.track[0]
                vb = ele.md_list[-1].varb_dict[ele.md_list[-1].varb_name[-2]]
                equ.add_varb(vb, 1)
            if node.track[1] is not None:
                ele = node.track[1]
                vb = ele.md_list[-1].varb_dict[ele.md_list[-1].varb_name[0]]
                equ.add_varb(vb, -1)
            equs.append(equ)
        return equs


# 从等式获取变量
def get_varb_set(equs):
    varb_set = set()
    for equ in equs:
        for ele in equ.vb_list:
            varb_set.add(ele[0])
    return varb_set.copy()


def get_matrix(equs):
    varb_set = get_varb_set(equs)
    set_varb_num(varb_set)
    length = len(equs)
    mtrx = np.matlib.zeros((length, length), dtype=complex)

    for num in range(length):
        for varb, value in equs[num].vb_list:
            mtrx[num, varb.num] = value
    return mtrx


# 变量编号
def set_varb_num(var_set):
    name_list = []
    for varb in var_set:
        name_list.append(varb.get_varb_name())
    name_list.sort()
    varb_list = [None] * len(name_list)
    for varb in var_set:
        name = varb.get_varb_name()
        varb.num = name_list.index(name)
        varb_list[varb.num] = varb
    return varb_list


########################################################################################################################

# 方程组排序
def equ_sort(equs):
    name_list = []
    for equ in equs:
        name_list.append(equ.name)
    name_list.sort()
    equ_dict = {}
    equ_list = [None] * len(name_list)
    for equ in equs:
        name = equ.name
        equ.num = name_list.index(name)
        equ_list[equ.num] = equ
        equ_dict[name] = equ
    return equ_list, equ_dict


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


# with open('TCSR_2000A_data_lib.pkl', 'rb') as pk_f:
#     TCSR_2000A = pickle.load(pk_f)
#
# TCSR_2000A['Ccmp_z'] = pc.ParaMultiF(1700, 2000, 2300, 2600)
# TCSR_2000A['Ccmp_z'].rlc_s = {
#     1700: [10e-3, None, 25e-6],
#     2000: [10e-3, None, 25e-6],
#     2300: [10e-3, None, 25e-6],
#     2600: [10e-3, None, 25e-6]}
#
# # 钢轨阻抗
# TCSR_2000A['Trk_z'] = pc.ParaMultiF(1700, 2000, 2300, 2600)
# TCSR_2000A['Trk_z'].rlc_s = {
#     1700: [1.177, 1.314e-3, None],
#     2000: [1.306, 1.304e-3, None],
#     2300: [1.435, 1.297e-3, None],
#     2600: [1.558, 1.291e-3, None]}
#
# TCSR_2000A['Rd'] = 10000
# TCSR_2000A['Rsht_z'] = 10e-3
#
# # 载频
# FREQ = 2600


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
    sg1 = SectionGroup(name_base='地面', posi=0, m_num=2, freq1=2600,
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
