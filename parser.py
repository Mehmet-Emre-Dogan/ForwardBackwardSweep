import pandas as pd
import numpy as np

complexizeArray = np.vectorize(complex)

# https://pythonbasics.org/read-excel/
myDf = pd.read_excel('lineIn.xlsx')
print(myDf.columns)
myDf["impedance"] = complexizeArray(myDf["r_ohm_"], myDf["x_ohm_"])
myDf.rename(columns={'fr.': 'fromNode', 'to': 'toNode'}, inplace=True)
print(myDf)
myDf.drop(['r_ohm_','x_ohm_'] , axis=1, inplace=True)
myDf.to_csv("lineData.csv", index_label="idx")
print("Line data converted successfully! ")

myDf = pd.read_excel('busIn.xlsx')
print(myDf.columns)
myDf["S"] = complexizeArray(myDf["kW"], myDf["kVAR"])
myDf["atNode"] = myDf.index + 1
myDf = myDf.reindex(columns=['atNode', 'kW', 'kVAR', 'S'])
print(myDf)
myDf.drop(['kW','kVAR'] , axis=1, inplace=True)
myDf.to_csv("busData.csv", index_label="idx")
print("Line data converted successfully! ")

    # for idx, line in enumerate(fptr.readlines()):
    #     lineArr = list(line.strip().split())
    #     lineArr.pop(-1)
    #     impedance = complex(lineArr[1].replace("j", "") + "j") # put j at the end, python is unhappy with j in middle
    #     nodes = lineArr[0].split("-")
    #     nodes = [int(node) for node in nodes] # convert to integer all items

    #     outdata.append(f"{idx}, {nodes[0]}, {nodes[1]}, {impedance.real}, {impedance.imag}\n")