# Script used to get compare temp data using individual calibration and whole calibration

import csv
import nidaqmx
import argparse
import logging 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Function to calculate temperature using whole calibration given output voltage
def totalCalc(voltList):
    totalTempList = []

    # Steinhart-Hart Equation Coefficients
    a = 1.262740397e-3
    b = 1.968014123e-4
    c = 3.483432557e-7

    voltIn = 5
    R0 = 10000 # 10k Ohm Resistor used for voltage divider

    # Calculate thermistor resistance
    for volt in voltList:
        Rt = (volt * R0) / (voltIn - volt)

        # Calculate temperature in Kelvin 
        tempK = 1 / (a + (b * np.log(Rt)) + c * (np.log(Rt))**3)

        # Convert from Kelvin to Celsius
        tempC = tempK - 273.15

        totalTempList.append(tempC)
    
    return totalTempList

# Function to calculate temperature using individual calibration given output voltage
def indCalc(voltList):
    indTempList = []

    # Thermistor Coefficients 
    coefficients = {
        1: [1.205128477e-3, 2.094565574e-4, 2.741892606e-7], 
        2: [1.406532446e-3, 1.754768206e-4, 4.163535932e-7], 
        3: [1.330672717e-3, 1.836781719e-4, 4.147272317e-7],
        4: [1.180427397e-3, 2.073609455e-4, 3.274716749e-7],
        5: [1.149354211e-3, 2.181719930e-4, 2.444470918e-7],
        6: [1.430276584e-3, 1.709819755e-4, 4.385882308e-7],
        7: [1.309786804e-3, 1.865957075e-4, 4.072690163e-7],
        8: [1.139845262e-3 , 2.144059319e-4, 2.970712604e-7]
    }

    voltIn = 5
    R0 = 10000 # 10k Ohm Resistor used for voltage divider

    # Calculate thermistor resistance
    for key, value in coefficients.items():
        index = key - 1
        volt = voltList[index]

        # Steinhart-Hart Equation Coefficients
        a = value[0]
        b = value[1]
        c = value[2]
        
        Rt = (volt * R0) / (voltIn - volt)

        # Calculate temperature in Kelvin 
        tempK = 1 / (a + (b * np.log(Rt)) + c * (np.log(Rt))**3)

        # Convert from Kelvin to Celsius
        tempC = tempK - 273.15

        indTempList.append(tempC)
    
    return indTempList


# Animation initialization script
def init():
    ax1.clear()
    ax2.clear()
    ax3.clear()

