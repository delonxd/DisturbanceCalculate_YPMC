from src.AbstractClass.Varb import *
from src.AbstractClass.ElePack import *
import numpy as np
import numpy.matlib
import sympy as sp
from numba import jit


# 方程组
class EquationGroup:
    def __init__(self, *equs):
        self.equs = list()
        # self.equ_dict = dict()
        self.varbs = VarbGroup()
        self.len_row = None
        self.len_column = None

        self.equ_num = dict()
        self.varb_num = dict()

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
            # self.equ_dict[equ.name] = equ
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
        num = 0
        for equ in self.equs:
            self.equ_num[equ] = num
            num += 1

    # 设置方程编号
    def config_varb_num(self):
        varb_set = set()
        num = 0
        for equ in self.equs:
            for varb in equ.varb_list:
                if not varb in varb_set:
                    varb_set.add(varb)
                    self.varb_num[varb] = num
                    num += 1

    # 创建矩阵
    def creat_matrix(self):
        self.config_varb_num()
        self.config_equ_num()

        len_row = len(self)
        len_column = len(self.varb_num)
        m_matrix = np.zeros((len_row, len_column), dtype=complex)
        constant = np.zeros((len_row, 1), dtype=complex)

        for equ in self.equs:
            row = self.equ_num[equ]
            for varb, coeff in zip(equ.varb_list, equ.coeff_list):
                column = self.varb_num[varb]
                m_matrix[row, column] = coeff
            constant[row] = equ.constant
        self.m_matrix, self.constant = m_matrix, constant

        return m_matrix, constant

    def solve_matrix(self):
        # mtrx = sp.Matrix(self.m_matrix)
        # a = mtrx.rref()
        self.solution = np.linalg.solve(self.m_matrix, self.constant)
        # self.solution = self.constant
        self.set_varbs_solution()

    def set_varbs_solution(self):
        for varb, idx in self.varb_num.items():
            varb.value = self.solution[idx]
            varb.value = varb.value[0]
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

    def del_num(self):
        for equ in self.equs:
            equ.num.pop(self)
        for varb in self.varbs.varb_set:
            varb.num.pop(self)

    def reload_coefficient(self, equs):
        if len(self.equs) == len(equs.equs):
            for num in range(len(self.equs)):
                self.equs[num].reload_coefficient(equs.equs[num])
        else:
            raise KeyboardInterrupt('异常: 方程组数量不同')

    def __len__(self):
        return len(self.equs)


    def simplify_equs(self, varbs1, varbs2, equ_name):
        if len(self.equs) < 6:
            return self
        self.creat_matrix()
        num_varbs = np.array(range(self.m_matrix.shape[1]))

        columns = np.array([], dtype='int64')
        for varb2 in varbs2:
            columns = np.append(columns, self.varb_num[varb2])

        column_array = self.m_matrix[:, columns]

        num_varbs = np.delete(num_varbs, columns, axis=0)

        row_new = np.array([], dtype='int64')
        for varb1 in varbs1:
            num_t = np.argwhere(num_varbs == self.varb_num[varb1])
            row_new = np.append(row_new, num_t[0, 0])

        a_temp = np.delete(self.m_matrix, columns, axis=1)
        b_temp = np.hstack((column_array, self.constant))

        solution = np.linalg.solve(a_temp, b_temp)
        simple_equ = solution[row_new, :]

        equs = EquationGroup()

        m_new = np.hstack((np.eye(len(row_new), dtype=complex), simple_equ))
        b_new = m_new[:, -1]
        a_new = np.delete(m_new, -1, axis=1)

        varb_list = varbs1.copy()
        varb_list.extend(varbs2)
        for row in range(len(row_new)):
            equ = Equation(name=equ_name + '化简方程_' + str(row + 1))
            equ.varb_list = varb_list.copy()
            equ.coeff_list = a_new[row, :]
            equ.constant = b_new[row]
            equs.add_equation(equ)
        return equs


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

    def reload_coefficient(self, equ):
        self.coeff_list = equ.coeff_list
        self.constant = equ.constant

    def add_coeff(self, varb, value=1):
        self.varb_list.append(varb)
        self.coeff_list.append(value)

    @property
    def varbs(self):
        varbs = VarbGroup()
        for varb in self.varb_list:
            varbs.add_varb(varb)
        return varbs


if __name__ == '__main__':
    ep = ElePack(None, 'test')
    ep.name = 'test'

    x1 = Varb(ep, 'x1')
    x2 = Varb(ep, 'x2')
    x3 = Varb(ep, 'x3')
    x4 = Varb(ep, 'x4')

    e1 = Equation(name='eq1')
    e2 = Equation(name='eq2')
    e3 = Equation(name='eq3')

    e1.varb_list = [x1, x2, x4]
    # e1.varb_list = [x2, x4]
    e1.coeff_list = [1, 2, 5]
    # e1.coeff_list = [1, 1]
    e1.constant = 4
    e2.varb_list = [x2, x3]
    e2.coeff_list = [1, 2]
    e2.constant = 5

    e3.varb_list = [x4, x3]
    e3.coeff_list = [2, 3]
    e3.constant = 12

    equs1 = EquationGroup(e1, e2, e3)

    equs1.config_equ_num()
    equs1.config_varb_num()
    equs1.creat_matrix()
    # equs1.solve_matrix()
    equs1.simplify_equs([x1], [x4], equ_name='测试')

    # equs2 = equs1.simplify_equs([x1], [x4])

    pass
