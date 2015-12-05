import sys

import sdl2hl

import geometry


class game(object):

    def __init__(self):
        sdl2hl.init()

        self.geometry = geometry.geometry()

        self.window_size = (1024, 576)

        self.window = sdl2hl.Window(title="Winter Wizard Jam",w=self.window_size[0], h=self.window_size[1])
        self.renderer = sdl2hl.Renderer(self.window)

    def run(self):
        while True:
            for event in sdl2hl.events.poll():
                if event.type == sdl2hl.QUIT:
                    sdl2hl.quit()
                    sys.exit()



            self.renderer.draw_color = (0,0,0,255)
            self.renderer.clear()
            self.renderer.draw_color = (255,255,255,255)
            for x in range(0, self.window_size[0]):
                y = self.window_size[1] - int(self.geometry.height(x))
                self.renderer.draw_point(x,y)

            self.renderer.present()
