from math import sin, cos, tanh, sqrt, fabs, pi

class player(object):

    def __init__(self, geometry):
        self.geometry = geometry
        self.x = 0
        self.y = 0
        self.grounded = True

        self.gravity = -10

        self.speed = 100
        self.angle = 0

    def update(self, dt):
        slope = self.geometry.slope(self.x)

        if self.grounded:
            #we started on the ground
            self.angle = tanh(slope)
            vel_x = self.speed * cos(self.angle)
            vel_y = self.speed * sin(self.angle) + sin(self.angle) * self.gravity * dt
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
            vel_x = self.speed * cos(self.angle)
            vel_y = self.speed * sin(self.angle) + self.gravity * dt
            self.x += vel_x * dt
            self.y += vel_y * dt

            self.speed = sqrt(vel_x*vel_x + vel_y*vel_y)
            self.angle = tanh(vel_y/vel_x)

            new_height = self.geometry.height(self.x)
            if self.y <= new_height:
                self.y = new_height
                self.grounded = True

                #we have landed. kill some speed
                new_angle = tanh(self.geometry.slope(self.x))
                landing_angle = fabs(new_angle - self.angle)
                self.speed *= cos(landing_angle)
                print landing_angle * 180 / pi


            else:
                self.grounded = False

