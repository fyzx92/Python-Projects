Patient Choice Analysis README

Program and README Authored by Bryce Burgess


Core Goal:
Separately or in aggregate take data from each of 4 different files, containing
structural hospital data and patient data for years 2015 (possibly to expand 
later), and look at which hospital features are most influential when informing
hospital choice for a given set of patients (optionally broken down by patient
characteristics, such as age, sex, severity, or ruralness).

Table of Contents

0.    Documentation

1.    Typical Use
1.1    first time setup, prerequisites
1.2    setting execution options, changing variables
1.3    running analysis
1.4    interpreting results

2.    Python Files
2.1    Executed files
2.2    ExtractVariables
2.3    TravelTime
2.4    MakeCategories
2.5    AnalysisFormat
2.6    GeneralFunctions
2.7    Descriptives
2.8    DummyDataGenerator

3.    Raw Data Files
3.1    treatment area
3.2    travel time

4.    Intermediate Files
4.1    imported
4.2    categorized
4.3    numerical
4.4    grouped
4.5    choice
4.6    travel time table
4.7    travel time subset table

*******************************************************************************
0. Documentation
The purpose of this documentation is to give a general sense for what the role 
of each component of the system does. This applies to the python files, the 
source files, and the intermediate files.

For any python files containing functions (any that don't start with Run_), the
functions are documented by listing brief descriptions of their inputs, what 
the function is intended to return, and any notes about how the function is 
used or potential pitfalls when using it. Additionally in the notes for a 
function, are listed both the places where the function is called, and the 
functions that it calls. The main exception to this is the GeneralFunctions 
module, where many of the functions are used almost everywhere.

The section on the input files lists the basic requirements that are expected 
by the code from the data files. If these conditions are not met, then the code
will either fail to function or produce highly unpredictable results.

*******************************************************************************
1. Typical Use
1.1    first time setup, prerequisites
User must have python installed, along with the modules pandas, scikit-learn, 
    matplotlib, and numpy (numbers, operator, os, sys, csv, and json, are also 
    used, but included by default in most python installations).

User must set appropriate path to find files in each run file (Run_format_data, 
    Run_subset_and_score, Run_decision_tree)

1.2    setting options, changing variables
There are a variety of setup options that can determine what is to be analyzed 
and how to analyze it. These options are in the file config.py. Some options 
govern the creation of data files, some are for selecting entries for the 
analysis, some are for how to perform the analysis. To change options more 
granularly, you must go to the relevant function call to set options, and 
override defaults as needed. There are additionally some functions for getting 
paths, names, and data files based on a treatment area.

Variables:
treatment_areas:
    This is an option that allows the user to determine which treatment areas 
    that they want to use The main options are already in the list, but 
    commented out. Whichever options are not commented out will be used in the 
    analysis. 
    This can be used to analyze multple treatment areas at once (not yet tested)
    EX. this would select only KOLREK as the treatment area
    treatment_areas = [
                       #"CHE",
                       #"RPE",
                       "KOLREK",
                       #"KNIETEP",
                       ] 

target_p_groups:
    If you only want to analyze a particular patient group or groups (you must 
    know the name beforehand), then you can enter the patient group name as a 
    string into this list. Make sure that it is a string within the list. The 
    variables, in order are ruralness, gender, severity, age category, and 
    travel time category.

    EX. this selects the patients who belong either to the group with ruralness
        3, gender 1, severity 3, age category 2, and travel time category 3, or
        the group with ruralness 2, gender 2, severity 3, age category 2, and 
         travel time category 1.
    target_p_groups=["patient_group_r3_g1_s3_a2_t3",
                     "patient_group_r2_g2_s3_a2_t1"]


target_h_groups:
    If you only want to analyze a particular hospital group or groups (you must 
    know the name beforehand), then you can enter the patient group name as a 
    string into this list. Make sure that it is a string within the list. The 
    variables, in order are quality category, case volume category, and 
    presence of dedicated department (0 or 1).

    EX. this selects only the hospitals belonging to the group with quality 
        category 2, case volume category 1, and dedicated department 1.
    target_h_groups = ["hospital_group_q2_v1_d1"]


patient_subset:
    For each patient variable (including travel time), you can enter a number 
    or numbers corresponding to the category(ies) of that variable. Entering 
    multiple values for one variable matches patients with any of those values.
    Entering values in multiple variables will by default match only patients 
    who meet all criteria, but can be changed to match patients who meet any of
    the criteria in the variable combine_subset_vars. Do not change the 
    dictionary keys, only the values in the respective lists. By default, 
    groups are formed into five categories (defined by n_quantiles in 
    categorize_vars in MakeCategories), and higher numbers indicate higher raw 
    values (not necessarily better)

    EX. this will filter patients based on being a man (gender 1), being in age
        category 1 or 2, and being in travel time category 3. Always verify 
        that check combine_subset_vars combines these the way you want.
    patient_subset = {
                      "_r":[],
                      "_g":[1],
                      "_s":[],
                      "_a":[1,2],
                      "_t":[3]
                      }


hospital_subset:
    For each hospital variable, you can enter a number or numbers corresponding
    to the category(ies) of that variable. Entering multiple values for one 
    variable match patients with any of those values. Entering values in 
    multiple variables will by default match only hospital that meet all 
    criteria, but can be changed to match hospitals that meet any of the 
    criteria in the variable combine_subset_vars. Do not change the dictionary 
    keys, only the values in the respective lists. By default, groups are 
    formed into five categories (defined by n_quantiles in categorize_vars in 
    MakeCategories), and higher numbers indicate higher raw values (not 
    necessarily better)

    EX. this will filter hospitals based on being in quality category 2 or 3, 
        having case volume category 1, and will ignore the presence or absence 
        of a dedicated department. Always verify that check combine_subset_vars
        combines these the way you want.
    hospital_subset = {
                       "_q":[2,3],
                       "_v":[1],
                       "_d":[],
                       }


combine_subset_vars:
    This variable, set to either "intersection" or "union" determines how to 
    filter based on values in different variables in either of the _subset 
    dictionaries. "intersection" will take only the patients who meet all 
    provided criteria, "union" will take patients who meet any of the criteria.


prune_groups=True:
    Prune groups determines whether you want to cut out groups (for both 
    patients and hospitals) that do not meet the thresholds. 


prune_cum_p_threshold=0.2:
    This takes a number between 0 and 1 to determine the percentage of the 
    total patient entries you want to remove starting with the smallest group. 
    It continues until removing more would put the number of removed patients 
    above the set fraction of the total.


prune_cum_h_threshold=0.2:
    This takes a number between 0 and 1 to determine the percentage of the 
    total hospital entries you want to remove starting with the smallest group.
    It continues until removing more would put the number of removed hospitals 
    above the set fraction of the total.


prune_simple_p_threshold=0.02:
    Takes a number between 0 and 1 to determine how big you allow the smallest 
    group to be relative to the total number of patients being analyzed. It 
    will cut any entries belonging to groups smaller than that percent.


prune_simple_h_threshold=0.02:
    Takes a number between 0 and 1 to determine how big you allow the smallest 
    group to be relative to the total number of hospital being analyzed. It 
    will cut any entries belonging to groups smaller than that percent.


scoring_type="linear":
    What kind of scoring compression to use. "linear" scales all values 
    linearly within a variable to the range [0,1], where "exponential" uses an 
    exponential curve (base 2) scaled to the mean (except for QI) in the data 
    set. Both then have a second adjustment that modifies the score based on 
    how it compares to the availability within the data.


reduce_hospital_pool:
    Binary option (True or False) to choose whether to limit the number of 
    hospitals considered as alternatives for a given patient. Further 
    customization is available in the function call linear_score2 in the file 
    Analysis_format.


patient_analysis_variables:
    List of strings containing the names of the patien variables that you want 
    to be analyzed. The names must be exactly as they appear in the raw data 
    set that you are extracting from.

    EX.
    patient_analysis_variables = [
                                  "Age", 
                                  "Gender", 
                                  "Ruralness_ktyp", 
                                  "Severity"
                                  ]


hospital_analysis_variables:
    List of strings containing the names of the patien variables that you want 
    to be analyzed. The names must be exactly as they appear in the raw data 
    set that you are extracting from.

    EX.
    hospital_analysis_variables = [
                                   "university_hospital", 
                                   "case_volume", 
                                   "number_beds_total", 
                                   "hospital_type", 
                                   "dedicated_dept", 
                                   "QI"
                                   ]

str_maps:
    A dictionary of dictionaries for mapping the values of string variables to 
    numerical values. The key for each entry is a column name and each value 
    is a dictionary mapping the possible string values of that column to the 
    desired numerical value. This option is not mandatory to set

    EX. When used in the categorize_vars function, this will take all entries
        in the column "hospital_type" and map those labeled "privat" to the 
        number 1, "freigemeinnützig" to the value 2, and "öffentlich" to the 
        value 3.
    str_maps = {"hospital_type":
                                {
                                "privat":1, 
                                "freigemeinnützig":2, 
                                "öffentlich":3
                                }
                }


n_quantiles=5:
    The number of quantiles to use when creating categories of continuous or
    nearly continuous variables. Primarily used in the function 
    categorize_nums, which is called from the function categorize_vars.


age_categories = [0, 50, 60, 70, 80, 1000]:
    The boundaries of the age categories to use when categorizing age in the 
    categorize_age function, called in categorize_vars. If this list has N
    entries, there will be N-1 created categories.


rank_cap=None:
    The maximum ranking value to assign in the TravelTime rank table. None
    does not limit the maximum value (worst ranking value) in the table.


effective_maximum_quantile = 0.95:
    Used in all linear scoring functions (found in TravelTime and 
    Analysis_format). This determines the "maximum" to use for linearly 
    compressing the raw values. This is to reduce or remove outlier values. 
    If set too low, it may cause issues with highly unbalanced binary 
    variables.

save_results:
    Binary (True or False) option to save results at the end of analysis. Leave
    False if testing, True for running analyses. Result file names are saved 
    with a treatment area and version number, so you can compare changes with 
    different methods


make_plots=False:
    Binary (True or False) option for whether to create descriptive plots 
    during the calculation. Doing so is very slow, recommend to leave it False 
    unless specifically needed.


all_from_scratch:
    Global binary (True or False) option to determine whether functions that 
    save calculated data as a file should load previously calculated data or 
    recalculate fresh. Files will only be loaded if they exist and are found. 
    Separate files can coexist for different treatment areas. To recompute only
    specific files, override all_from_scratch by going to that function call 
    and passing True to the from_scratch option.


all_drop_na:
    Global binary (True or False) option to drop entries with missing values at
    every step. Missing values often appear when combining the data of two 
    sets, as the lookup value may not be found.


global_export_path="../Intermediate_Files/":
    Path to export intermediate files to. Assign an empty string "" to not save
    files.


Functions:
ta_to_name:
    inputs:
        treatment_areas: List of strings, codes of each treatment area

    returns: A single joined string of provided codes. Joined by "_"
    notes: Called by other ta_to_ ... functions, Run_format_data, 
        Run_decision_tree, and Run_subset_and_score.

ta_to_path:
    inputs:
        treatment_areas: List of strings, codes of each treatment area

    returns: List of paths to the file containing data for that treatment area
    notes: This uses a dictionary of locations in the filesystem for where to 
        find raw data files for each of the possible treatment areas. If you 
        add new entries to the possible treatment areas, then you must also add
        an entry for the path to that treatment area. Note: paths are relative,
        so that putting this program onto a new computer does not require 
        updating these paths. Called by Run_format_data.

ta_to_pchoice:
    inputs:
        ta: A joined treatment area name, or list of codes (str or list of str)

    returns: A data frame of patient and associated hospital data for the 
        treatment area(s).
    notes: Called by Run_decision_tree, and Run_subset_and_score. 
        Calls ta_to_name.

ta_to_pattr:
    inputs:
        ta: A joined treatment area name, or list of codes (str or list of str)
    returns: A data frame of patient data for the treatment area(s).
    notes: Called by Run_subset_and_score. Calls ta_to_name.

ta_to_hstruct:
    inputs:
        ta: A joined treatment area name, or list of codes (str or list of str)

    returns: A data frame of hospital data for the treatment area(s).
    notes: Called by Run_subset_and_score. Calls ta_to_name.

ta_to_TT:
    inputs:
        ta=None: A joined treatment area name, or list of codes (str or list of str)

    returns: A data frame of reduced travel times of patients and hospitals 
        relevant to treatment area. No travel time chooses the full lookup table.
    notes: Called by Run_subset_and_score. Calls ta_to_name.


1.3     running analysis
After setting the desired analysis options in the config file, one can run 
whichever of the execution files you want. Note: both Run_subset_and_score and 
Run_decision_tree use data from Run_format_data, so Run_format_data must have 
been run on the correct treatment area previously. These can either be run in 
an IDE to allow for running it in parts and more investigation of the methods, 
or run from a terminal or command line.

Run_format_data:
Travel Time Table:
    Not an option, but if the only travel time data is listed in column format 
    (one column each for plz, hospital id, and travel time), this will 
    construct a new file with all of the same data, but reformatted to be much 
    faster to use. Try to preserve this generated file if possible, as it can 
    take upwards of two days to complete this one computation. This is still 
    much faster than trying to do the analysis with the column format.

Run_subset_and_score:
If the save_results option was set to True, the results of Run_subset_and_score
will be saved in a csv (or optionally json) file in the Results folder. This 
will have an entry for each variable and an associated score. The saved file 
will not be overwritten by subsequent analyses, and the name will include a 
simple counter for each time the file was saved. These files are not loaded by 
the program, so feel free to change the name to be more descriptive.

Run_decision_tree:
Run_decision_tree will also create, train and test a decision tree to determine
how well a series of patient variables can predict a hospital type. Similarly, 
it does the same for a second decision tree to predict a patient group based on
hospital variables [NOT YET FINISHED]. Then these predictions are repeated with 
Random Forest Classifiers.

If you want to perform sensitivity analyses on the algorithm, some likely 
variables are listed below. Each can be set within config.py:
    treatment area
    subgroups
    linear versus exponential scoring
    effective maximum in linear scoring methods
    the number of quantiles used for categorizing
    the age grouping categories
    setting and changing the rank cap for travel times


1.4     interpreting results
The results are a list of the hospital analysis variables, each of which is 
listed with a mean, median, and variance of the patient scores. The patient 
scoring method is set by an option, but in all cases, they take into account 
the availability of the variable values in the hospital population. A mean 
value of 0 means that this variable was very strongly selected against, 0.5 
that patients tended to be neutral about it, and 1 suggests that patients 
tended to strongly select for this variable.

The option to reduce the hospital pool on a per-patient basis changes 
interpretation somewhat. The hospital pool is determined by the travel time of 
the patient's choice and the method (multiplier, polynomial, ...). This may 
make the score more realistic, but also adds a potential bias, particularly in 
the travel time score.

The hospital types will be included here, each with their own score, showing 
the relative frequency that each was chosen over the others. 



*******************************************************************************
2. Python Files
2.1 Executed Files
These are the files that will be most used by the User. The Run_ files are for
executing tasks (formatting data, generating scores, predicting with decision 
trees), while the config file is to set options for these executed tasks.

Run_format_data, Run_subset_and_score, Run_decision_tree
    The three primary files that will be directly run by the user are 
    "Run_format_data.py", "Run_subset_and_score.py", "Run_decision_tree.py". 
    None declare any functions, but instead import the functions that they need 
    from the other files, and call them as needed. Function calls can be 
    overriden in place, but are generally best left alone. 

config
    To change the parameters of an analysis, look at the options in the 
    "config.py" file. This file is not directly run by the others, but is 
    imported and referenced by all of them, allowing for greater internal 
    consistency with options.

2.2 ExtractVariables
    ExtractVariables defines how the algorithm imports the raw data with only 
    the desired variables.

extract_patient_attr_data:
    inputs:
        patient_factors: list of variable names as strings that you want to 
            extract from the raw data for analysis. Other variables needed for 
            cross referencing are automatically included. These are "versid", 
            "ik_site_number", "plz", "year", and "treatment_area".

        treatment_area: string for the treatment area, used to name output
            file. Best to use the one computed in the main file as "ta", so 
            that naming is consistent across all saved files.

        paths: string representing the path to the raw file to use. If the path
            is not found, it will give an error.

        export_path="../Intermediate_Files/": path for saving data. Usually set
            to global_export_path, which is defined in config.py. Leave an 
            empty string "" to not save the file.

        from_scratch=False: option to recompute output data file instead of 
            loading previous calculation. Loading existing data is faster, but 
            not meaningful if parameters have changed. It does not check if the 
            data being loaded is different. Usually set by all_from_scratch in 
            config.py.

        dropna=False: option to drop all rows that have any missing values. Can
            majorly reduce the size of the dataset, but is needed for some of 
            the analyses. Usually set by all_drop_na in config.py.

    returns: a data frame of patient analysis variables and referencing 
        variables
    notes: it contains an option to output the data that it extracted 
        previously for the given treatment area. Setting from_scratch to True 
        makes it not look for existing files. Sets indexing, checks for 
        duplicates and missing values. Called in Run_format_data. 
        Calls assign_bulk_data, check_for_saved, files_to_dict, 
        export_data_to_file.


extract_hospital_struct_data:
    inputs:
        hospital_factors: the variables that you want to extract from the raw 
            data for analysis. Other variables needed for cross referencing are 
            automatically added. These are "treatment_area", "year", 
            "ik_site_number", and "ik_site_number_year".

        treatment_area: string for the treatment area, used to name output
            file. Best to use the one computed in the main file as "ta", so 
            that naming is consistent across all saved files.

        paths: string representing the path to the raw file to use. If the path
            is not found, it will give an error.

        export_path="../Intermediate_Files/": path for saving data. Usually set
            to global_export_path, which is defined in config.py. Leave an 
            empty string "" to not save the file.

        from_scratch=False: option to recompute output data file instead of 
            loading previous calculation. Loading existing data is faster, but 
            not meaningful if parameters have changed. It does not check if the
            data being loaded is different. Usually set by all_from_scratch in 
            config.py.

        dropna=False: option to drop all rows that have any missing values. Can
            majorly reduce the size of the dataset, but is needed for some of 
            the analyses. Usually set by all_drop_na in config.py.

    returns: a data frame of patient analysis variables and linking variables
    notes: it contains an option to output the data that it extracted previously 
        for the given treatment area. Setting from_scratch to True makes it not look 
        for existing files. Additionally checks that the hospital ID in the hospital 
        structural data is year-independent. Sets indexing, checks for duplicates and
        missing values. Called in Run_format_data. Calls assign_bulk_data, 
        check_for_saved, files_to_dict, export_data_to_file.


assign_bulk_data:
    inputs:
        data_pull: data frame to pull data from. 

        factors: list of column names to pull. 

    returns: data frame of desired columns
    notes: used as a helper function to the other two, for simply assigning 
        data. Called by extract_patient_attr_data, and 
        extract_hospital_struct_data.

2.3 TravelTime
    Travel_Time contains all functions to do with importing, restructuring, 
    categorizing, scoring and looking up travel time values.


subset_travel_time_table
    inputs:
        treatment_area: string for the treatment area, used to name output
            file. Best to use the one computed in the main file as "ta", so 
            that naming is consistent across all saved files.

        patient_plzs=None: relevant plzs to treatment area. If None, it will 
            not reduce the set of plzs in the table.

        hospitals=None: relevant hospitals to treatment area. If None, it will 
            not reduce the set of hospitals in the table.

        export_path="../Intermediate_Files/": path for saving data. Usually set
            to global_export_path, which is defined in config.py. Leave an 
            empty string "" to not save the file.

        from_scratch=False: option to recompute output data file instead of 
            loading previous calculation. Loading existing data is faster, but 
            not meaningful if parameters have changed. It does not check
            if the data being loaded is different. Usually set by 
            all_from_scratch in config.py.

        dropna=False: option to drop all rows that have any missing values. Can
            majorly reduce the size of the dataset, but is needed for some of 
            the analyses. Usually set by all_drop_na in config.py.

    returns: reduced travel time table containing only the hospitals and 
        patients relevant to a treatment area or group of treatment areas.
    notes: Called by Run_format_data. Calls check_for_saved, 
        export_data_to_file.

travel_time_categorize_rank_table
    inputs:
        travel_time_selected_TA: the reduced travel time table for only 
            hospitals and patients relevant to a given treatment area. 
            Calculated by subset_travel_time_table.

        treatment_area: string for the treatment area, used to name output
            file. Best to use the one computed in the main file as "ta", so 
            that naming is consistent across all saved files.

        export_path="../Intermediate_Files/": path for saving data. Usually set
            to global_export_path, which is defined in config.py. Leave an 
            empty string "" to not save the file.

        from_scratch=True: option to recompute output data file instead of 
            loading previous calculation. Loading existing data is faster, but 
            not meaningful if parameters have changed. It does not check
            if the data being loaded is different. Usually set by 
            all_from_scratch in config.py.

        rank_cap=None: maximum value for ranks. All greater values will be 
            replaced by this. None will not replace any greater values, it will
            just keep counting.
 
        verbose=False: whether to print progress or stay silent

    returns: New file of travel times, each entry is replaced by its rank 
        relative to alternatives for a plz.
    notes: Called by Run_format_data.

make_travel_time_plz_table:
    inputs: 
        fill="load": determines what to do if the saved file is found. "load" 
            is to return the save file if it is found, "nans" is to try and 
            complete the saved file,"from_scratch" is to recreate the entire 
            saved file. If told to "load" orbuild from "nans" on a nonexistent 
            file, it will try to create it from scratch.

    returns: Nothing
    notes: checks an internally defined path to the column structured travel 
        time and rearranges it so that each row is a plz code, each column is a
        hospital ID. Automatically saves every fifty entries, as it is easy for
        it to run out of memory. If memory runs out before it completes fifty 
        entries, try setting this to a smaller value. Called by 
        Run_format_data. Calls check_for_saved, file_to_df, find, 
        export_data_to_file.

travel_time_linear_score
    inputs:
        data_p: patient data frame, used to determine the alternative travel 
            times.

        travel_time_selected_TA: the reduced travel time table for only 
            hospitals and patients relevant to a given treatment area. 
            Calculated by subset_travel_time_table.

        dropna=True: option to drop all rows that have any missing values. Can 
            majorly reduce the size of the dataset, but is needed for some of 
            the analyses. Usually set by all_drop_na in config.py.

        verbose=False: whether to print progress or stay silent.

        effective_maximum_quantile: quantile to use as effective maximum when 
            compressing values

    returns: Two column data frame of patient ID and the score (calculated with
        linear function) of that patient's choice relative to their 
        alternatives. 
    notes: Called by Run_subset_and_score. Calls find, 
        find_travel_time_plz_from_table.


travel_time_exponential_score
    inputs:
        data_p: patient data frame, used to determine the alternative travel times.

        travel_time_selected_TA: the reduced travel time table for only 
            hospitals and patients relevant to a given treatment area. 
            Calculated by subset_travel_time_table.

        dropna=True: option to drop all rows that have any missing values. Can majorly 
            reduce the size of the dataset, but is needed for some of the 
            analyses. Usually set by all_drop_na in config.py.

        verbose=False: whether to print progress or stay silent.

    returns: Two column data frame of patient ID and the score (calculated with
        exponential function) of that patient's choice relative to their 
        alternatives.
    notes: Called by Run_subset_and_score. Calls find, 
        find_travel_time_plz_from_table.

find_travel_time_plz_from_table
    inputs:
        plz: plz or list of plzs to find.

        hospital_id: hospital or list of hospitals to find.

        tt_file= "../Intermediate_Files/tt_lookup_plz_all.csv": file to use for
        reference, defaults to full table.

    returns:
    notes: simple lookup function to find time between a plz and a hospital. If
        a list is provided to both arguments, it will return a dataframe of all 
        combinations. Called by travel_time_linear_score, 
        travel_time_exponential_score, pid_TT_rank_choice

pid_TT_quantile_of_chosen_ranks:
    inputs:
        chosen_tt_ranks: data frame of patient ID with the travel time rank of 
            their hospital.

        quantiles = [0,0.3,0.7,1]: list of fractions at which to break 
            quantiles. Defaults to the minimum, 30th percentile, 70th 
            percentile, and maximum.

    returns: single column data frame of patient IDs and quantiles of travel 
        time ranks
    notes: Called by Run_format_data.

pid_TT_rank_choice:
    inputs:
        data_pattr: data frame of patient attributes.

        travel_time_selected_TA: the reduced travel time table for only 
            hospitals and patients relevant to a given treatment area. 
            Calculated by subset_travel_time_table.

        treatment_area:string for the treatment area, used to name output
            file. Best to use the one computed in the main file as "ta", so 
            that naming is consistent across all saved files.

        rank_cap: maximum rank to assign, further entries will be given this 
            rank

    returns: data frame of ranks of patients' chosen hospitals compared to 
        their alternatives.
    notes: Called by  Run_format_data. Calls find_travel_time_plz_from_table.


2.4 MakeCategories
    MakeCategories categorizes, makes groups, and subsets based on categories 
        and groups.

categorize_vars: 
    inputs:
        data: data frame containing variables to categorize.

        analysis_variables: selected variables to put into categories.

        patient_or_hospital: string "patient" or "hospital" for file naming.

        treatment_area: string for the treatment area, used to name output.
            file. Best to use the one computed in the main file as "ta", so 
            that naming is consistent across all saved files.

        n_quantiles=5: desired number of quantiles to break patients into.
   
        age_categories=[0,50,60,70,80,1000]: values to use as borders between 
            age categories

        str_maps={}: dictionary of dictionaries, variable name to dictionary of
            string-number assignments.

        cat_nums: whether to categorize numerical variables. False only looks 
            at string variables.

        export_path="../Intermediate_Files/": path for saving data. Usually set
            to global_export_path, which is defined in config.py. Leave an 
            empty string "" to not save the file.

        return_map: whether to return the map relating the number to the string.

        from_scratch=False: option to recompute output data file instead of 
            loading previous calculation. Loading existing data is faster, but 
            not meaningful if parameters have changed. It does not check if the
            data being loaded is different. Usually set by all_from_scratch in 
            config.py.

        dropna=True: option to drop all rows that have any missing values. Can 
            majorly reduce the size of the dataset, but is needed for some of 
            the analyses. Usually set by all_drop_na in config.py.

    returns: data frame where values in designated columns have been lumped 
        into categories.
    notes: Called by Run_format_data. Calls categorize_age, categorize_str, and
        categorize_nums to perform main computations. Also calls 
        check_for_saved, export_data_to_file.

categorize_age:
    inputs:
        series: data frame column of numbers to lump into categories defined by
        the age_categories list.

        age_categories=[0,50,60,70,80,1000]: list of numbers defining the 
            borders of the age categories. Default is [0,50,60,70,80,1000]. 
            Don't forget to have a high upper limit.

        verbose: whether to print progress or stay silent.

    returns: categorized version of series, with row labels left intact
    notes: Called by categorize patient_vars. 

categorize_str:
    inputs:
        series: data frame column of string variables from which to create 
            categories

        str_to_num_map={}:dictionary mapping variable names to assigned numbers. If
            none, one will be created.

        verbose: whether to print progress or stay silent.

    returns: series where each string is assigned its own category, in order of
        appearance, and a dictionary of map between names and numbers.
    notes: since strings cannot generally be ordered or grouped in a meaningful
        way, each string is simply given its own category. Called by 
        categorize_patient_vars, and categorize_hospital_vars.

categorize_nums:
    inputs:
        series: data frame column of numerical variables from which to create 
            categories

        n_quantiles: the number of desired quantiles to use for creating 
            categories.

        verbose: whether to print progress or stay silent.

    returns: series of categories defined by quantiles of original numerical 
        data.
    notes: if there are not many unique values (< 2 * number quantiles) it will
        leave the list as it is. Also drops any repeated indices. Called by 
        categorize_patient_vars and categorize_hospital_vars. 

group_patients:
    inputs: 
        data_pattr_categorized: dataframe of categorized patient variables, 
            containing at least a ruralness, severity, and age variable

        treatment_area: string for the treatment area, used to name output
            file. Best to use the one computed in the main file as "ta", so 
            that naming is consistent across all saved files.

        data_output_alt=None: optional dataframe to append group names, even if
            loading from saved file. None just returns the series of patient 
            groups with patient ids as indices.

        export_path="../Intermediate_Files/": path for saving data. Usually set
            to global_export_path, which is defined in config.py. Leave an empty 
            string "" to not save the file.

        from_scratch=False: option to recompute output data file instead of 
            loading previous calculation. Loading existing data is faster, but 
            not meaningful if parameters have changed. It does not check if the
            data being loaded is different. Usually set by all_from_scratch in 
            config.py.

        dropna=True: option to drop all rows that have any missing values. Can 
            majorly reduce the size of the dataset, but is needed for some of 
            the analyses. Usually set by all_drop_na in config.py

    returns: data frame containing patient group names, optionally appended to 
        data_output_alt.
    notes: Saves groups as a file only containing the patient identifier and 
        group name. Called by Run_format_data. Calls check_for_saved, 
        export_data_to_file.

group_hospitals:
    inputs: 
        hospital_structural_data: dataframe of categorized hospital variables, 
            containing at least a QI, case_volume, and dedicated_department 
            variable.

        treatment_area: string for the treatment area, used to name output
            file. Best to use the one computed in the main file as "ta", so 
            that naming is consistent across all saved files.

        data_output_alt=None: optional dataframe to append group names, even if 
            loading from saved file. None just returns the series of patient 
            groups with patient ids as indices.

        export_path="../Intermediate_Files/": path for saving data. Usually set
            to global_export_path, which is defined in config.py. Leave an 
            empty string "" to not save the file.

        from_scratch=False: option to recompute output data file instead of 
            loading previous calculation. Loading existing data is faster, but 
            not meaningful if parameters have changed. It does not check
            if the data being loaded is different. Usually set by 
            all_from_scratch in config.py.

        dropna=True: option to drop all rows that have any missing values. Can 
            majorly reduce the size of the dataset, but is needed for some of 
            the analyses. Usually set by all_drop_na in config.py.


    returns: data frame containing hospital group names, optionally appended to
        data_output_alt.
    notes: Saves groups as a file only containing the hospital identifier and 
        group name.Called by Run_format_data. Calls check_for_saved, 
        export_data_to_file. 

prune_group:
    inputs:
        data: data containing either a Patient_Group or Hospital_Group column

        cumsum_threshold=None: threshold for a cumulative sum. If None, it will 
            not prune groups based on cumulative sum.

        simple_threshold=None: minimum percentage of total data contained in a 
            group to be worth keeping. If None, it will not prune groups based 
            on a simple threshold.

    returns: data set after being reduced based on groups.
    notes: The threshold values are defined as the percent of the original data
        that will be removed. The cumulative sum puts the group sizes in order 
        of decreasing size, and cuts groups that cumulatively have less than 
        cumsum_threshold of the total data, starting from the smallest. Called 
        by Run_subset_and_score, Calls find.

subset_patients_or_hospitals
    inputs:
        data: A data frame with a group label column to get subsets from

        params={}: Dictionary containing group identifier parameters and 
            desired values. Empty dictionary returns input data. Passed from 
            config.py.

        group_col=None: Define the name of the group column to look in. If 
            None, it will try "Patient_Group" and then "Hospital_Group". If 
            neither is found, it will give an error.

        combine="intersection": How to combine provided values from different 
            group identifier parameters. "intersection" selects only patients 
            that meet all conditions, "union" selects all patients that meet 
            any conditions. With any other values, it returns None.

    returns: subset of data matching the provided search parameters
    notes: Called by Run_subset_and_score.

2.5 Analysis_format
    Analysis_format is primarily concerned with joining the data into its final
        form, and scoring methods.


calculate_patient_choice_factors:
    inputs:
        treatment_area: string for the treatment area, used to name output
             file. Best to use the one computed in the main file as "ta", so 
             that naming is consistent across all saved files.

        hospital_data: dataframe of hospital data to add to patient data

        patient_data: dataframe of patient data

        hospital_analysis_vars: selected variables in hospital_data to put into
            categories

        patient_analysis_variables: selected variables in patient_data to put 
            into categories

        export_path="../Intermediate_Files/": path for saving data. Usually set
            to global_export_path, which is defined in config.py. Leave an 
            empty string "" to not save the file.

        from_scratch=False: option to recompute output data file instead of 
            loading previous calculation. Loading existing data is faster, but 
            not meaningful if parameters have changed. It does not check if the
            data being loaded is different. Usually set by all_from_scratch in 
            config.py.

        dropna=False: option to drop all rows that have any missing values. Can 
            majorly reduce the size of the dataset, but is needed for some of 
            the analyses. Usually set by all_drop_na in config.py.

    returns: data frame of patient data, and the data associated with their 
        chosen hospital.
    notes: This will be used for the scoring, so it's (probably) better to 
        leave the values raw instead of categorized, but may be helpful to 
        include the patient groups, if you want to subset and look at effects 
        within the subset. Called by Run_format_data. Calls check for saved, 
        export_data_to_file.

linear_score:
    inputs:
        data_p: dataframe of values to score.

        data_h: dataframe of values to determine availability.

        positively_scaling=[]: variables that are "better" with larger values. 
            Leaving as empty list means all variables are negatively scaling.

        negatively_scaling=[]: variables that are "better" with lower values. 
            Leaving as empty list means all variables are positively scaling.

        effective_maximum_quantile: quantile to use as effective maximum when 
            compressing values.

    returns: data frame of patient values rescaled relative to other patients, 
        and adjusted for hospital availability.
    notes: the values are linearly compressed to be between 0 and 1 before 
        adjusting for hospital availability. It uses the value at eh 0.95 
        quantile instead of the maximum to reduce the effect of outliers. 
        Called by Run_subset_and_score.

linear_score2:
    inputs:
        data_p: dataframe of values to score.

        data_h: dataframe of values to determine availability.

        travel_time_selected_TA: travel time data frame to use for reference.

        upper_time_bound="all": how to restrict the pool of hospitals relative 
            to choice("all", "multiplier", "proportional", "exponent").

        positively_scaling=[]: variables that are "better" with larger values. 
            Leaving as empty list means all variables are negatively scaling.

        negatively_scaling=[]: variables that are "better" with lower values. 
            Leaving as empty list means all variables are positively scaling.

        effective_maximum_quantile: quantile to use as effective maximum when 
            compressing values.

    returns: data frame of patient values rescaled relative to other patients, 
        and adjusted for hospital availability.
    notes: the values are linearly compressed to be between 0 and 1 before 
        adjusting for hospital availability. Hospitals considered as 
        alternatives for the mean are restricted by travel time. It uses the 
        value at the 0.95 quantile instead of the maximum to reduce the effect 
        of outliers. Called by Run_subset_and_score. Calls get_hospital_mean.

exponential_score:
    inputs:
        data_p: dataframe of values to score

        data_h: dataframe of values to determine availability

        positively_scaling=[]: variables that are "better" with larger values. 
            Leaving as empty list means all variables are negatively scaling.

        negatively_scaling=[]: variables that are "better" with lower values. 
            Leaving as empty list means all variables are positively scaling.

    returns: data frame of rescaled variable values per patient, adjusted for 
        hospital availability.
    notes: Applies decaying exponential function (base 2), scaled by the mean 
        value of all available hospitals. Called by Run_subset_and_score.

exponential_score2:
    inputs:
        data_p: dataframe of values to score

        data_h: dataframe of values to determine availability

        travel_time_selected_TA: travel time data frame to use for reference.

        upper_time_bound="all": how to determine the pool of hospitals ("all", 
            "multiplier", "proportional", "exponent").

        positively_scaling=[]: variables that are "better" with larger values. 
            Leaving as empty list means all variables are negatively scaling.

        negatively_scaling=[]: variables that are "better" with lower values. 
            Leaving as empty list means all variables are positively scaling.

    returns: data frame of rescaled variable values per patient, adjusted for 
        hospital availability.

    notes: Applies decaying exponential function (base 2), scaled by the mean 
        value of all available hospitals. Hospitals considered as alternatives 
        for the mean are restricted by travel time. Called by 
        Run_subset_and_score. Calls get_hospital_mean.

get_hospital_mean:
    inputs:
        plz: single plz value associated with a patient

        hospital: single hospital name chosen by the same patient

        variable: the variable for which to get the mean from the hospital pool

        data_h: data frame of hospitals and variables, must include variable

        travel_time_selected_TA: the reduced travel time table for only 
            hospitals and patients relevant to a given treatment area. 
            Calculated by subset_travel_time_table.

        upper_time_bound="all": how to determine the pool of hospitals ("all", 
            "multiplier", "proportional").

        mean=True: whether to return the mean or the median. True is default.

    returns: Determine a pool of hospitals based on the distance to the chosen 
        hospital, and calculates the mean of variable within this pool.
    notes: Called by linear_score2, exponential_score2.

hospital_type_scoring:
    inputs:
        data_pchoice: data frame of patients, containing the column hospital 
            type, and Hospital_Group if return_group_counts is True.

        data_hstruct: data frame of hospitals, containing the hospital_type, 
            for availability reference.

        h_type_map: map to use for recording scores of hospital types.

        return_group_counts=False: whether to return the raw proportions 
            (before availability adjustment) in addition to adjusted score.

    returns: fraction for each hospital type, scaled to the availability of 
        that type, and normalized so all sum to 1.
    notes: Called by Run_subset_and_score.

2.6 GeneralFunctions
    GeneralFunctions contains helper functions that are used for basic or 
        common tasks throughout the other files.

export_data_to_file:
    inputs:
        data: data to turn into a file.

        filename: name of file to be created.

        path: where file name will be created.

        ftype="xlsx": format of file to create (default xlsx), can also choose 
            "csv".

        overwrite=False: Whether to overwrite any existing files of the same 
            name. If False, it will append a version and counter to the name.

    returns: nothing
    notes: saves data to a file in path with name filename, and type ftype. If 
        the file exists, it can overwrite or append a version number.

files_to_dict:
    inputs:
        paths: paths to files that you want to load

        header_number=7: number at which to start taking data from the data 
            sheet. 7 is the typical value in the original raw files. Overwrite 
            as desired.

    returns: dictionary of data frames. One key for every sheet in the provided
    files, with checker to ensure no repeated key names
    notes: 

file_to_df:
    inputs:
        file_name: path and name from working directory to file to import

        sheetname=None: which sheet from the excel doc to import, leave as None
            to get all.

        header_number=0: how many lines down is the list of names. Beware 
            0-indexing.

        separator=",": symbol to use for separating csv cells. Common 
            alternative on European systems is ";".

    returns: A data frame containing the data in filename (which should include
         the path).
    notes:

find:
    inputs:
        ls: list or other iterable to find values in

        key=None: boolean function to check a condition. None will default to 
            finding values equal to val.

        val=None: value or list of values to compare with elements of ls using 
            key.

        *args: other needed arguments required for key.

        return_vals: whether to also return values at found indices.

    returns: list of indices where the given values were found. Optionally also
        returns the values at those indices.
    notes:

equal:
    inputs:
        x: number, string, list, other variable

        y: another variable of the same type as x

    returns: True if x==y, False if not
    notes: 


check_for_saved:
    inputs:
        path_name: path and name of file to check for, as a single string

    returns: the file as a data frame if present, otherwise returns false
    notes:

2.7 Descriptives
Contains only one function, to help in creating plots. If you want to add more
methods for describing your data before scoring and analysis, recommend putting
those methods here.

histogram:
    inputs:
        data: data with variables that you want histograms of.

        vars_to_plot=None: variables in data to plot. If left as None, all are
            plotted.

        nbins=10: number of bins for each histogram. 

    returns: Nothing
    notes: Produces a histogram separately for each variable. For more advanced
        plotting methods, use matplotlib.pyplot module.

2.8    DummyDataGenerator
A script to generate data that roughly takes the form of the raw patint and 
hospital data, not meaningful for analysis. Draws hospital IDs and plzs from 
TravelTime module.

*******************************************************************************
3. Source Data Files
3.1 treatment area
There are a collection of files containing the raw data for each treatment area
 in the path "project_root/Patient Choice/03 Patient & Hospital features". The 
two sheets of concern to this algorithm are "KH" and "Pat". 

"Pat" must contain columns for "versid", "plz", "ik_site_number","year", 
"treatment_area", and columns for all variables you want to investigate. By 
default, these are "Ruralness_ktyp", "Gender", "Age", and "Severity". 

"KH" must include columns for at least one of "ik_site_number_year" and 
"ik_site_number", and include "treatment_area", and "year", and columns for all
 variables you want to investigate. By default, these are 
"university_hospital", "case_volume", "number_beds_total","hospital_type",
"treatment_area", "dedicated_dept", and "QI". 

Adding new variables to investigate in either of these may require adding code 
to deal with special behaviors, cases, or preferences.




3.2 travel time

Travel time data files contain information about the travel time between a plz 
code and a hospital location. The raw files are found in 
"project_root/Patient Choice/03 Patient & Hospital features/RAW". These are 
structured in three columns: plz, hospital, and travel time, where each pair of
 plz and hospital has a unique travel time.

Some restructured but complete files are found in 
"project_root/Patient Choice/Intermediate_Files". These are structured so that 
each row corresponds to a single patient, each column to a hospital, and the 
value at the combination is the travel time. This structure drastically 
improves lookup time.

Technically, the travel time files in "Intermediate_Files" can be recreated 
from the raw files, but it is time consuming to do so, so it is suggested to 
make sure that they are left alone. Some subset files are also created for 
specific treatment areas to speed computation time.



*******************************************************************************
4. Intermediate Files
Intermediate files are files generated by the algorithm that can be imported 
and used to speed up future analyses. They are often overwritten, and deleting 
any of them will not cause problems with the algorithm's function.

4.1 imported
Imported files are saved versions of the first step of extracted data. They are
 created by the extract_patient_attr_data and extract_hospital_struct_data 
functions. They contain only information that is in the source files, and only 
variables for analysis and cross referencing. See the section on Source Data 
Files for a list of these variables. There is a separate file each for patients
 and hospitals, and it is also by treatment area.

4.2 categorized
Categorized data files contain information structured the same as imported 
data, with all the same columns, and the same rows. The difference is that the 
analysis variables have been categorized. There is a separate file each for 
patients and hospitals, calculated by categorize_patient_vars and 
categorize_hospital_vars respectively. There are also separate files for each 
treatment area.

Categorizing is calculated differently depending on the type of data (which is 
checked automatically).
    For strings (words), each unique string is given its own category. 

    For numbers, it first checks how many unique numbers there are, and 
    compares that to the number of desired quantiles (5 by default). If 
    there are not at least twice as many unique numbers as desired 
    quantiles, it leaves them unchanged, as their own category. Otherwise, 
    it assigns a value based on the quantile that it is in.

    For age (special case), it takes a provided list of values, and assigns
     a category number based on which pair of values the age falls between.

4.3 numerical
Numerical data files contain all the same information as the imported data 
files, except that any string variables to be analyzed have been turned into
numerical values, to enable analysis and scoring. If provided, the variable 
str_maps will be used to translate. If not, a map will be created and can be
optionally returned for later reference.

4.4 grouped
Group data files consist simply of an ID (versid or ik_site_number) and a 
string defining the group. The groups are created by the group_patients and 
group_hospitals functions, and strings are created based on the categories of 
the analysis variables

4.5 choice
File containing all patient data, and the characteristics (linking and 
analysis) of their hospital choice, and all linking and analysis data of the 
patient, in addition to hospital and patient group names. Rows correspond to 
patients, columns are variables describing those patients and the 
characteristics of their choice of hospital.

4.6 travel time table
The Travel time table data file is constructed from the raw 3 column travel 
time, such that each column is an individual hospital, each index is a plz 
code, and the cell value at the intersection is the travel time from the 
centroid of the plz to the hospital.

It is faster to create this table from the raw files and then use it in scoring
 than to try and use the raw files directly. Faster still if this file already 
exists for lookup.

4.7 travel time subset table
This is a reduced version of the travel time table, for a given treatment area.
It contains indices only for patients that have a treatment in that treatment
area, and columns for hospitals that treateda patient in that treatment area.

