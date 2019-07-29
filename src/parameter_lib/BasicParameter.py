import pickle
from src.ElectricParameter1 import *

Parameter = dict()

Parameter['z_pwr'] = dict()
Parameter['z_pwr'][1] = ImpedanceMultiFreq()
Parameter['z_pwr'][1].z = {
    1700: (22.30 + 29.00j),
    2000: (23.26 + 32.20j),
    2300: (23.93 + 36.77j),
    2600: (24.67 + 41.55j)}

Parameter['z_pwr'][2] = ImpedanceMultiFreq()
Parameter['z_pwr'][2].z = {
    1700: (18.60 + 21.50j),
    2000: (18.83 + 25.00),
    2300: (19.50 + 29.55j),
    2600: (19.80 + 31.85j)}

Parameter['z_pwr'][3] = ImpedanceMultiFreq()
Parameter['z_pwr'][3].z = {
    1700: (15.00 + 16.30j),
    2000: (15.20 + 18.50j),
    2300: (15.45 + 20.70j),
    2600: (15.90 + 23.90j)}

Parameter['z_pwr'][4] = ImpedanceMultiFreq()
Parameter['z_pwr'][4].z = {
    1700: (10.30 + 9.4j),
    2000: (11.00 + 11.0j),
    2300: (10.44 + 12.5j),
    2600: (11.00 + 14.0j)}

Parameter['z_pwr'][5] = ImpedanceMultiFreq()
Parameter['z_pwr'][5].z = {
    1700: (6.4 + 4.50j),
    2000: (6.4 + 5.16j),
    2300: (6.4 + 5.85j),
    2600: (6.4 + 6.52j)}

Parameter['z_pwr'][6] = ImpedanceMultiFreq()
Parameter['z_pwr'][6].z = {
    1700: (5.80 + 6.50j),
    2000: (5.70 + 7.55j),
    2300: (5.85 + 8.64j),
    2600: (6.00 + 9.65j)}

Parameter['z_pwr'][7] = ImpedanceMultiFreq()
Parameter['z_pwr'][7].z = {
    1700: (4.72 + 4.30j),
    2000: (4.77 + 5.05j),
    2300: (4.85 + 5.55j),
    2600: (4.93 + 6.23j)}

Parameter['z_pwr'][8] = ImpedanceMultiFreq()
Parameter['z_pwr'][8].z = {
    1700: (3.70 + 3.60j),
    2000: (3.76 + 4.18j),
    2300: (3.75 + 4.70j),
    2600: (3.86 + 5.23j)}

Parameter['z_pwr'][9] = ImpedanceMultiFreq()
Parameter['z_pwr'][9].z = {
    1700: (3.02 + 2.86j),
    2000: (3.09 + 3.30j),
    2300: (3.19 + 3.69j),
    2600: (3.21 + 4.10j)}

###################################################################
# 防雷变压器参数
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

# 匹配变压器参数
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

# 引接线参数
Parameter['CA_z_区间'] = ImpedanceMultiFreq()
Parameter['CA_z_区间'].z = {
    1700: (0.006459333 + 0.030996667j),
    2000: (0.007119667 + 0.035956660j),
    2300: (0.007735333 + 0.040813333j),
    2600: (0.008341333 + 0.045740000j)}

Parameter['CA_z_站内'] = ImpedanceMultiFreq()
Parameter['CA_z_站内'].rlc_s = {
    1700: (10.35e-3, 4.68e-6, None),
    2000: (11.71e-3, 4.49e-6, None),
    2300: (13.01e-3, 4.40e-6, None),
    2600: (14.55e-3, 4.59e-6, None)}

# SVA参数
Parameter['SVA_z'] = ImpedanceMultiFreq()
Parameter['SVA_z'].rlc_s = {
    1700: (15e-3, 33.001000e-6, None),
    2000: (17e-3, 32.897327e-6, None),
    2300: (20e-3, 32.800000e-6, None),
    2600: (22e-3, 32.700219e-6, None)}


