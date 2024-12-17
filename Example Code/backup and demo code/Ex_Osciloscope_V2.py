import matplotlib.pyplot as plt
import numpy
from drawnow import *
import os
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create an ADS1115 ADC (16-bit) instance.
i2c = busio.I2C(board.SCL, board.SDA)		# Initialize the I2C interface
ads = ADS.ADS1115(i2c)						# Create an ADS1115 object
channel0 = AnalogIn(ads, ADS.P0)			# Define the analog input channels


#create the figure function
def makeFig():
    plt.ylim(0,3.3)
    plt.title('Osciloscope')
    plt.grid(True)
    plt.ylabel('ADC outputs')
    plt.plot(val, 'ro-', label='Channel 0')
    plt.legend(loc='lower right')

def main():
    # Scope Config
    GAIN = 1
    global val
    val = []
    cnt = 0
    plt.ion()
    
    while (True):
        # Read the last ADC conversion value and print it out.
        # value = adc.get_last_result()
        value = channel0.voltage
        print('Channel 0: {0}'.format(value))
        # Sleep for half a second.
        time.sleep(0.5)
        val.append(int(value))
        drawnow(makeFig)
        plt.pause(.000001)
        cnt = cnt+1
        if(cnt>50):
            val.pop(0)

if __name__ == '__main__':
    main()