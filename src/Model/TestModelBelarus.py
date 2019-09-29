from src.TrackCircuitElement.SectionGroup import *
from src.TrackCircuitElement.Train import *
from src.TrackCircuitElement.Line import *
from src.TrackCircuitElement.LineGroup import *
from src.Model.MainModel import *
from src.Model.ModelParameter import *

import pandas as pd
import time


class TestModel:
    def __init__(self, freq, length, c_num, level, rd, r_cable, cab_len, turnout_list):
        # 导入参数
        parameter = ModelParameter()
        parameter['freq'] = freq
        parameter['length'] = length
        parameter['c_num'] = c_num
        parameter['Cable_R'] = r_cable
        parameter['cab_len'] = cab_len
        parameter['Rd'] = rd
        parameter['level'] = level

        self.parameter = parameter
        self.train = Train(name_base='列车1', posi=0, parameter=parameter)

        # 轨道电路初始化
        sg3 = SectionGroup(name_base='地面', posi=0, m_num=1, freq1=freq,
                           m_length=[length],
                           j_length=[22, 22],
                           m_type=['2000A_Belarus'],
                           c_num=[c_num],
                           parameter=parameter)
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

    level = 3
    cab_len = 10
    turnout_list = []

    # freq = fq_list[0]
    # length = len_list[0]
    # c_num = c_num_list[0]

    excel_list = []
    for freq in fq_list:
        for length, c_num in zip(len_list, c_num_list):
            data = dict()
            data['区段长度'] = length
            data['电容数'] = c_num
            data['区段频率'] = freq
            data['分路电阻'] = rd = 2
            data['道床电阻'] = r_sht = 0.15

            #####################################################################################
            # 调整最有利状态
            md = TestModel(freq=freq, length=length, c_num=c_num,
                           level=level, rd=10000, r_cable=43,
                           cab_len=cab_len, turnout_list=turnout_list)
            m1 = MainModel(md.lg, md=md)
            data['调整轨入最大值'] \
                = md.lg['线路3']['地面']['区段1']['右调谐单元']['1接收器']['U'].value_c

            #####################################################################################
            # 调整最不利状态
            md.parameter['Cable_R'] = 47
            md.parameter['Rd'] = rd
            m1 = MainModel(md.lg, md=md)
            data['调整轨入最小值'] \
                = md.lg['线路3']['地面']['区段1']['右调谐单元']['1接收器']['U'].value_c

            #####################################################################################
            # 分路最不利状态
            md.add_train()
            posi_list = range(11, (length-11), 1)
            md.parameter['Cable_R'] = 43
            md.parameter['Rd'] = 10000
            md.parameter['Rsht_z'] = r_sht
            v_rcv_list = []
            for posi_tr in posi_list:
                md.train.posi_rlt = posi_tr
                md.train.set_posi_abs(0)
                m1 = MainModel(md.lg, md=md)

                v_rcv = md.lg['线路3']['地面']['区段1']['右调谐单元']['1接收器']['U'].value_c
                v_rcv_list.append(v_rcv)
            data['分路残压最大值'] = max(v_rcv_list)

            #####################################################################################
            # 机车信号最不利状态
            md.add_train()
            posi_list = range(11, (length-11), 1)
            md.parameter['Cable_R'] = 47
            md.parameter['Rd'] = rd
            md.parameter['Rsht_z'] = r_sht
            i_trk_list = []
            for posi_tr in posi_list:
                md.train.posi_rlt = posi_tr
                md.train.set_posi_abs(0)
                m1 = MainModel(md.lg, md=md)
                if m1['线路3'].node_dict[posi_tr].l_track is not None:
                    i_trk = m1['线路3'].node_dict[posi_tr].l_track['I2'].value_c
                else:
                    i_trk = None
                i_trk_list.append(i_trk)
            data['机车信号最小值'] = min(i_trk_list)

            #####################################################################################
            row_list = [data['区段长度'],
                        data['电容数'],
                        data['区段频率'],
                        data['分路电阻'],
                        data['道床电阻'],
                        data['调整轨入最大值'],
                        data['调整轨入最小值'],
                        data['分路残压最大值'],
                        data['机车信号最小值']]
            excel_list.append(row_list)
            print(row_list)

    # df = pd.DataFrame(excel_list, columns=['真轨入最小值(V)', '真轨入最大值(V)',
    #                                        '轨入最小值(V)', '轨入最大值(V)',
    #                                        '发送轨面电压最小值', '发送轨面电压最大值',
    #                                        '接收轨面电压最小值', '接收轨面电压最大值'])

    df = pd.DataFrame(excel_list, columns=['区段长度', '电容数', '区段频率', '分路电阻', '道床电阻',
                                           '调整轨入最大值', '调整轨入最小值',
                                           '分路残压最大值', '机车信号最小值'])

    # 保存到本地excel
    filename = '../Output/实验室验证_调整表_有岔计算_' + timestamp + '.xlsx'
    with pd.ExcelWriter(filename) as writer:
        df.to_excel(writer, sheet_name="调整表", index=False)
        pass
