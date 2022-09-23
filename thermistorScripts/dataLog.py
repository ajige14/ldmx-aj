# Script used to get voltage data from the NI DAQ Device and record it into a csv file

import nidaqmx
import numpy as np
import csv
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

# Initialize the nidaqmx task
task = nidaqmx.Task()
task.ai_channels.add_ai_voltage_chan('Dev1/ai0', min_val = 0, max_val = 5)
task.start()

# Open file for data recording
fieldNames = ['time (s)', 'temperature (C)']
with open('tempData.csv', 'w') as csvFile:
    csvWriter = csv.DictWriter(csvFile, fieldnames = fieldNames)
    csvWriter.writeheader()

# Assign start time and time interval for recording, both in seconds
t = 0
interval = 1
stopTime = 5

# Logging temperature data from DAQ Device
while True:
    voltOut = task.read()
    temp = tempCalc(voltOut)

    with open('tempData.csv', 'a') as csvFile:
        csvWriter = csv.DictWriter(csvFile, fieldnames = fieldNames)
        data = {
            'time (s)': t,
            'temperature (C)': temp
        }

        print(f'time (s): {t}, temp (C): {temp}')

    if t == stopTime:
        break
    else:
        time.sleep(interval)
        t += interval 

# Stop and close task
task.stop()
task.close()