import pickle
from src.ImpedanceParaType import *

# 发送器参数
Parameter = dict()
Parameter['z_pwr'] = dict()

########################################################################################################################
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


with open('../parameter_pkl/Parameter_Power.pkl', 'wb') as pk_f:
    pickle.dump(Parameter, pk_f)

if __name__ == '__main__':
    pass
