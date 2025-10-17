import threading
import time
from modules import voice_recognition, insert, intent_recognizer

def run_data_insert():
    while True:
        insert.read_Temp_and_Humid_data()  # benutzt den globalen Serial-Port
        time.sleep(0.1) 

def main():
    mic_stream, wake_word_detector, speech_recognizer = voice_recognition.setup_recognize_speech()
    
    # Hintergrund-Thread für Arduino-Daten starten
    data_thread = threading.Thread(target=run_data_insert, daemon=True)
    data_thread.start()
    
    try:
        while True:
            spoken_text = voice_recognition.recognize_speech(
                mic_stream, wake_word_detector, speech_recognizer
            )
            intent_recognizer.handle_text(spoken_text)
            
    except KeyboardInterrupt:
        print("Programm beendet")
    finally:
        mic_stream.close()

if __name__ == "__main__":
    main()
