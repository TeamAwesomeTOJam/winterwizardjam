from pkg_resources import resource_string
import sys
from math import sin, cos, pi, atan2

import sdl2hl
import sdl2hl.mixer
import sdl2hl.ttf

import geometry
import player
import clock
import stickman
import camera
import kite


class game(object):
    def __init__(self, renderer, size):
        self.geometry = geometry.geometry()

        self.renderer = renderer

        self.camera = camera.camera(size[0], size[1])

        self.player = player.player(self.geometry)

        self.mouse_screen_x = 0
        self.mouse_screen_y = 0

        self.mouse_x = 0
        self.mouse_y = 0

        self.ghost = player.player(self.geometry, True)
        self.ghost_data_store = []
        self.ghost_data_replay = []
        self.ghost_replay_index = 0
        
        self.font = sdl2hl.ttf.Font(resource_string(__name__, 'res/font/LiberationSans-Regular.ttf'), 24)

    def run(self, ghost_data, use_mouse):
        self.ghost_data_replay = ghost_data
        self.ghost_replay_index = 0
        self.ghost_data_store = []

        run_start_time = sdl2hl.timer.get_ticks()
        run_finished = False

        my_clock = clock.clock()

        self.player = player.player(self.geometry)

        while True:
            dt = my_clock.tick(60)

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
                    if not ghost_data:
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
            # TODO poll the mouse for this so it always accurate even if the mouse never moved
            angle = (self.camera.height / 2.0 - self.mouse_screen_y) / self.camera.height * pi

            # handle the player
            self.player.update(dt, angle)

            # store the ghost
            t = sdl2hl.timer.get_ticks() - run_start_time
            self.ghost_data_store.append((t, self.player.get_state()))

            #check race end
            if not run_finished and self.player.x > self.geometry.course_length:
                run_end_time = sdl2hl.timer.get_ticks()
                run_time = (run_end_time - run_start_time) / 1000.0
                # print 'run time', run_time
                run_finished = True
                self.player.channel.pause()
                return run_time, self.ghost_data_store

            # restore the ghost
            if self.ghost_data_replay:
                while self.ghost_replay_index < len(self.ghost_data_replay) - 1 and self.ghost_data_replay[self.ghost_replay_index][0] < t:
                    self.ghost_replay_index += 1
                self.ghost.set_state(self.ghost_data_replay[self.ghost_replay_index][1])

            self.renderer.draw_color = (0, 0, 0, 255)
            self.renderer.clear()

            # draw the slope
            self.renderer.draw_color = (255, 255, 255, 255)
            points = []
            for x in range(0, self.camera.width):
                y = self.camera.to_screen_y(self.geometry.height(self.camera.to_world_x(x)))
                points.append(sdl2hl.Point(x,y))
                points.append(sdl2hl.Point(x,self.camera.height))

            self.renderer.draw_lines(*points)

            # draw the finish line
            finish = self.camera.to_screen_x(self.geometry.course_length)
            self.renderer.draw_color = (0, 255, 0, 255)
            self.renderer.draw_line(finish, 0, finish, self.camera.height)

            # draw the player
            self.player.draw(self.renderer, self.camera)

            # draw the ghost
            if self.ghost_data_replay:
                self.ghost.draw(self.renderer, self.camera)

            # text_texture = sdl2hl.Texture.from_surface(self.renderer, self.font.render_solid('Example!', (255,255,255,255)))
            # self.renderer.copy(text_texture, dest_rect=sdl2hl.Rect(x=100, y=100, w=text_texture.w, h=text_texture.h))

            self.renderer.present()

