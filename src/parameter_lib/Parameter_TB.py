import pickle
from src.ImpedanceParaType import *

# TB参数
Parameter = dict()
Parameter['TB'] = dict()

########################################################################################################################
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


with open('../parameter_pkl/Parameter_TB.pkl', 'wb') as pk_f:
    pickle.dump(Parameter, pk_f)

if __name__ == '__main__':
    pass

