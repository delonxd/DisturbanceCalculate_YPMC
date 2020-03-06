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
import os


class TestModel:
    def __init__(self, turnout_list, parameter):
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train2 = Train(name_base='列车2', posi=0, parameter=parameter)
        self.train3 = Train(name_base='列车3', posi=0, parameter=parameter)
        self.train4 = Train(name_base='列车4', posi=0, parameter=parameter)

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

        if para['主串拆卸情况'] > 0:
            str_temp = 'C' + str(para['主串拆卸情况'])
            sg3['区段1'].element.pop(str_temp)

        if para['被串拆卸情况'] > 0:
            str_temp = 'C' + str(para['被串拆卸情况'])
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

        sg3['区段1'].element.pop('TB1')
        sg3['区段1'].element.pop('TB2')
        #
        sg4['区段1'].element.pop('TB1')
        sg4['区段1'].element.pop('TB2')


        sg3['区段1'].element.pop('左调谐单元')
        sg4['区段1'].element.pop('左调谐单元')
        sg4['区段1'].element.pop('右调谐单元')


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

        self.lg.special_point = para['special_point']
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
                  parameter=self.parameter, train=[self.train1, self.train3])
        self.l4 = l4

        l3 = Line(name_base='线路3', sec_group=self.section_group3,
                  parameter=self.parameter, train=[self.train2, self.train4])
        self.l3 = l3

        self.lg = LineGroup(self.l3, self.l4, name_base='线路组')
        self.lg.special_point = para['special_point']
        self.lg.refresh()


class Data2Excel:
    def __init__(self, sheet_names):
        self.sheet_names = sheet_names
        self.data_dict = {}
        self.dataframes = {}
        for name in sheet_names:
            self.data_dict[name] = []

    def add_row(self):
        for value in self.data_dict.values():
            value.append([])

    def add_sheet_name(self, sheet_name):
        self.data_dict[sheet_name] = []

    def add_dataframes(self, sheet_name, dataframe):
        self.dataframes[sheet_name] = dataframe

    def add_data(self, sheet_name, data1):
        if sheet_name in self.data_dict.keys():
            self.data_dict[sheet_name][-1].append(data1)
        else:
            self.data_dict[sheet_name] = [[]]
            self.data_dict[sheet_name][-1].append(data1)

    # def create_dataframes(self):
    #     for name, value in self.data_dict.items():
    #         self.dataframes[name] = pd.DataFrame(value)

    def write2excel(self, sheet_names, header, writer1):
        for name in sheet_names:
            df_output = pd.DataFrame(self.data_dict[name], columns=header)
            df_output.to_excel(writer1, sheet_name=name, index=False)


