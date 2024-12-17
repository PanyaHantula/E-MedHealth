from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import matplotlib.pyplot as plt
from drawnow import *

import os
import time
import board
import busio
import numpy as np
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)       # Initialize the I2C interface
ads = ADS.ADS1115(i2c)                      # Create an ADS1115 object

# Define the analog input channels 
#channel0 = AnalogIn(ads, ADS.P0)            
channel1 = AnalogIn(ads, ADS.P1)

# ------global variables
data = np.array([])
cond = False

print("Demo Code for ADS1115 : Get Raw ADC Data")

# -----plot data-----
def plot_data():
    global cond, data

    if (cond == True):
        # Get ECG data Buffer
        cnt = 0
    
        while (cnt < 200):
            value = channel1.value
            # print('Channel 0: {0}'.format(value))
            #data.append(int(value))
            data = np.append(data,int(value))
            cnt = cnt+1

        lines.set_xdata(np.arange(0, len(data)))
        lines.set_ydata(data)
        canvas.draw()
        
    root.after(1, plot_data)
    data = np.array([])
    cnt = 0

def plot_start():
    global cond
    cond = True
    GAIN = 1
    print('Reading ADS1x15 channel 0...')

def plot_stop():
    global cond
    cond = False
    adc.stop_adc()
    
# ---Main GUI code-----
root = tk.Tk()
root.title('Real Time Plot')
root.configure(background='light blue')
root.geometry("700x500")  # set the window size

# ------create Plot object on GUI----------
# add figure canvas
fig = Figure();
ax = fig.add_subplot(111)

# ax = plt.axes(xlim=(0,100),ylim=(0, 120)); #displaying only 100 samples
ax.set_title('ECG Data');
ax.set_xlabel('Sample')
ax.set_ylabel('vlaue')
ax.set_xlim(0, 200)
ax.set_ylim(0, 40000)
lines = ax.plot([], [])[0]

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.get_tk_widget().place(x=20, y=10, width=500, height=400)
canvas.draw()

# ----------create button---------
root.update();
start = tk.Button(root, text="Start", font=('calbiri', 12), command=lambda: plot_start())
start.place(x=100, y=450)

root.update();
stop = tk.Button(root, text="Stop", font=('calbiri', 12), command=lambda: plot_stop())
stop.place(x=start.winfo_x() + start.winfo_reqwidth() + 20, y=450)

root.after(1, plot_data)
root.mainloop()





