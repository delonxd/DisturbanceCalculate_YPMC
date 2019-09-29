from src.Module.TCSRBasic import *


# ZPW2000A区间标准配置
class ZPW2000A_QJ_Normal(TCSR):
    def __init__(self, parent_ins, name_base,
                 posi_flag, cable_length, mode, level):
        super().__init__(parent_ins, name_base, posi_flag)
        self.parameter = para = parent_ins.parameter
        self.posi_flag = posi_flag
        self.init_position(0)
        self.flag_ele_list = True
        self.flag_ele_unit = True
        self.mode = mode
        self.send_level = level

        if self.mode == '发送':
            self.add_child('1发送器', TcsrPower(self, '1发送器', para['z_pwr']))
        elif self.mode == '接收':
            self.add_child('1接收器', TcsrReceiver(self, '1接收器', para['Z_rcv']))
        self.add_child('2防雷', TcsrFL(self, '2防雷',
                                     para['FL_z1_发送端'],
                                     para['FL_z2_发送端'],
                                     para['FL_n_发送端']))
        self.add_child('3Cab', TPortCable(self, '3Cab', cable_length,
                                          para['Cable_R'],
                                          para['Cable_L'],
                                          para['Cable_C']))
        self.add_child('4TAD', TcsrTAD(self, '4TAD',
                                       para['TAD_z1_发送端_区间'],
                                       para['TAD_z2_发送端_区间'],
                                       para['TAD_z3_发送端_区间'],
                                       para['TAD_n_发送端_区间'],
                                       para['TAD_c_发送端_区间']))
        self.add_child('5BA', TcsrBA(self, '5BA', para['PT']))
        self.add_child('6CA', TcsrCA(self, '6CA', para['CA_z_区间']))

        self.md_list = self.get_md_list([])
        self.config_varb()


# ZPW2000A站内PT+SVA'配置
class ZPW2000A_ZN_PTSVA1(TCSR):
    def __init__(self, parent_ins, name_base,
                 posi_flag, cable_length, mode, level):
        super().__init__(parent_ins, name_base, posi_flag)
        self.parameter = para = parent_ins.parameter
        self.posi_flag = posi_flag
        self.init_position(0)
        self.flag_ele_list = True
        self.flag_ele_unit = True
        self.mode = mode
        self.send_level = level

        if self.mode == '发送':
            self.add_child('1发送器', TcsrPower(self, '1发送器', para['z_pwr']))
        elif self.mode == '接收':
            self.add_child('1接收器', TcsrReceiver(self, '1接收器', para['Z_rcv']))
        self.add_child('2防雷', TcsrFL(self, '2防雷',
                                     para['FL_z1_发送端'],
                                     para['FL_z2_发送端'],
                                     para['FL_n_发送端']))
        self.add_child('3CabComp', TcsrCableComp(self, '3CabComp'))
        # self.add_child('3Cab', TPortCable(self, '3Cab', cable_length,
        #                                   para['Cable_R'],
        #                                   para['Cable_L'],
        #                                   para['Cable_C']))

        self.add_child('4TAD', TcsrTAD(self, '4TAD',
                                       para['TAD_z1_发送端_区间'],
                                       para['TAD_z2_发送端_区间'],
                                       para['TAD_z3_发送端_区间'],
                                       para['TAD_n_发送端_区间'],
                                       para['TAD_c_发送端_区间']))
        self.add_child('5BA', TcsrBA(self, '5BA', para['PT']))
        self.add_child('6SVA1', TPortZParallel(self, '6SVA1', para['SVA1_z']))
        self.add_child('7CA', TcsrCA(self, '7CA', para['CA_z_区间']))

        self.md_list = self.get_md_list([])
        self.config_varb()


# ZPW2000A区间白俄配置
class ZPW2000A_QJ_Belarus(TCSR):
    def __init__(self, parent_ins, name_base,
                 posi_flag, cable_length, mode, level):
        super().__init__(parent_ins, name_base, posi_flag)
        self.parameter = para = parent_ins.parameter
        self.posi_flag = posi_flag
        self.init_position(0)
        self.flag_ele_list = True
        self.flag_ele_unit = True
        self.mode = mode
        self.send_level = level

        if self.mode == '发送':
            self.add_child('1发送器', TcsrPower(self, '1发送器', para['z_pwr']))
        elif self.mode == '接收':
            self.add_child('1接收器', TcsrReceiver(self, '1接收器', para['Z_rcv']))
        self.add_child('1_隔离盒', TcsrIsolationBelarus(self, '1_隔离盒',
                                              para['Z_iso1_Belarus'],
                                              para['Z_iso2_Belarus']))
        self.add_child('2防雷', TcsrFL(self, '2防雷',
                                     para['FL_z1_发送端'],
                                     para['FL_z2_发送端'],
                                     para['FL_n_发送端']))
        self.add_child('3Cab', TPortCable(self, '3Cab', cable_length,
                                          para['Cable_R'],
                                          para['Cable_L'],
                                          para['Cable_C']))
        self.add_child('4TAD', TcsrTADBelarus(self, '4TAD',
                                              para['TAD_z1_Belarus'],
                                              para['TAD_z2_Belarus'],
                                              para['TAD_n_Belarus']))
        self.add_child('5BA', TcsrBA(self, '5BA', para['PT']))
        self.add_child('6CA', TcsrCA(self, '6CA', para['CA_z_区间']))

        self.md_list = self.get_md_list([])
        self.config_varb()


# ZPW2000A站内移频脉冲标准配置
class ZPW2000A_YPMC_Normal(TCSR):
    def __init__(self, parent_ins, name_base,
                 posi_flag, cable_length, mode, level):
        super().__init__(parent_ins, name_base, posi_flag)
        self.parameter = para = parent_ins.parameter
        self.posi_flag = posi_flag
        self.init_position(0)
        self.flag_ele_list = True
        self.flag_ele_unit = True
        self.mode = mode
        self.send_level = level

        if self.mode == '发送':
            self.add_child('1发送器', TcsrPowerYPMC(self, '1发送器',
                                                 para['z_pwr_yp'],
                                                 para['z_pwr_ypmc_iso']))
        elif self.mode == '接收':
            self.add_child('1接收器', TcsrReceiverYPMC(self, '1接收器',
                                                    para['z_rcv_ypmc_iso2'],
                                                    para['z_rcv_ypmc_iso'],
                                                    para['z_rcv_ypmc']))
        # 注意拓扑结构
        self.add_child('2防雷', TcsrFLYPMC(self, '2防雷',
                                         para['z1_FL_ypmc'],
                                         para['z2_FL_ypmc'],
                                         para['n_FL_ypmc']))
        self.add_child('3Cab', TPortCable(self, '3Cab', cable_length,
                                          para['Cable_R'],
                                          para['Cable_L'],
                                          para['Cable_C']))
        self.add_child('4扼流', TcsrELYPMC(self, '4扼流',
                                         para['z1_EL_ypmc'],
                                         para['z2_EL_ypmc'],
                                         para['n_EL_ypmc']))
        # self.add_child('5BA', TcsrBA(self, '5BA', para['PT']))
        self.add_child('6CA', TcsrCA(self, '6CA', para['CA_z_区间']))

        self.md_list = self.get_md_list([])
        self.config_varb()