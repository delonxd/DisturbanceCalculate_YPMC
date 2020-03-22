from src.Module.PortNetwork import *

class JumperWire(OnePortNetwork):
    def __init__(self, parent_ins, name_base, posi):
        super().__init__(parent_ins, name_base)
        self.init_position(posi)
        self.flag_ele_unit = True
        self.jumpergroup = [self]

    def init_equs(self, freq):
        equs = EquationGroup()
        group_index = self.jumpergroup.index(self)

        ele_last = self.jumpergroup[-1]
        for ele in self.jumpergroup[:-1]:
            equ = Equation()
            equ.varb_list = [ele['U'], ele_last['U']]
            equ.coeff_list = [1, -1]
            equs.add_equation(equ)

        equ = Equation()
        for ele in self.jumpergroup:
            equ.varb_list.append(ele['I'])
            equ.coeff_list.append(1)
        equs.add_equation(equ)

        self.equ1 = equs.equs[group_index]
        self.equ1 = self.name + '_跳线组方程' + str(group_index)

        self.equs = EquationGroup()
        self.equs.add_equation(self.equ1)
