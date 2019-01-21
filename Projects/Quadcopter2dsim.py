#
# Authored by Bryce Burgess
#
# 2d quadcopter simulation

import math
from matplotlib.pyplot import plot as plt

class Propeller():
    def ___init___(self):
        self.mass = 1
        self.rps_range = [0,1000]
        self.rps = 0
    def thrust(self, speed_change):
        self.rps += max(0,new_speed)

class Quadcopter():
    def ___init___(self):
        self.prop1 = Propeller()
        self.prop2 = Propeller()

        self.arm1_coord_local = [2,0]
        self.arm2_coord_local = [-2,0]

        self.mass = 3 + self.prop1.mass + self.prop2.mass




    def controller():

        def local_to_global(lpos, angle):
            return (lpos[0]-lpos[1]*tan(angle))/(1-sin(angle)*tan(angle))

        def global_to_local(gpos, angle):
            return (gpos[0]-gpos[1]*tan(angle))/(1-sin(angle)*tan(angle))
        #position change stimulated by accel, inhibited by momentum/vel

        # gives force in x/y, not left/right rotors
        F = K_p*(target_pos - copter_pos) + K_v*(target_vel - copter_vel) + g

        traj_angle = atan(F[1]/F[0]) + atan(target_vel[1]/target_vel[0])#direction of approach

        # creates rotational force on copter
        T = prop1.rps*prop1.arm1_coord_local - prop2.rps*prop2.arm2_coord_local
        # copter needs to tilt to move laterally




# SIMULATION
dt = 0.1
g = [0,1]
copter_pos = [0,0]
copter_vel = [0,0]
copter_acc = [0,0] - g
copter_tor = 0
copter_omg = 0
copter_ang = 0

def update_angle():
    copter_ang += omega*dt + 0.5*copter_tor*dt**2

def update_position():
    copter_pos[0] += copter_vel[0] + 0.5*copter_acc[0]*dt**2
    copter_pos[1] += copter_vel[1] + 0.5*copter_acc[1]*dt**2

def update_vel():
    copter_vel[0] += copter_acc[0]