Parameter['SVA1_z'] = ImpedanceMultiFreq()
Parameter['SVA1_z'].rlc_s = {
    1700: (37.95e-3, 31.55e-6, None),
    2000: (43.70e-3, 31.20e-6, None),
    2300: (45.60e-3, 31.00e-6, None),
    2600: (49.30e-3, 30.85e-6, None)}

# 接收端内阻
Parameter['Z_rcv'] = ImpedanceMultiFreq()
Parameter['Z_rcv'].rlc_s = {
    1700: (23e3, 3.370340e-3, None),
    2000: (23e3, 3.366127e-3, None),
    2300: (23e3, 3.363013e-3, None),
    2600: (23e3, 3.366739e-3, None)}

# PT
Parameter['PT'] = {}
Parameter['PT'][1700] = ImpedanceMultiFreq()
Parameter['PT'][1700].rlc_s = {
    1700: (7.02e-3, None, 261.48e-6),
    2000: (7.86e-3, None, 351.04e-6),
    2300: (11.63e-3, None, 2123e-6),
    2600: (85.9e-3, 50.823e-6, None)}

Parameter['PT'][2000] = ImpedanceMultiFreq()
Parameter['PT'][2000].rlc_s = {
    1700: (8.01e-3, None, 159.403e-6),
    2000: (8.64e-3, None, 188.255e-6),
    2300: (10.0e-3, None, 268.51e-6),
    2600: (13.73e-3, None, 1362e-6)}

Parameter['PT'][2300] = ImpedanceMultiFreq()
Parameter['PT'][2300].rlc_s = {
    1700: (23.54e-3, None, 2960e-6),
    2000: (1600e-3, 115.77e-6, None),
    2300: (39.51e-3, None, 141.889e-6),
    2600: (17.91e-3, None, 194.46e-6)}

Parameter['PT'][2600] = ImpedanceMultiFreq()
Parameter['PT'][2600].rlc_s = {
    1700: (13.1e-3, None, 436.52e-6),
    2000: (25.69e-3, None, 2248.8e-6),
    2300: (1464.4e-3, 97.468e-6, None),
    2600: (48.82e-3, None, 112.316e-6)}

# PT
Parameter['TB'] = {}
Parameter['TB'][1700] = ImpedanceMultiFreq()
Parameter['TB'][1700].rlc_s = {
    1700: (38.70e-3, None, 25.58e-6),
    2000: (38.11e-3, None, 48.47e-6),
    2300: (39.79e-3, 0.0040266e-3, None),
    2600: (42.46e-3, 0.094455398e-3, None)}

Parameter['TB'][2000] = ImpedanceMultiFreq()
Parameter['TB'][2000].rlc_s = {
    1700: (50.08e-3, None, 17.94e-6),
    2000: (44.95e-3, None, 25.13e-6),
    2300: (43.405e-3, None, 47.04e-6),
    2600: (43.74e-3, None, 7585.31e-6)}

Parameter['TB'][2300] = ImpedanceMultiFreq()
Parameter['TB'][2300].rlc_s = {
    1700: (17.64e-3, None, 3504.42e-6),
    2000: (165.57e-3, 0.1136e-3, None),
    2300: (207.115e-3, None, 25.29e-6),
    2600: (24.86e-3, None, 50.56e-6)}

Parameter['TB'][2600] = ImpedanceMultiFreq()
Parameter['TB'][2600].rlc_s = {
    1700: (7.345e-3, None, 231.27e-6),
    2000: (18.02e-3, None, 2573.66e-6),
    2300: (193.005e-3, 0.098589567e-3, None),
    2600: (182.545e-3, None, 25.48e-6)}

# 电缆参数
Parameter['Cable_R'] = 43
Parameter['Cable_L'] = 825e-6
Parameter['Cable_C'] = 28e-9

with open('Parameter_data.pkl', 'wb') as pk_f:
    pickle.dump(Parameter, pk_f)

if __name__ == '__main__':

    a = ImpedanceWithFreq(1700)
    b = ImpedanceMultiFreq()
    b.z = {
        1700: (0.006459333 + 0.030996667j),
        2000: (0.007119667 + 0.035956660j),
        2300: (0.007735333 + 0.040813333j),
        2600: (0.008341333 + 0.045740000j)}

    xxx = 10
