import serial
import time

RAK283_CMD = []

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

ser.reset_input_buffer()
ser.write(b"start\n")
print('waiting for get data from RAK283')
time.sleep(0.1)

while True:
	if ser.in_waiting > 0:
		line = ser.readline().decode('utf-8').rstrip()
		print(line)
		RAK283_CMD.append(str(line)) 
		time.sleep(1)
		
	if (str(line) == 'End of Process !!'):
		time.sleep(5)
		ser.reset_input_buffer()
		line = ''
	
