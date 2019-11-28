# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 17:37:31 2019

@author: Bryce_user
"""

import pandas as pd
import numpy as np
import numbers


import os
#os.chdir('/home/bryce/Documents/TUB_thesis/Patient Choice/Python_Files')
os.chdir('C:/Users/bryce/Documents/TUB_thesis/Patient Choice/Python_Files')
import sys
sys.path.insert(0, './')

import GeneralFunctions as GF
        

def categorize_vars(data, 
                    analysis_variables, 
                    patient_or_hospital,
                    treatment_area, 
                    n_quantiles=5, 
                    age_categories=[0, 50, 60, 70, 80, 1000], 
                    str_maps={}, 
                    cat_nums=True, 
                    export_path="../Intermediate_Files/", 
                    return_map=True, 
                    from_scratch=False, 
                    dropna=True
                    ):
    """
    data: data with columns to categorize
    analysis_variables: list of column names in the data to analyze
    patient_or_hospital: string of 'patient' or 'hospital' for file naming
    treatment_area: string for identifying saved file by treatment area
    n_quantiles: desired number of quantiles to break patients into
    age_categories: values to use as borders between age categories
    str_maps: dictionary of dictionaries, variable name to dictionary of string-number assignments
    cat_nums: whether to categorize numerical variables, False only considers strings
    export_path: path to export saved file
    return_map: whether to return the string to number maps
    dropna=True: boolean option to drop rows containing missing values
    from_scratch=False: calculate from raw data (True), or load from existing file (False)
    
    Returns a copy of the data frame where variables to study are categorized, and optionally the string to number map
    """
    # see if data is already saved
    id_col = "versid" if patient_or_hospital=="patient" else "ik_site_number"
    if cat_nums:
        file_name = f"{treatment_area}_categorized_{patient_or_hospital}_data"
    else:
        file_name = f"{treatment_area}_str_to_num_{patient_or_hospital}_data"
    file_ext = "csv"
    file_path = "../Intermediate_Files/"
    if not from_scratch:
        file = GF.check_for_saved(file_path+file_name+"."+file_ext)
        if isinstance(file, pd.DataFrame):
            file.index = file[id_col]
            return file
    
    print(f"categorizing {patient_or_hospital}s")

    data_categorized = data.copy()
    vars_to_categorize = analysis_variables
    
    str_dicts = {}
    for c in vars_to_categorize:
        if c not in data.columns: continue
        
        if cat_nums:
            if c == "Age":
                data_categorized[c] = categorize_age(data_categorized[c], age_categories=age_categories) 
            
            else: data_categorized[c] = categorize_nums(data_categorized[c], n_quantiles=n_quantiles)

        if isinstance(data[c].iloc[0], str): 
            data_categorized[c], str_dict = categorize_str(data_categorized[c], str_to_num_map = str_maps[c])
            str_dicts[c] = str_dict
            
    
    if dropna:
        data_categorized.dropna(inplace=True)
        
    GF.export_data_to_file(data_categorized, filename=file_name, path=export_path, ftype=file_ext, overwrite=True)
    
    if return_map:
        return data_categorized, str_dicts
    else:
        return data_categorized
    
    

def categorize_age(series, age_categories=[0, 50, 60, 70, 80, 1000], verbose=False):
    """
    series: data frame column to categorize
    age_categories: list of numbers of the borders of the age categories. don't forget to include an upper limit
    verbose: whether to print progress or stay silent
    
    Returns a series of values sorted into defined categories
    """
        
    if "Age" in series.name or "age" in series.name:
            
        for i,d in enumerate(series):
            #print(f"categorizing {series.index[i]}")
            for j in range(len(age_categories)-1):
                
                # check if between age thresholds, and assign accordingly
                if d >= age_categories[j] and d < age_categories[j+1]:
                    series.iloc[i] = j
            
            if i%1000 == 0 and verbose:
                print(f"{i} of {len(series)} completed")
    
    return series

        
                
def categorize_nums(series, n_quantiles, verbose=False):
    """
    series: data frame column to categorize
    n_quantiles: number of quantiles
    verbose: whether to print progress or stay silent

    
    Returns a data frame of values sorted into defined categories
    """
    
    series = series.sort_index()
    
    # if there are not many unique entries, assume it's categorical
    if len(pd.unique(series)) < 2*n_quantiles: return series
    
    # find indexes with useful numbers
    idx_to_cat = []
    for i in series.index:
        if pd.notnull(series.loc[i]):
            idx_to_cat.append(i)
    
    # check that entries are numbers
    if all([isinstance(i, numbers.Number) for i in series.loc[idx_to_cat]]):
        
        # set desired quantiles
        quantiles = [i/(n_quantiles-1) for i in range(n_quantiles)]
        categories = list(np.quantile(series.loc[idx_to_cat], quantiles))
        categories[-1] += 1
        
        
        # assign category to output
        for i,d in enumerate(series.loc[idx_to_cat]):
            
            # check if it's between categories, assign accordingly
            for j,x in enumerate(categories[:-1]): # x not needed, just enables enumerate
                if d >= categories[j] and d < categories[j+1]:
                    series.loc[idx_to_cat[i]] = j
                    break
    
            if i%1000 == 0 and verbose:
                print(f"{i} of {len(series.loc[idx_to_cat])} completed")
                
        return series

def categorize_str(series, str_to_num_map={}, verbose=False):
    """
    series: series of data to categorize
    str_to_num_map: dictionary mapping variable names to assigned numbers. If none, one will be created.
    verbose: whether to print progress or stay silent

    Returns a series of values sorted into defined categories, and a dictionary of map between names and numbers.
    """
    

    # check type of values
    if type(series.iloc[0]) == str:
        uniques = pd.unique(series)

        if not str_to_num_map:
            str_to_num_map = {u:i for i,u in enumerate(uniques)}
            
        for i,d in enumerate(series):
            series.iloc[i] = str_to_num_map[d]
            if i%1000 == 0 and verbose:
                print(f"{i} of {len(series)} completed")
                
    return series, str_to_num_map
        
    
def group_patients(data_pattr_categorized, 
                   treatment_area, 
                   data_output_alt=None,
                   export_path="../Intermediate_Files/", 
                   dropna=True, 
                   from_scratch=False):
    """
    data_pattr_categorized: dataframe of the patients attributes put into categories
    treatment_area: treatment area under analysis
    data_output_alt=None: an alternate file to use as output
    export_path: path to export saved file
    dropna=True: boolean option to drop rows containing missing values
    from_scratch=False: calculate from raw data (True), or load from existing file (False)

    Takes in patient attribute data that has been categorized, constructs each possible group using 
    ruralness, severity, and age groups. Returns list of groups, or appends to provided data frame
    """
    # see if data is already saved
    file_name = f"{treatment_area}_groups_patient_data"
    file_ext = "csv"
    file_path = "../Intermediate_Files/"
    
    if not from_scratch:
        file = GF.check_for_saved(file_path + file_name + "." + file_ext)
        
        # if file was found, prepare to return it
        if isinstance(file, pd.DataFrame): 
            file.index = file["Patient_Group"]
            
            # if alternate output, return groups appended to said output
            if isinstance(data_output_alt, pd.DataFrame):
                
                data_output_alt = data_output_alt.merge(file, left_index=True, right_index=True, how="left")
                if dropna: data_output_alt.dropna(inplace=True)
                return data_output_alt.groupby(data_output_alt.index).first()
            
            return file
    
    # prepare output structure
    patient_groups = pd.DataFrame(index=data_pattr_categorized.index, columns=["Patient_Group"])
    
    # create labels from categories, assign to row
    for i in data_pattr_categorized.index:
        #print(f"assigning group to {i}")
        
        if pd.notnull(data_pattr_categorized["Ruralness_ktyp"].loc[i]):
            r = int(data_pattr_categorized["Ruralness_ktyp"].loc[i])
        else: r = np.nan
        if pd.notnull(data_pattr_categorized["Gender"].loc[i]):
            g = int(data_pattr_categorized["Gender"].loc[i])
        else: g = np.nan
        if pd.notnull(data_pattr_categorized["Severity"].loc[i]):
            s = int(data_pattr_categorized["Severity"].loc[i])
        else: s = np.nan
        if pd.notnull(data_pattr_categorized["Age"].loc[i]):
            a = int(data_pattr_categorized["Age"].loc[i])
        else: a = np.nan
        if pd.notnull(data_pattr_categorized["travel_time_cat_quantile"].loc[i]):        
            t = int(data_pattr_categorized["travel_time_cat_quantile"].loc[i])
        else: t = np.nan
        
        patient_groups.loc[i] = f"patient_group_r{r}_g{g}_s{s}_a{a}_t{t}"
    
    GF.export_data_to_file(patient_groups, filename=file_name, path=export_path, ftype=file_ext, overwrite=True)

    # option to append data to data frame by index
    if isinstance(data_output_alt, pd.DataFrame):
        data_output_alt = data_output_alt.merge(patient_groups, left_index=True, right_index=True, how="left")
        
        # remove unhelpful entries
        if dropna: data_output_alt.dropna(inplace=True)
        data_output_alt.groupby(data_output_alt.index).first()
        
        return data_output_alt

    return patient_groups
    

def group_hospitals(hospital_structural_data, 
                    treatment_area, 
                    data_output_alt=None, 
                    export_path="../Intermediate_Files/", 
                    dropna=True, 
                    from_scratch=False):
    """
    hospital_structural_data: data of the hospital structural information
    treatment_area: treatment area under analysis
    data_output_alt=None: an alternate file to use as output
    export_path: path to export saved file
    dropna=True: boolean option to drop rows containing missing values
    from_scratch=False: calculate from raw data (True), or load from existing file (False)

    Takes in hospital structural data that has been categorized, constructs each possible group using 
    quality, case_volume, and dedicated department groups. Returns list of groups, or appends to 
    provided data frame
    """
    
    # see if data is already saved
    file_name = f"{treatment_area}_groups_hospital_data"
    file_ext = "csv"
    file_path = "../Intermediate_Files/"
    if not from_scratch:
        file = GF.check_for_saved(file_path + file_name + "." + file_ext)
        
        # if file was found, prepare to return it
        if isinstance(file, pd.DataFrame): 
            file.index = file["Hospital_Group"]
            
            # if alternate output, return groups appended to said output
            if isinstance(data_output_alt, pd.DataFrame):
                data_output_alt = data_output_alt.merge(file, left_index=True, right_index=True, how="left")
        
                if dropna: data_output_alt.dropna(inplace=True)
                return data_output_alt.groupby(data_output_alt.index).first()
        
            return file
        
    # prepare output structure
    hospital_groups = pd.DataFrame(index=hospital_structural_data.index, columns=["Hospital_Group"])  
    
    # create labels from categories, assign to row
    for i in hospital_structural_data.index:
        if pd.notnull(hospital_structural_data["QI"].loc[i]):
            q = int(hospital_structural_data["QI"].loc[i])
        else: q = np.nan
        if pd.notnull(hospital_structural_data["QI"].loc[i]):
            v = int(hospital_structural_data["case_volume"].loc[i])
        else: v = np.nan
        if pd.notnull(hospital_structural_data["QI"].loc[i]):
            d = int(hospital_structural_data["dedicated_dept"].loc[i])
        else: d = np.nan
        
        hospital_groups.loc[i] = f"hospital_group_q{q}_v{v}_d{d}"
    
    GF.export_data_to_file(hospital_groups, filename=file_name, path=export_path, ftype=file_ext, overwrite=True)

    # option to append data to data frame by index
    if isinstance(data_output_alt, pd.DataFrame):
        data_output_alt = data_output_alt.merge(hospital_groups, left_index=True, right_index=True, how="left")

        # remove unhelpful entries
        if dropna: hospital_structural_data.dropna(inplace=True)
        data_output_alt.groupby(data_output_alt.index).first()

        return data_output_alt
    
    return hospital_groups



def prune_group(data, cumsum_threshold=None, simple_threshold=None):
    """
    data: data containing group IDs
    cumsum_threshold=None: threshold defining maximum data remaining after pruning with cumulative sum (number b/w 0,1)
    simple_threshold=None: threshold defining minimum percent of total data a group must represent to be kept (number b/w 0,1)
    
    Reduce the number of groups by ignoring the patients in groups that are too small
    """
    
    # if nothing to remove, return original data
    if not cumsum_threshold and not simple_threshold:
        return data
    
    # record rows to remove
    to_remove = []
    
    # get group column identifier
    try:
        group_label = "Patient_Group"
        data[group_label]
    except KeyError:
        group_label = "Hospital_Group"
        data[group_label]


    # simple thresholding
    if simple_threshold:
        
        simple_threshold *= len(data.index)
        for label in pd.unique(data[group_label]):
            idx = GF.find(data[group_label], label)

            #print(len(idx)/len(data[group_label]))
            if len(idx) < simple_threshold:
                to_remove += GF.find(data[group_label], label)

                
    # cumulative sum threshold
    if cumsum_threshold:
        
        cumsum_threshold = 1 - cumsum_threshold
        cumsum_threshold *= len(data.index)
        # set up lists to record everything in the same order
        ls_unordered_labels  = []
        ls_unordered_lengths = []
        for label in pd.unique(data[group_label]):
            
            # find all indices matching the group label
            idx = GF.find(data[group_label], label)

            
            # record indices, labels and lengths
            ls_unordered_labels  += [label]
            ls_unordered_lengths += [len(idx)]
            
        
        # set up lists to record everything in new, consistent order
        ls_ordered_labels  = []
        ls_ordered_lengths = []
        while ls_unordered_labels:
            
            # find the index of the maximum value
            idx = GF.find(ls_unordered_lengths, max(ls_unordered_lengths))

            idx = idx[0]
    
            ls_ordered_labels.append(ls_unordered_labels.pop(idx))
            ls_ordered_lengths.append(ls_unordered_lengths.pop(idx))
    
        csum = 0
        for i, length in enumerate(ls_ordered_lengths):
            csum += length
            if csum > cumsum_threshold:
                to_remove += GF.find(data[group_label], ls_ordered_labels[i])

    
    to_remove = list(data.index[to_remove])
    
    
    return data.drop(to_remove)





def subset_patients_or_hospitals(data, params = {}, group_col=None, combine="intersection"):
    """
    data: data frame with a group label column to get subsets from
    params: dictionary of variables and values to search for. key for ruralness should be '_r', value is a single number
    group_col: string of the group name to look for. If none, look for "Patient_Group", then "Hospital_Group"
    combine: to take intersection or union of matches
    
    Return subset of patients belonging to patient groups with desired characteristics. Currently only allows
    one value per variable.
    """
    
    if not params: return data
    
    # allows it to work for either hospitals or patients
    if not group_col:
        for i in ["Patient_Group", "Hospital_Group"]:
            if i in data.columns:
                group_col = i
    
    # find indices of matches independently for each variable
    idx_k = {key:[] for key in params.keys() if params[key]}
    for i in data.index:
        for key in idx_k.keys():
            for val in params[key]:
                if f"{key}{val}" in data[group_col].loc[i]:
                    idx_k[key].append(i)
    
    if not idx_k:
        return data
    
    idx_k_all = list(pd.unique([value for sublist in idx_k.values() for value in sublist]))
    
    # how to combine the found matches
    if combine=="union":
        idx = idx_k_all
        return data.loc[idx]
    
    elif combine=="intersection":
        idx = []
        for i in idx_k_all:
            in_all = True
            for k in idx_k.keys():
                if i not in idx_k[k]: 
                    in_all = False
                    continue
            if in_all: idx.append(i)

        return data.loc[idx]
    
    else:
        return
