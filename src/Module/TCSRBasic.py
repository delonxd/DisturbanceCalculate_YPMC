from src.Module.Cable import *
from src.Module.TcsrElement import *

import src.TrackCircuitElement.Section as sc
import src.TrackCircuitElement.Joint as jt


class TCSR(ElePack):
    new_table = {
        '主轨类型': 'm_type',
        '模式': 'mode',
        '匹配频率': 'm_freq',
        '发送电平级': 'send_level',
        '电缆长度': 'cable_length'
    }
    prop_table = ElePack.prop_table.copy()
    prop_table.update(new_table)

    def __init__(self, parent_ins, name_base, posi_flag):
        super().__init__(parent_ins, name_base)
        self.posi_flag = posi_flag
        self.init_position(0)
        self.flag_ele_list = True
        self.flag_ele_unit = True
        self.mode = None
        self.md_list = list()

    @property
    def posi_rlt(self):
        posi = None
        parent = self.parent_ins
        if isinstance(parent, sc.Section):
            if self.posi_flag == '左':
                posi = parent['左绝缘节'].j_length / 2
            elif self.posi_flag == '右':
                posi = parent.s_length - parent['右绝缘节'].j_length / 2
        elif isinstance(parent, jt.Joint):
            if self.posi_flag == '左':
                posi = parent.j_length / 2
            elif self.posi_flag == '右':
                posi = - parent.j_length / 2
        return posi

    @property
    def parent_joint(self):
        joint = None
        if isinstance(self.parent_ins, sc.Section):
            name = self.posi_flag + '绝缘节'
            joint = self.parent_ins[name]
        elif isinstance(self.parent_ins, jt.Joint):
            joint = self.parent_ins
        return joint

    @property
    def m_type(self):
        m_type = None
        if isinstance(self.parent_ins, sc.Section):
            m_type = self.parent_ins.m_type
        elif isinstance(self.parent_ins, jt.Joint):
            m_type = self.parent_ins.parent_ins.m_type
        return m_type

    @property
    def m_freq(self):
        m_freq = None
        if isinstance(self.parent_ins, sc.Section):
            m_freq = self.parent_ins.m_freq
        elif isinstance(self.parent_ins, jt.Joint):
            section = self.parent_ins.parent_ins
            m_freq = section.change_freq(section.m_freq)
        return m_freq

    @property
    def cable_length(self):
        length = None
        for ele in self.element.values():
            if isinstance(ele, TPortCable):
                length = ele.length
        return length

    @cable_length.setter
    def cable_length(self, value):
        for ele in self.element.values():
            if isinstance(ele, TPortCable):
                ele.length = value

    @property
    def send_level(self):
        level = None
        for ele in self.element.values():
            if isinstance(ele, TcsrPower):
                level = ele.level
        return level

    @send_level.setter
    def send_level(self, value):
        for ele in self.element.values():
            if isinstance(ele, TcsrPower):
                ele.level = value

    # 变量赋值
    def config_varb(self):
        for num in range(len(self.md_list) - 1):
            self.equal_varb([self.md_list[num], -2], [self.md_list[num + 1], 0])
            self.equal_varb([self.md_list[num], -1], [self.md_list[num + 1], 1])
