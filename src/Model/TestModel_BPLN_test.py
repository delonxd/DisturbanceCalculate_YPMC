from src.TrackCircuitElement.SectionGroup import *
from src.TrackCircuitElement.Train import *
from src.TrackCircuitElement.Line import *
from src.TrackCircuitElement.LineGroup import *
from src.Model.MainModel import *
from src.Model.ModelParameter import *
from src.FrequencyType import Freq
from src.Method import *

import pandas as pd
import time
import itertools


class TestModel:
    def __init__(self, turnout_list, parameter):
        self.parameter = para = parameter
        self.train = Train(name_base='列车1', posi=0, parameter=parameter)

        # 轨道电路初始化
        send_level = para['send_level']
        m_lens = [para['length']]
        m_frqs = generate_frqs(Freq(para['freq_主']), 1)
        # c_nums = get_c_nums(m_frqs, m_lens)
        c_nums = [para['cmp_num']]
        m_typ = para['m_mode']
        sg3 = SectionGroup(name_base='地面', posi=0, m_num=1,
                           m_frqs=m_frqs,
                           m_lens=m_lens,
                           j_lens=[0]*4,
                           m_typs=[m_typ]*3,
                           c_nums=c_nums,
                           sr_mods=[para['sr_mod_主']]*3,
                           send_lvs=[send_level]*3,
                           parameter=parameter)

        flg = para['pwr_v_flg']
        if para['sr_mod_主'] == '左发':
            sg3['区段1']['左调谐单元'].set_power_voltage(flg)
        elif para['sr_mod_主'] == '右发':
            sg3['区段1']['右调谐单元'].set_power_voltage(flg)
        # sg3['区段1']['左调谐单元'].set_power_voltage()

        self.section_group3 = sg3

        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)

        self.lg = LineGroup(l3, name_base='线路组')
        self.lg.refresh()

    # def add_train(self):
    #     l3 = Line(name_base='线路3', sec_group=self.section_group3,
    #               parameter=self.parameter, train=self.train)
    #     self.l3 = l3
    #
    #     self.lg = LineGroup(l3, name_base='线路组')
    #     self.lg.refresh()

    def add_train(self):
        l3 = Line(name_base='线路3', sec_group=self.section_group3,
                  parameter=self.parameter, train=self.train)
        self.l3 = l3

        self.lg = LineGroup(self.l3, name_base='线路组')
        self.lg.refresh()


def get_output(lg):
    output = 13 * [0]
    output[0] = lg['线路3']['地面']['区段1']['左调谐单元']['1发送器']['2内阻']['U2'].value_c
    output[1] = lg['线路3']['地面']['区段1']['左调谐单元']['1发送器']['3隔离元件']['U2'].value_c
    output[2] = lg['线路3']['地面']['区段1']['左调谐单元']['1发送器']['3隔离元件']['I2'].value_c
    output[3] = lg['线路3']['地面']['区段1']['左调谐单元']['2防雷']['1开路阻抗']['U1'].value_c
    output[4] = lg['线路3']['地面']['区段1']['左调谐单元']['2防雷']['3变压器']['U2'].value_c
    output[5] = lg['线路3']['地面']['区段1']['左调谐单元']['3Cab']['U2'].value_c
    output[6] = lg['线路3']['地面']['区段1']['左调谐单元']['6CA']['U2'].value_c
    output[7] = lg['线路3']['地面']['区段1']['右调谐单元']['6CA']['U2'].value_c
    output[8] = lg['线路3']['地面']['区段1']['右调谐单元']['3Cab']['U2'].value_c
    output[9] = lg['线路3']['地面']['区段1']['右调谐单元']['2防雷']['3变压器']['U2'].value_c
    output[10] = lg['线路3']['地面']['区段1']['右调谐单元']['2防雷']['1开路阻抗']['U1'].value_c
    output[11] = lg['线路3']['地面']['区段1']['右调谐单元']['1接收器']['1隔离元件']['U2'].value_c
    output[12] = lg['线路3']['地面']['区段1']['右调谐单元']['1接收器']['0接收器']['U'].value_c
    return output


