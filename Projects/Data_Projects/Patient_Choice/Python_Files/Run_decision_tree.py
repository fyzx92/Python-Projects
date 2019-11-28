# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 13:39:43 2019

@author: bryce
Decision Trees
"""

import sklearn
import sklearn.tree
import sklearn.ensemble
import sklearn.model_selection as ms
import matplotlib.pyplot as plt

import os
#os.chdir('/home/bryce/Shared/TUB_thesis/Patient Choice/Python_Files')
os.chdir('C:/Users/bryce/Documents/TUB_thesis/Patient Choice/Python_Files')
import sys
sys.path.insert(0, './')

# contains options
import config



ta = config.ta_to_name(config.treatment_areas)

data_pchoice = config.ta_to_pchoice(ta)



###############################################################################
# decision tree [data about patient group to predict type of hospital]
###############################################################################
d = data_pchoice.dropna()


# decision tree patient attributes -> hospital group
patient_to_h_group_tree = sklearn.tree.DecisionTreeClassifier()
patient_dt_cv_scores = ms.cross_validate(patient_to_h_group_tree, d[config.patient_analysis_variables], d["Hospital_Group"], cv=10, return_train_score=True)
patient_to_h_group_tree.fit(d[config.patient_analysis_variables], d["Hospital_Group"])

sklearn.tree.export_text(patient_to_h_group_tree, feature_names=config.patient_analysis_variables)
sklearn.tree.plot_tree(patient_to_h_group_tree)
sklearn.tree.export_graphviz(patient_to_h_group_tree, feature_names=config.patient_analysis_variables, out_file="../Results/predict_hosp_type.dot")

# plot cross validation values
plt.figure()
plt.ylabel("score")
plt.xlabel("cv iteration")
plt.scatter(range(len(patient_dt_cv_scores["test_score"])), "test_score", c ="r", marker="^", data=patient_dt_cv_scores, label="test_score")
plt.scatter(range(len(patient_dt_cv_scores["train_score"])), "train_score", c="b", marker="s", data=patient_dt_cv_scores, label="train_score")
plt.legend()
plt.show()

#plt.savefig('myfig')




# TODO make sure all variables are numeric
# decision tree hospital features -> patient group
h = config.hospital_analysis_variables.copy()
h.remove("hospital_type")
hosp_to_p_group_tree = sklearn.tree.DecisionTreeClassifier()
hospital_dt_cv_scores = ms.cross_validate(hosp_to_p_group_tree, d[config.hospital_analysis_variables], d["Patient_Group"], cv=10, return_train_score=True)
hosp_to_p_group_tree.fit(d[config.hospital_analysis_variables], d["Patient_Group"])

sklearn.tree.export.export_text(hosp_to_p_group_tree, feature_names=config.hospital_analysis_variables)
sklearn.tree.plot_tree(hosp_to_p_group_tree)
sklearn.tree.export_graphviz(hosp_to_p_group_tree, feature_names=config.hospital_analysis_variables, out_file="../Results/predict_patient_type.dot")

# plot cross validation values
plt.figure()
plt.ylabel("score")
plt.xlabel("cv iteration")
plt.scatter(range(len(hospital_dt_cv_scores["test_score"])), "test_score", c ="r", marker="^", data=hospital_dt_cv_scores, label="test_score")
plt.scatter(range(len(hospital_dt_cv_scores["train_score"])), "train_score", c="b", marker="s", data=hospital_dt_cv_scores, label="train_score")
plt.legend()
plt.show()

#plt.savefig('myfig')






# Random forest:

# random forest patient attributes -> hospital group
patient_to_h_group_rforest = sklearn.ensemble.RandomForestClassifier(n_estimators = 16, max_features=1)
patient_rf_cv_scores = ms.cross_validate(patient_to_h_group_rforest, d[config.patient_analysis_variables], d["Hospital_Group"], cv=10, return_train_score=True)
patient_to_h_group_rforest.fit(d[config.patient_analysis_variables], d["Hospital_Group"])
#sklearn.tree.export.export_text(patient_to_h_group_rforest, feature_names=patient_analysis_variables)
#sklearn.tree.plot_tree(patient_to_h_group_rforest)
#sklearn.tree.export_graphviz()

# plot cross validation values
plt.figure()
plt.ylabel("score")
plt.xlabel("cv iteration")
plt.scatter(range(len(patient_rf_cv_scores["test_score"])), "test_score", c ="r", marker="^", data=patient_rf_cv_scores, label="test_score")
plt.scatter(range(len(patient_rf_cv_scores["train_score"])), "train_score", c="b", marker="s", data=patient_rf_cv_scores, label="train_score")
plt.legend()
plt.show()

#plt.savefig('myfig')




# TODO make sure all variables are numeric
# random forest hospital features -> patient group
hosp_to_p_group_rforest = sklearn.ensemble.RandomForestClassifier(n_estimators = 64, max_features=1)
hospital_rf_cv_scores = ms.cross_validate(hosp_to_p_group_rforest, d[config.patient_analysis_variables], d["Patient_Group"], cv=10, return_train_score=True)
hosp_to_p_group_rforest.fit(d[config.patient_analysis_variables], d["Patient_Group"])
#sklearn.tree.export.export_text(hosp_to_p_group_rforest, feature_names=h)
#sklearn.tree.plot_tree(hosp_to_p_group_rforest)
#sklearn.tree.export_graphviz()

plt.figure()
plt.ylabel("score")
plt.xlabel("cv iteration")
plt.scatter(range(len(hospital_rf_cv_scores["test_score"])), "test_score", c ="r", marker="^", data=hospital_rf_cv_scores, label="test_score")
plt.scatter(range(len(hospital_rf_cv_scores["train_score"])), "train_score", c="b", marker="s", data=hospital_rf_cv_scores, label="train_score")
plt.legend()
plt.show()

#plt.savefig('myfig')


# interpret output: if travel times are the same, patients with these values of these features will tend to prioritize hospitals with these characteristics
# try with different grouping mechanisms, incorporate travel times, ranked vs raw data
