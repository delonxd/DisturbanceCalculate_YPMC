import math


class PropZpolar:
    def __get__(self, instance, owner):
        return instance.getZpolar()    

    def __set__(self, instance, value):
        instance.setZpolar(value[0],value[1])


class PropRLC_s:
    def __get__(self, instance, owner):
        return instance.getRLC_s()    

    def __set__(self, instance, value):
        instance.setRLC_s(value[0],value[1],value[2])


class PropRLC_p:
    def __get__(self, instance, owner):
        return instance.getRLC_p()    

    def __set__(self, instance, value):
        instance.setRLC_p(value[0],value[1],value[2])


class ParaSingleF:
    def __init__(self,freq):
        self.freq = freq
        self.z = 0

    # 复数形式
    def setZcmplx(self,z):
        if z.real >= 0:
            self.z = z
        else:
            raise KeyboardInterrupt('复数实部不能为负数')
        
    def getZcmplx(self):
        return self.z

    # 极坐标形式
    def setZpolar(self,r,angle):
        if r >= 0:
            if angle <= 90 and angle >= -90:
                imag = r * math.sin(math.radians(angle))
                real = r * math.cos(math.radians(angle))
                self.z = complex(real,imag)
            else:
                raise KeyboardInterrupt('辐角需要在正负90度之间')
        else:
            raise KeyboardInterrupt('模值不能为负数')

    def getZpolar(self):
        r = abs(self.z)
        angle = math.degrees(math.atan2(self.z.imag,self.z.real))
        return r,angle

    # 串联等效
    def setRLC_s(self,R,L,C):
        real = 0
        imag = 0
        if R is not None:
            if R >= 0:
                real = R
            else:
                raise KeyboardInterrupt('串联等效电阻不能为负数')
        if L is not None:
            if L >= 0:
                imag += L * 2 * math.pi  * self.freq
            else:
                raise KeyboardInterrupt('串联等效电感不能为负数')
        if C is not None:
            if C > 0:
                imag -= 1/(C * 2 * math.pi  * self.freq)
            else:
                raise KeyboardInterrupt('串联等效电容不能为负数和零')
        self.z = complex(real,imag)

    def getRLC_s(self):
        real = self.z.real
        imag = self.z.imag
        R = None if real == 0 else real
        L = None
        C = None
        if imag > 0:
            L = imag / (2 * math.pi  * self.freq)
        elif imag < 0:
            C = - 1/ (imag * 2 * math.pi  * self.freq)
        return R,L,C
    
    # 并联等效
    def setRLC_p(self,R,L,C):
        y = 0
        if R is not None:
            if R > 0:
                y += 1 / R
            else:
                raise KeyboardInterrupt('并联等效电阻不能为负数和零')
        if L is not None:
            if L > 0:
                y += 1/(L * 2 * math.pi  * self.freq * 1j)
            else:
                raise KeyboardInterrupt('并联等效电感不能为负数和零')
        if C is not None:
            if C > 0:
                y += C * 2 * math.pi  * self.freq * 1j
            else:
                raise KeyboardInterrupt('并联等效电容不能为负数和零')
        if y == 0:
            self.z = 0
        else:
            self.z = 1 / y

    def getRLC_p(self):
        R = None
        L = None
        C = None
        if bool(self.z):
            y = 1 / self.z
            real = y.real
            imag = y.imag
            R = None if real == 0 else 1/real
            if imag < 0:
                L = - 1 / (imag * 2 * math.pi * self.freq)
            elif imag > 0:
                C = imag / (2 * math.pi * self.freq)
        return R,L,C
    
    def __repr__(self):
        return str(self.z)
    
    z_polar = PropZpolar()
    rlc_s = PropRLC_s()
    rlc_p = PropRLC_p()


class PropMultiF:
    def __init__(self, para):
        self.para = para
        
    def __get__(self, instance, owner):
        dict_para = {}
        for freq in instance.para.keys():
            exec('dict_para[freq] = instance.para[freq].' + self.para)
        return dict_para
    
    def __set__(self, instance, value):
        for freq in value.keys():
            if freq in instance.para.keys():
                exec('instance.para[freq].' + self.para + ' = value[freq]')


class ParaMultiF:
    def __init__(self, *value, data = None, datatype = None):
        self.para = {}
        if data:
            for item in data.items():
                self.para[item[0]] = ParaSingleF(item[0])
            exec('self.' + datatype + ' = data')
        else:
            for freq in value:
                self.para[freq] = ParaSingleF(freq)

    z = PropMultiF('z')
    z_polar = PropMultiF('z_polar')
    rlc_s = PropMultiF('rlc_s')
    rlc_p = PropMultiF('rlc_p')

    def values(self):
        return self.para.values()

    def keys(self):
        return self.para.keys()

    def items(self):
        return self.para.items()

    def __repr__(self):
        return str(self.z)
    
    def __len__(self):
        return len(self.para)

    def __getitem__(self, key):
        return self.para[key]

    
if __name__ == '__main__':
    # a = ParaMultiF(1700,2000,2300,2600)
    bb = {
        1700 : [1.38,   1.36e-3,    None],
        2000 : [1.53,   1.35e-3,    None],
        2300 : [1.68,   1.35e-3,    None],
        2600 : [1.79,   1.34e-3,    None]}
    a = ParaMultiF(data = bb, datatype = 'rlc_s')
    b = ParaMultiF(1700,2000,2300,2600)









        
