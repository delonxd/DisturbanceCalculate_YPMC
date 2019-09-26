from src.AbstractClass.ElePack import *
from src.Module.OutsideElement import JumperWireOutside
from src.AbstractClass.Equation import *


# 跳线连接
class JumperWireConnection(ElePack):
    def __init__(self, name_base, m_line, turnout, posi_abs):
        parent_ins = None
        name = turnout.name_base + '' + name_base
        super().__init__(parent_ins, name)
        # self.parameter = parameter

        # 为主轨添加跳线
        jumper1 = JumperWireOutside(parent_ins=m_line, name_base=name, posi=posi_abs)
        m_line.add_child(name, jumper1)
        jumper1.set_posi_abs(0)
        self.jumper1 = jumper1

        # 为岔区添加跳线
        jumper2 = JumperWireOutside(parent_ins=turnout, name_base=name_base, posi=posi_abs)
        turnout.add_child(name_base, jumper2)
        jumper2.set_posi_abs(0)
        self.jumper2 = jumper2

        self.set_ele_name(prefix='')
        self.equs = list()

    def get_equs(self):
        equ1 = Equation(name=self.name + '_方程1', constant=0)
        equ2 = Equation(name=self.name + '_方程2', constant=0)
        equ1.add_items(EquItem(self.jumper1['U'], 1),
                       EquItem(self.jumper2['U'], -1))
        equ2.add_items(EquItem(self.jumper1['I'], 1),
                       EquItem(self.jumper2['I'], 1))
        self.equs = EquationGroup(equ1, equ2)
        return self.equs
