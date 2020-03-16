from src.Model.MainModel import *
from src.Model.ModelParameter import *
from src.Model.PreModel import *
from src.FrequencyType import Freq
from src.Method import *
from src.Data2Excel import *

import pandas as pd
import time
import itertools
import os
import sys

pd.set_option('display.max_columns', None)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.width', None)

if __name__ == '__main__':
    df_input = pd.read_excel('邻线干扰参数输入.xlsx')
    # df_input = pd.read_excel('邻线干扰参数输入_拆电容.xlsx')

    localtime = time.localtime()
    timestamp = time.strftime("%Y%m%d%H%M%S", localtime)
    print(time.strftime("%Y-%m-%d %H:%M:%S", localtime))

    num_len = len(list(df_input['序号']))

    work_path = os.getcwd()
    para = ModelParameter(workpath=work_path)

    # 钢轨阻抗
    trk_2000A_21 = ImpedanceMultiFreq()
    trk_2000A_21.rlc_s = {
        1700: [1.177, 1.314e-3, None],
        2000: [1.306, 1.304e-3, None],
        2300: [1.435, 1.297e-3, None],
        2600: [1.558, 1.291e-3, None]}

    para['Trk_z'].rlc_s = trk_2000A_21.rlc_s

    para['Ccmp_z_change_zhu'] = ImpedanceMultiFreq()
    para['Ccmp_z_change_chuan'] = ImpedanceMultiFreq()

    para['TB_引接线_有砟'] = ImpedanceMultiFreq()
    para['TB_引接线_有砟'].z = {
        1700: (8.33 + 31.4j)*1e-3,
        2000: (10.11 + 35.2j)*1e-3,
        2300: (11.88 + 39.0j)*1e-3,
        2600: (13.60 + 42.6j)*1e-3}

    z_tb_2600_2000 = para['TB'][2600][2000].z

    # head_temp = ['序号', '区段长度', '耦合系数',
    #              '钢轨电阻', '钢轨电感',
    #              '主串道床电阻', '被串道床电阻',
    #              '主串频率', '被串频率',
    #              '主串电容数', '被串电容数',
    #              '主串电容值', '被串电容值',
    #              '分路电阻',
    #              '钢轨电流最大值', '最大值位置']

    head_list = ['序号', '区段长度', '耦合系数',
                 '钢轨电阻', '钢轨电感',
                 '道床电阻',
                 # '主串道床电阻', '被串道床电阻',
                 # '主串钢轨电阻', '主串钢轨电感',
                 # '被串钢轨电阻', '被串钢轨电感',
                 '主串频率', '被串频率',
                 '主串电容数', '被串电容数',
                 'TB模式',
                 '主串电容值', '被串电容值',
                 # '主串拆卸情况',
                 # '电感短路故障情况',
                 # '被串拆卸情况',
                 # '换电容位置',
                 '分路电阻',
                 # 'TB引接线阻抗',
                 '分路间隔', '电缆长度',
                 '主串电平级',
                 # '调整功出电压', '调整轨入最大值',
                 '钢轨电流最大值', '最大值位置',
                 '备注']

    # head_list = head_temp

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

    # rd_list = list(range(20, 0, -1))
    # rd_list.insert(0, 10000)

    # clist1 = [25e-6, 40e-6]
    # clist2 = [25e-6, 50e-6]
    # clist1 = [25e-6, 46e-6]
    # clist2 = [25e-6, 55e-6]
    # clist1 = [25e-6, 50e-6]
    # clist2 = [25e-6, 50e-6]
    # clist3 = [3,4,5,6,7]
    # clist4 = [3,4,5,6,7]
    # clist3 = [5]
    # clist4 = [5]
    # clist1 = [2, 1]
    # clist2 = [0]
    # clist3 = [2600]
    # clist4 = [2000]
    # clist1 = list(range(0,22,2))
    # clist2 = list(range(0,22,2))
    # clist1 = [1, 0.6]
    # clist2 = [0.15]

    freq_list = [1700, 2000, 2300, 2600]

    # clist1 = [(300, 3), (350, 3),
    #           (350, 4), (400, 4),
    #           (400, 5), (450, 5), (500, 5),
    #           (500, 6), (550, 6), (600, 6),
    #           (600, 7), (650, 7)]
    clist1 = [(650, 7)]
    clist2 = [0]

    clist3 = [2300]
    clist4 = [1700]
    # clist5 = list(range(75,126,1))
    clist5 = [[]]
    # clist6 = [[]]
    # clist5 = [[],[1],[2],[3],[4],[5]]
    clist6 = [[],[1],[2],[3],[4],[5]]
    clist6.extend(list(itertools.combinations([1, 2, 3, 4, 5], 2)))
    # clist5 = list(itertools.combinations([1, 2, 3, 4, 5], 2))
    # clist5.insert(0,)
    # clist6 = list(itertools.combinations([1, 2, 3, 4, 5], 2))
    # clist6.insert(0,[])

    # clist6 = list(itertools.combinations([1, 2, 4, 5], 2))
    # clist_temp = []
    # for temp in clist6:
    #     value1 = list(temp)
    #     value1.append(3)
    #     value2 = tuple(value1)
    #     clist_temp.append(value2)
    # clist6 = clist_temp
    # clist6.insert(0,())
    # clist = list(itertools.product(clist1, clist2, clist3, clist4))
    clist = list(itertools.product(clist1, clist2,
                                   clist3, clist4,
                                   clist5, clist6))

    columns_max = 0
    counter = 1
    for temp_temp in range(num_len):
    # for cv1, cv2, cv3, cv4, cv5, cv6 in clist:
    #     length_tt = cv1[0]
        # length_tt = 626

        # para['TB'][2600][2000].z = z_tb_2600_2000 + cv1/1000

        c_zhu = 25e-6
        c_bei = 25e-6

        # if cv1 == 2:
        #     if cv3 == 1700 or cv3 == 2000:
        #         c_zhu = 80e-6
        #     if cv4 == 1700 or cv4 == 2000:
        #         c_bei = 80e-6


        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # if getattr(sys, 'frozen', False):
        #     print(df_input[temp_temp:(temp_temp + 1)])


        # 数据表0
        data = dict()
        for key in head_list:
            data[key] = None

        # 添加数据行
        data2excel.add_row()

        # data['TB引接线阻抗'] = cv1

        #################################################################################

        data['故障情况'] = para['故障情况'] = '正常'
        # data['主串电平级'] = para['send_level'] = 5
        # data['主串电平级'] = para['send_level'] = cv1
        data['主串电平级'] = para['send_level'] = df_input['主串电平级'][temp_temp]

        data['序号'] = para['序号'] = counter
        # data['序号'] = para['序号'] = df_input['序号'][temp_temp]

        # data['区段长度'] = para['length'] = length = 626
        # data['区段长度'] = para['length'] = length = length_tt
        data['区段长度'] = para['length'] = length = df_input['区段长度(m)'][temp_temp]

        # data['耦合系数'] = para['耦合系数'] = 13
        data['耦合系数'] = para['耦合系数'] = df_input['耦合系数'][temp_temp]

        # data['主串频率'] = para['freq_主'] = freq = cv3
        data['主串频率'] = para['freq_主'] = freq = df_input['主串频率(Hz)'][temp_temp]

        # data['被串频率'] = para['freq_被'] = cv4
        data['被串频率'] = para['freq_被'] = df_input['被串频率(Hz)'][temp_temp]

        data['freq'] = para['freq'] = Freq(freq)

        # data['主串电容数'] = para['主串电容数'] = cv1[1]
        # data['主串电容数'] = para['主串电容数'] = cv3
        # data['主串电容数'] = para['主串电容数'] = df_input['主串电容数'][temp_temp]
        data['主串电容数'] = para['主串电容数'] = df_input['主串电容数(含TB)'][temp_temp]

        # data['被串电容数'] = para['被串电容数'] = cv1[1]
        # data['被串电容数'] = para['被串电容数'] = cv4
        # data['被串电容数'] = para['被串电容数'] = df_input['被串电容数'][temp_temp]
        data['被串电容数'] = para['被串电容数'] = df_input['被串电容数(含TB)'][temp_temp]

        # data['主串电容值'] = c_value = 25e-6
        data['主串电容值'] = c_value = c_zhu
        # data['主串电容值'] = c_value = df_input['主串电容值'][temp_temp]
        para['Ccmp_z_change_zhu'].rlc_s = {
            1700: [10e-3, None, c_value],
            2000: [10e-3, None, c_value],
            2300: [10e-3, None, c_value],
            2600: [10e-3, None, c_value]}

        # data['被串电容值'] = c_value = 25e-6
        data['被串电容值'] = c_value = c_bei
        # data['被串电容值'] = '抑制装置'
        # data['被串电容值'] = c_value = df_input['被串电容值'][temp_temp]
        para['Ccmp_z_change_chuan'].rlc_s = {
            1700: [10e-3, None, c_value],
            2000: [10e-3, None, c_value],
            2300: [10e-3, None, c_value],
            2600: [10e-3, None, c_value]}

        # para['Ccmp_z_change_chuan'].rlc_s = {
        #     1700: [10e-3, 390e-6, 11.9e-6],
        #     2000: [10e-3, 390e-6, 11.9e-6],
        #     2300: [10e-3, 390e-6, 11.9e-6],
        #     2600: [10e-3, 390e-6, 11.9e-6]}

        # para['抑制装置电感短路'] = ImpedanceMultiFreq()
        # para['抑制装置电感短路'].rlc_s = {
        #     1700: [10e-3, None, 11.9e-6],
        #     2000: [10e-3, None, 11.9e-6],
        #     2300: [10e-3, None, 11.9e-6],
        #     2600: [10e-3, None, 11.9e-6]}

        # data['换电容位置'] = para['换电容位置'] = cv2
        data['换电容位置'] = para['换电容位置'] = 0


        # data['道床电阻'] = rd_temp = 10000
        # data['道床电阻'] = rd_temp = cv1
        data['道床电阻'] = rd_temp = df_input['道床电阻(Ω·km)'][temp_temp]

        data['备注'] = '电容数为包含TB的电容数'

        #################################################################################

        data['主串道床电阻'] = data['道床电阻']
        # data['主串道床电阻'] = df_input['主串道床电阻'][temp_temp]
        para['主串道床电阻'] = Constant(data['主串道床电阻'])

        data['被串道床电阻'] = data['道床电阻']
        # data['被串道床电阻'] = df_input['被串道床电阻'][temp_temp]
        para['被串道床电阻'] = Constant(data['被串道床电阻'])

        # # data['主串钢轨电阻'] = cv3
        # data['主串钢轨电阻'] = df_input['主串钢轨电阻'][temp_temp]
        #
        # # data['主串钢轨电感'] = cv4
        # data['主串钢轨电感'] = df_input['主串钢轨电感'][temp_temp]
        #
        # # data['被串钢轨电阻'] = 1.558
        # data['被串钢轨电阻'] = df_input['被串钢轨电阻'][temp_temp]
        #
        # # data['被串钢轨电感'] = 1.291e-3
        # data['被串钢轨电感'] = df_input['被串钢轨电感'][temp_temp]
        #
        # para['主串钢轨阻抗'] = ImpedanceMultiFreq()
        # para['主串钢轨阻抗'].rlc_s = \
        #     {data['主串频率']: [data['主串钢轨电阻'], data['主串钢轨电感'], None]}
        # para['被串钢轨阻抗'] = ImpedanceMultiFreq()
        # para['被串钢轨阻抗'].rlc_s = \
        #     {data['主串频率']: [data['被串钢轨电阻'], data['被串钢轨电感'], None]}

        para['主串钢轨阻抗'] = para['Trk_z']
        para['被串钢轨阻抗'] = para['Trk_z']
        #################################################################################

        data['TB模式'] = flag_tb = df_input['TB模式'][temp_temp]
        if flag_tb == '双端TB':
            para['TB模式'] = '双'
        elif flag_tb == '发送端单TB':
            para['TB模式'] = '右'
        elif flag_tb == '接收端单TB':
            para['TB模式'] = '左'
        elif flag_tb == '无TB':
            para['TB模式'] = '无'
        else:
            raise KeyboardInterrupt('TB模式错误')

        #################################################################################

        data['主串发送器位置'] = para['sr_mod_主'] = '右发'
        data['被串发送器位置'] = para['sr_mod_被'] = '右发'

        # data['主串拆卸情况'] = para['主串拆卸情况'] = cv5
        data['主串拆卸情况'] = para['主串拆卸情况'] = []
        # data_str = str(df_input['主串拆卸情况'][temp_temp])
        # data['主串拆卸情况'] = para['主串拆卸情况'] = eval(df_input['主串拆卸情况'][temp_temp])

        # data['被串拆卸情况'] = para['被串拆卸情况'] = cv6
        # data['电感短路故障情况'] = data['被串拆卸情况']
        data['被串拆卸情况'] = para['被串拆卸情况'] = []
        # data_str = str(df_input['被串拆卸情况'][temp_temp])
        # data['被串拆卸情况'] = para['被串拆卸情况'] = eval(df_input['被串拆卸情况'][temp_temp])

        data['相对位置'] = para['offset'] = 0

        data['钢轨电阻'] = round(para['Trk_z'].rlc_s[freq][0], 10)
        data['钢轨电感'] = round(para['Trk_z'].rlc_s[freq][1], 10)

        data['电缆长度'] = para['cab_len'] = cab_len = 10
        data['分路电阻'] = para['Rsht_z'] = 0.0000001
        # data['分路电阻'] = para['Rsht_z'] = cv2

        # data['特殊位置'] = para['special_point'] = list(np.linspace(0,length + length, 21))
        data['特殊位置'] = para['special_point'] = []
        data['节点选取模式'] = para['节点选取模式'] = '特殊'

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

        data['机车信号感应系数'] = \
            str(para['机车信号比例V']) + '/' + str(para['机车信号比例I'][para['freq_主']])
        para['机车信号系数值'] = para['机车信号比例V'] / para['机车信号比例I'][para['freq_主']]

        data['电源电压'] = para['pwr_v_flg'] = '最大'
        # data['电源电压'] = para['pwr_v_flg'] = df_input['电源电压'][temp_temp]

        # 调整计算最大
        para['Rd'].value = data['道床电阻']
        para['pwr_v_flg'] = data['电源电压']

        para['Cable_R'].value = data['电缆电阻最小(Ω/km)']
        para['Cable_C'].value = data['电缆电容最大(F/km)']

        # md = PreModelAdjust(turnout_list=turnout_list, parameter=para)
        # md = PreModel_25Hz_coding(turnout_list=turnout_list, parameter=para)
        # m1 = MainModel(md.lg, md=md)

        # data1 = md.lg['线路3']['地面']['区段1']['左调谐单元']['1接收器']['U'].value_c
        # data['调整轨入最大值'] = data1
        #
        # data1 = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['U2'].value_c
        # data['调整功出电压'] = data1

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

        # data2excel.add_row()
        data['分路间隔'] = interval = 1
        posi_list = np.arange(length, -1, -interval)

        # # 轨面电压计算
        # para['Rsht_z'] = 100000
        # for posi_zhu in posi_list:
        #     md = PreModelAdjust(turnout_list=turnout_list, parameter=para)
        #     md.add_train()
        #     md.train1.posi_rlt = posi_zhu
        #     md.train1.set_posi_abs(0)
        #     m1 = MainModel(md.lg, md=md)
        #     v_sht_zhu = md.lg['线路3']['列车1']['分路电阻1']['U'].value_c
        #     data2excel.add_data(sheet_name="主串轨面电压", data1=v_sht_zhu)

        # 分路计算
        para['Rsht_z'] = data['分路电阻']
        for posi_bei in posi_list:
        # for posi_zhu in posi_list:
            md = PreModel(turnout_list=turnout_list, parameter=para)
            # md = PreModel_25Hz_coding(turnout_list=turnout_list, parameter=para)
            md.add_train()
            # posi_bei = (626-335)
            md.train1.posi_rlt = posi_bei
            md.train1.set_posi_abs(0)

            posi_zhu = posi_bei
            md.train2.posi_rlt = posi_zhu
            md.train2.set_posi_abs(0)

            # posi_rrr = length - posi_tr + length
            # md.train3.posi_rlt = posi_rrr
            # md.train3.set_posi_abs(0)
            # md.train4.posi_rlt = posi_rrr
            # md.train4.set_posi_abs(0)

            m1 = MainModel(md.lg, md=md)

            i_sht_zhu = md.lg['线路3']['列车2']['分路电阻1']['I'].value_c
            i_sht_bei = md.lg['线路4']['列车1']['分路电阻1']['I'].value_c
            i_trk_zhu = get_i_trk(line=m1['线路3'], posi=posi_zhu, direct='右')
            i_trk_bei = get_i_trk(line=m1['线路4'], posi=posi_bei, direct='右')

            # i_source_fs = m1['线路3'].node_dict[length].l_track['I2'].value
            # i_source_fs = md.lg['线路3']['地面']['区段1']['右调谐单元'].md_list[-1]['I2'].value
            # v_load_fs = m1['线路4'].node_dict[length].l_track['U2'].value

            # z_mm = np.inf if i_source_fs == 0 else v_load_fs / i_source_fs
            # z_mm = v_load_fs / i_source_fs
            # z_mm_abs = abs(z_mm)
            # co_mutal = z_mm_abs / 2 / np.pi / para['freq_主'] / (length-posi_tr)*1000 * 1e6 * 2
            # co_mutal = round(co_mutal, 2)

            # i_TB = md.lg['线路4']['地面']['区段1']['TB2']['I'].value_c
            # i_ca = md.lg['线路4']['地面']['区段1']['右调谐单元'].md_list[-1]['I2'].value_c
            # i_C1 = md.lg['线路4']['地面']['区段1']['C5']['I'].value_c
            # i_C2 = md.lg['线路4']['地面']['区段1']['C4']['I'].value_c
            # i_C3 = md.lg['线路4']['地面']['区段1']['C3']['I'].value_c
            # i_C4 = md.lg['线路4']['地面']['区段1']['C2']['I'].value_c
            # i_C5 = md.lg['线路4']['地面']['区段1']['C1']['I'].value_c

            data2excel.add_data(sheet_name="主串钢轨电流", data1=i_trk_zhu)
            data2excel.add_data(sheet_name="被串钢轨电流", data1=i_trk_bei)
            data2excel.add_data(sheet_name="被串分路电流", data1=i_sht_bei)
            # data2excel.add_data(sheet_name="实测阻抗", data1=z_mm)
            # data2excel.add_data(sheet_name="阻抗模值", data1=z_mm_abs)
            # data2excel.add_data(sheet_name="耦合系数", data1=co_mutal)

        if length > columns_max:
            columns_max = length

        i_trk_list = data2excel.data_dict["被串钢轨电流"][-1]
        i_sht_list = data2excel.data_dict["被串分路电流"][-1]

        data['钢轨电流最大值'] = max(i_trk_list)
        data['最大值位置'] = i_trk_list.index(max(i_trk_list))

        if not getattr(sys, 'frozen', False):
            print(data.keys())
            print(data.values())
            print(i_sht_list)

        data_row = [data[key] for key in head_list]
        excel_data.append(data_row)
        counter += 1

    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    posi_header = list(range(columns_max+1))
    posi_header[0] = '发送端'

    df_data = pd.DataFrame(excel_data, columns=head_list)


    # 保存到本地excel
    # filename = '仿真输出'
    filename = '仿真输出_拆电容'
    # filepath = 'src/Output/'+ filename + timestamp + '.xlsx'
    filepath = ''+ filename + '_' + timestamp + '.xlsx'
    with pd.ExcelWriter(filepath) as writer:
        df_input.to_excel(writer, sheet_name="参数设置", index=False)
        df_data.to_excel(writer, sheet_name="数据输出", index=False)

        names = ["被串钢轨电流", "被串分路电流",
                 "主串钢轨电流",
                 # "主串轨面电压"
                 ]


        # data2excel.write2excel(sheet_names=names, header=None, writer1=writer)
        data2excel.write2excel(sheet_names=names, header=posi_header, writer1=writer)

        pass