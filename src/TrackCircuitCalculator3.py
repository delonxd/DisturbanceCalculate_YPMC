from src.TrackCircuitElement.SectionGroup import *
from src.TrackCircuitElement.Train import *
from src.TrackCircuitElement.Line import *
from src.TrackCircuitElement.LineGroup import *
from src.MainModel import *
from src.ModelParameter import *
from src.Method import show_ele


#######################################################################################################################

if __name__ == '__main__':
    # print(time.asctime(time.localtime()))

    # 导入参数
    para = ModelParameter()
    # 轨道电路初始化
    sg1 = SectionGroup(name_base='地面', posi=0, m_num=1, freq1=2600,
                       m_length=[509, 389, 320],
                       j_length=[29, 29, 29, 29],
                       m_type=['2000A', '2000A', '2000A'],
                       c_num=[6, 6, 5],
                       parameter=para)

    sg2 = SectionGroup(name_base='地面', posi=0, m_num=2, freq1=1700,
                       m_length=[480, 200, 320],
                       j_length=[29, 29, 29, 29],
                       m_type=['2000A', '2000A', '2000A'],
                       c_num=[8, 6, 5],
                       parameter=para)

    train1 = Train(name_base='列车1', posi_abs=0, parameter=para)

    # 生成线路
    l1 = Line(name_base='线路1', sec_group=sg1, train=train1,
              parameter=para)
    l2 = Line(name_base='线路2', sec_group=sg2,
              parameter=para)
    lg = LineGroup(l1, name_base='线路组')

    # 建立模型
    model = MainModel(lg)
    show_ele('111')
    a = 1
    pass
    # output = []
    # for i in range(0, 600, 1):
    #     set_posi_abs(train1, i)
    #     l1.set_sub_rail(ele_all=ele_all)
    #     # l2.set_sub_rail(ele_all=ele_all)
    #     # 生成矩阵
    #     # m1 = Matrix(l1, l2, freq=FREQ)
    #     m1 = Matrix(l1, freq=FREQ)
    #     b = np.zeros(m1.length, dtype=complex)
    #     # b[m1.equ_dict['主串_区段1_电压源方程1'].num] = 100
    #     b[m1.equ_dict['主串_区段1_TCSR1_1发送器_1电压源方程1'].num] = 181
    #
    #     # 结果
    #     value_c = np.linalg.solve(m1.matrx, b)
    #     # del m1
    #
    #     if l1.node_dict[i].track[0] is not None:
    #         data = abs(value_c[l1.node_dict[i].track[0]['I2'].num])
    #     else:
    #         data = 0
    #
    #     # l2.node_dict[i].track[0]['I2']
    #     # x = abs(value_c[train1['分路电阻1']['阻抗']['I'].num])
    #     # x = np.angle(value_c[rc1['区段1']['TCSR2']['发送接收器']['采样电阻']['U'].num])/np.pi*180
    #     # print(x)
    #     output.append(data)

    # # 后处理
    # U_list = []
    # I_list = []
    # for i in range(2500):
    #     U,I = get_rail_ui(l1, value_c, i, FREQ)
    #     if U:
    #         U_list.append(abs(U))
    #         I_list.append(abs(I))

    # a = sp.Matrix(m1.matrx)
    # 画图
    # plt.title("Matplotlib demo")
    # plt.xlabel("x axis caption")
    # plt.ylabel("y axis caption")
    # plt.plot(output)
    # print(time.asctime(time.localtime()))
    # plt.show()

    pass
