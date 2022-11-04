import numpy as np
import pandas as pd
from constants import *
from functions import *
import timeit
import matplotlib.pyplot  as plt
DEBUG = False

print("Fetching data...")
startTime = timeit.default_timer()

# https://stackoverflow.com/questions/3518778/how-do-i-read-csv-data-into-a-record-array-in-numpy
lineData = pd.read_csv('lineData.csv', sep=',', header=0)
lineData.impedance = lineData.impedance.apply(lambda x: complex(x)) # ohms
lineData.impedance = lineData.impedance.apply(lambda r : r/Z_base) # p.u.
if DEBUG:
    print("Line Data")
    print(lineData)
busData = pd.read_csv('busData.csv', sep=',', header=0)
busData.S = busData.S.apply(lambda x: complex(x)) # MVA  *1e6
busData.S = busData.S.apply(lambda s : s/S_base/1000) # p.u. /1000 to convert kVA to MVA
if DEBUG:
    print("Bus Data")
    print(busData)

# the voltage at first node is already 1 p.u.
vArr = np.ones(busData.__len__(), dtype=np.complex64) # assume all other values are also 1 p.u.
vArrOld = vArr.copy()
if DEBUG:
    print(f"{vArr=}")

# the load current draw at first node is already 0 p.u.
# assume all other values are also 0 p.u.
iLoadArr = np.zeros(busData.__len__(), dtype=np.complex64) # in p.u  
iLineArr = np.zeros(lineData.__len__(), dtype=np.complex64) # fill it with zeros too

stopTime = timeit.default_timer()
print(f"-> Data fetched successfully in {stopTime-startTime} seconds.")

startTime = timeit.default_timer()
for iter in range(MAX_NUMBER_OF_ITERS):
    print(f"iteration: {iter+1}")

    # BACKWARD
    for idx, (vBus, sBus) in enumerate(zip(vArr, busData.S)):
        iLoadArr[idx] = np.conj(sBus/vBus)
    if DEBUG:
        print(f"{list(iLoadArr)=}")

    for idx, endNode in reversed(list(enumerate(lineData.toNode))):
        if endNode not in set(lineData.fromNode):
            iLineArr[idx] = iLoadArr[idx+1]
        else:
            boolSelector = lineData.fromNode == endNode
            if DEBUG:
                print(endNode)
                print(boolSelector)
                print(iLineArr[boolSelector])
                print(iLoadArr[endNode-1])
            iLineArr[idx] = np.sum(iLineArr[boolSelector]) + iLoadArr[idx+1]
            
    if DEBUG:
        print(f"{list(iLineArr)=}")

    # FORWARD
    for idx, (iLine, z) in enumerate(zip(iLineArr, lineData.impedance)):
        vArr[lineData.toNode[idx]-1] = vArr[lineData.fromNode[idx]-1] - iLine*z

    if np.max(np.abs(np.subtract(vArr, vArrOld))) < MAX_ERROR:
        print(f"--> Error requirement satisfied in {iter+1} iters.")
        break
    vArrOld = np.copy(vArr)
    if DEBUG:
        print(f"{list(vArr)=}")

stopTime = timeit.default_timer()
print(f"-> Calculation done in {stopTime-startTime} seconds.")
print("#"*70)
print("Bus voltages: ")
[print(f"{str(i).zfill(2)}-> {line}") for i, line in enumerate(list(getPolarArr(vArr)))]
print("Line currents: ")
[print(f"{str(i).zfill(2)}-> {line}") for i, line in enumerate(list(iLineArr))]
print("Line currents: ")
[print(f"{str(i).zfill(2)}-> {line}") for i, line in enumerate(list(getPolarArr(iLineArr)))]

print("#"*70)
sIn = getPolar(vArr[0]*np.conj(iLineArr[0])*S_base*1e3)
ploss = np.real(np.sum(getPowerArr(iLineArr, lineData.impedance)))
sOut= getPolar((np.sum(busData.S) + np.sum(getPowerArr(iLineArr, lineData.impedance)) )*S_base*1e3)
print(f"Line losses: {ploss*S_base*1e3} kW")
print(f"#S_in = {sIn} kVA  #S_out = {sOut} kVA")

fig, ax = plt.subplots()
ax.minorticks_on()
ax2 = ax.twinx()
# set x-axis label
ax.set_xlabel("Bus Number", fontsize = 14)
# set y-axis label
ax.set_ylabel("v (p.u.)", fontsize=14)
ax2.set_ylabel("∠°", fontsize=14)

ax.plot(abs(vArr))
ax2.plot([cmath.phase(v) for v in vArr], color="orange")

ax.grid(color='green',  which='major', linestyle = '--', linewidth = 1)
ax.grid(color='black',  which='minor', linestyle = '--', linewidth = 0.5)
ax.set_title('Bus voltages plot')
plt.show()