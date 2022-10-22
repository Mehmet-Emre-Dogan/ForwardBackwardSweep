MAX_NUMBER_OF_ITERS = 2000
MAX_ERROR = 0.001
S_BASE_MVA = 100 # MVA
V_BASE_KV = 54 # kV

################ DO NOT EDIT BELOW THE LINE ################
S_base = S_BASE_MVA#*1e6
V_base = V_BASE_KV#*1e3
Z_base = (V_base**2)/S_base
I_base = S_base/V_base#*1e3