

# 方程
class Equation:
    def __init__(self, varbs=None, values=None, constant=0, name=''):
        self.name = name
        if varbs is not None:
            self.vb_list = list(zip(varbs, values))
        else:
            self.vb_list = []
        self.constant = constant

    def set_varbs(self, varbs, values):
        self.vb_list = list(zip(varbs, values))

    def add_varb(self, varb, value):
        tuple1 = (varb, value)
        self.vb_list.append(tuple1)