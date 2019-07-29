import math


# 单一频率阻抗
class ImpedanceWithFreq:
    def __init__(self, freq):
        self.freq = freq
        self._z = None

    @property
    def z(self):
        return self._z

    @property
    def omega(self):
        value = 2 * math.pi * self.freq
        return value

    # 阻抗
    @property
    def z_complex(self):
        return self._z

    @z_complex.setter
    def z_complex(self, value):
        if value.real >= 0:
            self._z = value
        else:
            raise KeyboardInterrupt('复数实部不能为负数')

    # 阻抗极坐标形式
    @property
    def z_polar(self):
        r, angle = None, None
        if self._z:
            z = self._z
            r = abs(z)
            angle = math.degrees(math.atan2(z.imag, z.real))
        return r, angle

    @z_polar.setter
    def z_polar(self, value):
        r, angle = value
        if r >= 0:
            if -90 <= angle <= 90:
                imag = r * math.sin(math.radians(angle))
                real = r * math.cos(math.radians(angle))
                self._z = complex(real, imag)
            else:
                raise KeyboardInterrupt('辐角需要在正负90度之间')
        else:
            raise KeyboardInterrupt('模值不能为负数')

    # 阻抗串联等效
    @property
    def rlc_s(self):
        resistance, inductance, capacitance = None, None, None
        if self._z:
            real = self._z.real
            imag = self._z.imag
            resistance = None if real == 0 else real
            if imag > 0:
                inductance = imag / self.omega
            elif imag < 0:
                capacitance = - 1 / (imag * self.omega)
        return resistance, inductance, capacitance

    @rlc_s.setter
    def rlc_s(self, value):
        resistance, inductance, capacitance = value
        real, imag = 0, 0
        if resistance:
            if resistance >= 0:
                real = resistance
            else:
                raise KeyboardInterrupt('串联等效电阻不能为负数')
        if inductance:
            if inductance >= 0:
                imag += inductance * self.omega
            else:
                raise KeyboardInterrupt('串联等效电感不能为负数')
        if capacitance:
            if capacitance > 0:
                imag -= 1/(capacitance * self.omega)
            else:
                raise KeyboardInterrupt('串联等效电容不能为负数和零')
        self._z = complex(real, imag)

    # 并联等效
    @property
    def rlc_p(self):
        resistance, inductance, capacitance = None, None, None
        if self._z:
            y = 1 / self._z
            real = y.real
            imag = y.imag
            resistance = None if real == 0 else 1 / real
            if imag < 0:
                inductance = - 1 / (imag * self.omega)
            elif imag > 0:
                capacitance = imag / self.omega
        return resistance, inductance, capacitance

    @rlc_p.setter
    def rlc_p(self, value):
        resistance, inductance, capacitance = value
        y = 0
        if resistance:
            if resistance > 0:
                y += 1 / resistance
            else:
                raise KeyboardInterrupt('并联等效电阻不能为负数和零')
        if inductance:
            if inductance > 0:
                y += 1/(inductance * self.omega * 1j)
            else:
                raise KeyboardInterrupt('并联等效电感不能为负数和零')
        if capacitance:
            if capacitance > 0:
                y += capacitance * self.omega * 1j
            else:
                raise KeyboardInterrupt('并联等效电容不能为负数和零')
        if y == 0:
            self._z = 0
        else:
            self._z = 1 / y

    def __repr__(self):
        return str(self._z)


# 参数描述符
class ParaDescribe:
    def __init__(self, prop):
        self.prop = prop

    def __get__(self, instance, owner):
        para_dict = dict()
        for freq in instance.freq_dict.keys():
            exec('para_dict[freq] = instance.freq_dict[freq].' + self.prop)
        return para_dict

    def __set__(self, instance, value):
        for freq in value.keys():
            instance.freq_dict[freq] = ImpedanceWithFreq(freq)
            exec('instance.freq_dict[freq].' + self.prop + ' = value[freq]')


# 多频率阻抗
class ImpedanceMultiFreq:
    def __init__(self):
        self.freq_dict = {}

    # def get_value(self, freq):
    #     para = self.freq_dict[freq]
    #     z = para.z_complex
    #     return z

    def config_impedance(self, value):
        if isinstance(value, ImpedanceWithFreq):
            self.freq_dict[value.freq] = value
        else:
            raise KeyboardInterrupt('类型异常: 参数需要为阻抗类型')

    z = ParaDescribe('z_complex')
    z_complex = ParaDescribe('z_complex')
    z_polar = ParaDescribe('z_polar')
    rlc_s = ParaDescribe('rlc_s')
    rlc_p = ParaDescribe('rlc_p')

    def value(self, freq):
        return self[freq].z_complex

    def values(self):
        return self.freq_dict.values()

    def keys(self):
        return self.freq_dict.keys()

    def items(self):
        return self.freq_dict.items()

    def __repr__(self):
        return str(self.z)

    def __len__(self):
        return len(self.freq_dict)

    def __getitem__(self, key):
        return self.freq_dict[key]




    
if __name__ == '__main__':
    # a = ParaMultiF(1700,2000,2300,2600)
    # bb = {
    #     1700 : [1.38,   1.36e-3,    None],
    #     2000 : [1.53,   1.35e-3,    None],
    #     2300 : [1.68,   1.35e-3,    None],
    #     2600 : [1.79,   1.34e-3,    None]}
    # a = ParaMultiF(data = bb, datatype = 'rlc_s')
    # b = ParaMultiF(1700,2000,2300,2600)

    a = ImpedanceWithFreq(1700)
    b = ImpedanceMultiFreq()
    b.z = {
        1700: (0.006459333 + 0.030996667j),
        2000: (0.007119667 + 0.035956660j),
        2300: (0.007735333 + 0.040813333j),
        2600: (0.008341333 + 0.045740000j)}

    xxx = 10
