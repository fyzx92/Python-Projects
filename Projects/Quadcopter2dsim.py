#
# Authored by Bryce Burgess
#
# 2d quadcopter simulation

import math
from matplotlib.pyplot import plot as plt



def AddVectors(*x): # [ ] TODO Test that this works as intended
    out = []
    for i in x:
        sum = 0
        for j in i:
            sum += j
        out.append(sum)
    return out

def AddVector(x, y):
    out = []
    for i in list(range(len(x))):
        out.append(x[i] + y[i])
    return out
        

class Propeller():
    def ___init___(self):
        self.mass = 1
        self.thrust_range = (0,1000)
        self.thrust = 0

    def Thrust(self, speed_change):
        self.thrust += min(speed_change, self.thrust_range[1])
        self.thrust = max(self.thrust, self.thrust_range[0])

class Quadcopter():
    def ___init___(self):
        self.prop1 = Propeller()
        self.prop1.__init__()
        self.prop2 = Propeller()
        self.prop2.__init__()

        self.arm1_coord_local = (2,0)
        self.arm2_coord_local = (-2,0)

        self.mass = 3 + self.prop1.mass + self.prop2.mass

        self.pos = [0,0]
        self.vel = [0,0]
        self.acc = [0,0]
        self.angle   = 0
        self.ang_vel = 0
        self.ang_acc = 0



    # Getting and applying forces
    def ApplyForce(self, force, *force_args, **force_kwargs):
        self.acc = AddVectors(self.acc, force(*force_args, **force_kwargs)/self.mass)

    def ApplyTorque(self, torque, *torque_args, **torque_kwargs):
        self.ang_acc += torque(*torque_args, **torque_kwargs)/(self.mass*self.arm1_coord_local[0]**2)

    def PropellerForces(self, force1, force2):
        # sets thrust from each propeller
        self.prop1.Thrust(force1)
        self.prop2.Thrust(force2)

    def CalcLinAcc(self):
        # calculates the linear acceleration from propellers
        accel = (self.prop1.thrust + self.prop2.thrust)/(2.0 * self.mass)
        return accel

    def CalcAngAcc(self):
        # calculates the angular acceleration from propellers
        angular_accel = self.prop1.thrust/(self.prop1.mass*self.arm1_coord_local[0]**2) - self.prop2.thrust/(self.prop2.mass*self.arm2_coord_local[0]**2)
        return angular_accel
    
    def Thrust(self, strength): 
        # linear force from propellers, local frame up
        self.PropellerForces(strength/2.0, strength/2.0)

    def Torque(self, strength):
        # torque from propellers
        self.PropellerForces(strength/2.0, -strength/2.0)





    # Translating forces into velocities and positions
    def UpdatePos(self):
        self.vel = AddVector(self.vel, self.acc)
        self.pos = AddVector(self.pos, self.vel)
    
    def UpdateAng(self):
        self.ang_vel = AddVector(self.ang_vel, self.ang_acc)
        self.angle = AddVector(self.angle, self.ang_vel)



    # Guiding self to targets
    def Control(self, K_p, target_pos, K_v, target_vel, copter_ang, omega):

        def local_to_global(lpos, angle):
            return (lpos[0]-lpos[1]*math.tan(angle))/(1-math.sin(angle)*math.tan(angle))

        def global_to_local(gpos, angle):
            return (gpos[0]-gpos[1]*math.tan(angle))/(1-math.sin(angle)*math.tan(angle))


        # position change stimulated by accel, inhibited by momentum/vel

        # gives force in x/y, not left/right rotors
        F_desired = AddVectors(K_p*target_pos, -K_p*copter_pos, K_v*target_vel, -K_v*copter_vel, g)

        # direction of approach
        traj_angle = math.atan2(F_desired[1]/F_desired[0]) + math.atan2(target_vel[1]/target_vel[0]) 

        T_desired = K_a(traj_angle-self.angle) 

        # copter needs to tilt to move laterally




# SIMULATION
dt = 0.1
g = (0, -1)
copter_pos = [0,0]
copter_vel = [0,0]
copter_acc = [0,0] - g
copter_tor = 0
copter_omg = 0
copter_ang = 0

