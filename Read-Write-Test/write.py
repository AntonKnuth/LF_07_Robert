import serial
import time
time.sleep(2)

with serial.Serial('/dev/ttyACM1',9600,timeout=1) as ser:
	try:
		while True:
			ser.write(b'Hallo from RaspPi\\n')
			time.sleep(1)
	except KeyboardInterrupt:
		print("Exiting")
