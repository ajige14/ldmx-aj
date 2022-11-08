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

    # Steinhart-Hart Equation Coefficients
    a = 1.262740397e-3
    b = 1.968014123e-4
    c = 3.483432557e-7

    voltIn = 5
    R0 = 10000 # 10k Ohm Resistor used for voltage divider

    # Calculate thermistor resistance
    resList = (voltList * R0) / (voltIn - voltList)

    # Calculate temperature in Celsius
    tempList = 1 / (a + (b * np.log(resList)) + c * (np.log(resList))**3) - 273.15
    
    return tempList, resList

# Animation initialization script
def init():
    ax1.clear()
    ax2.clear()
    ax3.clear()

# Logging temperature data from DAQ Device and real time plotting
def animate(frame):

    # Read voltage and convert to temp
    voltOutDev1 = np.array(Dev1Task.read())
    voltOutDev2 = np.array(Dev2Task.read())
    voltOutDev3 = np.array(Dev3Task.read())

    tempDev1, resDev1 = tempCalc(voltOutDev1)
    tempDev2, resDev2 = tempCalc(voltOutDev2)
    tempDev3, resDev3 = tempCalc(voltOutDev3)

    time = frame * timeInterval

    with open(fileName, 'a', newline = '') as csvFile:
        csvWriter = csv.DictWriter(csvFile, fieldnames = fieldNames)
        data = {
            'time (s)': time,

            'temp1': tempDev1[0],   'temp2': tempDev1[1],   'temp3': tempDev1[2],   'temp4': tempDev1[3],
            'temp5': tempDev1[4],   'temp6': tempDev1[5],   'temp7': tempDev1[6],   'temp8': tempDev1[7],

            'temp9': tempDev2[0],   'temp10': tempDev2[1],  'temp11': tempDev2[2],  'temp12': tempDev2[3],
            'temp13': tempDev2[4],  'temp14': tempDev2[5],  'temp15': tempDev2[6],  'temp16': tempDev2[7],

            'temp17': tempDev3[0],  'temp18': tempDev3[1],  'temp19': tempDev3[2],  'temp20': tempDev3[3],
            'temp21': tempDev3[4],  'temp22': tempDev3[5],  'temp23': tempDev3[6],  'temp24': tempDev3[7],

            'res1': resDev1[0],     'res2': resDev1[1],     'res3': resDev1[2],     'res4': resDev1[3],
            'res5': resDev1[4],     'res6': resDev1[5],     'res7': resDev1[6],     'res8': resDev1[7],

            'res9': resDev2[0],     'res10': resDev2[1],    'res11': resDev2[2],   'res12': resDev2[3],
            'res13': resDev2[4],   'res14': resDev2[5],   'res15': resDev2[6],   'res16': resDev2[7],

            'res17': resDev3[0],   'res18': resDev3[1],   'res19': resDev3[2],   'res20': resDev3[3],
            'res21': resDev3[4],   'res22': resDev3[5],   'res23': resDev3[6],   'res24': resDev3[7]
        }
        csvWriter.writerow(data)
        logging.info(f'time: {time} \n'
        f'          temp1,  {tempDev1[0]:.3f}; temp2,  {tempDev1[1]:.3f}; temp3,  {tempDev1[2]:.3f}; temp4,  {tempDev1[3]:.3f} \n'
        f'          temp5,  {tempDev1[4]:.3f}; temp6,  {tempDev1[5]:.3f}; temp7,  {tempDev1[6]:.3f}; temp8,  {tempDev1[7]:.3f}\n'
        f'          temp9,  {tempDev2[0]:.3f}; temp10, {tempDev2[1]:.3f}; temp11, {tempDev2[2]:.3f}; temp12, {tempDev2[3]:.3f}\n'
        f'          temp13, {tempDev2[4]:.3f}; temp14, {tempDev2[5]:.3f}; temp15, {tempDev2[6]:.3f}; temp16, {tempDev2[7]:.3f}\n'
        f'          temp17, {tempDev3[0]:.3f}; temp18, {tempDev3[1]:.3f}; temp19, {tempDev3[2]:.3f}; temp20, {tempDev3[3]:.3f}\n'
        f'          temp21, {tempDev3[4]:.3f}; temp22, {tempDev3[5]:.3f}; temp23, {tempDev3[6]:.3f}; temp24, {tempDev3[7]:.3f}\n'
        
        )

    data = pd.read_csv(fileName)

    t = data['time (s)'][-50:]
    temp1 = data['temp1'][-50:]
    temp2 = data['temp2'][-50:]
    temp3 = data['temp3'][-50:]
    temp4 = data['temp4'][-50:]
    temp5 = data['temp5'][-50:]
    temp6 = data['temp6'][-50:]
    temp7 = data['temp7'][-50:]
    temp8 = data['temp8'][-50:]
    temp9 = data['temp9'][-50:]
    temp10 = data['temp10'][-50:]
    temp11 = data['temp11'][-50:]
    temp12 = data['temp12'][-50:]
    temp13 = data['temp13'][-50:]
    temp14 = data['temp14'][-50:]
    temp15 = data['temp15'][-50:]
    temp16 = data['temp16'][-50:]
    temp17 = data['temp17'][-50:]
    temp18 = data['temp18'][-50:]
    temp19 = data['temp19'][-50:]
    temp20 = data['temp20'][-50:]
    temp21 = data['temp21'][-50:]
    temp22 = data['temp22'][-50:]
    temp23 = data['temp23'][-50:]
    temp24 = data['temp24'][-50:]
    
    ax1.clear()
    ax1.plot(t, temp1, marker = 'o', linewidth = 1, label = 'Thermistor 1', markersize = 2)
    ax1.plot(t, temp2, marker = 'o', linewidth = 1, label = 'Thermistor 2', markersize = 2)
    ax1.plot(t, temp3, marker = 'o', linewidth = 1, label = 'Thermistor 3', markersize = 2)
    ax1.plot(t, temp4, marker = 'o', linewidth = 1,label = 'Thermistor 4', markersize = 2)
    ax1.plot(t, temp5, marker = 'o', linewidth = 1, label = 'Thermistor 5', markersize = 2)
    ax1.plot(t, temp6, marker = 'o', linewidth = 1, label = 'Thermistor 6', markersize = 2)
    ax1.plot(t, temp7, marker = 'o', linewidth = 1, label = 'Thermistor 7', markersize = 2)
    ax1.plot(t, temp8, marker = 'o', linewidth = 1, label = 'Thermistor 8', markersize = 2)
    ax1.legend()
    ax1.set_title('Thermistors 1 - 8')
    ax1.set_ylim(0, 30)
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('temperature (C)')

    ax2.clear()
    ax2.plot(t, temp9, marker = 'o', linewidth = 1, label = 'Thermistor 9', markersize = 2)
    ax2.plot(t, temp10, marker = 'o', linewidth = 1, label = 'Thermistor 10', markersize = 2)
    ax2.plot(t, temp11, marker = 'o', linewidth = 1, label = 'Thermistor 11', markersize = 2)
    ax2.plot(t, temp12, marker = 'o', linewidth = 1, label = 'Thermistor 12', markersize = 2)
    ax2.plot(t, temp13, marker = 'o', linewidth = 1, label = 'Thermistor 13', markersize = 2)
    ax2.plot(t, temp14, marker = 'o', linewidth = 1, label = 'Thermistor 14', markersize = 2)
    ax2.plot(t, temp15, marker = 'o', linewidth = 1, label = 'Thermistor 15', markersize = 2)
    ax2.plot(t, temp16, marker = 'o', linewidth = 1, label = 'Thermistor 16', markersize = 2)
    ax2.legend()
    ax2.set_title('Thermistors 9 - 16')
    ax2.set_xlabel('time (s)')

    ax3.clear()
    ax3.plot(t, temp17, marker = 'o', linewidth = 1, label = 'Thermistor 17', markersize = 2)
    ax3.plot(t, temp18, marker = 'o', linewidth = 1, label = 'Thermistor 18', markersize = 2)
    ax3.plot(t, temp19, marker = 'o', linewidth = 1, label = 'Thermistor 19', markersize = 2)
    ax3.plot(t, temp20, marker = 'o', linewidth = 1, label = 'Thermistor 20', markersize = 2)
    ax3.plot(t, temp21, marker = 'o', linewidth = 1, label = 'Thermistor 21', markersize = 2)
    ax3.plot(t, temp22, marker = 'o', linewidth = 1, label = 'Thermistor 22', markersize = 2)
    ax3.plot(t, temp23, marker = 'o', linewidth = 1, label = 'Thermistor 23', markersize = 2)
    ax3.plot(t, temp24, marker = 'o', linewidth = 1, label = 'Thermistor 24', markersize = 2)
    ax3.legend()
    ax3.set_title('Thermistors 17 - 24')
    ax3.set_xlabel('time (s)')

