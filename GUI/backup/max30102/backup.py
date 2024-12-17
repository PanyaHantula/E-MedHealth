from GUI.max30102 import MAX30102
import GUI.hrcalc as hrcalc
import time
import numpy as np

class HeartRateMonitor():
    def __init__(self):
        self.bpm = 0

    def run_sensor(self):
        sensor = MAX30102()
        ir_data = []
        red_data = []
        bpms = []

        #while True:
        # check if any data is available
        num_bytes = sensor.get_data_present()

        if num_bytes > 0:
            # grab all the data and stash it into arrays
            while num_bytes > 0:
                red, ir = sensor.read_fifo()
                num_bytes -= 1
                ir_data.append(ir)
                red_data.append(red)
                #print("{0}, {1}".format(ir, red))

            while len(ir_data) > 100:
                ir_data.pop(0)
                red_data.pop(0)

            if len(ir_data) == 100:
                self.bpm, valid_bpm, self.spo2, valid_spo2 = hrcalc.calc_hr_and_spo2(ir_data, red_data)
                if valid_bpm:
                    bpms.append(self.bpm)
                    while len(bpms) > 4:
                        bpms.pop(0)
                    self.bpm = np.mean(bpms)
                    if (np.mean(ir_data) < 50000 and np.mean(red_data) < 50000):
                        self.bpm = 0
                        print("Finger not detected")
                    else:
                        print("BPM: {:.2f}, SpO2: {:.2f}".format(self.bpm, self.spo2))
                        #return [self.bpm, self.spo2]
    
def main ():
    print('sensor starting...')
    SpO2_Sensor = HeartRateMonitor()
    LOOP_TIME = 1

    while True:
        SpO2_Sensor.run_sensor()
        #print(A)
       # print("BPM: {:.2f}, SpO2: {:.2f}".format(A, B))
        time.sleep(LOOP_TIME)

if __name__ == '__main__':
    main()