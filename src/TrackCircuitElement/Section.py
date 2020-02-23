from src.Module.OutsideElement import CapC
from src.Module.OutsideElement import TB
from src.TrackCircuitElement.Joint import *
import numpy as np

# 区段
class Section(ElePack):
    new_table = {
        '区段类型': 'm_type',
        '区段频率': 'm_freq',
        '区段长度': 's_length'
    }
    prop_table = ElePack.prop_table.copy()
    prop_table.update(new_table)

    def __init__(self, parent_ins, name_base,
                 m_frq, s_len, j_len, c_num,
                 j_typ, sr_mod, send_lv):
        super().__init__(parent_ins, name_base)
        self.parameter = parent_ins.parameter
        self.init_position(0)
        self.m_type = ''
        self.m_freq = m_frq
        self.s_length = s_len

        # 临时变量
        sr_mod_t = sr_mod
        if sr_mod_t == '左发':
            sr_mod = ['发送', '接收']
        elif sr_mod_t == '右发':
            sr_mod = ['接收', '发送']
        m_len = s_len - (j_len[0] + j_len[1]) / 2
        init_list = m_len, j_len, c_num, j_typ, sr_mod, send_lv
        self.set_element(init_list)

    @property
    def posi_rlt(self):
        posi = self.parent_ins.posi_dict[self.name_base]
        return posi

    def set_element(self, init_list):
        pass


# 2000A配置
class Section_ZPW2000A(Section):
    def __init__(self, parent_ins, name_base,
                 m_frq, s_len, j_len, c_num, j_typ, sr_mod, send_lv):
        super().__init__(parent_ins, name_base,
                         m_frq, s_len, j_len, c_num, j_typ, sr_mod, send_lv)
        self.m_type = '2000A'

    def set_element(self, init_list):
        m_len, j_lens, c_num, j_typs, sr_mods, send_lv = init_list
        offset = j_lens[0] / 2
        n_t = c_num * 2 + 1
        # 按ZPW-2000A原则设置电容
        hlf_pst = list(np.linspace(offset, (m_len + offset), n_t))
        c_pst = [hlf_pst[num*2+1] for num in range(c_num)]

        c_pst = c_pst[1:-1]

        # posi_mid2 = c_pst.pop(3)
        # posi_mid1 = c_pst.pop(1)

        self.config_c(c_pst)

        # frq = self.m_freq

        # ele = TB(parent_ins=self,
        #          name_base='TB1',
        #          posi=m_len/2,
        #          z=self.parameter['TB'][self.m_freq.value])
        # self.add_child('TB1', ele)

        # ele = TB(parent_ins=self,
        #          name_base='TB2',
        #          posi=(m_len-18),
        #          z=self.parameter['TB'][self.m_freq.value])
        # self.add_child('TB2', ele)

        # ele = TB(parent_ins=self,
        #          name_base='TB_mid1',
        #          posi=posi_mid1,
        #          z=self.parameter['TB'][self.m_freq.value])
        # self.add_child('TB_mid1', ele)
        #
        # ele = TB(parent_ins=self,
        #          name_base='TB_mid2',
        #          posi=posi_mid2,
        #          z=self.parameter['TB'][self.m_freq.value])
        # self.add_child('TB_mid2', ele)


        j_clss, tcsr_clss = self.config_class(j_typs=j_typs)



        self.config_joint_tcsr(j_clss=j_clss,
                               tcsr_clss=tcsr_clss,
                               j_lens=j_lens,
                               j_typs=j_typs,
                               sr_mods=sr_mods,
                               send_lv=send_lv)

    # 配置电容
    def config_c(self, c_pst):
        for num in range(len(c_pst)):
            c_name = 'C' + str(num + 1)
            ele = CapC(parent_ins=self,
                       name_base=c_name,
                       posi=c_pst[num],
                       z=self.parameter['Ccmp_z'])
            self.add_child(c_name, ele)

    @staticmethod
    def config_class(j_typs):
        j_clss, tcsr_clss = [None, None], [None, None]
        for num in range(2):
            if j_typs[num] == '电气':
                j_clss[num] = Joint_2000A_Electric
                tcsr_clss[num] = ZPW2000A_QJ_Normal
            elif j_typs[num] == '机械':
                j_clss[num] = Joint_Mechanical
                tcsr_clss[num] = ZPW2000A_ZN_PTSVA1
            else:
                raise KeyboardInterrupt("绝缘节类型异常：必须为'电气'或'机械'")
        return j_clss, tcsr_clss

    def config_joint_tcsr(self, j_clss, tcsr_clss, j_lens,
                          j_typs, sr_mods, send_lv):
        level = send_lv
        cab_len = self.parameter['cab_len']
        for num in range(2):
            flag = ['左', '右'][num]
            l_section = None if num == 0 else self
            r_section = self if num == 0 else None

            cls = j_clss[num]
            joint_name = flag + '绝缘节'
            ele = cls(parent_ins=self,
                      name_base=joint_name,
                      posi_flag=flag,
                      l_section=l_section,
                      r_section=r_section,
                      j_length=j_lens[num],
                      j_type=j_typs[num])
            self.add_child(joint_name, ele)

            cls = tcsr_clss[num]
            tcsr_name = flag + '调谐单元'
            ele = cls(parent_ins=self,
                      name_base=tcsr_name,
                      posi_flag=flag,
                      cable_length=cab_len,
                      mode=sr_mods[num],
                      level=level)
            self.add_child(tcsr_name, ele)

