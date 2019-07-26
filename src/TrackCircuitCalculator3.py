import numpy as np
import numpy.matlib
import pickle
import time
from src import ElectricParameter as pc
from matplotlib import pyplot as plt


# from src.TcsrModule import *
from src.BasicOutsideModel import *
from src.Equation import *

# from src.TCSR import *
from src.SectionGroup import *
# from src.TCSR import *

########################################################################################################################


# class Varb:
#     # def __init__(self, upper_module=None):im
#     #     self.upper_name = upper_module
#     #     self.num = None
#     #     self.name = ''
#
#     def __init__(self, upper_module=None, name_base=''):
#         self.upper_module = upper_module
#         self.name_base = name_base
#         self.num = None
#         self.name = ''
#
#     def get_varb_name(self):
#         self.name = self.upper_module.name + '_' + self.name_base
#         return self.name
#
#     def __repr__(self):
#         return repr((self.get_varb_name(), self.num))


########################################################################################################################

# # 元素包
# class ElePack:
#     prop_table = {
#         # '父对象': 'parent_ins',
#         '基础名称': 'name_base',
#         '元素字典': 'element',
#         '元素列表': 'ele_list',
#         # '室外元素标识': 'flag_outside',
#         # '元素列表标识': 'flag_ele_list',
#         # '单位元素标识': 'flag_ele_unit',
#         '相对位置': 'posi_rlt',
#         '绝对位置': 'posi_abs',
#     }
#
#     def __init__(self, parent_ins, name_base):
#         self.parent_ins = parent_ins
#         self.name_base = name_base
#         self.name = str()
#         self.element = dict()
#         self.ele_list = list()
#         self.flag_outside = False
#         self._posi_rlt = None
#         self.posi_abs = None
#         self.flag_ele_list = False
#         self.flag_ele_unit = False
#
#     @property
#     def posi_rlt(self):
#         return self._posi_rlt
#
#     @posi_rlt.setter
#     def posi_rlt(self, value):
#         self._posi_rlt = value
#
#     def init_position(self, posi):
#         self.flag_outside = True
#         self._posi_rlt = posi
#         self.posi_abs = 0
#
#     def add_element(self, name, instance):
#         if self.flag_ele_list:
#             self.element[name] = instance
#             self.ele_list.append(instance)
#
#     def __len__(self):
#         return len(self.element)
#
#     def __getitem__(self, key):
#         return self.element[key]
#
#     def __setitem__(self, key, value):
#         self.element[key] = value
#
#     def values(self):
#         return self.element.values()
#
#     def keys(self):
#         return self.element.keys()
#
#     def items(self):
#         return self.element.items()
#
#     def set_property(self, key, value):
#         prop_name = self.prop_table[key]
#         exec('self.' + prop_name + ' = value')
#         pass
#
#     def get_property(self, key):
#         value = None
#         try:
#             prop_name = self.prop_table[key]
#             value = eval('self.' + prop_name)
#         except KeyError:
#             pass
#         return value


# class EleModule(ElePack):
#     new_table = {
#         '变量名': 'varb_name',
#         '变量字典': 'varb_dict',
#         '公式列表': 'equs',
#         '模块列表': 'md_list',
#     }
#     prop_table = ElePack.prop_table.copy()
#     prop_table.update(new_table)
#
#     def __init__(self, parent_ins, name_base):
#         super().__init__(parent_ins, name_base)
#         self.varb_name = list()
#         self.varb_dict = dict()
#         self.equs = list()
#         self.md_list = [self]
#
#     def __len__(self):
#         return len(self.varb_dict)
#
#     def __getitem__(self, key):
#         return self.varb_dict[key]
#
#     def __setitem__(self, key, value):
#         self.varb_dict[key] = value
#
#     def values(self):
#         return self.varb_dict.values()
#
#     def keys(self):
#         return self.varb_dict.keys()
#
#     def items(self):
#         return self.varb_dict.items()


########################################################################################################################

# # 一端口元件
# class OnePortNetwork(EleModule):
#     def __init__(self, parent_ins, name_base):
#         super().__init__(parent_ins, name_base)
#         self.varb_name = ['U', 'I']
#         self.varb_dict = {'U': Varb(self, 'U'),
#                           'I': Varb(self, 'I')}
#
#
# # 二端口网络
# class TwoPortNetwork(EleModule):
#     def __init__(self, parent_ins, name_base):
#         super().__init__(parent_ins, name_base)
#         self.varb_name = ['U1', 'I1', 'U2', 'I2']
#         self.varb_dict = {'U1': Varb(self, 'U1'),
#                           'I1': Varb(self, 'I1'),
#                           'U2': Varb(self, 'U2'),
#                           'I2': Varb(self, 'I2')}


########################################################################################################################

# # 并联阻抗
# class OPortZ(OnePortNetwork):
#     new_table = {
#         '并联阻抗': 'z',
#     }
#     prop_table = OnePortNetwork.prop_table.copy()
#     prop_table.update(new_table)
#
#     def __init__(self, parent_ins, name_base, z):
#         super().__init__(parent_ins, name_base)
#         self.z = z
#
#     def get_equs(self, freq):
#         z = self.z[freq].z
#         equ1 = Equation(varbs=[self['U'], self['I']], values=[-1, z])
#         self.equs = [equ1]
#
#
# # 并联电压源
# class OPortPowerU(OnePortNetwork):
#     new_table = {
#         '电压值': 'voltage',
#     }
#     prop_table = OnePortNetwork.prop_table.copy()
#     prop_table.update(new_table)
#
#     def __init__(self, parent_ins, name_base, voltage=0):
#         super().__init__(parent_ins, name_base)
#         self.voltage = voltage
#
#     def get_equs(self, freq):
#         equ1 = Equation(varbs=[self['U']], values=[1])
#         self.equs = [equ1]


