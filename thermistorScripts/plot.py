# Script used to read the csv file and plot the data on a graph

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd

interval = 1000 # 1000 ms = 1 s

def animate(i):
    data = pd.read_csv('tempData.csv')
    t = data['Time (s)']
    temp = data['Temperature (C)']

    plt.cla()
    plt.plot(t, temp, marker = 'o')

ani = FuncAnimation(plt.gcf(), animate, interval = interval)
plt.show()
