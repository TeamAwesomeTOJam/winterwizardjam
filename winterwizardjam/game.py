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

        self.ghost = player.player(self.geometry, True)
        self.ghost_data_store = []
        self.ghost_data_replay = []
        self.ghost_replay_index = 0

    def run(self):

        run_start_time = sdl2hl.timer.get_ticks()
        run_finished = False

        while True:
            dt = self.clock.tick(60)

            for event in sdl2hl.events.poll():
                if event.type == sdl2hl.QUIT:
                    sdl2hl.quit()
                    sys.exit()
                elif event.type == sdl2hl.KEYDOWN and event.keycode == sdl2hl.KeyCode.escape:
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
                    self.ghost_data_replay = self.ghost_data_store
                    self.ghost_data_store = []
                    self.ghost_replay_index = 0
                    run_start_time = sdl2hl.timer.get_ticks()
                    run_finished = False
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

            if not run_finished and self.player.x > self.geometry.course_length:
                run_end_time = sdl2hl.timer.get_ticks()
                run_time = (run_end_time - run_start_time) / 1000.0
                print 'run time', run_time
                run_finished = True

            t = sdl2hl.timer.get_ticks() - run_start_time
            self.ghost_data_store.append((t, self.player.get_state()))

            # restore the ghost
            # store the ghost
            if self.ghost_data_replay:

                while self.ghost_replay_index < len(self.ghost_data_replay) - 1 and self.ghost_data_replay[self.ghost_replay_index][0] < t:
                    self.ghost_replay_index += 1
                self.ghost.set_state(self.ghost_data_replay[self.ghost_replay_index][1])
            self.renderer.draw_color = (0, 0, 0, 255)
            self.renderer.clear()
            self.renderer.draw_color = (255, 255, 255, 255)

            points = []
            # draw the slope
            for x in range(0, self.camera.width):

                y = self.camera.to_screen_y(self.geometry.height(self.camera.to_world_x(x)))
                points.append(sdl2hl.Point(x,y))
                points.append(sdl2hl.Point(x,self.window_size[1]))
            self.renderer.draw_lines(*points)
            finish = self.camera.to_screen_x(self.geometry.course_length)
            self.renderer.draw_color = (0, 255, 0, 255)
            self.renderer.draw_line(finish, 0, finish, self.camera.height)

            # draw the player
            self.player.draw(self.renderer, self.camera)

            # draw the ghost
            # draw the finish line
            if self.ghost_data_replay:

                self.ghost.draw(self.renderer, self.camera)

            self.renderer.present()