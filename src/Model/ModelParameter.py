import pickle
from src.ImpedanceParaType import ImpedanceMultiFreq


# 模型参数
class ModelParameter:
    def __init__(self, name='原始参数'):
        self.name = name
        self.parameter = dict()
        with open('../parameter_pkl/BasicParameter.pkl', 'rb') as pk_f:
            parameter = pickle.load(pk_f)

        parameter['Ccmp_z'] = ImpedanceMultiFreq()
        parameter['Ccmp_z'].rlc_s = {
            1700: [10e-3, None, 25e-6],
            2000: [10e-3, None, 25e-6],
            2300: [10e-3, None, 25e-6],
            2600: [10e-3, None, 25e-6]}

        # 钢轨阻抗
        parameter['Trk_z'] = ImpedanceMultiFreq()
        parameter['Trk_z'].rlc_s = {
            1700: [1.177, 1.314e-3, None],
            2000: [1.306, 1.304e-3, None],
            2300: [1.435, 1.297e-3, None],
            2600: [1.558, 1.291e-3, None]}

        parameter['Rd'] = 10000
        parameter['Rsht_z'] = 10e-3

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
