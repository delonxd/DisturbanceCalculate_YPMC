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

    def __init__(self, name_base, posi, m_num,
                 m_frqs, m_lens, j_lens, m_typs, c_nums, sr_mods, send_lvs,
                 parameter):
        super().__init__(None, name_base)
        self.init_position(posi)
        self.parameter = parameter
        init_list = m_num, m_frqs, m_lens, j_lens, \
                    m_typs, c_nums, sr_mods, send_lvs
        self.m_num = m_num
        self.section_list = list()
        self.ele_posi = list()

        self.init_element(init_list)
        self.link_section()
        self.refresh()

    def init_element(self, init_list):
        m_num, m_frqs, m_lens, j_lens, \
        m_typs, c_nums, sr_mods, send_lvs = init_list
        m_frqs = m_frqs[:m_num]
        m_lens = m_lens[:m_num]
        j_lens = j_lens[:(m_num + 1)]
        m_typs = m_typs[:m_num]
        c_nums = c_nums[:m_num]
        sr_mods = sr_mods[:m_num]
        send_lvs = send_lvs[:m_num]

        j_typs = ['电气' if num > 0 else '机械' for num in j_lens]
        j_lens = [[j_lens[num], j_lens[num+1]] for num in range(m_num)]
        j_typs = [[j_typs[num], j_typs[num+1]] for num in range(m_num)]

        for num in range(m_num):
            # sec_class = Section_ZPW2000A
            # cmd = 'sec_class = Section_ZPW' + m_typs[num]
            # exec(cmd)
            sec_class = eval('Section_ZPW' + m_typs[num])
            sec_name = '区段' + str(num + 1)
            sec_t = sec_class(parent_ins=self,
                              name_base=sec_name,
                              m_frq=m_frqs[num],
                              s_len=m_lens[num],
                              j_len=j_lens[num],
                              c_num=c_nums[num],
                              j_typ=j_typs[num],
                              sr_mod=sr_mods[num],
                              send_lv=send_lvs[num])
            self.add_child(sec_name, sec_t)
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

