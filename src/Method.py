from src.AbstractClass.ElePack import *
from src.Module.JumperWire import *
from src.Model.SingleLineModel import *
import numpy as np
from src.FrequencyType import Freq


#################################################################################

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


#################################################################################

# 获取频率
def generate_frqs(freq1, m_num):
    frqs = list()
    for _ in range(m_num):
        frqs.append(freq1)
        freq1 = freq1.copy()
        freq1.change_freq()
    return frqs


#################################################################################

# 获取电容数
def get_c_nums(m_frqs, m_lens):
    c_nums = list()
    for num in range(len(m_frqs)):
        freq = m_frqs[num]
        length = m_lens[num]
        c_num = get_c_num(freq, length)
        c_nums.append(c_num)
    return c_nums


#################################################################################

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


#################################################################################

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


#################################################################################

# 获取耦合系数
def get_mutual(distance):
    l1 = 6
    d = 1.435
    k1 = 13

    k_mutual = k1 / np.log((l1 * l1 - d * d) / l1 / l1)
    l2 = distance
    k2 = k_mutual * np.log((l2 * l2 - d * d) / l2 / l2)
    return k2


#################################################################################

# 配置SVA'互感
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


#################################################################################

# 配置跳线组
def config_jumpergroup(*jumpers):
    for jumper in jumpers:
        if not isinstance(jumper, JumperWire):
            raise KeyboardInterrupt('类型错误：参数需要为跳线类型')
        else:
            jumper.jumpergroup = list(jumpers)


#################################################################################

# 合并节点
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


#################################################################################

# 合并节点组
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


#################################################################################

# 配置25Hz电码化参数
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


#################################################################################

# 配置移频脉冲参数
def config_ypmc_para(df_input, temp_temp, para, data, pd_read_flag):

    # 设置变比
    if pd_read_flag:
        data['主串扼流变压器变比'] = value_n = df_input['主串扼流变压器变比'][temp_temp]
        para['主串扼流变比'] = {
            1700: value_n,
            2000: value_n,
            2300: value_n,
            2600: value_n}

        data['被串扼流变压器变比'] = value_n = df_input['被串扼流变压器变比'][temp_temp]
        para['被串扼流变比'] = {
            1700: value_n,
            2000: value_n,
            2300: value_n,
            2600: value_n}
    else:
        data['主串扼流变压器变比'] = para['主串扼流变比'] = None
        data['被串扼流变压器变比'] = para['被串扼流变比'] = None


    # 设置电缆长度
    data['电缆长度(km)'] = para['cab_len'] = 0.75
    if pd_read_flag:
        data['主串电缆长度(km)'] = para['主串电缆长度'] = df_input['主串电缆长度(km)'][temp_temp]
        data['被串电缆长度(km)'] = para['被串电缆长度'] = df_input['被串电缆长度(km)'][temp_temp]
    else:
        data['主串电缆长度(km)'] = para['主串电缆长度'] = 0.75
        data['被串电缆长度(km)'] = para['被串电缆长度'] = 0.75


    # 设置分路电阻
    data['分路电阻(Ω)'] = para['Rsht_z'] = 0.0000001
    if pd_read_flag:
        data['主串分路电阻(Ω)'] = para['主串分路电阻'] = df_input['主串分路电阻(Ω)'][temp_temp]
        data['被串分路电阻(Ω)'] = para['被串分路电阻'] = df_input['被串分路电阻(Ω)'][temp_temp]
    else:
        data['主串分路电阻(Ω)'] = para['主串分路电阻'] = 0.0000001
        data['被串分路电阻(Ω)'] = para['被串分路电阻'] = 0.0000001


#################################################################################

# 移频脉冲表头
def config_ypmc_headlist():
    head_list = [
        '序号', '备注',

        '主串区段长度(m)', '被串区段长度(m)',
        '钢轨电阻(Ω/km)', '钢轨电感(H/km)',

        '耦合系数',
        '主串频率(Hz)', '被串频率(Hz)',
        '主串道床电阻(Ω·km)', '被串道床电阻(Ω·km)',
        '主串电容数(含TB)', '被串电容数(含TB)',
        '主串电容值(μF)', '被串电容值(μF)',

        '主串分路电阻(Ω)', '被串分路电阻(Ω)',
        '分路间隔(m)',
        '主串电缆长度(km)', '被串电缆长度(km)',

        '主串扼流变压器变比', '被串扼流变压器变比',
        '主串电平级',

        '主串功出电压(V)', '主串轨入电压(V)',
        '被串最大干扰电流(A)', '被串最大干扰位置(m)',
    ]

    return head_list


