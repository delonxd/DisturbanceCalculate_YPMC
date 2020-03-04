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
        # c_nums = [7]


        sg3 = SectionGroup(name_base='地面', posi=para['offset'], m_num=1,
                           m_frqs=m_frqs,
                           m_lens=m_lens,
                           j_lens=[0]*4,
                           m_typs=['2000A']*3,
                           c_nums=[para['主串电容数']+2],
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
        # c_nums = [7]
        sg4 = SectionGroup(name_base='地面', posi=0, m_num=1,
                           m_frqs=m_frqs,
                           m_lens=m_lens,
                           j_lens=[0]*4,
                           m_typs=['2000A']*3,
                           c_nums=[para['被串电容数']+2],
                           sr_mods=[para['sr_mod_被']]*3,
                           send_lvs=[send_level]*3,
                           parameter=parameter)

        if para['adj_flag_zhu'] > 0:
            str_temp = 'C' + str(para['adj_flag_zhu'])
            sg3['区段1'].element.pop(str_temp)

        if para['adj_flag_chuan'] > 0:
            str_temp = 'C' + str(para['adj_flag_chuan'])
            sg4['区段1'].element.pop(str_temp)

        # if para['故障情况'] == '主串PT开路':
        #     sg3['区段1']['右调谐单元']['5BA'].z = {2600: para['标准开路阻抗']}
        # elif para['故障情况'] == '被串PT开路':
        #     sg4['区段1']['右调谐单元']['5BA'].z = {2000: para['标准开路阻抗']}
        # elif para['故障情况'] == '主被串PT开路':
        #     sg3['区段1']['右调谐单元']['5BA'].z = {2600: para['标准开路阻抗']}
        #     sg4['区段1']['右调谐单元']['5BA'].z = {2000: para['标准开路阻抗']}

        # sg3['区段1']['右调谐单元']['6SVA1'].z = para['标准开路阻抗']

        if para['故障情况'] == '主串PT开路':
            sg3['区段1']['右调谐单元']['5PT_CA'].z = para['标准开路阻抗']
        elif para['故障情况'] == '被串PT开路':
            sg4['区段1']['右调谐单元']['5PT_CA'].z = para['标准开路阻抗']
        elif para['故障情况'] == '主被串PT开路':
            sg3['区段1']['右调谐单元']['5PT_CA'].z = para['标准开路阻抗']
            sg4['区段1']['右调谐单元']['5PT_CA'].z = para['标准开路阻抗']

        elif para['故障情况'] == '主串PT短路':
            sg3['区段1']['右调谐单元']['5BA'].z = {2600: para['标准短路阻抗']}
        elif para['故障情况'] == '被串PT短路':
            sg4['区段1']['右调谐单元']['5BA'].z = {2000: para['标准短路阻抗']}
        elif para['故障情况'] == '主被串PT短路':
            sg3['区段1']['右调谐单元']['5BA'].z = {2600: para['标准短路阻抗']}
            sg4['区段1']['右调谐单元']['5BA'].z = {2000: para['标准短路阻抗']}

        elif para['故障情况'] == '主串SVA1开路':
            sg3['区段1']['右调谐单元']['6SVA1'].z = para['标准开路阻抗']
        elif para['故障情况'] == '被串SVA1开路':
            sg4['区段1']['右调谐单元']['6SVA1'].z = para['标准开路阻抗']
        elif para['故障情况'] == '主被串SVA1开路':
            sg3['区段1']['右调谐单元']['6SVA1'].z = para['标准开路阻抗']
            sg4['区段1']['右调谐单元']['6SVA1'].z = para['标准开路阻抗']
        elif para['故障情况'] == '主串SVA1短路':
            sg3['区段1']['右调谐单元']['6SVA1'].z = para['标准短路阻抗']
        elif para['故障情况'] == '被串SVA1短路':
            sg4['区段1']['右调谐单元']['6SVA1'].z = para['标准短路阻抗']
        elif para['故障情况'] == '主被串SVA1短路':
            sg3['区段1']['右调谐单元']['6SVA1'].z = para['标准短路阻抗']
            sg4['区段1']['右调谐单元']['6SVA1'].z = para['标准短路阻抗']

        elif para['故障情况'] == '主串TB开路':
            sg3['区段1']['TB2'].z = para['标准开路阻抗']
        elif para['故障情况'] == '被串TB开路':
            sg4['区段1']['TB2'].z = para['标准开路阻抗']
        elif para['故障情况'] == '主被串TB开路':
            sg3['区段1']['TB2'].z = para['标准开路阻抗']
            sg4['区段1']['TB2'].z = para['标准开路阻抗']
        elif para['故障情况'] == '主串TB短路':
            sg3['区段1']['TB2'].z = para['标准短路阻抗']
        elif para['故障情况'] == '被串TB短路':
            sg4['区段1']['TB2'].z = para['标准短路阻抗']
        elif para['故障情况'] == '主被串TB短路':
            sg3['区段1']['TB2'].z = para['标准短路阻抗']
            sg4['区段1']['TB2'].z = para['标准短路阻抗']

        # sg3['区段1'].element.pop('TB2')
        # sg4['区段1'].element.pop('TB2')

        # sg3['区段1']['右调谐单元']['6SVA1'].z = para['标准开路阻抗']
        # sg3['区段1']['右调谐单元']['5BA'].z = {2600: para['标准短路阻抗']}
        # sg4['区段1']['右调谐单元']['5BA'].z = {2000: para['标准短路阻抗']}

        # sg3['区段1']['TB2'].z = para['标准开路阻抗']
        # sg4['区段1']['TB2'].z = para['标准开路阻抗']

        self.section_group3 = sg3
        self.section_group4 = sg4

        # sg3.special_point = [para['special_point']]
        # sg4.special_point = []

        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)
        self.l4 = l4 = Line(name_base='线路4', sec_group=sg4,
                            parameter=parameter)

        self.lg = LineGroup(l3, l4, name_base='线路组')

        self.lg.special_point = [para['special_point']]
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
        self.lg.special_point = [para['special_point']]
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
    df_input = pd.read_excel('邻线干扰参数输入.xlsx')

    localtime = time.localtime()
    timestamp = time.strftime("%Y%m%d%H%M%S", localtime)
    print(time.strftime("%Y-%m-%d %H:%M:%S", localtime))
    print('开始计算')

    num_len = len(list(df_input['序号']))

    para = ModelParameter()

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


    # head_list = ['区段长度', '钢轨电阻', '钢轨电感',
    #              '主串频率','被串频率',
    #              '主串发送器位置', '被串发送器位置',
    #              '分路电阻', '道床电阻',
    #              '分路间隔','电缆长度', '主串电平级', '相对位置',
    #              '调整轨入最大值', '最小机车信号位置', '机车信号感应系数',
    #              '主串分路位置',
    #              '主串拆卸情况','被串拆卸情况',
    #              '线间距', '耦合系数',
    #              '钢轨电流最大值', '最大值位置',
    #              '故障情况', '极性交叉位置']

    head_list = ['序号', '区段长度', '耦合系数',
                 '钢轨电阻', '钢轨电感',
                 '主串频率', '被串频率',
                 '主串发送器位置', '被串发送器位置',
                 '分路电阻', '道床电阻',
                 '分路间隔', '电缆长度', '主串电平级',
                 '调整轨入最大值',
                 '钢轨电流最大值', '最大值位置']


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
    excel_z_trk_right = []


    i_trk_scale = {
        1700: 310-47,
        2000: 275-41,
        2300: 255-38,
        2600: 235-35}

    v_coil_scale = 115

    # rd_list = list(range(30,0,-1))
    # rd_list.insert(0, 10000)

    # temp_list = ['正常']
                 # '主串PT开路', '被串PT开路', '主被串PT开路',
                 # '主串PT短路', '被串PT短路', '主被串PT短路',
                 # '主串SVA1开路', '被串SVA1开路', '主被串SVA1开路',
                 # '主串SVA1短路', '被串SVA1短路', '主被串SVA1短路',
                 # '主串TB开路', '被串TB开路', '主被串TB开路',
                 # '主串TB短路', '被串TB短路', '主被串TB短路']
    # sp_list = list(range(0,626,10))
    # sp_list = [0]

    # for temp_temp in temp_list:
    # for temp_temp in [0]:

    columns_max = 0
    for temp_temp in range(num_len):

        localtime = time.localtime()
        print(time.strftime("%Y-%m-%d %H:%M:%S", localtime))
        print(df_input[temp_temp:(temp_temp+1)])

        para['故障情况'] = '正常'
        para['send_level'] = 5
        para['special_point'] = 0

        para['序号'] = df_input['序号'][temp_temp]
        length = df_input['区段长度(m)'][temp_temp]
        para['耦合系数'] = df_input['耦合系数'][temp_temp]
        para['send_level'] = df_input['主串电平级'][temp_temp]
        para['freq_主'] = df_input['主串频率(Hz)'][temp_temp]
        para['freq_被'] = df_input['被串频率(Hz)'][temp_temp]
        para['主串电容数'] = df_input['主串电容数'][temp_temp]
        para['被串电容数'] = df_input['被串电容数'][temp_temp]
        rd_temp = df_input['道床电阻(Ω·km)'][temp_temp]

        if length > columns_max:
            columns_max = length

        # l1 = 6
        # d = 1.435
        # k_mutual = 13 / np.log((l1 * l1 - d * d) / l1 / l1)
        # l2 = 4.5
        # kkk = k_mutual * np.log((l2 * l2 - d * d) / l2 / l2)


        for l_d in [6]:

            # para['线间距'] = l_d
            # para['耦合系数'] = k_mutual * np.log((l_d * l_d - d * d) / l_d / l_d)

            for frq_zhu in [2600]:
                for frq_chuan in [2000]:
                    # length = length_t = 626
                    adj_flag_zhu = 0
                    adj_flag_chuan = 0

                    offset = 0
                    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


                    # para['freq_主'] = frq_zhu
                    # para['freq_被'] = frq_chuan

                    freq = para['freq_主']
                    para['freq'] = Freq(freq)

                    para['sr_mod_主'] = '右发'
                    para['sr_mod_被'] = '右发'


                    # 数据表0
                    data = dict()
                    for key in head_list:
                        data[key] = None

                    data['主串拆卸情况'] = para['adj_flag_zhu'] = adj_flag_zhu
                    data['被串拆卸情况'] = para['adj_flag_chuan'] = adj_flag_chuan

                    # data['线间距'] = para['线间距']
                    data['序号'] = para['序号']
                    data['耦合系数'] = para['耦合系数']

                    data['相对位置'] = para['offset'] = offset
                    data['区段长度'] = para['length'] = length
                    data['钢轨电阻'] = round(para['Trk_z'].rlc_s[freq][0], 10)
                    data['钢轨电感'] = round(para['Trk_z'].rlc_s[freq][1], 10)
                    data['电缆长度'] = para['cab_len'] = cab_len = 10
                    data['主串频率'] = freq
                    data['被串频率'] = para['freq_被']
                    data['分路电阻'] = para['Rsht_z'] = r_sht = 0.0000001
                    data['道床电阻'] = rd = rd_temp

                    data['最小机车信号位置'] = '-'
                    data['主串电平级'] = para['send_level']
                    data['主串发送器位置'] = para['sr_mod_主']
                    data['被串发送器位置'] = para['sr_mod_被']

                    data['故障情况'] = para['故障情况']

                    data['道床电阻最大(Ω·km)'] = 1000
                    data['道床电阻最小(Ω·km)'] = 2
                    data['电缆电阻最大(Ω/km)'] = 45
                    data['电缆电阻最小(Ω/km)'] = 43

                    # data['电缆电容最大(F/km)'] = 30e-9
                    # data['电缆电容最小(F/km)'] = 26e-9

                    data['电缆电容最大(F/km)'] = 28e-9
                    data['电缆电容最小(F/km)'] = 28e-9

                    data['极性交叉位置'] = para['special_point']

                    # data['主串分路位置'] = posi_zhu_fenlu

                    i_trk_scale_t = i_trk_scale[frq_zhu]

                    data['机车信号感应系数'] = str(v_coil_scale) + '/' + str(i_trk_scale_t)

                    inductance_coff = v_coil_scale / i_trk_scale_t

                    para['Rd'].value = rd_temp
                    para['pwr_v_flg'] = '最大'

                    # 调整计算最大
                    para['Cable_R'].value = data['电缆电阻最小(Ω/km)']
                    para['Cable_C'].value = data['电缆电容最大(F/km)']

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
                    # print(data1)
                    data['调整功出电压max(V)'] = round(data1, 3)

                    data1 = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['I2'].value_c
                    data['调整功出电流max(I)'] = round(data1, 3)

                    data1 = md.lg['线路3']['地面']['区段1']['右调谐单元'].md_list[-1]['U2'].value_c
                    data['调整发送轨面max(V)'] = round(data1, 3)

                    data1 = md.lg['线路3']['地面']['区段1']['左调谐单元'].md_list[-1]['U2'].value_c
                    data['调整接收轨面max(V)'] = round(data1, 3)

                    data1 = m1['线路3'].node_dict[0].r_track['I1'].value_c
                    data['调整入口电流max(A)'] = data1

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

                    z_trk_right_list = list()


                    data['分路间隔'] = interval = 1

                    sht_length = length
                    # posi_list = np.arange(-14.5, (sht_length + 14.5), interval)

                    posi_list = np.arange(sht_length, -1, -interval)

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

                        i_sht = md.lg['线路4']['列车1']['分路电阻1']['I'].value_c

                        if m1['线路4'].node_dict[posi_tr].r_track is not None:
                            i_trk = m1['线路4'].node_dict[posi_tr].r_track['I1'].value_c
                            uuu = m1['线路4'].node_dict[posi_tr].r_track['U1'].value
                            iii = -m1['线路4'].node_dict[posi_tr].r_track['I1'].value
                            z_trk_right = uuu/iii
                        else:
                            # print('###')
                            i_trk = 0.0
                            z_trk_right = 0.0

                        i_sht_zhu = md.lg['线路3']['列车2']['分路电阻1']['I'].value_c
                        if m1['线路3'].node_dict[posi_zhu_fenlu].r_track is not None:
                            i_trk_zhu = m1['线路3'].node_dict[posi_zhu_fenlu].r_track['I1'].value_c
                        else:
                            # print('###')
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
                        z_trk_right_list.append(z_trk_right)


                        v_train_list.append(i_trk*inductance_coff)

                    data['钢轨电流最大值'] = max(i_trk_list)
                    data['最大值位置'] = i_trk_list.index(max(i_trk_list))

                    # print(data.keys())
                    # print(data.values())
                    # print(i_sht_list)

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

                    excel_z_trk_right.append(z_trk_right_list)


                    excel_i_sht.append(i_sht_list)
                    excel_v_train.append(v_train_list)


    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    posi_header = list(range(columns_max+1))
    posi_header[0] = '发送端'

    df_i_trk = pd.DataFrame(excel_i_trk, columns=posi_header)
    df_i_trk_zhu = pd.DataFrame(excel_i_trk_zhu, columns=posi_header)
    df_i_sht = pd.DataFrame(excel_i_sht, columns=posi_header)
    # df_v_train = pd.DataFrame(excel_v_train)
    # df_i_tb = pd.DataFrame(excel_i_tb)
    # df_i_ca = pd.DataFrame(excel_i_ca)

    # df_i_C1 = pd.DataFrame(excel_i_C1)
    # df_i_C2 = pd.DataFrame(excel_i_C2)
    # df_i_C3 = pd.DataFrame(excel_i_C3)
    # df_i_C4 = pd.DataFrame(excel_i_C4)
    # df_i_C5 = pd.DataFrame(excel_i_C5)
    #
    # df_z_trk_right = pd.DataFrame(excel_z_trk_right)

    df_data = pd.DataFrame(excel_data, columns=head_list)


    # 保存到本地excel
    filename = '邻线干扰仿真_' + timestamp + '.xlsx'
    with pd.ExcelWriter(filename) as writer:
        df_input.to_excel(writer, sheet_name="参数设置", index=False)
        df_data.to_excel(writer, sheet_name="数据输出", index=False)
        df_i_trk_zhu.to_excel(writer, sheet_name="主串分路钢轨电流", index=False)
        df_i_trk.to_excel(writer, sheet_name="被串分路钢轨电流", index=False)
        df_i_sht.to_excel(writer, sheet_name="分路线电流", index=False)

        # df_v_train.to_excel(writer, sheet_name="机车电压", index=False)
        # df_i_tb.to_excel(writer, sheet_name="右侧TB电流", index=False)
        # df_i_ca.to_excel(writer, sheet_name="右侧引接线电流", index=False)
        # df_i_C1.to_excel(writer, sheet_name="右侧C1电流", index=False)
        # df_i_C2.to_excel(writer, sheet_name="右侧C2电流", index=False)
        # df_i_C3.to_excel(writer, sheet_name="右侧C3电流", index=False)
        # df_i_C4.to_excel(writer, sheet_name="右侧C4电流", index=False)
        # df_i_C5.to_excel(writer, sheet_name="右侧C5电流", index=False)
        # df_z_trk_right.to_excel(writer, sheet_name="被串分路阻抗", index=False)

    localtime = time.localtime()
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print('计算结束')