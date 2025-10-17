# serial_port.py
import serial

# Serial-Port einmalig öffnen
# Pfad anpassen falls nötig, z.B. '/dev/ttyACM0'
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
