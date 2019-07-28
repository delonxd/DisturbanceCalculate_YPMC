from src.AbstractClass.ElePack import *
import numpy as np


# 钢轨
class Rail:
    def __init__(self, parant_line, l_posi, r_posi, ztrk, rd):
        self.parant_line = parant_line
        if l_posi >= r_posi:
            raise KeyboardInterrupt('钢轨左坐标不能大于右坐标')
        self.l_posi = l_posi
        self.r_posi = r_posi
        self.ztrk = ztrk
        self.rd = rd

    @property
    def posi_list(self):
        posi_list = [self.l_posi, self.r_posi]
        return posi_list


# 钢轨组
class RailGroup(ElePack):
    def __init__(self, parent_ins, name_base, parameter):
        super().__init__(parent_ins, name_base)
        self.parent_ins = parent_ins
        self.parameter = parameter
        self.rail_set = set()
        self.init_rail_set()

    @property
    def posi_list(self):
        posi_set = set()
        for rail in self.rail_set:
            posi_set.add(rail.l_posi)
            posi_set.add(rail.r_posi)
        posi_list = list(posi_set)
        posi_list.sort()
        return posi_list

    @property
    def rail_list(self):
        rail_list = len(self.rail_set)*[None]
        posi_list = self.posi_list[:-1]
        for rail in self.rail_set:
            n = posi_list.index(rail.l_posi)
            rail_list[n] = rail
        return rail_list

    # 初始化
    def init_rail_set(self):
        rail = Rail(parant_line=self.parent_ins,
                    l_posi=-np.inf, r_posi=np.inf,
                    ztrk=self.parameter['Trk_z'], rd=self.parameter['Rd'])
        self.rail_set = set()
        self.rail_set.add(rail)

    # 设置归属线路
    def set_parent_line(self, parent_line):
        self.parent_ins = parent_line
        for rail in list(self.rail_set):
            rail.parant_line = parent_line

    # 添加钢轨段
    def add_rail(self, new_rail):
        new_l = new_rail.l_posi
        new_r = new_rail.r_posi
        for rail in list(self.rail_set):
            left = rail.l_posi
            right = rail.r_posi
            if right <= new_l or new_r <= left:
                pass
            elif left < new_l < right <= new_r:
                rail.r_posi = new_l
            elif left < new_l < new_r < right:
                rail.r_posi = new_l
                rail_t = Rail(parant_line=rail.parant_line,
                              l_posi=new_r, r_posi=right,
                              ztrk=rail.ztrk, rd=rail.rd)
                self.rail_set.add(rail_t)
            elif new_l <= left < new_r < right:
                rail.l_posi = new_r
            elif new_l <= left < right <= new_r:
                self.rail_set.discard(rail)
        new_rail.parant_line = self.parent_ins
        self.rail_set.add(new_rail)


if __name__ == '__main__':
    import src.TrackCircuitCalculator3 as tc

    a = Rail(parant_line=None, l_posi=-20, r_posi=300, ztrk=1.314, rd=1000)
    rg = RailGroup(parent_ins=None, name_base='akdla', parameter=tc.TCSR_2000A)
    rg.add_rail(a)

    b = 1
