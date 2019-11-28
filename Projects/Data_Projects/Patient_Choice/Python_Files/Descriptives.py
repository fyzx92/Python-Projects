# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 14:44:01 2019

@author: bryce
"""


import matplotlib.pyplot as plt


def histogram(data, vars_to_plot=None, nbins = 10):
    """
    data: data with variables for histogramming
    vars_to_plot: variables of interest
    
    shows histogram of all or selected variables in data
    """
    
    #pd.notnull
    if vars_to_plot is None or vars_to_plot is False: vars_to_plot = data.columns
    for v in vars_to_plot:
        print(f"\nmaking histogram for {v}")
        plt.hist(data[v], bins = nbins)
        plt.xlabel(v)
        plt.ylabel("frequency")
        plt.show()