from cmath import pi
import numpy as np
import pandas as pd
from constants import *
from functions import *

# https://stackoverflow.com/questions/3518778/how-do-i-read-csv-data-into-a-record-array-in-numpy
lineData = pd.read_csv('lineData.csv', sep=',', header=0); lineData = lineData.apply(pd.to_numeric, errors='coerce')
busData = pd.read_csv('busData.csv', sep=',', header=0); busData = busData.replace("?", np.nan)
busData = busData.apply(pd.to_numeric, errors='coerce')

# lineData.loc[:, "resistance"].apply(lambda r : r/Z_base)
# print(lineData[["resistance", "reactance"]])
print(lineData)
print(busData)
lineData[["resistance", "reactance"]] = lineData[["resistance", "reactance"]].apply(lambda r : r/Z_base)
busData[["voltage"]] = busData[["voltage"]].applymap(lambda v : v/V_base, na_action="ignore")
busData[["P_loads", "Q_loads", "P_gens", "Q_gens"]] = busData[["P_loads", "Q_loads", "P_gens", "Q_gens"]].applymap(lambda s : s/S_base, na_action="ignore")
print(lineData)
print(busData)

zArr = lineData.resistance + 1j*lineData.reactance
print(zArr)
sArr = busData.P_loads - busData.P_gens + 1j*(busData.Q_loads - busData.Q_gens)
print(sArr)
print(np.isnan(sArr))

length = np.max([np.max(lineData.fromNode), np.max(lineData.toNode)])
print(f"{length=}")

vArr = np.ones(length)
iLineArr = np.zeros(length)


iLoadArr = np.conj(np.divide(sArr, vArr))
print(iLoadArr)
for i in range(NUMBER_OF_ITERS):
    print(i)
    for j in range(len(lineData)-1, -1, -1):
        # print(j)
        hub = np.where(lineData.iloc[:, 0:1] == lineData.iloc[j, 1])
        if np.size(hub) == 1: # start or endpoint
            iLineArr[lineData.iloc[j, 0]-1] = iLoadArr[lineData.iloc[j, 2]-1] + np.sum(iLineArr[lineData.iloc[hub, 0]-1]) - iLineArr[lineData.iloc[j, 0]-1]

    for j in range(len(lineData)):
        vArr[lineData.iloc[j, 2]-1] = vArr[lineData.iloc[j, 1]-1] - iLineArr[lineData.iloc[j, 0]-1]*zArr[j]    
print (iLineArr)
