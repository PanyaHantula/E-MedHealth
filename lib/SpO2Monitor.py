from max30102 import MAX30102
import hrcalc as hrcalc
import time
import numpy as np

class SpO2Monitor():
    def __init__(self):
        self.bpm = 0

    def GetSpO2Sensor(self):
        m = MAX30102()
        hr2 = 0
        sp2 = 0

        red, ir = m.read_sequential()
        hr,hrb,sp,spb = hrcalc.calc_hr_and_spo2(ir, red)

        #print("hr detected:",hrb)
        #print("sp detected:",spb)
        
        if(hrb == True and hr != -999):
            hr2 = int(hr)
            #print("Heart Rate : ",hr2)
        if(spb == True and sp != -999):
            sp2 = int(sp)
            #print("SPO2       : ",sp2)

        return hr2, sp2, red, ir
    
def main ():
    print('sensor starting...')
    SpO2_Sensor = SpO2Monitor()
    LOOP_TIME = 1

    while True:
        A, B = SpO2_Sensor.run_sensor()
        #print(A,B)
        print("BPM: {:.2f}, SpO2: {:.2f}".format(A, B))
        time.sleep(LOOP_TIME)

if __name__ == '__main__':
    main()