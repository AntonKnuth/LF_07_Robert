from modules import voice_recognition
from modules import insert
from fastapi import BackgroundTasks, FastAPI
import threading

def main():
    try:
        
        mic_stream, wake_word_detector, speech_recognizer = voice_recognition.setup_recognize_speech()
        
        while True:
            #print(voice_recognition.recognize_speech(mic_stream, wake_word_detector, speech_recognizer))
            voice_thread = create_voice_thread()
            voice_thread.start()
            voice_thread.join()
            thread = insert.create_thread()
            thread.start()
            thread.join()
            
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        mic_stream.close()

if __name__ == "__main__":
    main()


def create_voice_thread():
    return threading.Thread(target=voice_recognition.recognize_speech,arg=(mic_stream, wake_word_detector, speech_recognizer))