# Parse command line arguments
parser = argparse.ArgumentParser(description = 'Thermistor Temp Data Collection')
parser.add_argument('-t', '--time_interval',    help = 'Interval between each data collection, in seconds.')
parser.add_argument('-e', '--end_time',         help = 'End time for  data collection.')
parser.add_argument('-f', '--file_name',        help = 'Name of file to record data into.')

args = parser.parse_args()

# Configuring the logger
logging.basicConfig(format = '[ %(levelname)s ]: %(message)s', level = logging.INFO) 

# Assign start time and time interval for recording, both in seconds
timeInterval = float(args.time_interval)
aniInterval = int(timeInterval * 1000)

if not args.end_time:
    repeatBool = True
    numFrames = None
    logging.info('No final time specified, data collection will continue indefinitely.')
else:    
    endTime = float(args.end_time)
    numFrames = int((endTime / timeInterval) + 1)
    repeatBool = False

# Initialize the nidaqmx task, Dev1 --> Black, Dev2 --> Blue, Dev3 --> Yellow
logging.info('Initializing nidaqmx task.')
Dev1Task = nidaqmx.Task()
Dev2Task = nidaqmx.Task()
Dev3Task = nidaqmx.Task()
RSE = nidaqmx.constants.TerminalConfiguration(10083) # Referenced Single-Ended

