import serial
import time

class RAK283():
	def __init__(self) -> None:
		pass

	def run(self):
		print('Reading')

		self.ser = serial.Serial(
			port='/dev/ttyUSB0',
			baudrate = 115200,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			timeout=1
		)

		self.ser.reset_input_buffer()
		self.ser.write(b"start\n")
		print('waiting for get data from RAK283')
		time.sleep(0.1)

		SerialIncomming = []
		while self.ser.isOpen():
			if self.ser.in_waiting > 0:
				line = self.ser.readline().decode('utf-8').rstrip()
				print(line)
				SerialIncomming.append(str(line)) 
				time.sleep(1)
				
			if (str(line) == 'End of Process !!'):
				time.sleep(5)
				self.ser.reset_input_buffer()
				line = ''
				self.ser.close()
		return SerialIncomming
	
if __name__ == '__main__':
	bloodMeasure = RAK283()
	BloodRAK8232_DATA = bloodMeasure.run()
	print(BloodRAK8232_DATA)


	
