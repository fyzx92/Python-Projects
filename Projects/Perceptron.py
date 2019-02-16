# Authored by Bryce Burgess
# Perceptron model

import random as rand
import math

# needs to be given list of inputs to function
class Neuron():
    # initialize the neuron inputs and weights
    def __init__(self, input_list = []):
        self.init_inputs(input_list)
        self.init_weights()

    def init_inputs(self, input_list = [], bias_type = "rand"):
        if bias_type == "rand":
        	# Set seed for replicability
           	# seed(123456780)
            bias = rand.random()
        elif bias_type == "const":
            bias = 0.5
        self.inputs = [bias] + input_list

    def init_weights(self):
        self.weights = []
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
                sigmoid = lambda x: 1.0/(1.0 + math.exp(-x))
                return sigmoid(act_sum)
            elif fn == "atan":
                return math.atan2(act_sum)/math.pi + 1
            else: return "invalid activation function"

        else:
            if fn == "sigmoid":
                return sigmoid(act_sum) > 0.5
            elif fn == "atan":
                return math.atan2(act_sum)/math.pi + 1 > 0.5
            else: return "invalid activation function"

    # option to clear all inputs of neuron
    def clear_inputs(self, keep_bias = True):
        if keep_bias:
            self.inputs = self.inputs[0]
        else:
            self.inputs = []

    # train the neuron weights based on inputs and labels
    def train(self, training_set, labels, epochs = 1):
        if ~self.label_is_numeric(labels):
            return "Error: labels are not numeric"
        if len(training_set) != len(labels):
            return "Error: training data length does not match label length"

        for i in range(epochs):
            for j in range(len(training_set)):
                self.inputs.__init__(training_set[j])
                error = labels[j] - self.activation() # [ ] TODO check this, it seems wrong...
                self.update_weights(error)

    def label_is_numeric(self, labels): # does this distinguish between floats and ints?
        if type(labels[0]) != type( (int) (labels[0])):
            if type(labels[0]) != type( (float) (labels[0])):
                return False
        return True

    def update_weights(self, error, learn_rate = 0.05):
        for i in range(len(self.weights)):
            self.weights[i] += error * self.inputs[i] * learn_rate