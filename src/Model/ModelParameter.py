import pickle
from src.ImpedanceParaType import ImpedanceMultiFreq
from src.ConstantType import Constant


# 模型参数
class ModelParameter:
    def __init__(self, name='原始参数'):
        self.name = name
        self.parameter = dict()
        with open('../parameter_pkl/BasicParameter.pkl', 'rb') as pk_f:
            parameter = pickle.load(pk_f)

########################################################################################################################
        # 移频脉冲发送器
        parameter['z_pwr_yp'] = dict()
        parameter['z_pwr_yp'][1] = ImpedanceMultiFreq()
        parameter['z_pwr_yp'][1].rlc_s = {
            1700: [1.602, 0.165e-3, None],
            2000: [1.613, 0.165e-3, None],
            2300: [1.627, 0.165e-3, None],
            2600: [1.641, 0.165e-3, None]}

        parameter['z_pwr_yp'][2] = ImpedanceMultiFreq()
        parameter['z_pwr_yp'][2].rlc_s = {
            1700: [1.254, 0.126e-3, None],
            2000: [1.264, 0.126e-3, None],
            2300: [1.275, 0.126e-3, None],
            2600: [1.287, 0.126e-3, None]}

        parameter['z_pwr_yp'][3] = ImpedanceMultiFreq()
        parameter['z_pwr_yp'][3].rlc_s = {
            1700: [0.980, 0.091e-3, None],
            2000: [0.986, 0.091e-3, None],
            2300: [0.992, 0.091e-3, None],
            2600: [0.999, 0.091e-3, None]}

        parameter['z_pwr_yp'][4] = ImpedanceMultiFreq()
        parameter['z_pwr_yp'][4].rlc_s = {
            1700: [0.686, 0.058e-3, None],
            2000: [0.690, 0.058e-3, None],
            2300: [0.694, 0.058e-3, None],
            2600: [0.699, 0.058e-3, None]}

        parameter['z_pwr_ypmc_iso'] = ImpedanceMultiFreq()
        parameter['z_pwr_ypmc_iso'].rlc_s = {
            1700: [6.9, 2.62e-3, 2e-6],
            2000: [6.9, 2.62e-3, 2e-6],
            2300: [6.9, 2.62e-3, 2e-6],
            2600: [6.9, 2.62e-3, 2e-6]}

        parameter['z1_FL_ypmc'] = ImpedanceMultiFreq()
        parameter['z1_FL_ypmc'].rlc_s = {
            1700: [15.55, 6.90e-3, None],
            # 1700: [13.401, 6.683e-3, None],
            2000: [16.24, 6.86e-3, None],
            2300: [16.93, 6.84e-3, None],
            2600: [17.63, 6.81e-3, None]}

        parameter['z2_FL_ypmc'] = ImpedanceMultiFreq()
        parameter['z2_FL_ypmc'].rlc_s = {
            1700: [1883, 929e-3, None],
            # 1700: [1060, 663.437e-3, None],
            2000: [2611, 948e-3, None],
            2300: [3511, 972e-3, None],
            2600: [4643, 1003e-3, None]}

        para1 = parameter['z1_FL_ypmc']
        para2 = parameter['z2_FL_ypmc']
        para3 = para1 * para2 / (para2 - para1)
        parameter['z1_FL_ypmc'] = para3

        n_t = 1/1.095
        parameter['n_FL_ypmc'] = {
            1700: n_t,
            2000: n_t,
            2300: n_t,
            2600: n_t}

        parameter['z1_EL_ypmc'] = ImpedanceMultiFreq()
        parameter['z1_EL_ypmc'].rlc_s = {
            # 1700: [1.539, 502e-6, None],
            1700: [1.539, 502.818e-6, None],
            2000: [1.595, 500e-6, None],
            2300: [1.652, 498e-6, None],
            2600: [1.712, 496e-6, None]}

        parameter['z2_EL_ypmc'] = ImpedanceMultiFreq()
        parameter['z2_EL_ypmc'].rlc_s = {
            # 1700: [221, 44.2e-3, None],
            1700: [221.835, 44.169e-3, None],
            2000: [253, 40.9e-3, None],
            2300: [277, 38.3e-3, None],
            2600: [298, 36.1e-3, None]}

        para1 = parameter['z1_EL_ypmc']
        para2 = parameter['z2_EL_ypmc']
        para3 = para1 * para2 / (para2 - para1)
        parameter['z1_EL_ypmc'] = para3

        parameter['n_EL_ypmc'] = {
            1700: 5,
            2000: 5,
            2300: 5,
            2600: 5}

        parameter['z_rcv_ypmc_iso'] = ImpedanceMultiFreq()
        parameter['z_rcv_ypmc_iso'].rlc_s = {
            1700: [25, 0.61e-3, 2e-6],
            2000: [25, 0.61e-3, 2e-6],
            2300: [25, 0.61e-3, 2e-6],
            2600: [25, 0.61e-3, 2e-6]}

        parameter['z_rcv_ypmc'] = ImpedanceMultiFreq()
        parameter['z_rcv_ypmc'].rlc_p = {
            1700: [400, 1.5e-3, None],
            2000: [400, 1.5e-3, None],
            2300: [400, 1.5e-3, None],
            2600: [400, 1.5e-3, None]}

        parameter['z_rcv_ypmc_iso2'] = ImpedanceMultiFreq()
        parameter['z_rcv_ypmc_iso2'].z = {
            1700: (143.36382516667515 - 25.410367118195474j),
            2000: (139.327150916492943 - 24.74158309793951j),
            2300: (136.09533295271993 - 23.70236776631829j),
            2600: (133.519251755064408 - 22.51025702855196j)}

