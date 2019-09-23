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
                 m_type, m_freq, s_length,
                 j_length, c_num, j_type, sr_mode):
        super().__init__(parent_ins, name_base)
        self.parameter = parent_ins.parameter
        self.init_position(0)
        self.m_type = m_type
        self.m_freq = m_freq
        self.s_length = s_length

        # 临时变量
        sr_mode_list = [None, None]
        if sr_mode == '左发':
            sr_mode_list = ['发送', '接收']
        elif sr_mode == '右发':
            sr_mode_list = ['接收', '发送']
        m_length = s_length - (j_length[0] + j_length[1]) / 2
        init_list = (j_length, c_num, sr_mode_list, j_type, m_length)
        self.set_element(init_list)

    @property
    def posi_rlt(self):
        posi = self.parent_ins.posi_dict[self.name_base]
        return posi

    def set_element(self, init_list):
        pass

    # def set_element(self, init_list):
    #     j_length, c_num, sr_mode, j_type, m_length = init_list
    #     if self.m_type == '2000A':
    #         offset = j_length[0]
    #         # 设置电容
    #         lc = (m_length / c_num) if c_num > 0 else 0
    #         c_posi = [(num * lc + lc / 2 + offset) for num in range(c_num)]
    #         for num in range(c_num):
    #             name = 'C' + str(num + 1)
    #             # self[name] = CapC(parent_ins=self, name_base=name,
    #             #                   posi=c_posi[num], z=self.parameter['Ccmp_z'])
    #             ele = CapC(parent_ins=self, name_base=name,
    #                        posi=c_posi[num], z=self.parameter['Ccmp_z'])
    #             self.add_child(name, ele)
    #
    #         name = 'TB_1700_sp'
    #         ele = TB(parent_ins=self, name_base=name,
    #                  posi=18, z=self.parameter['TB'][1700])
    #         self.add_child(name, ele)
    #
    #         # 设置绝缘节
    #         for num in range(2):
    #             flag = ['左', '右'][num]
    #             name = flag + '绝缘节'
    #             l_section = None if num == 0 else self
    #             r_section = self if num == 0 else None
    #             # self[name] = Joint(parent_ins=self, name_base=name, posi_flag=flag,
    #             #                    l_section=l_section, r_section=r_section,
    #             #                    j_length=j_length[num], j_type=j_type[num])
    #             # joint = self[name]
    #             joint = Joint(parent_ins=self, name_base=name, posi_flag=flag,
    #                           l_section=l_section, r_section=r_section,
    #                           j_length=j_length[num], j_type=j_type[num])
    #             self.add_child(name, joint)
    #
    #             name = flag + '调谐单元'
    #             if joint.j_type == '电气':
    #                 # self[name] = ZPW2000A_QJ_Normal(parent_ins=self, name_base=name,
    #                 #                                 posi_flag=flag, cable_length=10,
    #                 #                                 mode=sr_mode[num], level=1)
    #                 ele = ZPW2000A_QJ_Normal(parent_ins=self, name_base=name,
    #                                          posi_flag=flag, cable_length=10,
    #                                          mode=sr_mode[num], level=1)
    #                 self.add_child(name, ele)
    #
    #             elif joint.j_type == '机械':
    #                 # self[name] = ZPW2000A_ZN_PTSVA1(parent_ins=self, name_base=name,
    #                 #                                 posi_flag=flag, cable_length=10,
    #                 #                                 mode=sr_mode[num], level=1)
    #                 ele = ZPW2000A_ZN_PTSVA1(parent_ins=self, name_base=name,
    #                                          posi_flag=flag, cable_length=0.5,
    #                                          mode=sr_mode[num], level=3)
    #                 self.add_child(name, ele)
    #
    #     else:
    #         raise KeyboardInterrupt(self.m_type + '暂为不支持的主轨类型')


# 2000A配置
class Section_ZPW2000A(Section):
    def __init__(self, parent_ins, name_base,
                 m_freq, s_length, j_length, c_num, j_type, sr_mode):
        self.m_type = m_type = '2000A'
        super().__init__(parent_ins, name_base,
                         m_type, m_freq, s_length,
                         j_length, c_num, j_type, sr_mode)

    def set_element(self, init_list):
        j_length, c_num, sr_mode, j_type, m_length = init_list
        offset = j_length[0]
        # 按ZPW-2000A原则设置电容
        lc = (m_length / c_num) if c_num > 0 else 0
        c_posi = [(num * lc + lc / 2 + offset) for num in range(c_num)]
        for num in range(c_num):
            name = 'C' + str(num + 1)
            ele = CapC(parent_ins=self, name_base=name,
                       posi=c_posi[num], z=self.parameter['Ccmp_z'])
            self.add_child(name, ele)

        # 设置绝缘节
        for num in range(2):
            flag = ['左', '右'][num]
            name = flag + '绝缘节'
            l_section = None if num == 0 else self
            r_section = self if num == 0 else None
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

            name = flag + '调谐单元'
            if j_type[num] == '电气':
                ele = ZPW2000A_QJ_Normal(parent_ins=self, name_base=name,
                                         posi_flag=flag, cable_length=10,
                                         mode=sr_mode[num], level=1)
                self.add_child(name, ele)

            elif j_type[num] == '机械':
                # ele = ZPW2000A_ZN_PTSVA1(parent_ins=self, name_base=name,
                #                          posi_flag=flag, cable_length=0.5,
                #                          mode=sr_mode[num], level=3)
                level = self.parameter['level']
                cab_len = self.parameter['cab_len']
                ele = ZPW2000A_YPMC_Normal(parent_ins=self, name_base=name,
                                           posi_flag=flag, cable_length=cab_len,
                                           mode=sr_mode[num], level=level)

                self.add_child(name, ele)