# Logging temperature data from DAQ Device and real time plotting
def animate(frame):
    voltOutList = task.read()
    totalTempList = totalCalc(voltOutList)
    indTempList = indCalc(voltOutList)
    difList = np.array(indTempList) - np.array(totalTempList)
    
    time = frame * timeInterval

    with open(fileName, 'a', newline = '') as csvFile:
        csvWriter = csv.DictWriter(csvFile, fieldnames = fieldNames)
        data = {
            'time (s)': time,
            'ind1': indTempList[0], 
            'ind2': indTempList[1],
            'ind3': indTempList[2],
            'ind4': indTempList[3],
            'ind5': indTempList[4],
            'ind6': indTempList[5],
            'ind7': indTempList[6],
            'ind8': indTempList[7],
            'total1': totalTempList[0],
            'total2': totalTempList[1],
            'total3': totalTempList[2],
            'total4': totalTempList[3],
            'total5': totalTempList[4],
            'total6': totalTempList[5],
            'total7': totalTempList[6],
            'total8': totalTempList[7],
            'dif1': difList[0],
            'dif2': difList[1],
            'dif3': difList[2],
            'dif4': difList[3],
            'dif5': difList[4],
            'dif6': difList[5],
            'dif7': difList[6],
            'dif8': difList[7]
        }
        csvWriter.writerow(data)
        logging.info(f'time: {time} \n'
        f'          ind1, {round(indTempList[0], 3)}; ind2, {round(indTempList[1], 3)}; ind3, {round(indTempList[2], 3)}; ind4, {round(indTempList[3], 3)} \n'
        f'          ind5, {round(indTempList[4], 3)}; ind6, {round(indTempList[5], 3)}; ind7, {round(indTempList[6], 3)}; ind8, {round(indTempList[7], 3)} \n\n'
        f'          total1, {round(totalTempList[0], 3)}; total2, {round(totalTempList[1], 3)}; total3, {round(totalTempList[2], 3)}; total4, {round(totalTempList[3], 3)} \n'
        f'          total5, {round(totalTempList[4], 3)}; total6, {round(totalTempList[5], 3)}; total7, {round(totalTempList[6], 3)}; total8, {round(totalTempList[7], 3)} \n\n'
        f'          dif1, {round(difList[0], 3)}; dif2, {round(difList[1], 3)}; dif3, {round(difList[2], 3)}; dif4, {round(difList[3], 3)} \n'
        f'          dif5, {round(difList[4], 3)}; dif6, {round(difList[5], 3)}; dif7, {round(difList[6], 3)}; dif8, {round(difList[7], 3)} \n'
        )

    data = pd.read_csv(fileName)
    t = data['time (s)']
    ind1 = np.array(data['ind1']) 
    ind2 = np.array(data['ind2']) + 2
    ind3 = np.array(data['ind3']) + 4
    ind4 = np.array(data['ind4']) + 6
    ind5 = np.array(data['ind5']) + 8
    ind6 = np.array(data['ind6']) + 10
    ind7 = np.array(data['ind7']) + 12
    ind8 = np.array(data['ind8']) + 14

    total1 = np.array(data['total1']) 
    total2 = np.array(data['total2']) + 2
    total3 = np.array(data['total3']) + 4
    total4 = np.array(data['total4']) + 6
    total5 = np.array(data['total5']) + 8
    total6 = np.array(data['total6']) + 10
    total7 = np.array(data['total7']) + 12
    total8 = np.array(data['total8']) + 14

    dif1 = np.array(data['dif1']) 
    dif2 = np.array(data['dif2']) + 2
    dif3 = np.array(data['dif3']) + 4
    dif4 = np.array(data['dif4']) + 6
    dif5 = np.array(data['dif5']) + 8
    dif6 = np.array(data['dif6']) + 10
    dif7 = np.array(data['dif7']) + 12
    dif8 = np.array(data['dif8']) + 14

    t = t[-50:]
    ind1 = ind1[-50:]
    ind2 = ind2[-50:]
    ind3 = ind3[-50:]
    ind4 = ind4[-50:]
    ind5 = ind5[-50:]
    ind6 = ind6[-50:]
    ind7 = ind7[-50:]
    ind8 = ind8[-50:]

    total1 = total1[-50:]
    total2 = total2[-50:]
    total3 = total3[-50:]
    total4 = total4[-50:]
    total5 = total5[-50:]
    total6 = total6[-50:]
    total7 = total7[-50:]
    total8 = total8[-50:]

    dif1 = dif1[-50:]
    dif2 = dif2[-50:]
    dif3 = dif3[-50:]
    dif4 = dif4[-50:]
    dif5 = dif5[-50:]
    dif6 = dif6[-50:]
    dif7 = dif7[-50:]
    dif8 = dif8[-50:]

    ax1.clear()
    ax1.plot(t, ind1, marker = 'o', label = 'Thermistor 1', markersize = 3)
    ax1.plot(t, ind2, marker = 'o', label = 'Thermistor 2', markersize = 3)
    ax1.plot(t, ind3, marker = 'o', label = 'Thermistor 3', markersize = 3)
    ax1.plot(t, ind4, marker = 'o', label = 'Thermistor 4', markersize = 3)
    ax1.plot(t, ind5, marker = 'o', label = 'Thermistor 5', markersize = 3)
    ax1.plot(t, ind6, marker = 'o', label = 'Thermistor 6', markersize = 3)
    ax1.plot(t, ind7, marker = 'o', label = 'Thermistor 7', markersize = 3)
    ax1.plot(t, ind8, marker = 'o', label = 'Thermistor 8', markersize = 3)
    ax1.legend()
    ax1.set_title('Temperature Graph of Individually Calibrated Thermistors')
    ax1.set_ylim(-50, 50)
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('temperature (C)')
    ax1.grid()

    ax2.clear()
    ax2.plot(t, total1, marker = 'o', label = 'Thermistor 1', markersize = 3)
    ax2.plot(t, total2, marker = 'o', label = 'Thermistor 2', markersize = 3)
    ax2.plot(t, total3, marker = 'o', label = 'Thermistor 3', markersize = 3)
    ax2.plot(t, total4, marker = 'o', label = 'Thermistor 4', markersize = 3)
    ax2.plot(t, total5, marker = 'o', label = 'Thermistor 5', markersize = 3)
    ax2.plot(t, total6, marker = 'o', label = 'Thermistor 6', markersize = 3)
    ax2.plot(t, total7, marker = 'o', label = 'Thermistor 7', markersize = 3)
    ax2.plot(t, total8, marker = 'o', label = 'Thermistor 8', markersize = 3)
    ax2.legend()
    ax2.set_title('Temperature Graph of Average Calibrated Thermistors')
    ax2.set_ylim(-50, 50)
    ax2.set_xlabel('time (s)')
    ax2.set_ylabel('temperature (C)')
    ax2.grid()

    ax3.clear()
    ax3.plot(t, dif1, marker = 'o', label = 'Thermistor 1', markersize = 3)
    ax3.plot(t, dif2, marker = 'o', label = 'Thermistor 2', markersize = 3)
    ax3.plot(t, dif3, marker = 'o', label = 'Thermistor 3', markersize = 3)
    ax3.plot(t, dif4, marker = 'o', label = 'Thermistor 4', markersize = 3)
    ax3.plot(t, dif5, marker = 'o', label = 'Thermistor 5', markersize = 3)
    ax3.plot(t, dif6, marker = 'o', label = 'Thermistor 6', markersize = 3)
    ax3.plot(t, dif7, marker = 'o', label = 'Thermistor 7', markersize = 3)
    ax3.plot(t, dif8, marker = 'o', label = 'Thermistor 8', markersize = 3)
    ax3.legend()
    ax3.set_title('Difference between Individual and Average Calibration')
    ax3.set_ylim(-50, 50)
    ax3.set_xlabel('time (s)')
    ax3.set_ylabel('temperature (C)')
    ax3.grid()


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
    'time (s)', 
    'ind1', 'ind2', 'ind3', 'ind4', 'ind5', 'ind6', 'ind7', 'ind8',
    'total1', 'total2', 'total3', 'total4', 'total5', 'total6', 'total7', 'total8',
    'dif1', 'dif2', 'dif3', 'dif4', 'dif5', 'dif6', 'dif7', 'dif8'
    ]
with open(fileName, 'w') as csvFile:
    csvWriter = csv.DictWriter(csvFile, fieldnames = fieldNames)
    csvWriter.writeheader()

# Initialize plotting figure
fig = plt.figure(figsize = (14, 14))
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)

# Start data collection and animation
logging.info('Starting data collection and plotting animation.')
ani = FuncAnimation(fig, animate, init_func = init, interval = aniInterval, frames = numFrames, repeat = repeatBool)
plt.show()

# Stop and close task
task.stop()
task.close()
