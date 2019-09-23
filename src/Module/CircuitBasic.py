from src.Module.PortNetwork import *
from src.AbstractClass.Equation import *
from src.Module.ParameterType import *


# 并联阻抗
class OPortZ(OnePortNetwork):
    new_table = {
        '并联阻抗': 'z',
    }
    prop_table = OnePortNetwork.prop_table.copy()
    prop_table.update(new_table)

    # 变量类型
    para_type = {
        'z': VariableImpedance}

    def __init__(self, parent_ins, name_base, z):
        super().__init__(parent_ins, name_base)
        self.z = z

    def get_equs(self, freq):
        z = self.z[freq].z
        equs = self.value2equs(z)
        return equs

    def value2equs(self, z):
        equ1 = Equation(name=self.name + '_方程')
        equ1.add_items(EquItem(self['U'], -1),
                       EquItem(self['I'], z))
        self.equs = EquationGroup(equ1)
        return self.equs


########################################################################################################################

# 并联电压源
class OPortPowerU(OnePortNetwork):
    new_table = {
        '电压值': 'voltage',
    }
    prop_table = OnePortNetwork.prop_table.copy()
    prop_table.update(new_table)

    # 变量类型
    para_type = {
        'voltage': Constant}

    def __init__(self, parent_ins, name_base, voltage=0):
        super().__init__(parent_ins, name_base)
        self.voltage = voltage

    def get_equs(self, freq):
        _ = freq
        equs = self.value2equs(self.voltage)
        return equs

    def value2equs(self, voltage):
        equ1 = Equation(name=self.name + '_方程',
                        constant=voltage)
        equ1.add_items(EquItem(self['U'], 1))
        self.equs = EquationGroup(equ1)
        return self.equs


# 并联电流源
class OPortPowerI(OnePortNetwork):
    new_table = {
        '电流值': 'current',
    }
    prop_table = OnePortNetwork.prop_table.copy()
    prop_table.update(new_table)

    # 变量类型
    para_type = {
        'current': Constant}

    def __init__(self, parent_ins, name_base, current=0):
        super().__init__(parent_ins, name_base)
        self.current = current

    def get_equs(self, freq):
        _ = freq
        equs = self.value2equs(self.current)
        return equs

    def value2equs(self, current):
        equ1 = Equation(name=self.name + '_方程',
                        constant=current)
        equ1.add_items(EquItem(self['I'], 1))
        self.equs = EquationGroup(equ1)
        return self.equs


########################################################################################################################

# Pi型二端口网络
class TPortCircuitPi(TwoPortNetwork):
    new_table = {
        '阻抗1': 'y1',
        '阻抗2': 'y2',
        '阻抗3': 'y3'
    }
    prop_table = TwoPortNetwork.prop_table.copy()
    prop_table.update(new_table)

    # 变量类型
    para_type = {
        'y1': VariableImpedance,
        'y2': VariableImpedance,
        'y3': VariableImpedance}

    def __init__(self, parent_ins, name_base, y1, y2, y3):
        super().__init__(parent_ins, name_base)
        self.y1 = y1
        self.y2 = y2
        self.y3 = y3

    def get_equs(self, freq):
        y1 = self.y1[freq].z
        y2 = self.y2[freq].z
        y3 = self.y3[freq].z
        equs = self.value2equs(y1, y2, y3)
        return equs

    def value2equs(self, y1, y2, y3):
        equ1 = Equation(name=self.name+'_方程1')
        equ2 = Equation(name=self.name+'_方程2')
        equ1.add_items(EquItem(self['I1'], -1),
                       EquItem(self['U1'], -(y1 + y2)),
                       EquItem(self['U2'], +y2))
        equ2.add_items(EquItem(self['I2'], -1),
                       EquItem(self['U1'], -y2),
                       EquItem(self['U2'], (y2 + y3)))
        self.equs = EquationGroup(equ1, equ2)
        return self.equs


