from pkg_resources import resource_string
from math import sin, cos, sqrt, fabs, pi, atan, atan2, fabs
from sdl2hl import mixer
import stickman, kite

class player(object):

    def __init__(self, geometry):
        self.geometry = geometry
        self.x = 0
        self.y = 0
        self.grounded = True

        self.gravity = -130

        self.speed = 10
        self.angle = 0
        self.kite_angle = 0
        self.forward_kite_force = 75
        self.top_kite_force = 75
        self.drag_coefficient = 0.00001
        self.max_speed = 550

        self.stickman = stickman.StickMan()
        self.kite = kite.kite()

        self.board_length = 20
        
        self.snow_sound = mixer.Chunk(resource_string(__name__, 'res/sound/snow.ogg'))
        self.channel = self.snow_sound.play(loops=-1)

    def update(self, dt, angle):

        shoulder_x, shoulder_y = self.stickman.shoulder_pos

        # rise = mouse_y - shoulder_y
        # run = mouse_x - shoulder_x
        #
        # self.kite_angle = atan2(rise, run)
        self.kite_angle = angle

        slope = self.geometry.slope(self.x)

        #kite force
        # f = self.kite_force * cos(self.kite_angle)
        f = self.forward_kite_force - (self.forward_kite_force - self.top_kite_force) * (fabs(self.kite_angle) / (pi / 2))
        kfx = f * cos(self.kite_angle)
        kfy = f * sin(self.kite_angle)

        #drag force
        d = - 1* self.drag_coefficient * self.speed * self.speed
        dfx = d * cos(self.angle)
        dfy = d * sin(self.angle)

        if self.grounded:
            #we started on the ground
            self.angle = atan(slope)
            vel_x = self.speed * cos(self.angle) + (kfx + dfx) * dt
            vel_y = self.speed * sin(self.angle) + sin(self.angle) * self.gravity * dt + (kfy + dfy) *dt
            self.x += vel_x * dt
            self.y += vel_y * dt

            self.speed = sqrt(vel_x*vel_x + vel_y*vel_y)
            if self.speed > self.max_speed:
                self.speed = self.max_speed
            # self.angle = tanh(vel_y/vel_x)

            new_height = self.geometry.height(self.x)
            if self.y <= new_height:
                self.y = new_height
                self.grounded = True
            else:
                self.channel.pause()
                self.grounded = False
        else:
            #we started in the air
            vel_x = self.speed * cos(self.angle) + (kfx + dfx) * dt
            vel_y = self.speed * sin(self.angle) + self.gravity * dt + (kfy + dfy) * dt
            self.x += vel_x * dt
            self.y += vel_y * dt

            self.speed = sqrt(vel_x*vel_x + vel_y*vel_y)
            if self.speed > self.max_speed:
                self.speed = self.max_speed
            self.angle = atan2(vel_y, vel_x)

            new_height = self.geometry.height(self.x)
            if self.y <= new_height:
                self.y = new_height
                self.grounded = True

                #we have landed. kill some speed
                self.channel.resume()
                new_angle = atan(self.geometry.slope(self.x))
                landing_angle = fabs(new_angle - self.angle)
                self.speed *= cos(landing_angle)
                print landing_angle * 180 / pi


            else:
                self.grounded = False

        self.stickman.update(self.x, self.y, self.angle, self.kite_angle)
        kite_x , kite_y = self.stickman.reach_pos
        self.kite.update(kite_x, kite_y, self.kite_angle)

    def draw(self, renderer, camera):
        self.stickman.draw(renderer, camera)
        self.kite.draw(renderer, camera)

        # draw the board
        p1x = self.x + cos(self.angle) * self.board_length
        p1y = self.y + sin(self.angle) * self.board_length

        p2x = self.x - cos(self.angle) * self.board_length
        p2y = self.y - sin(self.angle) * self.board_length


        renderer.draw_color = (255, 0, 0, 255)
        renderer.draw_line(camera.to_screen_x(p1x), camera.to_screen_y(p1y), camera.to_screen_x(p2x), camera.to_screen_y(p2y))

