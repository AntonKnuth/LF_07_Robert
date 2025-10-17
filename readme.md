Informationen zur Installation von Bibliotheken finden Sie unter: http://www.arduino.cc/en/Guide/Libraries

# Abhängigkeiten herunterladen
git clone https://github.com/deinname/deinprojekt.git  ## Klone das projekt über GitHub Desktop
cd deinprojekt                                         ## gehe in den Projekt ordner
python3 -m venv .venv                                  ## erstelle ein virtuelles invironment
source .venv/bin/activate                              ## aktiviere das virtuelle invironment
pip install -r requirements.txt                        ## lade alle abhängigkeiten herunter # (Depricated)


# Modell herunterladen
Bevor Sie das Programm benutzen können, müssen sie die sprach models in ihr project laden.
Lade das Vosk-Modell und Wake-Word-Modell herunter und lege es in den Ordner `models/`:
https://drive.google.com/drive/folders/1XHOXLhwmvvyDJ6p9NMgGnUrK8vX4y1ii?usp=sharing

# Text to Speech
Bevor man das Programm startet, muss man folgende Pakete via Pip3 installieren:
- pyttsx3
und folgende Pakete via apt:
- espeak-ng
- ffmpeg
- libespeak-ng1



