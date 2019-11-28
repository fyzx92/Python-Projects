# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 15:09:22 2019

@author: bryce
"""


import os
#os.chdir('/home/bryce/Shared/TUB_thesis/Patient Choice/Python_Files')
os.chdir('C:/Users/bryce/Documents/TUB_thesis/Patient Choice/Python_Files')
import sys
sys.path.insert(0, './')

import GeneralFunctions as GF

# select treatment area
treatment_areas = [
                   "Dummy"
                   #"CHE",
                   #"RPE",
                   #"KOLREK",
                   #"KNIETEP"
                  ]



###############################################################################
# choose specific patient or hospital groups by name
target_p_groups = [] 
target_h_groups = [] 




# choose patient or hospital groups by included categories
patient_subset = {
                  "_r":[], # ruralness
                  "_g":[], # gender
                  "_s":[], # severity
                  "_a":[], # age
                  "_t":[]  # time importance ranking
                  }
hospital_subset = {
                   "_q":[], # quality
                   "_v":[], # case volume
                   "_d":[], # dedicated dept
                   }
combine_subset_vars = "intersection"

subset_travel_time = False


# choose whether to prune groups, exclude below assigned thresholds
prune_groups = False
prune_cum_p_threshold = 0.2
prune_simple_p_threshold = 0.02
prune_cum_h_threshold = prune_cum_p_threshold
prune_simple_h_threshold = prune_simple_p_threshold


###############################################################################


# choose scoring method ("linear", "exponential"), and whether to reduce pool
scoring_type = "linear"
reduce_hospital_pool = True
hospital_pool_selection = "multiplier"





# variables you want to relate to choice
patient_analysis_variables = [
                              "Age", 
                              "Gender", 
                              "Ruralness_ktyp", 
                              "Severity"
                              ]

hospital_analysis_variables = [
                               "university_hospital", 
                               "case_volume", 
                               "number_beds_total", 
                               "hospital_type", 
                               "dedicated_dept", 
                               "QI"
                               ]

str_maps = {"hospital_type":
                            {
                            "private":1, 
                            "clinic":2, 
                            "public":3
                            }

            }

n_quantiles=5
age_categories = [0, 50, 60, 70, 80, 1000]


rank_cap=None
effective_maximum_quantile = 0.95

###############################################################################


# save results
save_results = True




# plot histograms. Can be very slow
make_plots = False





# all from scratch
all_from_scratch = True




# always drop all rows that have any missing values
all_drop_na = True




# overwrite all intermediate files in path, use "" to skip saving
global_export_path = "../Intermediate_Files/"
#global_export_path = ""


###############################################################################

def ta_to_name(treatment_areas):
    # naming system for files based on treatment area(s)
    return "_".join(treatment_areas)

def ta_to_path(treatment_areas):
    # find the path for the treatment area
    ta_to_path = {
                  "Dummy": "../03 Patient & Hospital features/dummy_data.xlsx",
                  "CHE":"../03 Patient & Hospital features/190123-data input-CHE-incl_struc_data.xlsx",
                  "RPE":"../03 Patient & Hospital features/190123-data input-RPE-incl_struc_data.xlsx",
                  "KOLREK":"../03 Patient & Hospital features/190123-data input-KOLREK-incl_struc_data.xlsx",
                  "KNIETEP":"../03 Patient & Hospital features/190123-data input-KNIETEP-incl_struc_data.xlsx"
                  }
    return [ta_to_path[i] for i in treatment_areas]

def ta_to_pchoice(ta):
    """
    from a treatment area name, load the file for pchoice for the treatment area
    """
    if not isinstance(ta, str):
        ta = ta_to_name(ta)
    path = f"../Intermediate_Files/{ta}_hospital_features_by_patient.csv"
    return GF.check_for_saved(path)

def ta_to_hstruct(ta):
    """
    from a treatment area name, load the file for hstruct for the treatment area
    """
    if not isinstance(ta, str):
        ta = ta_to_name(ta)
    path = f"../Intermediate_Files/{ta}_imported_hospital_structural_data.csv"
    return GF.check_for_saved(path)


def ta_to_pattr(ta):
    """
    from a treatment area name, load the file for pattr for the treatment area
    """
    if not isinstance(ta, str):
        ta = ta_to_name(ta)
    path = f"../Intermediate_Files/{ta}_imported_patient_attributes_data.csv"
    return GF.check_for_saved(path)

def ta_to_TT(ta=None):
    """
    from a treatment area name, load the file for TT_selected_ta for the treatment area
    """
    if ta=="Dummy":
        path = "../Intermediate_Files/tt_plz_full_lookup_table_dummy.csv"
        
    elif subset_travel_time or not ta:
        if not isinstance(ta, str):
            ta = ta_to_name(ta)
        path=f"../Intermediate_Files/{ta}_tt_plz_table.csv"
    else:
        path = "../Intermediate_Files/tt_plz_full_lookup_table.csv"

    return GF.check_for_saved(path)