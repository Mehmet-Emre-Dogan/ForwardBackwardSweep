import numpy as np
import pandas as pd
from constants import *
from functions import *

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
        lineData["currents_polar_pu_"] = getPolarArr(iLineArr)
        busData["voltages_polar_pu_"] = getPolarArr(vArr)
        lineData.to_csv(".\\output\\lineData.csv", index_label="idx")
        busData.to_csv(".\\output\\busData.csv", index_label="idx")

def fetchOutputData()->dict:
    lineData = pd.read_csv('.\\output\\lineData.csv', sep=',', header=0)
    busData = pd.read_csv('.\\output\\busData.csv', sep=',', header=0)
    return {"ld":lineData, "bd":busData}

def fetchVI()->tuple:
    data = fetchOutputData()
    vArr = complexizeArr(data["bd"].voltages_pu_)
    cArr = complexizeArr(data["ld"].currents_pu_)
    return (vArr, cArr)

def fetchImpedances()->np.array:
    data = fetchOutputData()
    return complexizeArr(data["ld"].impedance)

def fetchPowers()->np.array:
    data = fetchOutputData()
    return complexizeArr(data["bd"].S)

def printSweep()->None:
    data = fetchOutputData()
    data["ld"].drop(['impedance', 'currents_pu_', 'idx', 'idx.1'] , axis=1, inplace=True)
    data["bd"].drop(['S', 'voltages_pu_', 'idx', 'idx.1'] , axis=1, inplace=True)
    print(data["ld"])
    print(data["bd"])

def plotSweep()->None:
    data = fetchOutputData()
    # plot voltage data
    vArr, cArr = fetchVI()
    plot(data["bd"].atNode, "Bus Number", abs(vArr), "v (p.u.)",\
         getAngleArr(vArr), "∠°", ['magnitude', 'angle'], "Bus Voltages Plot", \
             ".\\output\\busVolt_pu.png" )
    # plot current data
    plot(data["ld"].idx + 1, "Line Number", abs(cArr), "i (p.u.)",\
         getAngleArr(cArr), "∠°", ['magnitude', 'angle'], "Line Currents Plot", \
             ".\\output\\LineCurr_pu.png" )

def printDiagnostics()->None:
    impedances = fetchImpedances()
    powers = fetchPowers()
    vArr, iLineArr = fetchVI()
    print("#"*70)
    sIn = getPolar(vArr[0]*np.conj(iLineArr[0])*S_base*1e3)
    ploss = np.real(np.sum(getPowerArr(iLineArr, impedances)))
    sOut= getPolar((np.sum(powers) + np.sum(getPowerArr(iLineArr, impedances)) )*S_base*1e3)
    print(f"Line losses: {ploss*S_base*1e3} kW")
    print(f"#S_in = {sIn} kVA  #S_out = {sOut} kVA")
    print("#"*70)

if __name__ == "__main__":
    performSweep()