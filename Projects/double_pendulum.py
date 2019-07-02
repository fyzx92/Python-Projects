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
    """
    *x: list of vectors to add together

    returns the resulting vector sum
    """
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
        """
        pivot: location of pivot in cartesian coordinates
        angle: starting angle for the pendulum (radians?)
        mass: mass at the end of the pendulum
        length: length of the pendulum
        angular_vel: starting angular velocity
        """
        
        self.mass = mass
        self.angle = angle # measured clockwise from downard y axis
        self.angular_vel = angular_vel
        self.angular_acc = 0
        self.length = length
        self.pivot = pivot
        self.position = self.get_position()
        
    # Calculate position (x,y) of the pendulum
    def get_position(self):
        """
        return the cartesian coordinates of the end point of the pendulum
        """
        self.position = [self.pivot[0] + self.length*sin(self.angle), 
                         self.pivot[1] - self.length*cos(self.angle)]
        
        if self.angle == pi/2.0 or self.angle == -pi/2.0: self.position[1] = self.pivot[1] 
        if self.angle == 0 or self.angle == pi: self.position[0] = self.pivot[0] 
        
        return self.position
    
    def get_angle(self):
        """
        return the angle of the pendulum
        """
        return self.angle

    def update_angle(self):
        """
        Euler integration to get angle from acceleration
        """
        self.angular_vel += self.angular_acc
        self.angle += self.angular_vel
        
    def apply_force(self, force, *force_args, **force_kwargs):
        """
        Apply arbitrary force
        """
        if not force: return
        
        if force_args or force_kwargs:
            force = force(*force_args, **force_kwargs)
        force[:] = [i / self.mass for i in force]
        
        self.angular_acc += np.arctan2(f[1], f[0])

    def force_from_pivot(self, g):
        """
        g: strength of gravity

        return the forces acting on a pendulum from connected pivot
        """
        return [-self.mass*self.g[0]*cos(self.angle)*sin(self.angle), 
                -self.mass*self.g[0]*cos(self.angle)*cos(self.angle)]
    
    def force_on_pivot(self, g):
        """
        g: strength of gravity
        
        return the force acting on the pivot from the pendulum
        """
        # f = force_from_pivot(g)
        # f = [-i for i in f]
        # return f
        return [self.mass*self.g[0]*cos(self.angle)*sin(self.angle), 
                self.mass*self.g[0]*cos(self.angle)*cos(self.angle)]

    # Print data about pendulum
    def print_status(self, all = False):
        """
        all: whether to print all attributes

        print the attributes of the pendulum
        """
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
        """
        from the position of each pendulum, calculate the angular acceleration
        """
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
    """
    angle_diff: how much to change the angles for the new pendulum

    copy and edit a double pendulum
    """
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
    
    def record_angle(self):
        self.positions.append((self.p1.get_angle(), self.p2.get_angle()))

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
                             n_pends = 2,
                             error_threshold = pi/20.0 # angle
                             # error_threshold = 0.1 # position
                             ):
        """
        sim: a function for how to calculate one step of the simulation
        measure_error: error range in each measurement
        error_threshold: error at which to start simulating a closer pendulum

        simulate the error, and take measurements at regular time intervals
        """
        

        dp_true = self.d
        dp_neg = self.d.copy_modify[-measure_error/2, -measure_error/2])
        dp_pos = self.d.copy_modify[measure_error/2, measure_error/2])
    
        for t in range(self.duration):
            
            sim(dp_true)
            sim(dp_neg)
            sim(dp_pos)
            
            # Record positions
            dp_true.record()
            dp_neg.record()
            dp_pos.record()
                    
            # calculate errors in angles
            pos_error = [0,0] 
            pos_error[0] += dp_true.p1.get_angle() - dp_pos.p1.get_angle()
            pos_error[1] += dp_true.p2.get_angle() - dp_pos.p2.get_angle()
                
            neg_error = [0,0] 
            neg_error[0] += dp_true.p1.get_angle() - dp_neg.p1.get_angle()
            neg_error[1] += dp_true.p2.get_angle() - dp_neg.p2.get_angle()
            
            if any(pos_error > error_threshold):
                # record t, with note of initial conditions

                # reinitialize dp_pos with smaller error
                dp_pos = # initial state of true with smaller error deviation
                
                # simulate dp_pos up to current time (still checking errors
                for u in range(t):
                    sim(dp_pos)

            if any(neg_error > error_threshold):
                # record t, with note of initial conditions

                # reinitialize dp_neg with smaller error
                dp_neg = # initial state of true with smaller error deviation
                
                # simulate dp_neg up to current time (still checking errors)
                for u in range(t):
                    sim(dp_neg)




    def simulate_time_split(self,
                            sim = simulate_numeric,
                            measure_time = 100,
                            measure_error = pi/100,
                            n_pends = 10
                            ):
        """
        sim: whether to solve numerically or analytically
        measure_time: how often to take measurements
        measure_error: error range in each measurement
        n_pends: number of pendulums to simulate

        simulate the error, and take measurements at regular time intervals
        """
        
        dp_true = self.d
        dps = []
        for i in range(n_pends):
            dps.append(self.d)
            dps[i] = dps[i].copy_modify([0, measure_error*i/n_pends])
        ref = n_pends//2
            
        # List for recording large errors
        # ???

        # Run simulation
        for t in range(self.duration):
            
            # Simulate
            sim(dp_true)
            for i,p in enumerate(dps):
                sim(dps[i])
            
            # Check timing intervals
            if t % measure_time == 0:
                
                # Record positions
                for i,d in enumerate(dps):
                    self.d.record_angle()
                
                # Check if out of error bounds
                for i,d in enumerate(dps):
                     if abs(dps[i] - dps[0]) > measure_error


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
