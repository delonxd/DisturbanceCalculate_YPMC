import numpy as np
import numpy.matlib
import pickle
import time
from src import ElectricParameter as pc
from matplotlib import pyplot as plt

########################################################################################################################


class Varb:
    # def __init__(self, upper_module=None):im
    #     self.upper_name = upper_module
    #     self.num = None
    #     self.name = ''

    def __init__(self, upper_module=None, name_base=''):
        self.upper_module = upper_module
        self.name_base = name_base
        self.num = None
        self.name = ''

    def get_varb_name(self):
        self.name = self.upper_module.name + '_' + self.name_base
        return self.name

    def __repr__(self):
        return repr((self.get_varb_name(), self.num))


class EquBase:
    def __init__(self, keys, values, typ=''):
        self.keys = keys
        self.values = values
        self.varb_dict = dict(zip(self.keys, self.values))
        self.typ = typ
        self.constant = 0

    def add_varb(self, key, value):
        self.keys.append(key)
        self.values.append(value)
        self.varb_dict[key] = value


########################################################################################################################

# 元素包
class ElePack:
    def __init__(self, upper_ins, name_base):
        self.para = dict()
        self.para['上级元素'] = upper_ins
        self.para['基础名称'] = name_base
        self.name = ''
        self.element = {}
        self.ele_list = []
        self.flag_outside = False
        self.flag_ele_list = False
        self.flag_ele_unit = False

    def __len__(self):
        return len(self.element)

    def __getitem__(self, key):
        return self.element[key]

    def __setitem__(self, key, value):
        self.element[key] = value

    def values(self):
        return self.element.values()

    def keys(self):
        return self.element.keys()

    def items(self):
        return self.element.items()

    def init_position(self, posi):
        self.para['相对位置'] = posi
        self.para['绝对位置'] = 0
        self.flag_outside = True

    def add_element(self, name, instance):
        if self.flag_ele_list:
            self.element[name] = instance
            self.ele_list.append(instance)


class EleModule(ElePack):
    def __init__(self, upper_ins, name_base):
        ElePack.__init__(self, upper_ins, name_base)
        self.varb_dict = dict()
        self.equ_base = list()
        self.equs = list()
        self.md_list = [self]

    def __len__(self):
        return len(self.varb_dict)

    def __getitem__(self, key):
        return self.varb_dict[key]

    def __setitem__(self, key, value):
        self.varb_dict[key] = value

    def values(self):
        return self.varb_dict.values()

    def keys(self):
        return self.varb_dict.keys()

    def items(self):
        return self.varb_dict.items()


########################################################################################################################

# 一端口元件
class OnePortNetwork(EleModule):
    def __init__(self, upper_ins, name_base):
        EleModule.__init__(self, upper_ins, name_base)
        self.varb_name = ['U', 'I']
        self.varb_dict = {'U': Varb(self, 'U'),
                          'I': Varb(self, 'I')}


# 二端口网络
class TwoPortNetwork(EleModule):
    def __init__(self, upper_ins, name_base):
        EleModule.__init__(self, upper_ins, name_base)
        self.varb_name = ['U1', 'I1', 'U2', 'I2']
        self.varb_dict = {'U1': Varb(self, 'U1'),
                          'I1': Varb(self, 'I1'),
                          'U2': Varb(self, 'U2'),
                          'I2': Varb(self, 'I2')}


########################################################################################################################

# 并联阻抗
class OPortZ(OnePortNetwork):
    def __init__(self, upper_ins, name_base, z):
        OnePortNetwork.__init__(self, upper_ins, name_base)
        self.z = z

    def get_equ_base(self, freq):
        z = self.z[freq].z
        self.equ_base = [EquBase(['U', 'I'], [-1, z])]

    def get_equs(self, freq):
        z = self.z[freq].z
        self.equs = [Equation(varbs=[self['U'], self['I']], values=[-1, z])]


# 并联电压源
class OPortPowerU(OnePortNetwork):
    def __init__(self, upper_ins, name_base, voltage=0):
        OnePortNetwork.__init__(self, upper_ins, name_base)
        self.voltage = voltage

    def get_equ_base(self, freq):
        self.equ_base = [EquBase(['U'], [1])]
        self.equ_base[0].constant = self.voltage

    def get_equs(self, freq):
        self.equs = [Equation(varbs=[self['U']], values=[1])]


# 并联电流源
class OPortPowerI(OnePortNetwork):
    def __init__(self, upper_ins, name_base):
        OnePortNetwork.__init__(self, upper_ins, name_base)

    def get_equ_base(self, freq):
        self.equ_base = [EquBase(['I'], [1])]

    def get_equs(self, freq):
        self.equs = [Equation(varbs=[self['I']], values=[1])]


########################################################################################################################

