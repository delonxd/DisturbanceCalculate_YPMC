from src.AbstractClass.Varb import *


# 方程组
class EquationGroup:
    def __init__(self, *equs):
        self.equs = list()
        self.equ_dict = dict()
        for equ in equs:
            self.add_equation(equ)

    def get_varbs(self):
        varbs = VarbGroup()
        for equ in self.equs:
            varbs.add_varbs(equ.varbs)
        return varbs

    def add_equation(self, equ):
        if isinstance(equ, Equation):
            if equ.name in self.equ_dict.keys():
                raise KeyboardInterrupt('名称异常: 方程名称重复')
            else:
                self.equs.append(equ)
                self.equ_dict[equ.name] = equ
        elif equ is None:
            pass
        else:
            raise KeyboardInterrupt('类型异常: 需添加Equation类型')

    def add_equations(self, equs):
        if isinstance(equs, EquationGroup):
            for equ in equs.equs:
                self.add_equation(equ)
        elif equs is None:
            pass
        else:
            raise KeyboardInterrupt('类型异常: 需添加EquationGroup类型')

    @property
    def equ_names(self):
        name_list = list(self.equ_dict.keys())
        name_list.sort()
        return name_list

    # 方程按名称排序
    def sort_by_name(self):
        name_list = self.equ_names
        equ_list = list()
        for name in name_list:
            equ = self.equ_dict[name]
            equ_list.append(equ)
        self.equs = equ_list

    def __len__(self):
        return len(self.equs)


# 方程项
class EquItem:
    def __init__(self, varb=None, coefficient=None):
        self.varb = varb
        self.coefficient = coefficient

# # 方程
# class Equation:
#     def __init__(self, varbs=None, values=None, constant=0, name=''):
#         self.name = name
#         if varbs is not None:
#             self.vb_list = list(zip(varbs, values))
#         else:
#             self.vb_list = []
#         self.constant = constant
#
#     def set_varbs(self, varbs, values):
#         self.vb_list = list(zip(varbs, values))
#
#     def add_varb(self, varb, value):
#         tuple1 = (varb, value)
#         self.vb_list.append(tuple1)


# 方程
class Equation:
    def __init__(self, *items, name='', constant=0):
        self.name = name
        self.items = set()
        self.constant = constant
        self.set_items(items)

    def set_items(self, items):
        self.items = set()
        for item in items:
            self.items.add(item)

    def add_items(self, *items):
        for item in items:
            self.items.add(item)

    @property
    def varbs(self):
        varbs = VarbGroup()
        for item in self.items:
            varbs.add_varb(item.varb)
        return varbs


if __name__ == '__main__':
    key1, key2 = 'aa', 'bb'
    e1 = Equation()
    e1.add_items(EquItem(key1, -1), EquItem(key2, 3))
    a = 1
