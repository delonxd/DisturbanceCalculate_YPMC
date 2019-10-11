from src.AbstractClass.EleModule import *
from src.AbstractClass.Varb import *
from src.AbstractClass.Equation import *


# 一端口元件
class OnePortNetwork(EleModule):
    def __init__(self, parent_ins, name_base):
        super().__init__(parent_ins, name_base)
        self.varb_name = ['U', 'I']
        self.varb_dict = {'U': Varb(self, 'U'),
                          'I': Varb(self, 'I')}
        self.equ1 = Equation()
        self.equs.add_equation(self.equ1)


# 二端口网络
class TwoPortNetwork(EleModule):
    def __init__(self, parent_ins, name_base):
        super().__init__(parent_ins, name_base)
        self.varb_name = ['U1', 'I1', 'U2', 'I2']
        self.varb_dict = {'U1': Varb(self, 'U1'),
                          'I1': Varb(self, 'I1'),
                          'U2': Varb(self, 'U2'),
                          'I2': Varb(self, 'I2')}
        self.equ1 = Equation()
        self.equ2 = Equation()
        self.equs.add_equation(self.equ1)
        self.equs.add_equation(self.equ2)