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
    voltOutList = np.array(task.read())
    tempList, resList = tempCalc(voltOutList)

    time = frame * timeInterval

    with open(fileName, 'a', newline = '') as csvFile:
        csvWriter = csv.DictWriter(csvFile, fieldnames = fieldNames)
        data = {
            'time (s)': time,

            'temp1': tempList[0],     'temp2': tempList[1],     'temp3': tempList[2],     'temp4': tempList[3],
            'temp5': tempList[4],     'temp6': tempList[5],     'temp7': tempList[6],     'temp8': tempList[7],
            'temp9': tempList[8],     'temp10': tempList[9],    'temp11': tempList[10],   'temp12': tempList[11],
            'temp13': tempList[12],   'temp14': tempList[13],   'temp15': tempList[14],   'temp16': tempList[15],
            'temp17': tempList[16],   'temp18': tempList[17],   'temp19': tempList[18],   'temp20': tempList[19],
            'temp21': tempList[20],   'temp22': tempList[21],   'temp23': tempList[22],   'temp24': tempList[23],

            'res1': resList[0],     'res2': resList[1],     'res3': resList[2],     'res4': resList[3],
            'res5': resList[4],     'res6': resList[5],     'res7': resList[6],     'res8': resList[7],
            'res9': resList[8],     'res10': resList[9],    'res11': resList[10],   'res12': resList[11],
            'res13': resList[12],   'res14': resList[13],   'res15': resList[14],   'res16': resList[15],
            'res17': resList[16],   'res18': resList[17],   'res19': resList[18],   'res20': resList[19],
            'res21': resList[20],   'res22': resList[21],   'res23': resList[22],   'res24': resList[23]
        }
        csvWriter.writerow(data)
        logging.info(f'time: {time} \n'
        f'          temp1, {round(tempList[0], 3)}; temp2, {round(tempList[1], 3)}; temp3, {round(tempList[2], 3)}; temp4, {round(tempList[3], 3)} \n'
        f'          temp5, {round(tempList[4], 3)}; temp6, {round(tempList[5], 3)}; temp7, {round(tempList[6], 3)}; temp8, {round(tempList[7], 3)}\n'
        f'          temp9, {round(tempList[8], 3)}; temp10, {round(tempList[9], 3)}; temp11, {round(tempList[10], 3)}; temp12, {round(tempList[11], 3)}\n'
        f'          temp13, {round(tempList[12], 3)}; temp14, {round(tempList[13], 3)}; temp15, {round(tempList[14], 3)}; temp16, {round(tempList[15], 3)}\n'
        f'          temp17, {round(tempList[16], 3)}; temp18, {round(tempList[17], 3)}; temp19, {round(tempList[18], 3)}; temp20, {round(tempList[19], 3)}\n'
        f'          temp21, {round(tempList[20], 3)}; temp22, {round(tempList[21], 3)}; temp23, {round(tempList[22], 3)}; temp24, {round(tempList[23], 3)}'
        )

    data = pd.read_csv(fileName)

    t = data['time (s)'][-50:]
    temp1 = np.array(data['temp1'])[-50:]
    temp2 = np.array(data['temp2'])[-50:]
    temp3 = np.array(data['temp3'])[-50:]
    temp4 = np.array(data['temp4'])[-50:]
    temp5 = np.array(data['temp5'])[-50:]
    temp6 = np.array(data['temp6'])[-50:]
    temp7 = np.array(data['temp7'])[-50:]
    temp8 = np.array(data['temp8'])[-50:]
    temp9 = np.array(data['temp9'])[-50:]
    temp10 = np.array(data['temp10'])[-50:]
    temp11 = np.array(data['temp11'])[-50:]
    temp12 = np.array(data['temp12'])[-50:]
    temp13 = np.array(data['temp13'])[-50:]
    temp14 = np.array(data['temp14'])[-50:]
    temp15 = np.array(data['temp15'])[-50:]
    temp16 = np.array(data['temp16'])[-50:]
    temp17 = np.array(data['temp17'])[-50:]
    temp18 = np.array(data['temp18'])[-50:]
    temp19 = np.array(data['temp19'])[-50:]
    temp20 = np.array(data['temp20'])[-50:]
    temp21 = np.array(data['temp21'])[-50:]
    temp22 = np.array(data['temp22'])[-50:]
    temp23 = np.array(data['temp23'])[-50:]
    temp24 = np.array(data['temp24'])[-50:]
    
    ax1.clear()
    ax1.plot(t, temp1, marker = 'o', label = 'Thermistor 1', markersize = 3)
    ax1.plot(t, temp2, marker = 'o', label = 'Thermistor 2', markersize = 3)
    ax1.plot(t, temp3, marker = 'o', label = 'Thermistor 3', markersize = 3)
    ax1.plot(t, temp4, marker = 'o', label = 'Thermistor 4', markersize = 3)
    ax1.plot(t, temp5, marker = 'o', label = 'Thermistor 5', markersize = 3)
    ax1.plot(t, temp6, marker = 'o', label = 'Thermistor 6', markersize = 3)
    ax1.plot(t, temp7, marker = 'o', label = 'Thermistor 7', markersize = 3)
    ax1.plot(t, temp8, marker = 'o', label = 'Thermistor 8', markersize = 3)
    ax1.legend()
    ax1.set_title('Thermistors 1 - 8')
    ax1.set_ylim(-10, 30)
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('temperature (C)')

    ax2.clear()
    ax2.plot(t, temp9, marker = 'o', label = 'Thermistor 9', markersize = 3)
    ax2.plot(t, temp10, marker = 'o', label = 'Thermistor 10', markersize = 3)
    ax2.plot(t, temp11, marker = 'o', label = 'Thermistor 11', markersize = 3)
    ax2.plot(t, temp12, marker = 'o', label = 'Thermistor 12', markersize = 3)
    ax2.plot(t, temp13, marker = 'o', label = 'Thermistor 13', markersize = 3)
    ax2.plot(t, temp14, marker = 'o', label = 'Thermistor 14', markersize = 3)
    ax2.plot(t, temp15, marker = 'o', label = 'Thermistor 15', markersize = 3)
    ax2.plot(t, temp16, marker = 'o', label = 'Thermistor 16', markersize = 3)
    ax2.legend()
    ax2.set_title('Thermistors 9 - 16')
    ax2.set_ylim(-10, 30)
    ax2.set_xlabel('time (s)')
    ax2.set_ylabel('temperature (C)')

    ax3.clear()
    ax3.plot(t, temp17, marker = 'o', label = 'Thermistor 17', markersize = 3)
    ax3.plot(t, temp18, marker = 'o', label = 'Thermistor 18', markersize = 3)
    ax3.plot(t, temp19, marker = 'o', label = 'Thermistor 19', markersize = 3)
    ax3.plot(t, temp20, marker = 'o', label = 'Thermistor 20', markersize = 3)
    ax3.plot(t, temp21, marker = 'o', label = 'Thermistor 21', markersize = 3)
    ax3.plot(t, temp22, marker = 'o', label = 'Thermistor 22', markersize = 3)
    ax3.plot(t, temp23, marker = 'o', label = 'Thermistor 23', markersize = 3)
    ax3.plot(t, temp24, marker = 'o', label = 'Thermistor 24', markersize = 3)
    ax3.legend()
    ax3.set_title('Thermistors 17 - 24')
    ax3.set_ylim(-10, 30)
    ax3.set_xlabel('time (s)')
    ax3.set_ylabel('temperature (C)')

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

