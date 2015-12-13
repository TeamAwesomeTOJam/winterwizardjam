from math import atan2, sqrt, cos, sin, pi

import sdl2hl
import sdl2hl.gfx


class kite(object):

    def __init__(self, ghost = False):
        self.length = 400
        self.spread = 200
        if ghost:
            self.color = (0, 255, 255, 255)
        else:
            self.color = (255, 0, 0, 255)
        self.center_to_string_end_angle = atan2(self.spread, (2 * self.length))
        self.center_to_string_end = sqrt(self.length * self.length + self.spread * self.spread / 4)

        self.bar_length = 10

        self.in_length = 20
        self.out_length = 40

    def update(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def draw(self, renderer, camera):
        renderer.draw_color = self.color

        # draw the bar
        bar_angle = self.angle - pi / 2

        bar_start_x = self.x + (self.bar_length / 2) * cos(bar_angle)
        bar_start_y = self.y + (self.bar_length / 2) * sin(bar_angle)

        bar_end_x = self.x - (self.bar_length / 2) * cos(bar_angle)
        bar_end_y = self.y - (self.bar_length / 2) * sin(bar_angle)

        renderer.draw_line(camera.to_screen_x(bar_start_x), camera.to_screen_y(bar_start_y), camera.to_screen_x(bar_end_x), camera.to_screen_y(bar_end_y))

        # draw the strings
        string_1_end_x = self.x + self.center_to_string_end * cos(self.angle - self.center_to_string_end_angle)
        string_1_end_y = self.y + self.center_to_string_end * sin(self.angle - self.center_to_string_end_angle)

        string_1_start_x = self.x + (self.bar_length / 2) * cos(bar_angle)
        string_1_start_y = self.y + (self.bar_length / 2) * sin(bar_angle)

        renderer.draw_line( camera.to_screen_x(string_1_start_x), camera.to_screen_y(string_1_start_y), camera.to_screen_x(string_1_end_x), camera.to_screen_y(string_1_end_y))

        string_2_end_x = self.x + self.center_to_string_end * cos(self.angle + self.center_to_string_end_angle)
        string_2_end_y = self.y + self.center_to_string_end * sin(self.angle + self.center_to_string_end_angle)

        string_2_start_x = self.x - (self.bar_length / 2) * cos(bar_angle)
        string_2_start_y = self.y - (self.bar_length / 2) * sin(bar_angle)

        renderer.draw_color = self.color
        renderer.draw_line( camera.to_screen_x(string_2_start_x), camera.to_screen_y(string_2_start_y), camera.to_screen_x(string_2_end_x), camera.to_screen_y(string_2_end_y))

        # draw the inner arc
        r = (self.in_length * self.in_length + self.spread * self.spread / 4) / (2 * self.in_length)
        offset_length = self.length + self.in_length - r

        px = self.x + offset_length * cos(self.angle)
        py = self.y + offset_length * sin(self.angle)

        angle1 = -1 * int(atan2(string_2_end_y - py, string_2_end_x - px) * 180 / pi)
        angle2 = -1 * int(atan2(string_1_end_y - py, string_1_end_x - px) * 180 / pi)

        primitives = sdl2hl.gfx.GfxPrimitives(renderer)
        primitives.draw_arc(camera.to_screen_x(px), camera.to_screen_y(py), camera.to_screen_len(r), angle1, angle2, self.color)

        # draw the outer arc
        r = (self.out_length * self.out_length + self.spread * self.spread / 4) / (2 * self.out_length)
        offset_length = self.length + self.out_length - r

        px = self.x + offset_length * cos(self.angle)
        py = self.y + offset_length * sin(self.angle)

        angle1 = -1 * int(atan2(string_2_end_y - py, string_2_end_x - px) * 180 / pi)
        angle2 = -1 * int(atan2(string_1_end_y - py, string_1_end_x - px) * 180 / pi)

        primitives = sdl2hl.gfx.GfxPrimitives(renderer)
        primitives.draw_arc(camera.to_screen_x(px), camera.to_screen_y(py), camera.to_screen_len(r), angle1, angle2, self.color)