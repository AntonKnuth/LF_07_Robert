import os
import onnxruntime_genai as engine

# --- Projektbasis bestimmen ---
# __file__ → Pfad zu dieser Datei (modules/code.py)
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))       # /.../projekt/modules
PROJECT_ROOT = os.path.dirname(MODULE_DIR)                    # /.../projekt

# --- Pfad zum Modell aufbauen ---
model_path = os.path.join(
    PROJECT_ROOT,
    "models",
    "onnxruntime-genai",
    "Phi-3-mini-4k-instruct-onnx",
    "cpu_and_mobile",
    "cpu-int4-rtn-block-32-acc-level-4"
)

print(f"Lade Modell von: {model_path}\n")

# --- Modell laden ---
model = engine.Model(model_path)
tokenizer = engine.Tokenizer(model)
tokenizer_stream = tokenizer.create_stream()

# --- Generierungsoptionen ---
search_options = {'max_length': 2048}

# --- Chat-Template ---
chat_tpl = '<|user|>\n{input}<|end|>\n<|assistant|>'

print("Let's chat!\n")

# --- Mehrfach-Dialogschleife (mit Ctrl+C beenden) ---
def generate_response(text):
    # text = input("> User: ")

    # if not text:
    #     print("Please, answer something")
    #     continue

    # Eingabe in Chat-Template einfügen
    prompt = chat_tpl.format(input=text)
    input_tokens = tokenizer.encode(prompt)

    # Generator konfigurieren
    gen_params = engine.GeneratorParams(model)
    gen_params.set_search_options(**search_options)
    gen_params.input_ids = input_tokens

    generator = engine.Generator(model, gen_params)

    print("\n> Assistant: ", end='', flush=True)

    try:
        # Antwort-Token für Token generieren und ausgeben
        while not generator.is_done():
            generator.compute_logits()
            generator.generate_next_token()
            next_token = generator.get_next_tokens()[0]
            #token_text = 
            print(tokenizer_stream.decode(next_token), end='', flush=True)

        print('\n')

    except KeyboardInterrupt:
        print("\nCtrl+C pressed, break\n")

    # Generator löschen
    del generator
