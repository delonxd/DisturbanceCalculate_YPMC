from src.PortNetwork import OnePortNetwork, TwoPortNetwork
from src.Equation import Equation

# 并联阻抗
class OPortZ(OnePortNetwork):
    new_table = {
        '并联阻抗': 'z',
    }
    prop_table = OnePortNetwork.prop_table.copy()
    prop_table.update(new_table)

    def __init__(self, parent_ins, name_base, z):
        super().__init__(parent_ins, name_base)
        self.z = z

    def get_equs(self, freq):
        z = self.z[freq].z
        equ1 = Equation(varbs=[self['U'], self['I']], values=[-1, z])
        self.equs = [equ1]


########################################################################################################################

# 并联电压源
class OPortPowerU(OnePortNetwork):
    new_table = {
        '电压值': 'voltage',
    }
    prop_table = OnePortNetwork.prop_table.copy()
    prop_table.update(new_table)

    def __init__(self, parent_ins, name_base, voltage=0):
        super().__init__(parent_ins, name_base)
        self.voltage = voltage

    def get_equs(self, freq):
        equ1 = Equation(varbs=[self['U']], values=[1])
        self.equs = [equ1]

# 并联电流源
class OPortPowerI(OnePortNetwork):
    new_table = {
        '电流值': 'current',
    }
    prop_table = OnePortNetwork.prop_table.copy()
    prop_table.update(new_table)

    def __init__(self, parent_ins, name_base, current=0):
        super().__init__(parent_ins, name_base)
        self.current = current

    def get_equs(self, freq):
        equ1 = Equation(varbs=[self['I']], values=[1])
        self.equs = [equ1]


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

    def __init__(self, parent_ins, name_base, y1, y2, y3):
        super().__init__(parent_ins, name_base)
        self.y1 = y1
        self.y2 = y2
        self.y3 = y3

    def get_equs(self, freq):
        y1 = self.y1[freq].z
        y2 = self.y2[freq].z
        y3 = self.y3[freq].z
        equ1 = Equation(varbs=[self['I1'], self['U1'], self['U2']],
                        values=[-1, -(y1 + y2), -y2])
        equ2 = Equation(varbs=[self['I2'], self['U1'], self['U2']],
                        values=[-1, -y2, (y2 + y3)])
        self.equs = [equ1, equ2]


# T型二端口网络
class TPortCircuitT(TwoPortNetwork):
    new_table = {
        '阻抗1': 'z1',
        '阻抗2': 'z2',
        '阻抗3': 'z3'
    }
    prop_table = TwoPortNetwork.prop_table.copy()
    prop_table.update(new_table)

    def __init__(self, parent_ins, name_base, z1, z2, z3):
        super().__init__(parent_ins, name_base)
        self.z1 = z1
        self.z2 = z2
        self.z3 = z3

    def get_equs(self, freq):
        z1 = self.z1[freq].z
        z2 = self.z2[freq].z
        z3 = self.z3[freq].z
        equ1 = Equation(varbs=[self['U1'], self['I1'], self['I2']],
                        values=[-1, -(z1 + z2), z2])
        equ2 = Equation(varbs=[self['U2'], self['I1'], self['I2']],
                        values=[-1, -z2, (z2 + z3)])
        self.equs = [equ1, equ2]


########################################################################################################################

# 变压器二端口网络
class TPortCircuitN(TwoPortNetwork):
    new_table = {
        '变比': 'n',
    }
    prop_table = TwoPortNetwork.prop_table.copy()
    prop_table.update(new_table)

    def __init__(self, parent_ins, name_base, n):
        super().__init__(parent_ins, name_base)
        self.n = n

    def get_equs(self, freq):
        n = self.n[freq]
        equ1 = Equation(varbs=[self['U1'], self['U2']],
                        values=[-1, n])
        equ2 = Equation(varbs=[self['I1'], self['I2']],
                        values=[n, -1])
        self.equs = [equ1, equ2]


# 串联二端口网络
class TPortZSeries(TwoPortNetwork):
    new_table = {
        '串联阻抗': 'z',
    }
    prop_table = TwoPortNetwork.prop_table.copy()
    prop_table.update(new_table)

    def __init__(self, parent_ins, name_base, z):
        super().__init__(parent_ins, name_base)
        self.z = z

    def get_equs(self, freq):
        z = self.z[freq].z
        equ1 = Equation(varbs=[self['U1'], self['U2'], self['I2']],
                        values=[1, -1, z])
        equ2 = Equation(varbs=[self['I1'], self['I2']],
                        values=[-1, 1])
        self.equs = [equ1, equ2]


# 并联二端口网络
class TPortZParallel(TwoPortNetwork):
    new_table = {
        '并联阻抗': 'z',
    }
    prop_table = TwoPortNetwork.prop_table.copy()
    prop_table.update(new_table)

    def __init__(self, parent_ins, name_base, z):
        super().__init__(parent_ins, name_base)
        self.z = z

    def get_equs(self, freq):
        z = self.z[freq].z
        equ1 = Equation(varbs=[self['U1'], self['I1'], self['I2']],
                        values=[-1, -z, z])
        equ2 = Equation(varbs=[self['U2'], self['I1'], self['I2']],
                        values=[-1, -z, z])
        self.equs = [equ1, equ2]
