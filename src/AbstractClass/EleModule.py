from src.AbstractClass.ElePack import *
from src.AbstractClass.Equation import *


# 电气模块
class EleModule(ElePack):
    new_table = {
        '变量名': 'varb_name',
        '变量字典': 'varb_dict',
        '公式列表': 'equs',
        '模块列表': 'md_list',
        '变量值': 'varb_value',
        '变量模值': 'varb_value_c',
    }
    prop_table = ElePack.prop_table.copy()
    prop_table.update(new_table)

    para_type = dict()

    def __init__(self, parent_ins, name_base):
        super().__init__(parent_ins, name_base)
        self.varb_name = list()
        self.varb_dict = dict()
        # self.equs = list()
        self.equs = EquationGroup()
        self.md_list = [self]

    def __len__(self):
        return len(self.varb_dict)

    def __getitem__(self, key):
        return self.varb_dict[key]

    def __setitem__(self, key, value):
        self.varb_dict[key] = value

    def values(self):
        return self.varb_dict.values()

    def keys(self):
        return self.varb_dict.keys()

    def items(self):
        return self.varb_dict.items()

    def get_varb(self, index):
        key = self.varb_name[index]
        varb = self.varb_dict[key]
        return varb

    def get_value(self, *items):
        for item in items:
            cls = self.para_type[item]
            value = self.__getattribute__(item)

    @property
    def varb_value(self):
        varb_value = dict()
        for key in self.varb_name:
            varb = self.varb_dict[key]
            varb_value[key] = varb.value
        return varb_value

    @property
    def varb_value_c(self):
        varb_value = dict()
        for key in self.varb_name:
            varb = self.varb_dict[key]
            varb_value[key] = varb.value_c
        return varb_value

    def get_equs(self, freq):
        pass

    def refresh_equs(self, freq):
        equs_old = self.equs
        self.get_equs(freq)
        for equ_new, equ_old in zip(self.equs.equs, equs_old.equs):
            equ_old.items = equ_new.items
        self.equs = equs_old
