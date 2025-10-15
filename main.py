from modules import voice_recognition
from modules import insert
from modules import intent_recognizer
from modules import handle_command
from modules.onnxruntime_genai import *

# einfach ohne absoluten Pfad
#intent_recognizer.init_intent_model()

def main():
    try:
        mic_stream, wake_word_detector, speech_recognizer = voice_recognition.setup_recognize_speech()
        
        while True:
            spoken_text = voice_recognition.recognize_speech(mic_stream, wake_word_detector, speech_recognizer)

            command = intent_recognizer.handle_text(spoken_text)

            if (command == "frage_ki"):
                answer = generate_response(spoken_text)
                print(answer)
                #print("KI")
            else:
                handle_command.handle_command(command)
            
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        mic_stream.close()

if __name__ == "__main__":
    main()
