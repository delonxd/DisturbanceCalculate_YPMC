from src.Model.MainModel import *
from src.Model.ModelParameter import *
from src.Model.PreModel import *
from src.FrequencyType import Freq
from src.ConstantType import *
from src.Method import *
from src.Data2Excel import *

import pandas as pd
import time
import itertools
import os
import sys

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', True)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.width', 180)

if __name__ == '__main__':

    #################################################################################

    # 参数输入
    # df_input = pd.read_excel('邻线干扰参数输入_v0.3.1.xlsx')
    # df_input = pd.read_excel('邻线干扰参数输入_拆电容.xlsx')
    df_input = pd.read_excel('邻线干扰参数输入_电码化.xlsx')
    # df_input = pd.read_excel('邻线干扰参数输入_v0.4.xlsx')

    df_input = df_input.where(df_input.notnull(), None)
    num_len = len(list(df_input['序号']))

    #################################################################################

    # 获取时间戳
    localtime = time.localtime()
    timestamp = time.strftime("%Y%m%d%H%M%S", localtime)
    print(time.strftime("%Y-%m-%d %H:%M:%S", localtime))

    #################################################################################

    # 初始化变量
    work_path = os.getcwd()
    para = ModelParameter(workpath=work_path)

    # 钢轨阻抗
    trk_2000A_21 = ImpedanceMultiFreq()
    trk_2000A_21.rlc_s = {
        1700: [1.177, 1.314e-3, None],
        2000: [1.306, 1.304e-3, None],
        2300: [1.435, 1.297e-3, None],
        2600: [1.558, 1.291e-3, None]}

    # trk_2000A_21.rlc_s = {
    #     1700: [1.59, 1.34e-3, None],
    #     2000: [1.72, 1.33e-3, None],
    #     2300: [1.86, 1.32e-3, None],
    #     2600: [2.00, 1.31e-3, None]}


    # trk_2000A_21.rlc_s = {
    #     1700: [1.80, 1.18e-3, None],
    #     2000: [1.98, 1.17e-3, None],
    #     2300: [2.16, 1.16e-3, None],
    #     2600: [2.33, 1.15e-3, None]}

    para['Trk_z'].rlc_s = trk_2000A_21.rlc_s

    para['Ccmp_z_change_zhu'] = ImpedanceMultiFreq()
    para['Ccmp_z_change_chuan'] = ImpedanceMultiFreq()

    para['TB_引接线_有砟'] = ImpedanceMultiFreq()
    para['TB_引接线_有砟'].z = {
        1700: (8.33 + 31.4j)*1e-3,
        2000: (10.11 + 35.2j)*1e-3,
        2300: (11.88 + 39.0j)*1e-3,
        2600: (13.60 + 42.6j)*1e-3}

    # z_tb_2600_2000 = para['TB'][2600][2000].z

    #################################################################################

    # 获取表头

    # head_list = [
    #     '序号',
    #     '区段长度',
    #     # '主串区段长度', '被串区段长度',
    #     # '区段实际长度',
    #     # '发送接收长度',
    #     '耦合系数',
    #     '钢轨电阻', '钢轨电感',
    #     # '道床电阻',
    #     '主串道床电阻', '被串道床电阻',
    #     # '主串钢轨电阻', '主串钢轨电感',
    #     # '被串钢轨电阻', '被串钢轨电感',
    #     '主串频率', '被串频率',
    #     '主串电容数', '被串电容数',
    #     # 'TB模式',
    #     '主串电容值', '被串电容值',
    #     '主串拆卸情况', '被串拆卸情况',
    #     # '电感短路故障情况',
    #     # '换电容位置',
    #     '分路电阻',
    #     # 'TB引接线阻抗',
    #     '分路间隔', '电缆长度',
    #     '主串电平级',
    #     '电源电压',
    #     # '调整功出电压', '调整轨入最大值',
    #     '钢轨电流最大值', '最大值位置',
    #     # "SVA'互感",
    #     # '主串出口电流', '主串入口电流',
    #     '备注'
    # ]

    # head_list = [
    #     '序号',
    #     '备注',
    #
    #     '主串区段长度(m)', '被串区段长度(m)',
    #
    #     '钢轨电阻(Ω/km)', '钢轨电感(H/km)',
    #
    #     '耦合系数',
    #     '主串频率(Hz)', '被串频率(Hz)',
    #     '主串道床电阻(Ω·km)', '被串道床电阻(Ω·km)',
    #     '主串电容数(含TB)', '被串电容数(含TB)',
    #     '主串电容值(μF)', '被串电容值(μF)',
    #     '主串拆卸情况', '被串拆卸情况',
    #
    #     '分路电阻(Ω)',
    #     '分路间隔(m)',
    #     '电缆长度(km)',
    #
    #     '主串电平级',
    #     '发码继电器状态',
    #
    #     # '调整电阻(Ω)', '调整电感(H)', '调整电容(F)',
    #     # '调整RLC模式',
    #     #
    #     # 'NGL-C1(μF)',
    #     #
    #     # 'WGL-C1(μF)',
    #     # 'WGL-C2(μF)',
    #     # 'WGL-L1-R(Ω)', 'WGL-L1-L(H)',
    #     # 'WGL-L2-R(Ω)', 'WGL-L2-L(mH)',
    #     #
    #     # 'WGL-BPM变比',
    #     # '扼流变压器变比',
    #     #
    #     # 'BE-Rm(Ω)', 'BE-Lm(H)',
    #
    #     '被串最大干扰电流(A)', '被串最大干扰位置(m)',
    #     '主串出口电流(A)', '主串入口电流(A)',
    # ]

    head_list = [
        '序号',
        '备注',

        '主串区段长度(m)', '被串区段长度(m)',

        '钢轨电阻(Ω/km)', '钢轨电感(H/km)',

        '耦合系数',
        '主串频率(Hz)', '被串频率(Hz)',
        '主串道床电阻(Ω·km)', '被串道床电阻(Ω·km)',
        '主串电容数(含TB)', '被串电容数(含TB)',
        '主串电容值(μF)', '被串电容值(μF)',
        '主串拆卸情况', '被串拆卸情况',

        'TB模式',
        # "SVA'互感",

        '分路电阻(Ω)',
        '分路间隔(m)',
        '电缆长度(km)',

        '主串电平级',
        '电源电压',

        '被串最大干扰电流(A)', '被串最大干扰位置(m)',
        '主串出口电流(A)', '主串入口电流(A)',
    ]


    #################################################################################

    turnout_list = []

    excel_data = []
    data2excel = Data2Excel(sheet_names=[])

    #################################################################################

    # 故障状态表
    # temp_list = ['正常']
                 # '主串PT开路', '被串PT开路', '主被串PT开路',
                 # '主串PT短路', '被串PT短路', '主被串PT短路',
                 # '主串SVA1开路', '被串SVA1开路', '主被串SVA1开路',
                 # '主串SVA1短路', '被串SVA1短路', '主被串SVA1短路',
                 # '主串TB开路', '被串TB开路', '主被串TB开路',
                 # '主串TB短路', '被串TB短路', '主被串TB短路']

    #################################################################################

    # 获取循环变量
    freq_list = [1700, 2000, 2300, 2600]

    # clist1 = [(300, 3), (350, 3),
    #           (350, 4), (400, 4),
    #           (400, 5), (450, 5), (500, 5),
    #           (500, 6), (550, 6), (600, 6),
    #           (600, 7), (650, 7)]
    # clist1 = [(650, 7)]
    # clist1 = list(range(-5, 6, 1))
    clist1 = [1]
    clist2 = [0]
    clist3 = [2600]
    clist4 = [2000]
    # clist3 = freq_list
    # clist4 = freq_list

    C_7_1 = list(itertools.combinations([1, 2, 3, 4, 5, 6, 7], 1))
    C_7_2 = list(itertools.combinations([1, 2, 3, 4, 5, 6, 7], 2))

    clist5 = [[]]
    clist6 = [[]]
    clist5.extend(C_7_1)
    clist6.extend(C_7_1)
    clist6.extend(C_7_2)
    # clist5 = [[],[1],[2],[3],[1,2],[1,2,3]]
    # clist6 = [[],[1],[2],[3],[1,2],[1,2,3]]
    # clist5 = [[],[11],[10],[9],[11,10],[11,10,9]]
    # clist6 = [[],[11],[10],[9],[11,10],[11,10,9]]

    clist = list(itertools.product(
        clist1, clist2, clist3, clist4, clist5, clist6))

    #################################################################################

    columns_max = 0
    counter = 1

    temp_temp = 0
    cv1, cv2, cv3, cv4, cv5, cv6 = [0] * 6

    # pd_read_flag = True
    pd_read_flag = False

    # for temp_temp in range(num_len):
    for cv1, cv2, cv3, cv4, cv5, cv6 in clist:

        #################################################################################

        # c_zhu = 60
        # c_bei = 80

        c_zhu = 25
        c_bei = 25

        # if cv3 == 1700 or cv3 == 2000:
        #     c_zhu = 80e-6
        # if cv4 == 1700 or cv4 == 2000:
        #     c_bei = 80e-6

        #################################################################################

        # 封装程序显示
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        if getattr(sys, 'frozen', False):
            print(df_input[temp_temp:(temp_temp + 1)])

        # print(df_input.head())
        #################################################################################

        # 数据表初始化
        data = dict()
        for key in head_list:
            data[key] = None

        # 添加数据行
        data2excel.add_row()

        #################################################################################

        if pd_read_flag:
            data['序号'] = para['序号'] = df_input['序号'][temp_temp]
        else:
            data['序号'] = para['序号'] = counter

        if pd_read_flag:
            data['备注'] =  df_input['备注'][temp_temp]
        else:
            data['备注'] = '电容数为包含TB的电容数'
            # data['备注'] = '发码继电器（0代表闭合，1代表断开）'

        data['故障情况'] = para['故障情况'] = '正常'

        #################################################################################

        # 区段长度位置
        # data['区段长度'] = para['length'] = length = 1050
        # data['区段长度'] = para['length'] = length = df_input['区段长度(m)'][temp_temp]

        if pd_read_flag:
            data['主串区段长度(m)'] = para['主串区段长度'] = df_input['主串区段长度(m)'][temp_temp]
            data['被串区段长度(m)'] = para['被串区段长度'] = df_input['被串区段长度(m)'][temp_temp]
        else:
            data['主串区段长度(m)'] = para['主串区段长度'] = 650
            data['被串区段长度(m)'] = para['被串区段长度'] = 650

        # data['发送接收长度'] = data['区段长度']
        # data['区段实际长度'] = df_input['区段长度(m)'][temp_temp]

        # data['相对位置'] = para['offset'] = 0

        data['主被发送相对位置'] = off_set_send = 0
        para['offset'] = data['被串区段长度(m)'] - data['主串区段长度(m)'] - off_set_send

        #################################################################################

        # 耦合系数
        if pd_read_flag:
            data['耦合系数'] = para['耦合系数'] = df_input['耦合系数'][temp_temp]
        else:
            data['耦合系数'] = para['耦合系数'] = 13

        #################################################################################

        # 频率
        if pd_read_flag:
            data['主串频率(Hz)'] = para['freq_主'] = freq = df_input['主串频率(Hz)'][temp_temp]
            data['被串频率(Hz)'] = para['freq_被'] = df_input['被串频率(Hz)'][temp_temp]
        else:
            # data['主串频率(Hz)'] = para['freq_主'] = freq = 1700
            # data['被串频率(Hz)'] = para['freq_被'] = 1700

            data['主串频率(Hz)'] = para['freq_主'] = freq = cv3
            data['被串频率(Hz)'] = para['freq_被'] = cv4

        data['freq'] = para['freq'] = Freq(freq)

        #################################################################################

        # 电容配置
        # data['主串电容数'] = para['主串电容数'] = get_c_num(Freq(data['主串频率']), data['区段长度'])
        # data['被串电容数'] = para['被串电容数'] = get_c_num(Freq(data['被串频率']), data['区段长度'])

        if pd_read_flag:
            data['主串电容数(含TB)'] = para['主串电容数'] = df_input['主串电容数(含TB)'][temp_temp]
            data['被串电容数(含TB)'] = para['被串电容数'] = df_input['被串电容数(含TB)'][temp_temp]
        else:
            data['主串电容数(含TB)'] = para['主串电容数'] = 7
            data['被串电容数(含TB)'] = para['被串电容数'] = 7

        #################################################################################

        # 电容位置

        # if pd_read_flag:
        #     data['主串电容(不含TB)位置'] = para['主串电容位置'] = df_input['主串电容(不含TB)位置'][temp_temp]
        #     data['被串电容(不含TB)位置'] = para['被串电容位置'] = df_input['主串电容(不含TB)位置'][temp_temp]
        # else:
        #     data['主串电容(不含TB)位置'] = para['主串电容位置'] = None
        #     data['被串电容(不含TB)位置'] = para['被串电容位置'] = None
        #     # data['主串电容(不含TB)位置'] = para['主串电容位置'] = [10, 20, 30, 40, 50]
        #     # data['被串电容(不含TB)位置'] = para['被串电容位置'] = None
        data['主串电容(不含TB)位置'] = para['主串电容位置'] = None
        data['被串电容(不含TB)位置'] = para['被串电容位置'] = None

        #################################################################################

        # 电容容值
        if pd_read_flag:
            data['主串电容值(μF)'] = c_value1 = df_input['主串电容值(μF)'][temp_temp]
            data['被串电容值(μF)'] = c_value2 = df_input['被串电容值(μF)'][temp_temp]
        else:
            data['主串电容值(μF)'] = c_value1 = c_zhu
            data['被串电容值(μF)'] = c_value2 = c_bei

        c_value1 = c_value1 * 1e-6
        c_value2 = c_value2 * 1e-6
        para['Ccmp_z_change_zhu'].rlc_s = {
            1700: [10e-3, None, c_value1],
            2000: [10e-3, None, c_value1],
            2300: [10e-3, None, c_value1],
            2600: [10e-3, None, c_value1]}
        para['Ccmp_z_change_chuan'].rlc_s = {
            1700: [10e-3, None, c_value2],
            2000: [10e-3, None, c_value2],
            2300: [10e-3, None, c_value2],
            2600: [10e-3, None, c_value2]}

        # para['Ccmp_z_change_chuan'].rlc_s = {
        #     1700: [10e-3, 390e-6, 11.9e-6],
        #     2000: [10e-3, 390e-6, 11.9e-6],
        #     2300: [10e-3, 390e-6, 11.9e-6],
        #     2600: [10e-3, 390e-6, 11.9e-6]}

        # data['被串电容值'] = '抑制装置'
        # para['抑制装置电感短路'] = ImpedanceMultiFreq()
        # para['抑制装置电感短路'].rlc_s = {
        #     1700: [10e-3, None, 11.9e-6],
        #     2000: [10e-3, None, 11.9e-6],
        #     2300: [10e-3, None, 11.9e-6],
        #     2600: [10e-3, None, 11.9e-6]}

        # data['换电容位置'] = para['换电容位置'] = cv2
        data['换电容位置'] = para['换电容位置'] = 0

        #################################################################################

        # 道床电阻
        data['道床电阻'] = rd_temp = 10000
        # data['道床电阻'] = rd_temp = 20
        # data['道床电阻'] = rd_temp = cv5
        # data['道床电阻'] = rd_temp = df_input['道床电阻(Ω·km)'][temp_temp]
        # data['道床电阻'] = df_input['主串道床电阻'][temp_temp]

        if pd_read_flag:
            data['主串道床电阻(Ω·km)'] = df_input['主串道床电阻(Ω·km)'][temp_temp]
            data['被串道床电阻(Ω·km)'] = df_input['被串道床电阻(Ω·km)'][temp_temp]
        else:
            data['主串道床电阻(Ω·km)'] = data['道床电阻']
            data['被串道床电阻(Ω·km)'] = data['道床电阻']

        para['主串道床电阻'] = Constant(data['主串道床电阻(Ω·km)'])
        para['被串道床电阻'] = Constant(data['被串道床电阻(Ω·km)'])

        #################################################################################

        # 钢轨阻抗
        data['钢轨电阻(Ω/km)'] = round(para['Trk_z'].rlc_s[freq][0], 10)
        data['钢轨电感(H/km)'] = round(para['Trk_z'].rlc_s[freq][1], 10)

        para['主串钢轨阻抗'] = para['Trk_z']
        para['被串钢轨阻抗'] = para['Trk_z']

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

        #################################################################################

        # TB模式
        # data['TB模式'] = flag_tb = '发送端单TB'
        # data['TB模式'] = flag_tb = '无TB'
        data['TB模式'] = flag_tb = '双端TB'
        # data['TB模式'] = flag_tb = df_input['TB模式'][temp_temp]
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

        # # 发码方向
        # if pd_read_flag:
        #     data['发码继电器状态'] = df_input['发码继电器状态'][temp_temp]
        # else:
        #     # data['发码继电器状态'] = 1
        #     data['发码继电器状态'] = 0

        data['主串发送器位置'] = para['sr_mod_主'] = '右发'
        data['被串发送器位置'] = para['sr_mod_被'] = '右发'

        # if data['发码继电器状态'] == 1:
        #     data['被串发送器位置'] = para['sr_mod_被'] = '不发码'
        # elif data['发码继电器状态'] == 0:
        #     data['被串发送器位置'] = para['sr_mod_被'] = '右发'

        #################################################################################

        # 设备拆卸情况
        if pd_read_flag:
            data['主串拆卸情况'] = para['主串拆卸情况'] = eval(df_input['主串拆卸情况'][temp_temp])
            data['被串拆卸情况'] = para['被串拆卸情况'] = eval(df_input['被串拆卸情况'][temp_temp])
        else:
            # data['主串拆卸情况'] = para['主串拆卸情况'] = []
            # data['被串拆卸情况'] = para['被串拆卸情况'] = []
            data['主串拆卸情况'] = para['主串拆卸情况'] = cv5
            data['被串拆卸情况'] = para['被串拆卸情况'] = cv6
            # data['电感短路故障情况'] = data['被串拆卸情况']

        #################################################################################

        # 极性交叉位置
        data['极性交叉位置'] = para['极性交叉位置'] = []

        # data['特殊位置'] = para['special_point'] = list(np.linspace(0,length + length, 21))
        data['特殊位置'] = para['special_point'] = data['极性交叉位置']

        data['节点选取模式'] = para['节点选取模式'] = '特殊'

        #################################################################################

        # SVA'互感
        data["SVA'互感"] = para["SVA'互感"] = 1

        #################################################################################

        # 机车信号
        data['最小机车信号位置'] = '-'

        data['机车信号感应系数'] = \
            str(para['机车信号比例V']) + '/' + str(para['机车信号比例I'][para['freq_主']])
        para['机车信号系数值'] = para['机车信号比例V'] / para['机车信号比例I'][para['freq_主']]

        #################################################################################

        # 电缆参数
        data['电缆电阻最大(Ω/km)'] = 45
        data['电缆电阻最小(Ω/km)'] = 43
        # data['电缆电容最大(F/km)'] = 30e-9
        # data['电缆电容最小(F/km)'] = 26e-9
        data['电缆电容最大(F/km)'] = 28e-9
        data['电缆电容最小(F/km)'] = 28e-9

        para['Cable_R'].value = data['电缆电阻最小(Ω/km)']
        para['Cable_C'].value = data['电缆电容最大(F/km)']

        #################################################################################

        # 电缆长度
        if pd_read_flag:
            data['电缆长度(km)'] = para['cab_len'] = df_input['电缆长度(km)'][temp_temp]
        else:
            data['电缆长度(km)'] = para['cab_len'] = cab_len = 10

        #################################################################################

        # 分路电阻
        if pd_read_flag:
            data['分路电阻(Ω)'] = para['Rsht_z'] = df_input['分路电阻(Ω)'][temp_temp]
        else:
            data['分路电阻(Ω)'] = para['Rsht_z'] = 0.0000001

        #################################################################################

        # 道床电阻
        # data['道床电阻最大(Ω·km)'] = 1000
        # data['道床电阻最小(Ω·km)'] = 2

        para['Rd'].value = data['道床电阻']

        #################################################################################

        # 电源配置
        if pd_read_flag:
            data['主串电平级'] = para['send_level'] = df_input['主串电平级'][temp_temp]
        else:
            data['主串电平级'] = para['send_level'] = 5

        data['电源电压'] = para['pwr_v_flg'] = '最大'
        # data['电源电压'] = para['pwr_v_flg'] = 105.9
        # data['电源电压'] = para['pwr_v_flg'] = df_input['电源电压'][temp_temp]

        # # 电码化参数配置
        config_25Hz_coding_para(df_input, temp_temp, para, data, pd_read_flag)

        #################################################################################

        # 分路间隔
        if pd_read_flag:
            data['分路间隔(m)'] = interval = df_input['分路间隔(m)'][temp_temp]
        else:
            data['分路间隔(m)'] = interval = 1

        len_posi = 0

        #################################################################################

        # # 轨面电压计算
        # md = PreModel_25Hz_coding(turnout_list=turnout_list, parameter=para)
        # md.lg = LineGroup(md.l3, name_base='线路组')
        # md.lg.special_point = para['special_point']
        # md.lg.refresh()
        # posi_list = np.arange(data['主串区段长度(m)'], -0.00001, -interval)
        #
        # len_posi = len(posi_list)
        #
        # for posi_zhu in posi_list:
        #     md.jumper.posi_rlt = posi_zhu
        #     md.jumper.set_posi_abs(0)
        #     m1 = MainModel(md.lg, md=md)
        #
        #     v_rail_zhu = md.lg['线路3']['地面']['区段1']['跳线']['U'].value_c
        #     data2excel.add_data(sheet_name="主串轨面电压", data1=v_rail_zhu)

        #################################################################################

        # # 轨面电压计算
        # md = PreModel_25Hz_coding(turnout_list=turnout_list, parameter=para)
        # md.lg = LineGroup(md.l3, name_base='线路组')
        # md.lg.special_point = para['special_point']
        # md.lg.refresh()
        # posi_list = np.arange(data['主串区段长度(m)'], -0.00001, -interval)
        #
        # len_posi = len(posi_list)
        #
        # for posi_zhu in posi_list:
        #     md.jumper.posi_rlt = posi_zhu
        #     md.jumper.set_posi_abs(0)
        #     m1 = MainModel(md.lg, md=md)
        #
        #     v_rail_zhu = md.lg['线路3']['地面']['区段1']['跳线']['U'].value_c
        #     data2excel.add_data(sheet_name="主串轨面电压", data1=v_rail_zhu)

        #################################################################################

        # data['调整轨入最大值'] = md.lg['线路3']['地面']['区段1']['左调谐单元']['1接收器']['U'].value_c
        # data['调整功出电压'] = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['U2'].value_c
        # data['调整接收轨入max(V)'] = md.lg['线路3']['地面']['区段1']['左调谐单元']['1接收器']['U'].value_c
        # data['调整功出电压max(V)'] = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['U2'].value_c
        # data['调整功出电流max(I)'] = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['I2'].value_c
        # data['调整发送轨面max(V)'] = md.lg['线路3']['地面']['区段1']['右调谐单元'].md_list[-1]['U2'].value_c
        # data['调整接收轨面max(V)'] = md.lg['线路3']['地面']['区段1']['左调谐单元'].md_list[-1]['U2'].value_c

        #################################################################################

        # 分路计算
        para['Rsht_z'] = data['分路电阻(Ω)']

        md = PreModel(turnout_list=turnout_list, parameter=para)
        # md = PreModel_EeMe(turnout_list=turnout_list, parameter=para)
        # md = PreModel_25Hz_coding(turnout_list=turnout_list, parameter=para)
        md.add_train()

        posi_list = np.arange(data['被串区段长度(m)'], -0.00001, -interval)
        len_posi = max(len(posi_list), len_posi)

        for posi_bei in posi_list:
            para['分路位置'] = posi_bei

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

            # zm_sva = 2 * np.pi * freq * data["SVA'互感"] * 1e-6 * 1j
            #
            # # list_sva1_mutual = [(3, 4, '右'), (3, 4, '左') ,(4, 3, '右') ,(4, 3, '左')]
            # list_sva1_mutual = [(3, 4, '右')]
            # for sva1_mutual in list_sva1_mutual:
            #     config_sva1_mutual(m1, sva1_mutual, zm_sva)
            #
            # m1.equs.creat_matrix()
            # m1.equs.solve_matrix()

            i_sht_zhu = md.lg['线路3']['列车2']['分路电阻1']['I'].value_c
            i_sht_bei = md.lg['线路4']['列车1']['分路电阻1']['I'].value_c

            i_trk_zhu = get_i_trk(line=m1['线路3'], posi=posi_zhu, direct='右')
            i_trk_bei = get_i_trk(line=m1['线路4'], posi=posi_bei, direct='右')

            # i1 = md.lg['线路3']['地面']['区段1']['右调谐单元']['6SVA1']['I1'].value
            # i2 = md.lg['线路3']['地面']['区段1']['右调谐单元']['6SVA1']['I2'].value
            #
            # i_sva1 = abs(i1 - i2)
            #
            # i_trk_bei_temp = i_trk_bei / i_sva1

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

            #################################################################################

            data2excel.add_data(sheet_name="主串钢轨电流", data1=i_trk_zhu)
            data2excel.add_data(sheet_name="主串分路电流", data1=i_sht_zhu)
            data2excel.add_data(sheet_name="被串钢轨电流", data1=i_trk_bei)
            data2excel.add_data(sheet_name="被串分路电流", data1=i_sht_bei)
            # data2excel.add_data(sheet_name="主串SVA'电流", data1=i_sva1)
            # data2excel.add_data(sheet_name="被串钢轨电流折算后", data1=i_trk_bei_temp)
            # data2excel.add_data(sheet_name="实测阻抗", data1=z_mm)
            # data2excel.add_data(sheet_name="阻抗模值", data1=z_mm_abs)
            # data2excel.add_data(sheet_name="耦合系数", data1=co_mutal)


        # if (length+1) > columns_max:
        #     columns_max = length + 1
        if len_posi > columns_max:
            columns_max = len_posi

        i_trk_list = data2excel.data_dict["被串钢轨电流"][-1]
        i_sht_list = data2excel.data_dict["被串分路电流"][-1]

        i_sht_list_zhu = data2excel.data_dict["主串分路电流"][-1]

        data['被串最大干扰电流(A)'] = max(i_trk_list)
        data['主串出口电流(A)'] = i_sht_list_zhu[0]
        data['主串入口电流(A)'] = i_sht_list_zhu[-1]
        data['被串最大干扰位置(m)'] = i_trk_list.index(max(i_trk_list))

        data_row = [data[key] for key in head_list]
        excel_data.append(data_row)
        counter += 1

        #################################################################################

        if not getattr(sys, 'frozen', False):
            print(data.keys())
            print(data.values())
            print(i_sht_list)

    #################################################################################

    # 修正表头
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    posi_header = list(range(columns_max))
    posi_header[0] = '发送端'
    # posi_header[0] = '调整状态'
    # posi_header[1] = '发送端0m分路'
    # posi_header = None

    df_data = pd.DataFrame(excel_data, columns=head_list)

    #################################################################################

    # 保存到本地excel
    filename = '仿真输出'
    # filename = '仿真输出_拆电容'
    # filepath = 'src/Output/'+ filename + timestamp + '.xlsx'
    filepath = ''+ filename + '_' + timestamp + '.xlsx'
    with pd.ExcelWriter(filepath) as writer:
        if pd_read_flag:
            df_input.to_excel(writer, sheet_name="参数设置", index=False)
        df_data.to_excel(writer, sheet_name="数据输出", index=False)

        names = [
            "被串钢轨电流",
            "被串分路电流",
            "主串钢轨电流",
            "主串分路电流",
            # "主串轨面电压",
            # "主串SVA'电流",
            # "被串钢轨电流折算后",
        ]

        # data2excel.write2excel(sheet_names=names, header=None, writer1=writer)
        data2excel.write2excel(sheet_names=names, header=posi_header, writer1=writer)

        pass