# # 并联电流源
# class OPortPowerI(OnePortNetwork):
#     new_table = {
#         '电流值': 'current',
#     }
#     prop_table = OnePortNetwork.prop_table.copy()
#     prop_table.update(new_table)
#
#     def __init__(self, parent_ins, name_base, current=0):
#         super().__init__(parent_ins, name_base)
#         self.current = current
#
#     def get_equs(self, freq):
#         equ1 = Equation(varbs=[self['I']], values=[1])
#         self.equs = [equ1]
#
#
# ########################################################################################################################
#
# # Pi型二端口网络
# class TPortCircuitPi(TwoPortNetwork):
#     new_table = {
#         '阻抗1': 'y1',
#         '阻抗2': 'y2',
#         '阻抗3': 'y3'
#     }
#     prop_table = TwoPortNetwork.prop_table.copy()
#     prop_table.update(new_table)
#
#     def __init__(self, parent_ins, name_base, y1, y2, y3):
#         super().__init__(parent_ins, name_base)
#         self.y1 = y1
#         self.y2 = y2
#         self.y3 = y3
#
#     def get_equs(self, freq):
#         y1 = self.y1[freq].z
#         y2 = self.y2[freq].z
#         y3 = self.y3[freq].z
#         equ1 = Equation(varbs=[self['I1'], self['U1'], self['U2']],
#                         values=[-1, -(y1 + y2), -y2])
#         equ2 = Equation(varbs=[self['I2'], self['U1'], self['U2']],
#                         values=[-1, -y2, (y2 + y3)])
#         self.equs = [equ1, equ2]
#
#
# # T型二端口网络
# class TPortCircuitT(TwoPortNetwork):
#     new_table = {
#         '阻抗1': 'z1',
#         '阻抗2': 'z2',
#         '阻抗3': 'z3'
#     }
#     prop_table = TwoPortNetwork.prop_table.copy()
#     prop_table.update(new_table)
#
#     def __init__(self, parent_ins, name_base, z1, z2, z3):
#         super().__init__(parent_ins, name_base)
#         self.z1 = z1
#         self.z2 = z2
#         self.z3 = z3
#
#     def get_equs(self, freq):
#         z1 = self.z1[freq].z
#         z2 = self.z2[freq].z
#         z3 = self.z3[freq].z
#         equ1 = Equation(varbs=[self['U1'], self['I1'], self['I2']],
#                         values=[-1, -(z1 + z2), z2])
#         equ2 = Equation(varbs=[self['U2'], self['I1'], self['I2']],
#                         values=[-1, -z2, (z2 + z3)])
#         self.equs = [equ1, equ2]
#
#
# ########################################################################################################################
#
# # 变压器二端口网络
# class TPortCircuitN(TwoPortNetwork):
#     new_table = {
#         '变比': 'n',
#     }
#     prop_table = TwoPortNetwork.prop_table.copy()
#     prop_table.update(new_table)
#
#     def __init__(self, parent_ins, name_base, n):
#         super().__init__(parent_ins, name_base)
#         self.n = n
#
#     def get_equs(self, freq):
#         n = self.n[freq]
#         equ1 = Equation(varbs=[self['U1'], self['U2']],
#                         values=[-1, n])
#         equ2 = Equation(varbs=[self['I1'], self['I2']],
#                         values=[n, -1])
#         self.equs = [equ1, equ2]
#
#
# # 串联二端口网络
# class TPortZSeries(TwoPortNetwork):
#     new_table = {
#         '串联阻抗': 'z',
#     }
#     prop_table = TwoPortNetwork.prop_table.copy()
#     prop_table.update(new_table)
#
#     def __init__(self, parent_ins, name_base, z):
#         super().__init__(parent_ins, name_base)
#         self.z = z
#
#     def get_equs(self, freq):
#         z = self.z[freq].z
#         equ1 = Equation(varbs=[self['U1'], self['U2'], self['I2']],
#                         values=[1, -1, z])
#         equ2 = Equation(varbs=[self['I1'], self['I2']],
#                         values=[-1, 1])
#         self.equs = [equ1, equ2]
#
#
# # 并联二端口网络
# class TPortZParallel(TwoPortNetwork):
#     new_table = {
#         '并联阻抗': 'z',
#     }
#     prop_table = TwoPortNetwork.prop_table.copy()
#     prop_table.update(new_table)
#
#     def __init__(self, parent_ins, name_base, z):
#         super().__init__(parent_ins, name_base)
#         self.z = z
#
#     def get_equs(self, freq):
#         z = self.z[freq].z
#         equ1 = Equation(varbs=[self['U1'], self['I1'], self['I2']],
#                         values=[-1, -z, z])
#         equ2 = Equation(varbs=[self['U2'], self['I1'], self['I2']],
#                         values=[-1, -z, z])
#         self.equs = [equ1, equ2]


########################################################################################################################

# class UPowerOut(OPortPowerU):
#     def __init__(self, parent_ins, name_base, posi):
#         super().__init__(parent_ins, name_base)
#         self.init_position(posi)
#         self.flag_ele_unit = True
#
#
# # 室外阻抗
# class ZOutside(OPortZ):
#     def __init__(self, parent_ins, name_base, posi, z):
#         super().__init__(parent_ins, name_base, z)
#         self.init_position(posi)
#         self.flag_ele_unit = True
#
#
# # 补偿电容
# class CapC(ZOutside):
#     def __init__(self, parent_ins, name_base, posi, z):
#         super().__init__(parent_ins, name_base, posi, z)
#
#
# # 空心线圈
# class SVA(ZOutside):
#     def __init__(self, parent_ins, name_base, posi, z):
#         super().__init__(parent_ins, name_base, posi, z)
#
#
# # TB
# class TB(ZOutside):
#     def __init__(self, parent_ins, name_base, posi, z):
#         super().__init__(parent_ins, name_base, posi, z)
#
#
# # 室外电阻
# class ROutside(ZOutside):
#     def __init__(self, parent_ins, name_base, posi, z):
#         super().__init__(parent_ins, name_base, posi, z)
#
#     def get_equs(self, freq):
#         z = self.z
#         equ1 = Equation(varbs=[self['U'], self['I']],
#                         values=[-1, z])
#         self.equs = [equ1]


########################################################################################################################

