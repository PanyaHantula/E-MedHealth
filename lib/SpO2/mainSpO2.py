from lib.SpO2.hrcalc import calc_hr_and_spo2
from lib.SpO2.max30102 import MAX30102
import time
import numpy as np

class SpO2_Sensor():
    def __init__(self):
        self.bpm = 0

    def GetSpO2Sensor(self):
        m = MAX30102()
        hr2 = 0
        sp2 = 0

        red, ir = m.read_sequential()
        hr,hrb,sp,spb = calc_hr_and_spo2(ir, red)

        #print("hr detected:",hrb)
        #print("sp detected:",spb)
        
        if(hrb == True and hr != -999):
            hr2 = int(hr)
            #print("Heart Rate : ",hr2)
        if(spb == True and sp != -999):
            sp2 = int(sp)
            #print("SPO2       : ",sp2)

        ir = ir[10:110]
        red = red[10:110]
        SpO2_red_Norm = red / np.max(red)
        SpO2_ir_Norm = ir / np.max(ir)
        
        return hr2, sp2, SpO2_red_Norm, SpO2_ir_Norm
    
def main ():
    print('SpO2 Sensor starting...')
    SpO2 = SpO2_Sensor()
    wait = 1

    while True:
        hr2, sp2, red, ir = SpO2.GetSpO2Sensor()
        #print(A,B)
        print("BPM: {:.2f}, SpO2: {:.2f}".format(hr2, sp2))
        try:
            time.sleep(wait)
        except KeyboardInterrupt:
            print('keyboard interrupt detected, exiting...')

if __name__ == '__main__':
    main()