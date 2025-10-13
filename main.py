from modules import voice_recognition
from modules import insert

def main():
    try:
        mic_stream, wake_word_detector, speech_recognizer = voice_recognition.setup_recognize_speech()
        
        dht_stream = insert
        
        while True:
            print(voice_recognition.recognize_speech(mic_stream, wake_word_detector, speech_recognizer))
            dht_stream.read_Temp_and_Humid_data()
    
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        mic_stream.close()

if __name__ == "__main__":
    main()
