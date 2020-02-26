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
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train2 = Train(name_base='列车2', posi=0, parameter=parameter)

        # 轨道电路初始化
        send_level = para['send_level']
        m_lens = [para['length']]*3
        m_frqs = generate_frqs(Freq(para['freq_主']), 3)
        # c_nums = get_c_nums(m_frqs, m_lens)
        c_nums = [7]


        sg3 = SectionGroup(name_base='地面', posi=para['offset'], m_num=1,
                           m_frqs=m_frqs,
                           m_lens=m_lens,
                           j_lens=[0]*4,
                           m_typs=['2000A']*3,
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

        m_lens = [para['length']]*3
        m_frqs = generate_frqs(Freq(para['freq_被']), 3)
        # c_nums = get_c_nums(m_frqs, m_lens)
        c_nums = [7]
        sg4 = SectionGroup(name_base='地面', posi=0, m_num=1,
                           m_frqs=m_frqs,
                           m_lens=m_lens,
                           j_lens=[0]*4,
                           m_typs=['2000A']*3,
                           c_nums=c_nums,
                           sr_mods=[para['sr_mod_被']]*3,
                           send_lvs=[send_level]*3,
                           parameter=parameter)

        if para['adj_flag_zhu'] > 0:
            str_temp = 'C' + str(para['adj_flag_zhu'])
            sg3['区段1'].element.pop(str_temp)

        if para['adj_flag_chuan'] > 0:
            str_temp = 'C' + str(para['adj_flag_chuan'])
            sg4['区段1'].element.pop(str_temp)

        # sg3['区段1'].element.pop('TB1')
        # sg3['区段1'].element.pop('TB2')


        self.section_group3 = sg3
        self.section_group4 = sg4

        # sg3.special_point = []
        # sg4.special_point = []

        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)
        self.l4 = l4 = Line(name_base='线路4', sec_group=sg4,
                            parameter=parameter)

        self.lg = LineGroup(l3, l4, name_base='线路组')

        self.lg.special_point = []
        self.lg.refresh()

    # def add_train(self):
    #     l3 = Line(name_base='线路3', sec_group=self.section_group3,
    #               parameter=self.parameter, train=self.train)
    #     self.l3 = l3
    #
    #     self.lg = LineGroup(l3, name_base='线路组')
    #     self.lg.refresh()

    def add_train(self):
        l4 = Line(name_base='线路4', sec_group=self.section_group4,
                  parameter=self.parameter, train=self.train1)
        self.l4 = l4

        l3 = Line(name_base='线路3', sec_group=self.section_group3,
                  parameter=self.parameter, train=self.train2)
        self.l3 = l3

        self.lg = LineGroup(self.l3, self.l4, name_base='线路组')
        self.lg.special_point = []
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
    # df = pd.read_excel('../Input/白俄验证输入参数.xlsx', header=None)

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
        2000: [1.306, 1.304e-3, None],
        2300: [1.435, 1.297e-3, None],
        2600: [1.558, 1.291e-3, None]}
    #
    # trk_2000A_21.rlc_s = {
    #     1700: [1.58, 1.38e-3, None],
    #     2000: [1.72, 1.37e-3, None],
    #     2300: [1.85, 1.36e-3, None],
    #     2600: [1.98, 1.35e-3, None]}

    # trk_2000A_21.rlc_s = {
    #     1700: [1.44, 1.25e-3, None],
    #     2000: [1.57, 1.24e-3, None],
    #     2300: [1.72, 1.23e-3, None],
    #     2600: [1.86, 1.22e-3, None]}

    # trk_2000A_21.rlc_s = {
    #     1700: [1.749, 1.255e-3, None],
    #     2000: [1.990, 1.243e-3, None],
    #     2300: [2.233, 1.232e-3, None],
    #     2600: [2.483, 1.222e-3, None]}

    para['Trk_z'].rlc_s = trk_2000A_21.rlc_s

    para['TAD_z3_发送端_区间'] = 2 * para['TAD_z3_发送端_区间']

    para['freq_主'] = 2600
    para['freq_被'] = 2000
    para['sr_mod_主'] = '右发'
    para['sr_mod_被'] = '右发'

    para['send_level'] = 5

    freq = para['freq_主']
    para['freq'] = Freq(freq)

    # head_list = ['区段长度', '电容间隔', '电容值', '电容数', '钢轨电阻', '钢轨电感',
    #              '区段频率', '分路电阻', '道床电阻',
    #              '调整轨入最大值', '调整轨入最小值',
    #              '分路残压最大值', '最大分路残压位置',
    #              '机车信号最小值', '最小机车信号位置']

    head_list = ['区段长度', '钢轨电阻', '钢轨电感',
                 '主串频率','被串频率',
                 '主串发送器位置', '被串发送器位置',
                 '分路电阻', '道床电阻',
                 '分路间隔','电缆长度', '主串电平级', '相对位置',
                 '调整轨入最大值', '最小机车信号位置', '机车信号感应系数',
                 '主串分路位置',
                 '主串拆卸情况','被串拆卸情况']

    # excel_list = []
    turnout_list = []

    excel_data = []
    excel_i_trk = []
    excel_i_sht = []
    excel_v_train = []
    excel_i_trk_zhu = []
    excel_i_tb = []
    excel_i_ca = []
    excel_i_C1 = []
    excel_i_C2 = []
    excel_i_C3 = []
    excel_i_C4 = []
    excel_i_C5 = []

    i_trk_scale = {
        1700: 310-47,
        2000: 275-41,
        2300: 255-38,
        2600: 235-35}

    v_coil_scale = 115

    # freq_list = [1700, 2000, 2300, 2600]
    # for length_t in [1000]:
    # for frq_zhu in [2600]:
    for frq_zhu in [2600]:
        frq_chuan = 2000
        # for direct in ['左发']:
        # for direct in ['右发']:
        direct = '右发'
            # frq_zhu = 2600
        for adj_flag_zhu in [0]:

        # for posi_zhu_fenlu in range(0, 626, 10):

            for adj_flag_chuan in [0]:
            # for frq_chuan in [2000]:
            # for frq_chuan in [2300]:
            # for frq_chuan in [2300, 2600, 1700, 2300]:
            # for frq_chuan in [1700, 2300]:
                # for length in range(700, 700, -50):
                length = length_t = 624
                # for offset in range(1400, 650, -50):
                # for offset in range((2*length), -50, -50):
                for offset in [0]:

                    # length = length_t = 1000
                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    para['freq_主'] = frq_zhu
                    para['freq_被'] = frq_chuan
                    freq = para['freq_主']
                    para['freq'] = Freq(freq)

                    para['sr_mod_主'] = direct
                    para['sr_mod_被'] = '左发'


                    # 数据表0
                    data = dict()
                    for key in head_list:
                        data[key] = None

                    data['主串拆卸情况'] = para['adj_flag_zhu'] = adj_flag_zhu
                    data['被串拆卸情况'] = para['adj_flag_chuan'] = adj_flag_chuan

                    data['相对位置'] = para['offset'] = offset
                    # length = 600
                    data['区段长度'] = para['length'] = length
                    data['钢轨电阻'] = round(para['Trk_z'].rlc_s[freq][0], 10)
                    data['钢轨电感'] = round(para['Trk_z'].rlc_s[freq][1], 10)
                    data['电缆长度'] = para['cab_len'] = cab_len = 10
                    data['主串频率'] = freq
                    data['被串频率'] = para['freq_被']
                    data['分路电阻'] = para['Rsht_z'] = r_sht = 0.0000001
                    data['道床电阻'] = rd = 1000
                    # data['道床电阻'] = 10000
                    data['最小机车信号位置'] = '-'
                    data['主串电平级'] = para['send_level']
                    data['主串发送器位置'] = para['sr_mod_主']
                    data['被串发送器位置'] = para['sr_mod_被']

                    data['道床电阻最大(Ω·km)'] = 1000
                    data['道床电阻最小(Ω·km)'] = 2
                    data['电缆电阻最大(Ω/km)'] = 45
                    data['电缆电阻最小(Ω/km)'] = 43

                    # data['电缆电容最大(F/km)'] = 30e-9
                    # data['电缆电容最小(F/km)'] = 26e-9

                    data['电缆电容最大(F/km)'] = 28e-9
                    data['电缆电容最小(F/km)'] = 28e-9

                    # data['主串分路位置'] = posi_zhu_fenlu

                    i_trk_scale_t = i_trk_scale[frq_zhu]

                    data['机车信号感应系数'] = str(v_coil_scale) + '/' + str(i_trk_scale_t)

                    inductance_coff = v_coil_scale / i_trk_scale_t

                    # para['Cable_R'].value = 43
                    # para['Rd'].value = 10000
                    para['Rd'].value = 6.6
                    para['pwr_v_flg'] = '最大'

                    # 调整计算最大
                    para['Cable_R'].value = data['电缆电阻最小(Ω/km)']
                    para['Cable_C'].value = data['电缆电容最大(F/km)']

                    # para['Rd'].value = data['道床电阻最大(Ω·km)']

                    # para['Rsht_z'] = data['分路电阻(Ω)']
                    # para['pwr_v_flg'] = '最大'
                    # para['length'] = data['区段长度min(m)']

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

                    data1 = md.lg['线路3']['地面']['区段1']['右调谐单元'].md_list[-1]['U2'].value_c
                    data['调整发送轨面max(V)'] = round(data1, 3)

                    data1 = md.lg['线路3']['地面']['区段1']['左调谐单元'].md_list[-1]['U2'].value_c
                    data['调整接收轨面max(V)'] = round(data1, 3)

                    # 调整计算
                    md = TestModel(turnout_list=turnout_list, parameter=para)
                    m1 = MainModel(md.lg, md=md)

                    drc_tmp = para['sr_mod_主']
                    string_t = None
                    if drc_tmp == '左发':
                        string_t = '右调谐单元'
                    elif drc_tmp == '右发':
                        string_t = '左调谐单元'

                    data1 = md.lg['线路3']['地面']['区段1'][string_t]['1接收器']['U'].value_c
                    data['调整轨入最大值'] = data1

                    # 分路计算
                    i_trk_list = list()
                    i_sht_list = list()
                    v_train_list = list()
                    i_trk_zhu_list = list()
                    i_tb_list = list()
                    i_ca_list = list()

                    i_C1_list = list()
                    i_C2_list = list()
                    i_C3_list = list()
                    i_C4_list = list()
                    i_C5_list = list()


                    # para['Cable_R'].value = data['电缆电阻最大(Ω/km)']
                    # para['Cable_C'].value = data['电缆电容最小(F/km)']
                    # para['Rd'].value = data['道床电阻最小(Ω·km)']
                    # para['Rsht_z'] = data['分路电阻(Ω)']
                    # para['pwr_v_flg'] = '最小'
                    # para['length'] = data['区段长度max(m)']


                    data['分路间隔'] = interval = 1

                    sht_length = length
                    # posi_list = np.arange(-14.5, (sht_length + 14.5), interval)

                    posi_list = np.arange(0, (sht_length), interval)
                    # posi_list = [291]
                    counter = 1
                    for posi_tr in posi_list:
                        md = TestModel(turnout_list=turnout_list, parameter=para)
                        md.add_train()
                        md.train1.posi_rlt = posi_tr
                        md.train1.set_posi_abs(0)

                        posi_zhu_fenlu = posi_tr
                        md.train2.posi_rlt = posi_zhu_fenlu
                        md.train2.set_posi_abs(0)
                        m1 = MainModel(md.lg, md=md)
                        # print(md.train.posi_abs)
                        # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                        i_sht = md.lg['线路4']['列车1']['分路电阻1']['I'].value_c

                        if m1['线路4'].node_dict[posi_tr].r_track is not None:
                            i_trk = m1['线路4'].node_dict[posi_tr].r_track['I1'].value_c
                        else:
                            print('###')
                            i_trk = 0.0

                        i_sht_zhu = md.lg['线路3']['列车2']['分路电阻1']['I'].value_c
                        if m1['线路3'].node_dict[posi_zhu_fenlu].r_track is not None:
                            i_trk_zhu = m1['线路3'].node_dict[posi_zhu_fenlu].r_track['I1'].value_c
                        else:
                            print('###')
                            i_trk_zhu = 0.0

                        # i_TB = md.lg['线路4']['地面']['区段1']['TB2']['I'].value_c

                        i_ca = md.lg['线路4']['地面']['区段1']['右调谐单元'].md_list[-1]['I2'].value_c

                        # i_C1 = md.lg['线路4']['地面']['区段1']['C5']['I'].value_c
                        # i_C2 = md.lg['线路4']['地面']['区段1']['C4']['I'].value_c
                        # i_C3 = md.lg['线路4']['地面']['区段1']['C3']['I'].value_c
                        # i_C4 = md.lg['线路4']['地面']['区段1']['C2']['I'].value_c
                        # i_C5 = md.lg['线路4']['地面']['区段1']['C1']['I'].value_c



                        # i_tb_list.append(i_TB)
                        i_ca_list.append(i_ca)

                        # i_C1_list.append(i_C1)
                        # i_C2_list.append(i_C2)
                        # i_C3_list.append(i_C3)
                        # i_C4_list.append(i_C4)
                        # i_C5_list.append(i_C5)

                        i_trk_list.append(i_trk)
                        i_trk_zhu_list.append(i_trk_zhu)
                        i_sht_list.append(i_sht)

                        v_train_list.append(i_trk*inductance_coff)
                    print(data.keys())
                    print(data.values())
                    print(i_sht_list)

                    data_row = [data[key] for key in head_list]
                    excel_data.append(data_row)
                    excel_i_trk.append(i_trk_list)
                    excel_i_trk_zhu.append(i_trk_zhu_list)
                    excel_i_tb.append(i_tb_list)
                    excel_i_ca.append(i_ca_list)

                    excel_i_C1.append(i_C1_list)
                    excel_i_C2.append(i_C2_list)
                    excel_i_C3.append(i_C3_list)
                    excel_i_C4.append(i_C4_list)
                    excel_i_C5.append(i_C5_list)


                    excel_i_sht.append(i_sht_list)
                    excel_v_train.append(v_train_list)


    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    df_i_trk = pd.DataFrame(excel_i_trk)
    df_i_trk_zhu = pd.DataFrame(excel_i_trk_zhu)
    df_i_sht = pd.DataFrame(excel_i_sht)
    df_v_train = pd.DataFrame(excel_v_train)
    df_i_tb = pd.DataFrame(excel_i_tb)
    df_i_ca = pd.DataFrame(excel_i_ca)

    df_i_C1 = pd.DataFrame(excel_i_C1)
    df_i_C2 = pd.DataFrame(excel_i_C2)
    df_i_C3 = pd.DataFrame(excel_i_C3)
    df_i_C4 = pd.DataFrame(excel_i_C4)
    df_i_C5 = pd.DataFrame(excel_i_C5)

    # head_list.extend(['最大干扰位置'])
    # excel_data.extend([])


    df_data = pd.DataFrame(excel_data, columns=head_list)

    # 保存到本地excel
    filename = '../Output/邻线干扰2000A' + timestamp + '.xlsx'
    with pd.ExcelWriter(filename) as writer:
        df_data.to_excel(writer, sheet_name="参数设置", index=False)
        df_i_trk_zhu.to_excel(writer, sheet_name="主串钢轨电流", index=False)
        df_i_trk.to_excel(writer, sheet_name="被串钢轨电流(分路点右侧)", index=False)
        df_i_sht.to_excel(writer, sheet_name="分路线电流", index=False)
        df_v_train.to_excel(writer, sheet_name="机车电压", index=False)
        df_i_tb.to_excel(writer, sheet_name="右侧TB电流", index=False)
        df_i_ca.to_excel(writer, sheet_name="右侧引接线电流", index=False)
        df_i_C1.to_excel(writer, sheet_name="右侧C1电流", index=False)
        df_i_C2.to_excel(writer, sheet_name="右侧C2电流", index=False)
        df_i_C3.to_excel(writer, sheet_name="右侧C3电流", index=False)
        df_i_C4.to_excel(writer, sheet_name="右侧C4电流", index=False)
        df_i_C5.to_excel(writer, sheet_name="右侧C5电流", index=False)


        pass