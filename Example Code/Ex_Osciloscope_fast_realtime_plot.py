import time
import matplotlib.pyplot as plt
import numpy
from drawnow import *

# Scope Config  
import Adafruit_ADS1x15
adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1
#plt.ion()
adc.start_adc(0, gain=GAIN)
print('Reading ADS1x15 channel 0...')

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
    val = []
    cnt = 0
    
    while (True):
        value = adc.get_last_result()
        # print('Channel 0: {0}'.format(value))
        val.append(int(value))
        cnt = cnt+1
        if(cnt>7000):
            drawnow(makeFig)
            #plt.pause(.000001)
            cnt = 0
            val = []

if __name__ == '__main__':
    main()
    