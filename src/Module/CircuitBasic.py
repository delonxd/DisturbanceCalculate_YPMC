from src.Module.PortNetwork import *
from src.AbstractClass.Equation import *
from src.Module.ParameterType import *
import numpy as np


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

    def init_equs(self, freq):
        self.equ1.name = self.name + '_方程'
        self.equ1.varb_list = [self['U'], self['I']]
        self.get_coeffs(freq)

    def get_coeffs(self, freq):
        z = self.z[freq].z
        self.value2coeffs(z)
        return self.equs

    def value2coeffs(self, z):
        self.equ1.coeff_list = np.array([-1, z])


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

    def init_equs(self, freq):
        self.equ1.name = self.name + '_方程'
        self.equ1.varb_list = [self['U']]
        self.get_coeffs(freq)

    def get_coeffs(self, freq):
        voltage = float(self.voltage)
        self.value2coeffs(voltage)
        return self.equs

    def value2coeffs(self, voltage):
        self.equ1.coeff_list = np.array([1])
        self.equ1.constant = voltage


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

    def init_equs(self, freq):
        self.equ1.name = self.name + '_方程'
        self.equ1.varb_list = [self['I']]
        self.get_coeffs(freq)

    def get_coeffs(self, freq):
        current = float(self.current)
        self.value2coeffs(current)
        return self.equs

    def value2coeffs(self, current):
        self.equ1.coeff_list = np.array([1])
        self.equ1.constant = current


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

    def init_equs(self, freq):
        self.equ1.name = self.name + '_方程1'
        self.equ2.name = self.name + '_方程2'
        self.equ1.varb_list = [self['I1'], self['U1'], self['U2']]
        self.equ2.varb_list = [self['I2'], self['U1'], self['U2']]
        self.get_coeffs(freq)

    def get_coeffs(self, freq):
        y1 = self.y1[freq].z
        y2 = self.y2[freq].z
        y3 = self.y3[freq].z
        self.value2coeffs(y1, y2, y3)
        return self.equs

    def value2coeffs(self, y1, y2, y3):
        self.equ1.coeff_list = np.array([-1, -(y1 + y2), +y2])
        self.equ2.coeff_list = np.array([-1, -y2, +(y2 + y3)])


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

    def init_equs(self, freq):
        self.equ1.name = self.name + '_方程1'
        self.equ2.name = self.name + '_方程2'
        self.equ1.varb_list = [self['U1'], self['I1'], self['I2']]
        self.equ2.varb_list = [self['U2'], self['I1'], self['I2']]
        self.get_coeffs(freq)

    def get_coeffs(self, freq):
        z1 = self.z1[freq].z
        z2 = self.z2[freq].z
        z3 = self.z3[freq].z
        self.value2coeffs(z1, z2, z3)
        return self.equs

    def value2coeffs(self, z1, z2, z3):
        self.equ1.coeff_list = np.array([-1, -(z1 + z2), +z2])
        self.equ2.coeff_list = np.array([-1, -z2, +(z2 + z3)])


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

    def init_equs(self, freq):
        self.equ1.name = self.name + '_方程1'
        self.equ2.name = self.name + '_方程2'
        self.equ1.varb_list = [self['U1'], self['U2']]
        self.equ2.varb_list = [self['I1'], self['I2']]
        self.get_coeffs(freq)

    def get_coeffs(self, freq):
        n = self.n[freq]
        self.value2coeffs(n)
        return self.equs

    def value2coeffs(self, n):
        self.equ1.coeff_list = np.array([-1, n])
        self.equ2.coeff_list = np.array([n, -1])


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

    def init_equs(self, freq):
        self.equ1.name = self.name + '_方程1'
        self.equ2.name = self.name + '_方程2'
        self.equ1.varb_list = [self['U1'], self['U2'], self['I2']]
        self.equ2.varb_list = [self['I1'], self['I2']]
        self.get_coeffs(freq)

    def get_coeffs(self, freq):
        z = self.z[freq].z
        self.value2coeffs(z)
        return self.equs

    def value2coeffs(self, z):
        self.equ1.coeff_list = np.array([1, -1, z])
        self.equ2.coeff_list = np.array([-1, 1])


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

    def init_equs(self, freq):
        self.equ1.name = self.name + '_方程1'
        self.equ2.name = self.name + '_方程2'
        self.equ1.varb_list = [self['U1'], self['I1'], self['I2']]
        # self.equ2.varb_list = [self['U2'], self['I1'], self['I2']]
        self.equ2.varb_list = [self['U2'], self['U1']]
        self.get_coeffs(freq)

    def get_coeffs(self, freq):
        z = self.z[freq].z
        self.value2coeffs(z)
        return self.equs

    def value2coeffs(self, z):
        self.equ1.coeff_list = np.array([-1, -z, z])
        # self.equ2.coeff_list = np.array([-1, -z, z])
        self.equ2.coeff_list = np.array([-1, 1])


