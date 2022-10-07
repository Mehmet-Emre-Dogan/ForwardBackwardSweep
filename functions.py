import numpy as np
import pandas as pd
import cmath, math

from sympy import true

# https://medogan.com/blogs/2022/06/06/transmission_line_analysis/transmission_line_sending_edge_vi.html
# https://stackoverflow.com/questions/6913532/display-a-decimal-in-scientific-notation
def getPolar(var):
    PRECISION = 3
    USE_DEGREES = True
    magnitude = abs(var)
    angle = cmath.phase(var)

    if (abs(magnitude) < 0.1 or abs(magnitude) > 1e3): # display in exponential form
        magnitude = '{num:.{prec}e}'.format(num=magnitude, prec=PRECISION)
    else:
        magnitude = round(magnitude, PRECISION)

    if USE_DEGREES:
        return f"{magnitude}∠{round(math.degrees(angle), PRECISION)}°"
    else:
        return f"{magnitude}∠{round(angle, PRECISION)} rad"

# If the file is run standalone, perform DEBUG
if __name__ == "__main__":
    print(getPolar(4 - 4j))
