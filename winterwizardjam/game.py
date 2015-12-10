import sys
import sdl2hl
from math import sin, cos, pi, atan2
import geometry
import player
import clock
import stickman
import camera
import kite


class game(object):
    def __init__(self):
        sdl2hl.init()

        self.geometry = geometry.geometry()

        self.window_size = (1920, 1080)

        self.window = sdl2hl.Window(title="Winter Wizard Jam", w=self.window_size[0], h=self.window_size[1])
        # self.renderer = sdl2hl.Renderer(self.window,-1, sdl2hl.RendererFlags.presentvsync)
        self.renderer = sdl2hl.Renderer(self.window)

        self.camera = camera.camera(self.window_size[0], self.window_size[1])

        self.player = player.player(self.geometry)
        self.clock = clock.clock()

        self.mouse_screen_x = 0
        self.mouse_screen_y = 0

        self.mouse_x = 0
        self.mouse_y = 0

        self.kite = kite.kite()

    def run(self):
        while True:
            dt = self.clock.tick(60)

            # move the camera
            self.camera.x = self.player.x - 300
            self.camera.y = self.geometry.line_height(self.camera.x) - 300

            for event in sdl2hl.events.poll():
                if event.type == sdl2hl.QUIT:
                    sdl2hl.quit()
                    sys.exit()
                elif event.type == sdl2hl.KEYDOWN and event.keycode == sdl2hl.KeyCode.up:
                    self.camera.y += 5
                elif event.type == sdl2hl.KEYDOWN and event.keycode == sdl2hl.KeyCode.down:
                    self.camera.y -= 5
                elif event.type == sdl2hl.KEYDOWN and event.keycode == sdl2hl.KeyCode.left:
                    self.camera.x -= 5
                elif event.type == sdl2hl.KEYDOWN and event.keycode == sdl2hl.KeyCode.right:
                    self.camera.x += 5
                elif event.type == sdl2hl.KEYDOWN and event.keycode == sdl2hl.KeyCode.kp_minus:
                    self.camera.zoom *= 1.05
                elif event.type == sdl2hl.KEYDOWN and event.keycode == sdl2hl.KeyCode.kp_plus:
                    self.camera.zoom *= .95
                elif event.type == sdl2hl.MOUSEMOTION:
                    self.mouse_screen_x = event.x
                    self.mouse_screen_y = event.y

            self.mouse_x, self.mouse_y = self.camera.to_world(self.mouse_screen_x, self.mouse_screen_y)

            # handle the player

            rise = self.mouse_y - self.player.y
            run = self.mouse_x - self.player.x

            self.player.kite_angle = atan2(rise, run)

            self.player.update(dt)

            self.renderer.draw_color = (0, 0, 0, 255)
            self.renderer.clear()
            self.renderer.draw_color = (255, 255, 255, 255)

            points = []
            for x in range(0, self.camera.width):
                y = self.camera.to_screen_y(self.geometry.height(self.camera.to_world_x(x)))
                points.append(sdl2hl.Point(x,y))
                points.append(sdl2hl.Point(x,self.window_size[1]))
            self.renderer.draw_lines(*points)

            # draw the player
            s = stickman.StickMan(self.camera.to_screen_x(self.player.x), self.camera.to_screen_y(self.player.y),
                                  self.player.angle)
            s.draw(self.renderer)

            # draw the board
            l = 20

            p1x = self.player.x + cos(self.player.angle) * l
            p1y = self.player.y + sin(self.player.angle) * l

            p2x = self.player.x - cos(self.player.angle) * l
            p2y = self.player.y - sin(self.player.angle) * l

            self.renderer.draw_color = (255, 0, 0, 255)
            self.renderer.draw_line(self.camera.to_screen_x(p1x), self.camera.to_screen_y(p1y), self.camera.to_screen_x(p2x), self.camera.to_screen_y(p2y))

            # draw the kite
            self.kite.draw(self.renderer, self.camera, self.player.x, self.player.y, self.player.kite_angle)

            self.renderer.present()