# Pi型二端口网络
class TPortCircuitPi(TwoPortNetwork):
    def __init__(self, upper_ins, name_base, y1, y2, y3):
        TwoPortNetwork.__init__(self, upper_ins, name_base)
        self.y1 = y1
        self.y2 = y2
        self.y3 = y3

    def get_equ_base(self, freq):
        y1 = self.y1[freq].z
        y2 = self.y2[freq].z
        y3 = self.y3[freq].z
        equ1 = EquBase(['I1', 'U1', 'U2'], [-1, -(y1 + y2), -y2])
        equ2 = EquBase(['I2', 'U1', 'U2'], [-1, -y2, (y2 + y3)])
        self.equ_base = [equ1, equ2]

    def get_equs(self, freq):
        y1 = self.y1[freq].z
        y2 = self.y2[freq].z
        y3 = self.y3[freq].z
        equ1 = Equation(varbs=[self['I1'], self['U1'], self['U2']],
                        values=[-1, -(y1 + y2), -y2])
        equ2 = Equation(varbs=[self['I2'], self['U1'], self['U2']],
                        values=[-1, -y2, (y2 + y3)])
        self.equs = [equ1, equ2]


# T型二端口网络
class TPortCircuitT(TwoPortNetwork):
    def __init__(self, upper_ins, name_base, z1, z2, z3):
        TwoPortNetwork.__init__(self, upper_ins, name_base)
        self.z1 = z1
        self.z2 = z2
        self.z3 = z3

    def get_equ_base(self, freq):
        z1 = self.z1[freq].z
        z2 = self.z2[freq].z
        z3 = self.z3[freq].z
        equ1 = EquBase(['U1', 'I1', 'I2'], [-1, -(z1 + z2), z2])
        equ2 = EquBase(['U2', 'I1', 'I2'], [-1, -z2, (z2 + z3)])
        self.equ_base = [equ1, equ2]

    def get_equs(self, freq):
        z1 = self.z1[freq].z
        z2 = self.z2[freq].z
        z3 = self.z3[freq].z
        equ1 = Equation(varbs=[self['U1'], self['I1'], self['I2']],
                        values=[-1, -(z1 + z2), z2])
        equ2 = Equation(varbs=[self['U2'], self['I1'], self['I2']],
                        values=[-1, -z2, (z2 + z3)])
        self.equs = [equ1, equ2]


########################################################################################################################

# 变压器二端口网络
class TPortCircuitN(TwoPortNetwork):
    def __init__(self, upper_ins, name_base, n):
        TwoPortNetwork.__init__(self, upper_ins, name_base)
        self.n = n

    def get_equ_base(self, freq):
        n = self.n[freq]
        equ1 = EquBase(['U1', 'U2'], [-1, n])
        equ2 = EquBase(['I1', 'I2'], [n, -1])
        self.equ_base = [equ1, equ2]

    def get_equs(self, freq):
        n = self.n[freq]
        equ1 = Equation(varbs=[self['U1'], self['U2']],
                        values=[-1, n])
        equ2 = Equation(varbs=[self['I1'], self['I2']],
                        values=[n, -1])
        self.equs = [equ1, equ2]


# 串联二端口网络
class TPortZSeries(TwoPortNetwork):
    def __init__(self, upper_ins, name_base, z):
        TwoPortNetwork.__init__(self, upper_ins, name_base)
        self.z = z

    def get_equ_base(self, freq):
        z = self.z[freq].z
        equ1 = EquBase(['U1', 'U2', 'I2'], [1, -1, z])
        equ2 = EquBase(['I1', 'I2'], [-1, 1])
        self.equ_base = [equ1, equ2]

    def get_equs(self, freq):
        z = self.z[freq].z
        equ1 = Equation(varbs=[self['U1'], self['U2'], self['I2']],
                        values=[1, -1, z])
        equ2 = Equation(varbs=[self['I1'], self['I2']],
                        values=[-1, 1])
        self.equs = [equ1, equ2]


# 并联二端口网络
class TPortZParallel(TwoPortNetwork):
    def __init__(self, upper_ins, name_base, z):
        TwoPortNetwork.__init__(self, upper_ins, name_base)
        self.z = z

    def get_equ_base(self, freq):
        z = self.z[freq].z
        equ1 = EquBase(['U1', 'I1', 'I2'], [-1, -z, z])
        equ2 = EquBase(['U2', 'I1', 'I2'], [-1, -z, z])
        self.equ_base = [equ1, equ2]

    def get_equs(self, freq):
        z = self.z[freq].z
        equ1 = Equation(varbs=[self['U1'], self['I1'], self['I2']],
                        values=[-1, -z, z])
        equ2 = Equation(varbs=[self['U2'], self['I1'], self['I2']],
                        values=[-1, -z, z])
        self.equs = [equ1, equ2]


########################################################################################################################

class UPowerOut(OPortPowerU):
    def __init__(self, upper_ins, name_base, posi):
        OPortPowerU.__init__(self, upper_ins, name_base)
        ElePack.init_position(self, posi)
        self.flag_ele_unit = True


# 室外阻抗
class ZOutside(OPortZ):
    def __init__(self, upper_ins, name_base, posi, z):
        OPortZ.__init__(self, upper_ins, name_base, z)
        ElePack.init_position(self, posi)
        self.flag_ele_unit = True
        self.z = z


# 补偿电容
class CapC(ZOutside):
    def __init__(self, upper_ins, name_base, posi, z):
        ZOutside.__init__(self, upper_ins, name_base, posi, z)


# 空心线圈
class SVA(ZOutside):
    def __init__(self, upper_ins, name_base, posi, z):
        ZOutside.__init__(self, upper_ins, name_base, posi, z)


