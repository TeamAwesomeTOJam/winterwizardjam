from math import sin, cos, sqrt, fabs, pi, atan, atan2

class player(object):

    def __init__(self, geometry):
        self.geometry = geometry
        self.x = 0
        self.y = 0
        self.grounded = True

        self.gravity = -20

        self.speed = 10
        self.angle = 0
        self.kite_angle = 0
        self.kite_force = 20
        self.drag_coificient = 0.001

    def update(self, dt):
        slope = self.geometry.slope(self.x)

        #kite force
        f = self.kite_force * cos(self.kite_angle)
        kfx = f * cos(self.kite_angle)
        kfy = f * sin(self.kite_angle)

        #drag force
        d = - 1* self.drag_coificient * self.speed * self.speed
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
            # self.angle = tanh(vel_y/vel_x)

            new_height = self.geometry.height(self.x)
            if self.y <= new_height:
                self.y = new_height
                self.grounded = True
            else:
                self.grounded = False
        else:
            #we started in the air
            vel_x = self.speed * cos(self.angle) + (kfx + dfx) * dt
            vel_y = self.speed * sin(self.angle) + self.gravity * dt + (kfy + dfy) * dt
            self.x += vel_x * dt
            self.y += vel_y * dt

            self.speed = sqrt(vel_x*vel_x + vel_y*vel_y)
            self.angle = atan2(vel_y, vel_x)

            new_height = self.geometry.height(self.x)
            if self.y <= new_height:
                self.y = new_height
                self.grounded = True

                #we have landed. kill some speed
                new_angle = atan(self.geometry.slope(self.x))
                landing_angle = fabs(new_angle - self.angle)
                self.speed *= cos(landing_angle)
                print landing_angle * 180 / pi


            else:
                self.grounded = False

