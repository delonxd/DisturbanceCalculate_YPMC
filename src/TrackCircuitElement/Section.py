from src.Module.OutsideElement import CapC
from src.Module.OutsideElement import TB
from src.TrackCircuitElement.Joint import *


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
                 m_freq, s_length, j_length, c_num, j_type, sr_mode):
        super().__init__(parent_ins, name_base)
        self.parameter = parent_ins.parameter
        self.init_position(0)
        self.m_type = ''
        self.m_freq = m_freq
        self.s_length = s_length

        # 临时变量
        sr_mode_t = sr_mode
        if sr_mode_t == '左发':
            sr_mode = ['发送', '接收']
        elif sr_mode_t == '右发':
            sr_mode = ['接收', '发送']
        m_length = s_length - (j_length[0] + j_length[1]) / 2
        init_list = (j_length, c_num, sr_mode, j_type, m_length)
        self.set_element(init_list)

    @property
    def posi_rlt(self):
        posi = self.parent_ins.posi_dict[self.name_base]
        return posi

    def set_element(self, init_list):
        pass

    def get_joint_info(self, num):
        flag = ['左', '右'][num]
        l_section = None if num == 0 else self
        r_section = self if num == 0 else None
        return flag, l_section, r_section


# 2000A配置
class Section_ZPW2000A(Section):
    def __init__(self, parent_ins, name_base,
                 m_freq, s_length, j_length, c_num, j_type, sr_mode):
        super().__init__(parent_ins, name_base,
                         m_freq, s_length, j_length, c_num, j_type, sr_mode)
        self.m_type = '2000A'

    def set_element(self, init_list):
        j_length, c_num, sr_mode, j_type, m_length = init_list
        offset = j_length[0]
        # 按ZPW-2000A原则设置电容
        lc = (m_length / c_num) if c_num > 0 else 0
        c_posi = [(num * lc + lc / 2 + offset) for num in range(c_num)]
        self.config_c(c_posi)
        self.config_joint(j_type, j_length)
        self.config_tcsr(j_type, sr_mode)

    # 配置电容
    def config_c(self, c_posi):
        for num in range(len(c_posi)):
            name = 'C' + str(num + 1)
            ele = CapC(parent_ins=self, name_base=name,
                       posi=c_posi[num], z=self.parameter['Ccmp_z'])
            self.add_child(name, ele)

    # 配置绝缘节
    def config_joint(self, j_type, j_length):
        # 设置绝缘节
        for num in range(2):
            flag, l_section, r_section = self.get_joint_info(num)
            name = flag + '绝缘节'
            if j_type[num] == '电气':
                joint = Joint_2000A_Electric(parent_ins=self, name_base=name, posi_flag=flag,
                                             l_section=l_section, r_section=r_section,
                                             j_length=j_length[num], j_type=j_type[num])
                self.add_child(name, joint)
            elif j_type[num] == '机械':
                joint = Joint_Mechanical(parent_ins=self, name_base=name, posi_flag=flag,
                                         l_section=l_section, r_section=r_section,
                                         j_length=j_length[num], j_type=j_type[num])
                self.add_child(name, joint)

    # 配置调谐匹配单元
    def config_tcsr(self, j_type, sr_mode):
        for num in range(2):
            flag, _, _ = self.get_joint_info(num)
            name = flag + '调谐单元'
            level = self.parameter['level']
            cab_len = self.parameter['cab_len']
            if j_type[num] == '电气':
                ele = ZPW2000A_QJ_Normal(parent_ins=self, name_base=name,
                                         posi_flag=flag, cable_length=cab_len,
                                         mode=sr_mode[num], level=level)
                self.add_child(name, ele)
            elif j_type[num] == '机械':
                ele = ZPW2000A_ZN_PTSVA1(parent_ins=self, name_base=name,
                                         posi_flag=flag, cable_length=cab_len,
                                         mode=sr_mode[num], level=level)
                self.add_child(name, ele)


# 2000A移频脉冲配置
class Section_ZPW2000A_YPMC(Section_ZPW2000A):
    def __init__(self, parent_ins, name_base,
                 m_freq, s_length, j_length, c_num, j_type, sr_mode):
        super().__init__(parent_ins, name_base,
                         m_freq, s_length, j_length, c_num, j_type, sr_mode)
        self.m_type = '2000A_YPMC'

    # 配置绝缘节
    def config_joint(self, j_type, j_length):
        for num in range(2):
            flag, l_section, r_section = self.get_joint_info(num)
            name = flag + '绝缘节'
            if j_type[num] == '电气':
                raise KeyboardInterrupt('2000A移频脉冲不支持电气绝缘节')
            elif j_type[num] == '机械':
                joint = Joint_Mechanical(parent_ins=self, name_base=name, posi_flag=flag,
                                         l_section=l_section, r_section=r_section,
                                         j_length=j_length[num], j_type=j_type[num])
                self.add_child(name, joint)

    def config_tcsr(self, j_type, sr_mode):
        for num in range(2):
            flag, _, _ = self.get_joint_info(num)
            name = flag + '调谐单元'
            if j_type[num] == '电气':
                raise KeyboardInterrupt('2000A移频脉冲不支持电气绝缘节')
            elif j_type[num] == '机械':
                level = self.parameter['level']
                cab_len = self.parameter['cab_len']
                ele = ZPW2000A_YPMC_Normal(parent_ins=self, name_base=name,
                                           posi_flag=flag, cable_length=cab_len,
                                           mode=sr_mode[num], level=level)
                self.add_child(name, ele)
