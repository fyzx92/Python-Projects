# -*- coding: utf-8 -*-
"""
NN From scratch
"""

import numpy as np


# initialize
def __init__(input_size, layer_sizes):
    """
    
    Create arrays of weights and biases for each layer

    Parameters
    ----------
    input_size : TYPE
        DESCRIPTION.
    layer_sizes : TYPE
        DESCRIPTION.

    Returns
    -------
    weight_list : TYPE
        DESCRIPTION.
    biases : TYPE
        DESCRIPTION.

    """
    weight_list = []
    biases = []
    for size in layer_sizes:
        print(size)
        weight_list.append(np.random.rand(input_size, size)) # modify creation for small numbers
        biases.append(np.random.rand(1, size))
        input_size = size
    return weight_list, biases



# activation function
def relu(x):
    """
    Replace negative values with 0

    Parameters
    ----------
    x : iterable of numbers
        weighted sum of neuron inputs

    Returns
    -------
    numpy array
        activation function

    """
    return np.array([max(0,xi) for xi in x])


# feeding signal forward manually
def forward(inp, weight_list, biases):
    """
    get an output for a given model input
    Parameters
    ----------
    inp : numpy array model input
    weight_list : list of numpy arrays containing model weights
    biases : list of numpy arrays containing model biases

    Returns
    -------
    output_list : list of numpy arrays
        output of each layer of the model

    """

    # feeding more flexibly
    output_list = []
    for i, weights in enumerate(weight_list):
        wsum = np.sum(weights.T * inp + biases[i].T, axis=1)
        output = relu(wsum)
        
        output_list.append(output)
        inp = output
    return output_list
    

def backprop(output_list, output_labels, weight_list):
    """
    Parameters
    ----------
    output_list : list of numpy arrays
        per layer output of model
    output_labels : numpy array
        target output values (last layer only)
    weight_list : list of numpy arrays
        model weights per layer

    Returns
    -------
    weight_list : list of numpy arrays
        updated weight arrays

    """
    error = np.subtract(output_labels, output_list[-1])
    
    learning_rate = 0.05
    new_weight_list = []
    for i, weights in enumerate(reversed(weight_list)):
        
        j = -(i+1)
        
        # compute derivatives
        loss_to_output_deriv_outer = np.multiply(-2, error) # j is output
        loss_to_output_deriv_inner = np.sum(weights * output_list[j], axis = 0) # j is input
        output_to_sum_deriv = np.greater(output_list[j], 0)
        
        # combined values
        if j == -1:
            delta = np.multiply(output_to_sum_deriv, loss_to_output_deriv_outer)
        else:
            delta = np.multiply(output_to_sum_deriv, loss_to_output_deriv_inner)
    
        echo = np.multiply(learning_rate, output_list[j])
    
        # change weight values
        new_weights = weights - np.multiply(delta, echo)
        new_weight_list.append(new_weights)
        
    weight_list = new_weight_list
    return weight_list

def train(inp, output_labels):
    """
    Parameters
    ----------
    inp : numpy array
        model input
    output_labels : numpy array
        target output values (last layer only)

    Returns
    -------
    None.
    """
    # predictions
    output_list = forward(inp, weight_list, biases)
    
    # backprop
    weight_list = backprop(output_list, output_labels, weight_list)


#architecture and initialization
input_size, layer_sizes = 15, np.array([5]) # input, hidden, output
weight_list, biases = __init__(input_size, layer_sizes)



# inputs and outputs
inp = np.array([5,4,3,2,1,0,9,8,7,6,3,4,5,6,7])
output_labels = np.array([0,0,1,1,0])
#output_labels = np.array([1,2,3,4,5])
    
train(inp, output_labels)