# 发送器
# class TcsrPower(ElePack):
#     new_table = {
#         '发送器内阻': 'z',
#         '发送电平级': 'level',
#     }
#     prop_table = ElePack.prop_table.copy()
#     prop_table.update(new_table)
#
#     def __init__(self, parent_ins, name_base, z, level):
#         super().__init__(parent_ins, name_base)
#         self.flag_ele_list = True
#         # self.z = z
#         self.add_element('1电压源', OPortPowerU(self, '1电压源'))
#         self.add_element('2内阻', TcsrPowerZ(self, '2内阻', z, level))
#
#     @property
#     def z(self):
#         return self.element['2内阻'].z
#
#     @z.setter
#     def z(self, value):
#         self.element['2内阻'].z = value
#
#     @property
#     def level(self):
#         return self.element['2内阻'].level
#
#     @level.setter
#     def level(self, value):
#         self.element['2内阻'].level = value
#
#
# # 串联二端口网络
# class TcsrPowerZ(TwoPortNetwork):
#     new_table = {
#         '阻抗': 'z',
#         '电平级': 'level',
#     }
#     prop_table = TwoPortNetwork.prop_table.copy()
#     prop_table.update(new_table)
#
#     def __init__(self, parent_ins, name_base, z, level):
#         super().__init__(parent_ins, name_base)
#         self.z = z
#         self.level = level
#
#     def get_equs(self, freq):
#         z = self.z[self.level][freq].z
#         equ1 = Equation(varbs=[self['U1'], self['U2'], self['I2']],
#                         values=[1, -1, z])
#         equ2 = Equation(varbs=[self['I1'], self['I2']],
#                         values=[-1, 1])
#         self.equs = [equ1, equ2]
#
#
# # 接收器
# class TcsrReceiver(OPortZ):
#     def __init__(self, parent_ins, name_base, z):
#         super().__init__(parent_ins, name_base, z)
#
#
# ########################################################################################################################
#
# # 变压器模板
# class TcsrTransformer(ElePack):
#     def __init__(self, parent_ins, name_base, z1, z2, n):
#         super().__init__(parent_ins, name_base)
#         self.flag_ele_list = True
#         self.add_element('1等效内阻', TPortCircuitT(self, '1等效内阻', z1, z2, z1))
#         self.add_element('2变压器', TPortCircuitN(self, '2变压器', n))
#
#
# # 防雷变压器
# class TcsrFL(TcsrTransformer):
#     def __init__(self, parent_ins, name_base, z1, z2, n):
#         super().__init__(parent_ins, name_base, z1, z2, n)
#
#
# # TAD变压器
# class TcsrTAD(ElePack):
#     def __init__(self, parent_ins, name_base, z1, z2, z3, n, zc):
#         super().__init__(parent_ins, name_base)
#         self.flag_ele_list = True
#         self.add_element('1共模电感', TPortZSeries(self, '1共模电感', z3))
#         self.add_element('2等效内阻', TPortCircuitT(self, '2等效内阻', z1, z2, z1))
#         self.add_element('3变压器', TPortCircuitN(self, '3变压器', n))
#         self.add_element('4串联电容', TPortZSeries(self, '4串联电容', zc))
#
#
# ########################################################################################################################
#
# # 电缆等效电路
# class TPortCable(TwoPortNetwork):
#     new_table = {
#         '电阻': 'R',
#         '电感': 'L',
#         '电容': 'C',
#         '电缆长度': 'length',
#     }
#     prop_table = TwoPortNetwork.prop_table.copy()
#     prop_table.update(new_table)
#
#     def __init__(self, parent_ins, name_base, length, cab_r=43, cab_l=825e-6, cab_c=28e-9):
#         super().__init__(parent_ins, name_base)
#         self.R = cab_r
#         self.L = cab_l
#         self.C = cab_c
#         self.length = length
#
#     def get_equs(self, freq):
#         length = self.length
#         w = 2 * np.pi * freq
#         z0 = self.R + 1j * w * self.L
#         y0 = 1j * w * self.C
#         zc = np.sqrt(z0 / y0)
#         gama = np.sqrt(z0 * y0)
#         zii = zc * np.sinh(gama * length)
#         yii = (np.cosh(gama * length) - 1) / zc / np.sinh(gama * length)
#         y1 = yii
#         y2 = 1 / zii
#         y3 = yii
#         equ1 = Equation(varbs=[self['I1'], self['U1'], self['U2']],
#                         values=[-1, -(y1 + y2), -y2])
#         equ2 = Equation(varbs=[self['I2'], self['U1'], self['U2']],
#                         values=[-1, -y2, (y2 + y3)])
#         self.equs = [equ1, equ2]
#
#
# ########################################################################################################################
#
# # 匹配单元
# class TcsrBA(TPortZParallel):
#     def __init__(self, parent_ins, name_base, z):
#         super().__init__(parent_ins, name_base, z)
#
#     def get_equs(self, freq):
#         z = self.z[self.m_freq][freq].z
#         equ1 = Equation(varbs=[self['U1'], self['I1'], self['I2']],
#                         values=[-1, -z, z])
#         equ2 = Equation(varbs=[self['U2'], self['I1'], self['I2']],
#                         values=[-1, -z, z])
#         self.equs = [equ1, equ2]
#
#     @property
#     def m_freq(self):
#         return self.parent_ins.m_freq
#
#
# # 引接线
# class TcsrCA(TPortZSeries):
#     def __init__(self, parent_ins, name_base, z):
#         super().__init__(parent_ins, name_base, z)
#

########################################################################################################################

# 发送接收端
# class TCSR(ElePack):
#     new_table = {
#         '主轨类型': 'm_type',
#         '模式': 'mode',
#         '匹配频率': 'm_freq',
#         '发送电平级': 'send_level',
#         '电缆长度': 'cable_length'
#     }
#     prop_table = ElePack.prop_table.copy()
#     prop_table.update(new_table)
#
#     def __init__(self, parent_ins, name_base, posi_flag):
#         super().__init__(parent_ins, name_base)
#         self.posi_flag = posi_flag
#         self.init_position(0)
#         self.flag_ele_list = True
#         self.flag_ele_unit = True
#         self.mode = None
#         self.md_list = list()
#
#     @property
#     def posi_rlt(self):
#         posi = None
#         parent = self.parent_ins
#         if isinstance(parent, Section):
#             if self.posi_flag == '左':
#                 posi = parent['左绝缘节'].j_length / 2
#             elif self.posi_flag == '右':
#                 posi = parent.s_length - parent['右绝缘节'].j_length / 2
#         elif isinstance(parent, Joint):
#             if self.posi_flag == '左':
#                 posi = parent.j_length / 2
#             elif self.posi_flag == '右':
#                 posi = - parent.j_length / 2
#         return posi
#
#     @property
#     def parent_joint(self):
#         joint = None
#         if isinstance(self.parent_ins, Section):
#             name = self.posi_flag + '绝缘节'
#             joint = self.parent_ins[name]
#         elif isinstance(self.parent_ins, Joint):
#             joint = self.parent_ins
#         return joint
#
#     @property
#     def m_type(self):
#         m_type = None
#         if isinstance(self.parent_ins, Section):
#             m_type = self.parent_ins.m_type
#         elif isinstance(self.parent_ins, Joint):
#             m_type = self.parent_ins.parent_ins.m_type
#         return m_type
#
#     @property
#     def m_freq(self):
#         m_freq = None
#         if isinstance(self.parent_ins, Section):
#             m_freq = self.parent_ins.m_freq
#         elif isinstance(self.parent_ins, Joint):
#             m_freq = change_freq(self.parent_ins.parent_ins.m_freq)
#         return m_freq
#
#     @property
#     def cable_length(self):
#         length = None
#         for ele in self.element.values():
#             if isinstance(ele, TPortCable):
#                 length = ele.length
#         return length
#
#     @cable_length.setter
#     def cable_length(self, value):
#         for ele in self.element.values():
#             if isinstance(ele, TPortCable):
#                 ele.length = value
#
#     @property
#     def send_level(self):
#         level = None
#         for ele in self.element.values():
#             if isinstance(ele, TcsrPower):
#                 level = ele.level
#         return level
#
#     @send_level.setter
#     def send_level(self, value):
#         for ele in self.element.values():
#             if isinstance(ele, TcsrPower):
#                 ele.level = value
#
#     # 变量赋值
#     def config_varb(self):
#         for num in range(len(self.md_list) - 1):
#             self.equal_varb([self.md_list[num], -2], [self.md_list[num + 1], 0])
#             self.equal_varb([self.md_list[num], -1], [self.md_list[num + 1], 1])


