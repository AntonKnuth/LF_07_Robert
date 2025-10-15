from .database import *
from modules import database
import serial
import time
import datetime
import threading

def read_Temp_and_Humid_data():
	time.sleep(2)
	with serial.Serial('/dev/ttyACM0',9600,timeout=1) as ser:
		try:
			executed = False
			while not executed:
				if ser.in_waiting > 0:
					data = ser.readline().decode('utf-8').strip()
					tempAndHumidAndPPM = data.split(',')
					print(tempAndHumidAndPPM)
					temp = float(tempAndHumidAndPPM[0])
					humid = float(tempAndHumidAndPPM[1])
					ppm = float(tempAndHumidAndPPM[2])
					now = datetime.datetime.now()
					print(f"{data}")
					database.insert_sensor_data([(now, "Temperatur", temp),(now, "Luftfeuchigkeit", humid),(now, "PPM", ppm)])
					executed = True
		except KeyboardInterrupt:
			print("Exiting")

def create_thread():
    return threading.Thread(target=read_Temp_and_Humid_data)


#schedule.every(5).seconds.do(read_Temp_and_Humid_data())