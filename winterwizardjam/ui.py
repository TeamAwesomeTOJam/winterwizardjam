import sdl2hl
from pkg_resources import resource_string


class Button(object):

    def __init__(self, x, y, width, height, colour = (255, 255, 255, 255), selected = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.selected = selected
        self.colour = colour

        self.factor = 0.8

    def intersect_point(self,x,y):
        return self.x < x < self.x + self.width and self.y < y < self.y + self.height

    def draw(self, renderer):
        renderer.draw_color = self.colour

        r = sdl2hl.Rect(self.x, self.y, self.width, self.height)
        renderer.draw_rect(r)

        if self.selected:
            x = int(self.x + self.width * (1 - self.factor) / 2)
            y = int(self.y + self.height * (1 - self.factor) / 2)
            w = int(self.width * self.factor)
            h = int(self.height * self.factor)

            r = sdl2hl.Rect(x, y, w, h)
            renderer.fill_rect(r)


class Text(object):

    def __init__(self, x, y, text, size, colour = (255,255,255,255)):
        self.x = x
        self.y = y
        self.text = text
        self.size = size
        self.font = sdl2hl.ttf.Font(resource_string(__name__, 'res/font/LiberationSans-Regular.ttf'), size)
        self.colour = colour
        if self.text:
            self.surface = self.font.render_solid(self.text, self.colour)
            self.width = self.surface.w
            self.height = self.surface.h
        else:
            self.surface = None
            self.height = 0
            self.width = 0

    def set_text(self, text):
        self.text = text
        if self.text:
            self.surface = self.font.render_solid(self.text, self.colour)
            self.width = self.surface.w
            self.height = self.surface.h
        else:
            self.surface = None
            self.width = 0
            self.height = 0

    def draw(self, renderer):
        if self.text:
            text_texture = sdl2hl.Texture.from_surface(renderer, self.surface)
            renderer.copy(text_texture, dest_rect=sdl2hl.Rect(x=self.x, y=self.y, w=text_texture.w, h=text_texture.h))
