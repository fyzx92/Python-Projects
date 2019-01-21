#!/usr/bin/python3

import matplotlib.animation as ani
import numpy as np
from math import pi, sin, cos


# ESTABLISHING CLASSES
class Pendulum:
	def __init__(self, pivot = [0,0], angle = pi/6.0, mass=1, length=1, angular_vel=0):
		self.mass = mass
		self.angle = angle # measured clockwise from usual x axis
		self.angular_vel = angular_vel
		self.length = length
		self.pivot = pivot
		self.position = self.get_position()
		
	def get_position(self):
		self.position = [0,0]
		self.position = [self.pivot[0] + self.length*cos(self.angle), 
						self.pivot[1] + self.length*sin(self.angle)]

		if self.angle == pi/2.0 or self.angle == -pi/2.0: self.position[0] = self.pivot[0] 
		if self.angle == 0 or self.angle == pi: self.position[1] = self.pivot[1] 
		return self.position
		
	def update_angle(self, angular_accel):
		self.angular_vel += angular_accel
		self.angle += self.angular_vel
	
	def update_angle2(self, angular_accel):
		#Runge Kutta
		pass

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

		self.p1 = Pendulum()
		self.p1.__init__(self.origin, pi/6)

		self.p2 = Pendulum()
		self.p2.__init__(self.p1.get_position(), pi/3)

	def get_ang_acc(self, p1, p2, g=1):
		num1 = -g*(2*self.p1.mass + self.p2.mass)*sin(self.p1.angle)
		num2 = -self.p2.mass*g*sin(self.p1.angle-2*self.p2.angle)
		num3 = -2*self.p2.mass*sin(self.p1.angle-self.p2.angle) 
		num4 = self.p2.angular_vel**2 * self.p2.length + self.p1.angular_vel**2 * self.p1.length * cos(self.p1.angle - self.p2.angle)
		den = 2*self.p1.mass + self.p2.mass*(1-cos(2*(self.p1.angle-self.p2.angle)))

		aa1 = (num1 + num2 + num3*num4)/(p1.length*den)


		num1 = 2*sin(p1.angle-p2.angle)
		num2 = p1.angular_vel**2 * p1.length * (p1.mass + p2.mass)
		num3 = g*(p1.mass+p2.mass)*cos(p1.angle)
		num4 = p2.angular_vel**2 * p2.length * p2.mass * cos(p1.angle - p2.angle)

		aa2 = num1*(num2 + num3 + num4)/(p2.length*den)

		return [aa1, aa2]


# INITIALIZING
double_pend = Double_Pend()



# PREPPING SIMULATION
simulation_time = 10
dt = 0.01
t = 0.0

# RUNNING SIMULATION
g = 1
positions = []
while(t < simulation_time):
	aa = double_pend.get_ang_acc(double_pend.p1, double_pend.p2, g)
	double_pend.p1.update_angle(aa[0])
	double_pend.p2.update_angle(aa[1])

	double_pend.p2.pivot = double_pend.p1.get_position()

	positions.append((double_pend.p1.get_position(), double_pend.p2.get_position()))

	t += dt
