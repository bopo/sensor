import serial

def main():
	ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)
	while True:
		try:
			if not ser.isOpen():
				ser.open()

			data = ser.readline()
			print(data)

			if data:
				ser.write(b"hello")

		except KeyboardInterrupt:  
			ser.close() 


if __name__ == '__main__':
	main()