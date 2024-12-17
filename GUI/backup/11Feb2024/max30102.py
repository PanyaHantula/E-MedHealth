import max30102
import hrcalc

import matplotlib.pyplot as plt
import numpy as np
from drawnow import *

m = max30102.MAX30102()

#create the figure function
def makeFig():
    plt.ylim(160000,170000)
    plt.title('Osciloscope')
    plt.grid(True)
    plt.ylabel('ADC outputs')
    plt.plot(val, 'r', label='red')
    plt.legend(loc='lower right')

def main():
    global val
    val = []
    cnt = 0
    
    while (True):
        red, ir = m.read_fifo()
        # print(str(red) + ',' + str(ir))
        
        val.append(int(red))
        cnt = cnt+1
        if(cnt>2000):
            drawnow(makeFig)
            # val.pop(0)
            val = []
            cnt = 0
            
        # print(hrcalc.calc_hr_and_spo2(ir, red))

if __name__ == '__main__':
    main()
    
