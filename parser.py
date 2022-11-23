import pandas as pd
import numpy as np
from constants import *

complexizeArray = np.vectorize(complex)

# https://pythonbasics.org/read-excel/
def parseLineData(printEnabled: bool)->None:
    myDf = pd.read_excel('.\\input\\lineIn.xlsx')
    if printEnabled:
        print(myDf.columns)
    myDf["impedance"] = complexizeArray(myDf["r_ohm_"], myDf["x_ohm_"])
    myDf.rename(columns={'from': 'fromNode', 'to': 'toNode'}, inplace=True)
    if printEnabled:
        print(myDf)
    myDf.drop(['r_ohm_','x_ohm_'] , axis=1, inplace=True)
    if not INPUT_IS_PU:
        myDf.impedance = myDf.impedance.apply(lambda r : r/Z_base) # p.u.
    myDf.to_csv(".\\temp\\lineData.csv", index_label="idx")
    print("Line data converted successfully! ")

def parseBusData(printEnabled: bool)->None:
    myDf = pd.read_excel('.\\input\\busIn.xlsx')
    if printEnabled:
        print(myDf.columns)
    myDf["S"] = complexizeArray(myDf["kW"], myDf["kVAR"])
    myDf.rename(columns={'at': 'atNode'}, inplace=True)
    myDf = myDf.reindex(columns=['name', 'atNode', 'kW', 'kVAR', 'S'])
    if printEnabled:
        print(myDf)
    myDf.drop(['kW','kVAR'] , axis=1, inplace=True)
    if not INPUT_IS_PU:
        myDf.S = myDf.S.apply(lambda s : s/S_base/1000) # p.u. /1000 to convert kVA to MVA
    myDf.to_csv(".\\temp\\busData.csv", index_label="idx")
    print("Line data converted successfully! ")

if __name__ == "__main__":
    parseLineData(printEnabled=True)
    parseBusData(printEnabled=True)