class Varb:
    # def __init__(self, upper_module=None):im
    #     self.upper_name = upper_module
    #     self.num = None
    #     self.name = ''

    def __init__(self, upper_module=None, name_base=''):
        self.upper_module = upper_module
        self.name_base = name_base
        self.num = None
        self.name = ''

    def get_varb_name(self):
        self.name = self.upper_module.name + '_' + self.name_base
        return self.name

    def __repr__(self):
        return repr((self.get_varb_name(), self.num))
