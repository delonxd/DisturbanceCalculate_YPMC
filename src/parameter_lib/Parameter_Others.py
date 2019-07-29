import pickle
from src.ImpedanceParaType import *

# 其他参数
Parameter = dict()

########################################################################################################################
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

########################################################################################################################
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

########################################################################################################################
# 接收端内阻
Parameter['Z_rcv'] = ImpedanceMultiFreq()
Parameter['Z_rcv'].rlc_s = {
    1700: (23e3, 3.370340e-3, None),
    2000: (23e3, 3.366127e-3, None),
    2300: (23e3, 3.363013e-3, None),
    2600: (23e3, 3.366739e-3, None)}

########################################################################################################################
# 电缆参数
Parameter['Cable_R'] = 43
Parameter['Cable_L'] = 825e-6
Parameter['Cable_C'] = 28e-9


with open('../parameter_pkl/Parameter_Others.pkl', 'wb') as pk_f:
    pickle.dump(Parameter, pk_f)

if __name__ == '__main__':
    pass
