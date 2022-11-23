from json import load
DEBUG = False

with open(".\\input\\config.json", "r", encoding="UTF-8") as fptr:
    jsonData = load(fptr)
    MAX_NUMBER_OF_ITERS = jsonData["MAX_NUMBER_OF_ITERS"]
    MAX_ERROR = jsonData["MAX_ERROR"]

    S_BASE_MVA = jsonData["S_BASE_MVA"] # MVA
    V_BASE_KV = jsonData["V_BASE_KV"] # kV

################ DO NOT EDIT BELOW THE LINE ################
S_base = S_BASE_MVA#*1e6
V_base = V_BASE_KV#*1e3
Z_base = ((V_base)**2)/(S_base)
# I_base = S_base/V_base/sqrt(3)