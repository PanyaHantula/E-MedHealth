import serial
import time
import sys

class BloodPressureSensor():
    def __init__(self):
         self.ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
    
    def Start(self):
        print('Start Get Blood Pressure')
        self.ser.reset_input_buffer()
        self.ser.write(b"start\n")
        print('waiting for get data from AC21CN3508 Board')
        print("Raw Serial Data:")
        time.sleep(0.1)

        SerialIncomming = []
        while self.ser.isOpen():
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').rstrip()
                print(line)
                SerialIncomming.append(str(line)) 
                time.sleep(0.1)
                
            if (str(line) == 'Done'):
                self.ser.reset_input_buffer()
                line = ''
                self.ser.close()

        # Data parsing
        try:
            index = SerialIncomming.index('Done') 
        except ValueError:
            index = -1   # Or any default value 
                   
        if index > -1:
            BloodPressureRawData = SerialIncomming[index-1]
            # print(BloodPressureRawData)
            BloodPressureRawData = BloodPressureRawData.split(",")
            SYS_data = BloodPressureRawData[0].strip("SYS:")
            DIA_data = BloodPressureRawData[1].strip("DIA:")
            PUL_data = BloodPressureRawData[2].strip("PUL:")
        else:
            SYS_data = 0
            DIA_data = 0
            PUL_data = 0
        
        return SYS_data, DIA_data, PUL_data
        
if __name__ == "__main__":
    BloodSensor = BloodPressureSensor()
    SYS,DIA,PUL = BloodSensor.Start()
    print(f'SYS : {SYS}, DIA : {DIA}, PUL : {PUL}')
    