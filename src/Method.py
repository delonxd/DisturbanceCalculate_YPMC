from src.AbstractClass.ElePack import *
from src.Module.JumperWire import *
from src.Model.SingleLineModel import *
import numpy as np
from src.FrequencyType import Freq

# 显示元素
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

# 获取频率
def generate_frqs(freq1, m_num):
    frqs = list()
    for _ in range(m_num):
        frqs.append(freq1)
        freq1 = freq1.copy()
        freq1.change_freq()
    return frqs

# 获取电容数
def get_c_nums(m_frqs, m_lens):
    c_nums = list()
    for num in range(len(m_frqs)):
        freq = m_frqs[num]
        length = m_lens[num]
        c_num = get_c_num(freq, length)
        c_nums.append(c_num)
    return c_nums

# 获取电容数
def get_c_num(freq, length):
    if 0 < length < 300:
        index = 0
    elif length == 300:
        index = 1
    elif length > 300:
        index = int((length - 251) / 50)
    else:
        index  = 0

    CcmpTable1 = [0, 5, 6, 7, 8, 9, 10, 10, 11, 12, 13, 14, 15, 15, 16, 17, 18, 19, 20, 20, 21, 22, 23, 24, 25]
    CcmpTable2 = [0, 4, 5, 5, 6, 7,  7,  8,  8,  9, 10, 10, 11, 12, 12, 13, 13, 14, 15, 15, 16, 17, 17, 18, 18]

    freq = freq.value
    if freq == 1700 or freq == 2000:
        table = CcmpTable1
    elif freq == 2300 or freq == 2600:
        table = CcmpTable2
    else:
        table = []

    c_num = table[index]

    return c_num

# 获取钢轨电流
def get_i_trk(line, posi, direct='右'):
    i_trk = None
    if direct == '右':
        if line.node_dict[posi].r_track is not None:
            i_trk = line.node_dict[posi].r_track['I1'].value_c
        else:
            i_trk = 0.0
    elif direct == '左':
        if line.node_dict[posi].l_track is not None:
            i_trk = line.node_dict[posi].l_track['I2'].value_c
        else:
            i_trk = 0.0

    return i_trk


# 获取耦合系数
def get_mutual(distance):
    l1 = 6
    d = 1.435
    k1 = 13

    k_mutual = k1 / np.log((l1 * l1 - d * d) / l1 / l1)
    l2 = distance
    k2 = k_mutual * np.log((l2 * l2 - d * d) / l2 / l2)
    return k2


def config_sva1_mutual(model, temp, zm_sva):
    # zm_sva = 2 * np.pi * 1700 * 1 * 1e-6 * 1j
    m1 = model

    # temp_list = [(3, 4, '右'), (3, 4, '左') ,(4, 3, '左') ,(4, 3, '左')]
    # for temp in temp_list:
    line_zhu = '线路' + str(temp[0])
    line_bei = '线路' + str(temp[1])
    str_t = '线路组_' + line_bei + '_地面_区段1_' + temp[2] + '调谐单元_6SVA1_方程1'
    equ_t = m1.equs.equ_dict[str_t]
    str_t = '线路组_' + line_zhu + '_地面_区段1_' + temp[2] + '调谐单元'
    varb1 = m1[line_zhu]['元件'][str_t]['6SVA1']['I1']
    varb2 = m1[line_zhu]['元件'][str_t]['6SVA1']['I2']
    equ_t.varb_list.append(varb1)
    equ_t.varb_list.append(varb2)
    equ_t.coeff_list = np.append(equ_t.coeff_list, zm_sva)
    equ_t.coeff_list = np.append(equ_t.coeff_list, -zm_sva)


def config_jumpergroup(*jumpers):
    for jumper in jumpers:
        if not isinstance(jumper, JumperWire):
            raise KeyboardInterrupt('类型错误：参数需要为跳线类型')
        else:
            jumper.jumpergroup = list(jumpers)


def combine_node(nodes):
    if len(nodes) < 1:
        raise KeyboardInterrupt('数量错误：合并node至少需要1个参数')

    posi = nodes[0].posi
    node_new = Node(posi)
    node_new.node_type = 'combined'
    node_new.l_track = list()
    node_new.r_track = list()
    for node in nodes:
        if not isinstance(node, Node):
            raise KeyboardInterrupt('类型错误：合并node参数需要为节点类型')
        elif not node.posi == posi:
            raise KeyboardInterrupt('位置错误：合并node需要节点在相同水平位置')
        else:
            if node.l_track is not None:
                node_new.l_track.append(node.l_track)
            if node.r_track is not None:
                node_new.r_track.append(node.r_track)
            for key, value in node.element.items():
                node_new.element[key] = value
            node_new.equs.add_equations(node.equs)
    node_new.group_type = 'combined'
    return node_new


