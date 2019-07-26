from src.BasicCircuitModel import OPortZ, OPortPowerU
from src.Equation import Equation

class UPowerOut(OPortPowerU):
    def __init__(self, parent_ins, name_base, posi):
        super().__init__(parent_ins, name_base)
        self.init_position(posi)
        self.flag_ele_unit = True


# 室外阻抗
class ZOutside(OPortZ):
    def __init__(self, parent_ins, name_base, posi, z):
        super().__init__(parent_ins, name_base, z)
        self.init_position(posi)
        self.flag_ele_unit = True


# 补偿电容
class CapC(ZOutside):
    def __init__(self, parent_ins, name_base, posi, z):
        super().__init__(parent_ins, name_base, posi, z)


# 空心线圈
class SVA(ZOutside):
    def __init__(self, parent_ins, name_base, posi, z):
        super().__init__(parent_ins, name_base, posi, z)


# TB
class TB(ZOutside):
    def __init__(self, parent_ins, name_base, posi, z):
        super().__init__(parent_ins, name_base, posi, z)


# 室外电阻
class ROutside(ZOutside):
    def __init__(self, parent_ins, name_base, posi, z):
        super().__init__(parent_ins, name_base, posi, z)

    def get_equs(self, freq):
        z = self.z
        equ1 = Equation(varbs=[self['U'], self['I']],
                        values=[-1, z])
        self.equs = [equ1]

