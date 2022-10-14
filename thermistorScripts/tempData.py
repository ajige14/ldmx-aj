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
def tempCalc(voltList):
    tempList = []
    resList = []

    # Steinhart-Hart Equation Coefficients
    a = 1.262740397e-3
    b = 1.968014123e-4
    c = 3.483432557e-7

    voltIn = 5
    R0 = 10000 # 10k Ohm Resistor used for voltage divider

    # Calculate thermistor resistance
    for volt in voltList:
        Rt = (volt * R0) / (voltIn - volt)
        resList.append(Rt)

        # Calculate temperature in Kelvin 
        tempK = 1 / (a + (b * np.log(Rt)) + c * (np.log(Rt))**3)

        # Convert from Kelvin to Celsius
        tempC = tempK - 273.15

        tempList.append(tempC)
    
    return tempList, resList

# Animation initialization script
def init():
    ax.clear()

# Logging temperature data from DAQ Device and real time plotting
def animate(frame):
    voltOutList = task.read()
    tempList, resList = tempCalc(voltOutList)

    time = frame * timeInterval

    with open(fileName, 'a', newline = '') as csvFile:
        csvWriter = csv.DictWriter(csvFile, fieldnames = fieldNames)
        data = {
            'time (s)': time,
            'temp1 (C)': tempList[0], 
            'temp2 (C)': tempList[1],
            'temp3 (C)': tempList[2],
            'temp4 (C)': tempList[3],
            'temp5 (C)': tempList[4],
            'temp6 (C)': tempList[5],
            'temp7 (C)': tempList[6],
            'temp8 (C)': tempList[7],
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
        f'          temp1, {round(tempList[0], 3)}; temp2, {round(tempList[1], 3)}; temp3, {round(tempList[2], 3)}; temp4, {round(tempList[3], 3)} \n'
        f'          temp5, {round(tempList[4], 3)}; temp6, {round(tempList[5], 3)}; temp7, {round(tempList[6], 3)}; temp8, {round(tempList[7], 3)}')

    data = pd.read_csv(fileName)
    t = data['time (s)']
    temp1 = np.array(data['temp1 (C)']) 
    temp2 = np.array(data['temp2 (C)']) + 2
    temp3 = np.array(data['temp3 (C)']) + 4
    temp4 = np.array(data['temp4 (C)']) + 6
    temp5 = np.array(data['temp5 (C)']) + 8
    temp6 = np.array(data['temp6 (C)']) + 10
    temp7 = np.array(data['temp7 (C)']) + 12
    temp8 = np.array(data['temp8 (C)']) + 14
    
    t = t[-50:]
    temp1 = temp1[-50:]
    temp2 = temp2[-50:]
    temp3 = temp3[-50:]
    temp4 = temp4[-50:]
    temp5 = temp5[-50:]
    temp6 = temp6[-50:]
    temp7 = temp7[-50:]
    temp8 = temp8[-50:]

    ax.clear()
    ax.plot(t, temp1, marker = 'o', label = 'Thermistor 1', markersize = 3)
    ax.plot(t, temp2, marker = 'o', label = 'Thermistor 2', markersize = 3)
    ax.plot(t, temp3, marker = 'o', label = 'Thermistor 3', markersize = 3)
    ax.plot(t, temp4, marker = 'o', label = 'Thermistor 4', markersize = 3)
    ax.plot(t, temp5, marker = 'o', label = 'Thermistor 5', markersize = 3)
    ax.plot(t, temp6, marker = 'o', label = 'Thermistor 6', markersize = 3)
    ax.plot(t, temp7, marker = 'o', label = 'Thermistor 7', markersize = 3)
    ax.plot(t, temp8, marker = 'o', label = 'Thermistor 8', markersize = 3)
    ax.legend()
    ax.set_title('Temperature Graph')
    ax.set_ylim(-50, 50)
    ax.set_xlabel('time (s)')
    ax.set_ylabel('temperature (C)')
    ax.grid()

# Parse command line arguments
parser = argparse.ArgumentParser(description = 'Thermistor Temp Data Collection')
parser.add_argument('-t', '--time_interval',      help = 'Interval between each data collection, in seconds.')
parser.add_argument('-f', '--final_time',         help = 'Final data collection time.')
parser.add_argument('-n', '--file_name',          help = 'Name of file to record data into.')

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
fileName = str(args.file_name)
logging.info(f'Opening file {fileName} for data collection.')
fieldNames = [
    'time (s)', 'temp1 (C)', 'temp2 (C)', 'temp3 (C)', 'temp4 (C)', 'temp5 (C)', 'temp6 (C)', 'temp7 (C)', 'temp8 (C)',
    'res1 (ohm)', 'res2 (ohm)', 'res3 (ohm)', 'res4 (ohm)', 'res5 (ohm)', 'res6 (ohm)', 'res7 (ohm)', 'res8 (ohm)'
]
with open(fileName, 'w') as csvFile:
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
