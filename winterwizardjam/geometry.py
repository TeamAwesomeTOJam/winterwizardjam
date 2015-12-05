from math import cos, sin, pi

class geometry(object):

    def __init__(self):
        self.line_slope = 0.5
        self.sin_1_amplitude = 100
        self.sin_1_period = 1000
        self.sin_2_amplitude = 150
        self.sin_2_period = 1300

    def height(self, x):
        return self.line_slope * x + self.sin_1_amplitude * sin ((2*pi / self.sin_1_period) * x) + self.sin_2_amplitude * sin ((2*pi / self.sin_2_period) * x)

    def slope(self, x):
        return self.line_slope + self.sin_1_amplitude * (2*pi / self.sin_1_period) * cos ((2*pi / self.sin_1_period) * x) + self.sin_2_amplitude * (2*pi / self.sin_2_period) * cos ((2*pi / self.sin_2_period) * x)