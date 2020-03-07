from src.TrackCircuitElement.SectionGroup import *
from src.TrackCircuitElement.Train import *
from src.TrackCircuitElement.Line import *
from src.TrackCircuitElement.LineGroup import *
from src.Model.MainModel import *
from src.Model.ModelParameter import *
from src.FrequencyType import Freq
from src.Method import *


class PreModel:
    def __init__(self, turnout_list, parameter):
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train2 = Train(name_base='列车2', posi=0, parameter=parameter)
        # self.train3 = Train(name_base='列车3', posi=0, parameter=parameter)
        # self.train4 = Train(name_base='列车4', posi=0, parameter=parameter)

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

        for cv in range(1,para['主串电容数']+1):
            str_temp = 'C' + str(cv)
            sg3['区段1'][str_temp].z = para['Ccmp_z_change_zhu']

        for cv in range(1,para['被串电容数']+1):
            str_temp = 'C' + str(cv)
            sg4['区段1'][str_temp].z = para['Ccmp_z_change_chuan']

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

        # sg3['区段1'].element.pop('TB1')
        # sg3['区段1'].element.pop('TB2')
        # #
        # sg4['区段1'].element.pop('TB1')
        # sg4['区段1'].element.pop('TB2')
        #
        #
        # sg3['区段1'].element.pop('左调谐单元')
        # sg4['区段1'].element.pop('左调谐单元')
        # sg4['区段1'].element.pop('右调谐单元')


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
                  parameter=self.parameter, train=[self.train1])
        self.l4 = l4

        l3 = Line(name_base='线路3', sec_group=self.section_group3,
                  parameter=self.parameter, train=[self.train2])
        self.l3 = l3

        self.lg = LineGroup(self.l3, self.l4, name_base='线路组')
        self.lg.special_point = para['special_point']
        self.lg.refresh()