#################################################################################

# 25Hz电码化表头
def config_25Hz_coding_headlist():
    head_list = [
        '序号', '备注',

        '主串区段长度(m)', '被串区段长度(m)',

        '钢轨电阻(Ω/km)', '钢轨电感(H/km)',

        '耦合系数',
        '主串频率(Hz)', '被串频率(Hz)',
        '主串道床电阻(Ω·km)', '被串道床电阻(Ω·km)',
        '主串电容数(含TB)', '被串电容数(含TB)',
        '主串电容值(μF)', '被串电容值(μF)',
        '主串拆卸情况', '被串拆卸情况',

        '分路电阻(Ω)',
        '分路间隔(m)',
        '电缆长度(km)',

        '主串电平级',
        '发码继电器状态',

        '调整电阻(Ω)', '调整电感(H)', '调整电容(F)',
        '调整RLC模式',

        'NGL-C1(μF)',

        'WGL-C1(μF)',
        'WGL-C2(μF)',
        'WGL-L1-R(Ω)', 'WGL-L1-L(H)',
        'WGL-L2-R(Ω)', 'WGL-L2-L(mH)',

        'WGL-BPM变比',
        '扼流变压器变比',

        'BE-Rm(Ω)', 'BE-Lm(H)',

        '被串最大干扰电流(A)', '被串最大干扰位置(m)',
        '主串出口电流(A)', '主串入口电流(A)',
    ]

    return head_list


#################################################################################

# 绝缘破损防护表头
def config_2000A_TB_headlist():
    head_list = [
        '序号',
        '备注',

        '主串区段长度(m)', '被串区段长度(m)',

        '钢轨电阻(Ω/km)', '钢轨电感(H/km)',

        '耦合系数',
        '主串频率(Hz)', '被串频率(Hz)',
        '主串道床电阻(Ω·km)', '被串道床电阻(Ω·km)',
        '主串电容数(含TB)', '被串电容数(含TB)',
        '主串电容值(μF)', '被串电容值(μF)',
        '主串拆卸情况', '被串拆卸情况',

        'TB模式',
        # "SVA'互感",

        '分路电阻(Ω)',
        '分路间隔(m)',
        '电缆长度(km)',

        '主串电平级',
        '电源电压',

        # '是否全部更换TB',

        # '主串轨入电压(调整状态)',
        # '被串最大轨入电压(主备串同时分路状态)',

        '被串最大干扰电流(A)', '被串最大干扰位置(m)',
        # '主串出口电流(A)', '主串入口电流(A)',
    ]

    return head_list


#################################################################################

# 配置序号
def config_data_number(df_input, row, para, data, pd_read_flag, counter):
    if pd_read_flag:
        data['序号'] = para['序号'] = df_input['序号'][row]
    else:
        data['序号'] = para['序号'] = counter


#################################################################################

# 配置备注
def config_data_remarks(df_input, row, para, data, pd_read_flag, remarks):
    if pd_read_flag:
        data['备注'] = para['备注'] = df_input['备注'][row]
    else:
        data['备注'] = para['备注'] = remarks


#################################################################################

# 配置区段长度
def config_data_length(df_input, row, para, data, pd_read_flag, len_zhu, len_bei):
    if pd_read_flag:
        data['主串区段长度(m)'] = para['主串区段长度'] = df_input['主串区段长度(m)'][row]
        data['被串区段长度(m)'] = para['被串区段长度'] = df_input['被串区段长度(m)'][row]
    else:
        data['主串区段长度(m)'] = para['主串区段长度'] = len_zhu
        data['被串区段长度(m)'] = para['被串区段长度'] = len_bei

    data['主被发送相对位置'] = off_set_send = 0
    para['offset'] = data['被串区段长度(m)'] - data['主串区段长度(m)'] - off_set_send

#################################################################################

# 配置耦合系数
def config_data_mutualcoeff(df_input, row, para, data, pd_read_flag, coeff):
    if pd_read_flag:
        data['耦合系数'] = para['耦合系数'] = df_input['耦合系数'][row]
    else:
        data['耦合系数'] = para['耦合系数'] = coeff


#################################################################################

