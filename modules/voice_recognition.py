import pvporcupine
import pyaudio
import struct
from vosk import Model, KaldiRecognizer
import json
import time
import os

# === VOSK MODEL LADEN ===
print("Lade Vosk-Modell...")

model_path = os.path.abspath("../model/model")
model = Model(model_path)

rec = KaldiRecognizer(model, 16000)

# === HOTWORD ===
porcupine = pvporcupine.create(
  access_key='D9SyE/UBhAweDksvLLc/SvVPemxnW7KBcFyejFB42NVIIaV7V7PdAQ==',
  keyword_paths=['/home/lenn/code/speech_assistant/model/hotword/Robert_de_raspberry-pi_v3_0_0.ppn'],
  model_path='/home/lenn/code/speech_assistant/model/hotword/porcupine_params_de.pv'
)

pa = pyaudio.PyAudio()
stream = pa.open(rate=porcupine.sample_rate,
                 channels=1,
                 format=pyaudio.paInt16,
                 input=True,
                 frames_per_buffer=porcupine.frame_length)

print("Bereit. Sag 'Raspberry' oder 'Computer', um zu starten.")

while True:
    pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
    pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)
    keyword_index = porcupine.process(pcm_unpacked)

    if keyword_index >= 0:
        print("✅ Hotword erkannt! Sprich jetzt...")
        start_time = time.time()

        # Sprachaufnahme für 8 Sekunden
        frames = []
        while time.time() - start_time < 8:
            data = stream.read(4000, exception_on_overflow=False)
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                text = res.get("text", "")
                if text:
                    print("➡️ Gesagt:", text)

        print("⏹️ Aufnahme beendet. Warte auf nächstes Hotword...\n")

