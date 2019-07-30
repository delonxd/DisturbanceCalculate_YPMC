# 变量
class Varb:
    def __init__(self, parent_module, name_base):
        self.parent_module = parent_module
        self.name_base = name_base
        self.num = None
        self.name = ''
        self.value = None
        self.value_c = None
        self.get_varb_name()

    def get_varb_name(self):
        self.name = self.parent_module.name + '_' + self.name_base
        return self.name

    def __repr__(self):
        return repr((self.get_varb_name(), self.num))


# 变量组
class VarbGroup:
    def __init__(self, *varbs):
        self.varb_set = set()
        for varb in varbs:
            self.add_varb(varb)

    def add_varb(self, varb):
        if isinstance(varb, Varb):
            self.varb_set.add(varb)
        else:
            raise KeyboardInterrupt('类型异常: 需添加Varb类型')

    def add_varbs(self, varbs):
        if isinstance(varbs, VarbGroup):
            for varb in varbs.varb_set:
                self.add_varb(varb)
        else:
            raise KeyboardInterrupt('类型异常: 需添加VarbGroup类型')

    @property
    def varb_dict(self):
        varb_dict = dict()
        for varb in self.varb_set:
            varb_dict[varb.name] = varb
        return varb_dict

    @property
    def varb_names(self):
        name_list = list()
        for varb in self.varb_set:
            name = varb.get_varb_name()
            if name in name_list:
                raise KeyboardInterrupt('名称异常: 变量名称重复')
            else:
                name_list.append(name)
        name_list.sort()
        return name_list

    @property
    def varb_list(self):
        name_list = self.varb_names
        varb_dict = self.varb_dict
        varb_list = list()
        for name in name_list:
            varb_list.append(varb_dict[name])
        return varb_list

    def config_varb_num(self):
        varb_list = self.varb_list
        num = 0
        for varb in varb_list:
            varb.num = num
            num += 1

    def __len__(self):
        return len(self.varb_set)

    # def __repr__(self):
    #     for varb
    #     return repr(self.varb_names)
