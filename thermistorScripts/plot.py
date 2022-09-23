# Script used to read the csv file and plot the data on a graph

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd

interval = 1000 # 1000 ms = 1 s

def animate(i):
    data = pd.read_csv('tempData.csv')
    t = data['time (s)']
    temp = data['temperature (C)']

    t = t[-10:]
    temp = temp[-10:]

    plt.cla()
    plt.plot(t, temp, marker = 'o')
    plt.title('Temperature Graph')
    plt.xlabel('time (s)')
    plt.ylabel('temperature (C)')
    plt.grid()

ani = FuncAnimation(plt.gcf(), animate, interval = interval)
plt.show()
