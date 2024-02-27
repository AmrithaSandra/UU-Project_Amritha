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
    
        
# Print the data matrix
#print(data_matrix)
data_matrix_shape =data_matrix.shape
#print(data_matrix_shape)

xdata = data_matrix[:,0]/3600
ydata = data_matrix[:,1]

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
T = 308        # Temperature in Kelvin
Pressure = 1.214 
Totalfraction = gases.sum(axis = 1)
Molefractions = gases.div(Totalfraction, axis= 0)

Partial_pressure = np.multiply(Pressure,Molefractions)/1000
number_of_moles = Partial_pressure * V / (R * T)


plt.plot(Time, number_of_moles)
plt.xlabel('Time(hr)')
plt.ylabel('Gases(no. of moles)')
plt.title(' Gas evolution Curve')
plt.savefig('Gasevolution_curve.png')