# TB
class TB(ZOutside):
    def __init__(self, upper_ins, name_base, posi, z):
        ZOutside.__init__(self, upper_ins, name_base, posi, z)


# 室外电阻
class ROutside(ZOutside):
    def __init__(self, upper_ins, name_base, posi, z):
        ZOutside.__init__(self, upper_ins, name_base, posi, z)

    def get_equ_base(self, freq):
        z = self.z
        self.equ_base = [EquBase(['U', 'I'], [-1, z])]

    def get_equs(self, freq):
        z = self.z
        equ1 = Equation(varbs=[self['U'], self['I']],
                        values=[-1, z])
        self.equs = [equ1]


########################################################################################################################

# 发送器
class TcsrPower(ElePack):
    def __init__(self, upper_ins, name_base, z):
        ElePack.__init__(self, upper_ins, name_base)
        self.flag_ele_list = True
        self.para['电阻'] = z
        self.add_element('1电压源', OPortPowerU(self, '1电压源'))
        self.add_element('2内阻', TPortZSeries(self, '2内阻', z))


# 接收器
class TcsrReceiver(OPortZ):
    def __init__(self, upper_ins, name_base, z):
        OPortZ.__init__(self, upper_ins, name_base, z)


########################################################################################################################

# 变压器模板
class TcsrTransformer(ElePack):
    def __init__(self, upper_ins, name_base, z1, z2, n):
        ElePack.__init__(self, upper_ins, name_base)
        self.flag_ele_list = True
        self.add_element('1等效内阻', TPortCircuitT(self, '1等效内阻', z1, z2, z1))
        self.add_element('2变压器', TPortCircuitN(self, '2变压器', n))


# 防雷变压器
class TcsrFL(TcsrTransformer):
    def __init__(self, upper_ins, name_base, z1, z2, n):
        TcsrTransformer.__init__(self, upper_ins, name_base, z1, z2, n)


# TAD变压器
class TcsrTAD(TcsrTransformer):
    def __init__(self, upper_ins, name_base, z1, z2, z3, n, zc):
        ElePack.__init__(self, upper_ins, name_base)
        self.flag_ele_list = True
        self.add_element('1共模电感', TPortZSeries(self, '1共模电感', z3))
        self.add_element('2等效内阻', TPortCircuitT(self, '2等效内阻', z1, z2, z1))
        self.add_element('3变压器', TPortCircuitN(self, '3变压器', n))
        self.add_element('4串联电容', TPortZSeries(self, '4串联电容', zc))


########################################################################################################################

# 电缆等效电路
class TPortCable(TwoPortNetwork):
    def __init__(self, upper_ins, name_base, length, cab_r=43, cab_l=825e-6, cab_c=28e-9):
        TwoPortNetwork.__init__(self, upper_ins, name_base)
        self.R = cab_r
        self.L = cab_l
        self.C = cab_c
        self.length = length

    def get_equ_base(self, freq):
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
        equ1 = EquBase(['I1', 'U1', 'U2'], [-1, -(y1 + y2), -y2])
        equ2 = EquBase(['I2', 'U1', 'U2'], [-1, -y2, (y2 + y3)])
        self.equ_base = [equ1, equ2]

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


########################################################################################################################

# 匹配单元
class TcsrBA(TPortZParallel):
    def __init__(self, upper_ins, name_base, z):
        TPortZParallel.__init__(self, upper_ins, name_base, z)


# 引接线
class TcsrCA(TPortZSeries):
    def __init__(self, upper_ins, name_base, z):
        TPortZSeries.__init__(self, upper_ins, name_base, z)


########################################################################################################################

# 发送接收端
class TCSR(ElePack):
    def __init__(self, upper_ins, name_base, posi, m_type, j_type, freq, cable_length=10,
                 mode='发送', level=1):
        ElePack.__init__(self, upper_ins, name_base)
        ElePack.init_position(self, posi)
        self.flag_ele_list = True
        self.flag_ele_unit = True
        self.para['主轨类型'] = m_type
        self.para['绝缘节类型'] = j_type
        self.para['频率'] = freq
        self.para['模式'] = mode
        self.para['电平级'] = level
        self.para['电缆长度'] = cable_length

        if self.para['模式'] == '发送':
            self.add_element('1发送器', TcsrPower(self, '1发送器', TCSR_2000A['z_pwr'][level]))
        elif self.para['模式'] == '接收':
            self.add_element('1接收器', TcsrReceiver(self, '1接收器', TCSR_2000A['Z_rcv']))
        self.add_element('2防雷', TcsrFL(self, '2防雷',
                                       TCSR_2000A['FL_z1_发送端'],
                                       TCSR_2000A['FL_z2_发送端'],
                                       TCSR_2000A['FL_n_发送端']))
        self.add_element('3Cab', TPortCable(self, '3Cab', self.para['电缆长度']))
        self.add_element('4TAD', TcsrTAD(self, '4TAD',
                                         TCSR_2000A['TAD_z1_发送端_区间'],
                                         TCSR_2000A['TAD_z2_发送端_区间'],
                                         TCSR_2000A['TAD_z3_发送端_区间'],
                                         TCSR_2000A['TAD_n_发送端_区间'],
                                         TCSR_2000A['TAD_c_发送端_区间']))
        self.add_element('5BA', TcsrBA(self, '5BA', TCSR_2000A['PT'][freq]))
        self.add_element('6CA', TcsrCA(self, '6CA', TCSR_2000A['CA_z_区间']))

        self.md_list = get_md_list(self, [])
        self.config_varb()

    # 变量赋值
    def config_varb(self):
        for num in range(len(self.md_list) - 1):
            equal_varb([self.md_list[num], -2], [self.md_list[num + 1], 0])
            equal_varb([self.md_list[num], -1], [self.md_list[num + 1], 1])


