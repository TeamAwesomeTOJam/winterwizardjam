import sys

import sdl2hl

import geometry


class game(object):

    def __init__(self):
        sdl2hl.init()

        self.geometry = geometry.geometry()

        self.window_size = (1920, 1080)

        self.window = sdl2hl.Window(title="Winter Wizard Jam",w=self.window_size[0], h=self.window_size[1])
        #self.renderer = sdl2hl.Renderer(self.window,-1, sdl2hl.RendererFlags.presentvsync)
        self.renderer = sdl2hl.Renderer(self.window)

    def run(self):
        start_time = sdl2hl.timer.get_ticks()
        frames = 0
        while True:
            frames += 1
            for event in sdl2hl.events.poll():
                if event.type == sdl2hl.QUIT:
                    end_time = sdl2hl.timer.get_ticks()
                    print 1000.0*frames / (end_time - start_time)
                    sdl2hl.quit()
                    sys.exit()



            self.renderer.draw_color = (0,0,0,255)
            self.renderer.clear()
            self.renderer.draw_color = (255,255,255,255)
            rects = []
            for x in range(0, self.window_size[0]):
                y = self.window_size[1] - int(self.geometry.height(x))
                #self.renderer.draw_point(x,y)
                r = sdl2hl.Rect(x, y, 0, int(self.geometry.height(x)))
                rects.append(r)
                # self.renderer.draw_rect(r)
            self.renderer.draw_rects(*rects)

            self.renderer.present()