# 2000A移频脉冲配置
class Section_ZPW2000A_YPMC(Section_ZPW2000A):
    def __init__(self, parent_ins, name_base,
                 m_frq, s_len, j_len, c_num, j_typ, sr_mod, send_lv):
        super().__init__(parent_ins, name_base,
                         m_frq, s_len, j_len, c_num, j_typ, sr_mod, send_lv)
        self.m_type = '2000A_YPMC'

    @staticmethod
    def config_class(j_type):
        j_cls, tcsr_cls = [None, None], [None, None]
        for num in range(2):
            if j_type[num] == '电气':
                raise KeyboardInterrupt('2000A移频脉冲不支持电气绝缘节')
            elif j_type[num] == '机械':
                j_cls[num] = Joint_Mechanical
                tcsr_cls[num] = ZPW2000A_YPMC_Normal
            else:
                raise KeyboardInterrupt("绝缘节类型异常：必须为'电气'或'机械'")
        return j_cls, tcsr_cls


# 2000A白俄配置
class Section_ZPW2000A_Belarus(Section_ZPW2000A):
    def __init__(self, parent_ins, name_base,
                 m_frq, s_len, j_len, c_num, j_typ, sr_mod, send_lv):
        super().__init__(parent_ins, name_base,
                         m_frq, s_len, j_len, c_num, j_typ, sr_mod, send_lv)
        self.m_type = '2000A_Belarus'

    @staticmethod
    def config_class(j_type):
        j_cls, tcsr_cls = [None, None], [None, None]
        for num in range(2):
            if j_type[num] == '电气':
                j_cls[num] = Joint_2000A_Electric_Belarus
                tcsr_cls[num] = ZPW2000A_QJ_Belarus
            elif j_type[num] == '机械':
                raise KeyboardInterrupt('2000A白俄暂不支持机械绝缘节')
            else:
                raise KeyboardInterrupt("绝缘节类型异常：必须为'电气'或'机械'")
        return j_cls, tcsr_cls


# 2000A_BPLN配置
class Section_ZPW2000A_BPLN(Section_ZPW2000A):
    def __init__(self, parent_ins, name_base,
                 m_frq, s_len, j_len, c_num, j_typ, sr_mod, send_lv):
        super().__init__(parent_ins, name_base,
                         m_frq, s_len, j_len, c_num, j_typ, sr_mod, send_lv)
        self.m_type = '2000A_BPLN'

    @staticmethod
    def config_class(j_typs):
        j_clss, tcsr_clss = [None, None], [None, None]
        for num in range(2):
            if j_typs[num] == '电气':
                raise KeyboardInterrupt('2000A_BPLN不支持电气绝缘节')
            elif j_typs[num] == '机械':
                j_clss[num] = Joint_Mechanical
                tcsr_clss[num] = ZPW2000A_ZN_BPLN
            else:
                raise KeyboardInterrupt("绝缘节类型异常：必须为'电气'或'机械'")
        return j_clss, tcsr_clss
