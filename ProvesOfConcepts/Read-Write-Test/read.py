import serial
import time
time.sleep(2)

with serial.Serial('/dev/ttyACM0',9600,timeout=1) as ser:
	try:
		while True:
			if ser.in_waiting > 0:
				data = ser.readline().decode('utf-8').strip()
				print(f"{data}")
	except KeyboardInterrupt:
		print("Exiting")
