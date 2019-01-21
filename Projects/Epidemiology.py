

import math
import random as rand

# [ ] TODO multiple diseases
# [x] change population based on travelers

class Disease():
	def ___init___(self, _inf_prob = 0.1, _death_prob = 0.01, _rec_prob = 0.05, _rein_prob = 0.001):
		self.infect_prob    = _inf_prob 
		self.death_prob     = _death_prob
		self.recover_prob   = _rec_prob
		self.reinfect_prob  = _rein_prob

# one box refers to all the people in a city with a given status
class Box():
	def ___init___(self, n):
		self.n = n
	
	# allows for the changing of people between different boxes
	def transfer_people(self, n, Box b):
		n_change = min(self.n, n_change)
		n_change = max(n_change, 0)
		self.n -= n_change
		b.n += n_change


# one city refers to all people within a region of all statuses
class City():
	def ___init___(self, n_unf, n_inf, n_rec = 0, n_dead = 0, connections = None):
		self.uninfected = Box()
		self.uninfected.n= n_unf

		self.infected = Box()
		self.infected = n_inf
		
		self.recovered = Box()
		self.recovered = n_rec
		
		self.dead = Box()
		self.dead = n_dead

		self.total = self.uninfected.n + self.infected.n + 
						self.recovered.n + self.dead.n
		if connections == None: self.con = []
		
	def update_city_status(self, disease):
		self.infect(disease)
		self.recover(disease)
		self.die(disease)
		self.research(disease)

		def infect(self, Disease d, prob_fn = "ratio"):
			# [ ] TODO include option to be dependent upon number dead
			if prob_fn == "ratio":
				new_infected = d.infect_prob   * self.uninfected.n * self.infected.n/(self.uninfected.n + self.infected.n)
				reinfected   = d.reinfect_prob * self.recovered.n  * self.infected.n/(self.recovered.n  + self.infected.n) 

			elif prob_fn == "erf": 
				new_infected = d.infect_prob   * self.uninfected.n * erf(self.infected.n/self.uninfected)
				reinfected   = d.reinfect_prob * self.recovered.n  * erf(self.infected.n/self.recovered)

			self.uninfected.transfer_people(new_infected, self.infected.n)
			self.recovered.transfer_people(reinfected, self.infected)

		def recover(self, Disease d):
			new_recovered = d.recov_prob * self.infected
			self.infected.transfer_people(new_recovered, self.recovered)
			
		def die(self, Disease d):
			died = d.death_prob * self.infected
			self.infected.transfer_people(died, self.dead)
		
	# [ ] TODO Ugly, needs fixing
	# Transfer from any self box to a connection's box of same type
	def travel(self, n_people, Box b1, Box b2):
		b1.transfer_people(n_people, b2)
	
	# [ ] TODO implement ability to conduct research with connected cities
	def research(self, Disease d)
		pass
	
	def remove_connection():
		pass

	def add_connection():
		pass

# Geographic and transportation linkage of cities
class Graph():
	def ___init___(self, n_cities):
		self.n = n_cities
		city_list = []
		for i in range(n_cities):
			city_list.append(City())

		make_connections()

		def make_connections(self, con_prob = 0.1):
			for city1, city2 in zip(city_list, city_list):
				# Cities cannot connect to themselves
				if city1 == city2: continue
	
				# With given probability, connect pairs of cities
				if rand.random() < con_prob:
					city1.con.append(city2)
					city2.con.append(city1)

				# Make city connection lists ordered
				city1.con = list(set(city1.con))
				city2.con = list(set(city2.con))


# Initialize disease
disease = Disease()
disease.___init___()

# Initialize graph
graph = Graph()
graph.___init___(100)
graph.make_connections()

# Initialize cities in graph
for city in graph.city_list:
	city.___init___(100, 5)

# Simulation
for t in frange(0,100,0.1)
	for city in graph.city_list:
		city.update_city_status(disease)
		# [ ] TODO implement travel probability and conditions
		# [ ] TODO implement research across cities
