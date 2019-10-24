from src.TrackCircuitElement.SectionGroup import *
from src.TrackCircuitElement.Train import *
from src.TrackCircuitElement.Line import *
from src.TrackCircuitElement.LineGroup import *
from src.Model.MainModel import *
from src.Model.ModelParameter import *
from src.FrequencyType import Freq

import pandas as pd
import time
import itertools


class TestModel:
    # def __init__(self, freq, length, c_num, level, rd, r_cable, cab_len, turnout_list):
    def __init__(self, turnout_list, parameter):

        self.parameter = parameter
        self.train = Train(name_base='列车1', posi=0, parameter=parameter)

        # 轨道电路初始化
        # print(type(parameter['freq']))

        sg3 = SectionGroup(name_base='地面', posi=0, m_num=3, freq1=parameter['freq'],
                           m_length=[700, 700, 700],
                           j_length=[29, 29, 29, 29],
                           m_type=['2000A', '2000A', '2000A'],
                           c_num=[8, 11, 8],
                           parameter=parameter)

        # sg2 = SectionGroup(name_base='地面', posi=0, m_num=2, freq1=1700,
        #                    m_length=[480, 200, 320],
        #                    j_length=[29, 29, 29, 29],
        #                    m_type=['2000A', '2000A', '2000A'],
        #                    c_num=[8, 6, 5],
        #                    parameter=parameter)

        # sg3 = SectionGroup(name_base='地面', posi=0, m_num=1, freq1=parameter['freq'],
        #                    m_length=[parameter['length']],
        #                    j_length=[29, 29],
        #                    m_type=['2000A'],
        #                    c_num=[parameter['c_num']],
        #                    parameter=parameter)
        self.section_group3 = sg3

        l3 = Line(name_base='线路3', sec_group=sg3,
                  parameter=parameter)
        self.l3 = l3

        self.lg = LineGroup(l3, name_base='线路组')
        self.lg.refresh()

    def add_train(self):
        l3 = Line(name_base='线路3', sec_group=self.section_group3,
                  parameter=self.parameter, train=self.train)
        self.l3 = l3

        self.lg = LineGroup(l3, name_base='线路组')
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

    fq_list = [1700, 2000, 2300, 2600]
    len_list = [num for num in range(100, 1600, 100)]
    len_list.insert(3, 300)
    c_interval = 50
    c_num_list = [int(len_list[num] / c_interval) for num in range(len(len_list))]
    c_num_list[0] = 0
    c_num_list[1] = 0
    c_num_list[2] = 0

    para = ModelParameter()

    # 电容白俄
    c_value = 25e-6
    para['Ccmp_z'].rlc_s = {
        1700: [10e-3, None, c_value],
        2000: [10e-3, None, c_value],
        2300: [10e-3, None, c_value],
        2600: [10e-3, None, c_value]}

    # 白俄钢轨阻抗800
    trk_2000A_21 = ImpedanceMultiFreq()
    trk_2000A_21.rlc_s = {
        1700: [1.177, 1.314e-3, None],
        2000: [1.306, 1.304e-3, None],
        2300: [1.435, 1.297e-3, None],
        2600: [1.558, 1.291e-3, None]}

    # trk_Belarus_list = [trk_Belarus_25, trk_Belarus_800]

    para['cab_len'] = cab_len = 10
    para['level'] = level = 3

    # head_list = ['区段长度', '电容间隔', '电容值', '电容数', '钢轨电阻', '钢轨电感',
    #              '区段频率', '分路电阻', '道床电阻',
    #              '调整轨入最大值', '调整轨入最小值',
    #              '分路残压最大值', '最大分路残压位置',
    #              '机车信号最小值', '最小机车信号位置']

    head_list = ['区段长度', '电容间隔', '钢轨电阻', '钢轨电感',
                 '主串频率', '分路电阻', '道床电阻',
                 '调整轨入最大值', '最小机车信号位置']

    excel_list = []
    turnout_list = []

    # 数据表
    data = dict()
    for key in head_list:
        data[key] = None

    data['最小机车信号位置'] = '-'

    # 固定参数
    para['length'] = length = 1200
    rd = 2
    para['Rsht_z'] = r_sht = 0.01
    freq = 1700
    para['freq'] = Freq(freq)

    # 循环参数
    cab_rd_list = [(43, 10000), (47, rd)]

    # 调整状态计算
    para['Trk_z'].rlc_s = trk_2000A_21.rlc_s
    para['freq'].value = freq
    rd = 2
    # r_sht = 0.15

    data['区段长度'] = para['length']
    data['电容间隔'] = c_interval
    data['钢轨电阻'] = round(para['Trk_z'].rlc_s[freq][0], 10)
    data['钢轨电感'] = round(para['Trk_z'].rlc_s[freq][1], 10)
    data['主串频率'] = freq
    data['分路电阻'] = r_sht
    data['道床电阻'] = rd

    cab_rd = (43, 10000)

    para['Cable_R'].value = cab_rd[0]
    para['Rd'].value = cab_rd[1]

    md = TestModel(turnout_list=turnout_list, parameter=para)
    m1 = MainModel(md.lg, md=md)

    data1 = md.lg['线路3']['地面']['区段1']['右调谐单元']['1接收器']['U'].value_c
    data['调整轨入最大值'] = data1

    print(data)

    i_trk_list = list()
    i_sht_list = list()

    # 分路计算
    posi_list = range(11, (length - 11), 1)
    for posi_tr in posi_list:
        md = TestModel(turnout_list=turnout_list, parameter=para)
        md.add_train()
        md.train.posi_rlt = posi_tr
        md.train.set_posi_abs(0)
        m1 = MainModel(md.lg, md=md)
        print(md.train.posi_abs)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        i_sht = md.lg['线路3']['列车1']['分路电阻1']['I'].value_c
        if m1['线路3'].node_dict[posi_tr].l_track is not None:
            i_trk = m1['线路3'].node_dict[posi_tr].l_track['I2'].value_c
        else:
            i_trk = 0.0
        i_trk_list.append(i_trk)
        i_sht_list.append(i_sht)
    print(i_trk_list)

    df = pd.DataFrame([i_trk_list, i_sht_list])

    # 保存到本地excel
    filename = '../Output/邻线干扰2000A' + timestamp + '.xlsx'
    with pd.ExcelWriter(filename) as writer:
        df.to_excel(writer, sheet_name="调整表", index=False)
        pass