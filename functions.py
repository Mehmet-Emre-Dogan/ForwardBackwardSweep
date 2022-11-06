import numpy as np
import pandas as pd
import cmath, math

# https://medogan.com/blogs/2022/06/06/transmission_line_analysis/transmission_line_sending_edge_vi.html
# https://stackoverflow.com/questions/6913532/display-a-decimal-in-scientific-notation
def getPolar(var):
    PRECISION = 4
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

# If the file is run standalone, perform DEBUG
if __name__ == "__main__":
    print(getPolar(4 - 4j))
    print(getComplex("5∠37°"))
    print(getComplex("10∠0.785 rad"))
