from src.ImpedanceParaType import ImpedanceMultiFreq


# # 常量
# class Constant:
#     def __init__(self, name, value):
#         self.name = name
#         self.value = value
#
#     @classmethod
#     def func_get_value(cls):
#         func = lambda obj, *para: obj.value
#         return func


# 多频率的变量
class VariableMultiFreq:
    def __init__(self, name, value):
        self.name = name
        if isinstance(value, dict):
            self._value = value
        else:
            raise KeyboardInterrupt('变量类型应为字典')

    def value(self, freq):
        return self._value[freq]

class VariableByFreq:
    def __init__(self, name, value):
        self.name = name
        pass


# 阻抗类型变量
class VariableImpedance:
    def __init__(self, name, value):
        self.name = name
        if isinstance(value, ImpedanceMultiFreq):
            self._value = value
        else:
            raise KeyboardInterrupt('变量类型应为阻抗')

    def value(self, freq):
        return self._value[freq].z


# 发送器内阻
class TcsrSenderImpedance:
    def __init__(self, name, value):
        self.name = name
        if isinstance(value, dict):
            self._value = value
        else:
            raise KeyboardInterrupt('变量类型应为字典')

    def value(self, freq, level=1):
        value = self._value[level][freq].z
        return value


# 调谐单元内阻
class TcsrBAImpedance:
    def __init__(self, name, value):
        self.name = name
        if isinstance(value, dict):
            self._value = value
        else:
            raise KeyboardInterrupt('变量类型应为字典')

    def value(self, freq, m_freq=1700):
        value = self._value[m_freq][freq].z
        return value