def combine_node_group(lines):
    groups = NodeGroup()
    posi_set = set()
    for line in lines:
        posi_set.update(line.node_dict.posi_set)

    posi_list = list(posi_set)
    posi_list.sort()

    for posi in posi_list:
        nodes_list = list()
        for line in lines:
            if posi in line.node_dict.keys():
                nodes_list.append(line.node_dict[posi])
        nodes = tuple(nodes_list)
        node_new = combine_node(nodes)
        groups.node_dict[posi] = node_new

    return groups


def config_25Hz_coding_para(df_input, temp_temp, para, data, pd_read_flag):

    # 发码方向
    if pd_read_flag:
        data['发码继电器状态'] = df_input['发码继电器状态'][temp_temp]
    else:
        # data['发码继电器状态'] = 1
        data['发码继电器状态'] = 0

    if data['发码继电器状态'] == 1:
        data['被串发送器位置'] = para['sr_mod_被'] = '不发码'
    elif data['发码继电器状态'] == 0:
        data['被串发送器位置'] = para['sr_mod_被'] = '右发'

    #################################################################################

    # FT1-U参数
    if pd_read_flag:
        # data['FT1-U短路阻抗-Rs(Ω)'] = value_r1 = df_input['FT1-U短路阻抗-Rs(Ω)'][temp_temp]
        # data['FT1-U短路阻抗-Ls(mH)'] = value_l1 = df_input['FT1-U短路阻抗-Ls(mH)'][temp_temp]
        # data['FT1-U开路阻抗-Rs(Ω)'] = value_r2 = df_input['FT1-U开路阻抗-Rs(Ω)'][temp_temp]
        # data['FT1-U开路阻抗-Ls(H)'] = value_l2 = df_input['FT1-U开路阻抗-Ls(H)'][temp_temp]
        #
        # value_l1 = value_l1 * 1e-3
        # para['zm_FT1u_25Hz_Coding'].rlc_s = {
        #     1700: [value_r2, value_l2, None],
        #     2000: [value_r2, value_l2, None],
        #     2300: [value_r2, value_l2, None],
        #     2600: [value_r2, value_l2, None]}
        #
        # para['zs_FT1u_25Hz_Coding'].rlc_s = {
        #     1700: [value_r1, value_l1, None],
        #     2000: [value_r1, value_l1, None],
        #     2300: [value_r1, value_l1, None],
        #     2600: [value_r1, value_l1, None]}

        n2_FT1u = df_input['FT1-U二次侧输出电压(V)'][temp_temp]
    else:
        n2_FT1u = 40

    value_n = 170 / n2_FT1u
    para['n_FT1u_25Hz_Coding'] = {
        1700: value_n,
        2000: value_n,
        2300: value_n,
        2600: value_n}

    #################################################################################

    # 设备参数
    if pd_read_flag:
        data['调整电阻(Ω)'] = Rt = df_input['调整电阻(Ω)'][temp_temp]
        data['调整电感(H)'] = Lt = df_input['调整电感(H)'][temp_temp]
        data['调整电容(F)'] = Ct = df_input['调整电容(F)'][temp_temp]
        data['调整RLC模式'] = mode_rlc = df_input['调整RLC模式'][temp_temp]
    else:
        data['调整电阻(Ω)'] = Rt = 50
        data['调整电感(H)'] = Lt = None
        data['调整电容(F)'] = Ct = None
        data['调整RLC模式'] = mode_rlc = '串联'

    if mode_rlc == '串联':
        para['Rt_25Hz_Coding'].rlc_s = {
            1700: [Rt, Lt, Ct],
            2000: [Rt, Lt, Ct],
            2300: [Rt, Lt, Ct],
            2600: [Rt, Lt, Ct]}
    elif mode_rlc == '并联':
        para['Rt_25Hz_Coding'].rlc_p = {
            1700: [Rt, Lt, Ct],
            2000: [Rt, Lt, Ct],
            2300: [Rt, Lt, Ct],
            2600: [Rt, Lt, Ct]}

    #################################################################################

    # 室内隔离盒
    if pd_read_flag:
        data['NGL-C1(μF)'] = value_c = df_input['NGL-C1(μF)'][temp_temp]
    else:
        data['NGL-C1(μF)'] = value_c = 1

    value_c = value_c * 1e-6
    para['C1_NGL_25Hz_Coding'].rlc_s = {
        1700: [None, None, value_c],
        2000: [None, None, value_c],
        2300: [None, None, value_c],
        2600: [None, None, value_c]}

    #################################################################################

    # 室外隔离盒
    if pd_read_flag:
        data['WGL-C1(μF)'] = value_c1 = df_input['WGL-C1(μF)'][temp_temp]
        data['WGL-C2(μF)'] = value_c2 = df_input['WGL-C2(μF)'][temp_temp]
        data['WGL-L1-R(Ω)'] = value_r1 = df_input['WGL-L1-R(Ω)'][temp_temp]
        data['WGL-L1-L(H)'] = value_l1 = df_input['WGL-L1-L(H)'][temp_temp]
        data['WGL-L2-R(Ω)'] = value_r2 = df_input['WGL-L2-R(Ω)'][temp_temp]
        data['WGL-L2-L(mH)'] = value_l2 = df_input['WGL-L2-L(mH)'][temp_temp]
        data['WGL-BPM变比'] = value_n = df_input['WGL-BPM变比'][temp_temp]
    else:
        data['WGL-C1(μF)'] = value_c1 = 1
        data['WGL-C2(μF)'] = value_c2 = 20
        data['WGL-L1-R(Ω)'] = value_r1 = None
        data['WGL-L1-L(H)'] = value_l1 = 0.5
        data['WGL-L2-R(Ω)'] = value_r2 = None
        data['WGL-L2-L(mH)'] = value_l2 = 5
        data['WGL-BPM变比'] = value_n = 4

    value_c1 = value_c1 * 1e-6
    value_c2 = value_c2 * 1e-6
    value_l2 = value_l2 * 1e-3

    para['C1_WGL_25Hz_Coding'].rlc_s = {
        1700: [None, None, value_c1],
        2000: [None, None, value_c1],
        2300: [None, None, value_c1],
        2600: [None, None, value_c1]}

    para['C2_WGL_25Hz_Coding'].rlc_s = {
        1700: [None, None, value_c2],
        2000: [None, None, value_c2],
        2300: [None, None, value_c2],
        2600: [None, None, value_c2]}

    para['L1_WGL_25Hz_Coding'].rlc_s = {
        1700: [value_r1, value_l1, None],
        2000: [value_r1, value_l1, None],
        2300: [value_r1, value_l1, None],
        2600: [value_r1, value_l1, None]}

    para['L2_WGL_25Hz_Coding'].rlc_s = {
        1700: [value_r2, value_l2, None],
        2000: [value_r2, value_l2, None],
        2300: [value_r2, value_l2, None],
        2600: [value_r2, value_l2, None]}

    para['n_WGL_25Hz_Coding'] = {
        1700: value_n,
        2000: value_n,
        2300: value_n,
        2600: value_n}

    #################################################################################

    # 扼流变压器
    if pd_read_flag:
        data['扼流变压器变比'] = value_n = df_input['扼流变压器变比'][temp_temp]
        data['BE-Rm(Ω)'] = value_r = df_input['BE-Rm(Ω)'][temp_temp]
        data['BE-Lm(H)'] = value_l = df_input['BE-Lm(H)'][temp_temp]
    else:
        data['扼流变压器变比'] = value_n = 3
        data['BE-Rm(Ω)'] = value_r = 110
        data['BE-Lm(H)'] = value_l = 0.024

    para['n_EL_25Hz_Coding'] = {
        1700: value_n,
        2000: value_n,
        2300: value_n,
        2600: value_n}

    para['zm_EL_25Hz_Coding'].rlc_s = {
        1700: [value_r, value_l, None],
        2000: [value_r, value_l, None],
        2300: [value_r, value_l, None],
        2600: [value_r, value_l, None]}

    ################################################################################

def config_ypmc_para(df_input, temp_temp, para, data, pd_read_flag):

    # 设置变比
    if pd_read_flag:
        data['主串扼流变比'] = value_n = df_input['主串扼流变压器变比'][temp_temp]
        para['主串扼流变比'] = {
            1700: value_n,
            2000: value_n,
            2300: value_n,
            2600: value_n}

        data['被串扼流变比'] = value_n = df_input['被串扼流变压器变比'][temp_temp]
        para['被串扼流变比'] = {
            1700: value_n,
            2000: value_n,
            2300: value_n,
            2600: value_n}

    else:
        data['主串扼流变比'] = para['主串扼流变比'] = None
        data['被串扼流变比'] = para['被串扼流变比'] = None


if __name__ == '__main__':
    # m_lens = [700, 700, 700]
    # m_frqs = generate_frqs(Freq(2600), 3)
    # c_nums = get_c_nums(m_frqs, m_lens)
    a = [1,2,3]
    pass