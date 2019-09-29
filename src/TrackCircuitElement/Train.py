from src.AbstractClass.ElePack import *
from src.Module.OutsideElement import ROutside


# 列车
class Train(ElePack):
    def __init__(self, name_base, posi, parameter):
        parent_ins = None
        super().__init__(parent_ins, name_base)
        self.init_position(posi)
        self.parameter = parameter
        self.element['分路电阻1'] = ROutside(parent_ins=self, name_base='分路电阻1',
                                         posi=0, z=self.parameter['Rsht_z'])
        self.set_ele_name(prefix='')
        self.set_posi_abs(0)