Dev1Task.ai_channels.add_ai_voltage_chan('Dev1/ai0', terminal_config = RSE, min_val = 0, max_val = 5)
Dev1Task.ai_channels.add_ai_voltage_chan('Dev1/ai1', terminal_config = RSE, min_val = 0, max_val = 5)
Dev1Task.ai_channels.add_ai_voltage_chan('Dev1/ai2', terminal_config = RSE, min_val = 0, max_val = 5)
Dev1Task.ai_channels.add_ai_voltage_chan('Dev1/ai3', terminal_config = RSE, min_val = 0, max_val = 5)
Dev1Task.ai_channels.add_ai_voltage_chan('Dev1/ai4', terminal_config = RSE, min_val = 0, max_val = 5)
Dev1Task.ai_channels.add_ai_voltage_chan('Dev1/ai5', terminal_config = RSE, min_val = 0, max_val = 5)
Dev1Task.ai_channels.add_ai_voltage_chan('Dev1/ai6', terminal_config = RSE, min_val = 0, max_val = 5)
Dev1Task.ai_channels.add_ai_voltage_chan('Dev1/ai7', terminal_config = RSE, min_val = 0, max_val = 5)

Dev2Task.ai_channels.add_ai_voltage_chan('Dev2/ai0', terminal_config = RSE, min_val = 0, max_val = 5)
Dev2Task.ai_channels.add_ai_voltage_chan('Dev2/ai1', terminal_config = RSE, min_val = 0, max_val = 5)
Dev2Task.ai_channels.add_ai_voltage_chan('Dev2/ai2', terminal_config = RSE, min_val = 0, max_val = 5)
Dev2Task.ai_channels.add_ai_voltage_chan('Dev2/ai3', terminal_config = RSE, min_val = 0, max_val = 5)
Dev2Task.ai_channels.add_ai_voltage_chan('Dev2/ai4', terminal_config = RSE, min_val = 0, max_val = 5)
Dev2Task.ai_channels.add_ai_voltage_chan('Dev2/ai5', terminal_config = RSE, min_val = 0, max_val = 5)
Dev2Task.ai_channels.add_ai_voltage_chan('Dev2/ai6', terminal_config = RSE, min_val = 0, max_val = 5)
Dev2Task.ai_channels.add_ai_voltage_chan('Dev2/ai7', terminal_config = RSE, min_val = 0, max_val = 5)