# class ZPW2000A_QJ_Normal(TCSR):
#     def __init__(self, parent_ins, name_base, posi_flag,
#                  cable_length, mode, level):
#         super().__init__(parent_ins, name_base, posi_flag)
#         self.posi_flag = posi_flag
#         self.init_position(0)
#         self.flag_ele_list = True
#         self.flag_ele_unit = True
#         self.mode = mode
#
#         if self.mode == '发送':
#             self.add_element('1发送器', TcsrPower(self, '1发送器', TCSR_2000A['z_pwr'], level))
#         elif self.mode == '接收':
#             self.add_element('1接收器', TcsrReceiver(self, '1接收器', TCSR_2000A['Z_rcv']))
#         self.add_element('2防雷', TcsrFL(self, '2防雷',
#                                        TCSR_2000A['FL_z1_发送端'],
#                                        TCSR_2000A['FL_z2_发送端'],
#                                        TCSR_2000A['FL_n_发送端']))
#         self.add_element('3Cab', TPortCable(self, '3Cab', cable_length))
#         self.add_element('4TAD', TcsrTAD(self, '4TAD',
#                                          TCSR_2000A['TAD_z1_发送端_区间'],
#                                          TCSR_2000A['TAD_z2_发送端_区间'],
#                                          TCSR_2000A['TAD_z3_发送端_区间'],
#                                          TCSR_2000A['TAD_n_发送端_区间'],
#                                          TCSR_2000A['TAD_c_发送端_区间']))
#         self.add_element('5BA', TcsrBA(self, '5BA', TCSR_2000A['PT']))
#         self.add_element('6CA', TcsrCA(self, '6CA', TCSR_2000A['CA_z_区间']))
#
#         self.md_list = self.get_md_list([])
#         self.config_varb()


########################################################################################################################

# 钢轨段
class SubRailPi(TwoPortNetwork):
    def __init__(self, parent_ins, name_base, l_posi, r_posi, z_trk, rd):
        super().__init__(parent_ins, name_base)
        self.init_position(l_posi)
        self.flag_ele_unit = True
        self.l_posi = l_posi
        self.r_posi = r_posi
        self.track_length = r_posi - l_posi
        self.z_trk = z_trk
        self.rd = rd

    def get_equs(self, freq):
        z_trk = self.z_trk
        rd = self.rd
        length = self.track_length / 1000

        y_tk = 1 / z_trk[freq].z / length
        y_rd = 1 / rd * length
        equ1 = Equation(varbs=[self['I1'], self['U1'], self['U2']],
                        values=[-1, (y_rd + y_tk), -y_tk])
        equ2 = Equation(varbs=[self['I2'], self['U1'], self['U2']],
                        values=[-1, -y_tk, (y_tk + y_rd)])
        self.equs = [equ1, equ2]
        if hasattr(self, 'mutual_trk'):
            m_circuit = self.mutual_trk
            m = length * 0.30
            self.varb_dict['Im'] = m_circuit.varb_dict['I1']
            equ1.add_varb(self['Im'], (m * (y_rd + y_tk)))
            equ2.add_varb(self['Im'], -(m * y_tk))


########################################################################################################################

# # 绝缘节
# class Joint(ElePack):
#     new_table = {
#         '位置标志': 'posi_flag',
#         '左侧区段': 'l_section',
#         '右侧区段': 'r_section',
#         '绝缘节长度': 'j_length',
#         '区段类型': 'sec_type'
#     }
#     prop_table = ElePack.prop_table.copy()
#     prop_table.update(new_table)
#
#     def __init__(self, parent_ins, name_base, posi_flag,
#                  l_section, r_section, j_type, j_length):
#         super().__init__(parent_ins, name_base)
#         self.posi_flag = posi_flag
#         self.init_position(0)
#         self.j_type = j_type
#         self.l_section = l_section
#         self.r_section = r_section
#         self.j_length = j_length
#         self.set_element()
#
#     @property
#     def posi_rlt(self):
#         posi = self.parent_ins.s_length if self.posi_flag == '右' else 0
#         return posi
#
#     @posi_rlt.setter
#     def posi_rlt(self, value):
#         self._posi_rlt = value
#
#     @property
#     def sec_type(self):
#         # sec_type = None
#         if self.l_section and self.r_section:
#             if self.j_type == '电气':
#                 if not self.l_section.m_type == self.r_section.m_type:
#                     raise KeyboardInterrupt(
#                         repr(self.l_section) + '和' + repr(self.r_section) + '区段类型不符')
#         sec_type = self.parent_ins.m_type
#         return sec_type
#
#     def set_element(self):
#         if self.j_type == '电气':
#             if self.sec_type == '2000A':
#                 self.element['SVA'] = SVA(parent_ins=self,
#                                           name_base='SVA',
#                                           posi=0,
#                                           z=TCSR_2000A['SVA_z'])
#
#     def add_joint_tcsr(self):
#         if self.j_type == '电气':
#             name = '相邻调谐单元'
#             if not self.l_section:
#                 tcsr = self.r_section['左调谐单元']
#                 flag = '右'
#             elif not self.r_section:
#                 tcsr = self.l_section['右调谐单元']
#                 flag = '左'
#             else:
#                 return
#
#             if isinstance(tcsr, ZPW2000A_QJ_Normal):
#                 self[name] = ZPW2000A_QJ_Normal(parent_ins=self, name_base=name, posi_flag=flag,
#                                                 cable_length=tcsr.cable_length,
#                                                 mode=change_sr_mode(tcsr.mode), level=1)


