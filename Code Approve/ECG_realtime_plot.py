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
channel0 = AnalogIn(ads, ADS.P0)            

#create the figure function
def makeFig():
    plt.ylim(0,40000)
    plt.title('Osciloscope')
    plt.grid(True)
    plt.ylabel('ADC outputs')
    plt.plot(val, 'r', label='Channel 0')
    plt.legend(loc='lower right')

def main():
    global val
    val = np.array([])
    cnt = 0
    
    while (True):
        value = channel0.value
        #print('Channel 0: {0}'.format(value))
        val = np.append(val,int(value))
        cnt = cnt+1
        if(cnt > 200):
            drawnow(makeFig)
            #plt.pause(.000001)
            cnt = 0
            val = []

if __name__ == '__main__':
    main()
    