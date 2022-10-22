from cmath import pi
import numpy as np
import pandas as pd
from constants import *
from functions import *
DEBUG = False

# https://stackoverflow.com/questions/3518778/how-do-i-read-csv-data-into-a-record-array-in-numpy
lineData = pd.read_csv('lineData.csv', sep=',', header=0)
lineData.impedance = lineData.impedance.apply(lambda x: complex(x)) # ohms
lineData.impedance = lineData.impedance.apply(lambda r : r/Z_base) # p.u.
if DEBUG:
    print("Line Data")
    print(lineData)
busData = pd.read_csv('busData.csv', sep=',', header=0)
busData.S = busData.S.apply(lambda x: complex(x)) # MVA
busData.S = busData.S.apply(lambda s : s/S_base) # p.u.
if DEBUG:
    print("Bus Data")
    print(busData)

# the voltage at first node is already 1 p.u.
vArr = np.ones(busData.__len__(), dtype=np.complex64) # assume all other values are also 1 p.u.
if DEBUG:
    print(f"{vArr=}")

# the load current draw at first node is already 0 p.u.
# assume all other values are also 0 p.u.
iLoadArr = np.zeros(busData.__len__(), dtype=np.complex64) # in p.u  
iLineArr = np.zeros(lineData.__len__(), dtype=np.complex64) # fill it with zeros too
zeroArr = np.zeros(lineData.__len__())

for iter in range(NUMBER_OF_ITERS):
    print(f"iteration: {iter+1}")
    if DEBUG:
        print(f"{iLoadArr=}")

    # BACKWARD
    for idx, (vBus, sBus) in enumerate(zip(vArr, busData.S)):
        iLoadArr[idx] = np.conj(sBus/vBus)
    iLoadArr[0] = np.conj(0)
    if DEBUG:
        print(f"{iLoadArr=}")

    # print(list(lineData.fromNode))
    for idx, endNode in reversed(list(enumerate(lineData.toNode))):
        # print(idx, endNode)
        if endNode not in set(lineData.fromNode):
            # print(endNode)
            iLineArr[idx] = iLoadArr[idx+1]
        else:
            iLineArr[idx] = np.sum(np.where(lineData.fromNode == endNode, iLineArr, zeroArr))
    if DEBUG:
        print(f"{iLineArr=}")

    # FORWARD
    # print(len(vArr), len(iLineArr), len(lineData.impedance))
    for idx, (vBus, iLine, z) in enumerate(zip(vArr, iLineArr, lineData.impedance)):
        vArr[idx+1] = vArr[idx] - iLine*z

    if DEBUG:
        print(f"{vArr=}")

print(list(vArr))
print(list(getPolarArr(vArr)))