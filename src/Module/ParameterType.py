from src.ElectricParameter1 import ImpedanceMultiFreq


# 常量
class Constant:
    def __init__(self, parent, name, value):
        self.parent_class = parent
        self.name = name
        self._value = value

    def value(self, freq):
        _ = freq
        return self._value


class VariableImpedance:
    def __init__(self, parent, name, value):
        self.parent_class = parent
        self.name = name
        if isinstance(value, ImpedanceMultiFreq):
            self.value = value
        else:
            raise KeyboardInterrupt('变量类型应为阻抗')

    def value(self, freq):
        value = self.value[freq].z
        return value
