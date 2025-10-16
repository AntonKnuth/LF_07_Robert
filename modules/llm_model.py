import os
import threading
import queue
import time
import onnxruntime_genai as engine
import pyttsx3

# -----------------------------------------------------
# 🔊 Text-to-Speech im Hintergrund (nicht blockierend)
# -----------------------------------------------------
def tts_worker(text_queue):
    """Liest Textstücke aus der Queue und spricht sie mit pyttsx3"""
    engine_tts = pyttsx3.init()

    # Deutsche Stimme auswählen (wenn vorhanden)
    for v in engine_tts.getProperty('voices'):
        if "de" in v.id.lower() or "german" in v.name.lower():
            engine_tts.setProperty('voice', v.id)
            break

    engine_tts.setProperty('rate', 180)
    engine_tts.setProperty('volume', 1.0)

    buffer = ""
    last_speak_time = time.time()

    while True:
        try:
            chunk = text_queue.get(timeout=0.5)

            # Thread beenden, wenn STOP-Signal kommt
            if chunk == "__STOP__":
                break

            if not chunk.strip():
                continue

            buffer += chunk

            # Satzweise oder nach Zeitintervall sprechen
            if any(p in buffer for p in [".", "?", "!", "\n"]) or (time.time() - last_speak_time > 2):
                if buffer.strip():
                    engine_tts.say(buffer.strip())
                    engine_tts.runAndWait()
                buffer = ""
                last_speak_time = time.time()

        except queue.Empty:
            continue


# -----------------------------------------------------
# 🧩 KI-Modell laden
# -----------------------------------------------------
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(MODULE_DIR)

model_path = os.path.join(
    PROJECT_ROOT,
    "models",
    "onnxruntime-genai",
    "Phi-3-mini-4k-instruct-onnx",
    "cpu_and_mobile",
    "cpu-int4-rtn-block-32-acc-level-4"
)

print(f"Lade Modell von: {model_path}\n")

model = engine.Model(model_path)
tokenizer = engine.Tokenizer(model)
tokenizer_stream = tokenizer.create_stream()

search_options = {'max_length': 2048}
chat_tpl = '<|user|>\n{input}<|end|>\n<|assistant|>'

print("Let's chat!\n")


# -----------------------------------------------------
# 🚀 Antwort generieren + Streaming-TTS
# -----------------------------------------------------
def generate_response(text):
    """
    Erzeugt eine Antwort vom Modell und liest sie parallel per TTS vor.
    Englische Hinweise wie '(Note: ...)', '**', 'As an AI model', oder
    'Note to the user:' werden direkt vor der TTS-Ausgabe herausgefiltert.
    """
    prompt = chat_tpl.format(input=text)
    input_tokens = tokenizer.encode(prompt)

    gen_params = engine.GeneratorParams(model)
    gen_params.set_search_options(**search_options)
    gen_params.input_ids = input_tokens

    generator = engine.Generator(model, gen_params)

    print("\n> Assistant: ", end='', flush=True)

    response_text = ""
    text_queue = queue.Queue()

    # Hintergrundthread starten für TTS
    tts_thread = threading.Thread(target=tts_worker, args=(text_queue,), daemon=True)
    tts_thread.start()

    try:
        while not generator.is_done():
            generator.compute_logits()
            generator.generate_next_token()
            next_token = generator.get_next_tokens()[0]
            decoded = tokenizer_stream.decode(next_token)

            # --- Englische Hinweise direkt filtern ---
            lower_decoded = decoded.strip().lower()
            if (
                lower_decoded.startswith("(note:") or
                "**" in lower_decoded or
                "note: " in lower_decoded or
                "as an ai" in lower_decoded or
                "note to the user:" in lower_decoded
            ):
                continue  # nicht an TTS oder response_text weitergeben

            # Text ausgeben und gleichzeitig an TTS schicken
            print(decoded, end='', flush=True)
            response_text += decoded
            text_queue.put(decoded)

        print("\n")

    except KeyboardInterrupt:
        print("\n⛔ Abgebrochen durch Benutzer.")
    finally:
        # Stop-Signal an TTS schicken und Generator schließen
        text_queue.put("__STOP__")
        tts_thread.join()
        del generator

    # Optional: Restbereinigung (Leerzeichen, Zeilenumbrüche)
    response_text = response_text.strip()

    return response_text