########################################################################################################################

# 钢轨段
class SubRailPi(TwoPortNetwork):
    def __init__(self, upper_ins, name_base, l_posi, r_posi, z_trk, rd):
        TwoPortNetwork.__init__(self, upper_ins, name_base)
        ElePack.init_position(self, l_posi)
        self.flag_ele_unit = True
        self.para['左端位置'] = l_posi
        self.para['右端位置'] = r_posi
        self.para['钢轨长度'] = r_posi - l_posi
        self.para['钢轨阻抗'] = z_trk
        self.para['道床电阻'] = rd

    def get_equ_base(self, freq):
        z_trk = self.para['钢轨阻抗']
        rd = self.para['道床电阻']
        length = self.para['钢轨长度'] / 1000
        y_tk = 1 / z_trk[freq].z / length
        y_rd = 1 / rd * length
        equ1 = EquBase(['I1', 'U1', 'U2'], [-1, (y_rd + y_tk), -y_tk])
        equ2 = EquBase(['I2', 'U1', 'U2'], [-1, -y_tk, (y_tk + y_rd)])
        self.equ_base = [equ1, equ2]
        if hasattr(self, 'mutual_trk'):
            m_circuit = self.mutual_trk
            m = length * 0.30
            equ1.add_varb('Im', (m * (y_rd + y_tk)))
            equ2.add_varb('Im', -(m * y_tk))
            self.varb_dict['Im'] = m_circuit.varb_dict['I1']

    def get_equs(self, freq):
        z_trk = self.para['钢轨阻抗']
        rd = self.para['道床电阻']
        length = self.para['钢轨长度'] / 1000
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

# 绝缘节
class Joint(ElePack):
    def __init__(self, upper_ins, name_base, posi):
        ElePack.__init__(self, upper_ins, name_base)
        ElePack.init_position(self, posi)

        self.para['本区段元件'] = {}
        self.para['邻区段元件'] = {}
        self.para['绝缘节元件'] = {}

    def set_element(self):
        self.element = {}
        for ele in self.para['本区段元件'].values():
            self.element['本区段' + str(ele.para['基础名称'])] = ele
        for ele in self.para['绝缘节元件'].values():
            self.element[str(ele.para['基础名称'])] = ele
        for ele in self.para['邻区段元件'].values():
            self.element['邻区段' + str(ele.para['基础名称'])] = ele


########################################################################################################################

# 区段
class Section(ElePack):
    def __init__(self, upper_ins, name_base,
                 posi, m_type, m_freq, m_length, j_length, c_num, j_type, j_devi, sr_mode):
        ElePack.__init__(self, upper_ins, name_base)
        ElePack.init_position(self, posi)

        self.para['主轨类型'] = m_type
        self.para['主轨频率'] = m_freq
        self.para['主轨长度'] = m_length
        self.para['调谐区长度'] = j_length
        self.para['电容数量'] = c_num
        self.para['调谐区类型'] = j_type
        self.para['发送器类型'] = j_devi
        if sr_mode == '左发':
            self.para['发送接收模式'] = ['发送', '接收']
        elif sr_mode == '右发':
            self.para['发送接收模式'] = ['接收', '发送']
        self.set_element()

    def set_element(self):
        para = self.para
        if para['主轨类型'] == '2000A':
            # 位置参数
            lc = (para['主轨长度'] / para['电容数量']) if para['电容数量'] > 0 else 0
            para['电容位置'] = [(num * lc + lc / 2 + para['调谐区长度'][0]) for num in range(para['电容数量'])]
            para['TCSR位置'] = [para['调谐区长度'][0], self.para['主轨长度'] + para['调谐区长度'][0]]
            para['绝缘节位置'] = [0, para['TCSR位置'][1]]
            posi_tcsr_o = [0, para['调谐区长度'][1]]

            # 设置电容
            for num in range(para['电容数量']):
                self.element['C' + str(num + 1)] = CapC(upper_ins=self, name_base='C' + str(num + 1),
                                                        posi=para['电容位置'][num], z=TCSR_2000A['Ccmp_z'])

            # self.element['TB'] = TB(upper_ins=self, name_base='TB', posi=23, z=TCSR_2000A['TB_z'])

            # 设置发送接收器
            for num in range(2):
                self.element['TCSR' + str(num+1)] = TCSR(upper_ins=self,
                                                         name_base='TCSR' + str(num+1),
                                                         posi=para['TCSR位置'][num],
                                                         m_type=para['主轨类型'],
                                                         j_type=para['调谐区类型'][num],
                                                         freq=para['主轨频率'],
                                                         cable_length=10,
                                                         mode=para['发送接收模式'][num],
                                                         level=1)
            # 设置绝缘节
            for num in range(2):
                name_j = '左侧绝缘节' if num == 0 else '右侧绝缘节'
                joint_t = Joint(upper_ins=self, name_base=name_j, posi=para['绝缘节位置'][num])
                joint_t.para['本区段元件']['TCSR'] = self.element['TCSR' + str(num+1)]
                if para['调谐区类型'][num] == '电气':
                    joint_t.para['邻区段元件']['TCSR'] = TCSR(upper_ins=joint_t,
                                                         name_base='相邻TCSR',
                                                         posi=posi_tcsr_o[num],
                                                         m_type=para['主轨类型'],
                                                         j_type='电气',
                                                         freq=change_freq(para['主轨频率']),
                                                         cable_length=10,
                                                         mode=para['发送接收模式'][-1 - num],
                                                         level=1)

                    joint_t.para['绝缘节元件']['SVA'] = SVA(upper_ins=joint_t,
                                                       name_base='SVA',
                                                       posi=(para['调谐区长度'][num] / 2),
                                                       z=TCSR_2000A['SVA_z'])
                joint_t.set_element()
                self.element[name_j] = joint_t
            self.para = para
        else:
            raise KeyboardInterrupt(para['主轨类型'] + '暂为不支持的主轨类型')


