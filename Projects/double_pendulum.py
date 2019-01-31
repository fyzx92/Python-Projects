#!/usr/bin/python3

import matplotlib.animation as ani
import numpy as np
from math import pi, sin, cos


# ESTABLISHING CLASSES
class Pendulum:
	# initiate starting position and constant parameters
	def __init__(self, pivot = [0,0], angle = pi/6.0, mass=1, length=1, angular_vel=0):
		self.mass = mass
		self.angle = angle # measured clockwise from usual x axis
		self.angular_vel = angular_vel
		self.angular_acc = 0
		self.length = length
		self.pivot = pivot
		self.position = self.get_position()
		
	# calculate position (x,y) of the pendulum
	def get_position(self):
		self.position = [self.pivot[0] + self.length*cos(self.angle), 
						self.pivot[1] + self.length*sin(self.angle)]

		if self.angle == pi/2.0 or self.angle == -pi/2.0: self.position[0] = self.pivot[0] 
		if self.angle == 0 or self.angle == pi: self.position[1] = self.pivot[1] 
		return self.position
	
	# Euler integration to get angle from acceleration
	def update_angle(self):
		self.angular_vel += self.angular_acc
		self.angle += self.angular_vel
	
	# [TODO] Runge Kutta integration alternative
	def update_angle2(self, angular_accel):
		#Runge Kutta
		pass

	# Apply arbitrary forces
	def apply_force(self, force, *force_nargs, **force_kwargs):
		cartesian_acc = [] 
		cartesian_acc.append(force(*force_nargs, **force_kwargs)[0]/self.mass)
		cartesian_acc.append(force(*force_nargs, **force_kwargs)[1]/self.mass)

		self.angular_acc += np.arctan2(cartesian_acc[1], cartesian_acc[0])

	def force_from_pivot(self, g):
		return [self.mass*g*np.cos(self.angle), -self.angle]

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

		self.p1 = Pendulum()
		self.p1.__init__(self.origin, angle = pi/6)

		self.p2 = Pendulum()
		self.p2.__init__(self.p1.get_position(), angle = pi/3)

	def get_ang_acc(self, p1, p2, g=1):
		num1 = -g*(2*self.p1.mass + self.p2.mass)*sin(self.p1.angle)
		num2 = -self.p2.mass*g*sin(self.p1.angle-2*self.p2.angle)
		num3 = -2*self.p2.mass*sin(self.p1.angle-self.p2.angle) 
		num4 = self.p2.angular_vel**2 * self.p2.length + self.p1.angular_vel**2 * self.p1.length * cos(self.p1.angle - self.p2.angle)
		den = 2*self.p1.mass + self.p2.mass*(1-cos(2*(self.p1.angle-self.p2.angle)))

		self.p1.angular_acc = (num1 + num2 + num3*num4)/(p1.length*den)
		


		num1 = 2*sin(p1.angle-p2.angle)
		num2 = p1.angular_vel**2 * p1.length * (p1.mass + p2.mass)
		num3 = g*(p1.mass+p2.mass)*cos(p1.angle)
		num4 = p2.angular_vel**2 * p2.length * p2.mass * cos(p1.angle - p2.angle)

		self.p1.angular_acc = num1*(num2 + num3 + num4)/(p2.length*den)


	def copy_modify(self, angle_diff = [0,0], av_diff = [0,0], aa_diff = [0,0]):
		# copy step
		copy = Double_Pend()
		copy.origin = self.origin
		copy.p1 = self.p1
		copy.p2 = self.p2

		# modify step
		copy.p1.angle += angle_diff[0]
		copy.p1.angular_vel += av_diff[0]
		copy.p1.angular_acc += aa_diff[0]

		copy.p2.angle += angle_diff[1]
		copy.p2.angular_vel += av_diff[1]
		copy.p2.angular_acc += aa_diff[1]
		return copy


# INITIALIZING
double_pend = Double_Pend()

dp_copies = []
for i in range(10):
	dp_copies.append(Double_Pend())


#pend1 = Pendulum()
#pend2 = Pendulum()
#pend1.__init__()
#pend2.__init__(pivot=pend1.get_position)

# split by error or time interval
split_by_error = True
split_by_time = ~split_by_error

# PHYSICS
# gravity
g = 1

# PREPPING SIMULATION
simulation_time = 7000
measure_time = 100
t = 0

# allowed error
apos_error_threshold = pi/20.0
avel_error_threshold = pi/100.0
aacc_error_threshold = pi/50.0

# RUNNING SIMULATION 1 Analytic accel
positions = []
#for t in list(np.arange(0, simulation_time, dt)):
while(t < simulation_time):
	double_pend.get_ang_acc(double_pend.p1, double_pend.p2, g)
	double_pend.p1.update_angle()
	double_pend.p2.update_angle()

	double_pend.p2.pivot = double_pend.p1.get_position()

	positions.append((double_pend.p1.get_position(), double_pend.p2.get_position()))

	#if split_by_error:
	#	if abs(apos_error) > apos_error_threshold:
	#		pass
	#	if abs(avel_error) > apos_error_threshold:
	#		pass
	#	if abs(aacc_error) > apos_error_threshold:
	#		pass
	#elif split_by_time:
	#	if t%measure_time == 0:
			# find values
			# find close pendulums
			# (alt: find error each time, note when error is large)

	#		pass

	t += 1

# RUNNING SIMULATION 2 Simulated accel
t = 0

# allowed error
apos_error_threshold = pi/20.0
avel_error_threshold = pi/100.0
aacc_error_threshold = pi/50.0

# record positions of pendulums
positions = []
#for t in list(np.arange(0, simulation_time, dt)):
while(t < simulation_time):
	double_pend.p2.apply_force(g)
	double_pend.p1.apply_force(g)
	double_pend.p1.apply_force(-double_pend.p2.force_from_pivot(g)[0])

	double_pend.p1.update_angle()
	double_pend.p2.update_angle()

	double_pend.p1.pivot = [0,0]
	double_pend.p2.pivot = double_pend.p1.get_position()

	positions.append((double_pend.p1.get_position(), double_pend.p2.get_position()))

	#apos_error = [double_pend.p1.angle- , double_pend.p2.angle-]
	#avel_error = 
	#aacc_error = 

	#if split_by_error:
	#	if abs(apos_error) > apos_error_threshold or abs(avel_error) > apos_error_threshold or abs(aacc_error) > apos_error_threshold:
	#		pass

	#elif split_by_time:
	#	if t%measure_time == 0:
			# find values
			# find close pendulums
			# (alt: find error each time, note when error is large)

	#		pass

	t += 1







# ANIMATION
