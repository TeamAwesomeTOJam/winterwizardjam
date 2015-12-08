import os, sys
import math
import pickle

import sdl2hl
import sdl2hl.gfx


class StickMan(object):

    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
    
        self.color = (255, 255, 255, 255)
        self.width = 2
        
        self.upper_arm_length = 9
        self.lower_arm_length = 9
        self.upper_leg_length = 12
        self.lower_leg_length = 12
        self.head_radius = 8
        self.torso_length = 16
        self.foot_offset = 6
        self.hip_height = 16
        
        self.torso_angle = -math.pi / 2.0
        self.l_shoulder_angle = 1
        self.r_shoulder_angle = 2
        self.l_elbow_angle = 1
        self.r_elbow_angle = 2
        self.l_hip_angle = 1
        self.r_hip_angle = 2
        self.l_knee_angle = 1
        self.r_knee_angle = 2
        
    def _get_endpoint(self, start, angle, length):
        x = int(start[0] + length * math.cos(angle))
        y = int(start[1] + length * math.sin(angle))
        return (x, y)
    
    def _get_leg_posture(self, side):
        if side == 'r': # no idea what I'm doing here
            angle = self.angle + math.pi/2.0
        elif side == 'l':
            angle = self.angle - math.pi/2.0
        
        # use law of cosines to get hip-foot distance
        hip_foot_distance = (self.hip_height**2 + self.foot_offset**2 
                - 2 * self.hip_height * self.foot_offset * math.cos(angle))**0.5
                
        # use law of cosines to find hip angle
        hip_angle = math.acos((self.upper_leg_length**2 + hip_foot_distance**2 - self.lower_leg_length**2)
                               / (2 * self.upper_leg_length * hip_foot_distance))
                               
        # use law of cosines to find hip angle
        knee_angle = math.acos((self.lower_leg_length**2 + self.upper_leg_length**2 - hip_foot_distance**2)
                               / (2 * self.lower_leg_length * self.upper_leg_length))
        if side == 'l':
            hip_angle = math.pi - hip_angle # this is totally wrong
        return (hip_angle, knee_angle)
    
    def draw(self, renderer):
        self.l_hip_angle, self.l_knee_angle = self._get_leg_posture('l')
        self.r_hip_angle, self.r_knee_angle = self._get_leg_posture('r')
    
        hip_pos = (self.x, self.y - self.hip_height)
        shoulder_pos = self._get_endpoint(hip_pos, self.torso_angle, self.torso_length * 0.9)
        neck_pos = self._get_endpoint(hip_pos, self.torso_angle, self.torso_length)
        head_pos = self._get_endpoint(hip_pos, self.torso_angle, self.torso_length + self.head_radius)
        l_elbow_pos = self._get_endpoint(shoulder_pos, self.torso_angle + self.l_shoulder_angle, self.upper_arm_length) 
        r_elbow_pos = self._get_endpoint(shoulder_pos, self.torso_angle + self.r_shoulder_angle, self.upper_arm_length)
        l_hand_pos = self._get_endpoint(l_elbow_pos, self.torso_angle + self.l_shoulder_angle + self.l_elbow_angle, self.lower_arm_length)
        r_hand_pos = self._get_endpoint(r_elbow_pos, self.torso_angle + self.r_shoulder_angle + self.r_elbow_angle, self.lower_arm_length)
        l_knee_pos = self._get_endpoint(hip_pos, self.l_hip_angle, self.upper_leg_length)
        r_knee_pos = self._get_endpoint(hip_pos, self.r_hip_angle, self.upper_leg_length)
        l_foot_pos = self._get_endpoint(l_knee_pos, self.l_hip_angle + self.l_knee_angle, self.lower_leg_length)
        r_foot_pos = self._get_endpoint(r_knee_pos, self.r_hip_angle + self.r_knee_angle, self.lower_leg_length)

        lines = [(hip_pos, neck_pos),
                 (shoulder_pos, l_elbow_pos),
                 (shoulder_pos, r_elbow_pos),
                 (l_elbow_pos, l_hand_pos),
                 (r_elbow_pos, r_hand_pos),
                 (hip_pos, l_knee_pos),
                 (hip_pos, r_knee_pos),
                 (l_knee_pos, l_foot_pos),
                 (r_knee_pos, r_foot_pos)]
        renderer.draw_color = self.color
        for i, (start, end) in enumerate(lines):
            renderer.draw_line(start[0], start[1], end[0], end[1])
        primitives = sdl2hl.gfx.GfxPrimitives(renderer)
        primitives.draw_circle(head_pos[0], head_pos[1], self.head_radius, self.color)

