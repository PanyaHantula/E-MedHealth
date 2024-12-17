import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import random
import serial

# initialize serial port
ser = serial.Serial()
ser.port = '/dev/ttyUSB0'  # Arduino serial port
ser.baudrate = 115200
ser.timeout = 10  # specify timeout when using readline()
ser.open()
if ser.is_open == True:
    print("\nAll right, serial port now open. Configuration:\n")
    print(ser, "\n")  # print serial parameters

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []  # store trials here (n)
ys = []  # store relative frequency here
rs = []  # for theoretical probability


# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    # Aquire and parse data from serial port
    relProb_float = float(ser.readline())  # ascii

    # Add x and y to lists
    xs.append(i)
    ys.append(relProb_float)
    rs.append(0.5)

    # Limit x and y lists to 20 items
    # xs = xs[-20:]
    # ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys, label="ECG Detected")

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('ECG Monitoring')
    plt.ylabel('Relative ADC of ECG Value')
    plt.xlabel('Time(ms)')
    plt.legend()
    plt.axis([1, None, 0, 1024])  # Use for arbitrary number of trials
    # plt.axis([1, 100, 0, 1.1]) #Use for 100 trial demo


# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1)
plt.show()