import sys

import sdl2hl

import geometry
import player
import clock


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

    def run(self):

        tangent_x = 0

        while True:
            dt = self.clock.tick(60)
            for event in sdl2hl.events.poll():
                if event.type == sdl2hl.QUIT:
                    sdl2hl.quit()
                    sys.exit()
                elif event.type == sdl2hl.KEYDOWN and event.keycode == sdl2hl.KeyCode.left:
                    tangent_x -= 1
                elif event.type == sdl2hl.KEYDOWN and event.keycode == sdl2hl.KeyCode.right:
                    tangent_x += 1


            #handle the player
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
            self.renderer.draw_color = (255, 0, 0, 255)
            r = sdl2hl.Rect(int(self.player.x) - 5, self.window_size[1] - int(self.player.y) - 5, 10, 10)
            self.renderer.draw_rect(r)

            self.renderer.present()
