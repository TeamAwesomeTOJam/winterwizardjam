from math import cos, sin, pi

class geometry(object):

    def __init__(self):
        self.line_slope = 0.5
        self.amplitude_1 = 50
        self.period_1 = 500
        self.amplitude_2 = 75
        self.period_2 = 600

    def height(self, x):
        return self.line_slope * x + self.amplitude_1 * cos ((2 * pi / self.period_1) * x) + self.amplitude_2 * cos ((2 * pi / self.period_2) * x)

    def slope(self, x):
        return self.line_slope + self.amplitude_1 * (2 * pi / self.period_1) * sin ((2 * pi / self.period_1) * x) + self.amplitude_2 * (2 * pi / self.period_2) * sin ((2 * pi / self.period_2) * x)

    def line_height(self, x):
        return self.line_slope * x