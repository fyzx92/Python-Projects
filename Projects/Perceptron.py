# Authored by Bryce Burgess
# Perceptron model

import random as rand
import math

# needs to be given list of inputs to function
class Neuron():
    # initialize the neuron inputs and weights
    def __init__(self, input_list = []):
        self.__init_inputs(input_list)
        self.__init_weights()

    def __init_inputs(self, 
                    input_list = [], 
                    bias_type = "rand"
                    ):
        
        if not input_list:
            # seed(12345)
            input_list = [rand.random() for i in range(9)]
        
        if bias_type == "rand":
            # Set seed for replicability
            # seed(123456780)
            bias = rand.uniform(-1,1)

        elif bias_type == "const":
            bias = 0.5

        self.inputs = [bias] + input_list

    def __init_weights(self):
        self.weights = []
        for i in self.inputs:
            # Set seed for replicability
            # seed(987654321)
            self.weights.append(rand.uniform(-1,1))


    # define activation behavior of neuron
    def activation(self, 
                   fn = "sigmoid", 
                   prob_out = False
                   ):
        
        
        # define a sigmoid if needed
        if fn == "sigmoid":
            sigmoid = lambda x: 1.0/(1.0 + math.exp(-x))
            
        act_sum = 0
        # calculate activation
        for i in range(len(self.inputs)):
            act_sum += self.inputs[i] * self.weights[i]
        
        # return probability or binary
        if prob_out:
            if fn == "sigmoid":
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
        self.inputs = self.inputs[0] if keep_bias else []

    # train the neuron weights based on inputs and labels
    def train(self, training_set, expected_activation, epochs = 1):
        if not self.expected_activation_is_numeric(expected_activation):
            return "Error: labels are not numeric"
        if len(training_set) != len(expected_activation):
            return "Error: training data length does not match label length"

        for i in range(epochs):
            for j in range(len(training_set)):
                self.inputs = training_set[j]
                error = expected_activation[j] - self.activation() 
                self.update_weights(error)

    # test if labels are numeric
    def expected_activation_is_numeric(self, expected_activation):
        return all(expected_activation == 0 or expected_activation == 1)
    
    
    def update_weights(self, error, learn_rate = 0.05):
        for i in range(len(self.weights)):
            self.weights[i] += error * self.inputs[i] * learn_rate




class Layer():
    def __init__(self, n):
        self.n_neurons = n
        self.init_neurons()
        
    def __init_neurons(self):
        self.neurons = []
        for i in range(self.n_neurons):
            self.neurons.append(Neuron())
    
    def get_activations(self):
        acts = []
        for n in self.neurons():
            acts.append(n.activation)
        return acts



class Neural_Network():
    def __init__(self, *layers):
        self.id = "Dodger"
        for i in layers:
            self.__init_layers(i)
    
    def __init_layers(self, n):
        self.layers = []
        for i in range(n):
            self.layers.append(Layer(n))
    
    
    
    
    def get_input_layer(self):
        return self.layers[0]
    
    def get_output_layer(self):
        return self.layers[-1]
    
    def get_output(self):
        max_activation = 0
        for i, a in enumerate(self.get_output_layer):
            if a > max_activation:
                max_activation = a
                output_index = i
        return output_index
    
    
    
    
    def train_supervised(self, labels):
        errors = []
        for l in reversed(self.layers):
            for i,n in enumerate(l):
                errors.append(n.activation-labels[i])
                n.update_weights(errors[-1])
                # update weights of activating neurons proportional to activation strength
        
    def backpropagation(self):
        pass
    
    def check_labels(self, labels):
        labels_valid = []
        for i in labels:
            labels_valid.append(all(i == 0 or i == 1))
        return all(labels_valid)
    
    
    
    
    def train_reinforcement(self, game):
        # play a game
        self.play(game)
        
        # get value of that game
        if game.winner == self.id:
            self.is_winner = True
        elif game.winner != self.id:
            self.is_winner = False
        
        self.reinforcement_update_weights(game)
    
    def play(self, game):
        while game.is_going:
            game.get_possible_moves()
            # make moves
            pass
        
        
    def reinforcement_update_weights(self, game, learn_rate = 0.1):
        
        # positive feedback for successes
        # negative feedback for failures, mitigated by duration
        for l in self.layers:
            for n in l:
                for i,w in enumerate(n.weights):
                    
                    # assign reward or penalty to series of moves
                    if self.is_winner:
                        n.weights[i] += learn_rate*w
                    
                    # TODO reduce penalty for moves that happened longer ago
                    if not self.is_winner:
                        n.weights[i] -= learn_rate*w/game.length
    
    
    
    
    
class Game():
    def __init__(self):
        self.winner = None
        self.is_going = True
        self.players = self.__init_players()
        
        self.length = 0
        self.moves = self.get_possible_moves()
        self.get_game_state()
        
        self.update_game_state()
        
    def __init_players(self):
        pass
    
    def get_possible_moves(self):
        pass
    
    def get_current_state(self):
        pass
    
    def update_game_state(self):
        self.length += 1
        pass