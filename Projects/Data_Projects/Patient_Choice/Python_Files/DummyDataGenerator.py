# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 11:25:39 2019

@author: bryce
"""

import os
#os.chdir('/home/bryce/Shared/TUB_thesis/Patient Choice/Python_Files')
os.chdir('C:/Users/bryce/Documents/TUB_thesis/Patient Choice/Python_Files')
import sys
sys.path.insert(0, './')

import pandas as pd
import random
import string

import TravelTime as TT
import GeneralFunctions as GF




n_patients = 10000
n_hospitals = 100



def randomString(stringLength=10, letters=True, numbers=False):
    """Generate a random string of fixed length """
    if letters:
        chars = string.ascii_lowercase
    if numbers:
        chars += string.digits
    return ''.join(random.choice(chars) for i in range(stringLength))


    
def patient_group(p_d):
    groupnames = []
    for i,j in enumerate(p_d["versid"]): 
        r = p_d['Ruralness_ktyp'][i]
        g = p_d['Gender'][i]
        s = p_d['Severity'][i]
        a = random.choice([1,2,3,4,5])
        t = random.choice([1,2,3])
        groupnames += [f"patient_group_r{r}_g{g}_s{s}_a{a}_t{t}"]
    p_d["Patient_Group"] = groupnames

def hospital_group(h_d):
    groupnames = []
    for i,j in enumerate(h_d["ik_site_number"]):
        q = random.choice([1,2,3,4,5])
        v = random.choice([1,2,3,4,5])
        d = h_d['dedicated_dept'][i]
        groupnames += [f"hospital_group_q{q}_v{v}_d{d}"]
    h_d["Hospital_Group"] = groupnames


# check if dummy data exists for travel time
dummy_TT_file_exists = True
travel_time_all_TA = GF.check_for_saved("../Intermediate_Files/tt_plz_full_lookup_table_dummy.csv")

# set up dummy data for travel times if it doesn't already exist
if not isinstance(travel_time_all_TA, pd.DataFrame):
    print("no dummy travel time data found")
    travel_time_all_TA = GF.check_for_saved("../Intermediate_Files/tt_plz_full_lookup_table.csv")
    dummy_TT_file_exists = False
       
    if not isinstance(travel_time_all_TA, pd.DataFrame):
        print("no reference travel time structure found")
        # create arbitrary data set
        plzs = []
        for p in range(1000):
            plzs.append(randomString(letters=False, numbers=True))

        hospitals = []
        for h in range(200):
            hospitals.append(randomString(numbers=True))

        travel_time_all_TA = pd.DataFrame(index = plzs, columns=hospitals)
    
    print("randomizing travel time values")
    for i,h in enumerate(travel_time_all_TA.columns):
        for p in travel_time_all_TA.index:
            travel_time_all_TA.loc[p,h] = random.randint(10, 1000)
            
        print(f"{i} of {len(travel_time_all_TA.columns)} hospitals complete")


# save dummy travel time data if it doesn't already exist
if not dummy_TT_file_exists:
    travel_time_all_TA.to_csv("../Intermediate_Files/tt_plz_full_lookup_table_dummy.csv")

# select hospital names for hospital df
ik_site_numbers = [random.choice(travel_time_all_TA.columns) for i in range(n_hospitals)]

# labels, columns some data for patients
patient_data = {
    "treatment_area": "Dummy",
    "versid": [],
    "ik_site_number": [],
    "year": [],
    "plz": [],
    "Age": [],
    "Gender": [],
    "Ruralness_ktyp": [],
    "Severity": []
}
for i in range(n_patients):
    patient_data["versid"] += [randomString()]
    patient_data["ik_site_number"] += [random.choice(ik_site_numbers)]
    patient_data["year"] += [2015]
    patient_data["plz"] += [random.choice(travel_time_all_TA.index)]
    patient_data["Age"] += [random.randint(15,100)]
    patient_data["Gender"] += [random.choice([1,2])]
    patient_data["Ruralness_ktyp"] += [random.choice([1,2,3,4])]
    patient_data["Severity"] += [1]
    
patient_group(patient_data)




# labels, columns some data for hospitals
hospital_data = {
    "treatment_area": "",
    "dedicated_dept": [],
    "QI": [],
    "year": [],
    "university_hospital": [],
    "case_volume": [],
    "number_beds_total": [],
    "hospital_type": [],
    "ik_site_number": None
}

for i in range(n_hospitals):
    patient_data["treatment_area"] += [randomString()]
    patient_data["dedicated_dept"] += [random.choice([0,1])]
    patient_data["year"] += [2015]
    patient_data["QI"] += [random.random()*10]
    patient_data["university_hospital"] += [random.choice([0,1])]
    patient_data["case_volume"] += [random.randint(5,100)]
    patient_data["number_beds_total"] += [random.randint(5,100)]
    patient_data["hospital_type"] += [random.choice(["private", "clinic", "public"])]

patient_data["ik_site_number"]  = ik_site_numbers
hospital_group(hospital_data)



# dictionaries to data frames
df_h = pd.DataFrame.from_dict(hospital_data)
df_h.index = hospital_data["ik_site_number"]

df_p = pd.DataFrame(patient_data)
df_p.index = patient_data["versid"]



# save hospital and patient data to same file
with pd.ExcelWriter("../03 Patient & Hospital features/dummy_data.xlsx") as writer:
    df_h.to_excel(writer, sheet_name = "KH", index_label="index", startrow=7)
    df_p.to_excel(writer, sheet_name = "Pat", index_label="index", startrow=7)



    