########################################################################################################################

# 轨道电路
class TrackCircuit(ElePack):
    def __init__(self, name_base, posi, m_num, freq1, m_length, j_length, m_type, c_num):
        ElePack.__init__(self, None, name_base)
        ElePack.init_position(self, posi)
        self.para['区段数量'] = m_num
        self.para['左端区段载频'] = freq1
        self.para['主轨类型'] = m_type
        self.para['主轨长度'] = m_length
        self.para['小轨长度'] = j_length
        self.para['电容数量'] = c_num
        self.section_list = []
        self.ele_posi = []
        self.set_element()

    # 配置线路
    def set_element(self):
        self.check_num()
        self.config_freq()
        self.config_para()
        self.link_section()
        self.refresh()

    def refresh(self):
        set_posi_abs(self, 0)
        set_ele_name(self, '')
        self.ele_posi = get_posi_abs(self, posi_list=[])

    # 检查主轨与绝缘节数量
    def check_num(self):
        para = self.para
        para['主轨类型'] = para['主轨类型'][:para['区段数量']]
        para['主轨长度'] = para['主轨长度'][:para['区段数量']]
        para['电容数量'] = para['电容数量'][:para['区段数量']]
        para['小轨长度'] = para['小轨长度'][:(para['区段数量'] + 1)]

    # 设置频率
    def config_freq(self):
        para = self.para
        para['主轨频率'] = []
        freq = para['左端区段载频']
        for num in range(para['区段数量']):
            para['主轨频率'].append(freq)
            freq = change_freq(freq)

    # 设置区段参数
    def config_para(self):
        para = self.para
        j_length = para['小轨长度']
        j_type = ['电气' if num > 0 else '机械' for num in j_length]
        para['调谐区长度'] = [[j_length[num], j_length[num+1]] for num in range(para['区段数量'])]
        para['调谐区类型'] = [[j_type[num], j_type[num+1]] for num in range(para['区段数量'])]
        para['发送器类型'] = ['PT', 'PT']
        para['区段位置'] = []
        posi_t = 0
        for num in range(para['区段数量']):
            para['区段位置'].append(posi_t)
            posi_t += para['小轨长度'][num] + para['主轨长度'][num]

        for num in range(para['区段数量']):
            sec_t = Section(upper_ins=self,
                            name_base='区段' + str(num+1),
                            posi=para['区段位置'][num],
                            m_type=para['主轨类型'][num],
                            m_freq=para['主轨频率'][num],
                            m_length=para['主轨长度'][num],
                            j_length=para['调谐区长度'][num],
                            c_num=para['电容数量'][num],
                            j_type=para['调谐区类型'][num],
                            j_devi=para['发送器类型'],
                            sr_mode='左发')
            self.element['区段' + str(num+1)] = sec_t
            self.section_list.append(sec_t)
        self.para = para

    # 连接相邻区段
    def link_section(self):
        for num in range(self.para['区段数量'] - 1):
            sec1 = self.section_list[num]
            sec2 = self.section_list[num+1]

            if not sec1.para['调谐区类型'][1] == sec2.para['调谐区类型'][0]:
                raise KeyboardInterrupt(repr(sec1) + '和' + repr(sec2) + '调谐区类型不符无法相连')
            elif sec1.para['调谐区类型'][1] == '电气':
                if not sec1.para['主轨类型'] == sec2.para['主轨类型']:
                    raise KeyboardInterrupt(repr(sec1) + '和' + repr(sec2) + '主轨类型不符无法相连')
                elif not sec1.para['主轨频率'] == change_freq(sec2.para['主轨频率']):
                    raise KeyboardInterrupt(repr(sec1) + '和' + repr(sec2) + '主轨频率不符无法相连')
                elif not sec1.para['调谐区长度'][1] == sec2.para['调谐区长度'][0]:
                    raise KeyboardInterrupt(repr(sec1) + '和' + repr(sec2) + '调谐区长度不符无法相连')
                elif not sec1.para['发送器类型'][1] == sec2.para['发送器类型'][0]:
                    raise KeyboardInterrupt(repr(sec1) + '和' + repr(sec2) + '发送器类型不符无法相连')
                if not sec1.para['相对位置'] + sec1.para['绝缘节位置'][1] == sec2.para['相对位置']:
                    raise KeyboardInterrupt(repr(sec1) + '和' + repr(sec2) + '位置不符无法相连')
                else:
                    joint1 = sec1.element['右侧绝缘节']
                    joint2 = sec2.element['左侧绝缘节']
                    joint1.para['邻区段元件'] = joint2.para['本区段元件']
                    joint2.para['邻区段元件'] = joint1.para['本区段元件']
                    joint2.para['绝缘节元件'] = joint1.para['绝缘节元件']
                    joint1.set_element()
                    joint2.set_element()


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
    def __init__(self, upper_ins=None, name_base='',
                 trk_num=1, posi=None,
                 ztrk=None, rd=None):
        ElePack.__init__(self, upper_ins, name_base)
        self.para['节点位置'] = [-np.inf, np.inf] if posi is None else posi
        self.para['钢轨类型数量'] = trk_num
        self.para['钢轨阻抗'] = [TCSR_2000A['Trk_z']] if ztrk is None else ztrk
        self.para['道床电阻'] = [TCSR_2000A['Rd']] if rd is None else rd
        self.rail_list = []
        self.posi_list = []
        self.sub_rail_list = []
        self.set_rail_list()

    # 配置线路
    def set_rail_list(self):
        self.check_num()
        para = self.para
        self.posi_list = para['节点位置']
        for num in range(para['钢轨类型数量']):
            self.rail_list.append(RailSegment(l_posi=para['节点位置'][num],
                                              r_posi=para['节点位置'][num+1],
                                              ztrk=para['钢轨阻抗'][num],
                                              rd=para['道床电阻'][num]))

    def check_num(self):
        para = self.para
        para['节点位置'] = para['节点位置'][:(para['钢轨类型数量']+1)]
        para['钢轨阻抗'] = para['钢轨阻抗'][:para['钢轨类型数量']]
        para['道床电阻'] = para['道床电阻'][:para['钢轨类型数量']]

    def set_sub_rail(self, posi_all):
        self.sub_rail_list = []
        self.element = {}
        for num in range(len(posi_all) - 1):
            l_posi = posi_all[num]
            r_posi = posi_all[num+1]
            z_trk = None
            rd = None
            for ele in self.rail_list:
                if l_posi >= ele.l_posi and r_posi <= ele.r_posi:
                    z_trk = ele.ztrk
                    rd = ele.rd
            self.element['段'+str(num+1)] = SubRailPi(self, '段'+str(num+1),
                                                     l_posi=l_posi, r_posi=r_posi,
                                                     z_trk=z_trk, rd=rd)
            self.sub_rail_list.append(self.element['段'+str(num+1)])


