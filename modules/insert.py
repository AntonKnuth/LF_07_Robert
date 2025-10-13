import database
import serial
import time
import datetime
time.sleep(2)

with serial.Serial('/dev/ttyACM0',9600,timeout=1) as ser:
	try:
		while True:
			if ser.in_waiting > 0:
				data = ser.readline().decode('utf-8').strip()
				temp, humid = data.split(',')
				temp = float(temp)
				humid = float(humid)
				now = datetime.datetime.now()
				print(f"{data}")
				database.insert_sensor_data([(now, "Temperatur", temp),(now, "Luftfeuchigkeit", humid)])
	except KeyboardInterrupt:
		print("Exiting")

