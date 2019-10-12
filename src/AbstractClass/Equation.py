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
        self.len_row = len_row = len(self)
        self.len_column = len_column = len(self.varbs)
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
        # mtrx = sp.Matrix(self.m_matrix)
        # a = mtrx.rref()
        self.solution = np.linalg.solve(self.m_matrix, self.constant)
        # self.solution = self.constant
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

    # @jit
    def simplify_equs(self, varbs1, varbs2, name):
        self.config_equ_num()
        self.config_varb_num()
        self.creat_matrix()
        nums1 = list()
        nums2 = list()
        for varb in varbs1:
            nums1.append(varb.num[self])
        for varb in varbs2:
            nums2.append(varb.num[self])
        len_smp = len(nums1)
        rng_smp = np.array(range(len_smp))
        mtrx_smp = np.matlib.zeros((len_smp, len_smp+1), dtype=complex)
        mtrx_smp[:, 0] = 1
        mtrx_t = np.matlib.zeros((len_smp, self.len_column), dtype=complex)
        cstt_t = np.zeros(len_smp, dtype=complex)
        for row in rng_smp:
            mtrx_t[row, nums1[row]] = 1
        mtrx_t = np.insert(self.m_matrix, 0, values=mtrx_t, axis=0)
        cstt_t = np.insert(self.constant, 0, values=cstt_t, axis=0)

        cstt_smp = np.linalg.solve(mtrx_t, cstt_t)
        cstt_smp = cstt_smp[nums2]

        for row in rng_smp:
            cstt_t[rng_smp] = np.zeros(len_smp)
            cstt_t[row] = 1
            solution = np.linalg.solve(mtrx_t, cstt_t)
            solution = solution[nums2]
            mtrx_smp[:, row+1] = (cstt_smp - solution).reshape(len_smp, 1)

        equs = EquationGroup()
        for row in rng_smp:
            equ = Equation(name=name + '_化简方程_' + str(row+1))
            equ.varb_list = [varbs2[row]]
            equ.varb_list.extend(varbs1)
            equ.coeff_list = np.array(mtrx_smp[row])
            equ.constant = cstt_smp[row]
            equs.add_equation(equ)

        self.del_num()
        # print(mtrx_smp, cstt_smp)
        return equs

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


# # 方程项
# class EquItem:
#     def __init__(self, varb=None, coefficient=None):
#         self.varb = varb
#         self.coefficient = coefficient


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
    e1.coeff_list = [1, 2, 5]
    e1.constant = 1
    e2.varb_list = [x2, x3]
    e2.coeff_list = [2, 4]
    e2.constant = 3

    e3.varb_list = [x4, x3]
    e3.coeff_list = [1, 6]
    e3.constant = 2

    equs1 = EquationGroup(e1, e2, e3)
    equs2 = equs1.simplify_equs([x1], [x4])

    pass
