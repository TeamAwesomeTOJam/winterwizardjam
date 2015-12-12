from pkg_resources import resource_string
import sys
from math import sin, cos, pi, atan2

import sdl2hl
import sdl2hl.mixer

import geometry
import player
import clock
import stickman
import camera
import kite


class game(object):
    def __init__(self):
        sdl2hl.init()
        sdl2hl.mixer.init(sdl2hl.mixer.AudioInitFlag.ogg)
        sdl2hl.mixer.open_audio()
        
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

    def run(self):
        while True:
            dt = self.clock.tick(60)

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
                elif event.type == sdl2hl.KEYDOWN and event.keycode == sdl2hl.KeyCode.r:
                    self.player = player.player(self.geometry)
                elif event.type == sdl2hl.MOUSEMOTION:
                    self.mouse_screen_x = event.x
                    self.mouse_screen_y = event.y

            self.mouse_x, self.mouse_y = self.camera.to_world(self.mouse_screen_x, self.mouse_screen_y)

            # move the camera
            self.camera.x = self.player.x - 300
            self.camera.y = self.geometry.line_height(self.camera.x) - 200

            # get the kite angle
            angle = (self.camera.height / 2.0 - self.mouse_screen_y) / self.camera.height * pi

            # handle the player
            self.player.update(dt, angle)

            # draw the slope
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
            self.player.draw(self.renderer, self.camera)

            self.renderer.present()