########################################################################################################################

# 列车
class Train(ElePack):
    def __init__(self, upper_ins, name_base, posi_abs):
        ElePack.__init__(self, upper_ins, name_base)
        ElePack.init_position(self, 0)
        self.element['分路电阻1'] = ROutside(upper_ins=self, name_base='分路电阻1',
                                         posi=0, z=TCSR_2000A['Rsht_z'])
        set_ele_name(self)
        set_posi_abs(self, posi_abs)


########################################################################################################################

# 节点
class Node:
    def __init__(self, posi):
        self.posi = posi
        self.element = {}
        self.track = [None, None]


########################################################################################################################

# 线路
class Line(ElePack):
    def __init__(self, tc, rail=None):
        name = tc.para['基础名称'] + '线路'
        ElePack.__init__(self, None, name)
        self.tc = tc
        self.element['元件'] = ElePack(self, '元件')
        if rail is None:
            rail = Rail()
        rail.para['基础名称'] = tc.para['基础名称'] + '钢轨'
        self.element['钢轨'] = rail

        self.ele_set = get_element(tc, ele_set=set())
        self.posi_line = []
        self.var_set = set()
        self.node_dict = {}

    def add_train(self, train):
        self.ele_set = get_element(train, ele_set=self.ele_set)

    def get_posi_line(self, ele_all, ftype='元件'):
        # global ele_all
        posi_rail = self['钢轨'].posi_list
        posi_all = get_posi_fast(ele_all)
        posi_ele = get_posi_fast(self.ele_set)
        if ftype == '元件':
            rg = [posi_ele[0], posi_ele[-1]]
            if posi_ele[0] < posi_rail[0] or posi_ele[-1] > posi_rail[-1]:
                raise KeyboardInterrupt('钢轨范围异常')
        elif ftype == '钢轨':
            rg = [posi_rail[0], posi_rail[-1]]
        posi_line = sort_posi_list(list(filter(lambda posit: rg[0] <= posit <= rg[-1], posi_all)))
        return posi_line

    # 生成钢轨段
    def set_sub_rail(self, ele_all, ftype='元件'):
        self.posi_line = self.get_posi_line(ele_all=ele_all, ftype=ftype)
        self.element['元件'].element = choose_element(self.ele_set, self.posi_line)
        self.element['钢轨'].set_sub_rail(self.posi_line)
        set_ele_name(self, '')
        self.set_node_dict()
        self.link_track_ele()
        self.var_set = get_varb(self, varb_set=set())

    # 获得节点
    def set_node_dict(self):
        self.node_dict = {}
        for posi in self.posi_line:
            self.node_dict[posi] = Node(posi)
        for ele in self['元件'].values():
            self.node_dict[ele.para['绝对位置']].element[ele.name] = ele
        for ele in self['钢轨'].element.values():
            self.node_dict[ele.para['左端位置']].track[1] = ele
            self.node_dict[ele.para['右端位置']].track[0] = ele

    # 设备和钢轨相连
    def link_track_ele(self):
        for node in self.node_dict.values():
            for ele in node.element.values():
                if node.track[1] is not None:
                    equal_varb([ele.md_list[-1], -2], [node.track[1].md_list[0], 0])
                else:
                    equal_varb([ele.md_list[-1], -2], [node.track[0].md_list[0], 2])


