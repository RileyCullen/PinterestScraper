# Cullen, Riley 
# CSVHelper.py
# Created on 5/30/20

import os, glob
import pandas as pd

def CreateMasterCSV(root, filename):
    rootContents = __GetSubDirectories(root)
    dataList = []
    for dir in rootContents:
        data = pd.read_csv(glob.glob(os.path.join(dir, "*.csv"))[0])
        dataList.append(data)
    
    if (DoesCSVExist(root, filename)):
        RemoveCSV(root, filename)

    masterCSV = pd.concat(dataList, axis=0, ignore_index=True)
    masterCSV.to_csv(root + "/" + filename, index=True)
    

def __GetSubDirectories(root):
    rootContents = os.listdir(root + "/.")
    results = []
    for elem in rootContents:
        elem = root + '/' + elem
        if (os.path.isdir(os.path.join(os.path.abspath("."), elem))):
            results.append(elem)  
    return results

def DoesCSVExist(root, filename):
    if (os.path.isfile(root + "/" + filename)):
        return True
    return False

def RemoveCSV(root, filename):
    os.remove(root + "/" + filename)