# 配置区段频率
def config_data_freq(df_input, row, para, data, pd_read_flag, frq_zhu, frq_bei):
    if pd_read_flag:
        data['主串频率(Hz)'] = para['freq_主'] = freq = df_input['主串频率(Hz)'][row]
        data['被串频率(Hz)'] = para['freq_被'] = df_input['被串频率(Hz)'][row]
    else:
        data['主串频率(Hz)'] = para['freq_主'] = freq = frq_zhu
        data['被串频率(Hz)'] = para['freq_被'] = frq_bei

    data['freq'] = para['freq'] = Freq(freq)


#################################################################################

# 配置电容数量
def config_data_c_num(df_input, row, para, data, pd_read_flag, cnum_zhu, cnum_bei):
    # data['主串电容数'] = para['主串电容数'] = get_c_num(Freq(data['主串频率']), data['区段长度'])
    # data['被串电容数'] = para['被串电容数'] = get_c_num(Freq(data['被串频率']), data['区段长度'])
    if pd_read_flag:
        data['主串电容数(含TB)'] = para['主串电容数'] = df_input['主串电容数(含TB)'][row]
        data['被串电容数(含TB)'] = para['被串电容数'] = df_input['被串电容数(含TB)'][row]
    else:
        data['主串电容数(含TB)'] = para['主串电容数'] = cnum_zhu
        data['被串电容数(含TB)'] = para['被串电容数'] = cnum_bei


#################################################################################

# 配置电容位置
def config_data_c_posi(df_input, row, para, data, pd_read_flag, c_pst_zhu, c_pst_bei):
    pd_read_flag = False
    if pd_read_flag:
        data['主串电容(不含TB)位置'] = para['主串电容位置'] = df_input['主串电容(不含TB)位置'][row]
        data['被串电容(不含TB)位置'] = para['被串电容位置'] = df_input['主串电容(不含TB)位置'][row]
    else:
        data['主串电容(不含TB)位置'] = para['主串电容位置'] = c_pst_zhu
        data['被串电容(不含TB)位置'] = para['被串电容位置'] = c_pst_bei

    # hlf_pst = list(np.linspace(0, 650, 15))
    # c_pst = [hlf_pst[num * 2 + 1] - 90 for num in range(7)]
    # c_pst = c_pst[1:-1]
    # data['主串电容(不含TB)位置'] = para['主串电容位置'] = c_pst
    # data['被串电容(不含TB)位置'] = para['被串电容位置'] = c_pst

    pass

#################################################################################

# 配置电容换TB
def config_data_c2TB(para, data, change_flag):
    data['是否全部更换TB'] = change_flag

    if data['是否全部更换TB'] is True:
        # if data['主串频率(Hz)'] == 1700 or data['主串频率(Hz)'] == 2000:
        #     data['主串更换TB'] = para['主串更换TB'] = True
        # if data['被串频率(Hz)'] == 1700 or data['被串频率(Hz)'] == 2000:
        #     data['被串更换TB'] = para['被串更换TB'] = True

        data['主串更换TB'] = para['主串更换TB'] = True
        data['被串更换TB'] = para['被串更换TB'] = True
    else:
        data['主串更换TB'] = para['主串更换TB'] = False
        data['被串更换TB'] = para['被串更换TB'] = False


#################################################################################

# 配置电容容值
def config_data_c_value(df_input, row, para, data, pd_read_flag, c_val_zhu, c_val_bei):
    if pd_read_flag:
        data['主串电容值(μF)'] = c_value1 = df_input['主串电容值(μF)'][row]
        data['被串电容值(μF)'] = c_value2 = df_input['被串电容值(μF)'][row]
    else:
        data['主串电容值(μF)'] = c_value1 = c_val_zhu
        data['被串电容值(μF)'] = c_value2 = c_val_bei

    c_value1 = c_value1 * 1e-6
    c_value2 = c_value2 * 1e-6

    para['Ccmp_z_change_zhu'].rlc_s = {
        1700: [10e-3, None, c_value1],
        2000: [10e-3, None, c_value1],
        2300: [10e-3, None, c_value1],
        2600: [10e-3, None, c_value1]}
    para['Ccmp_z_change_chuan'].rlc_s = {
        1700: [10e-3, None, c_value2],
        2000: [10e-3, None, c_value2],
        2300: [10e-3, None, c_value2],
        2600: [10e-3, None, c_value2]}

    # para['Ccmp_z_change_chuan'].rlc_s = {
    #     1700: [10e-3, 390e-6, 11.9e-6],
    #     2000: [10e-3, 390e-6, 11.9e-6],
    #     2300: [10e-3, 390e-6, 11.9e-6],
    #     2600: [10e-3, 390e-6, 11.9e-6]}

    # data['被串电容值'] = '抑制装置'
    # para['抑制装置电感短路'] = ImpedanceMultiFreq()
    # para['抑制装置电感短路'].rlc_s = {
    #     1700: [10e-3, None, 11.9e-6],
    #     2000: [10e-3, None, 11.9e-6],
    #     2300: [10e-3, None, 11.9e-6],
    #     2600: [10e-3, None, 11.9e-6]}

    # data['换电容位置'] = para['换电容位置'] = cv2
    # data['换电容位置'] = para['换电容位置'] = 0


