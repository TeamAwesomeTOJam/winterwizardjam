class camera(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.zoom = 1

    def to_world_x(self, x):
        return self.x + x * self.zoom

    def to_world_y(self, y):
        return self.y + (self. height - y) * self.zoom

    def to_world(self, x, y):
        world_x = self.to_world_x(x)
        world_y = self.to_world_y(y)

        return world_x, world_y

    def to_screen_x(self, x):
        return int((x - self.x) / self.zoom)

    def to_screen_y(self, y):
        return int(self.height - (y - self.y) / self.zoom)

    def to_screen(self, x, y):
        screen_x = self.to_screen_x(x)
        screen_y = self.to_screen_y(y)

        return screen_x, screen_y