# # 区段
# class Section(ElePack):
#     new_table = {
#         '区段类型': 'm_type',
#         '区段频率': 'm_freq',
#         '区段长度': 's_length'
#     }
#     prop_table = ElePack.prop_table.copy()
#     prop_table.update(new_table)
#
#     def __init__(self, parent_ins, name_base,
#                  m_type, m_freq, s_length,
#                  j_length, c_num, j_type, sr_mode):
#         super().__init__(parent_ins, name_base)
#         self.init_position(0)
#         self.m_type = m_type
#         self.m_freq = m_freq
#         self.s_length = s_length
#
#         # 临时变量
#         sr_mode_list = [None, None]
#         if sr_mode == '左发':
#             sr_mode_list = ['发送', '接收']
#         elif sr_mode == '右发':
#             sr_mode_list = ['接收', '发送']
#         m_length = s_length - (j_length[0] + j_length[1]) / 2
#         init_list = (j_length, c_num, sr_mode_list, j_type, m_length)
#         self.set_element(init_list)
#
#     @property
#     def posi_rlt(self):
#         posi = self.parent_ins.posi_dict[self.name_base]
#         return posi
#
#     def set_element(self, init_list):
#         j_length, c_num, sr_mode, j_type, m_length = init_list
#         if self.m_type == '2000A':
#             offset = j_length[0]
#             # 设置电容
#             lc = (m_length / c_num) if c_num > 0 else 0
#             c_posi = [(num * lc + lc / 2 + offset) for num in range(c_num)]
#             for num in range(c_num):
#                 name = 'C' + str(num + 1)
#                 self[name] = CapC(parent_ins=self, name_base=name,
#                                   posi=c_posi[num], z=TCSR_2000A['Ccmp_z'])
#             # 设置绝缘节
#             for num in range(2):
#                 flag = ['左', '右'][num]
#                 name = flag + '绝缘节'
#                 l_section = None if num == 0 else self
#                 r_section = self if num == 0 else None
#                 self[name] = Joint(parent_ins=self, name_base=name, posi_flag=flag,
#                                    l_section=l_section, r_section=r_section,
#                                    j_length=j_length[num], j_type=j_type[num],)
#                 joint = self[name]
#
#                 name = flag + '调谐单元'
#                 if joint.j_type == '电气':
#                     self[name] = ZPW2000A_QJ_Normal(parent_ins=self, name_base=name,
#                                                     posi_flag=flag, cable_length=10,
#                                                     mode=sr_mode[num], level=1)
#         else:
#             raise KeyboardInterrupt(self.m_type + '暂为不支持的主轨类型')


########################################################################################################################

# 区段组
# class SectionGroup(ElePack):
#     new_table = {
#         '区段数量': 'sec_num',
#         '区段列表': 'section_list',
#         '位置列表': 'ele_posi',
#         '位置字典': 'posi_dict'
#     }
#     prop_table = ElePack.prop_table.copy()
#     prop_table.update(new_table)
#
#     def __init__(self, name_base, posi, m_num, freq1, m_length, j_length, m_type, c_num):
#         super().__init__(None, name_base)
#         self.init_position(posi)
#         init_list = (m_num, freq1, m_type, m_length, j_length, c_num)
#         self.m_num = m_num
#         self.section_list = list()
#         self.ele_posi = list()
#
#         self.init_element(init_list)
#         self.link_section()
#         self.refresh()
#
#     def init_element(self, init_list):
#         m_num, freq, m_type, m_length, j_length, c_num = init_list
#         freq_list = list()
#         for num in range(m_num):
#             freq_list.append(freq)
#             freq = change_freq(freq)
#         m_type = m_type[:m_num]
#         m_length = m_length[:m_num]
#         j_length = j_length[:(m_num + 1)]
#         c_num = c_num[:m_num]
#
#         j_type = ['电气' if num > 0 else '机械' for num in j_length]
#         j_length = [[j_length[num], j_length[num+1]] for num in range(m_num)]
#         j_type = [[j_type[num], j_type[num+1]] for num in range(m_num)]
#         # sr_type = ['PT', 'PT']
#
#         for num in range(m_num):
#             name = '区段' + str(num+1)
#             sec_t = Section(parent_ins=self, name_base=name,
#                             m_type=m_type[num], m_freq=freq_list[num], s_length=m_length[num],
#                             j_length=j_length[num], c_num=c_num[num],
#                             j_type=j_type[num], sr_mode='左发')
#             self.element[name] = sec_t
#             self.section_list.append(sec_t)
#
#     @property
#     def sec_num(self):
#         return len(self.section_list)
#
#     @property
#     def posi_dict(self):
#         posi_t = 0
#         posi_dict = dict()
#         for sec in self.section_list:
#             posi_dict[sec.name_base] = posi_t
#             posi_t = posi_t + sec.s_length
#         return posi_dict
#
#     def refresh(self):
#         set_posi_abs(self, 0)
#         # set_ele_name(self, '')
#         self.ele_posi = get_posi_abs(self, posi_list=[])
#
#     # 连接相邻区段
#     def link_section(self):
#         for num in range(self.sec_num - 1):
#             sec1 = self.section_list[num]
#             sec2 = self.section_list[num+1]
#             joint1 = sec1['右绝缘节']
#             joint2 = sec2['左绝缘节']
#             if not joint1.j_type == joint2.j_type:
#                 raise KeyboardInterrupt(repr(sec1) + '和' + repr(sec2) + '绝缘节类型不符无法相连')
#             elif not joint1.j_length == joint2.j_length:
#                 raise KeyboardInterrupt(repr(sec1) + '和' + repr(sec2) + '绝缘节长度不符无法相连')
#             elif joint1.r_section:
#                 raise KeyboardInterrupt(repr(sec1) + '右侧已与区段相连')
#             elif joint2.l_section:
#                 raise KeyboardInterrupt(repr(sec2) + '左侧已与区段相连')
#             elif joint1.j_type == '电气':
#                 if not sec1.m_type == sec2.m_type:
#                     raise KeyboardInterrupt(repr(sec1) + '和' + repr(sec2) + '主轨类型不符无法相连')
#                 elif not sec1.m_freq == change_freq(sec2.m_freq):
#                     raise KeyboardInterrupt(repr(sec1) + '和' + repr(sec2) + '主轨频率不符无法相连')
#                 else:
#                     joint1.r_section = sec2
#                     sec2['左绝缘节'] = joint1
#
#         for sec in self.section_list:
#             for j_name in ['左绝缘节', '右绝缘节']:
#                 sec[j_name].add_joint_tcsr()
#

########################################################################################################################

# 钢轨分割段
class RailSegment:
    def __init__(self, l_posi, r_posi, ztrk, rd):
        self.l_posi = l_posi
        self.r_posi = r_posi
        self.ztrk = ztrk
        self.rd = rd


# 钢轨
class Rail(ElePack):
    def __init__(self, parent_ins=None, name_base='',
                 trk_num=1, posi=None, ztrk=None, rd=None):
        super().__init__(parent_ins, name_base)
        posi = [-np.inf, np.inf] if posi is None else posi
        ztrk = [TCSR_2000A['Trk_z']] if ztrk is None else ztrk
        rd = [TCSR_2000A['Rd']] if rd is None else rd
        init_list = [trk_num, posi, ztrk, rd]
        self.posi_list = list()
        self.rail_list = list()
        # self.sub_rail_list = list()
        self.init_rail_list(init_list)

    def init_rail_list(self, init_list):
        trk_num = init_list[0]
        posi_list = init_list[1][:(trk_num+1)]
        ztrk_list = init_list[2][:trk_num]
        rd_list = init_list[3][:trk_num]

        self.posi_list = posi_list
        for num in range(trk_num):
            self.rail_list.append(RailSegment(l_posi=posi_list[num],
                                              r_posi=posi_list[num + 1],
                                              ztrk=ztrk_list[num],
                                              rd=rd_list[num]))


