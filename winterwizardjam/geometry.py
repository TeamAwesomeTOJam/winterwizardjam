from math import cos, sin, pi, acos, sqrt

class geometry(object):

    def __init__(self):
        self.line_slope = 0.25
        self.amplitude_1 = 20
        self.period_1 = 450
        self.amplitude_2 = 100
        self.period_2 = 800

        self.lead_up_length = 600
        self.ramp_length = 450
        self.ramp_rad = 500

        self.total_lead_up = self.lead_up_length + self.ramp_length

    def height(self, x):
        if x <= self.lead_up_length:
            return 0
        elif x <= self.total_lead_up:
            return self.ramp_rad - sqrt((self.ramp_rad + self.lead_up_length - x) * (self.ramp_rad - self.lead_up_length + x))
            # return -1 * self.ramp_rad * sin(acos((1.0 / self.ramp_rad) * (x - self.lead_up_length))) + self.ramp_rad
        else:
            return self.line_slope * x - self.line_slope * self.total_lead_up + self.amplitude_1 * cos ((2 * pi / self.period_1) * x) + self.amplitude_2 * cos ((2 * pi / self.period_2) * x)

    def slope(self, x):
        if x <= self.lead_up_length:
            return 0
        elif x <= self.total_lead_up:
            return (x - self.lead_up_length)/(self.ramp_rad * sqrt(1 - (self.lead_up_length - x)**2 / self.ramp_rad**2))
        else:
            return self.line_slope - self.amplitude_1 * (2 * pi / self.period_1) * sin ((2 * pi / self.period_1) * x) - self.amplitude_2 * (2 * pi / self.period_2) * sin ((2 * pi / self.period_2) * x)

    def line_height(self, x):
        if x <= self.total_lead_up:
            return 0
        else:
            return self.line_slope * x - self.line_slope * self.total_lead_up