Dev3Task.ai_channels.add_ai_voltage_chan('Dev3/ai0', terminal_config = RSE, min_val = 0, max_val = 5)
Dev3Task.ai_channels.add_ai_voltage_chan('Dev3/ai1', terminal_config = RSE, min_val = 0, max_val = 5)
Dev3Task.ai_channels.add_ai_voltage_chan('Dev3/ai2', terminal_config = RSE, min_val = 0, max_val = 5)
Dev3Task.ai_channels.add_ai_voltage_chan('Dev3/ai3', terminal_config = RSE, min_val = 0, max_val = 5)
Dev3Task.ai_channels.add_ai_voltage_chan('Dev3/ai4', terminal_config = RSE, min_val = 0, max_val = 5)
Dev3Task.ai_channels.add_ai_voltage_chan('Dev3/ai5', terminal_config = RSE, min_val = 0, max_val = 5)
Dev3Task.ai_channels.add_ai_voltage_chan('Dev3/ai6', terminal_config = RSE, min_val = 0, max_val = 5)
Dev3Task.ai_channels.add_ai_voltage_chan('Dev3/ai7', terminal_config = RSE, min_val = 0, max_val = 5)

Dev1Task.start()
Dev2Task.start()
Dev3Task.start()

# Open file for data recording
fileName = str(args.file_name)
logging.info(f'Opening file {fileName} for data collection.')
fieldNames = [
    'time (s)', 

    'temp1',    'temp2',    'temp3',    'temp4',    'temp5',    'temp6',    'temp7',    'temp8',
    'temp9',    'temp10',   'temp11',   'temp12',   'temp13',   'temp14',   'temp15',   'temp16',
    'temp17',   'temp18',   'temp19',   'temp20',   'temp21',   'temp22',   'temp23',   'temp24',

    'res1',     'res2',     'res3',     'res4',     'res5',     'res6',     'res7',     'res8',
    'res9',     'res10',    'res11',    'res12',    'res13',    'res14',    'res15',    'res16',
    'res17',    'res18',    'res19',    'res20',    'res21',    'res22',    'res23',    'res24'
]

with open(fileName, 'w') as csvFile:
    csvWriter = csv.DictWriter(csvFile, fieldnames = fieldNames)
    csvWriter.writeheader()

# Initialize plotting figure
fig = plt.figure(figsize = (18, 6))
fig.tight_layout()
fig.subplots_adjust(left = 0.05, right = 0.975, wspace = 0.1, top = 0.925)
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132, sharey = ax1)
ax3 = fig.add_subplot(133, sharey = ax1)

# Start data collection and animation
logging.info('Starting data collection and plotting animation.')
ani = FuncAnimation(fig, animate, init_func = init, interval = aniInterval, frames = numFrames, repeat = repeatBool)
plt.show()

# Stop and close task
Dev1Task.stop()
Dev2Task.stop()
Dev3Task.stop()

Dev1Task.close()
Dev2Task.close()
Dev3Task.close()
