from src.TrackCircuitElement.SectionGroup import *
from src.TrackCircuitElement.Train import *
from src.TrackCircuitElement.Line import *
from src.TrackCircuitElement.LineGroup import *
from src.Model.MainModel import *
from src.Model.ModelParameter import *


class TestModel:
    def __init__(self):
        # 导入参数
        parameter = ModelParameter()
        self.parameter = parameter
        # 轨道电路初始化
        sg1 = SectionGroup(name_base='地面', posi=0, m_num=1, freq1=2600,
                           m_length=[509, 389, 320],
                           j_length=[29, 29, 29, 29],
                           m_type=['2000A', '2000A', '2000A'],
                           c_num=[6, 6, 5],
                           parameter=parameter)

        sg2 = SectionGroup(name_base='地面', posi=0, m_num=2, freq1=1700,
                           m_length=[480, 200, 320],
                           j_length=[29, 29, 29, 29],
                           m_type=['2000A', '2000A', '2000A'],
                           c_num=[8, 6, 5],
                           parameter=parameter)
        train1 = Train(name_base='列车1', posi_abs=0, parameter=parameter)

        # 生成线路
        l1 = Line(name_base='线路1', sec_group=sg1, train=train1,
                  parameter=parameter)
        l2 = Line(name_base='线路2', sec_group=sg2,
                  parameter=parameter)
        lg = LineGroup(l1, name_base='线路组')

        # 建立模型
        model = MainModel(lg)

        self.section_group1 = sg1
        self.section_group2 = sg2
        self.train1 = train1
        self.line1 = l1
        self.line2 = l2
        self.line_group = lg
        self.model = model
