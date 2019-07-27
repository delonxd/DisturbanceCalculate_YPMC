from src.PortNetwork import TwoPortNetwork

# 钢轨段模型
class SubRailPi(TwoPortNetwork):
    def __init__(self, parent_ins, name_base, l_posi, r_posi, z_trk, rd):
        super().__init__(parent_ins, name_base)
        self.init_position(l_posi)
        self.flag_ele_unit = True
        self.l_posi = l_posi
        self.r_posi = r_posi
        self.track_length = r_posi - l_posi
        self.z_trk = z_trk
        self.rd = rd

    def get_equs(self, freq):
        z_trk = self.z_trk
        rd = self.rd
        length = self.track_length / 1000

        y_tk = 1 / z_trk[freq].z / length
        y_rd = 1 / rd * length
        equ1 = Equation(varbs=[self['I1'], self['U1'], self['U2']],
                        values=[-1, (y_rd + y_tk), -y_tk])
        equ2 = Equation(varbs=[self['I2'], self['U1'], self['U2']],
                        values=[-1, -y_tk, (y_tk + y_rd)])
        self.equs = [equ1, equ2]
        if hasattr(self, 'mutual_trk'):
            m_circuit = self.mutual_trk
            m = length * 0.30
            self.varb_dict['Im'] = m_circuit.varb_dict['I1']
            equ1.add_varb(self['Im'], (m * (y_rd + y_tk)))
            equ2.add_varb(self['Im'], -(m * y_tk))
