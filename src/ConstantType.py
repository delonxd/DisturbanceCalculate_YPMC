

# 单一频率阻抗
class Constant:
    def __init__(self, value=0.0):
        self.value = float(value)

    def __float__(self):
        return float(self.value)

    def copy(self):
        obj = Constant(self.value)
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
    a = Constant(15)

    xxx = 10
