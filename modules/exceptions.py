import serial
def writeException(e):
	with serial.Serial('/dev/ttyACM0',9600,timeout=1) as ser:
		ser.write(e.encode())
		ser.write(b'\n')

