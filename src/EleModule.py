from src.ElePack import *


# 电气模块
class EleModule(ElePack):
    new_table = {
        '变量名': 'varb_name',
        '变量字典': 'varb_dict',
        '公式列表': 'equs',
        '模块列表': 'md_list',
    }
    prop_table = ElePack.prop_table.copy()
    prop_table.update(new_table)

    def __init__(self, parent_ins, name_base):
        super().__init__(parent_ins, name_base)
        self.varb_name = list()
        self.varb_dict = dict()
        self.equs = list()
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
