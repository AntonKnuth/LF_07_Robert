from modules.llm_model import *
from modules.database import *
import pyttsx3

def lampe_an():
    print("Lampe wurde eingeschaltet.")

def lampe_aus():
    print("Lampe wurde ausgeschaltet.")

def lampe_farbe(farbe):
    print(f"Lampe auf {farbe} gestellt.")

def licht_heller():
    print("Licht wurde heller gemacht.")

def licht_dunkler():
    print("Licht wurde dunkler gemacht.")

engine = pyttsx3.init()
def spreche(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

# --- Methoden ---
def temperatur_abfragen():
    wert = get_current_sensor_value("Temperatur")
    if wert is not None:
        spreche(f"Aktuelle Temperatur: {wert:.1f}°C")
    else:
        spreche("Keine Temperaturdaten verfügbar.")

def temperatur_durchschnittlich():
    wert = get_average_sensor_value("Temperatur")
    if wert is not None:
        spreche(f"Durchschnittliche Temperatur: {wert:.1f}°C")
    else:
        spreche("Keine Temperaturdaten verfügbar.")

def feuchtigkeit_abfragen():
    wert = get_current_sensor_value("Feuchtigkeit")
    if wert is not None:
        spreche(f"Aktuelle Luftfeuchtigkeit: {wert:.1f}%")
    else:
        spreche("Keine Feuchtigkeitsdaten verfügbar.")

def feuchtigkeit_durchschnittlich():
    wert = get_average_sensor_value("Feuchtigkeit")
    if wert is not None:
        spreche(f"Durchschnittliche Luftfeuchtigkeit: {wert:.1f}%")
    else:
        spreche("Keine Feuchtigkeitsdaten verfügbar.")

def luftqualitaet_abfragen():
    wert = get_current_sensor_value("Luftqualität")
    if wert is not None:
        spreche(f"Aktuelle Luftqualität: {wert:.1f} AQI")
    else:
        spreche("Keine Luftqualitätsdaten verfügbar.")

def luftqualitaet_durchschnittlich():
    wert = get_average_sensor_value("Luftqualität")
    if wert is not None:
        spreche(f"Durchschnittliche Luftqualität: {wert:.1f} AQI")
    else:
        spreche("Keine Luftqualitätsdaten verfügbar.")

def befehl_nicht_erkannt():
    spreche("Befehl nicht erkannt. Bitte wiederhole deine Eingabe.")

DURCHSCHNITT_KEYWORDS = [
    "durchschnitt", "durchschnittlich", "im schnitt",
    "im mittel", "mittelwert", "mittel", "schnitt"
]

LICHT_KEYWORDS = ["licht", "lampe"]

AN_KEYWORDS = ["an", "einschalten", "anmachen", "einmachen", "anschalten", "aktivieren"]
AUS_KEYWORDS = ["aus", "ausschalten", "ausmachen", "abschalten", "deaktivieren"]

FARBEN = {
    "weiß": ["weiß", "weiss"],
    "rot": ["rot"],
    "grün": ["grün", "gruen"],
    "blau": ["blau"]
}

FRAGEWORTE = [
    "wer", "was", "wie", "warum", "wo", "wann", "welche", "welcher",
    "welches", "wieviel", "wieviele", "wofür", "wozu"
]

def contains_any(text, keywords):
    """Hilfsfunktion: prüft, ob einer der Begriffe in text vorkommt"""
    return any(kw in text for kw in keywords)

def handle_text(text):
    text = text.lower().strip()

    if contains_any(text, LICHT_KEYWORDS):
        if contains_any(text, AN_KEYWORDS):
            lampe_an()
            return "licht_an"
        elif contains_any(text, AUS_KEYWORDS):
            lampe_aus()
            return "licht_aus"
        else:
            for farbe, keys in FARBEN.items():
                if contains_any(text, keys):
                    lampe_farbe(farbe)
                    return f"licht_{farbe}"
        if "heller" in text:
            licht_heller()
            return "licht_heller"
        elif "dunkler" in text or "dimmen" in text:
            licht_dunkler()
            return "licht_dunkler"

    if any(word in text for word in ["temperatur", "warm", "heiß", "heiss"]):
        if contains_any(text, DURCHSCHNITT_KEYWORDS):
            temperatur_durchschnittlich()
            return "temperatur_durchschnittlich"
        else:
            temperatur_abfragen()
            return "temperatur_abfragen"

    if any(word in text for word in ["feuchtigkeit", "luftfeuchtigkeit", "feuchtigkeits", "luftfeuchtigkeits"]):
        if contains_any(text, DURCHSCHNITT_KEYWORDS):
            feuchtigkeit_durchschnittlich()
            return "feuchtigkeit_durchschnittlich"
        else:
            feuchtigkeit_abfragen()
            return "feuchtigkeit_abfragen"

    if "luftqualität" in text or ("luft" in text and "qualität" in text):
        if contains_any(text, DURCHSCHNITT_KEYWORDS):
            luftqualitaet_durchschnittlich()
            return "luftqualitaet_durchschnittlich"
        else:
            luftqualitaet_abfragen()
            return "luftqualitaet_abfragen"

    if contains_any(text, FRAGEWORTE):
        print(f"[Info] Frage erkannt: '{text}' Anfrage an KI")

        #text = "halte dich etwas kürzer: \"" + text + "\""
        generate_response(text)
        return "frage_ki"
    else:
        befehl_nicht_erkannt()
        return "befehl_nicht_erkannt"

