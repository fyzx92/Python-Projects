# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 14:59:20 2019

@author: bryce
"""
import numpy as np
import pandas as pd

import os
#os.chdir('/home/bryce/Documents/TUB_thesis/Patient Choice/Python_Files')
os.chdir('C:/Users/bryce/Documents/TUB_thesis/Patient Choice/Python_Files')
import sys
sys.path.insert(0, './')

import GeneralFunctions as GF
import TravelTime as TT


def calculate_patient_choice_factors(treatment_area, 
                                     hospital_data, 
                                     patient_data, 
                                     hospital_analysis_vars,
                                     patient_analysis_vars,
                                     export_path="../Intermediate_Files/",
                                     from_scratch=False,
                                     dropna=False
                                     ):
    """
    treatment_area: string for identifying saved file by treatment area
    hospital_data=None: raw structural hospital data, not needed if loading from file
    patient_data=None: raw patient data, not needed if loading from file
    hospital_vars: variables to look for in hospital data
    patient_analysis_vars: variables to include from patient data
    export_path: path to export saved file
    from_scratch=False: calculate from raw data (True), or load from existing file (False)
    dropna=True: boolean option to drop rows containing missing values
    
    Returns: data frame of patient IDs with the characteristics of their chosen
    hospitals, and the patients' own attributes
    """
    
    # see if data is already saved
    file_name = f"{treatment_area}_hospital_features_by_patient"
    file_ext = "csv"
    file_path = "../Intermediate_Files/"
    if not from_scratch:
        file = GF.check_for_saved(file_path + file_name + "." + file_ext)
        if isinstance(file, pd.DataFrame): 
            file.index = file["versid"]
            return file
    
    # ensure that needed hospital variables are included
    hospital_vars = hospital_analysis_vars + ["ik_site_number", "treatment_area", "Hospital_Group"]
    hospital_vars = list(pd.unique(hospital_vars))
    
    # ensure that needed hospital variables are included
    patient_vars = patient_analysis_vars + ["versid", "Patient_Group", "plz"]
    patient_vars = list(pd.unique(patient_vars))
    
    # preallocating structures
    patient_variable_data = patient_data[patient_vars]
    patient_hospital_data = pd.DataFrame(columns=hospital_vars, index=patient_data.index)
    
    for a, h in enumerate(pd.unique(patient_data["ik_site_number"])):
        patients_chose_h = GF.find(patient_data["ik_site_number"], h)
        
        if h not in hospital_data.index: continue
        
        for j,k in enumerate(hospital_vars):
            patient_hospital_data.iloc[patients_chose_h, j] = hospital_data.loc[h, k]
            
        
    patient_hospital_data = patient_hospital_data.merge(patient_variable_data, left_index=True, right_index=True)


    if dropna: patient_hospital_data.dropna(inplace=True)
    
    GF.export_data_to_file(patient_hospital_data, filename=file_name, path=export_path, ftype=file_ext, overwrite=True)
            
    return patient_hospital_data


 
def linear_score(data_p, data_h, positively_scaling=[], negatively_scaling=[], effective_maximum_quantile=0.95):
    """
    data_p: a dataframe to linearly scale to [0,1] (approximately) on columns
    data_h: dataframe of hospital data to compare score to available options
    positively_scaling: list of column names for values that are more important when they are more positive
    negatively_scaling: list of column names for values that are more important when they are less positive
    effective_maximum_quantile: quantile to use as effective maximum when compressing values
    
    take a real valued range of input values and map them approximately to the
    range [0,1], by using the minimum and 95 percentile as boundaries, and then
    uses an exponential function to account for the availability
    """
    
    data_p_scaled = data_p.copy().dropna()
    
    not_quite_zero = 0.01

        
    for v in positively_scaling + negatively_scaling:
        print(f"\nthe hospital mean of {v} is {data_h[v].mean()}")
        print(f"the choice mean of {v} is {data_p_scaled[v].mean()}")
        
        series = data_p_scaled[v].copy()
        hmean = data_h[v].dropna().mean()
        if v == "QI":
            hmean = data_h[v].dropna().median()
        
        if all([i==0 or i==1 for i in series]):
            choice_rate = sum(series)/len(series)
            series = pd.Series([choice_rate]*len(series), index=series.index)
        else:
                
            # subtract minimum
            hmean  -= min(series)
            series -= min(series)
            
            # compress based on (near) maximum
            effective_max = series.quantile(effective_maximum_quantile)
            if effective_max:
                hmean  /= effective_max
                series /= effective_max
            else:
                hmean  /= not_quite_zero
                series /= not_quite_zero
    
            # treat anything greater than the 95th percentile as 95th percentile
            effective_max = series.quantile(effective_maximum_quantile)
            series = series.apply(lambda x: min(x, effective_max))
            
            # invert scores
            if v in negatively_scaling:
                hmean  = 1 - hmean
                series = 1 - series

        # set up function to modify scaling based on availability
        if not hmean:
            hmean = not_quite_zero
        h_log = np.log(hmean)
        if not h_log:
            h_log = -not_quite_zero
        exponent = np.log(0.5)/(h_log)
        
        # modify scaling based on availability
        series = series**exponent
        
        data_p_scaled[v] = series
        
    return data_p_scaled


def linear_score2(data_p, data_h, travel_time_selected_TA, upper_time_bound = "all", positively_scaling=[], negatively_scaling=[], effective_maximum_quantile=0.95):
    """
    data_p: a dataframe to linearly scale to [0,1] (approximately) on columns
    data_h: dataframe of hospital data to compare score to available options
    travel_time_selected_TA: travel time data frame to use for reference
    upper_time_bound: how to determine the pool of hospitals ("all", "multiplier", "proportional", "exponent")
    positively_scaling: list of column names for values that are more important when they are more positive
    negatively_scaling: list of column names for values that are more important when they are less positive
    effective_maximum_quantile: quantile to use as effective maximum when compressing values

    take a real valued range of input values and map them approximately to the
    range [0,1], by using the minimum and 95 percentile as boundaries, and then
    uses an exponential function to account for the availability
    """
    
    data_p_scaled = data_p.copy().dropna()
    
    effective_maximum_quantile = 0.95 # must be between 0 and 1
    not_quite_zero = 0.01


    for v in positively_scaling + negatively_scaling:
        print(f"\nthe hospital mean of {v} is {data_h[v].mean()}")
        print(f"the choice mean of {v} is {data_p_scaled[v].mean()}")
        
        series = data_p_scaled[v].copy()
        
        # if binary, assign average choice rate
        isbinary = False
        if all([i==0 or i==1 for i in series]):
            isbinary = True
            choice_rate = sum(series)/len(series)
            series4 = pd.Series([choice_rate]*len(series), index=series.index)
            
        else:
            
            # subtract minimum
            series2 = series - min(series)
            
            # compress based on (near) maximum
            effective_max1 = series2.quantile(effective_maximum_quantile)
            if effective_max1:
                series3 = series2/effective_max1
            else:
                series3 = series2/not_quite_zero
                
            # treat anything greater than the 95th percentile as 95th percentile
            effective_max2 = series3.quantile(effective_maximum_quantile)
            series4 = series3.apply(lambda x: min(x, effective_max2))
    
            # invert scores if needed        
            if v in negatively_scaling:
                series4 = 1 - series4
            
        # scale hmean same way
        for p in series.index:
            # get mean from hospital pool
            if v == "QI":
                hmean = get_hospital_mean(data_p["plz"].loc[p], data_p["ik_site_number"].loc[p], v, data_h, travel_time_selected_TA, upper_time_bound = upper_time_bound, mean=False)
            else:
                hmean = get_hospital_mean(data_p["plz"].loc[p], data_p["ik_site_number"].loc[p], v, data_h, travel_time_selected_TA, upper_time_bound = upper_time_bound)
            
            # if variable is not binary, compress 
            if not isbinary:

                # subtract minimum
                hmean -= min(series)
                
                # compress based on (near) maximum
                if effective_max1:
                    hmean /= effective_max1
                else:
                    hmean /= not_quite_zero
                    
                # invert scores
                if v in negatively_scaling:
                    hmean  = 1 - hmean
            
            # set up function to modify scaling based on availability
            if not hmean:
                hmean = not_quite_zero
            h_log = np.log(hmean)
            if not h_log:
                h_log = -not_quite_zero
            exponent = np.log(0.5)/(h_log)
            
            # modify scaling based on availability
            series4.loc[p] = series4.loc[p]**exponent
        
        data_p_scaled[v] = series4
        
    return data_p_scaled



def exponential_score(data_p, data_h, positively_scaling=[], negatively_scaling=[]):
    """
    data_p: a dataframe to exponentially scale to [0,1) (approximately) on columns
    data_h: dataframe of hospital data to compare score to available options
    positively_scaling: list of column names for values that are more important when they are more positive
    negatively_scaling: list of column names for values that are more important when they are less positive
    
    take a real valued range of input values and map them approximately to the 
    range [0,1], by using a decaying exponential function
    """
    
    data_p_scaled = data_p.copy().dropna()
    not_quite_zero = 0.01

    for v in positively_scaling + negatively_scaling:
        print(f"\nthe hospital mean of {v} is {data_h[v].mean()}")
        print(f"the choice mean of {v} is {data_p_scaled[v].mean()}")
        
        series = data_p_scaled[v].copy()

        hmean = data_h[v].dropna().mean()
        if v == "QI":
            hmean = data_h[v].dropna().median()
        
        if not hmean: hmean = not_quite_zero
        series = np.exp2(list(-series/hmean))
        
        if v in positively_scaling:
            # correct scaling direction
            series = 1 - series
            
        data_p_scaled[v] = series
        
    return data_p_scaled


def exponential_score2(data_p, data_h, travel_time_selected_TA, upper_time_bound = "all", positively_scaling=[], negatively_scaling=[]):
    """
    data_p: a dataframe to exponentially scale to [0,1) (approximately) on columns
    data_h: dataframe of hospital data to compare score to available options
    travel_time_selected_TA: travel time data frame to use for reference
    upper_time_bound: how to determine the pool of hospitals ("all", "multiplier", "proportional", "exponent")
    positively_scaling: list of column names for values that are more important when they are more positive
    negatively_scaling: list of column names for values that are more important when they are less positive
    
    take a real valued range of input values and map them approximately to the 
    range [0,1], by using a decaying exponential function
    """
    
    data_p_scaled = data_p.copy().dropna()
    not_quite_zero = 0.01

    for v in positively_scaling + negatively_scaling:
        print(f"\nthe hospital mean of {v} is {data_h[v].mean()}")
        print(f"the choice mean of {v} is {data_p_scaled[v].mean()}")
        
        series = data_p_scaled[v].copy()
        
        for p in series.index:
            hmean = get_hospital_mean(data_p["plz"].loc[p], data_p["ik_site_number"].loc[p], v, data_h, travel_time_selected_TA, upper_time_bound = upper_time_bound)
            if v == "QI":
                hmean = get_hospital_mean(data_p["plz"].loc[p], data_p["ik_site_number"].loc[p], v, data_h, travel_time_selected_TA, upper_time_bound = upper_time_bound, mean=False)
            
            if not hmean: hmean = not_quite_zero
            series.loc[p] = np.exp2(-series.loc[p]/hmean)
            
            if v in positively_scaling:
                # correct scaling direction
                series.loc[p] = 1 - series.loc[p]
            
        data_p_scaled[v] = series
        
    return data_p_scaled

def get_hospital_mean(plz, hospital, variable, data_h, travel_time_selected_TA, upper_time_bound = "all", mean=True):
    """
    plz: single plz value associated with a patient
    hospital: single hospital name chosen by the same patient
    variable: the variable for which to get the mean from the hospital pool
    data_h: data frame of hospitals and variables, must include variable
    travel_time_selected_TA: data frame of relevant travel times, for restricting pool of hospitals
    upper_time_bound: how to determine the pool of hospitals ("all", "multiplier", "proportional")
    mean: whether to return the mean or the median
    
    Selects a pool of hospitals based on the distance to the chosen hospital,
    and calculates the mean of variable within this pool
    """
    
    # interpret method to determine alternatives
    if upper_time_bound == "all": 
        if mean:
            return data_h[variable].mean()
        else: 
            return data_h[variable].median()
    
    elif upper_time_bound == "multiplier": 
        fn = lambda x: x*1.2
        
    elif upper_time_bound == "exponent": 
        fn = lambda x: x**1.2
        
    elif upper_time_bound == "proportional": 
        fn = lambda x: x*np.log(x)
    else:
        fn = upper_time_bound
    
    # get time to choice
    chosen_time = TT.find_travel_time_plz_from_table(plz, hospital, tt_file=travel_time_selected_TA)

    # get hospital pool
    max_alt_time = fn(chosen_time)
    
    # find all hospitals closer than max_alt_time
    hospital_pool = [h for h in travel_time_selected_TA.columns if travel_time_selected_TA[h].loc[plz] <= max_alt_time]
    h_var = data_h[variable].loc[hospital_pool]

    # get mean of relevant variable (all variables?)
    if mean:
        return h_var.mean()
    else: return h_var.median()
    
    

def hospital_type_scoring(data_pchoice, data_hstruct, h_type_map, return_group_counts=False):
    """
    data_pchoice: data frame of patients, containing the column hospital_type, and Hospital_Group if return_group_counts is True
    data_hstruct: data frame of hospitals, containing the column hospital_type, for availability reference
    h_type_map: map to use for recording scores of hospital types
    return_group_counts: whether to return the raw proportions in addition to adjusted score
        
    Returns availability adjusted scores of preference for each hospital type, normalized to sum to 1.
    """
    
    reverse_map = {value:key for key, value in zip(h_type_map.keys(), h_type_map.values())}
    
    hospital_type_count = {reverse_map[i]: 0 for i in pd.unique(data_pchoice["hospital_type"].dropna())}
    for i in data_pchoice["hospital_type"].dropna():
        hospital_type_count[reverse_map[i]] += 1

    # get counts of hospital types available
    hospital_availability = {i: 0 for i in pd.unique(data_hstruct["hospital_type"].dropna())}
    for i in data_hstruct["hospital_type"].dropna():
        hospital_availability[i] += 1

    # correct for availability
    hospital_type_score = hospital_type_count.copy()
    for i in hospital_type_score:
        hospital_type_score[i] /= hospital_availability[i]

    # normalize so scores sum to 1
    score_sum = sum(hospital_type_score.values())
    for i in hospital_type_score:
        hospital_type_score[i] /= score_sum
    
    if return_group_counts:
        # get proportions of hospital groups
        hospital_group_count = {i: 0 for i in pd.unique(data_pchoice["Hospital_Group"])}
        for i in data_pchoice["Hospital_Group"]:
            hospital_group_count[i] += 1

        for i in hospital_group_count:
            hospital_group_count[i] /= len(data_pchoice.index)
            
        return hospital_type_score, hospital_group_count
    
    return hospital_type_score
        
        