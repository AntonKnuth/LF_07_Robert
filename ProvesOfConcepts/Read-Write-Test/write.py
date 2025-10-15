import serial
import time
time.sleep(2)

counter = 0
with serial.Serial('/dev/ttyACM0',9600,timeout=1) as ser:
	try:
		while True:
			if counter == 0:
				ser.write(b'LichtAn\n')
			if counter == 1:
				ser.write(b'Blue\n')
			if counter == 2:
				ser.write(b'Darker\n')	
			counter +=1
			if counter > 3:
				counter = 0
			time.sleep(1)
	except KeyboardInterrupt:
		print("Exiting")
