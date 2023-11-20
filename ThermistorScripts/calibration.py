# Script to calibrate thermistors

import csv
import nidaqmx
import argparse
import logging 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Function to calculate temperature in celsius given output voltage
def resCalc(voltList):
    resList = []

    voltIn = 5
    R0 = 10000 # 10k Ohm Resistor used for voltage divider

    # Calculate thermistor resistance
    for volt in voltList:
        Rt = (volt * R0) / (voltIn - volt)

        resList.append(Rt)

    return resList

# Animation initialization script
def init():
    ax.clear()

# Logging temperature data from DAQ Device and real time plotting
def animate(frame):
    voltOutList = task.read()
    resList = resCalc(voltOutList)

    time = frame * timeInterval

    with open('resData.csv', 'a', newline = '') as csvFile:
        csvWriter = csv.DictWriter(csvFile, fieldnames = fieldNames)
        data = {
            'time (s)': time,
            'res1 (ohm)': resList[0], 
            'res2 (ohm)': resList[1],
            'res3 (ohm)': resList[2],
            'res4 (ohm)': resList[3],
            'res5 (ohm)': resList[4],
            'res6 (ohm)': resList[5],
            'res7 (ohm)': resList[6],
            'res8 (ohm)': resList[7]
        }
        csvWriter.writerow(data)
        logging.info(f'time: {time} \n'
        f'          res1, {round(resList[0], 3)}; res2, {round(resList[1], 3)}; res3, {round(resList[2], 3)}; res4, {round(resList[3], 3)} \n'
        f'          res5, {round(resList[4], 3)}; res6, {round(resList[5], 3)}; res7, {round(resList[6], 3)}; res8, {round(resList[7], 3)}')

    data = pd.read_csv('resData.csv')
    t = data['time (s)']
    res1 = np.array(data['res1 (ohm)']) 
    res2 = np.array(data['res2 (ohm)']) + 2
    res3 = np.array(data['res3 (ohm)']) + 4
    res4 = np.array(data['res4 (ohm)']) + 6
    res5 = np.array(data['res5 (ohm)']) + 8
    res6 = np.array(data['res6 (ohm)']) + 10
    res7 = np.array(data['res7 (ohm)']) + 12
    res8 = np.array(data['res8 (ohm)']) + 14
    

    t = t[-50:]
    res1 = res1[-50:]
    res2 = res2[-50:]
    res3 = res3[-50:]
    res4 = res4[-50:]
    res5 = res5[-50:]
    res6 = res6[-50:]
    res7 = res7[-50:]
    res8 = res8[-50:]

    ax.clear()
    ax.plot(t, res1, marker = 'o', label = 'Thermistor 1', markersize = 3)
    ax.plot(t, res2, marker = 'o', label = 'Thermistor 2', markersize = 3)
    ax.plot(t, res3, marker = 'o', label = 'Thermistor 3', markersize = 3)
    ax.plot(t, res4, marker = 'o', label = 'Thermistor 4', markersize = 3)
    ax.plot(t, res5, marker = 'o', label = 'Thermistor 5', markersize = 3)
    ax.plot(t, res6, marker = 'o', label = 'Thermistor 6', markersize = 3)
    ax.plot(t, res7, marker = 'o', label = 'Thermistor 7', markersize = 3)
    ax.plot(t, res8, marker = 'o', label = 'Thermistor 8', markersize = 3)
    ax.legend()
    ax.set_title('Resistance Graph')
    ax.set_xlabel('time (s)')
    ax.set_ylabel('resistance (ohm)')
    ax.grid()


# Parse command line arguments
parser = argparse.ArgumentParser(description = 'Thermistor Resistance Data Collection')
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
RSE = nidaqmx.constants.TerminalConfiguration(10083) # Referenced Single-Ended
task.ai_channels.add_ai_voltage_chan('Dev1/ai0', terminal_config = RSE, min_val = 0, max_val = 5)
task.ai_channels.add_ai_voltage_chan('Dev1/ai1', terminal_config = RSE, min_val = 0, max_val = 5)
task.ai_channels.add_ai_voltage_chan('Dev1/ai2', terminal_config = RSE, min_val = 0, max_val = 5)
task.ai_channels.add_ai_voltage_chan('Dev1/ai3', terminal_config = RSE, min_val = 0, max_val = 5)
task.ai_channels.add_ai_voltage_chan('Dev1/ai4', terminal_config = RSE, min_val = 0, max_val = 5)
task.ai_channels.add_ai_voltage_chan('Dev1/ai5', terminal_config = RSE, min_val = 0, max_val = 5)
task.ai_channels.add_ai_voltage_chan('Dev1/ai6', terminal_config = RSE, min_val = 0, max_val = 5)
task.ai_channels.add_ai_voltage_chan('Dev1/ai7', terminal_config = RSE, min_val = 0, max_val = 5)
task.start()

# Open file for data recording
logging.info('Opening file resData.csv for data collection.')
fieldNames = ['time (s)', 'res1 (ohm)', 'res2 (ohm)', 'res3 (ohm)', 'res4 (ohm)', 'res5 (ohm)', 'res6 (ohm)', 'res7 (ohm)', 'res8 (ohm)']
with open('resData.csv', 'w') as csvFile:
    csvWriter = csv.DictWriter(csvFile, fieldnames = fieldNames)
    csvWriter.writeheader()

# Initialize plotting figure
fig = plt.figure(figsize = (14, 7))
ax = fig.add_subplot(111)

# Start data collection and animation
logging.info('Starting data collection and plotting animation.')
ani = FuncAnimation(fig, animate, init_func = init, interval = aniInterval, frames = numFrames, repeat = repeatBool)
plt.show()

# Stop and close task
task.stop()
task.close()