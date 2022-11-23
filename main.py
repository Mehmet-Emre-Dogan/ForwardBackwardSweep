   # startTime = timeit.default_timer()
# print("Fetching data...")
   
   stopTime = timeit.default_timer()
    print(f"-> Data fetched successfully in {stopTime-startTime} seconds.")


    # stopTime = timeit.default_timer()

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

# print(f"-> Calculation done in {stopTime-startTime} seconds.")

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