########################################################################################################################

# 列车
class Train(ElePack):
    def __init__(self, parent_ins, name_base, posi_abs):
        super().__init__(parent_ins, name_base)
        self.init_position(0)
        self.element['分路电阻1'] = ROutside(parent_ins=self, name_base='分路电阻1',
                                         posi=0, z=TCSR_2000A['Rsht_z'])
        set_ele_name(self)
        set_posi_abs(self, posi_abs)


########################################################################################################################

# 线路信息
class Line(ElePack):
    def __init__(self, parent_ins=None, name_base='',
                 sec_group=None, rail=None, train=None):
        super().__init__(parent_ins, name_base)
        self.rail = Rail() if rail is None else rail
        if sec_group is not None:
            self.add_element(sec_group.name_base, sec_group)
        if train is not None:
            self.add_element(train.name_base, train)
        self.ele_set = get_element(self, ele_set=set())
        set_ele_name(self, '')

    def add_element(self, name, instance):
        self.element[name] = instance
        instance.parent_ins = self


# 线路组
class LineGroup(ElePack):
    def __init__(self, *lines, name_base=''):
        super().__init__(None, name_base)
        self.ele_set = set()
        for line in lines:
            line.parent_ins = self
            self.element[line.name_base] = line
            self.ele_set.update(line.ele_set)
        set_ele_name(self, '')


########################################################################################################################

# 交换载频
def change_freq(freq):
    new = None
    if freq == 1700:
        new = 2300
    elif freq == 2000:
        new = 2600
    elif freq == 2300:
        new = 1700
    elif freq == 2600:
        new = 2000
    return new


# 交换载频
def change_sr_mode(mode):
    new = None
    if mode == '发送':
        new = '接收'
    elif mode == '接收':
        new = '发送'
    return new


# 按位置筛选元件
def choose_element(ele_set, posi_abs):
    ele_dict = dict()
    for ele in ele_set:
        if ele.posi_abs in posi_abs:
            ele_dict[ele.name] = ele
    return ele_dict


# 快速获取绝对位置
def get_posi_fast(ele_set):
    posi_all = list()
    for ele in ele_set:
        posi_all.append(ele.posi_abs)
    posi_all = sort_posi_list(posi_all)
    return posi_all


# 设置绝对位置
def set_posi_abs(vessel, abs_posi):
    if vessel.flag_outside is True:
        if vessel.parent_ins is None:
            vessel.posi_abs = vessel.posi_rlt + abs_posi
        else:
            # print(vessel.parent_ins.posi_abs,vessel.name_base, vessel.posi_rlt)
            vessel.posi_abs = vessel.parent_ins.posi_abs + vessel.posi_rlt
        if hasattr(vessel, 'element') and (not vessel.flag_ele_unit):
            for ele in vessel.element.values():
                set_posi_abs(ele, abs_posi)


# 获取元器件绝对位置
def get_posi_abs(vessel, posi_list):
    posi_list = posi_list.copy()
    if hasattr(vessel, 'element') and (not vessel.flag_ele_unit):
        for ele in vessel.element.values():
            posi_list = get_posi_abs(ele, posi_list)
    else:
        posi_list.append(vessel.posi_abs)
        posi_list = sort_posi_list(posi_list)
    return posi_list


# 配置元器件的名称
def set_ele_name(vessel, prefix=''):
    if hasattr(vessel, 'parent_ins'):
        if vessel.parent_ins is None:
            vessel.name = prefix + vessel.name_base
        else:
            vessel.name = vessel.parent_ins.name + '_' + vessel.name_base
    if hasattr(vessel, 'element'):
        for value in vessel.element.values():
            set_ele_name(value, prefix)


# 获得所有元器件的字典
def get_element(*vessels, ele_set, flag_ele_unit=True):
    for vessel in vessels:
        if hasattr(vessel, 'element') and (not (flag_ele_unit * vessel.flag_ele_unit)):
            for value in vessel.element.values():
                ele_set = get_element(value, ele_set=ele_set, flag_ele_unit=flag_ele_unit)
        else:
            ele_set.add(vessel)
    return ele_set


########################################################################################################################

# 节点排序
def sort_posi_list(posi_list):
    new_list = list(set(posi_list))
    new_list.sort()
    return new_list

########################################################################################################################


# # 获得元器件连接顺序的列表
# def get_md_list(vessel, md_list):
#     if vessel.flag_ele_list is True:
#         for ele in vessel.ele_list:
#             md_list = get_md_list(ele, md_list)
#     else:
#         md_list.append(vessel)
#     return md_list


# # 使两个模块的变量映射到同一个变量对象
# def equal_varb(pack1, pack2):
#     module1 = pack1[0]
#     module2 = pack2[0]
#     num1 = pack1[1]
#     num2 = pack2[1]
#     name1 = module1.varb_name[num1]
#     name2 = module2.varb_name[num2]
#     module1.varb_dict[name1] = module2.varb_dict[name2]


# 获得所有变量
def get_varb(vessel, varb_set):
    if hasattr(vessel, 'varb_dict'):
        for ele in vessel.varb_dict.values():
            varb_set.add(ele)
    else:
        for ele in vessel.element.values():
            varb_set = get_varb(ele, varb_set)
    return varb_set.copy()


# # 变量编号
# def set_varb_num(var_set):
#     name_list = []
#     for varb in var_set:
#         name_list.append(varb.get_varb_name())
#     name_list.sort()
#     varb_list = [None] * len(name_list)
#     for varb in var_set:
#         name = varb.get_varb_name()
#         varb.num = name_list.index(name)
#         varb_list[varb.num] = varb
#     return varb_list

########################################################################################################################

# 节点
class Node:
    def __init__(self, posi):
        self.posi = posi
        self.element = dict()
        self.track = [None, None]


class LineElement(ElePack):
    def __init__(self, parent_ins, name_base):
        super().__init__(parent_ins, name_base)


