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