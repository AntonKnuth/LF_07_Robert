from modules import database
from modules.serial_port import ser  # globaler Port
import time
import datetime
import threading
import pyttsx3
import serial

# Text-to-Speech Engine initialisieren
tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 160)
has_not_spoken = True


def speak_safely(text):
    """Spricht Text nur, wenn gerade keine andere Ausgabe läuft"""
    try:
        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception as e:
        print(f"TTS Fehler: {e}")

def check_environment_conditions(temp, humid, ppm):
    """Prüft die Sensorwerte und gibt ggf. Warnungen aus"""
    messages = []

    if temp < 15:
        messages.append("Zu kalt!")
        has_not_spoken = True
    elif temp > 30:
        messages.append("Zu heiss!")
        has_not_spoken = True
    
    if humid < 30:
        messages.append("Luft zu trocken!")
        has_not_spoken = True
    elif humid > 70:
        messages.append("Luft zu feucht!")
        has_not_spoken = True

    if ppm > 1500:
        messages.append("Schlechte Luft!")
        has_not_spoken = True

    for msg in messages:
        if (has_not_spoken):
            print(f"{msg}")
            speak_safely(msg)
            has_not_spoken = False

    return " / ".join(messages) if messages else ""

def read_Temp_and_Humid_data():
    """Liest kontinuierlich Daten vom Arduino und schreibt sie in die DB"""
    print("Warte auf Arduino-Daten...")
    time.sleep(2)

    while True:
        try:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8', errors='ignore').strip()
                if not data:
                    continue

                

                
                parts = data.split(',')
                if len(parts) != 3:
                    
                    continue
                
                try:
                    
                    temp_str = parts[0].replace("SENSOR:", "").strip()
                    temp = float(temp_str)
                    humid = float(parts[1].strip())
                    ppm = float(parts[2].strip())
                except ValueError:
                    continue

                now = datetime.datetime.now()

                database.insert_sensor_data([
                    (now, "Temperatur", temp),
                    (now, "Luftfeuchtigkeit", humid),
                    (now, "PPM", ppm)
                ])

                warning_message = check_environment_conditions(temp, humid, ppm)

                if warning_message:
                    print(f"Hinweis: {warning_message}")
                    try:
                        ser.write(f"{warning_message}\n".encode('utf-8'))
                    except Exception as e:
                        print(f"Fehler beim Senden an Arduino: {e}")

            time.sleep(1)

        except serial.SerialException as e:
            print(f"Serieller Fehler: {e}")
            time.sleep(2)
        except Exception as e:
            print(f"Unerwarteter Fehler: {e}")
            time.sleep(2)

def create_thread():
    """Erstellt den Thread für kontinuierliches Auslesen"""
    return threading.Thread(target=read_Temp_and_Humid_data, daemon=True)
