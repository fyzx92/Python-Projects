# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 10:48:18 2020

@author: bryce
"""
import numpy as np

inp = np.random.rand(5,2)

def sigmoid(inp):
    return np.array([(1+np.exp(-x))**-1 for x in inp])
    
sigmoid(inp)