# T型二端口网络
class TPortCircuitT(TwoPortNetwork):
    new_table = {
        '阻抗1': 'z1',
        '阻抗2': 'z2',
        '阻抗3': 'z3'
    }
    prop_table = TwoPortNetwork.prop_table.copy()
    prop_table.update(new_table)

    # 变量类型
    para_type = {
        'z1': VariableImpedance,
        'z2': VariableImpedance,
        'z3': VariableImpedance}

    def __init__(self, parent_ins, name_base, z1, z2, z3):
        super().__init__(parent_ins, name_base)
        self.z1 = z1
        self.z2 = z2
        self.z3 = z3

    def get_equs(self, freq):
        z1 = self.z1[freq].z
        z2 = self.z2[freq].z
        z3 = self.z3[freq].z
        equs = self.value2equs(z1, z2, z3)
        return equs

    def value2equs(self, z1, z2, z3):
        equ1 = Equation(name=self.name+'_方程1')
        equ2 = Equation(name=self.name+'_方程2')
        equ1.add_items(EquItem(self['U1'], -1),
                       EquItem(self['I1'], -(z1 + z2)),
                       EquItem(self['I2'], z2))
        equ2.add_items(EquItem(self['U2'], -1),
                       EquItem(self['I1'], -z2),
                       EquItem(self['I2'], (z2 + z3)))
        self.equs = EquationGroup(equ1, equ2)
        return self.equs


########################################################################################################################

# 变压器二端口网络
class TPortCircuitN(TwoPortNetwork):
    new_table = {
        '变比': 'n',
    }
    prop_table = TwoPortNetwork.prop_table.copy()
    prop_table.update(new_table)

    # 变量类型
    para_type = {
        'n': VariableByFreq}

    def __init__(self, parent_ins, name_base, n):
        super().__init__(parent_ins, name_base)
        self.n = n

    def get_equs(self, freq):
        n = self.n[freq]
        equs = self.value2equs(n)
        return equs

    def value2equs(self, n):
        equ1 = Equation(name=self.name+'_方程1')
        equ2 = Equation(name=self.name+'_方程2')
        equ1.add_items(EquItem(self['U1'], -1),
                       EquItem(self['U2'], n))
        equ2.add_items(EquItem(self['I1'], n),
                       EquItem(self['I2'], -1))
        self.equs = EquationGroup(equ1, equ2)
        return self.equs


# 串联二端口网络
class TPortZSeries(TwoPortNetwork):
    new_table = {
        '串联阻抗': 'z',
    }
    prop_table = TwoPortNetwork.prop_table.copy()
    prop_table.update(new_table)

    # 变量类型
    para_type = {
        'z': VariableImpedance}

    def __init__(self, parent_ins, name_base, z):
        super().__init__(parent_ins, name_base)
        self.z = z

    def get_equs(self, freq):
        z = self.z[freq].z
        equs = self.value2equs(z)
        return equs

    def value2equs(self, z):
        equ1 = Equation(name=self.name+'_方程1')
        equ2 = Equation(name=self.name+'_方程2')
        equ1.add_items(EquItem(self['U1'], 1),
                       EquItem(self['U2'], -1),
                       EquItem(self['I2'], z))
        equ2.add_items(EquItem(self['I1'], -1),
                       EquItem(self['I2'], 1))
        self.equs = EquationGroup(equ1, equ2)
        return self.equs


# 并联二端口网络
class TPortZParallel(TwoPortNetwork):
    new_table = {
        '并联阻抗': 'z',
    }
    prop_table = TwoPortNetwork.prop_table.copy()
    prop_table.update(new_table)

    # 变量类型
    para_type = {
        'z': VariableImpedance}

    def __init__(self, parent_ins, name_base, z):
        super().__init__(parent_ins, name_base)
        self.z = z

    def get_equs(self, freq):
        z = self.z[freq].z
        equs = self.value2equs(z)
        return equs

    def value2equs(self, z):
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
