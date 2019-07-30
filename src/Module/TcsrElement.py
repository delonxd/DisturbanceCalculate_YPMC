from src.Module.CircuitBasic import *


########################################################################################################################


# 发送器模型
class TcsrPower(ElePack):
    new_table = {
        '发送器内阻': 'z',
        '发送电平级': 'level',
    }
    prop_table = ElePack.prop_table.copy()
    prop_table.update(new_table)

    def __init__(self, parent_ins, name_base, z):
        super().__init__(parent_ins, name_base)
        self.flag_ele_list = True
        self.add_element('1电压源', OPortPowerU(self, '1电压源', voltage=0))
        self.add_element('2内阻', TcsrPowerZ(self, '2内阻', z))

    @property
    def voltage(self):
        voltage_list = [183, 164, 142, 115, 81.5, 68, 60.5, 48.6, 40.8]
        voltage = voltage_list[self.level + 1]
        return voltage

    @property
    def z(self):
        return self.element['2内阻'].z

    @z.setter
    def z(self, value):
        self.element['2内阻'].z = value

    @property
    def level(self):
        return self.parent_ins.send_level

    @level.setter
    def level(self, value):
        self.parent_ins.send_level = value


########################################################################################################################

# 发送器内阻
class TcsrPowerZ(TPortZSeries):
    new_table = {
        '电平级': 'level'
    }
    prop_table = TPortZSeries.prop_table.copy()
    prop_table.update(new_table)

    def __init__(self, parent_ins, name_base, z):
        super().__init__(parent_ins, name_base, z)

    @property
    def level(self):
        return self.parent_ins.level

    @level.setter
    def level(self, value):
        self.parent_ins.level = value

    def get_equs(self, freq):
        z = self.z[self.level][freq].z
        equs = self.value2equs(z)
        return equs


########################################################################################################################

# 接收器
class TcsrReceiver(OPortZ):
    def __init__(self, parent_ins, name_base, z):
        super().__init__(parent_ins, name_base, z)


########################################################################################################################

# 变压器模板
class TcsrTransformer(ElePack):
    def __init__(self, parent_ins, name_base, z1, z2, n):
        super().__init__(parent_ins, name_base)
        self.flag_ele_list = True
        self.add_element('1等效内阻', TPortCircuitT(self, '1等效内阻', z1, z2, z1))
        self.add_element('2变压器', TPortCircuitN(self, '2变压器', n))


########################################################################################################################

# 防雷变压器
class TcsrFL(TcsrTransformer):
    def __init__(self, parent_ins, name_base, z1, z2, n):
        super().__init__(parent_ins, name_base, z1, z2, n)


########################################################################################################################

# TAD变压器
class TcsrTAD(ElePack):
    def __init__(self, parent_ins, name_base, z1, z2, z3, n, zc):
        super().__init__(parent_ins, name_base)
        self.flag_ele_list = True
        self.add_element('1共模电感', TPortZSeries(self, '1共模电感', z3))
        self.add_element('2等效内阻', TPortCircuitT(self, '2等效内阻', z1, z2, z1))
        self.add_element('3变压器', TPortCircuitN(self, '3变压器', n))
        self.add_element('4串联电容', TPortZSeries(self, '4串联电容', zc))


########################################################################################################################

# 匹配单元
class TcsrBA(TPortZParallel):
    def __init__(self, parent_ins, name_base, z):
        super().__init__(parent_ins, name_base, z)

    def get_equs(self, freq):
        z = self.z[self.m_freq][freq].z
        equs = self.value2equs(z)
        return equs

    @property
    def m_freq(self):
        return self.parent_ins.m_freq


########################################################################################################################

# 引接线
class TcsrCA(TPortZSeries):
    def __init__(self, parent_ins, name_base, z):
        super().__init__(parent_ins, name_base, z)