########################################################################################################################
        # 白俄TAD
        parameter['TAD_z1_Belarus'] = ImpedanceMultiFreq()
        parameter['TAD_z1_Belarus'].rlc_s = {
            1700: (20.0739, 9.74608e-3, None),
            2000: (22.4710, 9.68749e-3, None),
            2300: (25.0969, 9.62455e-3, None),
            2600: (27.9120, 9.55859e-3, None)}

        parameter['TAD_z2_Belarus'] = ImpedanceMultiFreq()
        parameter['TAD_z2_Belarus'].rlc_s = {
            1700: (3.56163e3, 2.02889e-3, None),
            2000: (4.98841e3, 2.05249e-3, None),
            2300: (6.74819e3, 2.08324e-3, None),
            2600: (8.94749e3, 2.12174e-3, None)}

        n_bel = 630 / 62
        parameter['TAD_n_Belarus'] = {
            1700: n_bel,
            2000: n_bel,
            2300: n_bel,
            2600: n_bel}

        # 白俄隔离盒Z1
        parameter['Z_iso1_Belarus'] = ImpedanceMultiFreq()
        parameter['Z_iso1_Belarus'].rlc_s = {
            1700: [6.9, 2.63e-3, 2e-6],
            2000: [6.9, 2.63e-3, 2e-6],
            2300: [6.9, 2.63e-3, 2e-6],
            2600: [6.9, 2.63e-3, 2e-6]}

        # 白俄隔离盒Z2
        parameter['Z_iso2_Belarus'] = ImpedanceMultiFreq()
        parameter['Z_iso2_Belarus'].rlc_s = {
            1700: [10, 200e-3, 2e-6],
            2000: [10, 200e-3, 2e-6],
            2300: [10, 200e-3, 2e-6],
            2600: [10, 200e-3, 2e-6]}

########################################################################################################################
        # 电容
        parameter['Ccmp_z'] = ImpedanceMultiFreq()
        parameter['Ccmp_z'].rlc_s = {
            1700: [10e-3, None, 25e-6],
            2000: [10e-3, None, 25e-6],
            2300: [10e-3, None, 25e-6],
            2600: [10e-3, None, 25e-6]}

        # # 电容
        # parameter['Ccmp_z'] = ImpedanceMultiFreq()
        # parameter['Ccmp_z'].rlc_s = {
        #     1700: [10e-3, None, 40e-6],
        #     2000: [10e-3, None, 40e-6],
        #     2300: [10e-3, None, 40e-6],
        #     2600: [10e-3, None, 40e-6]}

########################################################################################################################
        # 钢轨阻抗
        parameter['Trk_z'] = ImpedanceMultiFreq()
        parameter['Trk_z'].rlc_s = {
            1700: [1.177, 1.314e-3, None],
            # 1700: [1.84, 1.36e-3, None],
            2000: [1.306, 1.304e-3, None],
            2300: [1.435, 1.297e-3, None],
            2600: [1.558, 1.291e-3, None]}

        parameter['Cable_R'] = Constant(43)
        parameter['Cable_L'] = Constant(825e-6)
        parameter['Cable_C'] = Constant(28e-9)

        parameter['Rd'] = Constant(10000)
        parameter['Rsht_z'] = Constant(0.15)

        # # 钢轨阻抗21
        # parameter['Trk_z'] = ImpedanceMultiFreq()
        # parameter['Trk_z'].rlc_s = {
        #     # 1700: [1.177, 1.314e-3, None],
        #     1700: [1.349, 1.316e-3, None],
        #     2000: [1.306, 1.304e-3, None],
        #     2300: [1.435, 1.297e-3, None],
        #     2600: [1.558, 1.291e-3, None]}


        c_value = 25e-6
        parameter['Ccmp_z'].rlc_s = {
            1700: [10e-3, None, c_value],
            2000: [10e-3, None, c_value],
            2300: [10e-3, None, c_value],
            2600: [10e-3, None, c_value]}

        parameter['标准开路阻抗'] = ImpedanceMultiFreq()
        parameter['标准开路阻抗'].rlc_s = {
            1700: [1e10, None, None],
            2000: [1e10, None, None],
            2300: [1e10, None, None],
            2600: [1e10, None, None]}

        parameter['标准短路阻抗'] = ImpedanceMultiFreq()
        parameter['标准短路阻抗'].rlc_s = {
            1700: [1e-10, None, None],
            2000: [1e-10, None, None],
            2300: [1e-10, None, None],
            2600: [1e-10, None, None]}

        parameter['TAD_z3_发送端_区间'] = 2 * parameter['TAD_z3_发送端_区间']

        self.parameter = parameter

    def __len__(self):
        return len(self.parameter)

    def __getitem__(self, key):
        return self.parameter[key]

    def __setitem__(self, key, value):
        self.parameter[key] = value

    def values(self):
        return self.parameter.values()

    def keys(self):
        return self.parameter.keys()

    def items(self):
        return self.parameter.items()


if __name__ == '__main__':
    # print(time.asctime(time.localtime()))

    # 导入参数
    para = ModelParameter()
