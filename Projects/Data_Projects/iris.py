
"""
Authored by Bryce Burgess

Iris data, python
Predict flower class
"""

import pandas as pd
import matplotlib.pyplot as plt
import sklearn.datasets
import sklearn.model_selection

import torch
import tensorflow
import keras

import sklearn.naive_bayes
import sklearn.ensemble
#import pylearn2
import bokeh

import seaborn


split_strat = sklearn.model_selection.KFold(n_splits=10, shuffle=True)

iris = sklearn.datasets.load_iris()

iris.target # labels
iris.data # entries


# transform data to simplify
pca_obj = sklearn.decomposition.PCA()
iris_pca = pca_obj.fit_transform(iris.data)

# select highly important variables
s=0
for i,j in enumerate(pca_obj.explained_variance_ratio_):
    s+=j
    if s > 0.9:
        iris_pca = iris_pca[:,:i+1]


# machine learning models

# exploratory
# scatterplots, histograms, boxplots, stem and leaf plots, gaussian fit
seaborn.pairplot(iris.data)
seaborn.pairplot(iris_pca.data)



# sklearn naive_bayes
nb = sklearn.naive_bayes.GaussianNB()
sklearn.model_selection.cross_validate(nb,iris.data, iris.target, cv=split_strat)


# sklearn random forest
rf = sklearn.ensemble.RandomForestClassifier()
n_trees = {"n_estimators":range(1,101,5)}
gscv = sklearn.model_selection.GridSearchCV(estimator=rf, cv = split_strat, param_grid=n_trees)
sklearn.model_selection.cross_validate(gscv.estimator, iris.data, iris.target, cv=split_strat)



# pytorch


# tensorflow


# keras