########################################################################################################################

# # 方程
# class Equation:
#     def __init__(self, name):
#         self.name = name
#         self.vb_list = []
#
#     def set_equ_unit(self, module, equ_base):
#         for key in equ_base.keys:
#             tuple1 = (module.varb_dict[key], equ_base.varb_dict[key])
#             self.vb_list.append(tuple1)
#
#     def add_vrb(self, varb, value):
#         tuple1 = (varb, value)
#         self.vb_list.append(tuple1)


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


# 按位置筛选元件
def choose_element(ele_set, posi_abs):
    ele_dict = {}
    for ele in ele_set:
        if ele.para['绝对位置'] in posi_abs:
            ele_dict[ele.name] = ele
    return ele_dict


# 快速获取绝对位置
def get_posi_fast(ele_set):
    posi_all = []
    for ele in ele_set:
        posi_all.append(ele.para['绝对位置'])
    posi_all = sort_posi_list(posi_all)
    return posi_all


# 设置绝对位置
def set_posi_abs(vessel, abs_posi):
    if vessel.para['上级元素'] is None:
        vessel.para['绝对位置'] = vessel.para['相对位置'] + abs_posi
    else:
        vessel.para['绝对位置'] = vessel.para['上级元素'].para['绝对位置'] + vessel.para['相对位置']
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
        posi_list.append(vessel.para['绝对位置'])
        posi_list = sort_posi_list(posi_list)
    return posi_list


# 配置元器件的名称
def set_ele_name(vessel, prefix=''):
    if hasattr(vessel, 'para'):
        if '上级元素' in vessel.para.keys():
            if vessel.para['上级元素'] is None:
                vessel.name = prefix + vessel.para['基础名称']
            else:
                vessel.name = vessel.para['上级元素'].name + '_' + vessel.para['基础名称']
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


# # 获得所有节点
# def get_posi_all(*element, posi):
#     posi_all = posi
#     for ele in element:
#         posi_all.extend(get_posi_abs(ele))
#     posi_all = sort_posi_list(posi_all)
#     return posi_all


########################################################################################################################

# 获得元器件连接顺序的列表
def get_md_list(vessel, md_list):
    if vessel.flag_ele_list is True:
        for ele in vessel.ele_list:
            md_list = get_md_list(ele, md_list)
    else:
        md_list.append(vessel)
    return md_list


# 使两个模块的变量映射到同一个变量对象
def equal_varb(pack1, pack2):
    module1 = pack1[0]
    module2 = pack2[0]
    num1 = pack1[1]
    num2 = pack2[1]
    name1 = module1.varb_name[num1]
    name2 = module2.varb_name[num2]
    module1.varb_dict[name1] = module2.varb_dict[name2]


# 从等式获取变量
def get_varb_set(equs):
    varb_set = set()
    for equ in equs:
        for ele in equ.vb_list:
            varb_set.add(ele[0])
    return varb_set.copy()


# 获得所有变量
def get_varb(vessel, varb_set):
    if hasattr(vessel, 'varb_dict'):
        for ele in vessel.varb_dict.values():
            varb_set.add(ele)
    else:
        for ele in vessel.element.values():
            varb_set = get_varb(ele, varb_set)
    return varb_set.copy()


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

class Matrix:
    def __init__(self, *lines, freq):
        equs = []
        # varb_set = set()
        if len(lines) == 2:
            set1 = set(lines[0].node_dict.keys())
            set2 = set(lines[1].node_dict.keys())
            node_set = list(set1.intersection(set2))
            node_set.sort()
            for posi in node_set[:-2]:
                lines[0].node_dict[posi].track[1].mutual_trk = lines[1].node_dict[posi].track[1]
                lines[1].node_dict[posi].track[1].mutual_trk = lines[0].node_dict[posi].track[1]

        for line in lines:
            equs.extend(get_equ_unit(line, freq))
            equs.extend(get_equ_kvl(line))
            equs.extend(get_equ_kcl(line))
        # varb_set = get_varb(line, varb_set)
        self.equs = equs
        equs, self.equ_dict = equ_sort(equs)
        # show_ele(equs)
        # show_ele(self.equ_dict)
        varb_set = get_varb_set(equs)
        self.varb_list = set_varb_num(varb_set)

        length = len(varb_set)
        self.length = length
        matrx = np.matlib.zeros((length, length), dtype=complex)

        for num in range(length):
            for vb in equs[num].vb_list:
                matrx[num, vb[0].num] = vb[1]
        self.matrx = matrx


