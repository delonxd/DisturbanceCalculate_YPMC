

# 单一频率阻抗
class Freq:
    def __init__(self, value=0.0):
        self.value = value

    def change_freq(self):
        new = self.value
        if self.value == 1700:
            new = 2300
        elif self.value == 2000:
            new = 2600
        elif self.value == 2300:
            new = 1700
        elif self.value == 2600:
            new = 2000
        self.value = new
        return new

    def __float__(self):
        return float(self.value)

    def copy(self):
        obj = Freq(self.value)
        return obj

    def __add__(self, other):
        value_new = self.value + other
        return value_new

    def __radd__(self, other):
        value_new = self.value + other
        return value_new

    def __sub__(self, other):
        value_new = self.value - other
        return value_new

    def __rsub__(self, other):
        value_new = other - self.value
        return value_new

    def __neg__(self):
        value_new = -self.value
        return value_new

    def __mul__(self, other):
        value_new = self.value * other
        return value_new

    def __rmul__(self, other):
        value_new = self.value * other
        return value_new

    def __truediv__(self, other):
        value_new = self.value / other
        return value_new

    def __rtruediv__(self, other):
        value_new = other / self.value
        return value_new

    def __repr__(self):
        return str(self.value)


if __name__ == '__main__':
    a = Freq(1700)

    xxx = 10
