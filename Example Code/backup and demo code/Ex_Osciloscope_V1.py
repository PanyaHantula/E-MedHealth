import time
import matplotlib.pyplot as plt
import numpy
from drawnow import *

# Import the ADS1x15 module.
import Adafruit_ADS1x15

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

# Scope Config
GAIN = 1
val = [ ]
cnt = 0
plt.ion()

# Start continuous ADC conversions on channel 0 using the previously set gain
adc.start_adc(0, gain=GAIN)
print('Reading ADS1x15 channel 0...')
#create the figure function
def makeFig():
    plt.ylim(0,40000)
    plt.title('Osciloscope')
    plt.grid(True)
    plt.ylabel('ADC outputs')
    plt.plot(val, 'ro-', label='Channel 0')
    plt.legend(loc='lower right')

while (True):
    value = adc.get_last_result()
    print('Channel 0: {0}'.format(value))
    val.append(int(value))
    drawnow(makeFig)
    plt.pause(.000001)
    cnt = cnt+1
    if(cnt>50):
        val.pop(0)
