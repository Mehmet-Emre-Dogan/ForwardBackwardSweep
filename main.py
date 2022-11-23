import timeit
import numpy as np
import parser
import sweep

mainStartTime = timeit.default_timer()
startTime = timeit.default_timer()
print("Main: Parsing data...")
parser.parseLineData(printEnabled=False)
parser.parseBusData(printEnabled=False)
stopTime = timeit.default_timer()
print(f"-> Main: Data parsed successfully in {stopTime-startTime} seconds.")

startTime = timeit.default_timer()
print("Main: Performing sweep...")
sweep.performSweep()
stopTime = timeit.default_timer()
print(f"-> Main: Sweep performed successfully in {stopTime-startTime} seconds.")

startTime = timeit.default_timer()
print("Main: Printing & plotting results...")
sweep.printSweep()
sweep.plotSweep()
sweep.printDiagnostics()
stopTime = timeit.default_timer()
print(f"-> Main: Printing & plotting completed in {stopTime-startTime} seconds.")

stopTime = timeit.default_timer()
print(f"-> Main: Code completed in {stopTime-mainStartTime} seconds.")