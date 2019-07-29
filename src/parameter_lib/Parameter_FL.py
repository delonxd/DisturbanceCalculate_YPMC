import pickle
from src.ImpedanceParaType import *

# 防雷变压器参数
Parameter = dict()

########################################################################################################################
# 发送端配置
Parameter['FL_z1_发送端'] = ImpedanceMultiFreq()
Parameter['FL_z1_发送端'].rlc_s = {
    1700: (5.4106, 609.94e-6, None),
    2000: (5.5075, 732.70e-6, None),
    2300: (5.3495, 834.41e-6, None),
    2600: (5.4294, 949.34e-6, None)}

Parameter['FL_z2_发送端'] = ImpedanceMultiFreq()
Parameter['FL_z2_发送端'].rlc_p = {
    1700: (12.7514e3, 2.314239, None),
    2000: (13.5088e3, 2.841193, None),
    2300: (12.7879e3, 2.597024, None),
    2600: (14.7951e3, 4.116232, None)}

Parameter['FL_n_发送端'] = {
    1700: 0.9645,
    2000: 0.9695,
    2300: 0.9627,
    2600: 0.9668}

########################################################################################################################
# 接收端配置
Parameter['FL_z1_接收端'] = ImpedanceMultiFreq()
Parameter['FL_z1_接收端'].rlc_s = {
    1700: (5.5239, 513.56e-6, None),
    2000: (5.4992, 608.52e-6, None),
    2300: (5.5807, 705.17e-6, None),
    2600: (5.4392, 791.83e-6, None)}

Parameter['FL_z2_接收端'] = ImpedanceMultiFreq()
Parameter['FL_z2_接收端'].rlc_p = {
    1700: (6.1620e3, 269.488e-3, None),
    2000: (6.8163e3, 279.317e-3, None),
    2300: (7.2892e3, 285.537e-3, None),
    2600: (8.0493e3, 296.218e-3, None)}

Parameter['FL_n_接收端'] = {
    1700: 0.9690,
    2000: 0.9680,
    2300: 0.9719,
    2600: 0.9656}


with open('../parameter_pkl/Parameter_FL.pkl', 'wb') as pk_f:
    pickle.dump(Parameter, pk_f)

if __name__ == '__main__':
    pass
