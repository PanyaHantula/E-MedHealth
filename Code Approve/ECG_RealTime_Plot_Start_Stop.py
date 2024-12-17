from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk

import numpy as np
import time
import matplotlib.pyplot as plt
from drawnow import *

# Scope Config  
import Adafruit_ADS1x15
adc = Adafruit_ADS1x15.ADS1115()

# ------global variables
data = np.array([])
cond = False

# -----plot data-----
def plot_data():
    global cond, data

    if (cond == True):
        # Get ECG data Buffer
        cnt = 0
    
        while (cnt < 6000):
            value = adc.get_last_result()
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
    adc.start_adc(0, gain=GAIN)
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
ax.set_ylabel('Voltage')
ax.set_xlim(0, 6000)
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