class SingleLineModel(ElePack):
    def __init__(self, m_model, line):
        super().__init__(m_model, line.name_base)
        self.name = line.name
        self.line = line
        self.element['元件'] = ElePack(self, '元件')
        self.element['钢轨'] = ElePack(self, '钢轨')
        self.posi_line = None
        self.node_dict = dict()
        self.var_set = set()
        self.get_model_element()
        print(line.name)

    # 获得矩阵模型的元件
    def get_model_element(self):
        self.get_posi_line()
        self.element['元件'].element = choose_element(self.line.ele_set, self.posi_line)
        self.element['钢轨'].element = self.set_sub_rail(self.posi_line)
        set_ele_name(self['钢轨'], '')
        self.set_node_dict()
        self.link_track_ele()
        self.var_set = get_varb(self, varb_set=set())

    # 获得钢轨分割点位置（参数：全局元件及位置、线路元件）
    def get_posi_line(self, ftype='元件'):
        posi_global = get_posi_fast(self.parent_ins.line_group.ele_set)
        posi_self_ele = get_posi_fast(self.line.ele_set)
        posi_rail = self.line.rail.posi_list
        if ftype == '元件':
            rg = [posi_self_ele[0], posi_self_ele[-1]]
            if posi_self_ele[0] < posi_rail[0] or posi_self_ele[-1] > posi_rail[-1]:
                raise KeyboardInterrupt('钢轨范围异常')
        elif ftype == '钢轨':
            rg = [posi_rail[0], posi_rail[-1]]
        self.posi_line = sort_posi_list(list(filter(lambda posit: rg[0] <= posit <= rg[-1], posi_global)))
        print(self.posi_line)
        return self.posi_line

    def set_sub_rail(self, posi_all):
        sub_rail_list = list()
        sub_rail_dict = dict()
        for num in range(len(posi_all) - 1):
            l_posi = posi_all[num]
            r_posi = posi_all[num+1]
            z_trk = None
            rd = None
            for ele in self.line.rail.rail_list:
                if l_posi >= ele.l_posi and r_posi <= ele.r_posi:
                    z_trk = ele.ztrk
                    rd = ele.rd
            sub_rail_dict['钢轨段'+str(num+1)] = SubRailPi(self.line, '钢轨段'+str(num+1),
                                                        l_posi=l_posi, r_posi=r_posi,
                                                        z_trk=z_trk, rd=rd)
            sub_rail_list.append(sub_rail_dict['钢轨段'+str(num+1)])

        return sub_rail_dict

    # 获得模型的节点
    def set_node_dict(self):
        self.node_dict.clear()
        for posi in self.posi_line:
            self.node_dict[posi] = Node(posi)
        for ele in self['元件'].values():
            self.node_dict[ele.posi_abs].element[ele.name] = ele
        for ele in self['钢轨'].values():
            self.node_dict[ele.l_posi].track[1] = ele
            self.node_dict[ele.r_posi].track[0] = ele

    # 设备和钢轨相连
    def link_track_ele(self):
        for node in self.node_dict.values():
            for ele in node.element.values():
                if node.track[1] is not None:
                    self.equal_varb([ele.md_list[-1], -2], [node.track[1].md_list[0], 0])
                else:
                    self.equal_varb([ele.md_list[-1], -2], [node.track[0].md_list[0], 2])


class MainModel(ElePack):
    def __init__(self, line_group):
        super().__init__(None, line_group.name_base)
        self.line_group = line_group

        for line in line_group.element.values():
            self[line.name_base] = SingleLineModel(self, line)
        self.set_line_mutual()
        # self.ele_set = get_element()
        self.equs_kirchhoff = self.get_equs_kirchhoff()

    def set_line_mutual(self):
        if len(self.element) == 2:
            lines = list(self.element.values())
            set1 = set(lines[0].node_dict.keys())
            set2 = set(lines[1].node_dict.keys())
            node_set = list(set1.intersection(set2))
            node_set.sort()
            for posi in node_set[:-1]:
                lines[0].node_dict[posi].track[1].mutual_trk = lines[1].node_dict[posi].track[1]
                lines[1].node_dict[posi].track[1].mutual_trk = lines[0].node_dict[posi].track[1]

    def get_equs_kirchhoff(self):
        equs = list()
        for line_model in self.element.values():
            # equs.extend(self.get_equ_unit(line_model, freq))
            equs.extend(self.get_equ_kcl(line_model))
            equs.extend(self.get_equ_kvl(line_model))
        return equs

    # 元器件方程
    @staticmethod
    def get_equ_unit(vessel, freq, equs):
        ele_set = get_element(vessel, ele_set=set())
        # equs = []
        for ele in ele_set:
            for module in ele.md_list:
                module.get_equs(freq)
                num = 1
                for equ in module.equs:
                    equ.name = module.name + '方程' + str(num)
                    equs.append(equ)
                    num += 1
        return equs

    # KCL方程
    @staticmethod
    def get_equ_kcl(line):
        equs = list()
        for num in range(len(line.posi_line)):
            node = line.node_dict[line.posi_line[num]]
            name = line.name + '_节点KCL方程' + str(num+1)
            equ = Equation(name=name)
            for ele in node.element.values():
                vb = ele.md_list[-1].varb_dict[ele.md_list[-1].varb_name[-1]]
                equ.add_varb(vb, 1)
            if node.track[0] is not None:
                ele = node.track[0]
                vb = ele.md_list[-1].varb_dict[ele.md_list[-1].varb_name[-1]]
                equ.add_varb(vb, 1)
            if node.track[1] is not None:
                ele = node.track[1]
                vb = ele.md_list[-1].varb_dict[ele.md_list[-1].varb_name[1]]
                equ.add_varb(vb, 1)
            equs.append(equ)
        return equs

    # KVL方程
    @staticmethod
    def get_equ_kvl(line):
        equs = list()
        posi_line = line.posi_line[1:-1]
        for num in range(len(posi_line)):
            node = line.node_dict[posi_line[num]]
            name = line.name + '_节点KVL方程' + str(num+1)
            equ = Equation(name=name)
            if node.track[0] is not None:
                ele = node.track[0]
                vb = ele.md_list[-1].varb_dict[ele.md_list[-1].varb_name[-2]]
                equ.add_varb(vb, 1)
            if node.track[1] is not None:
                ele = node.track[1]
                vb = ele.md_list[-1].varb_dict[ele.md_list[-1].varb_name[0]]
                equ.add_varb(vb, -1)
            equs.append(equ)
        return equs


# 从等式获取变量
def get_varb_set(equs):
    varb_set = set()
    for equ in equs:
        for ele in equ.vb_list:
            varb_set.add(ele[0])
    return varb_set.copy()


def get_matrix(equs):
    varb_set = get_varb_set(equs)
    set_varb_num(varb_set)
    length = len(equs)
    mtrx = np.matlib.zeros((length, length), dtype=complex)

    for num in range(length):
        for varb, value in equs[num].vb_list:
            mtrx[num, varb.num] = value
    return mtrx


