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
        self.parameter = parameter
        self.train = Train(name_base='列车1', posi=0, parameter=parameter)

        # 轨道电路初始化
        m_lens = [para['length']]*3
        m_frqs = generate_frqs(Freq(para['freq_主']), 3)
        c_nums = get_c_nums(m_frqs, m_lens)
        sg3 = SectionGroup(name_base='地面', posi=para['offset'], m_num=1,
                           m_frqs=m_frqs,
                           m_lens=m_lens,
                           j_lens=[29]*4,
                           m_typs=['2000A']*3,
                           c_nums=c_nums,
                           sr_mods=[para['sr_mod_主']]*3,
                           send_lvs=[3, 3, 3],
                           parameter=parameter)
        sg3['区段1']['左调谐单元'].set_power_voltage()

        m_lens = [para['length']]*3
        m_frqs = generate_frqs(Freq(para['freq_被']), 3)
        c_nums = get_c_nums(m_frqs, m_lens)
        sg4 = SectionGroup(name_base='地面', posi=0, m_num=3,
                           m_frqs=m_frqs,
                           m_lens=m_lens,
                           j_lens=[29]*4,
                           m_typs=['2000A']*3,
                           c_nums=c_nums,
                           sr_mods=[para['sr_mod_被']]*3,
                           send_lvs=[3, 3, 3],
                           parameter=parameter)

        self.section_group3 = sg3
        self.section_group4 = sg4

        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)
        self.l4 = l4 = Line(name_base='线路4', sec_group=sg4,
                            parameter=parameter)

        self.lg = LineGroup(l3, l4, name_base='线路组')
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
                  parameter=self.parameter, train=self.train)
        self.l4 = l4

        self.lg = LineGroup(self.l3, self.l4, name_base='线路组')
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
    para['Trk_z'].rlc_s = trk_2000A_21.rlc_s

    para['freq_主'] = 2600
    para['freq_被'] = 2300
    para['sr_mod_主'] = '左发'
    para['sr_mod_被'] = '右发'

    freq = para['freq_主']
    para['freq'] = Freq(freq)

    # head_list = ['区段长度', '电容间隔', '电容值', '电容数', '钢轨电阻', '钢轨电感',
    #              '区段频率', '分路电阻', '道床电阻',
    #              '调整轨入最大值', '调整轨入最小值',
    #              '分路残压最大值', '最大分路残压位置',
    #              '机车信号最小值', '最小机车信号位置']

    head_list = ['区段长度', '钢轨电阻', '钢轨电感',
                 '主串频率','被串频率', '分路电阻', '道床电阻',
                 '分路间隔','电缆长度', '主串电平级', '相对位置',
                 '调整轨入最大值', '最小机车信号位置']

    # excel_list = []
    turnout_list = []

    excel_data = []
    excel_i_trk = []
    excel_i_sht = []

    freq_list = [1700, 2000, 2300, 2600]
    for frq_zhu in [1700, 2000, 2300, 2600]:
        for frq_chuan in [1700, 2000, 2300, 2600]:
            # for length in range(700, 700, -50):
            length = 700
            for offset in range(1400, 650, -50):

                length = 700
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                para['freq_主'] = frq_zhu
                para['freq_被'] = frq_chuan
                freq = para['freq_主']
                para['freq'] = Freq(freq)

                # 数据表0
                data = dict()
                for key in head_list:
                    data[key] = None

                data['相对位置'] = para['offset'] = offset
                # length = 600
                data['区段长度'] = para['length'] = length
                data['钢轨电阻'] = round(para['Trk_z'].rlc_s[freq][0], 10)
                data['钢轨电感'] = round(para['Trk_z'].rlc_s[freq][1], 10)
                data['电缆长度'] = para['cab_len'] = cab_len = 10
                data['主串频率'] = freq
                data['被串频率'] = para['freq_被']
                data['分路电阻'] = para['Rsht_z'] = r_sht = 0.01
                data['道床电阻'] = rd = 2
                data['最小机车信号位置'] = '-'
                data['主串电平级'] = 3

                para['Cable_R'].value = 43
                para['Rd'].value = 10000

                # 调整计算
                md = TestModel(turnout_list=turnout_list, parameter=para)
                m1 = MainModel(md.lg, md=md)

                data1 = md.lg['线路3']['地面']['区段1']['右调谐单元']['1接收器']['U'].value_c
                data['调整轨入最大值'] = data1

                # 分路计算
                i_trk_list = list()
                i_sht_list = list()

                data['分路间隔'] = interval = 2

                sht_length = length
                # posi_list = np.arange(-14.5, (sht_length + 14.5), interval)
                posi_list = np.arange(-14.5, (sht_length - 14.5), interval)
                for posi_tr in posi_list:
                    md = TestModel(turnout_list=turnout_list, parameter=para)
                    md.add_train()
                    md.train.posi_rlt = posi_tr
                    md.train.set_posi_abs(0)
                    m1 = MainModel(md.lg, md=md)
                    print(md.train.posi_abs)
                    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    i_sht = md.lg['线路4']['列车1']['分路电阻1']['I'].value_c
                    if m1['线路4'].node_dict[posi_tr].r_track is not None:
                        i_trk = m1['线路4'].node_dict[posi_tr].r_track['I1'].value_c
                    else:
                        print('###')
                        i_trk = 0.0
                    i_trk_list.append(i_trk)
                    i_sht_list.append(i_sht)
                print(i_sht_list)

                data_row = [data[key] for key in head_list]
                excel_data.append(data_row)
                excel_i_trk.append(i_trk_list)
                excel_i_sht.append(i_sht_list)

    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    df_i_trk = pd.DataFrame(excel_i_trk)
    df_i_sht = pd.DataFrame(excel_i_sht)

    df_data = pd.DataFrame(excel_data, columns=head_list)

    # 保存到本地excel
    filename = '../Output/邻线干扰2000A' + timestamp + '.xlsx'
    with pd.ExcelWriter(filename) as writer:
        df_i_trk.to_excel(writer, sheet_name="钢轨电流", index=False)
        df_i_sht.to_excel(writer, sheet_name="分路电流", index=False)
        df_data.to_excel(writer, sheet_name="调整状态", index=False)
        pass