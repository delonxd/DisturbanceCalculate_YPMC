import numpy as np
from src.PortNetwork import *
from src.Equation import *


# 电缆等效电路
class TPortCable(TwoPortNetwork):
    new_table = {
        '电阻': 'R',
        '电感': 'L',
        '电容': 'C',
        '电缆长度': 'length',
    }
    prop_table = TwoPortNetwork.prop_table.copy()
    prop_table.update(new_table)

    def __init__(self, parent_ins, name_base, length, cab_r=43, cab_l=825e-6, cab_c=28e-9):
        super().__init__(parent_ins, name_base)
        self.R = cab_r
        self.L = cab_l
        self.C = cab_c
        self.length = length

    def get_equs(self, freq):
        length = self.length
        w = 2 * np.pi * freq
        z0 = self.R + 1j * w * self.L
        y0 = 1j * w * self.C
        zc = np.sqrt(z0 / y0)
        gama = np.sqrt(z0 * y0)
        zii = zc * np.sinh(gama * length)
        yii = (np.cosh(gama * length) - 1) / zc / np.sinh(gama * length)
        y1 = yii
        y2 = 1 / zii
        y3 = yii
        equ1 = Equation(varbs=[self['I1'], self['U1'], self['U2']],
                        values=[-1, -(y1 + y2), -y2])
        equ2 = Equation(varbs=[self['I2'], self['U1'], self['U2']],
                        values=[-1, -y2, (y2 + y3)])
        self.equs = [equ1, equ2]
