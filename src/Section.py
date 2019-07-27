from src.BasicOutsideModel import CapC
from src.Joint import *

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
        j_length, c_num, sr_mode, j_type, m_length = init_list
        if self.m_type == '2000A':
            offset = j_length[0]
            # 设置电容
            lc = (m_length / c_num) if c_num > 0 else 0
            c_posi = [(num * lc + lc / 2 + offset) for num in range(c_num)]
            for num in range(c_num):
                name = 'C' + str(num + 1)
                self[name] = CapC(parent_ins=self, name_base=name,
                                  posi=c_posi[num], z=self.parameter['Ccmp_z'])
            # 设置绝缘节
            for num in range(2):
                flag = ['左', '右'][num]
                name = flag + '绝缘节'
                l_section = None if num == 0 else self
                r_section = self if num == 0 else None
                self[name] = Joint(parent_ins=self, name_base=name, posi_flag=flag,
                                   l_section=l_section, r_section=r_section,
                                   j_length=j_length[num], j_type=j_type[num])
                joint = self[name]

                name = flag + '调谐单元'
                if joint.j_type == '电气':
                    self[name] = ZPW2000A_QJ_Normal(parent_ins=self, name_base=name,
                                                    posi_flag=flag, cable_length=10,
                                                    mode=sr_mode[num], level=1)
        else:
            raise KeyboardInterrupt(self.m_type + '暂为不支持的主轨类型')
