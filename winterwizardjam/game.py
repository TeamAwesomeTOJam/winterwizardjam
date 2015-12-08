import sys

import sdl2hl

from math import sin, cos, pi, atan2

import geometry
import player
import clock
import stickman


class game(object):

    def __init__(self):
        sdl2hl.init()

        self.geometry = geometry.geometry()

        self.window_size = (1920, 1080)

        self.window = sdl2hl.Window(title="Winter Wizard Jam",w=self.window_size[0], h=self.window_size[1])
        #self.renderer = sdl2hl.Renderer(self.window,-1, sdl2hl.RendererFlags.presentvsync)
        self.renderer = sdl2hl.Renderer(self.window)

        self.player = player.player(self.geometry)
        self.clock = clock.clock()

        self.mouse_x = 0
        self.mouse_y = 0

    def run(self):
        while True:
            dt = self.clock.tick(60)
            for event in sdl2hl.events.poll():
                if event.type == sdl2hl.QUIT:
                    sdl2hl.quit()
                    sys.exit()
                elif event.type == sdl2hl.KEYDOWN and event.keycode == sdl2hl.KeyCode.left:
                    pass
                elif event.type == sdl2hl.KEYDOWN and event.keycode == sdl2hl.KeyCode.right:
                    pass
                elif event.type == sdl2hl.MOUSEMOTION:
                    self.mouse_x = event.x
                    self.mouse_y = self.window_size[1] - event.y

            #handle the player

            rise = self.mouse_y - self.player.y
            run = self.mouse_x - self.player.x

            self.player.kite_angle = atan2(rise, run)

            self.player.update(dt)


            self.renderer.draw_color = (0,0,0,255)
            self.renderer.clear()
            self.renderer.draw_color = (255,255,255,255)

            rects = []
            points = []
            for x in range(0, self.window_size[0]):
                y = self.window_size[1] - int(self.geometry.height(x))
                #self.renderer.draw_point(x,y)
                r = sdl2hl.Rect(x, y, 0, int(self.geometry.height(x)))
                rects.append(r)
                # points.append(sdl2hl.Point(x,y))
                # points.append(sdl2hl.Point(x,self.window_size[1]))
                # self.renderer.draw_rect(r)
            self.renderer.draw_rects(*rects)
            # self.renderer.draw_lines(*points)

            ##draw the player
            s = stickman.StickMan(int(self.player.x) - 5, self.window_size[1] - int(self.player.y) - 5, self.player.angle)
            s.draw(self.renderer)

            ##draw the mouse
            self.renderer.draw_color = (0, 255, 0, 255)
            r = sdl2hl.Rect(int(self.mouse_x) - 5, self.window_size[1] - int(self.mouse_y) - 5, 10, 10)
            self.renderer.draw_rect(r)

            # draw the kite
            self.renderer.draw_color = (0, 0, 255, 255)
            k_x = int(self.player.x + cos(self.player.kite_angle) * 200)
            k_y = int(self.player.y + sin(self.player.kite_angle) * 200)

            self.renderer.draw_line(int(self.player.x), self.window_size[1] - int(self.player.y), k_x, self.window_size[1] - k_y)

            self.renderer.present()
