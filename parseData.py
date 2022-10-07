import math
outdata = []
with open("dataGeneration\\sampleLineData.txt", "r", encoding="UTF-8") as fptr:
    for idx, line in enumerate(fptr.readlines()):
        lineArr = list(line.strip().split())
        lineArr.pop(-1)
        impedance = complex(lineArr[1].replace("j", "") + "j") # put j at the end, python is unhappy with j in middle
        nodes = lineArr[0].split("-")
        nodes = [int(node) for node in nodes] # convert to integer all items

        outdata.append(f"{idx}, {nodes[0]}, {nodes[1]}, {impedance.real}, {impedance.imag}")
[print(line.strip()) for line in outdata]
with open("lineData.csv", "w", encoding="UTF-8") as fptr:
    fptr.writelines(outdata)
    print("--> File write successful!")

# TODO
# outdata = []
# with open("dataGeneration\\sampleBusData.txt", "r", encoding="UTF-8") as fptr:
#     for idx, line in enumerate(fptr.readlines()):
#         lineArr = list(line.strip().split())
#         lineArr.pop(-1)
#         impedance = complex(lineArr[1].replace("j", "") + "j") # put j at the end, python is unhappy with j in middle
#         nodes = lineArr[0].split("-")
#         nodes = [int(node) for node in nodes] # convert to integer all items

#         outdata.append(f"{idx}, {nodes[0]}, {nodes[1]}, {impedance.real}, {impedance.imag}")
# [print(line.strip()) for line in outdata]
# with open("busData.csv", "w", encoding="UTF-8") as fptr:
#     fptr.writelines(outdata)
#     print("--> File write successful!")