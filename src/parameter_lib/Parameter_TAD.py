import pickle
from src.ImpedanceParaType import *

# 匹配变压器参数
Parameter = dict()

########################################################################################################################
# 区间发送端配置
Parameter['TAD_z1_发送端_区间'] = ImpedanceMultiFreq()
Parameter['TAD_z1_发送端_区间'].rlc_s = {
    1700: (3.9146, 581.14e-6, None),
    2000: (3.9695, 684.89e-6, None),
    2300: (3.8636, 769.06e-6, None),
    2600: (3.7937, 959.15e-6, None)}

Parameter['TAD_z2_发送端_区间'] = ImpedanceMultiFreq()
Parameter['TAD_z2_发送端_区间'].rlc_p = {
    1700: (3.0451e3, 551.191e-3, None),
    2000: (3.1163e3, 580.653e-3, None),
    2300: (3.1775e3, 605.011e-3, None),
    2600: (3.2591e3, 635.065e-3, None)}

Parameter['TAD_z3_发送端_区间'] = ImpedanceMultiFreq()
Parameter['TAD_z3_发送端_区间'].rlc_s = {
    1700: (250e-3, 4.2e-3, None),
    2000: (250e-3, 4.2e-3, None),
    2300: (250e-3, 4.2e-3, None),
    2600: (250e-3, 4.2e-3, None)}

Parameter['TAD_c_发送端_区间'] = ImpedanceMultiFreq()
Parameter['TAD_c_发送端_区间'].rlc_s = {
    1700: (None, None, 4.7e-3),
    2000: (None, None, 4.7e-3),
    2300: (None, None, 4.7e-3),
    2600: (None, None, 4.7e-3)}

Parameter['TAD_n_发送端_区间'] = {
    1700: 8.9202,
    2000: 8.8912,
    2300: 8.8508,
    2600: 8.8688}

########################################################################################################################
# 站内发送端配置
Parameter['TAD_z1_发送端_站内'] = ImpedanceMultiFreq()
Parameter['TAD_z1_发送端_站内'].rlc_s = {
    1700: (2.5082, 313.43e-6, None),
    2000: (2.5082, 313.43e-6, None),
    2300: (2.5082, 313.43e-6, None),
    2600: (2.5082, 313.43e-6, None)}

Parameter['TAD_z2_发送端_站内'] = ImpedanceMultiFreq()
Parameter['TAD_z2_发送端_站内'].rlc_p = {
    1700: (2.5312e3, 0.284779, None),
    2000: (2.5312e3, 0.284779, None),
    2300: (2.5312e3, 0.284779, None),
    2600: (2.5312e3, 0.284779, None)}

Parameter['TAD_z3_发送端_站内'] = ImpedanceMultiFreq()
Parameter['TAD_z3_发送端_站内'].rlc_s = {
    1700: (0.1, 4.2e-3, None),
    2000: (0.1, 4.2e-3, None),
    2300: (0.1, 4.2e-3, None),
    2600: (0.1, 4.2e-3, None)}

Parameter['TAD_c_发送端_站内'] = ImpedanceMultiFreq()
Parameter['TAD_c_发送端_站内'].rlc_s = {
    1700: (None, None, 2.35e-3),
    2000: (None, None, 2.35e-3),
    2300: (None, None, 2.35e-3),
    2600: (None, None, 2.35e-3)}

Parameter['TAD_n_发送端_区间'] = {
    1700: 13.5,
    2000: 13.5,
    2300: 12,
    2600: 12}

########################################################################################################################
# 接收端配置
Parameter['TAD_z1_接收端'] = ImpedanceMultiFreq()
Parameter['TAD_z1_接收端'].rlc_s = {
    1700: (2.5082, 313.43e-6, None),
    2000: (2.5082, 313.43e-6, None),
    2300: (2.5082, 313.43e-6, None),
    2600: (2.5082, 313.43e-6, None)}

Parameter['TAD_z2_接收端'] = ImpedanceMultiFreq()
Parameter['TAD_z2_接收端'].rlc_p = {
    1700: (2.5312e3, 0.284779, None),
    2000: (2.5312e3, 0.284779, None),
    2300: (2.5312e3, 0.284779, None),
    2600: (2.5312e3, 0.284779, None)}

Parameter['TAD_z3_接收端'] = ImpedanceMultiFreq()
Parameter['TAD_z3_接收端'].rlc_s = {
    1700: (0.1, 4.2e-3, None),
    2000: (0.1, 4.2e-3, None),
    2300: (0.1, 4.2e-3, None),
    2600: (0.1, 4.2e-3, None)}

Parameter['TAD_c_接收端'] = ImpedanceMultiFreq()
Parameter['TAD_c_接收端'].rlc_s = {
    1700: (None, None, 2.35e-3),
    2000: (None, None, 2.35e-3),
    2300: (None, None, 2.35e-3),
    2600: (None, None, 2.35e-3)}

Parameter['TAD_n_发送端_区间'] = {
    1700: 8.7351,
    2000: 8.7384,
    2300: 8.6904,
    2600: 8.7085}


with open('../parameter_pkl/Parameter_TAD.pkl', 'wb') as pk_f:
    pickle.dump(Parameter, pk_f)

if __name__ == '__main__':
    pass
