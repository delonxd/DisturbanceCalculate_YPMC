from src.AbstractClass.EleModule import *

class BreakPoint(EleModule):
    def __init__(self, parent_ins, name_base, posi):
        super().__init__(parent_ins, name_base)
        self.init_position(posi)
        self.flag_ele_unit = True