# 变量编号
def set_varb_num(var_set):
    name_list = []
    for varb in var_set:
        name_list.append(varb.get_varb_name())
    name_list.sort()
    varb_list = [None] * len(name_list)
    for varb in var_set:
        name = varb.get_varb_name()
        varb.num = name_list.index(name)
        varb_list[varb.num] = varb
    return varb_list


########################################################################################################################

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


########################################################################################################################

# 方程组排序
def equ_sort(equs):
    name_list = []
    for equ in equs:
        name_list.append(equ.name)
    name_list.sort()
    equ_dict = {}
    equ_list = [None] * len(name_list)
    for equ in equs:
        name = equ.name
        equ.num = name_list.index(name)
        equ_list[equ.num] = equ
        equ_dict[name] = equ
    return equ_list, equ_dict


########################################################################################################################

# # 获得钢轨上任意位置电压电流
# def get_rail_ui(line, value, posi, freq):
#     u_rail = 0
#     i_rail = 0
#     for ele in line['钢轨'].element.values():
#         if posi == ele.para['左端位置']:
#             u_rail = value[ele['等效电路']['U1'].num]
#             i_rail = value[ele['等效电路']['I1'].num]
#         elif posi == ele.para['右端位置']:
#             u_rail = value[ele['等效电路']['U2'].num]
#             i_rail = - value[ele['等效电路']['I2'].num]
#         elif ele.para['左端位置'] < posi < ele.para['右端位置']:
#             pi_temp = TCircuitRailPi('未定义', 'Pi等效',
#                                      l_posi=ele.para['左端位置'],
#                                      r_posi=ele.para['右端位置'],
#                                      z_trk=ele['等效电路'].z_trk,
#                                      rd=ele['等效电路'].rd)
#             u1 = value[ele['等效电路']['U1'].num]
#             i1 = value[ele['等效电路']['I1'].num]
#             u_rail, i_rail = pi_temp.getU2I2(u1, i1, freq)
#             i_rail = -i_rail
#     return u_rail, i_rail


def show_ele(vessel, para=''):
    if isinstance(vessel, (list, set)):
        list_t = list()
        for ele in vessel:
            if para == '':
                list_t.append(ele.__repr__())
            else:
                list_t.append(ele.__dict__[para].__repr__())
        list_t.sort()
        for ele in list_t:
            print(ele)
    elif isinstance(vessel, (dict, ElePack)):
        keys = sorted(list(vessel.keys()))
        for key in keys:
            if para == '':
                print(key, ':', vessel[key])
            else:
                print(vessel[key].__dict__[para])


with open('TCSR_2000A_data_lib.pkl', 'rb') as pk_f:
    TCSR_2000A = pickle.load(pk_f)

TCSR_2000A['Ccmp_z'] = pc.ParaMultiF(1700, 2000, 2300, 2600)
TCSR_2000A['Ccmp_z'].rlc_s = {
    1700: [10e-3, None, 25e-6],
    2000: [10e-3, None, 25e-6],
    2300: [10e-3, None, 25e-6],
    2600: [10e-3, None, 25e-6]}

# 钢轨阻抗
TCSR_2000A['Trk_z'] = pc.ParaMultiF(1700, 2000, 2300, 2600)
TCSR_2000A['Trk_z'].rlc_s = {
    1700: [1.177, 1.314e-3, None],
    2000: [1.306, 1.304e-3, None],
    2300: [1.435, 1.297e-3, None],
    2600: [1.558, 1.291e-3, None]}

TCSR_2000A['Rd'] = 10000
TCSR_2000A['Rsht_z'] = 10e-3

# 载频
FREQ = 2600


#######################################################################################################################

if __name__ == '__main__':
    # print(time.asctime(time.localtime()))
    # # 载频
    # # 钢轨初始化
    # r1 = Rail(upper_ins=None, name_base='主串钢轨', trk_num=1,
    #           posi=[-np.inf, np.inf],
    #           ztrk=[TCSR_2000A['Trk_z']],
    #           rd=[TCSR_2000A['Rd']])

    # 轨道电路初始化
    sg1 = SectionGroup(name_base='地面', posi=0, m_num=2, freq1=2600,
                       m_length=[509, 389, 320],
                       j_length=[29, 29, 29, 29],
                       m_type=['2000A', '2000A', '2000A'],
                       c_num=[6, 6, 5])

    sg2 = SectionGroup(name_base='地面', posi=0, m_num=2, freq1=1700,
                       m_length=[480, 200, 320],
                       j_length=[29, 29, 29, 29],
                       m_type=['2000A', '2000A', '2000A'],
                       c_num=[8, 6, 5])

    train1 = Train(parent_ins=None, name_base='列车1', posi_abs=0)

    # 生成线路
    l1 = Line(name_base='线路1', sec_group=sg1, train=train1)
    l2 = Line(name_base='线路2', sec_group=sg2)
    lg = LineGroup(l1, name_base='线路组')

    # 建立模型
    model = MainModel(lg)

    # output = []
    # for i in range(0, 600, 1):
    #     set_posi_abs(train1, i)
    #     l1.set_sub_rail(ele_all=ele_all)
    #     # l2.set_sub_rail(ele_all=ele_all)
    #     # 生成矩阵
    #     # m1 = Matrix(l1, l2, freq=FREQ)
    #     m1 = Matrix(l1, freq=FREQ)
    #     b = np.zeros(m1.length, dtype=complex)
    #     # b[m1.equ_dict['主串_区段1_电压源方程1'].num] = 100
    #     b[m1.equ_dict['主串_区段1_TCSR1_1发送器_1电压源方程1'].num] = 181
    #
    #     # 结果
    #     value_c = np.linalg.solve(m1.matrx, b)
    #     # del m1
    #
    #     if l1.node_dict[i].track[0] is not None:
    #         data = abs(value_c[l1.node_dict[i].track[0]['I2'].num])
    #     else:
    #         data = 0
    #
    #     # l2.node_dict[i].track[0]['I2']
    #     # x = abs(value_c[train1['分路电阻1']['阻抗']['I'].num])
    #     # x = np.angle(value_c[rc1['区段1']['TCSR2']['发送接收器']['采样电阻']['U'].num])/np.pi*180
    #     # print(x)
    #     output.append(data)

    # # 后处理
    # U_list = []
    # I_list = []
    # for i in range(2500):
    #     U,I = get_rail_ui(l1, value_c, i, FREQ)
    #     if U:
    #         U_list.append(abs(U))
    #         I_list.append(abs(I))

    # a = sp.Matrix(m1.matrx)
    # 画图
    # plt.title("Matplotlib demo")
    # plt.xlabel("x axis caption")
    # plt.ylabel("y axis caption")
    # plt.plot(output)
    # print(time.asctime(time.localtime()))
    # plt.show()

    pass
