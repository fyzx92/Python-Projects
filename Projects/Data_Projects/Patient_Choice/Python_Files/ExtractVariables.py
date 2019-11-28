# Authored by Bryce Burgess 18/2/2019
# create data structure with all desired variables and raw data

import pandas as pd


import os
#os.chdir('/home/bryce/Shared/TUB_thesis/Patient Choice/Python_Files')
os.chdir('C:/Users/bryce/Documents/TUB_thesis/Patient Choice/Python_Files')
import sys
sys.path.insert(0, './')

import GeneralFunctions as GF


###############################################################################
def extract_patient_attr_data(patient_factors, 
                             treatment_area,
                             paths,
                             export_path="../Intermediate_Files/",
                             from_scratch=False,
                             dropna = False
                             ):
    """
    patient_factors: factors to extract for the patient data
    treatment_area: string for naming the save file
    paths: where to pull data from
    export_path: Path to export saved data to. Blank does not export
    from_scratch=False: calculate from raw data (True), or load from existing file (False)
    dropna=False: (True) drop rows that have missing values
    
    Looks in every file in paths, and extracts patient factors, into patient table
    Returns table
    """
    
    
    # see if data is already saved
    file_name = f"{treatment_area}_imported_patient_attributes_data"
    file_ext = "csv"
    file_path = "../Intermediate_Files/"
    if not from_scratch:
        file = GF.check_for_saved(file_path + file_name + "." + file_ext)
        if isinstance(file, pd.DataFrame): 
            file.index = file["versid"]
            return file
    
    # variables for keeping track of entries, subsetting
    patient_ident_factors = ["plz", "year", "versid", "treatment_area", "ik_site_number"]
    
    # Import raw data file
    dfs = GF.files_to_dict(paths, header_number=7)
    
    # assign data to patient data frame
    print("\n\nloading patient data")
    patient_data = assign_bulk_data(dfs["Pat"], patient_factors + patient_ident_factors)
    
    # assign meaningful index values
    patient_data.index = patient_data["versid"]
    
    # ensure unique indices
    patient_data=patient_data.sort_index()
    indices = list(patient_data.index)
    for i, name in enumerate(patient_data.index):
        x = 1
        while i+x < len(patient_data.index):
            # check for duplicate indices
            if patient_data.index[i] == patient_data.index[i+x]:
                # if data is redundant, mark index for deletion
                if all(k == l for k, l in zip(patient_data.iloc[i], patient_data.iloc[i+x])):
                    indices[i+x] = ""
                    
                # if data is not redundant, append a modifying tag
                else: 
                    indices[i+x] = name + f"_{x}"

            else: break
            x += 1
    patient_data.index = indices
    if "" in patient_data.index:
        patient_data.drop(index="", inplace=True)
    
    # whether or not to drop rows with missing values
    if dropna:
        patient_data.dropna(inplace=True)
    
    GF.export_data_to_file(data = patient_data, filename=file_name, path=export_path, ftype=file_ext, overwrite=True)
    
    return patient_data
###############################################################################




###############################################################################
def extract_hospital_struct_data(hospital_factors,
                                treatment_area,
                                paths,
                                export_path="../Intermediate_Files/",
                                from_scratch=False,
                                dropna = False
                                ):
    """
    hospital_factors: factors to extract for hospital data
    treatment_area: string for naming the save file
    paths: where to pull data from
    export_path: where to export data to a new file (None to not export)
    from_scratch=False: calculate from raw data (True), or load from existing file (False)
    dropna=False: (True) drop rows that have missing values
    
    Looks in every file in paths, and extracts hospital factors, into hospital table
    Returns table
    """    
    

    
    # see if data is already saved
    file_name = f"{treatment_area}_imported_hospital_structural_data"
    file_ext = "csv"
    file_path = "../Intermediate_Files/"
    if not from_scratch:
        file = GF.check_for_saved(file_path + file_name + "." + file_ext)
        if isinstance(file, pd.DataFrame): 
            file.index = file["ik_site_number"]
            return file
    
    # variables for keeping track of entries, subsetting
    hospital_ident_factors = ["ik_site_number_year", "ik_site_number", "treatment_area", "year"]
    
    # Import raw data file
    dfs = GF.files_to_dict(paths, header_number=7)
    
    # assign data to hospital data frame
    print("\n\nloading hospital data")
    hospital_data = assign_bulk_data(dfs["KH"], hospital_factors + hospital_ident_factors)
    
    # change hospital ID to exclude year
    if not "ik_site_number" in hospital_data.columns:
        print("\n\nmaking ID year independent")
        if "ik_site_number_year" in hospital_data.columns:
            hospital_data.rename(inplace = True, columns={"ik_site_number_year": "ik_site_number"})
        
            for i in hospital_data.index:
                h = hospital_data["ik_site_number"][i]
                if h[-4:] in str(set(hospital_data["year"])):
                    hospital_data["ik_site_number"][i] = h[:-5]
    
    
    # assign meaningful index values
    hospital_data.index = hospital_data["ik_site_number"]
    
    # ensure unique indices 
    hospital_data=hospital_data.sort_index()
    indices = list(hospital_data.index)
    for i, name in enumerate(hospital_data.index):
        x = 1
        while i+x < len(hospital_data.index):
            # check for duplicate indices
            if hospital_data.index[i] == hospital_data.index[i+x]:
                # if data is redundant, mark index for deletion
                if all(k == l for k,l in zip(hospital_data.iloc[i], hospital_data.iloc[i+x])):
                    indices[i+x] = ""
                
                # if data is not redundant, append a modifying tag
                else: 
                    indices[i+x] = name + f"_{x}"

            else: break
            x += 1
    hospital_data.index = indices
    if "" in hospital_data.index:
        hospital_data.drop(index="", inplace=True)

    
    # whether or not to drop rows with missing values
    if dropna:
        hospital_data.dropna(inplace=True)
    
    GF.export_data_to_file(data = hospital_data, filename=file_name, path=export_path, ftype=file_ext, overwrite=True)
    
    return hospital_data
###############################################################################




###############################################################################
def assign_bulk_data(data_pull, factors):
    """
    data_pull: source file to import from
    factors: list of variables to look for
    
    Assign data from imported file
    """

    # find matching columns
    cols = [c for c in data_pull.columns if c in factors]

    # set up output structure, and fill
    data_push = pd.DataFrame(columns=cols, index=data_pull.index)
    for c in data_push.columns:
        data_push[c] = data_pull.loc[:,c]
            
            
    return data_push
