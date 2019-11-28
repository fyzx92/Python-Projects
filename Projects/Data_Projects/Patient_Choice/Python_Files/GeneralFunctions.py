# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 15:14:21 2019

@author: Bryce_user
"""

import os
import pandas as pd
import numpy as np

import csv
import json


def export_data_to_file(data, filename, path, ftype="xlsx", overwrite=False):
    """
    data: data to turn into a file
    filename: name of file to be created
    path: where file name will be created
    ftype: format of file to create (default xlsx)
    overwrite: overwrite, or no?
    """
    
    # option to skip if desired
    if not path: return
    
    # check path validity
    tmp = os.getcwd()
    os.chdir(path)

    
    if filename:
        # write patient data with unique name
        if not overwrite:
            i = 1
            while os.path.isfile(filename + f"_v{i}.{ftype}"): i += 1
            filename += f"_v{i}"
        filename += f".{ftype}"

        if ftype == "xlsx":
            data.to_excel(filename, header=data.columns, index_label="index")
            
        elif ftype == "csv" and isinstance(data, pd.DataFrame):
            data.to_csv(filename, header=data.columns, index_label="index")
            
        elif ftype == "csv":
            w = csv.writer(open(filename, "w"))
            for key, val in data.items():
                w.writerow([key, val])
                
        elif ftype == "json":
            j = json.dumps(data)
            with open(filename,"w") as f:
                f.write(j)
            
        elif ftype == "txt":
            with open(filename, "w") as f:
                f.write( str(data) )
            
    os.chdir(tmp)           
        
        
        

def files_to_dict(paths, header_number = 7):
    """
    paths: paths to files that you want to load
    header_number: number at which to start taking data from the data sheet
    
    Returns a dictionary of data frames. One key for every sheet in the provided
    files, with checker to ensure no repeated key names
    """    
    
    # Import raw data file
    dfs = {}
    for p in paths:
        print(f"loading {p} to dictionary")
        f = file_to_df(p, header_number = header_number)
        
        i=0
        # f will be a dict if it comes from excel w/ multiple sheets
        if isinstance(f, dict):
            f_new_keys = list(f.keys())
            f_keys = list(f.keys())
            dfkeys = list(dfs.keys())
            
            print(f"checking that keys are unique")
            # check if default keys are unique, append digit if not
            for j in range(len(f_keys)):
            #for j,fk in enumerate(f_keys)
                #if fk in dfkeys:
                if f_keys[j] in dfkeys:
                    for k in f_keys: 
                        f_new_keys[j] = k + f"_{i}"
                    i += 1
            f_new = dict(zip(f_new_keys, f.values()))
            dfs.update(f_new)
            
        # if f has only one sheet, f will be a data frame
        else:
            print(f"checking that keys are unique")
            dfkeys = list(dfs.keys())
            k = f"key_{i}"
            while k in dfkeys: 
                k = f"key_{i}"
                i += 1

            dfs[k] = f
    return dfs


def file_to_df(file_name,
               sheetname = None,
               header_number = 0,
               separator = ","
               ):
    """
    file_name: path and name from working directory to file to import
    sheetname: which file from the excel doc you want to import, leave none for all
    header_number: how many lines down is the list of names. Beware 0-indexing
    separator: symbol to use for separating csv cells
    
    Returns a data frame containing the data in filename (which should include the path)
    """
    
    # Check that path exists
    if not os.path.isfile(file_name):
        raise FileNotFoundError("error: path or file does not exist")
        

    # pull file data into data frame
    if ".csv" in file_name[-4:]:
        file = pd.read_csv(file_name, sep = separator)
    elif ".xlsx" in file_name[-5:]:
        file = pd.read_excel(file_name, sheet_name=sheetname, header=header_number)

    # remove empty rows and columns
    if isinstance(file, dict):
        for key in file.keys():
            while all(pd.isnull(file[key].iloc[:,0])): file[key] = file[key].iloc[:,1:]
            while all(pd.isnull(file[key].iloc[0,:])): file[key] = file[key].iloc[1:,:]
    elif isinstance(file, pd.DataFrame):
            while all(pd.isnull(file.iloc[:,0])): file = file.iloc[:,1:]
            while all(pd.isnull(file.iloc[0,:])): file = file.iloc[1:,:]
            
    return file


def find(ls, val=None, key=None, *args, return_vals=False):
    """
    ls: list or other iterable to query
    key: a function to use for searching the list
        pd.isnull() for missing values
        pd.notnull() for nonmissing values
        isinstance(), type   for finding a type
        lambda x: x == val or GF.equal, val     for comparisons
        can also negate these
    val: value used for searching the list (depends on function)
    args: list of arguments that might be used for an arbitrary key
    return_vals: whether to return the values at the found indices
        
    Returns: a list of numerical indices, corresponding to the values that fit the key
    """
    
    if not key: key = equal

    ls = list(ls)
    
    try:
        list(val)
        if isinstance(val, str): val = [val]
    except TypeError:
        val = [val]
    
    idx_list = []
    val_list = []
    
    # if a value was passed
    if val:
        for i,j in enumerate(ls):
            for v in val:
                if key(j, v, *args):
                    idx_list.append(i)
                    val_list.append(j)
    
    # if a value was not passed
    else:
        for i,j in enumerate(ls):
            if key(j, *args):
                idx_list.append(i)
                val_list.append(j)
            
    if return_vals:
        return idx_list, val_list
    return idx_list
        
    
def equal(x,y):
    return x==y

def check_for_saved(path_name):
    """
    path_name: path and name of file to check for, as a single string
    
    returns the file as a data frame if present, otherwise returns false
    """

    if os.path.isfile(path_name):
        print(f"loading from file {path_name}")
        try:
            saved_file = file_to_df(path_name)
            saved_file.index = saved_file["Unnamed: 0"]
            saved_file.drop(columns="Unnamed: 0", inplace=True)
            
        except KeyError:
            try:
                saved_file = file_to_df(path_name)
                saved_file.index = saved_file["index"]
                saved_file.drop(columns="index", inplace=True)
            except KeyError:
                saved_file = file_to_df(path_name)
        return saved_file
    
    else: return False
