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

        # sg3 = SectionGroup(name_base='地面', posi=0, m_num=1, freq1=freq,
        #                    m_length=[length],
        #                    j_length=[22, 22],
        #                    m_type=['2000A_Belarus'],
        #                    c_num=[c_num],
        #                    parameter=parameter)

        self.train = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train.posi_rlt = 58

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

        self.l3 = l3

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
    df = pd.read_excel('../Input/襄阳动车所输入参数_有道岔版.xlsx', header=None)

    localtime = time.localtime()
    timestamp = time.strftime("%Y%m%d%H%M%S", localtime)
    print(time.strftime("%Y-%m-%d %H:%M:%S", localtime))

    sec_num = 79*2
    excel_list = []
    excel_list1 = []

    head_list = ['区段名称', '区段长度', '区段频率', '发送电平级',
                 '电缆长度', '电容值', '电容数', '道岔数量',
                 '钢轨电阻', '钢轨电感', '道床电阻',
                 '理想电压', '功出电压', '功出电流',
                 '真轨入最大值', '真轨入最小值',
                 '轨入最大值', '轨入最小值',
                 '发送轨面最大值', '发送轨面最小值',
                 '接收轨面最大值', '接收轨面最小值']
    for num in range(sec_num):
        data = dict()

        output = 8 * [0]
        row = num + 2
        data['区段名称'] = df.loc[row, 2]
        data['区段频率'] = freq = df.loc[row, 3]
        data['区段长度'] = length = df.loc[row, 4]
        data['道岔数量'] = turnout_num = df.loc[row, 5]
        turnout_list = []
        if turnout_num > 0:
            p1 = length - df.loc[row, 6]
            p2 = length - df.loc[row, 7]
            turnout_list.append((p1, p2))
        if turnout_num == 2:
            p1 = length - df.loc[row, 9]
            p2 = length - df.loc[row, 10]
            turnout_list.append((p1, p2))

        data['电容数'] = c_num = df.loc[row, 19]
        data['发送电平级'] = level = df.loc[row, 20]
        cab_len = df.loc[row, 14]
        data['电缆长度'] = round(cab_len, 10)

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

        data['理想电压'] =  md.lg['线路3']['地面']['区段1']['左调谐单元']['1发送器']['1电压源']['U'].value_c
        data['功出电压'] =  md.lg['线路3']['地面']['区段1']['左调谐单元']['1发送器']['2内阻']['U2'].value_c
        data['功出电流'] =  md.lg['线路3']['地面']['区段1']['左调谐单元']['1发送器']['2内阻']['I2'].value_c

        para = md.parameter
        data['钢轨电阻'] = round(para['Trk_z'].rlc_s[freq][0], 10)
        data['钢轨电感'] = round(para['Trk_z'].rlc_s[freq][1], 10)
        data['电容值'] = round(para['Ccmp_z'].rlc_s[freq][2], 10)

        data['真轨入最大值'] = output[1] = v_rcv_true
        data['轨入最大值'] = output[3] = v_rcv
        data['发送轨面最大值'] = output[5] = v_fs_guimian
        data['接收轨面最大值'] = output[7] = v_js_guimian

        excel_list1.append(get_output(md.lg))

        # row = 2 * num + 2
        freq = df.loc[row, 3]
        length = df.loc[row, 4]
        c_num = df.loc[row, 19]
        level = df.loc[row, 20]
        cab_len = df.loc[row, 14]
        data['道床电阻'] = r_d = df.loc[row, 16]

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

        data['真轨入最小值'] = output[0] = v_rcv_true
        data['轨入最小值'] = output[2] = v_rcv
        data['发送轨面最小值'] = output[4] = v_fs_guimian
        data['接收轨面最小值'] = output[6] = v_js_guimian

        row_list = [data[key] for key in head_list]
        excel_list.append(row_list)
        # excel_list.append(output)
        # excel_list1.append(get_output(md.lg))

        print('xxx', row_list)

    df = pd.DataFrame(excel_list, columns=head_list)

    # df = pd.DataFrame(excel_list1, columns=['电源', '功出电压', '功出电流',
    #                                         '发送设备侧', '发送防雷侧', '发送电缆侧', '发送钢轨侧',
    #                                         '接收钢轨侧', '接收电缆侧', '接收防雷侧', '接收设备侧',
    #                                         '隔离盒', '真轨入'])

    # 保存到本地excel
    filename = '../Output/襄阳动车所_调整表_有岔计算_' + timestamp + '.xlsx'
    with pd.ExcelWriter(filename) as writer:
        df.to_excel(writer, sheet_name="调整表", index=False)
        pass
