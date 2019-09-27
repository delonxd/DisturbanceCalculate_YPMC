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
        # 轨道电路初始化
        # sg1 = SectionGroup(name_base='地面', posi=0, m_num=1, freq1=2600,
        #                    m_length=[509, 389, 320],
        #                    j_length=[29, 29, 29, 29],
        #                    m_type=['2000A', '2000A', '2000A'],
        #                    c_num=[6, 6, 5],
        #                    parameter=parameter)

        # sg2 = SectionGroup(name_base='地面', posi=0, m_num=2, freq1=1700,
        #                    m_length=[480, 200, 320],
        #                    j_length=[29, 29, 29, 29],
        #                    m_type=['2000A', '2000A', '2000A'],
        #                    c_num=[8, 6, 5],
        #                    parameter=parameter)

        sg3 = SectionGroup(name_base='地面', posi=0, m_num=1, freq1=freq,
                           m_length=[length],
                           j_length=[0, 0],
                           m_type=['2000A_YPMC'],
                           c_num=[c_num],
                           parameter=parameter)

        # train1 = Train(name_base='列车1', posi_abs=0, parameter=parameter)

        # 生成线路
        # l1 = Line(name_base='线路1', sec_group=sg1, train=train1,
        #           parameter=parameter)
        # l1 = Line(name_base='线路1', sec_group=sg1,
        #           parameter=parameter)
        # l2 = Line(name_base='线路2', sec_group=sg2,
        #           parameter=parameter)

        l3 = Line(name_base='线路3', sec_group=sg3,
                  parameter=parameter)
        self.lg = LineGroup(l3, name_base='线路组')

        for i in range(len(turnout_list)):
            name = '道岔' + str(i+1)
            posi1, posi2 = turnout_list[i]
            turnout = Turnout(name_base=name, parameter=parameter,
                              main_line=l3, posi1=posi1, posi2=posi2)
            self.lg.add_turnout(turnout)

        self.lg.refresh()

        # 建立模型
        # self.model = MainModel(self.lg)

        # self.section_group1 = sg1
        # self.section_group2 = sg2
        self.section_group3 = sg3

        # self.train1 = train1
        # self.line1 = l1
        # self.line2 = l2
        # self.line3 = l3


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
    df = pd.read_excel('../Input/实验室验证输入参数.xlsx', header=None)

    localtime = time.localtime()
    timestamp = time.strftime("%Y%m%d%H%M%S", localtime)
    print(time.strftime("%Y-%m-%d %H:%M:%S", localtime))

    sec_num = 3
    excel_list = []
    excel_list1 = []

    for num in range(sec_num):
        output = 8 * [0]
        row = 2 * num + 2
        freq = df.loc[row, 3]
        length = df.loc[row, 4]
        turnout_num = df.loc[row, 5]
        turnout_list = []
        if turnout_num > 0:
            p1 = length - df.loc[row, 6]
            p2 = length - df.loc[row, 7]
            turnout_list.append((p1, p2))
        if turnout_num == 2:
            p1 = length - df.loc[row, 9]
            p2 = length - df.loc[row, 10]
            turnout_list.append((p1, p2))

        c_num = df.loc[row, 19]
        level = df.loc[row, 20]
        cab_len = df.loc[row, 14]

        md = TestModel(freq=freq,
                       length=length,
                       c_num=c_num,
                       level=level,
                       rd=10000,
                       r_cable=43,
                       cab_len=cab_len,
                       turnout_list=turnout_list)
        m1 = MainModel(md.lg, md=md)
        v_rcv = md.lg['线路3']['地面']['区段1']['右调谐单元']['1接收器']['2隔离元件']['U2'].value_c
        v_rcv_true = md.lg['线路3']['地面']['区段1']['右调谐单元']['1接收器']['0接收器']['U'].value_c
        v_fs_guimian = md.lg['线路3']['地面']['区段1']['左调谐单元']['6CA']['U2'].value_c
        v_js_guimian = md.lg['线路3']['地面']['区段1']['右调谐单元']['6CA']['U2'].value_c

        output[1] = v_rcv_true
        output[3] = v_rcv
        output[5] = v_fs_guimian
        output[7] = v_js_guimian

        excel_list1.append(get_output(md.lg))

        row = 2 * num + 3
        freq = df.loc[row, 3]
        length = df.loc[row, 4]
        c_num = df.loc[row, 19]
        level = df.loc[row, 20]
        cab_len = df.loc[row, 14]
        r_d = df.loc[row, 16]

        md = TestModel(freq=freq,
                       length=length,
                       c_num=c_num,
                       level=level,
                       rd=r_d,
                       r_cable=47,
                       cab_len=cab_len,
                       turnout_list=turnout_list)
        m1 = MainModel(md.lg, md=md)
        v_rcv = md.lg['线路3']['地面']['区段1']['右调谐单元']['1接收器']['2隔离元件']['U2'].value_c
        v_rcv_true = md.lg['线路3']['地面']['区段1']['右调谐单元']['1接收器']['0接收器']['U'].value_c
        v_fs_guimian = md.lg['线路3']['地面']['区段1']['左调谐单元']['6CA']['U2'].value_c
        v_js_guimian = md.lg['线路3']['地面']['区段1']['右调谐单元']['6CA']['U2'].value_c

        output[0] = v_rcv_true
        output[2] = v_rcv
        output[4] = v_fs_guimian
        output[6] = v_js_guimian

        excel_list.append(output)
        excel_list1.append(get_output(md.lg))
        print('xxx', output)

    # df = pd.DataFrame(excel_list, columns=['真轨入最小值(V)', '真轨入最大值(V)',
    #                                        '轨入最小值(V)', '轨入最大值(V)',
    #                                        '发送轨面电压最小值', '发送轨面电压最大值',
    #                                        '接收轨面电压最小值', '接收轨面电压最大值'])

    df = pd.DataFrame(excel_list1, columns=['电源', '功出电压', '功出电流',
                                            '发送设备侧', '发送防雷侧', '发送电缆侧', '发送钢轨侧',
                                            '接收钢轨侧', '接收电缆侧', '接收防雷侧', '接收设备侧',
                                            '隔离盒', '真轨入'])

    # 保存到本地excel
    filename = '../Output/实验室验证_调整表_有岔计算_' + timestamp + '.xlsx'
    with pd.ExcelWriter(filename) as writer:
        df.to_excel(writer, sheet_name="调整表", index=False)
        pass
