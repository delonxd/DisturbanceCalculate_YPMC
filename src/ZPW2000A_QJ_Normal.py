from src.TCSR import *

import src.TrackCircuitCalculator3 as tc

TCSR_2000A = tc.TCSR_2000A

class ZPW2000A_QJ_Normal(TCSR):
    def __init__(self, parent_ins, name_base, posi_flag,
                 cable_length, mode, level):
        super().__init__(parent_ins, name_base, posi_flag)
        self.posi_flag = posi_flag
        self.init_position(0)
        self.flag_ele_list = True
        self.flag_ele_unit = True
        self.mode = mode

        if self.mode == '发送':
            self.add_element('1发送器', TcsrPower(self, '1发送器', TCSR_2000A['z_pwr'], level))
        elif self.mode == '接收':
            self.add_element('1接收器', TcsrReceiver(self, '1接收器', TCSR_2000A['Z_rcv']))
        self.add_element('2防雷', TcsrFL(self, '2防雷',
                                       TCSR_2000A['FL_z1_发送端'],
                                       TCSR_2000A['FL_z2_发送端'],
                                       TCSR_2000A['FL_n_发送端']))
        self.add_element('3Cab', TPortCable(self, '3Cab', cable_length))
        self.add_element('4TAD', TcsrTAD(self, '4TAD',
                                         TCSR_2000A['TAD_z1_发送端_区间'],
                                         TCSR_2000A['TAD_z2_发送端_区间'],
                                         TCSR_2000A['TAD_z3_发送端_区间'],
                                         TCSR_2000A['TAD_n_发送端_区间'],
                                         TCSR_2000A['TAD_c_发送端_区间']))
        self.add_element('5BA', TcsrBA(self, '5BA', TCSR_2000A['PT']))
        self.add_element('6CA', TcsrCA(self, '6CA', TCSR_2000A['CA_z_区间']))

        self.md_list = self.get_md_list([])
        self.config_varb()
