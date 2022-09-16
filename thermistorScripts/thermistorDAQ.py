import nidaqmx
import numpy as np
import matplotlib.pyplot as plt
import time

# Function to calculate temperature in celsius given output voltage
def tempCalc(voltOut):

    # Steinhart-Hart Equation Coefficients
    a = 0.00058563
    b = 0.000286668
    c = 0.000000163801

    voltIn = 5
    R0 = 10000 # 10k Ohm Resistor used for voltage divider

    # Calculate thermistor resistance
    Rt = (voltOut * R0) / (voltIn - voltOut)

    # Calculate temperature in Kelvin 
    tempK = 1 / (a + (b * np.log(Rt)) + (c * np.log(Rt))**3)

    # Convert from Kelvin to Celsius
    tempC = tempK - 273.15
    
    return tempC

# Function to record temperature data into a text file
def recordFileData(time, temp):
    time = str(time)
    temp = str(temp)

    file.write(time + '\t' + temp + '\n')

# Configure plotting parameters
fig = plt.figure(figsize = (6, 3))
ax = fig.add_subplot(1, 1, 1)

# Initialize the nidaqmx task
task = nidaqmx.Task()
task.ai_channels.add_ai_voltage_chan('Dev1/ai0', min_val = 0, max_val = 5)
task.start()

# Open file for data recording
file = open('tempData.txt', 'w')

# Assign start time and time interval for recording, both in seconds
t = 0
interval = 1
tList = []
tempList = []

# Logging temperature data from DAQ Device
while True:
    voltOut = task.read()
    temp = tempCalc(voltOut)
    recordFileData(t, temp)

    tList.append(t)
    tempList.append(temp)
    ax.plot(tList, tempList, marker = 'o')
    fig.canvas.draw()
    
    time.sleep(interval)
    t += interval 

# Stop and close task
task.stop()
task.close()

