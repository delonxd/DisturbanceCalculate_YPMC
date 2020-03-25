from src.Module.OutsideElement import SVA
from src.Module.TcsrLib import *
from src.Module.BreakPoint import *


# 绝缘节
class Joint(ElePack):
    new_table = {
        '位置标志': 'posi_flag',
        '左侧区段': 'l_section',
        '右侧区段': 'r_section',
        '绝缘节长度': 'j_length',
        '区段类型': 'sec_type'
    }
    prop_table = ElePack.prop_table.copy()
    prop_table.update(new_table)

    def __init__(self, parent_ins, name_base, posi_flag,
                 l_section, r_section, j_type, j_length):
        super().__init__(parent_ins, name_base)
        self.parameter = parent_ins.parameter
        self.posi_flag = posi_flag
        self.init_position(0)
        self.j_type = j_type
        self.l_section = l_section
        self.r_section = r_section
        self.j_length = j_length
        # self.tcsr_cls = ZPW2000A_ZN_PTSVA1
        self.tcsr_cls = None
        self.set_element()

    @property
    def posi_rlt(self):
        posi = self.parent_ins.s_length if self.posi_flag == '右' else 0
        return posi

    @posi_rlt.setter
    def posi_rlt(self, value):
        self._posi_rlt = value

    @property
    def sec_type(self):
        # sec_type = None
        if self.l_section and self.r_section:
            if self.j_type == '电气':
                if not self.l_section.m_type == self.r_section.m_type:
                    raise KeyboardInterrupt(
                        repr(self.l_section) + '和' + repr(self.r_section) + '区段类型不符')
        sec_type = self.parent_ins.m_type
        return sec_type

    def set_element(self):
        pass

    def add_joint_tcsr(self):
        tcsr_name = '相邻调谐单元'
        if not self.l_section:
            tcsr = self.r_section['左调谐单元']
            flag = '右'
        elif not self.r_section:
            tcsr = self.l_section['右调谐单元']
            flag = '左'
        else:
            return

        if isinstance(tcsr, self.tcsr_cls):
            cls = self.tcsr_cls
            ele = cls(parent_ins=self,
                      name_base=tcsr_name,
                      posi_flag=flag,
                      cable_length=tcsr.cable_length,
                      mode=self.change_sr_mode(tcsr.mode),
                      level=tcsr.send_level)
            self.add_child(tcsr_name, ele)

    # 交换发送接收
    @staticmethod
    def change_sr_mode(mode):
        new = None
        if mode == '发送':
            new = '接收'
        elif mode == '接收':
            new = '发送'
        return new


# 机械绝缘节
class Joint_Mechanical(Joint):
    def set_element(self):
        ele = BreakPoint(parent_ins=self,
                         name_base='断点',
                         posi=0)
        self.add_child('断点', ele)
        self.tcsr_cls = ZPW2000A_ZN_PTSVA1
        pass

    def add_joint_tcsr(self):
        pass


# 2000A电气绝缘节
class Joint_2000A_Electric(Joint):
    def set_element(self):
        ele = SVA(parent_ins=self,
                  name_base='SVA',
                  posi=0,
                  z=self.parameter['SVA_z'])
        self.add_child('SVA', ele)
        self.tcsr_cls = ZPW2000A_QJ_Normal


# 2000A电气绝缘节
class Joint_2000A_Electric_Belarus(Joint):
    def set_element(self):
        self.tcsr_cls = ZPW2000A_QJ_Belarus