if __name__ == '__main__':
    df_input = pd.read_excel('src/Input/邻线干扰参数输入.xlsx')

    localtime = time.localtime()
    timestamp = time.strftime("%Y%m%d%H%M%S", localtime)
    print(time.strftime("%Y-%m-%d %H:%M:%S", localtime))

    num_len = len(list(df_input['序号']))

    # para = ModelParameter()

    work_path = os.getcwd()
    para = ModelParameter(workpath=work_path)

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

    i_trk_scale = {
        1700: 310-47,
        2000: 275-41,
        2300: 255-38,
        2600: 235-35}

    v_coil_scale = 115


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
    data2excel = Data2Excel(sheet_names=[])

    # temp_list = ['正常']
                 # '主串PT开路', '被串PT开路', '主被串PT开路',
                 # '主串PT短路', '被串PT短路', '主被串PT短路',
                 # '主串SVA1开路', '被串SVA1开路', '主被串SVA1开路',
                 # '主串SVA1短路', '被串SVA1短路', '主被串SVA1短路',
                 # '主串TB开路', '被串TB开路', '主被串TB开路',
                 # '主串TB短路', '被串TB短路', '主被串TB短路']

    # columns_max = 0
    # for temp_temp in range(num_len):

    # rd_list = list(range(20, 0, -1))
    rd_list = list()
    rd_list.insert(0, 10000)

    counter = 1
    for temp_temp in rd_list:

        # if length > columns_max:
        #     columns_max = length

        l1 = 6
        d = 1.435
        k_mutual = 13 / np.log((l1 * l1 - d * d) / l1 / l1)
        l2 = 4.5
        kkk = k_mutual * np.log((l2 * l2 - d * d) / l2 / l2)


        for l_d in [6]:

            # para['线间距'] = l_d
            # para['耦合系数'] = k_mutual * np.log((l_d * l_d - d * d) / l_d / l_d)

            for frq_zhu in [2600]:
                for frq_chuan in [2000]:

                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    # 数据表0
                    data = dict()
                    for key in head_list:
                        data[key] = None

                    # data['序号'] = para['序号'] = df_input['序号'][temp_temp]
                    # data['区段长度'] = para['length'] = length = df_input['区段长度(m)'][temp_temp]
                    # data['耦合系数'] = para['耦合系数'] = df_input['耦合系数'][temp_temp]
                    # data['主串电平级'] =para['send_level'] = df_input['主串电平级'][temp_temp]
                    # data['主串频率'] = para['freq_主'] = freq = df_input['主串频率(Hz)'][temp_temp]
                    # data['被串频率'] = para['freq_被'] = df_input['被串频率(Hz)'][temp_temp]
                    # data['主串电容数'] = para['主串电容数'] = df_input['主串电容数'][temp_temp]
                    # data['被串电容数'] = para['被串电容数'] = df_input['被串电容数'][temp_temp]
                    # data['道床电阻'] = rd_temp = df_input['道床电阻(Ω·km)'][temp_temp]

                    data['故障情况'] = para['故障情况'] = '正常'
                    data['主串电平级'] = para['send_level'] = 5

                    data['序号'] = para['序号'] = counter
                    data['区段长度'] = para['length'] = length = 650
                    data['耦合系数'] = para['耦合系数'] = 13

                    data['主串频率'] = para['freq_主'] = freq = 2600
                    data['被串频率'] = para['freq_被'] = 2000
                    data['freq'] = para['freq'] = Freq(freq)

                    data['主串电容数'] = para['主串电容数'] = 0
                    data['被串电容数'] = para['被串电容数'] = 0

                    data['道床电阻'] = rd_temp = temp_temp
                    data['特殊位置'] = para['special_point'] = list(np.linspace(0,length + length, 21))

                    data['主串发送器位置'] = para['sr_mod_主'] = '右发'
                    data['被串发送器位置'] = para['sr_mod_被'] = '右发'

                    data['主串拆卸情况'] = para['主串拆卸情况'] = adj_flag_zhu = 0
                    data['被串拆卸情况'] = para['被串拆卸情况'] = adj_flag_chuan = 0

                    data['相对位置'] = para['offset'] = offset = 0

                    data['钢轨电阻'] = round(para['Trk_z'].rlc_s[freq][0], 10)
                    data['钢轨电感'] = round(para['Trk_z'].rlc_s[freq][1], 10)
                    data['电缆长度'] = para['cab_len'] = cab_len = 10
                    data['分路电阻'] = para['Rsht_z'] = r_sht = 0.0000001

                    data['最小机车信号位置'] = '-'

                    # data['线间距'] = para['线间距'] = l_d
                    # freq = para['freq_主']
                    # data['freq'] = para['freq'] = Freq(freq)
                    # data['道床电阻'] = rd_temp
                    # data['极性交叉位置'] = para['special_point']
                    # data['主串分路位置'] = posi_zhu_fenlu

                    data['道床电阻最大(Ω·km)'] = 1000
                    data['道床电阻最小(Ω·km)'] = 2
                    data['电缆电阻最大(Ω/km)'] = 45
                    data['电缆电阻最小(Ω/km)'] = 43

                    # data['电缆电容最大(F/km)'] = 30e-9
                    # data['电缆电容最小(F/km)'] = 26e-9
                    data['电缆电容最大(F/km)'] = 28e-9
                    data['电缆电容最小(F/km)'] = 28e-9


                    denominator = i_trk_scale[frq_zhu]
                    nominator = v_coil_scale

                    data['机车信号感应系数'] = str(nominator) + '/' + str(denominator)
                    para['机车信号系数值'] = nominator / denominator


                    # 调整计算最大
                    para['Rd'].value = rd_temp
                    para['pwr_v_flg'] = '最大'
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

                    # data1 = md.lg['线路3']['地面']['区段1'][string_t]['1接收器']['U'].value_c
                    # data['调整接收轨入max(V)'] = round(data1, 3)
                    #
                    # data1 = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['U2'].value_c
                    # # print(data1)
                    # data['调整功出电压max(V)'] = round(data1, 3)
                    #
                    # data1 = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['I2'].value_c
                    # data['调整功出电流max(I)'] = round(data1, 3)
                    #
                    # data1 = md.lg['线路3']['地面']['区段1']['右调谐单元'].md_list[-1]['U2'].value_c
                    # data['调整发送轨面max(V)'] = round(data1, 3)
                    #
                    # data1 = md.lg['线路3']['地面']['区段1']['左调谐单元'].md_list[-1]['U2'].value_c
                    # data['调整接收轨面max(V)'] = round(data1, 3)

                    # # 调整计算
                    # md = TestModel(turnout_list=turnout_list, parameter=para)
                    # m1 = MainModel(md.lg, md=md)


                    # 分路计算
                    data2excel.add_row()
                    data['分路间隔'] = interval = 1

                    sht_length = length
                    posi_list = np.arange(sht_length, -1, -interval)

                    for posi_tr in posi_list:
                        md = TestModel(turnout_list=turnout_list, parameter=para)
                        md.add_train()
                        md.train1.posi_rlt = posi_tr
                        md.train1.set_posi_abs(0)

                        posi_zhu_fenlu = posi_tr
                        md.train2.posi_rlt = posi_zhu_fenlu
                        md.train2.set_posi_abs(0)

                        posi_rrr = length - posi_tr + length

                        md.train3.posi_rlt = posi_rrr
                        md.train3.set_posi_abs(0)

                        md.train4.posi_rlt = posi_rrr
                        md.train4.set_posi_abs(0)

                        m1 = MainModel(md.lg, md=md)


                        i_sht_zhu = md.lg['线路3']['列车2']['分路电阻1']['I'].value_c
                        i_sht_chuan = md.lg['线路4']['列车1']['分路电阻1']['I'].value_c
                        i_trk_zhu = get_i_trk(line=m1['线路3'], posi=posi_zhu_fenlu, direct='右')
                        i_trk_chuan = get_i_trk(line=m1['线路4'], posi=posi_tr, direct='右')

                        # i_source_fs = m1['线路3'].node_dict[length].l_track['I2'].value
                        i_source_fs = md.lg['线路3']['地面']['区段1']['右调谐单元'].md_list[-1]['I2'].value
                        v_load_fs = m1['线路4'].node_dict[length].l_track['U2'].value

                        # z_mm = np.inf if i_source_fs == 0 else v_load_fs / i_source_fs
                        z_mm = v_load_fs / i_source_fs
                        z_mm_abs = abs(z_mm)
                        co_mutal = z_mm_abs / 2 / np.pi / para['freq_主'] / (length-posi_tr)*1000 * 1e6 * 2
                        co_mutal = round(co_mutal, 2)

                        # i_TB = md.lg['线路4']['地面']['区段1']['TB2']['I'].value_c
                        # i_ca = md.lg['线路4']['地面']['区段1']['右调谐单元'].md_list[-1]['I2'].value_c
                        # i_C1 = md.lg['线路4']['地面']['区段1']['C5']['I'].value_c
                        # i_C2 = md.lg['线路4']['地面']['区段1']['C4']['I'].value_c
                        # i_C3 = md.lg['线路4']['地面']['区段1']['C3']['I'].value_c
                        # i_C4 = md.lg['线路4']['地面']['区段1']['C2']['I'].value_c
                        # i_C5 = md.lg['线路4']['地面']['区段1']['C1']['I'].value_c

                        data2excel.add_data(sheet_name="主串钢轨电流", data1=i_trk_zhu)
                        data2excel.add_data(sheet_name="被串钢轨电流", data1=i_trk_chuan)
                        data2excel.add_data(sheet_name="被串分路电流", data1=i_sht_chuan)
                        data2excel.add_data(sheet_name="实测阻抗", data1=z_mm)
                        data2excel.add_data(sheet_name="阻抗模值", data1=z_mm_abs)
                        data2excel.add_data(sheet_name="耦合系数", data1=co_mutal)

                    i_trk_list = data2excel.data_dict["被串钢轨电流"][-1]
                    i_sht_list = data2excel.data_dict["被串分路电流"][-1]

                    data['钢轨电流最大值'] = max(i_trk_list)
                    data['最大值位置'] = i_trk_list.index(max(i_trk_list))

                    print(data.keys())
                    print(data.values())
                    print(i_sht_list)

                    data_row = [data[key] for key in head_list]
                    excel_data.append(data_row)
                    counter += 1


    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    #
    # posi_header = list(range(columns_max+1))
    # posi_header[0] = '发送端'

    df_data = pd.DataFrame(excel_data, columns=head_list)


    # 保存到本地excel
    filename = 'src/Output/邻线干扰2000A' + timestamp + '.xlsx'
    with pd.ExcelWriter(filename) as writer:
        df_input.to_excel(writer, sheet_name="参数设置", index=False)
        df_data.to_excel(writer, sheet_name="数据输出", index=False)

        names = ["主串钢轨电流",
                 "被串钢轨电流",
                 "被串分路电流",
                 "实测阻抗",
                 "阻抗模值",
                 "耦合系数"]

        data2excel.write2excel(sheet_names=names, header=None, writer1=writer)

        pass