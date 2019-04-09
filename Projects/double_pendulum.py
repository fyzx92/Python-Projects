#!/usr/bin/python3

# authored by Bryce Burgess
# 27/9/2018
# simulate a double pendulum
# copy that pendulum with error
# see how the initial error can be reduced with subsequent measurements
# can use error threshold on the pendulum (easier), or periodic(more useful)

import matplotlib.animation as ani
import matplotlib.pyplot as plt
import numpy as np
from math import pi, sin, cos



def AddVectors(*x):
    out = [0]*len(x[0])
    for i in x:
        k = 0
        #print("i = {}\n".format(i))
        for j in i:
            #print("j = {}\n".format(j))
            out[k] += j
            k += 1
    return out


# ESTABLISHING CLASSES
class Pendulum:
    # initiate starting position and constant parameters
    def __init__(self,
                 pivot = [0,0],
                 angle = pi/6.0,
                 mass = 1,
                 length = 1,
                 angular_vel = 0):
        
        self.mass = mass
        self.angle = angle # measured clockwise from downard y axis
        self.angular_vel = angular_vel
        self.angular_acc = 0
        self.length = length
        self.pivot = pivot
        self.position = self.get_position()
        
    #calculate position (x,y) of the pendulum
    def get_position(self):
        self.position = [self.pivot[0] + self.length*sin(self.angle), 
                         self.pivot[1] - self.length*cos(self.angle)]
        
        if self.angle == pi/2.0 or self.angle == -pi/2.0: self.position[1] = self.pivot[1] 
        if self.angle == 0 or self.angle == pi: self.position[0] = self.pivot[0] 
        
        return self.position
    
    def get_angle(self):
        return self.angle

    # Euler integration to get angle from acceleration
    def update_angle(self):
        self.angular_vel += self.angular_acc
        self.angle += self.angular_vel
        
    # Apply arbitrary force
    def apply_force(self, force, *force_args, **force_kwargs):
        if not force: return
        
        f = force
        if force_args or force_kwargs:
            f = force(*force_args, **force_kwargs)
        f[:] = [i / self.mass for i in f]
        
        self.angular_acc += np.arctan2(f[1], f[0])

    def force_from_pivot(self, g):
        return [-self.mass*self.g[0]*cos(self.angle)*sin(self.angle), 
                -self.mass*self.g[0]*cos(self.angle)*cos(self.angle)]
    
    def force_on_pivot(self, g):
        # f = force_from_pivot(g)
        # f = [-i for i in f]
        # return f
        return [self.mass*self.g[0]*cos(self.angle)*sin(self.angle), 
                self.mass*self.g[0]*cos(self.angle)*cos(self.angle)]

    # Print data about pendulum
    def print_status(self, all = False):
        if all:
            print("mass is %d"% (self.mass))
            print("length is %d"% (self.length))
            print("pivot is %d"% (self.pivot))
        print("angle is %d"% (self.angle))
        print("angular velocity is %d"% (self.angular_vel))


class Double_Pend():
    def __init__(self):
        self.origin = (0,0)
        self.p1 = Pendulum(self.origin, angle = pi/6)
        self.p2 = Pendulum(self.p1.get_position(), angle = pi/3)
        self.positions = []

    def get_ang_acc(self, g=[0,-1]):
        # TODO one should be p1 the other should be p2 - which is which?
        num1 = -g[1]*(2*self.p1.mass + self.p2.mass)*sin(self.p1.angle)
        num2 = -self.p2.mass*g[1]*sin(self.p1.angle-2*self.p2.angle)
        num3 = -2*self.p2.mass*sin(self.p1.angle-self.p2.angle) 
        num4 = self.p2.angular_vel**2 * self.p2.length + self.p1.angular_vel**2 * self.p1.length * cos(self.p1.angle - self.p2.angle)
        den = 2*self.p1.mass + self.p2.mass*(1-cos(2*(self.p1.angle-self.p2.angle)))

        self.p1.angular_acc = (num1 + num2 + num3*num4)/(self.p1.length*den)
        
        num1 = 2*sin(self.p1.angle-self.p2.angle)
        num2 = self.p1.angular_vel**2 * self.p1.length * (self.p1.mass + self.p2.mass)
        num3 = g[1]*(self.p1.mass+self.p2.mass)*cos(self.p1.angle)
        num4 = self.p2.angular_vel**2 * self.p2.length * self.p2.mass * cos(self.p1.angle - self.p2.angle)

        self.p1.angular_acc = num1*(num2 + num3 + num4)/(self.p2.length*den)


    def copy_modify(self, angle_diff = [0,0]):
        #copy step
        copy = Double_Pend()
        copy.origin = self.origin
        copy.p1 = self.p1
        copy.p2 = self.p2

        # modify step
        copy.p1.angle += angle_diff[0]
        copy.p2.angle += angle_diff[1]

        return copy
    
    def record(self):
        self.positions.append((self.p1.get_position(), self.p2.get_position()))
    
    def record_to_file(self):
        pass
    
    def get_record(self):
        return self.positions()


