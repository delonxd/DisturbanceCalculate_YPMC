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
        self.send_level = 0
        self.equs = EquationGroup()
        self.equs_cmplx = EquationGroup()

        self.pwr_voltage = Constant()
        self.u_list_max = list()
        self.u_list_min = list()

    # 相对位置
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

    # 隶属的绝缘节
    @property
    def parent_joint(self):
        joint = None
        if isinstance(self.parent_ins, sc.Section):
            name = self.posi_flag + '绝缘节'
            joint = self.parent_ins[name]
        elif isinstance(self.parent_ins, jt.Joint):
            joint = self.parent_ins
        return joint

    # 区段类型
    @property
    def m_type(self):
        m_type = None
        if isinstance(self.parent_ins, sc.Section):
            m_type = self.parent_ins.m_type
        elif isinstance(self.parent_ins, jt.Joint):
            m_type = self.parent_ins.parent_ins.m_type
        return m_type

    # 区段频率
    @property
    def m_freq(self):
        m_freq = None
        if isinstance(self.parent_ins, sc.Section):
            m_freq = self.parent_ins.m_freq
        elif isinstance(self.parent_ins, jt.Joint):
            section = self.parent_ins.parent_ins
            m_freq = section.m_freq.copy()
            m_freq.change_freq()
            # m_freq = section.change_freq(section.m_freq)
        return m_freq

    # 电缆长度
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

    # 设置电压源输出
    def set_power_voltage(self, flag):
        if flag == '最大':
            self.pwr_voltage.value = self.u_list_max[self.send_level - 1]
        elif flag == '最小':
            self.pwr_voltage.value = self.u_list_min[self.send_level - 1]
        else:
            self.pwr_voltage.value = flag

    # 变量赋值
    def config_varb(self):
        for num in range(len(self.md_list) - 1):
            self.equal_varb([self.md_list[num], -2], [self.md_list[num + 1], 0])
            self.equal_varb([self.md_list[num], -1], [self.md_list[num + 1], 1])

    def init_equs(self, freq):
        equs = EquationGroup()
        for module in self.md_list:
            module.init_equs(freq)
            equs.add_equations(module.equs)
        varb_U2 = self.md_list[-1].get_varb(-2)
        varb_I2 = self.md_list[-1].get_varb(-1)
        self.equs = equs.simplify_equs([varb_U2], [varb_I2], equ_name=self.name)
        # self.equs = equs
        return self.equs

    def refresh_coeffs(self, freq):
        for module in self.md_list:
            module.refresh_coeffs(freq)
        varb_U2 = self.md_list[-1].get_varb(-2)
        varb_I2 = self.md_list[-1].get_varb(-1)
        varb_U1 = self.md_list[0].get_varb(0)
        varb_I1 = self.md_list[0].get_varb(1)
        name = self.name
        equs = self.equs_cmplx.simplify_equs([varb_U1, varb_I1], [varb_U2, varb_I2], name=name)
        equs.add_equations(self.md_list[0].equs)
        self.equs.reload_coefficient(equs)
        return self.equs