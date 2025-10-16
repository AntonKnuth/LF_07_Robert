from modules import voice_recognition
from modules import insert
from modules import Speech
from modules import exceptions
from fastapi import BackgroundTasks, FastAPI
import threading
from modules import intent_recognizer
from modules import handle_command
from modules.llm_model import *

# einfach ohne absoluten Pfad
#intent_recognizer.init_intent_model()

def main():
    try:
        
        mic_stream, wake_word_detector, speech_recognizer = voice_recognition.setup_recognize_speech()
        
        while True:
            spoken_text = voice_recognition.recognize_speech(mic_stream, wake_word_detector, speech_recognizer)

            intent_recognizer.handle_text(spoken_text)

            # if (command == "frage_ki"):
            #     answer = generate_response(spoken_text)
            #     print(answer)
            #     #print("KI")
            # else:
            #     handle_command.handle_command(command)

            #voice_thread = create_voice_thread()
            #data_thread = insert.create_thread()
            #speaking_thread = Speech.creat_speaking_thread("Irgendein Text lul")
            #voice_thread.start()
            #data_thread.start()
            #speaking_thread.start()
            #data_thread.join()
            #voice_thread.join()
            #speaking_thread.join()
    except KeyboardInterrupt:
        pass
            
            
    except Exception as e:
        print(f"{e}")
        #exceptions.writeException(type(e).__name__)
        raise
    finally:
        mic_stream.close()

if __name__ == "__main__":
    main()


#def create_voice_thread():
    #return threading.Thread(target=voice_recognition.recognize_speech,arg=(mic_stream, wake_word_detector, speech_recognizer))
