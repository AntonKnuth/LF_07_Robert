#include "DHT.h"
#include "MQ135.h"
#include "LiquidCrystal_PCF8574.h"
#include "RGBLED.h"

//#define LCD_ADDRESS 0x3F /*if the define below does not work replace the line below with this line*/
#define LCD_ADDRESS 0x27

#define DHT_PIN 2
#define LED_PIN_BLUE 5
#define LED_PIN_GREEN 6
#define LED_PIN_RED 9

#define DHTTYPE DHT11

#define LCD_ROWS 2
#define LCD_COLUMNS 16
#define BACKLIGHT 255

int r = 0;
int g = 0;
int b = 0;

LiquidCrystal_PCF8574 display(LCD_ADDRESS);
MQ135 gasSensor = MQ135(0, (150*1.2));
RGBLED led(LED_PIN_RED, LED_PIN_GREEN, LED_PIN_BLUE);
DHT dht(DHT_PIN, DHTTYPE);

bool readFlag = false;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  dht.begin();
  display.begin(LCD_COLUMNS, LCD_ROWS);
  display.setBacklight(BACKLIGHT);

  // LED initial aus
  showColor(r, g, b);
}

void loop() {
  delay(2000);

  // Prüfen auf serielle Befehle
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    handleSerialCommand(command); // LED nur hier ändern
  }

  // Sensorwerte auslesen
  if (readFlag) {
    String sensorData = writeTempAndHumidandPpmData();
    writeOnDisplay(sensorData);
    readFlag = false;
  } else {
    readFlag = true;
  }
}

String writeTempAndHumidandPpmData() {
  float ppm = gasSensor.getPPM();
  float humidity = dht.readHumidity();
  float tempInCelsius = dht.readTemperature();

  if (isnan(humidity) || isnan(tempInCelsius)) {
    Serial.println(F("Failed to read from THC"));
    return "";
  }

  // Sensorwerte mit Prefix senden
  Serial.println("SENSOR:" + String(tempInCelsius) + "," + String(humidity) + "," + String(ppm));
  return String(tempInCelsius) + "," + String(humidity) + "," + String(ppm);
}

void writeOnDisplay(String message) {
  int sep1 = message.indexOf(',');
  int sep2 = message.indexOf(',', sep1 + 1);
  String temp = message.substring(0, sep1);
  String humid = message.substring(sep1 + 1, sep2);
  String ppm = message.substring(sep2 + 1);

  resetDisplay();
  outputData("Temp:", temp, ("\xDF""C"));
  display.setCursor(0,1);
  outputData("Humid:", humid, "%");
  delay(2000);
  resetDisplay();
  outputData("Luftqualitaet:", "", "");
  display.setCursor(0,1);
  outputData("", ppm, "ppm");

  // Falls Python eine Warnung schickt:
  if (Serial.available() > 0) {
    String warning = Serial.readStringUntil('\n');
    
    resetDisplay();
    if(warning.length() > 16)
    {
      String part1 = warning.substring(0,16);
      String part2 = warning.substring(17,32);
      display.print(part1);
      display.setCursor(0,1);
      display.print(part2);
      delay(3000);
      return;
      
      }
    display.print(warning);
    delay(3000);
  }
}


void outputData(String prefix, String data, String suffix) {
  display.print(prefix);
  display.print(data);
  display.print(suffix);
}

void resetDisplay() {
  display.clear();
  display.setCursor(0,0);
}

void showColor(int rVal, int gVal, int bVal) {
  led.setRGB(rVal, gVal, bVal);
}

int substractRGB(int col) {
  int newCol = col + 1 - 80;
  if (newCol < 0) return 0;
  return newCol;
}

void handleSerialCommand(String cmd) {
  cmd.toLowerCase();

  if (cmd == "lichtan" || cmd == "led_on") {
    r = 255; g = 255; b = 255;
  } else if (cmd == "lichtaus" || cmd == "led_off") {
    r = 0; g = 0; b = 0;
  } else if (cmd == "rot") {
    r = 255; g = 0; b = 0;
  } else if (cmd == "grün") {
    r = 0; g = 255; b = 0;
  } else if (cmd == "blau") {
    r = 0; g = 0; b = 255;
    } else if (cmd == "weiß") {
    r = 255; g = 255; b = 255;
  } else if (cmd == "darker") {
    r = substractRGB(r);
    g = substractRGB(g);
    b = substractRGB(b);
  } else if (cmd == "brighter") {
    r = min(r + 80, 255);
    g = min(g + 80, 255);
    b = min(b + 80, 255);
  }

  // LED aktualisieren
  showColor(r, g, b);

  // Bestätigung senden
  Serial.println("Command executed: " + cmd);
}