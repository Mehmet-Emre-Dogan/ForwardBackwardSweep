###################### EDITABLE LINES ######################
MAX_NUMBER_OF_ITERS = 200
MAX_ERROR = 1e-10

S_BASE_MVA = 100 # MVA
V_BASE_KV = 12.66 # kV
############################################################


################ DO NOT EDIT BELOW THE LINE ################
S_base = S_BASE_MVA#*1e6
V_base = V_BASE_KV#*1e3
Z_base = ((V_base)**2)/(S_base)
# Z_base = ((V_base*1e3)**2)/(S_base*1e6)
# I_base = S_base/V_base/sqrt(3)