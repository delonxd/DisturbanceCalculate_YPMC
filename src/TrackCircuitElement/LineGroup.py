from src.AbstractClass.ElePack import *
from src.TrackCircuitElement.JumperWires import *


class LineGroup(ElePack):
    def __init__(self, *lines, name_base=''):
        super().__init__(None, name_base)
        for line in lines:
            line.parent_ins = self
            # self.element[line.name_base] = line
            self.add_child(line.name_base, line)
        self.refresh()

    def refresh(self):
        self.get_ele_set(ele_set=set())
        self.set_ele_name(prefix='')

    def add_jumpers(self, line1, line2, name_base, posi_abs):
        jumper = JumperWireConnection(name_base, line1, line2, posi_abs)
        self.add_child(name_base, jumper)
        self.refresh()
        pass

    def add_line(self, line):
        self.add_child(line.name_base, line)

    def add_turnout(self, turnout):
        self.add_child(turnout.name_base, turnout)
