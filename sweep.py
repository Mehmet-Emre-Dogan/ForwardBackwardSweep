import numpy as np
import pandas as pd
from constants import *
from functions import *
import timeit
import matplotlib.pyplot  as plt

def performSweep():
    # https://stackoverflow.com/questions/3518778/how-do-i-read-csv-data-into-a-record-array-in-numpy
    lineData = pd.read_csv('.\\temp\\lineData.csv', sep=',', header=0)
    lineData.impedance = lineData.impedance.apply(lambda x: complex(x)) # p.u.

    busData = pd.read_csv('.\\temp\\busData.csv', sep=',', header=0)
    busData.S = busData.S.apply(lambda x: complex(x)) # p.u.

    # the voltage at first node is already 1 p.u.
    vArr = np.ones(busData.__len__(), dtype=np.complex64) # assume all other values are also 1 p.u.
    vArrOld = vArr.copy()

    # the load current draw at first node is already 0 p.u.
    # assume all other values are also 0 p.u.
    iLoadArr = np.zeros(busData.__len__(), dtype=np.complex64) # in p.u  
    iLineArr = np.zeros(lineData.__len__(), dtype=np.complex64) # fill it with zeros too

    for iter in range(MAX_NUMBER_OF_ITERS):
        print(f"Sweep: iteration: {iter+1}")

        # BACKWARD
        for idx, (vBus, sBus) in enumerate(zip(vArr, busData.S)):
            iLoadArr[idx] = np.conj(sBus/vBus)

        for idx, endNode in reversed(list(enumerate(lineData.toNode))):
            if endNode not in set(lineData.fromNode):
                iLineArr[idx] = iLoadArr[idx+1]
            else:
                boolSelector = lineData.fromNode == endNode
                iLineArr[idx] = np.sum(iLineArr[boolSelector]) + iLoadArr[idx+1]
                
        # FORWARD
        for idx, (iLine, z) in enumerate(zip(iLineArr, lineData.impedance)):
            vArr[lineData.toNode[idx]-1] = vArr[lineData.fromNode[idx]-1] - iLine*z

        if np.max(np.abs(np.subtract(vArr, vArrOld))) < MAX_ERROR:
            print(f"--> Sweep: Error requirement satisfied in {iter+1} iters.")
            break
        vArrOld = np.copy(vArr)

        lineData["currents_pu_"] = iLineArr
        busData["voltages_pu_"] = vArr
        lineData.to_csv(".\\output\\lineData.csv", index_label="idx")
        busData.to_csv(".\\output\\busData.csv", index_label="idx")

if __name__ == "__main__":
    performSweep()