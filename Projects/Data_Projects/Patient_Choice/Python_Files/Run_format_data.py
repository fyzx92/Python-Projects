# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 13:38:29 2019

@author: bryce
Format Data
"""

import pandas as pd
import seaborn as sns

import os
#os.chdir('/home/bryce/Shared/TUB_thesis/Patient Choice/Python_Files')
os.chdir('C:/Users/bryce/Documents/TUB_thesis/Patient Choice/Python_Files')
import sys
sys.path.insert(0, './')

import ExtractVariables as EV
import MakeCategories as MC
import TravelTime as TT
import AnalysisFormat as AF
import GeneralFunctions as GF
import config


ta = config.ta_to_name(config.treatment_areas)

paths = config.ta_to_path(config.treatment_areas)

# travel time file structure, table is much faster, but must be generated, columns may not work
if not os.path.isfile("../Intermediate_Files/tt_plz_full_lookup_table.csv"):
    for i in range(100):
        try:
            TT.make_travel_time_plz_table(fill="nans")
        except MemoryError:
            pass
#%%
###############################################################################
# load patient, hospital and time data for a given treatment area
###############################################################################


# extract patient and hospital data directly to data frame
# selected variables are optional parameter passed as list to functions (hospital_factors, patient_factors)
data_pattr = EV.extract_patient_attr_data(patient_factors=config.patient_analysis_variables, 
                                          treatment_area=ta, 
                                          paths=paths, 
                                          export_path=config.global_export_path, 
                                          from_scratch=config.all_from_scratch, 
                                          dropna=config.all_drop_na)

data_hstruct = EV.extract_hospital_struct_data(hospital_factors=config.hospital_analysis_variables, 
                                               treatment_area=ta, 
                                               paths=paths, 
                                               export_path=config.global_export_path, 
                                               from_scratch=config.all_from_scratch, 
                                               dropna=config.all_drop_na)

if config.make_plots:
    sns.pairplot(data_pattr, vars=data_pattr.columns)
    sns.pairplot(data_hstruct, vars=data_pattr.columns)



#%%
# find subset of travel times between relevant hospitals and patients


print("finding relevant plzs and hospitals")
patient_plzs = list(pd.unique(data_pattr["plz"]))
hospitals = list(pd.unique(data_hstruct["ik_site_number"]))

if config.subset_travel_time:
    travel_time_selected_TA = TT.subset_travel_time_table(ta, 
                                                          patient_plzs, 
                                                          hospitals, 
                                                          export_path=config.global_export_path, 
                                                          from_scratch=config.all_from_scratch)
else:
    travel_time_selected_TA = GF.check_for_saved("../Intermediate_Files/tt_plz_full_lookup_table.csv")


#%%
# travel time ranking of all patients

# include ranked travel time in categorizing, for group construction
chosen_tt_ranks = TT.pid_TT_rank_choice(data_pattr, travel_time_selected_TA, treatment_area = ta, rank_cap=config.rank_cap)

chosen_tt_quantile = TT.pid_TT_quantile_of_chosen_ranks(chosen_tt_ranks, quantiles = [0, 0.3, 0.7, 1])

data_pattr = data_pattr.merge(chosen_tt_quantile["travel_time_cat_quantile"], 
                              left_index=True, right_index=True, how="left")




#%%
###############################################################################
# categorizing, and grouping patients, times, hospitals
# requires data_pattr, data_hstruct, target_group
###############################################################################


                    
data_pattr_numerical, patient_str_maps = \
            MC.categorize_vars(data_pattr, 
                               config.patient_analysis_variables, 
                               patient_or_hospital="patient",
                               treatment_area = ta, 
                               n_quantiles=config.n_quantiles, 
                               age_categories = config.age_categories,
                               str_maps=config.str_maps, 
                               cat_nums=False,
                               export_path=config.global_export_path, 
                               from_scratch=config.all_from_scratch, 
                               dropna=config.all_drop_na)



data_pattr_categorized, patient_str_maps = \
            MC.categorize_vars(data_pattr, 
                               config.patient_analysis_variables, 
                               patient_or_hospital="patient",
                               treatment_area = ta, 
                               n_quantiles=config.n_quantiles, 
                               age_categories = config.age_categories,
                               str_maps=config.str_maps,
                               export_path=config.global_export_path,
                               from_scratch=config.all_from_scratch, 
                               dropna=config.all_drop_na)

GF.export_data_to_file(patient_str_maps, "patient_string_maps", "../Results/", ftype="csv", overwrite=True)


#%%
# assign group identifiers to patients based on numerical category
                   
data_pattr_groups = MC.group_patients(data_pattr_categorized, 
                                      ta, 
                                      data_output_alt=data_pattr_numerical, 
                                      export_path=config.global_export_path, 
                                      dropna=config.all_drop_na, 
                                      from_scratch=config.all_from_scratch)


#%%
# define hospital variable categories

data_hstruct_numerical, hospital_str_maps = \
            MC.categorize_vars(data_hstruct, 
                               config.hospital_analysis_variables, 
                               patient_or_hospital="hospital",
                               treatment_area = ta, 
                               n_quantiles=config.n_quantiles, 
                               age_categories = config.age_categories,
                               str_maps=config.str_maps, 
                               cat_nums=False,
                               export_path=config.global_export_path, 
                               from_scratch=config.all_from_scratch, 
                               dropna=config.all_drop_na)
            
data_hstruct_categorized, hospital_str_maps = \
            MC.categorize_vars(data_hstruct, 
                               config.hospital_analysis_variables, 
                               patient_or_hospital="hospital",
                               treatment_area = ta, 
                               n_quantiles=config.n_quantiles, 
                               age_categories = config.age_categories,
                               str_maps=config.str_maps,
                               export_path=config.global_export_path,
                               from_scratch=config.all_from_scratch, 
                               dropna=config.all_drop_na)

GF.export_data_to_file(hospital_str_maps, "hospital_string_maps", "../Results/", ftype="csv", overwrite=True)

#%%
# assign group identifiers to hospitals based o numerical category
                    
data_hstruct_groups = MC.group_hospitals(data_hstruct_categorized, 
                                         ta, 
                                         data_output_alt=data_hstruct_numerical,
                                         export_path=config.global_export_path,
                                         dropna=config.all_drop_na,
                                         from_scratch=config.all_from_scratch)


#%%
###############################################################################
# scoring system by variable, scaled relative to alternatives
# requires data_pattr, data_hstruct
###############################################################################

# restructure data to get patient ID and structural information of their chosen hospital
data_pchoice = AF.calculate_patient_choice_factors(treatment_area = ta,
                                                   hospital_data = data_hstruct_groups, 
                                                   patient_data = data_pattr_groups, 
                                                   hospital_analysis_vars = config.hospital_analysis_variables, 
                                                   patient_analysis_vars = config.patient_analysis_variables, 
                                                   export_path = config.global_export_path, 
                                                   from_scratch = config.all_from_scratch, 
                                                   dropna = config.all_drop_na)