########################################################################################################################

# # 元器件方程
# def get_equ_unit(vessel, freq):
#     ele_dict = get_element(vessel, ele_set=set())
#     equs = []
#     for ele in ele_dict:
#         for module in ele.md_list:
#             module.get_equ_base(freq)
#             num = 1
#             for equ_base in module.equ_base:
#                 name = module.name + '方程' + str(num)
#                 equ = Equation(name)
#                 equ.set_equ_unit(module, equ_base)
#                 equs.append(equ)
#                 num += 1
#     return equs

# 元器件方程
def get_equ_unit(vessel, freq):
    ele_dict = get_element(vessel, ele_set=set())
    equs = []
    for ele in ele_dict:
        for module in ele.md_list:
            module.get_equs(freq)
            num = 1
            for equ in module.equs:
                equ.name = module.name + '方程' + str(num)
                equs.append(equ)
                num += 1
    return equs


# KCL方程
def get_equ_kcl(line):
    equs = []
    for num in range(len(line.posi_line)):
        node = line.node_dict[line.posi_line[num]]
        name = line.para['基础名称'] + '_节点KCL方程' + str(num+1)
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
def get_equ_kvl(line):
    equs = []
    posi_line = line.posi_line[1:-1]
    for num in range(len(posi_line)):
        node = line.node_dict[posi_line[num]]
        name = line.para['基础名称'] + '_节点KVL方程' + str(num+1)
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
        for ele in vessel:
            if para == '':
                print(ele)
            else:
                exec('print(ele.' + para + ')')
    elif isinstance(vessel, dict):
        for ele in vessel.items():
            if para == '':
                print(ele[0], ':', ele[1])
            else:
                exec('print(ele[1].' + para + ')')


#######################################################################################################################

if __name__ == '__main__':
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
    print(time.asctime(time.localtime()))
    # 载频
    FREQ = 2600
    # 钢轨初始化
    # r1 = Rail(upper_ins=None, name_base='主串钢轨', trk_num=1,
    #           posi=[-np.inf, np.inf],
    #           ztrk=[TCSR_2000A['Trk_z']],
    #           rd=[TCSR_2000A['Rd']])

    # 轨道电路初始化
    tc1 = TrackCircuit(name_base='主串', posi=0, m_num=1, freq1=2600,
                       m_length=[480, 500, 320],
                       j_length=[29, 29, 29, 29],
                       m_type=['2000A', '2000A', '2000A'],
                       c_num=[6, 6, 5])
    # rc1['区段1'].element['电压源'] = UPowerOut(upper_ins=rc1['区段1'], name_base='电压源', posi=29)
    # rc1.refresh()

    tc2 = TrackCircuit(name_base='被串', posi=0, m_num=2, freq1=1700,
                       m_length=[480, 200, 320],
                       j_length=[29, 29, 29, 29],
                       m_type=['2000A', '2000A', '2000A'],
                       c_num=[8, 6, 5])
    # rc1['区段1'].element.pop('C1')

    train1 = Train(upper_ins=None, name_base='列车1', posi_abs=0)
    # train2 = Train(name_base = '列车2', posi_abs = 150)
    # set_posi_abs(train1, 30)

    # 获得所有元件
    # ele_all = get_element(tc1, tc2, train1, ele_set=set())

    ele_all = get_element(tc1, train1, ele_set=set())

    # 生成线路
    l1 = Line(tc=tc1)
    # l2 = Line(tc=tc2)
    l1.add_train(train1)

    output = []
    for i in range(0, 600, 1):
        set_posi_abs(train1, i)
        l1.set_sub_rail(ele_all=ele_all)
        # l2.set_sub_rail()
        # 生成矩阵
        # m1 = Matrix(l1, l2, freq=FREQ)
        m1 = Matrix(l1, freq=FREQ)
        b = np.zeros(m1.length, dtype=complex)
        # b[m1.equ_dict['主串_区段1_电压源方程1'].num] = 100
        b[m1.equ_dict['主串_区段1_TCSR1_1发送器_1电压源方程1'].num] = 181

        # 结果
        value_c = np.linalg.solve(m1.matrx, b)
        # del m1

        if l1.node_dict[i].track[0] is not None:
            data = abs(value_c[l1.node_dict[i].track[0]['I2'].num])
        else:
            data = 0

        # l2.node_dict[i].track[0]['I2']
        # x = abs(value_c[train1['分路电阻1']['阻抗']['I'].num])
        # x = np.angle(value_c[rc1['区段1']['TCSR2']['发送接收器']['采样电阻']['U'].num])/np.pi*180
        # print(x)
        output.append(data)

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
    plt.title("Matplotlib demo")
    plt.xlabel("x axis caption")
    plt.ylabel("y axis caption")
    plt.plot(output)
    print(time.asctime(time.localtime()))
    plt.show()

