import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


directory = "C:/Users/amps/OneDrive - KTH/Dokument/Amps_PhD/2024/Amps90-plated cells/"
filename = "Amps90-"
extension = ".DTA"

data_matrix = np.empty((0, 2), dtype=float)

a = 0

for i in range (1,8):
    
    file_number = i
    file_path = directory + filename + str(file_number) + extension


    # Skip the text rows until row 52 and read the data into a DataFrame
    df = pd.read_csv(file_path, delimiter='\t', skiprows=51, usecols=[2, 3], decimal=',', header=None)

   
    # convert DataFrame to NumPy matrix
    ith_matrix = df.to_numpy()
    
    #print(ith_matrix)
    
    for j in range(0, len(ith_matrix[:,0])):
        ith_matrix[j,0] = str(a + ith_matrix[j,0])
        
        
    data_matrix = np.concatenate((data_matrix, ith_matrix), axis=0)
    
    a = ith_matrix[len(ith_matrix)-1,0]
    
        
data_matrix_shape =data_matrix.shape

xdata = data_matrix[:,0]/3600 #time
ydata = data_matrix[:,1] #voltage

plt.plot(xdata, ydata, label="Voltage-Time curve")
plt.xlabel('Time(hr)')
plt.ylabel('Voltage(V)')
plt.title(' Time-Voltage Curve')
plt.savefig('time-voltage_curve.png')


# Load the data from the CSV file
data = pd.read_csv("C:/Users/amps/OneDrive - KTH/Dokument/Amps_PhD/2024/Amps90-plated cells/Amps-90.csv", dtype=np.float64, skiprows=23, usecols=[0,1,2,3,4,5,6])
gases = pd.read_csv("C:/Users/amps/OneDrive - KTH/Dokument/Amps_PhD/2024/Amps90-plated cells/Amps-90.csv", dtype=np.float64, skiprows=23, usecols=[1,2,3,4,5,6])

#Isolating the time from the data-converting it into hrs and substracting the delay time
Time = data.iloc[:,0]/3600

V = 0.0000125  # Volume in m^3
R = 0.08134    # Gas constant in bar * m^3 / (mol * K)
T = 298     # Temperature in Kelvin
Pressure = 1.210
#Converting it into number of moles
Totalfraction = gases.sum(axis = 1)
Molefractions = gases.div(Totalfraction, axis= 0)
molefractions1 = Molefractions[['Hydrogen', 'Ethylene', 'Carbon dioxide']]
Partial_pressure = np.multiply(Pressure,molefractions1)
number_of_moles = Partial_pressure * V / (R * T)


#plotting these datas together
with plt.rc_context({'axes.edgecolor': 'grey', 'xtick.color': 'grey', 'ytick.color': 'grey', 'figure.facecolor': 'white'}):
    fig, ax = plt.subplots(2)
    ax[0].plot(xdata, ydata, color='blue', alpha=0.5)
    ax[0].set_xlabel('Time (hr)')
    ax[0].set_ylabel('Voltage (V)', color = 'grey')
    ax[0].set_xlim(0,61)
    #ax[1].plot(Time/3600, number_of_moles[['Hydrogen.1','Ethylene.1','Carbon dioxide.1']], alpha=0.7)
    ax[1].plot(Time, number_of_moles['Hydrogen'], label='Hydrogen', color='#ff7fb9', alpha=0.7)
    ax[1].plot(Time, number_of_moles['Ethylene'], label='Ethylene', color='purple', alpha=0.6)
    ax[1].plot(Time, number_of_moles['Carbon dioxide'], label='CO2', color='#17becf', alpha=0.7)
    ax[1].set_ylabel('No. of moles', color = 'grey')
    ax[1].set_xlabel('Time (hr)', color = 'grey')
    ax[1].set_xlim(0,61)
    ax[1].legend(['Hydrogen m/z = 1','Ethylene m/z = 27','Carbon dioxide m/z = 44'], loc = 'upper left', fontsize='xx-small', edgecolor= 'None')
    plt.savefig('Plating.png', dpi=300)

#Case 1: When temperature is at 50 degree celsius, pressure at 1.2 bar
T1 = 323
number_of_moles_50degrees = Partial_pressure * V / (R * T1)

#Case 2 : when pressure is higher, temperature at 25 degree celsius
P1 = 2 #bar
Partial_pressure1 = np.multiply(P1,molefractions1)
number_of_moles_2bars = Partial_pressure1 * V / (R * T)

#Case 3: both temperature and pressure are higher
number_of_moles_2bars_50degrees = Partial_pressure1 * V / (R * T1)

with plt.rc_context({'axes.edgecolor': 'grey', 'xtick.color': 'grey', 'ytick.color': 'grey', 'figure.facecolor': 'white'}):
    plt.figure() 
    plt.plot(Time, number_of_moles_50degrees, color = 'red', label='T = 5O degree, P = 1.2bar' )
    plt.plot(Time, number_of_moles_2bars, color = 'blue', label='T = 25 degree, P = 2bar ')
    plt.plot(Time, number_of_moles_2bars_50degrees, color = 'green', label='T = 50 degree, P = 2bar ')
    plt.xlabel ('Time (hr)')
    plt.ylabel('Number of moles')  
    plt.savefig('P-T effect in number of moles', dpi =300)
    
    #this calculation helps to understand the effect of temperature and pressure in gas evolution. This calculations are based on the Ideal gas equation.
    #number of moles is proportional to the gas pressure and inversly proportional to the temperature.


