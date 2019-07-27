from src.ElePack import *
import numpy as np

# 钢轨
class Rail:
    def __init__(self, parant_line, l_posi, r_posi, ztrk, rd):
        self.parant_line = parant_line
        if l_posi >= r_posi:
            KeyboardInterrupt('钢轨左坐标不能大于右坐标')
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
            l = rail.l_posi
            r = rail.r_posi
            if r <= new_l or new_r <= l:
                pass
            elif l < new_l < r <= new_r:
                rail.r_posi = new_l
            elif l < new_l < new_r< r:
                rail.r_posi = new_l
                rail_t = Rail(parant_line=rail.parant_line,
                              l_posi=new_r, r_posi=r,
                              ztrk=rail.ztrk, rd=rail.rd)
                self.rail_set.add(rail_t)
            elif new_l <= l < new_r < r:
                rail.l_posi = new_r
            elif new_l <= l < r <= new_r:
                self.rail_set.discard(rail)
        new_rail.parant_line = self.parent_ins
        self.rail_set.add(new_rail)


# # 钢轨分割段
# class RailSegment:
#     def __init__(self, l_posi, r_posi, ztrk, rd):
#         self.l_posi = l_posi
#         self.r_posi = r_posi
#         self.ztrk = ztrk
#         self.rd = rd

# # 钢轨
# class Rail(ElePack):
#     def __init__(self, parent_ins, name_base, parameter,
#                  trk_num=1, posi=None, ztrk=None, rd=None):
#         super().__init__(parent_ins, name_base)
#         posi = [-np.inf, np.inf] if posi is None else posi
#         ztrk = [parameter['Trk_z']] if ztrk is None else ztrk
#         rd = [parameter['Rd']] if rd is None else rd
#         init_list = [trk_num, posi, ztrk, rd]
#         self.posi_list = list()
#         self.rail_list = list()
#         # self.sub_rail_list = list()
#         self.init_rail_list(init_list)
#
#     def init_rail_list(self, init_list):
#         trk_num = init_list[0]
#         posi_list = init_list[1][:(trk_num+1)]
#         ztrk_list = init_list[2][:trk_num]
#         rd_list = init_list[3][:trk_num]
#
#         self.posi_list = posi_list
#         for num in range(trk_num):
#             self.rail_list.append(RailSegment(l_posi=posi_list[num],
#                                               r_posi=posi_list[num + 1],
#                                               ztrk=ztrk_list[num],
#                                               rd=rd_list[num]))


if __name__ == '__main__':
    import src.TrackCircuitCalculator3 as tc


    a = Rail(parant_line=None, l_posi=-20, r_posi=300, ztrk=1.314, rd=1000)
    rg = RailGroup(parent_ins=None, name_base='akdla', parameter=tc.TCSR_2000A)
    rg.add_rail(a)


    b = 1

