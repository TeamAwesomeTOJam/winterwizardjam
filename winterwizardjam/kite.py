from math import atan2, sqrt, cos, sin

import sdl2hl
import sdl2hl.gfx


class kite(object):

    def __init__(self):
        self.length = 400
        self.spread = 200
        self.color = (255, 0, 0, 255)
        self.spread_angle = atan2(self.spread, (2 * self.length))
        self.string_length = sqrt(self.length * self.length + self.spread * self.spread / 4)

        self.in_length = 20
        self.out_length = 40

    def draw(self, renderer, camera, x, y, angle):
        renderer.draw_color = self.color

        # draw the strings
        px = x + self.string_length * cos(angle - self.spread_angle)
        py = y + self.string_length * sin(angle - self.spread_angle)

        renderer.draw_line( camera.to_screen_x(x), camera.to_screen_y(y), camera.to_screen_x(px), camera.to_screen_y(py))

        px = x + self.string_length * cos(angle + self.spread_angle)
        py = y + self.string_length * sin(angle + self.spread_angle)

        renderer.draw_color = self.color
        renderer.draw_line( camera.to_screen_x(x), camera.to_screen_y(y), camera.to_screen_x(px), camera.to_screen_y(py))

        # draw the inner arc
        r = (self.in_length * self.in_length + self.spread * self.spread / 4) / (2 * self.in_length)
        offset_length = self.length + self.in_length - r

        px = x + offset_length * cos(angle)
        py = y + offset_length * sin(angle)

        primitives = sdl2hl.gfx.GfxPrimitives(renderer)
        primitives.draw_circle(camera.to_screen_x(px), camera.to_screen_y(py), r, self.color)

        # draw the outer arc
        r = (self.out_length * self.out_length + self.spread * self.spread / 4) / (2 * self.out_length)
        offset_length = self.length + self.out_length - r

        px = x + offset_length * cos(angle)
        py = y + offset_length * sin(angle)

        primitives = sdl2hl.gfx.GfxPrimitives(renderer)
        primitives.draw_circle(camera.to_screen_x(px), camera.to_screen_y(py), r, self.color)