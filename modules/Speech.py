import pyttsx3
import threading
import time

def speak(text):
	engine = pyttsx3.init()
	engine.setProperty('voice', 'de')
	engine.say(text)
	engine.runAndWait()
	time.sleep(1)
	
def creat_speaking_thread():
	return threading.Thread(target=speak,args=(['Guten Morgen, ich bin Robert']))

