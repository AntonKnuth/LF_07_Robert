def handle_command(best_intent):
    command_functions[best_intent]()

def licht_an():
    print("[Befehl] Licht wird eingeschaltet")

def licht_aus():
    print("[Befehl] Licht wird ausgeschaltet")

def licht_weiß():
    print("[Befehl] Licht wird weiß")

def licht_rot():
    print("[Befehl] Licht wird rot")

def licht_gruen():
    print("[Befehl] Licht wird gruen")

def licht_blau():
    print("[Befehl] Licht wird blau")

def licht_dunkler():
    print("[Befehl] Licht wird dunkler")

def licht_heller():
    print("[Befehl] Licht wird heller")

def temperatur_abfragen():
    print("[Befehl] temperatur")

def temperatur_durchschnittlich():
    print("[Befehl] temperatur durchschnittlich")

def feuchtigkeit_abfragen():
    print("[Befehl] feuchtigkeit")

def feuchtigkeit_durchschnittlich():
    print("[Befehl] feuchtigkeit durchschnittlich")

def luftqualitaet_abfragen():
    print("[Befehl] luftqualität")

def luftqualitaet_durchschnittlich():
    print("[Befehl] luftqualität durchschnittlich")

command_functions = {
    "licht_an": licht_an,
    "licht_aus": licht_aus,
    "licht_weiß": licht_weiß,
    "licht_rot": licht_rot,
    "licht_gruen": licht_gruen,
    "licht_blau": licht_blau,
    "licht_dunkler": licht_dunkler,
    "licht_heller":licht_heller,
    "temperatur_abfragen": temperatur_abfragen,
    "temperatur_durchschnittlich": temperatur_durchschnittlich,
    "feuchtigkeit_abfragen": feuchtigkeit_abfragen,
    "feuchtigkeit_durchschnittlich": feuchtigkeit_durchschnittlich,
    "luftqualitaet_abfragen": luftqualitaet_abfragen,
    "luftqualitaet_durchschnittlich": luftqualitaet_durchschnittlich
}