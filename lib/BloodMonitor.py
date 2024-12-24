import serial
import time
import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QDesktopWidget, \
    QVBoxLayout, QWidget, QLabel, QPushButton

class RAK283(QWidget):
	def __init__(self):
		super().__init__()
		pass

	def start(self):
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

		self.SerialIncomming = []
		while self.ser.isOpen():
			if self.ser.in_waiting > 0:
				line = self.ser.readline().decode('utf-8').rstrip()
				print(line)
				self.SerialIncomming.append(str(line)) 
				time.sleep(1)
				
			if (str(line) == '#:Done'):
				#time.sleep(5)
				self.ser.reset_input_buffer()
				line = ''
				self.ser.close()

		return self.SerialIncomming
	
def main():
    app = QApplication([])
    RAK283Window = RAK283()
    app.exec()

if __name__ == "__main__":
    main()


	