# 传输矩阵二端口网络（ABCD）
class TPortABCD_re(TwoPortNetwork):
    new_table = {
        '参数11': 'a',
        '参数12': 'b',
        '参数21': 'c',
        '参数22': 'd'
    }
    prop_table = TwoPortNetwork.prop_table.copy()
    prop_table.update(new_table)

    # 变量类型
    para_type = {
        'a': VariableImpedance,
        'b': VariableImpedance,
        'c': VariableImpedance,
        'd': VariableImpedance,}

    def __init__(self, parent_ins, name_base, p1, p2, p3, p4):
        super().__init__(parent_ins, name_base)
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def init_equs(self, freq):
        self.equ1.name = self.name + '_方程1'
        self.equ2.name = self.name + '_方程2'
        self.equ1.varb_list = [self['U2'], self['U1'], self['I1']]
        self.equ2.varb_list = [self['I2'], self['U1'], self['I1']]
        self.get_coeffs(freq)

    def get_coeffs(self, freq):
        p1 = self.p1[freq].z
        p2 = self.p2[freq].z
        p3 = self.p3[freq].z
        p4 = self.p4[freq].z
        self.value2coeffs(p1, p2, p3, p4)
        return self.equs

    def value2coeffs(self, p1, p2, p3, p4):
        self.equ1.coeff_list = np.array([-1, p1, p2])
        self.equ2.coeff_list = np.array([-1, p3, p4])


# 传输矩阵二端口网络（ABCD）
class TPortABCD_tr(TwoPortNetwork):
    new_table = {
        '参数11': 'a',
        '参数12': 'b',
        '参数21': 'c',
        '参数22': 'd'
    }
    prop_table = TwoPortNetwork.prop_table.copy()
    prop_table.update(new_table)

    # 变量类型
    para_type = {
        'a': VariableImpedance,
        'b': VariableImpedance,
        'c': VariableImpedance,
        'd': VariableImpedance,}

    def __init__(self, parent_ins, name_base, p1, p2, p3, p4):
        super().__init__(parent_ins, name_base)
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def init_equs(self, freq):
        self.equ1.name = self.name + '_方程1'
        self.equ2.name = self.name + '_方程2'
        self.equ1.varb_list = [self['U1'], self['U2'], self['I2']]
        self.equ2.varb_list = [self['I1'], self['U2'], self['I2']]
        self.get_coeffs(freq)

    def get_coeffs(self, freq):
        p1 = self.p1[freq].z
        p2 = self.p2[freq].z
        p3 = self.p3[freq].z
        p4 = self.p4[freq].z
        self.value2coeffs(p1, p2, p3, p4)
        return self.equs

    def value2coeffs(self, p1, p2, p3, p4):
        self.equ1.coeff_list = np.array([-1, p4, -p2])
        self.equ2.coeff_list = np.array([1, p3, -p1])