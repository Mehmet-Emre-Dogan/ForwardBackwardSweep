import numpy as np
import pandas as pd

# https://stackoverflow.com/questions/3518778/how-do-i-read-csv-data-into-a-record-array-in-numpy
lineData = pd.read_csv('lineData.csv', sep=',', header=None)
busData = pd.read_csv('busData.csv', sep=',', header=None)