from src.ElePack import ElePack
from src.BasicCircuitModel import *
from src.Equation import *

########################################################################################################################


# 发送器模型
class TcsrPower(ElePack):
    new_table = {
        '发送器内阻': 'z',
        '发送电平级': 'level',
    }
    prop_table = ElePack.prop_table.copy()
    prop_table.update(new_table)

    def __init__(self, parent_ins, name_base, z, level):
        super().__init__(parent_ins, name_base)
        self.flag_ele_list = True
        # self.z = z
        self.add_element('1电压源', OPortPowerU(self, '1电压源'))
        self.add_element('2内阻', TcsrPowerZ(self, '2内阻', z, level))

    @property
    def z(self):
        return self.element['2内阻'].z

    @z.setter
    def z(self, value):
        self.element['2内阻'].z = value

    @property
    def level(self):
        return self.element['2内阻'].level

    @level.setter
    def level(self, value):
        self.element['2内阻'].level = value


########################################################################################################################

# 发送器内阻
class TcsrPowerZ(TwoPortNetwork):
    new_table = {
        '阻抗': 'z',
        '电平级': 'level',
    }
    prop_table = TwoPortNetwork.prop_table.copy()
    prop_table.update(new_table)

    def __init__(self, parent_ins, name_base, z, level):
        super().__init__(parent_ins, name_base)
        self.z = z
        self.level = level

    # def get_equs(self, freq):
    #     z = self.z[self.level][freq].z
    #     equ1 = Equation(varbs=[self['U1'], self['U2'], self['I2']],
    #                     values=[1, -1, z])
    #     equ2 = Equation(varbs=[self['I1'], self['I2']],
    #                     values=[-1, 1])
    #     self.equs = [equ1, equ2]

    def get_equs(self, freq):
        z = self.z[self.level][freq].z
        equ1 = Equation(name=self.name+'_方程1')
        equ2 = Equation(name=self.name+'_方程2')
        equ1.add_items(EquItem(self['U1'], 1),
                       EquItem(self['U2'], -1),
                       EquItem(self['I2'], z))
        equ2.add_items(EquItem(self['I1'], -1),
                       EquItem(self['I2'], 1))
        self.equs = EquationGroup(equ1, equ2)
        return self.equs


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

    # def get_equs(self, freq):
    #     z = self.z[self.m_freq][freq].z
    #     equ1 = Equation(varbs=[self['U1'], self['I1'], self['I2']],
    #                     values=[-1, -z, z])
    #     equ2 = Equation(varbs=[self['U2'], self['I1'], self['I2']],
    #                     values=[-1, -z, z])
    #     self.equs = [equ1, equ2]

    def get_equs(self, freq):
        z = self.z[self.m_freq][freq].z
        equ1 = Equation(name=self.name+'_方程1')
        equ2 = Equation(name=self.name+'_方程2')
        equ1.add_items(EquItem(self['U1'], -1),
                       EquItem(self['I1'], -z),
                       EquItem(self['I2'], z))
        equ2.add_items(EquItem(self['U2'], -1),
                       EquItem(self['I1'], -z),
                       EquItem(self['I2'], z))
        self.equs = EquationGroup(equ1, equ2)
        return self.equs

    @property
    def m_freq(self):
        return self.parent_ins.m_freq


########################################################################################################################

# 引接线
class TcsrCA(TPortZSeries):
    def __init__(self, parent_ins, name_base, z):
        super().__init__(parent_ins, name_base, z)
