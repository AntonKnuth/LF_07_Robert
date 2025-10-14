from modules import database
import serial
import time
import datetime
import schedule
import threading
time.sleep(2)

def read_Temp_and_Humid_data():
	with serial.Serial('/dev/ttyACM0',9600,timeout=1) as ser:
		try:
			executed = False
			while not executed:
				if ser.in_waiting > 0:
					data = ser.readline().decode('utf-8').strip()
					tempAndHumid = data.split(',')
					print(tempAndHumid)
					temp = float(tempAndHumid[0])
					humid = float(tempAndHumid[1])
					now = datetime.datetime.now()
					print(f"{data}")
					database.insert_sensor_data([(now, "Temperatur", temp),(now, "Luftfeuchigkeit", humid)])
					executed = True
		except KeyboardInterrupt:
			print("Exiting")

def create_thread():
    return threading.Thread(target=read_Temp_and_Humid_data)
