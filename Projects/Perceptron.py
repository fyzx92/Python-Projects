#
# Authored by Bryce Burgess
#
# Perceptron model
#

import random as rand
import math

# needs to be given list of inputs to function
class Neuron():
    # initialize the neuron inputs and weights
	def ___init___(self, input_list = []):
        init_inputs()
        init_weights()

        def init_inputs(self, bias_type = "rand"):
            if bias_type == "rand":
            	# Set seed for replicability
            	# seed(123456780)
                bias = rand.random()
            elif bias_type == "const":
                bias = 0.5

            self.inputs = [bias] + input_list

    	def init_weights(self):
    		for i in self.inputs:
        		# Set seed for replicability
        		# seed(987654321)
    			self.weights.append(rand.random())


    # define activation behavior of neuron
	def activation(self, fn = "sigmoid", prob_out = False):
		act_sum = 0

		for i in len(self.inputs):
			act_sum += self.inputs[i] * self.weights[i]

        if prob_out:
		    if fn == "sigmoid":
		        sigmoid = lambda x: 1.0/(1.0 + exp(-x))
		        return sigmoid(act_sum)
            elif fn == "atan":
		        return atan(act_sum)/pi + 1
            else return "invalid activation function"

        elif ~prob_out:
		    if fn == "sigmoid":
		        return sigmoid(act_sum) > 0.5
            elif fn == "atan":
		        return atan(act_sum)/pi + 1 > 0.5
            else return "invalid activation function"

    # option to clear all inputs of neuron
	def clear_inputs(self, keep_bias = True):
		if keep_bias:
            self.inputs = self.inputs[0]
        elif ~keep_bias:
            self.inputs = []

    # train the neuron weights based on inputs and labels
	def train(self, training_set, labels, epochs = 1):
		if len(training_set) ~= len(labels):
			return "Error, training data length does not match label length"

        def check_label_format(self, labels): # does this distinguish between floats and ints?
        	if type(labels[0]) ~= type( (int) (labels[0])):
        		unique = list(set(labels))
        		for i in unique:
        			tmp = labels.index(unique[i])


        def update_weights(self, error):
        	learn_rate = 0.05
        	for i in range(len(self.weights)):
        		self.weights[i] += error * self.inputs[i] * learn_rate

		# self.inputs = element # [ ] TODO define element
		# init_weights()

        for i in range(epochs):
		    for j in range(len(training_set)):
			    self.inputs.___init___(training_set[j])
                error = label[j] - self.activation() # seems wrong...
			    update_weights(error)
