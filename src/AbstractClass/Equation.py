from src.AbstractClass.Varb import *
import numpy as np
import numpy.matlib


# 方程组
class EquationGroup:
    def __init__(self, *equs):
        self.equs = list()
        # self.equ_dict = dict()
        self.varbs = VarbGroup()
        self.m_matrix = None
        self.constant = None
        self.solution = None
        for equ in equs:
            self.add_equation(equ)

    # 获取变量
    def get_varbs(self):
        varbs = VarbGroup()
        for equ in self.equs:
            varbs.add_varbs(equ.varbs)
        self.varbs = varbs
        return varbs

    # 添加方程式
    def add_equation(self, equ):
        if isinstance(equ, Equation):
            # if equ.name in self.equ_dict.keys():
            #     raise KeyboardInterrupt('名称异常: 方程名称重复')
            # else:
            self.equs.append(equ)
            self.equ_dict[equ.name] = equ
        elif equ is None:
            pass
        else:
            raise KeyboardInterrupt('类型异常: 需添加Equation类型')

    # 添加方程组
    def add_equations(self, equs):
        if isinstance(equs, EquationGroup):
            for equ in equs.equs:
                self.add_equation(equ)
        elif equs is None:
            pass
        else:
            raise KeyboardInterrupt('类型异常: 需添加EquationGroup类型')

    # @property
    # def equ_names(self):
    #     name_list = list(self.equ_dict.keys())
    #     name_list.sort()
    #     return name_list

    @property
    def equ_dict(self):
        equ_dict = dict()
        for equ in self.equs:
            equ_dict[equ.name] = equ
        return equ_dict

    @property
    def equ_names(self):
        name_list = list()
        for equ in self.equs:
            name = equ.name
            if name in name_list:
                raise KeyboardInterrupt('名称异常: 变量名称重复')
            else:
                name_list.append(name)
        name_list.sort()
        return name_list

    # 设置方程编号
    def config_equ_num(self):
        name_list = self.equ_names
        num = 0
        for name in name_list:
            equ = self.equ_dict[name]
            # equ.num = num
            equ.num[self] = num
            num += 1

    # 设置方程编号
    def config_varb_num(self):
        varbs = self.get_varbs()
        varbs.config_varb_num(self)

    # 创建矩阵
    def creat_matrix(self):
        len_row = len(self)
        len_column = len(self.varbs)
        m_matrix = np.matlib.zeros((len_row, len_column), dtype=complex)
        constant = np.zeros(len_row, dtype=complex)

        for equ in self.equs:
            row = equ.num[self]
            equ.get_varbs_num_list(self)
            columns = equ.varbs_num_list[self]
            m_matrix[row, columns] = equ.coeff_list
            constant[row] = equ.constant
        self.m_matrix, self.constant = m_matrix, constant
        return m_matrix, constant

    def solve_matrix(self):
        self.solution = np.linalg.solve(self.m_matrix, self.constant)
        self.set_varbs_solution()

    def set_varbs_solution(self):
        for varb in self.varbs.varb_set:
            varb.value = self.solution[varb.num[self]]
            varb.value_c = abs(varb.value)

    # 方程按名称排序
    def sort_by_name(self):
        name_list = self.equ_names
        equ_list = list()
        for name in name_list:
            equ = self.equ_dict[name]
            equ_list.append(equ)
        self.equs = equ_list

    def set_type(self, equ_type):
        for equ in self.equs:
            equ.equ_type = equ_type

    def set_src_ele(self, ele):
        for equ in self.equs:
            equ.src_ele = ele

    def __len__(self):
        return len(self.equs)


# 方程项
class EquItem:
    def __init__(self, varb=None, coefficient=None):
        self.varb = varb
        self.coefficient = coefficient


# 方程
class Equation:
    def __init__(self, *items, name='', constant=0, equ_type=None):
        self.name = name
        self.equ_type = equ_type
        self.src_ele = None
        self.num = dict()

        self.varb_list = list()
        self.coeff_list = list()
        self.varbs_num_list = dict()
        self.constant = constant

    def get_varbs_num_list(self, equs):
        num_list = list()
        for varb in self.varb_list:
            num_list.append(varb.num[equs])
        num_list = np.array(num_list, dtype=int)
        self.varbs_num_list[equs] = num_list
        return num_list

    def set_type(self, equ_type):
        self.equ_type = equ_type

    def set_src_ele(self, ele):
        self.src_ele = ele

    @property
    def varbs(self):
        varbs = VarbGroup()
        for varb in self.varb_list:
            varbs.add_varb(varb)
        return varbs


if __name__ == '__main__':
    key1, key2 = 'aa', 'bb'
    e1 = Equation()
    a = 1
