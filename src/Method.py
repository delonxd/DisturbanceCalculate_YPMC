from src.AbstractClass.ElePack import *
from src.Module.JumperWire import *
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


if __name__ == '__main__':
    # m_lens = [700, 700, 700]
    # m_frqs = generate_frqs(Freq(2600), 3)
    # c_nums = get_c_nums(m_frqs, m_lens)

    pass