if __name__ == '__main__':
    df_input = pd.read_excel('../Input/BPLN参数输入1.xlsm')
    # aaa = list(df_input['min'])
    # print(aaa)

    localtime = time.localtime()
    timestamp = time.strftime("%Y%m%d%H%M%S", localtime)
    print(time.strftime("%Y-%m-%d %H:%M:%S", localtime))

    para = ModelParameter()

    # 电容
    c_value = 25e-6
    para['Ccmp_z'].rlc_s = {
        1700: [10e-3, None, c_value],
        2000: [10e-3, None, c_value],
        2300: [10e-3, None, c_value],
        2600: [10e-3, None, c_value]}

    # 钢轨阻抗
    trk_2000A_21 = ImpedanceMultiFreq()
    trk_2000A_21.rlc_s = {
        1700: [1.177, 1.314e-3, None],
        # 1700: [1.3, 1.314e-3, None],
        2000: [1.306, 1.304e-3, None],
        2300: [1.435, 1.297e-3, None],
        2600: [1.558, 1.291e-3, None]}


    para['Trk_z'].rlc_s = trk_2000A_21.rlc_s

    # # 钢轨阻抗
    # trk_2000A_21 = ImpedanceMultiFreq()
    # trk_2000A_21.rlc_s = {
    #     1700: [1.38, 1.36e-3, None],
    #     2000: [1.53, 1.35e-3, None],
    #     2300: [1.68, 1.35e-3, None],
    #     2600: [1.79, 1.34e-3, None]}
    #
    # para['Trk_z'].rlc_s = trk_2000A_21.rlc_s

    para['TAD_n_发送端_站内'] = {
        1700: 13.5,
        2000: 13.5,
        2300: 12,
        2600: 12}

    para['freq_主'] = 2600
    para['freq_被'] = 2300
    para['sr_mod_主'] = '左发'
    para['sr_mod_被'] = '右发'

    para['send_level'] = 9

    freq = para['freq_主']
    para['freq'] = Freq(freq)

    head_list = ['变压器类型',
                 '区段长度min(m)', '区段长度max(m)',
                 '电容数量',
                 '区段频率(Hz)', '电缆长度(km)',
                 '功出电平级',
                 '钢轨电阻(Ω/km)', '钢轨电感(H/km)',
                 '道床电阻最大(Ω·km)', '道床电阻最小(Ω·km)',
                 '电缆电阻最大(Ω/km)', '电缆电阻最小(Ω/km)',
                 '分路电阻(Ω)', '分路间隔(m)',
                 '调整接收轨出min(V)', '调整接收轨出max(V)',
                 '调整接收轨入min(V)', '调整接收轨入max(V)',
                 '调整接收轨面min(V)', '调整接收轨面max(V)',
                 # '调整区段轨面min(V)', '调整区段轨面max(V)',
                 '调整发送轨面min(V)', '调整发送轨面max(V)',
                 '调整功出电压min(V)', '调整功出电压max(V)',
                 '调整功出电流min(I)', '调整功出电流max(I)',

                 # '机车信号感应系数',
                 '机车电流最小值(I)',
                 # '机车信号电压最小值(V)',
                 # '轨入残压最大值(V)',
                 '功出电流最大值(I)',
                 '轨出残压最大值(V)',
                 '电缆电流最大值(I)']

    turnout_list = []

    excel_data = []
    excel_i_trk = []
    excel_i_sht = []
    excel_v_train = []
    excel_v_residual = []
    excel_v_trk = []

    i_trk_scale = {
        1700: 310-47,
        2000: 275-41,
        2300: 255-38,
        2600: 235-35}

    v_coil_scale = 115

    # len_min_list = list(range(51, 1152, 50))
    # len_min_list[0] = 50
    # len_max_list = list(range(100, 1201, 50))
    #

    # c_num_list = []
    # for ii in len_max_list:
    #     if ii > 300:
    #         xx = int((ii + 50) / 100)
    #         c_num_list.append(xx)
    #     else:
    #         c_num_list.append(0)
    #
    # len_min_list = list(df_input['min'])
    # len_max_list = list(df_input['max'])
    # c_num_list = list(df_input['num'])
    #
    # zip_list = zip(len_min_list, len_max_list, c_num_list)

    # freq_list = [1700, 2000, 2300, 2600]
    # for length_t in [1000]:
    for frq_zhu in [1700]:
        # for direct in ['左发']:
        for cab_len in [3]:
            # frq_zhu = 2600
            direct = '右发'
            frq_chuan = None

            len_min_list = list(df_input['min'])
            len_max_list = list(df_input['max'])
            c_num_list = list(df_input['num'])

            send_lvl_list = list(df_input[frq_zhu])

            zip_list = zip(len_min_list, len_max_list, c_num_list)
            # length_list = [200, 300, 300, 300, 400, 500, 600, 700, 800]
            # c_num_list = [0, 0, 3, 4, 4, 5, 6, 7, 8]

            for len_min, len_max, cmp_num in zip_list:
                send_lvl = 7
                # length = length_t = 500
                # for offset in range(1400, 650, -50):
                # for offset in range((2*length), -50, -50):
                # for transfomer_mode in ["PT+SVA'", 'BPLN']:
                for transfomer_mode in ['BPLN']:

                    para['send_level'] = send_lvl

                    para['m_mode'] = '2000A'
                    if transfomer_mode == 'BPLN':
                        para['m_mode'] = '2000A_BPLN'

                    print(para['m_mode'])

                    # offset = length
                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    para['freq_主'] = frq_zhu
                    para['freq_被'] = frq_chuan
                    freq = para['freq_主']
                    para['freq'] = Freq(freq)

                    para['sr_mod_主'] = direct
                    para['sr_mod_被'] = '右发'

                    # 数据表0
                    data = dict()
                    for key in head_list:
                        data[key] = None

                    data['变压器类型'] = transfomer_mode
                    # data['区段长度(m)'] = para['length'] = length
                    data['区段长度min(m)'] = len_min
                    data['区段长度max(m)'] = len_max

                    data['电容数量'] = para['cmp_num'] = cmp_num
                    data['钢轨电阻(Ω/km)'] = round(para['Trk_z'].rlc_s[freq][0], 10)
                    data['钢轨电感(H/km)'] = round(para['Trk_z'].rlc_s[freq][1], 10)
                    data['电缆长度(km)'] = para['cab_len'] = cab_len
                    data['区段频率(Hz)'] = freq
                    data['分路电阻(Ω)'] = para['Rsht_z'] = r_sht = 0.15
                    data['道床电阻最大(Ω·km)'] = 10000
                    data['道床电阻最小(Ω·km)'] = 2
                    data['电缆电阻最大(Ω/km)'] = 45
                    data['电缆电阻最小(Ω/km)'] = 43
                    data['最小机车信号位置(m)'] = '-'
                    data['功出电平级'] = para['send_level']
                    data['发送器位置'] = para['sr_mod_主']

                    # data['主串频率(Hz)'] = freq
                    # data['被串频率(Hz)'] = para['freq_被']
                    # data['主串电平级'] = para['send_level']
                    # data['主串发送器位置'] = para['sr_mod_主']
                    # data['被串发送器位置'] = para['sr_mod_被']

                    data['分路间隔(m)'] = interval = 1
                    # posi_list = np.arange(0, (length + 0), interval)

                    i_trk_scale_t = i_trk_scale[frq_zhu]
                    data['机车信号感应系数'] = str(v_coil_scale) + '/' + str(i_trk_scale_t)
                    inductance_coff = v_coil_scale / i_trk_scale_t


                    ############################################################################

                    # 调整计算最大
                    para['Cable_R'].value = data['电缆电阻最小(Ω/km)']
                    para['Rd'].value = data['道床电阻最大(Ω·km)']
                    para['Rsht_z'] = data['分路电阻(Ω)']
                    para['pwr_v_flg'] = '最大'
                    para['length'] = data['区段长度min(m)']

                    md = TestModel(turnout_list=turnout_list, parameter=para)
                    m1 = MainModel(md.lg, md=md)

                    drc_tmp = para['sr_mod_主']
                    string_t = None
                    if drc_tmp == '左发':
                        string_t = '右调谐单元'
                    elif drc_tmp == '右发':
                        string_t = '左调谐单元'

                    data1 = md.lg['线路3']['地面']['区段1'][string_t]['1接收器']['U'].value_c
                    data['调整接收轨入max(V)'] = round(data1, 3)

                    data1 = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['U2'].value_c
                    print(data1)
                    data['调整功出电压max(V)'] = round(data1, 3)

                    data1 = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['I2'].value_c
                    data['调整功出电流max(I)'] = round(data1, 3)


                    ############################################################################

                    # 调整计算最小
                    para['Cable_R'].value = data['电缆电阻最大(Ω/km)']
                    # para['Cable_C'].value = 26e-9
                    para['Rd'].value = data['道床电阻最小(Ω·km)']
                    para['Rsht_z'] = data['分路电阻(Ω)']
                    para['pwr_v_flg'] = '最小'
                    para['length'] = data['区段长度max(m)']

                    md = TestModel(turnout_list=turnout_list, parameter=para)
                    m1 = MainModel(md.lg, md=md)

                    drc_tmp = para['sr_mod_主']
                    string_t = None
                    if drc_tmp == '左发':
                        string_t = '右调谐单元'
                    elif drc_tmp == '右发':
                        string_t = '左调谐单元'

                    data1 = md.lg['线路3']['地面']['区段1'][string_t]['1接收器']['U'].value_c
                    data['调整接收轨入min(V)'] = round(data1, 3)

                    data1 = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['U2'].value_c
                    data['调整功出电压min(V)'] = round(data1, 3)

                    data1 = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['I2'].value_c
                    data['调整功出电流min(I)'] = round(data1, 3)


                    ############################################################################

                    # 最大轨面电压计算
                    v_trk_list = list()

                    para['Cable_R'].value = data['电缆电阻最小(Ω/km)']
                    para['Rd'].value = data['道床电阻最大(Ω·km)']
                    para['Rsht_z'] = 10000
                    para['pwr_v_flg'] = '最大'
                    para['length'] = data['区段长度min(m)']

                    posi_list = np.arange(0, (para['length'] + 0), interval)

                    for posi_tr in posi_list:
                        md = TestModel(turnout_list=turnout_list, parameter=para)
                        md.add_train()
                        md.train.posi_rlt = posi_tr
                        md.train.set_posi_abs(0)
                        m1 = MainModel(md.lg, md=md)

                        v_trk = md.lg['线路3']['列车1']['分路电阻1']['U'].value_c
                        v_trk_list.append(v_trk)

                    data['调整发送轨面max(V)'] = round(v_trk_list[-1], 3)
                    data['调整接收轨面max(V)'] = round(v_trk_list[0], 3)

                    data['调整区段轨面max(V)'] = round(max(v_trk_list), 3)


                    ############################################################################

                    # 最小轨面电压计算
                    v_trk_list = list()

                    para['Cable_R'].value = data['电缆电阻最大(Ω/km)']
                    para['Rd'].value = data['道床电阻最小(Ω·km)']
                    para['Rsht_z'] = 10000
                    para['pwr_v_flg'] = '最小'
                    para['length'] = data['区段长度max(m)']

                    posi_list = np.arange(0, (para['length'] + 0), interval)

                    for posi_tr in posi_list:
                        md = TestModel(turnout_list=turnout_list, parameter=para)
                        md.add_train()
                        md.train.posi_rlt = posi_tr
                        md.train.set_posi_abs(0)
                        m1 = MainModel(md.lg, md=md)

                        v_trk = md.lg['线路3']['列车1']['分路电阻1']['U'].value_c
                        v_trk_list.append(v_trk)


                    data['调整发送轨面min(V)'] = round(v_trk_list[-1], 3)
                    data['调整接收轨面min(V)'] = round(v_trk_list[0], 3)
                    data['调整区段轨面min(V)'] = round(min(v_trk_list), 3)


                    ############################################################################

                    # 计算轨入电压
                    data['调整接收轨出min(V)'] = round(0.24, 3)
                    data['调整接收轨出max(V)'] = round((data['调整接收轨入max(V)'] / data['调整接收轨入min(V)'] * 0.240), 3)

                    ############################################################################

                    # 最大分路残压计算
                    v_residual_list = list()

                    para['Cable_R'].value = data['电缆电阻最小(Ω/km)']
                    para['Rd'].value = data['道床电阻最大(Ω·km)']
                    para['Rsht_z'] = data['分路电阻(Ω)']
                    para['pwr_v_flg'] = '最大'
                    para['length'] = data['区段长度min(m)']

                    posi_list = np.arange(0, (para['length'] + 0), interval)

                    for posi_tr in posi_list:
                        md = TestModel(turnout_list=turnout_list, parameter=para)
                        md.add_train()
                        md.train.posi_rlt = posi_tr
                        md.train.set_posi_abs(0)
                        m1 = MainModel(md.lg, md=md)

                        v_residual = md.lg['线路3']['地面']['区段1']['左调谐单元']['1接收器']['U'].value_c
                        v_residual_list.append(v_residual)

                    data['轨入残压最大值(V)'] = round(max(v_residual_list), 3)


                    data['轨出残压最大值(V)'] = round(0.24 / data['调整接收轨入min(V)'] * data['轨入残压最大值(V)'], 3)


                    ############################################################################

                    # 最小机车信号计算
                    i_trk_list = list()
                    i_sht_list = list()
                    v_train_list = list()

                    para['Cable_R'].value = data['电缆电阻最大(Ω/km)']
                    para['Rd'].value = data['道床电阻最小(Ω·km)']
                    para['Rsht_z'] = data['分路电阻(Ω)']
                    para['pwr_v_flg'] = '最小'
                    para['length'] = data['区段长度max(m)']

                    posi_list = np.arange(0, (para['length'] + 0), interval)

                    for posi_tr in posi_list:
                        md = TestModel(turnout_list=turnout_list, parameter=para)
                        md.add_train()
                        md.train.posi_rlt = posi_tr
                        md.train.set_posi_abs(0)
                        m1 = MainModel(md.lg, md=md)

                        i_sht = md.lg['线路3']['列车1']['分路电阻1']['I'].value_c
                        if m1['线路3'].node_dict[posi_tr].r_track is not None:
                            i_trk = m1['线路3'].node_dict[posi_tr].r_track['I1'].value_c
                        else:
                            print('###')
                            i_trk = 0.0

                        i_trk_list.append(i_trk)
                        i_sht_list.append(i_sht)
                        v_train_list.append(i_trk*inductance_coff)

                    data['机车电流最小值(I)'] = round(min(i_trk_list), 3)
                    data['机车信号电压最小值(V)'] = round(min(v_train_list), 3)


                    ############################################################################

                    # 最大功出电流计算
                    i_pwr_list = list()
                    i_cab_list = list()

                    para['Cable_R'].value = data['电缆电阻最小(Ω/km)']
                    para['Rd'].value = data['道床电阻最小(Ω·km)']
                    para['Rsht_z'] = 0.01
                    para['pwr_v_flg'] = '最大'
                    para['length'] = data['区段长度min(m)']

                    posi_list = np.arange(0, (para['length'] + 0), interval)

                    for posi_tr in posi_list:
                        md = TestModel(turnout_list=turnout_list, parameter=para)
                        md.add_train()
                        md.train.posi_rlt = posi_tr
                        md.train.set_posi_abs(0)
                        m1 = MainModel(md.lg, md=md)

                        i_pwr = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['I2'].value_c
                        i_cab = md.lg['线路3']['地面']['区段1']['右调谐单元']['3Cab']['I1'].value_c

                        i_pwr_list.append(i_pwr)
                        i_cab_list.append(i_cab)

                    data['功出电流最大值(I)'] = round(max(i_pwr_list), 3)
                    data['电缆电流最大值(I)'] = round(max(i_cab_list), 3)


                    ############################################################################

                    print(data.keys())
                    print(data.values())
                    # print(i_sht_list)

                    data_row = [data[key] for key in head_list]
                    excel_data.append(data_row)
                    excel_i_trk.append(i_trk_list)
                    excel_i_sht.append(i_sht_list)
                    excel_v_train.append(v_train_list)
                    excel_v_residual.append(v_residual_list)
                    excel_v_trk.append(v_trk_list)



    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    df_i_trk = pd.DataFrame(excel_i_trk)
    df_i_sht = pd.DataFrame(excel_i_sht)
    df_v_train = pd.DataFrame(excel_v_train)
    df_v_residual = pd.DataFrame(excel_v_residual)
    df_v_trk = pd.DataFrame(excel_v_trk)

    df_data = pd.DataFrame(excel_data, columns=head_list)

    # 保存到本地excel
    filename = '../Output/站内断轨2000A' + timestamp + '.xlsx'
    with pd.ExcelWriter(filename) as writer:
        df_data.to_excel(writer, sheet_name="参数设置", index=False)
        df_i_trk.to_excel(writer, sheet_name="最小钢轨电流", index=False)
        df_i_sht.to_excel(writer, sheet_name="最小分路电流", index=False)
        df_v_train.to_excel(writer, sheet_name="最小机车电压", index=False)
        df_v_residual.to_excel(writer, sheet_name="最大分路残压", index=False)
        df_v_trk.to_excel(writer, sheet_name="最小轨面电压", index=False)
        pass