# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 13:37:31 2019

@author: bryce
Subsetting and Scoring
"""

import pandas as pd
import seaborn as sns

import os
#os.chdir('/home/bryce/Shared/TUB_thesis/Patient Choice/Python_Files')
os.chdir('C:/Users/bryce/Documents/TUB_thesis/Patient Choice/Python_Files')
import sys
sys.path.insert(0, './')


# contains main run options
import config

import GeneralFunctions as GF
import MakeCategories as MC
import AnalysisFormat as AF
import TravelTime as TT



# get reference data for analysis
ta = config.ta_to_name(config.treatment_areas)
data_hstruct = config.ta_to_hstruct(ta)
data_pattr = config.ta_to_pattr(ta)
data_pchoice = config.ta_to_pchoice(ta)
travel_time_selected_TA = config.ta_to_TT(ta)

#%%
# subset established data

# look for specific groups
if config.target_p_groups:
    data_pchoice = data_pchoice.iloc[GF.find(data_pchoice["Patient_Group"], config.target_p_groups)]
if config.target_h_groups:
    data_pchoice = data_pchoice.iloc[GF.find(data_pchoice["Hospital_Group"], config.target_h_groups)]



# look for groups with certain attributes
data_pchoice = MC.subset_patients_or_hospitals(data_pchoice, 
                                               params = config.hospital_subset,
                                               group_col="Hospital_Group", 
                                               combine=config.combine_subset_vars)

data_pchoice = MC.subset_patients_or_hospitals(data_pchoice, 
                                               params = config.patient_subset,
                                               group_col="Patient_Group",
                                               combine=config.combine_subset_vars)



# look for large groups
if config.prune_groups:
    data_pchoice = MC.prune_group(data_pchoice["Patient_Group"], 
                                  cumsum_threshold=config.prune_cum_h_threshold, 
                                  simple_threshold=config.prune_simple_h_threshold)
    
    data_pchoice = MC.prune_group(data_pchoice["Hospital_Group"], 
                                  cumsum_threshold=config.prune_cum_p_threshold, 
                                  simple_threshold=config.prune_simple_p_threshold)





#%%
positively_scaling = ["case_volume", "university_hospital", "number_beds_total", "dedicated_dept"]
negatively_scaling = ["QI"] # travel time scored separately

# linear scale
if config.scoring_type == "linear":
    if config.reduce_hospital_pool:
        patient_priority_scores = AF.linear_score2(data_pchoice, 
                                                   data_hstruct, 
                                                   travel_time_selected_TA, 
                                                   config.hospital_pool_selection, 
                                                   positively_scaling, 
                                                   negatively_scaling,
                                                   effective_maximum_quantile=config.effective_maximum_quantile)
    else:
        patient_priority_scores = AF.linear_score(data_pchoice, 
                                                  data_hstruct, 
                                                  positively_scaling, 
                                                  negatively_scaling,
                                                  effective_maximum_quantile=config.effective_maximum_quantile)

# exponential scale
elif config.scoring_type == "exponential":
    if config.reduce_hospital_pool:
        patient_priority_scores = AF.exponential_score2(data_pchoice, 
                                                        data_hstruct, 
                                                        travel_time_selected_TA, 
                                                        config.hospital_pool_selection, 
                                                        positively_scaling, 
                                                        negatively_scaling)
    else:
        patient_priority_scores = AF.exponential_score(data_pchoice, 
                                                       data_hstruct, 
                                                       positively_scaling, 
                                                       negatively_scaling)




#%%
# travel time scoring


if config.scoring_type == "linear":
    TT_scores = TT.travel_time_linear_score(data_pattr, travel_time_selected_TA, effective_maximum_quantile=config.effective_maximum_quantile)

elif config.scoring_type == "exponential":
    TT_scores = TT.travel_time_exponential_score(data_pattr, travel_time_selected_TA)


#%%
# calculate actual scores
hospital_type_score = AF.hospital_type_scoring(data_pchoice, data_hstruct, config.str_maps["hospital_type"], return_group_counts=False)



#%%
# add travel times to scores
patient_priority_scores = patient_priority_scores.merge(TT_scores, left_index=True, right_index=True, how="left")
patient_priority_scores.dropna(inplace=True)

# calculate descriptive data for each variable
mean_score_dict = dict(patient_priority_scores.mean()) # not found
mean_score_dict.update(hospital_type_score)

median_score_dict = dict(patient_priority_scores.median())
median_score_dict.update(hospital_type_score)

var_score_dict = dict(patient_priority_scores.var())
var_score_dict.update(hospital_type_score)

summarized_scores = pd.DataFrame(columns = mean_score_dict.keys(), index = ["mean", "median", "variance"])
summarized_scores.loc["mean"] = mean_score_dict
summarized_scores.loc["median"] = median_score_dict
summarized_scores.loc["variance"] = var_score_dict

# histograms
if config.make_plots:
    sns.distplot(patient_priority_scores[config.hospital_analysis_variables])

# optionally save results
if config.save_results:
    GF.export_data_to_file(summarized_scores, path="../Results", 
                           filename=f"preference_scores_{ta}_{config.scoring_type}", 
                           ftype="csv") # or json, or text
    #GF.export_data_to_file(summarized_scores, path="../Results", 
       #                     filename=f"preference_scores_{ta}_{scoring_type}", ftype="json")

