import math


# 单一频率阻抗
class ImpedanceWithFreq:
    def __init__(self, freq, value=0):
        self.freq = freq
        self._z = None
        self.z_complex = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self.z_complex = value

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
        # if value.real >= 0:
        #     self._z = value
        # else:
        #     raise KeyboardInterrupt('复数实部不能为负数')
        if value.real or value.real == 0:
            self._z = value

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
            # if -90 <= angle <= 90:
            imag = r * math.sin(math.radians(angle))
            real = r * math.cos(math.radians(angle))
            self._z = complex(real, imag)
            # else:
            #     raise KeyboardInterrupt('辐角需要在正负90度之间')
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
            if real < 0:
                return None
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

    def copy(self):
        obj = ImpedanceWithFreq(self.freq, self.z)
        return obj

    def __add__(self, other):
        if isinstance(other, ImpedanceWithFreq):
            if other.freq == self.freq:
                z_new = self._z + other._z
            else:
                raise KeyboardInterrupt('频率不同不能运算')
        else:
            z_new = self._z + other
        obj = ImpedanceWithFreq(self.freq)
        obj.z = z_new
        return obj

    def __radd__(self, other):
        obj = self.__add__(other)
        return obj

    def __sub__(self, other):
        obj = -other
        return self.__add__(obj)

    def __rsub__(self, other):
        obj = -self
        return obj.__add__(other)

    def __neg__(self):
        obj = ImpedanceWithFreq(self.freq)
        obj.z = -self.z
        return obj

    def __mul__(self, other):
        if isinstance(other, ImpedanceWithFreq):
            if other.freq == self.freq:
                z_new = self._z * other._z
            else:
                raise KeyboardInterrupt('频率不同不能运算')
        else:
            z_new = self._z * other
        obj = ImpedanceWithFreq(self.freq)
        obj.z = z_new
        return obj

    def __rmul__(self, other):
        obj = self.__mul__(other)
        return obj

    def __truediv__(self, other):
        if isinstance(other, ImpedanceWithFreq):
            if other.freq == self.freq:
                z_new = self._z / other._z
            else:
                raise KeyboardInterrupt('频率不同不能运算')
        else:
            z_new = self._z / other
        obj = ImpedanceWithFreq(self.freq)
        obj.z = z_new
        return obj

    def __rtruediv__(self, other):
        z_new = other / self._z
        obj = ImpedanceWithFreq(self.freq)
        obj.z = z_new
        return obj

    def __floordiv__(self, other):
        if isinstance(other, ImpedanceWithFreq):
            if other.freq == self.freq:
                z_new = self._z / (self._z + other._z) * other._z
            else:
                raise KeyboardInterrupt('频率不同不能运算')
        else:
            raise KeyboardInterrupt('并联错误')
        obj = ImpedanceWithFreq(self.freq)
        obj.z = z_new
        return obj


    def get_branch(self, other):
        if isinstance(other, ImpedanceWithFreq):
            if other.freq == self.freq:
                z_new = self._z / (other._z - self._z) * other._z
            else:
                raise KeyboardInterrupt('频率不同不能运算')
        else:
            raise KeyboardInterrupt('并联错误')
        obj = ImpedanceWithFreq(self.freq)
        obj.z = z_new
        return obj

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

    z = ParaDescribe('z_complex')
    z_complex = ParaDescribe('z_complex')
    z_polar = ParaDescribe('z_polar')
    rlc_s = ParaDescribe('rlc_s')
    rlc_p = ParaDescribe('rlc_p')

    @property
    def freq(self):
        f = set(self.freq_dict.keys())
        return f

    def value(self, freq):
        return self[freq].z_complex

    def values(self):
        return self.freq_dict.values()

    def keys(self):
        return self.freq_dict.keys()

    def items(self):
        return self.freq_dict.items()

    def copy(self):
        return self.select_freqs(self.keys())

    def __repr__(self):
        return str(self.z)

    def __len__(self):
        return len(self.freq_dict)

    def __getitem__(self, key):
        return self.freq_dict[key]

    def config_impedance(self, value):
        if isinstance(value, ImpedanceWithFreq):
            self.freq_dict[value.freq] = value.copy()
        else:
            raise KeyboardInterrupt('类型异常: 参数需要为阻抗类型')

    def get_property(self, key):
        value = None
        try:
            value = self.freq_dict[key]
        except KeyError:
            pass
        return value

    def set_property(self, key, value_t):
        obj = ImpedanceWithFreq(key, value_t)
        self.config_impedance(obj)

    def pop_property(self, key):
        self.freq_dict.pop(key)

    def select_freqs(self, freqs):
        obj = ImpedanceMultiFreq()
        for freq in freqs:
            obj.config_impedance(self[freq])
        return obj

    def convert_to_multi_freq(self, value):
        obj_m = ImpedanceMultiFreq()
        if isinstance(value, ImpedanceMultiFreq):
            obj_m = value.select_freqs(self.keys())
        else:
            for freq in self.keys():
                obj = ImpedanceWithFreq(freq, value)
                obj_m.config_impedance(obj)
        return obj_m

    def __add__(self, other):
        other = self.convert_to_multi_freq(other)
        obj = ImpedanceMultiFreq()
        for key in self.keys():
            obj.config_impedance(self[key] + other[key])
        return obj

    def __radd__(self, other):
        obj = self.__add__(other)
        return obj

    def __sub__(self, other):
        other = self.convert_to_multi_freq(other)
        obj = self.__add__(-other)
        return obj

    def __rsub__(self, other):
        other = self.convert_to_multi_freq(other)
        obj = other.__add__(-self)
        return obj

    def __neg__(self):
        obj = ImpedanceMultiFreq()
        for key in self.keys():
            obj.config_impedance(-self[key])
        return obj

    def __mul__(self, other):
        other = self.convert_to_multi_freq(other)
        obj = ImpedanceMultiFreq()
        for key in self.keys():
            obj.config_impedance(self[key] * other[key])
        return obj

    def __rmul__(self, other):
        obj = self.__mul__(other)
        return obj

    def __truediv__(self, other):
        other = self.convert_to_multi_freq(other)
        obj = ImpedanceMultiFreq()
        for key in self.keys():
            obj.config_impedance(self[key] / other[key])
        return obj

    def __rtruediv__(self, other):
        other = self.convert_to_multi_freq(other)
        obj = ImpedanceMultiFreq()
        for key in self.keys():
            obj.config_impedance(other[key] / self[key])
        return obj

    def __floordiv__(self, other):
        other = self.convert_to_multi_freq(other)
        obj = ImpedanceMultiFreq()
        for key in self.keys():
            obj.config_impedance(other[key] // self[key])
        return obj

    def get_branch(self, other):
        other = self.convert_to_multi_freq(other)
        obj = ImpedanceMultiFreq()
        for key in self.keys():
            # obj.config_impedance(other[key] // self[key])
            obj.config_impedance(self[key].get_branch(other[key]))
        return obj


if __name__ == '__main__':
    pass
    # a = ImpedanceMultiFreq()
    # a.rlc_s = {
    #     # 1700: [1.539, 502e-6, None],
    #     1700: [1.539, 502.818e-6, None],
    #     2000: [1.595, 500e-6, None],
    #     2300: [1.652, 498e-6, None],
    #     2600: [1.712, 496e-6, None]}
    #
    # b = ImpedanceMultiFreq()
    # b.rlc_s = {
    #     # 1700: [221, 44.2e-3, None],
    #     1700: [221.835, 44.169e-3, None],
    #     2000: [253, 40.9e-3, None],
    #     2300: [277, 38.3e-3, None],
    #     2600: [298, 36.1e-3, None]}
    # c = ImpedanceWithFreq(1700)
    # c.z = 20
    #
    # d = c.copy()
    # d.freq = 1700

    a = ImpedanceMultiFreq()
    # l1 = 0.38594e-3

    a.rlc_s = {
        1700: [None, None, 25e-6],
        2000: [None, None, 25e-6],
        2300: [None, None, 25e-6],
        2600: [None, None, 25e-6]}

    b = ImpedanceMultiFreq()
    c1 = 100e-6
    b.rlc_s = {
        1700: [None, None, c1],
        2000: [None, None, c1],
        2300: [None, None, c1],
        2600: [None, None, c1]}

    # c = a + b

    c = a[2300].get_branch(b[2300])

    d = ImpedanceMultiFreq()
    l1 = 6.384447614514039e-05
    d.rlc_s = {
        1700: [None, l1, None],
        2000: [None, l1, None],
        2300: [None, l1, None],
        2600: [None, l1, None]}

    e = b // d


    xxx = 10