#################################################################################

# 配置道床电阻
def config_data_rd(df_input, row, para, data, pd_read_flag, rd_zhu, rd_bei):
    data['道床电阻'] = rd_zhu

    if pd_read_flag:
        data['主串道床电阻(Ω·km)'] = df_input['主串道床电阻(Ω·km)'][row]
        data['被串道床电阻(Ω·km)'] = df_input['被串道床电阻(Ω·km)'][row]
    else:
        data['主串道床电阻(Ω·km)'] = data['道床电阻']
        data['被串道床电阻(Ω·km)'] = data['道床电阻']

    para['主串道床电阻'] = Constant(data['主串道床电阻(Ω·km)'])
    para['被串道床电阻'] = Constant(data['被串道床电阻(Ω·km)'])

    # data['道床电阻最大(Ω·km)'] = 1000
    # data['道床电阻最小(Ω·km)'] = 2

    para['Rd'].value = data['道床电阻']


#################################################################################

# 配置钢轨阻抗
def config_data_trk_z(df_input, row, para, data, pd_read_flag):
    freq = data['主串频率(Hz)']

    if pd_read_flag:
        data['钢轨电阻(Ω/km)'] = df_input['钢轨电阻(Ω/km)'][row]
        data['钢轨电感(H/km)'] = df_input['钢轨电感(H/km)'][row]
        para['Trk_z'].rlc_s = \
                {freq: [data['钢轨电阻(Ω/km)'], data['钢轨电感(H/km)'], None]}
    else:
        data['钢轨电阻(Ω/km)'] = round(para['Trk_z'].rlc_s[freq][0], 10)
        data['钢轨电感(H/km)'] = round(para['Trk_z'].rlc_s[freq][1], 10)


    # data['钢轨电阻(Ω/km)'] = round(para['Trk_z'].rlc_s[freq][0], 10)
    # data['钢轨电感(H/km)'] = round(para['Trk_z'].rlc_s[freq][1], 10)

    para['主串钢轨阻抗'] = para['Trk_z']
    para['被串钢轨阻抗'] = para['Trk_z']



    # # data['主串钢轨电阻'] = cv3
    # data['主串钢轨电阻'] = df_input['主串钢轨电阻'][temp_temp]
    #
    # # data['主串钢轨电感'] = cv4
    # data['主串钢轨电感'] = df_input['主串钢轨电感'][temp_temp]
    #
    # # data['被串钢轨电阻'] = 1.558
    # data['被串钢轨电阻'] = df_input['被串钢轨电阻'][temp_temp]
    #
    # # data['被串钢轨电感'] = 1.291e-3
    # data['被串钢轨电感'] = df_input['被串钢轨电感'][temp_temp]
    #
    # para['主串钢轨阻抗'] = ImpedanceMultiFreq()
    # para['主串钢轨阻抗'].rlc_s = \
    #     {data['主串频率']: [data['主串钢轨电阻'], data['主串钢轨电感'], None]}
    # para['被串钢轨阻抗'] = ImpedanceMultiFreq()
    # para['被串钢轨阻抗'].rlc_s = \
    #     {data['主串频率']: [data['被串钢轨电阻'], data['被串钢轨电感'], None]}


#################################################################################

# 配置TB模式
def config_data_TB_mode(df_input, row, para, data, pd_read_flag, tb_mode):
    pd_read_flag = False

    if pd_read_flag:
        data['TB模式'] = flag_tb = df_input['TB模式'][row]
    else:
        data['TB模式'] = flag_tb = tb_mode

    if flag_tb == '双端TB':
        para['TB模式'] = '双'
    elif flag_tb == '发送端单TB':
        para['TB模式'] = '右'
    elif flag_tb == '接收端单TB':
        para['TB模式'] = '左'
    elif flag_tb == '无TB':
        para['TB模式'] = '无'
    else:
        raise KeyboardInterrupt('TB模式错误')


#################################################################################

