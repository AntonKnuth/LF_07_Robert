import pyttsx3

engine = pyttsx3.init()
engine.setProperty('voice', 'de')
engine.say("Guten Morgen, ich bin Robert")
engine.runAndWait()
