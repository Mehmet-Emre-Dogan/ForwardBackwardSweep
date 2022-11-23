import numpy as np
import pandas as pd
import cmath, math
import matplotlib.pyplot as plt

# https://medogan.com/blogs/2022/06/06/transmission_line_analysis/transmission_line_sending_edge_vi.html
# https://stackoverflow.com/questions/6913532/display-a-decimal-in-scientific-notation
def getPolar(var):
    PRECISION = 5
    USE_DEGREES = True
    magnitude = abs(var)
    angle = cmath.phase(var)

    if (abs(magnitude) < 0.1 or abs(magnitude) > 1e3): # display in exponential form
        magnitude = '{num:.{prec}e}'.format(num=magnitude, prec=PRECISION)
    else:
        magnitude = round(magnitude, PRECISION)

    if USE_DEGREES:
        return f"{magnitude}∠{round(np.degrees(angle), PRECISION)}°"
    else:
        return f"{magnitude}∠{round(angle, PRECISION)} rad"

def getComplex(string: str) -> complex: 
    useDegrees = None
    # parse input string
    splitted = string.split()
    lenSplitted = len(splitted)
    if (lenSplitted == 1) and (string[-1] == "°" ):
        useDegrees = True
    elif (lenSplitted == 2) and (splitted[-1] == "rad"):
        useDegrees = False
    else:
        raise Exception("Incompatible string input!")

    compStr = splitted[0].replace("°", "").split("∠")
    magnitude = float(compStr[0]); angle = float(compStr[1])

    if useDegrees:
        angle = np.deg2rad(angle)
    
    return complex(real=magnitude*np.cos(angle), imag=magnitude*np.sin(angle))

def getPower(current:complex, impedance:complex)->complex:
    return np.abs(current)**2 * impedance

getPolarArr = np.vectorize(getPolar)
getPowerArr = np.vectorize(getPower)

def plot(xData:np.array, xLabel:str, yData1:np.array, yLabel1:str, yData2:np.array, yLabel2:str, title="plotName", savePath=".\\output\\fig.png" )->None:
    fig, ax = plt.subplots()
    ax.minorticks_on()
    ax2 = ax.twinx()
    # set x-axis label
    ax.set_xlabel(xLabel, fontsize = 14)
    # set y-axis label
    ax.set_ylabel(yLabel1, fontsize=14)
    ax2.set_ylabel(yLabel2, fontsize=14)

    ax.plot(xData)
    ax2.plot(yData2, color="orange")

    ax.grid(color='green',  which='major', linestyle = '--', linewidth = 1)
    ax.grid(color='black',  which='minor', linestyle = '--', linewidth = 0.5)
    ax.set_title(title)
    plt.savefig(savePath)

# If the file is run standalone, perform DEBUG
if __name__ == "__main__":
    print(getPolar(4 - 4j))
    print(getComplex("5∠37°"))
    print(getComplex("10∠0.785 rad"))
