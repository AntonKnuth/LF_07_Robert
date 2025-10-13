import pvporcupine
import pyaudio
import struct
from vosk import Model, KaldiRecognizer
import json
import time
import os

def setup_recognize_speech():
    mic_stream = get_microphone_stream()
    wake_word_detector = get_wake_word_detector()
    speech_recognizer = get_speech_recognizer()

    return mic_stream, wake_word_detector, speech_recognizer
    

def recognize_speech(mic_stream, wake_word_detector, speech_recognizer) -> str:
    print("Bereit. Sag 'Robert', um zu starten.")

    detect_wake_word(wake_word_detector, mic_stream)

    print("Wake-Word erkannt! Sprich jetzt:")

    captured_text = capture_spoken_text(speech_recognizer, mic_stream)

    print(captured_text)
    print("Aufnahme beendet.\n")

    return captured_text
    


def get_wake_word_detector():
    detector = pvporcupine.create(
        access_key='D9SyE/UBhAweDksvLLc/SvVPemxnW7KBcFyejFB42NVIIaV7V7PdAQ==',
        keyword_paths=['/home/lenn/code/speech_assistant/model/hotword/Robert_de_raspberry-pi_v3_0_0.ppn'],
        model_path='/home/lenn/code/speech_assistant/model/hotword/porcupine_params_de.pv'
    )

    return detector

def get_speech_recognizer(model_dir: str = "model/model_test", sample_rate: int = 16000):
    model_path = os.path.abspath(model_dir)
    model = Model(model_path)
    rec = KaldiRecognizer(model, sample_rate)

    return rec

def get_microphone_stream(sample_rate: int = 16000, frame_length: int = 512):
    pa = pyaudio.PyAudio()
    stream = pa.open(rate=sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=frame_length)
    
    return stream

def detect_wake_word(detector, stream):
    while True:
        pcm = stream.read(detector.frame_length, exception_on_overflow=False)
        pcm_unpacked = struct.unpack_from("h" * detector.frame_length, pcm)
        keyword_index = detector.process(pcm_unpacked)

        if keyword_index >= 0:
            break

def capture_spoken_text(recognizer, stream, silence_threshold=4) -> str:
    last_speech_time = time.time()
    collected_text = ""

    while time.time() - last_speech_time < silence_threshold:
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            res = json.loads(recognizer.Result())
            text = res.get("text", "")
            if text:
                print(text)
                collected_text += " " + text
                last_speech_time = time.time()

    return collected_text.strip()

