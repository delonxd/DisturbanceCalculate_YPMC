from src.TrackCircuitElement.Section import *


# 区段组
class SectionGroup(ElePack):
    new_table = {
        '区段数量': 'sec_num',
        '区段列表': 'section_list',
        '位置列表': 'ele_posi',
        '位置字典': 'posi_dict'
    }
    prop_table = ElePack.prop_table.copy()
    prop_table.update(new_table)

    def __init__(self, name_base, posi, m_num, freq1, m_length, j_length, m_type, c_num,
                 parameter):
        super().__init__(None, name_base)
        self.init_position(posi)
        self.parameter = parameter
        init_list = (m_num, freq1, m_type, m_length, j_length, c_num)
        self.m_num = m_num
        self.section_list = list()
        self.ele_posi = list()

        self.init_element(init_list)
        self.link_section()
        self.refresh()

    def init_element(self, init_list):
        m_num, freq, m_type, m_length, j_length, c_num = init_list
        freq_list = list()
        for num in range(m_num):
            freq_list.append(freq)
            freq = freq.copy()
            freq.change_freq()
        m_type = m_type[:m_num]
        m_length = m_length[:m_num]
        j_length = j_length[:(m_num + 1)]
        c_num = c_num[:m_num]

        j_type = ['电气' if num > 0 else '机械' for num in j_length]
        j_length = [[j_length[num], j_length[num+1]] for num in range(m_num)]
        j_type = [[j_type[num], j_type[num+1]] for num in range(m_num)]
        # sr_type = ['PT', 'PT']

        for num in range(m_num):
            name = '区段' + str(num+1)
            sec_t = None
            if m_type[num] == '2000A':
                sec_t = Section_ZPW2000A(parent_ins=self, name_base=name,
                                         m_freq=freq_list[num], s_length=m_length[num],
                                         j_length=j_length[num], c_num=c_num[num],
                                         j_type=j_type[num], sr_mode='左发')
            elif m_type[num] == '2000A_YPMC':
                sec_t = Section_ZPW2000A_YPMC(parent_ins=self, name_base=name,
                                              m_freq=freq_list[num], s_length=m_length[num],
                                              j_length=j_length[num], c_num=c_num[num],
                                              j_type=j_type[num], sr_mode='左发')
            elif m_type[num] == '2000A_Belarus':
                sec_t = Section_ZPW2000A_Belarus(parent_ins=self, name_base=name,
                                                 m_freq=freq_list[num], s_length=m_length[num],
                                                 j_length=j_length[num], c_num=c_num[num],
                                                 j_type=j_type[num], sr_mode='左发')
            self.add_child(name, sec_t)
            # self.element[name] = sec_t
            self.section_list.append(sec_t)

    @property
    def sec_num(self):
        return len(self.section_list)

    @property
    def posi_dict(self):
        posi_t = 0
        posi_dict = dict()
        for sec in self.section_list:
            posi_dict[sec.name_base] = posi_t
            posi_t = posi_t + sec.s_length
        return posi_dict

    def refresh(self):
        self.set_posi_abs(0)
        # set_ele_name(self, '')
        self.ele_posi = self.get_posi_abs(posi_list=[])

    # 连接相邻区段
    def link_section(self):
        for num in range(self.sec_num - 1):
            sec1 = self.section_list[num]
            sec2 = self.section_list[num+1]
            joint1 = sec1['右绝缘节']
            joint2 = sec2['左绝缘节']
            if not joint1.j_type == joint2.j_type:
                raise KeyboardInterrupt(repr(sec1) + '和' + repr(sec2) + '绝缘节类型不符无法相连')
            elif not joint1.j_length == joint2.j_length:
                raise KeyboardInterrupt(repr(sec1) + '和' + repr(sec2) + '绝缘节长度不符无法相连')
            elif joint1.r_section:
                raise KeyboardInterrupt(repr(sec1) + '右侧已与区段相连')
            elif joint2.l_section:
                raise KeyboardInterrupt(repr(sec2) + '左侧已与区段相连')
            elif joint1.j_type == '电气':
                if not sec1.m_type == sec2.m_type:
                    raise KeyboardInterrupt(repr(sec1) + '和' + repr(sec2) + '主轨类型不符无法相连')
                elif not sec1.m_freq.value == sec2.m_freq.copy().change_freq():
                    raise KeyboardInterrupt(repr(sec1) + '和' + repr(sec2) + '主轨频率不符无法相连')
                else:
                    joint1.r_section = sec2
                    sec2['左绝缘节'] = joint1

        for sec in self.section_list:
            for j_name in ['左绝缘节', '右绝缘节']:
                sec[j_name].add_joint_tcsr()

