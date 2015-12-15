from math import cos, sin, pi, acos, sqrt
import random
from datetime import datetime


class geometry(object):

    def __init__(self):
        # self.line_slope = 0.3
        # self.amplitude_1 = 20
        # self.period_1 = 750
        # self.amplitude_2 = 100
        # self.period_2 = 1100
        seed = now = datetime.utcnow().strftime('%Y-%m-%d')
        random.seed(seed)

        self.line_slope = random.uniform(0.2, 0.35)
        self.amplitude_1 = random.randint(20, 30)
        self.period_1 = random.randint(650, 800)
        self.amplitude_2 = random.randint(80, 120)
        self.period_2 = random.randint(900, 1150)

        # print 'line_slope', self.line_slope
        # print 'amplitude_1', self.amplitude_1
        # print 'period_1', self.period_1
        # print 'amplitude_2', self.amplitude_2
        # print 'period_2', self.period_2

        self.lead_up_length = 600
        self.ramp_length = 450
        self.ramp_rad = 500

        self.total_lead_up = self.lead_up_length + self.ramp_length

        self.course_length = 25000
        # self.course_length = 2000

    def height(self, x):
        if x <= self.lead_up_length:
            return 0
        elif x <= self.total_lead_up:
            return self.ramp_rad - sqrt((self.ramp_rad + self.lead_up_length - x) * (self.ramp_rad - self.lead_up_length + x))
            # return -1 * self.ramp_rad * sin(acos((1.0 / self.ramp_rad) * (x - self.lead_up_length))) + self.ramp_rad
        elif x <= self.course_length:
            return self.line_slope * x - self.line_slope * self.total_lead_up + self.amplitude_1 * cos ((2 * pi / self.period_1) * x) + self.amplitude_2 * cos ((2 * pi / self.period_2) * x)
        else:
            return self.line_slope * self.course_length - self.line_slope * self.total_lead_up + self.amplitude_1 * cos ((2 * pi / self.period_1) * self.course_length) + self.amplitude_2 * cos ((2 * pi / self.period_2) * self.course_length)

    def slope(self, x):
        if x <= self.lead_up_length:
            return 0
        elif x <= self.total_lead_up:
            return (x - self.lead_up_length)/(self.ramp_rad * sqrt(1 - (self.lead_up_length - x)**2 / self.ramp_rad**2))
        elif x <= self.course_length:
            return self.line_slope - self.amplitude_1 * (2 * pi / self.period_1) * sin ((2 * pi / self.period_1) * x) - self.amplitude_2 * (2 * pi / self.period_2) * sin ((2 * pi / self.period_2) * x)
        else:
            return 0

    def line_height(self, x):
        if x <= self.total_lead_up:
            return 0
        elif x < self.course_length:
            return self.line_slope * x - self.line_slope * self.total_lead_up
        else:
            return self.line_slope * self.course_length - self.line_slope * self.total_lead_up