task.ai_channels.add_ai_voltage_chan('Dev2/ai0', terminal_config = RSE, min_val = 0, max_val = 5)
task.ai_channels.add_ai_voltage_chan('Dev2/ai1', terminal_config = RSE, min_val = 0, max_val = 5)
task.ai_channels.add_ai_voltage_chan('Dev2/ai2', terminal_config = RSE, min_val = 0, max_val = 5)
task.ai_channels.add_ai_voltage_chan('Dev2/ai3', terminal_config = RSE, min_val = 0, max_val = 5)
task.ai_channels.add_ai_voltage_chan('Dev2/ai4', terminal_config = RSE, min_val = 0, max_val = 5)
task.ai_channels.add_ai_voltage_chan('Dev2/ai5', terminal_config = RSE, min_val = 0, max_val = 5)
task.ai_channels.add_ai_voltage_chan('Dev2/ai6', terminal_config = RSE, min_val = 0, max_val = 5)
task.ai_channels.add_ai_voltage_chan('Dev2/ai7', terminal_config = RSE, min_val = 0, max_val = 5)

task.ai_channels.add_ai_voltage_chan('Dev3/ai0', terminal_config = RSE, min_val = 0, max_val = 5)
task.ai_channels.add_ai_voltage_chan('Dev3/ai1', terminal_config = RSE, min_val = 0, max_val = 5)
task.ai_channels.add_ai_voltage_chan('Dev3/ai2', terminal_config = RSE, min_val = 0, max_val = 5)
task.ai_channels.add_ai_voltage_chan('Dev3/ai3', terminal_config = RSE, min_val = 0, max_val = 5)
task.ai_channels.add_ai_voltage_chan('Dev3/ai4', terminal_config = RSE, min_val = 0, max_val = 5)
task.ai_channels.add_ai_voltage_chan('Dev3/ai5', terminal_config = RSE, min_val = 0, max_val = 5)
task.ai_channels.add_ai_voltage_chan('Dev3/ai6', terminal_config = RSE, min_val = 0, max_val = 5)
task.ai_channels.add_ai_voltage_chan('Dev3/ai7', terminal_config = RSE, min_val = 0, max_val = 5)

task.start()

# Open file for data recording
fileName = str(args.file_name)
logging.info(f'Opening file {fileName} for data collection.')
fieldNames = [
    'time (s)', 

    'temp1',    'temp2',    'temp3',    'temp4',    'temp5',    'temp6',    'temp7',    'temp8',
    'temp9',    'temp10',   'temp11',   'temp12',   'temp13',   'temp14',   'temp15',   'temp16',
    'temp17',   'temp18',   'temp19',   'temp20',   'temp21',   'temp22',   'temp23',   'temp24',

    'res1',     'res2',     'res3',     'res4',     'res5',     'res6',     'res7',     'res8'
    'res9',     'res10',    'res11',    'res12',    'res13',    'res14',    'res15',    'res16'
    'res17',    'res18',    'res19',    'res20',    'res21',    'res22',    'res23',    'res24'
]
with open(fileName, 'w') as csvFile:
    csvWriter = csv.DictWriter(csvFile, fieldnames = fieldNames)
    csvWriter.writeheader()

# Initialize plotting figure
fig = plt.figure(figsize = (15, 5))
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)

# Start data collection and animation
logging.info('Starting data collection and plotting animation.')
ani = FuncAnimation(fig, animate, init_func = init, interval = aniInterval, frames = numFrames, repeat = repeatBool)
plt.show()

# Stop and close task
task.stop()
task.close()