class Simulation():
    def __init__(self, dur = 7000):
        self.d = Double_Pend()
        self.duration = dur
        self.g = [0,-1]
    
    def display(self):
        plt.plot()
        return None

    def simulate_analytic(self, dp):
        dp.get_ang_acc(self.g)
        dp.p1.update_angle()
        dp.p2.update_angle()
        dp.p2.pivot = self.d.p1.get_position()

    def simulate_numeric(self, dp):
            
        # Apply gravitational and reaction forces
        dp.p2.apply_force(self.g)
        dp.p1.apply_force(self.g)
        dp.p2.apply_force(dp.p1.force_from_pivot(self.g))
        dp.p1.apply_force(dp.p2.force_on_pivot(self.g))
        
        # Update angle from acc
        dp.p1.update_angle()
        dp.p2.update_angle()

        # ensure that pivots are in correct places
        dp.p1.pivot = [0,0]
        dp.p2.pivot = self.d.p1.get_position()

    def simulate_error_split(self,
                             sim = simulate_numeric,
                             measure_error = pi/100,
                             n_pends = 10,
                             error_threshold = pi/20.0 # angle
                             # error_threshold = 0.1 # position
                             ):
        
        dps = []
        for i in range(-n_pends/2,0):
            dps.append(self.d)
            dps[i] = dps[i].copy_modify([0, measure_error*i/n_pends])
            
        for i in range(1,n_pends/2+1):
            dps.append(self.d)
            dps[i] = dps[i].copy_modify([0, measure_error*i/n_pends])
            
        for t in range(self.duration):
            
            sim(self.d)
            for i in range(len(dps)):
                sim(dps[i])
            # Record positions
            self.d.record()
            for i in range(len(dps)):
                dps[i].record()
                    
            #find errors
            for i in range(len(dps)):
                error = [0,0]
                
                # use get_position
                error[0] += np.sqrt(abs(self.d.p1.get_position()[0]**2 - 
                                dps[i].p1.get_angle()[0]**2))
                
                error[0] += np.sqrt(abs(self.d.p1.get_position()[1]**2 - 
                                dps[i].p1.get_angle()[1]**2))
                
                error[1] += np.sqrt(abs(self.d.p2.get_position()[0]**2 - 
                                dps[i].p1.get_angle()[0]**2))
                
                error[1] += np.sqrt(abs(self.d.p2.get_position()[1]**2 - 
                                dps[i].p1.get_angle()[1]**2))
                
                # use angles
                error[0] += self.d.p1.get_angle() - dps[i].p1.get_angle()
                error[1] += self.d.p2.get_angle() - dps[i].p2.get_angle()
                
            
            if error[0] > error_threshold or error[1] > error_threshold:
                # make new pendulums with smaller initial error
                dps = []
                for i in range(-n_pends/2,0):
                    dps.append(self.d)
                    dps[i] = dps[i].copy_modify([0, error_threshold*i/n_pends])
            
                for i in range(1,n_pends/2+1):
                    dps.append(self.d)
                    dps[i] = dps[i].copy_modify([0, error_threshold*i/n_pends])



    def simulate_time_split(self,
                            sim = simulate_numeric,
                            measure_time = 100,
                            measure_error = pi/100,
                            n_pends = 10
                            ):
        
        dps = []
        for i in range(-n_pends/2,0):
            dps.append(self.d)
            dps[i] = dps[i].copy_modify([0, measure_error*i/n_pends])
            
        for i in range(1,n_pends/2+1):
            dps.append(self.d)
            dps[i] = dps[i].copy_modify([0, measure_error*i/n_pends])
        
        for t in range(self.duration):
            
            # Simulate
            sim(self.d)
            for i in enumerate(dps):
                sim(dps[i])

            # Record positions
            if t%measure_time == 0:
                self.d.record()
                for i in enumerate(dps):
                    dps[i].record()
                    
                #find errors
                for i in enumerate(dps):
                    error = [0,0]
                    
                    # use get_position
                    self.d.p1.get_position()[0] - dps[i].p1.get_angle()[0]
                    self.d.p1.get_position()[1] - dps[i].p1.get_angle()[1]
                
                    self.d.p2.get_position()[0] - dps[i].p1.get_angle()[0]
                    self.d.p2.get_position()[1] - dps[i].p1.get_angle()[1]
                
                    # use angles
                    self.d.p1.get_angle() - dps[i].p1.get_angle()
                    self.d.p2.get_angle() - dps[i].p2.get_angle()
                    
                    if error > measure_error:
                        # get initial deviance of pendulum
                        # create new pendulums
                        pass
                    
                    
                    
                #
                dps = []
                for i in range(-n_pends/2,0):
                    dps.append(self.d)
                    dps[i] = dps[i].copy_modify([0, error_threshold*i/n_pends])
            
                for i in range(1,n_pends/2+1):
                    dps.append(self.d)
                    dps[i] = dps[i].copy_modify([0, error_threshold*i/n_pends])
