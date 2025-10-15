from .database import *
import serial
import time
import datetime
import schedule

def read_Temp_and_Humid_data():
	time.sleep(2)
	with serial.Serial('/dev/ttyACM0',9600,timeout=1) as ser:
		try:
			if ser.in_waiting > 0:
				data = ser.readline().decode('utf-8').strip()
				temp, humid = data.split(',')
				temp = float(temp)
				humid = float(humid)
				temp = float(temp)
				now = datetime.datetime.now()
				print(f"{data}")
				insert_sensor_data([(now, "Temperatur", temp),(now, "Luftfeuchigkeit", humid)])
		except KeyboardInterrupt:
			print("Exiting")


#schedule.every(5).seconds.do(read_Temp_and_Humid_data())