import sdl2hl
from pkg_resources import resource_string

import clock
import sys


class End(object):

    def __init__(self, renderer):
        self.renderer = renderer

        self.font = sdl2hl.ttf.Font(resource_string(__name__, 'res/font/LiberationSans-Regular.ttf'), 24)

        self.name = ''
        self.max_name_length = 20

    def run(self, last_time, best_time, best_time_set):
        my_clock = clock.clock()
        while True:
            dt = my_clock.tick(60)

            for event in sdl2hl.events.poll():
                if event.type == sdl2hl.QUIT:
                    sdl2hl.quit()
                    sys.exit()
                elif event.type == sdl2hl.KEYDOWN and event.keycode == sdl2hl.KeyCode.escape:
                    sdl2hl.quit()
                    sys.exit()
                elif event.type == sdl2hl.KEYDOWN and event.keycode == sdl2hl.KeyCode.return_:
                    return
                elif event.type == sdl2hl.KEYDOWN and event.keycode == sdl2hl.KeyCode.backspace:
                    if self.name:
                        self.name = self.name[:-1]
                elif event.type == sdl2hl.TEXTINPUT:
                    if len(self.name) <= self.max_name_length:
                        self.name += event.text

            self.renderer.draw_color = (0, 0, 0, 255)
            self.renderer.clear()

            s = ''
            if best_time_set:
                if last_time <= best_time:
                    s = 'New personal best! Your time was ' + str(last_time) + ' seconds.'
                else:
                    s = 'Your time was ' + str(last_time) + ' seconds. Your personal best is ' + str(best_time) + ' seconds.'
            else:
                s = 'Your time was ' + str(last_time) + ' seconds.'

            text_texture = sdl2hl.Texture.from_surface(self.renderer, self.font.render_solid(s, (255,255,255,255)))
            self.renderer.copy(text_texture, dest_rect=sdl2hl.Rect(x=100, y=100, w=text_texture.w, h=text_texture.h))
            if self.name:
                text_texture = sdl2hl.Texture.from_surface(self.renderer, self.font.render_solid(self.name, (255,255,255,255)))
                self.renderer.copy(text_texture, dest_rect=sdl2hl.Rect(x=100, y=500, w=text_texture.w, h=text_texture.h))

            self.renderer.present()