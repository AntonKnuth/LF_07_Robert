import pyttsx3
import threading
import time

def speak(text):
	engine = pyttsx3.init()
	engine.setProperty('voice', 'de')
	engine.say(text)
	engine.runAndWait()
	engine.stop()
	
def creat_speaking_thread(text):
	return threading.Thread(target=speak,args=([text]))

