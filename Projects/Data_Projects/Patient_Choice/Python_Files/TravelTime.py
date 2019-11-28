# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 15:13:43 2019

@author: Bryce_user
create and import travel time tables
"""

import pandas as pd
import numpy as np
import operator

import os
#os.chdir('/home/bryce/Shared/TUB_thesis/Patient Choice/Python_Files')
os.chdir('C:/Users/bryce/Documents/TUB_thesis/Patient Choice/Python_Files')
import sys
sys.path.insert(0, './')

import GeneralFunctions as GF



def subset_travel_time_table(treatment_area, patient_plzs=None, hospitals=None, export_path="../Intermediate_Files/", from_scratch=False, dropna=True):
    """
    treatment_area: string describing treatment area for output file name
    patient_plzs=None: list-like string of plzs to look for (as np.int64) (will be checked in near future)
    hospitals=None: list-like structure of hospital IDs to look for
    from_scratch=False: calculate from raw data (True), or load from existing file (False)
    dropna=True: boolean option to drop rows containing missing values

    Return a data frame of a subset of the full travel time calculations, based
    on which plzs and hospitals are relevant to the analysis
    """    
        
    # check if data is already saved
    file_name = f"{treatment_area}_tt_plz_table"
    file_ext = "csv"
    file_path = "../Intermediate_Files/"
    if not from_scratch:
        file = GF.check_for_saved(file_path + file_name + "." + file_ext)
        if isinstance(file, pd.DataFrame): return file
    
    travel_time_all_TA = GF.check_for_saved("../Intermediate_Files/tt_plz_full_lookup_table.csv")

    print("reducing travel time table")
    travel_time_selected_TA = travel_time_all_TA.loc[patient_plzs, hospitals]
    

            
    if dropna:
        travel_time_selected_TA.dropna(inplace=True)
        
    GF.export_data_to_file(travel_time_selected_TA, filename=file_name, path=export_path, ftype = file_ext, overwrite=True)

    return travel_time_selected_TA
            
            
def travel_time_categorize_rank_table(travel_time_selected_TA, treatment_area, export_path="../Intermediate_Files/", from_scratch=True, rank_cap = None, verbose=False):
    """
    travel_time_selected_TA: reduced travel time set to find alternatives to create scale
    rank_cap=None: integer rank at which to stop increasing
    verbose: whether to print progress or stay silent

    returns data frame of value ranks across a row instead of raw values
    """
    file_name = f"{treatment_area}_ranked_tt_plz_table"
    file_ext = "csv"
    file_path = "../Intermediate_Files/"
    if not from_scratch:
        file = GF.check_for_saved(file_path + file_name + "." + file_ext)
        if isinstance(file, pd.DataFrame): return file
    
    # prepare output structure
    tt_categorized = travel_time_selected_TA.copy()

    # assign rank within the row, up to rank cap    
    for i,p in enumerate(travel_time_selected_TA.index):
        if verbose: print(f"ranking plz {p}, {i} of {len(travel_time_selected_TA.index)}")
        
        if not rank_cap:
            tt_categorized.loc[p] = [t[0] for t in sorted(enumerate(list(travel_time_selected_TA.loc[p])), key=operator.itemgetter(1))]
        else:
            tt_categorized.loc[p] = [min(t[0], rank_cap) for t in sorted(enumerate(list(travel_time_selected_TA.loc[p])), key=operator.itemgetter(1))]
    
    GF.export_data_to_file(tt_categorized, filename=file_name, path=export_path, ftype = file_ext, overwrite=True)

    return tt_categorized

def make_travel_time_plz_table(fill="load"):
    """
    fill="load": "load" and return saved file, "nans" fill missing values in file, "from_scratch" rebuild entirely
    
    Builds, saves, and returns table of plz and the quantiles of available 
    travel times
    """
    
    # import travel time data file
    tt_file = "../03 Patient & Hospital features/RAW/plz_to_hospital_travel_times.csv"
    
    # deciding to check if data is already saved
    if fill == "load":
        from_scratch = False
        return_saved_file = True
        
    elif fill == "from_scratch":
        from_scratch = True
        return_saved_file = False
    
    elif fill == "nans":    
        from_scratch = False
        return_saved_file = False
    

    
    # check if file exists, return if desired
    file_name = f"tt_plz_full_lookup_table"
    file_ext = "csv"
    file_path = "../Intermediate_files/"
    if not from_scratch:
        print(f"trying to load {file_name}")
        tt_plz = GF.check_for_saved(file_path + file_name + "." + file_ext)
        if isinstance(tt_plz, pd.DataFrame) and return_saved_file: return tt_plz
    else: tt_plz = False

    # load needed travel time data
    if isinstance(tt_file, str):
        tt_file = GF.file_to_df(tt_file, header_number=0, separator=",")
    elif not isinstance(tt_file, pd.DataFrame):
        return "Error: data needs to either be a data frame or a file path"

    
    # prepare structure to output data: unique patients are rows, hospitals are columns
    unique_p = pd.unique(tt_file["plz"])
    unique_h = pd.unique(tt_file["hospital"])
    if tt_plz is False:
        tt_plz = pd.DataFrame(index=unique_p, columns=unique_h)
    tt_plz.index = unique_p
    tt_plz.columns = unique_h



    # find unfilled plzs in existing file
    plzs_to_fill = list(unique_p)
    if fill == "nans" and tt_plz is not False:
        print("finding place to start")
        for p in unique_p:
            if not all([pd.isnull(j) for j in tt_plz.loc[p]]):
                plzs_to_fill.remove(p)

    
    for i, p in enumerate(plzs_to_fill):
        print(f"finding times for plz {p}, {i}/{len(plzs_to_fill)} empty lines completed, " +
              "{len(unique_p) - len(plzs_to_fill) + i}/{len(unique_p)} of total")
        idx = GF.find(tt_file["plz"], p)
        
        hospitals = tt_file["hospital"].iloc[idx]
        times = tt_file["travel_time"].iloc[idx]
    
    
        for j, h in enumerate(hospitals):
            tt_plz[h].loc[p] = times.iloc[j]

        tt_file.drop(tt_file.index[idx], inplace=True)

        if i % 50 == 0:
            print("intermediate save")
            GF.export_data_to_file(tt_plz, filename=file_name, path=file_path, ftype=file_ext, overwrite=True)

    GF.export_data_to_file(tt_plz, filename=file_name, path=file_path, ftype=file_ext, overwrite=True)
    
    return tt_plz



def travel_time_linear_score(data_p, travel_time_selected_TA, dropna=True, verbose=False, effective_maximum_quantile = 0.95):
    """
    data_p: patient attribute data as data frame for getting chosen travel time and plz
    travel_time_selected_TA: reduced travel time set to find alternatives to create scale
    dropna=True: boolean option to drop rows containing missing values
    verbose: whether to print progress or stay silent
    effective_maximum_quantile: quantile to use as effective maximum when compressing values


    returns a data frame of the chosen travel times, linearly rescaled relative
    to a patient's alternatives
    """
    
    # set ouptut structure
    tt_scores = pd.DataFrame(index = data_p.index, columns = ["travel_time"])

    n_completed = 0
    
    print("\ncomputing linear scores on travel time")
    
    for plz in pd.unique(data_p["plz"]):
        if verbose: print(f"getting tt scale for plz {plz}")
        
        # find index of all patients in plz
        idx = GF.find(data_p["plz"], plz)

        
        # find all alternative travel times for plz (method to limit pool as with linear scoring?)
        try:
            tt_alts = travel_time_selected_TA.loc[plz]
        except KeyError:
            tt_scores.iloc[idx] = np.nan
            continue
                
        
        tt_alts.dropna(inplace=True)

        # if alternatives not found, skip and continue
        if len(tt_alts.index) == 0:
            print(f"{plz} scale not found")
            n_completed += len(idx)
            continue
        
        # rescale all patients in a single plz
        series = tt_scores.iloc[idx].copy()
        for i, h in enumerate(data_p["ik_site_number"].iloc[idx]):
            series.iloc[i] = find_travel_time_plz_from_table(plz, h, tt_file=travel_time_selected_TA)
        series -= min(tt_alts)
        series /= np.quantile(tt_alts - min(tt_alts), effective_maximum_quantile)
        series = 1-series
        tt_scores.iloc[idx] = series
        
        n_completed += len(series)

    if dropna:
        tt_scores.dropna(inplace=True)
        
    return tt_scores


def travel_time_exponential_score(data_p, travel_time_selected_TA, dropna=True, verbose=False):
    """
    data_p: patient attribute data as data frame for getting chosen travel time and plz
    travel_time_selected_TA: reduced travel time set to find alternatives to create scale
    dropna=True: boolean option to drop rows containing missing values
    verbose: whether to print progress or stay silent
    
    returns a data frame of the chosen travel times, exponentially rescaled 
    relative to a patient's alternatives
    """
    
    # set ouptut structure
    tt_scores = pd.DataFrame(index = data_p["versid"], columns = ["travel_time"])

    n_completed = 0
    
    scale_param_q = 0.5
    
    print("computing exponential score on travel time")
    
    for plz in pd.unique(data_p["plz"]):
        if verbose: print(f"getting tt scale for plz {plz}")
        
        # find index of all patients in plz
        idx = GF.find(data_p["plz"], plz)

        
        # find all alternative travel times for plz
        try:
            tt_alts = travel_time_selected_TA.loc[plz]
        except KeyError:
            tt_scores.iloc[idx] = np.nan
            continue
        tt_alts.dropna(inplace=True)


        # if alternatives not found, skip and continue
        if len(tt_alts.index) == 0:
            print(f"{plz} scale not found")
            n_completed += len(idx)
            continue
        
        # rescale all patients in a single plz
        for i, h in enumerate(data_p["ik_site_number"].iloc[idx]):
            
            if verbose: print(f"scaling {data_p['versid'].iloc[idx[i]]}, {n_completed} of {len(tt_scores)} is {n_completed*100//len(tt_scores)}%")
            
            # get travel time for chosen hospital
            if pd.notnull(h) and pd.notnull(plz):
                tt_chosen = find_travel_time_plz_from_table(plz, h, tt_file = travel_time_selected_TA)
            
            # check if time was found
            if pd.isnull(tt_chosen): 
                print(f"{plz} to {h} not found")
                n_completed += 1
                continue
            
            # rescale
            tt_chosen -= min(tt_alts)
            tt_chosen = np.exp2(-tt_chosen/np.quantile(tt_alts, scale_param_q))
            
            # assign
            tt_scores.iloc[idx[i]] = tt_chosen
            
            n_completed += 1
    
    if dropna:
        tt_scores.dropna(inplace=True)
        
    return tt_scores

def find_travel_time_plz_from_table(plz, hospital_id, tt_file = "../Intermediate_Files/tt_lookup_plz_all.csv"):
    """
    plz: plz5 code for patient
    hospital_id: destination hospital
    tt_file: data frame or path to plz to hospital data file with columns corresponding to hospitals, rows with plz
    
    return travel time floating point number from plz to hospital
    """
    
    # load in reference data
    if isinstance(tt_file, str):
        # import file at path
        tt_file = GF.file_to_df(tt_file, header_number=0, separator = ",")
    elif not isinstance(tt_file, pd.DataFrame):
        raise ValueError("patient data needs to either be a data frame or a file path")

    try:
        return tt_file.loc[plz, hospital_id]
    except LookupError:
        return None
    


def pid_TT_quantile_of_chosen_ranks(chosen_tt_ranks, quantiles = [0, 0.3, 0.7, 1]):
    """
    chosen_tt_ranks: data frame of patient ID with the travel time rank of their hospital
    quantiles: list of fractions at which to break quantiles
    
    Returns single column data frame of patient IDs and quantiles of travel time ranks
    """
    
    # set up output structure and find needed quantile values
    chosen_tt_quantile = pd.DataFrame(index=chosen_tt_ranks.index, columns=["travel_time_cat_quantile"])
    quantile_vals = np.quantile(chosen_tt_ranks["travel_time_cat_quantile"], quantiles).tolist()
    
    # find quantile group for each patient
    for i in chosen_tt_ranks.index:
        for j, q in enumerate(quantiles[:-1]):
            if chosen_tt_ranks["travel_time_cat_quantile"].loc[i] > quantile_vals[j]:
                if chosen_tt_ranks["travel_time_cat_quantile"].loc[i] <= quantile_vals[j+1]:
                    chosen_tt_quantile["travel_time_cat_quantile"].loc[i] = j+1
    
    return chosen_tt_quantile.dropna()


def pid_TT_rank_choice(data_pattr, travel_time_selected_TA, treatment_area, rank_cap=None):
    """
    data_pattr: data frame of patient attributes to 
    travel_time_selected_TA:
    rank_cap: maximum rank to assign, further entries will be given this rank
    
    Returns series of the rank of each patient's choice
    """
    tt_rank = travel_time_categorize_rank_table(travel_time_selected_TA, treatment_area=treatment_area, rank_cap=rank_cap)

    chosen_tt_ranks = pd.DataFrame(index=data_pattr.index, columns=["travel_time_cat_quantile"])
    for i in data_pattr.index:
        if pd.notnull(data_pattr["plz"].loc[i]) and pd.notnull(data_pattr["ik_site_number"].loc[i]):
            chosen_tt_ranks["travel_time_cat_quantile"].loc[i] = find_travel_time_plz_from_table(data_pattr["plz"].loc[i], data_pattr["ik_site_number"].loc[i], tt_file=tt_rank)
    
    return chosen_tt_ranks.dropna()



