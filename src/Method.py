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


if __name__ == '__main__':
    # m_lens = [700, 700, 700]
    # m_frqs = generate_frqs(Freq(2600), 3)
    # c_nums = get_c_nums(m_frqs, m_lens)
    a = [1,2,3]
    pass