# Script used to get temp data from the NI DAQ Device and record it into a csv file while plotting it

import csv
import nidaqmx
import argparse
import logging 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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

# Animation initialization script
def init():
    ax.clear()

# Logging temperature data from DAQ Device and real time plotting
def animate(frame):
    voltOut = task.read()
    temp = tempCalc(voltOut)

    time = frame * timeInterval

    with open('tempData.csv', 'a', newline = '') as csvFile:
        csvWriter = csv.DictWriter(csvFile, fieldnames = fieldNames)
        data = {
            'time (s)': time,
            'temperature (C)': temp
        }
        csvWriter.writerow(data)
        logging.info(f'time (s): {time}; temperature (C): {temp}')

    data = pd.read_csv('tempData.csv')
    t = data['time (s)']
    temp = data['temperature (C)']

    t = t[-10:]
    temp = temp[-10:]

    ax.clear()
    ax.plot(t, temp, marker = 'o')
    ax.set_title('Temperature Graph')
    ax.set_ylim(-50, 50)
    ax.set_xlabel('time (s)')
    ax.set_ylabel('temperature (C)')
    ax.grid()

# Parse command line arguments
parser = argparse.ArgumentParser(description = 'Thermistor Temp Data Collection')
parser.add_argument('-t', '--time_interval',      help = 'Interval between each data collection, in seconds.')
parser.add_argument('-f', '--final_time',         help = 'Final data collection time.')

args = parser.parse_args()

# Configuring the logger
logging.basicConfig(format = '[ %(levelname)s ]: %(message)s', level = logging.INFO) 

# Assign start time and time interval for recording, both in seconds
timeInterval = float(args.time_interval)
aniInterval = int(timeInterval * 1000)

if not args.final_time:
    repeatBool = True
    numFrames = None
    logging.info('No final time specified, data collection will continue indefinitely.')
else:    
    finalTime = float(args.final_time)
    numFrames = int((finalTime / timeInterval) + 1)
    repeatBool = False

# Initialize the nidaqmx task
logging.info('Initializing nidaqmx task.')
task = nidaqmx.Task()
task.ai_channels.add_ai_voltage_chan('Dev1/ai0', min_val = 0, max_val = 5)
task.start()

# Open file for data recording
logging.info('Opening file tempData.csv for data collection.')
fieldNames = ['time (s)', 'temperature (C)']
with open('tempData.csv', 'w') as csvFile:
    csvWriter = csv.DictWriter(csvFile, fieldnames = fieldNames)
    csvWriter.writeheader()

# Initialize plotting figure
fig, ax = plt.subplots()

# Start data collection and animation
logging.info('Starting data collection and plotting animation.')
ani = FuncAnimation(fig, animate, init_func = init, interval = aniInterval, frames = numFrames, repeat = repeatBool)
plt.show()

# Stop and close task
task.stop()
task.close()