# 配置发码方向
def config_data_sr_mode(df_input, row, para, data, pd_read_flag, sr_zhu, sr_bei):
    data['主串发送器位置'] = para['sr_mod_主'] = sr_zhu
    data['被串发送器位置'] = para['sr_mod_被'] = sr_bei

    # # 发码方向
    # if pd_read_flag:
    #     data['发码继电器状态'] = df_input['发码继电器状态'][temp_temp]
    # else:
    #     # data['发码继电器状态'] = 1
    #     data['发码继电器状态'] = 0
    #
    # if data['发码继电器状态'] == 1:
    #     data['被串发送器位置'] = para['sr_mod_被'] = '不发码'
    # elif data['发码继电器状态'] == 0:
    #     data['被串发送器位置'] = para['sr_mod_被'] = '右发'


#################################################################################

# 配置设备拆卸情况
def config_data_pop(df_input, row, para, data, pd_read_flag, pop_zhu, pop_bei):
    pd_read_flag = False
    if pd_read_flag:
        data['主串拆卸情况'] = para['主串拆卸情况'] = eval(df_input['主串拆卸情况'][row])
        data['被串拆卸情况'] = para['被串拆卸情况'] = eval(df_input['被串拆卸情况'][row])
    else:
        data['主串拆卸情况'] = para['主串拆卸情况'] = pop_zhu
        data['被串拆卸情况'] = para['被串拆卸情况'] = pop_bei


#################################################################################

# 配置电缆参数
def config_data_cable_para(para, data):
    data['电缆电阻最大(Ω/km)'] = 45
    data['电缆电阻最小(Ω/km)'] = 43
    # data['电缆电容最大(F/km)'] = 30e-9
    # data['电缆电容最小(F/km)'] = 26e-9
    data['电缆电容最大(F/km)'] = 28e-9
    data['电缆电容最小(F/km)'] = 28e-9

    para['Cable_R'].value = data['电缆电阻最小(Ω/km)']
    para['Cable_C'].value = data['电缆电容最大(F/km)']


#################################################################################

# 配置电缆长度
def config_data_cable_length(df_input, row, para, data, pd_read_flag, len_cable):
    pd_read_flag = False
    if pd_read_flag:
        data['电缆长度(km)'] = para['cab_len'] = df_input['电缆长度(km)'][row]
    else:
        data['电缆长度(km)'] = para['cab_len'] = len_cable


#################################################################################

# 配置分路电阻
def config_data_r_sht(df_input, row, para, data, pd_read_flag, r_sht):
    pd_read_flag = False
    if pd_read_flag:
        data['分路电阻(Ω)'] = para['Rsht_z'] = df_input['分路电阻(Ω)'][row]
    else:
        data['分路电阻(Ω)'] = para['Rsht_z'] = r_sht


#################################################################################

# 配置功出电源
def config_data_power(df_input, row, para, data, pd_read_flag, send_level, v_power):
    if pd_read_flag:
        data['主串电平级'] = para['send_level'] = df_input['主串电平级'][row]
    else:
        data['主串电平级'] = para['send_level'] = send_level

    data['电源电压'] = para['pwr_v_flg'] = v_power


#################################################################################

# 配置分路间隔
def config_data_interval(df_input, row, data, pd_read_flag, interval):
    if pd_read_flag:
        data['分路间隔(m)'] = df_input['分路间隔(m)'][row]
    else:
        data['分路间隔(m)'] = interval

    return data['分路间隔(m)']


#################################################################################

# 配置特殊位置
def config_data_sp_posi(para, data):

    # 极性交叉位置
    data['极性交叉位置'] = para['极性交叉位置'] = []

    # data['特殊位置'] = para['special_point'] = list(np.linspace(0,length + length, 21))
    data['特殊位置'] = para['special_point'] = data['极性交叉位置']

    data['节点选取模式'] = para['节点选取模式'] = '特殊'


# 配置机车信号
def config_data_train_signal(para, data):
    data['最小机车信号位置'] = '-'

    data['机车信号感应系数'] = \
        str(para['机车信号比例V']) + '/' + str(para['机车信号比例I'][para['freq_主']])
    para['机车信号系数值'] = para['机车信号比例V'] / para['机车信号比例I'][para['freq_主']]


if __name__ == '__main__':
    # m_lens = [700, 700, 700]
    # m_frqs = generate_frqs(Freq(2600), 3)
    # c_nums = get_c_nums(m_frqs, m_lens)
    a = [1,2,3]
    pass