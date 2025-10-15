
#include "DHT.h"
#include "MQ135.h"
//#include "Arduino.h"
#include "LiquidCrystal_PCF8574.h"
#include <Transition.h>
#include <RGB.h>
#include <RGBLED.h>
#include "RGBLED.h"

//#define LCD_ADDRESS 0x3F
#define LCD_ADDRESS 0x27

#define DHT_PIN 2
#define LED_PIN_BLUE 5
#define LED_PIN_GREEN 6
#define LED_PIN_RED 9

#define DHTTYPE DHT11

#define LCD_ROWS 2
#define LCD_COLUMNS 16
#define SCROLL_DELAY 150
#define BACKLIGHT 255

int r = 255;
int g = 255;
int b = 255;

LiquidCrystal_PCF8574 display(LCD_ADDRESS);

MQ135 gasSensor = MQ135(0, (150*1.2));

RGBLED led(LED_PIN_RED, LED_PIN_GREEN, LED_PIN_BLUE);

DHT dht(DHT_PIN, DHTTYPE);

float rzeroMin;
float rzeroMax;
int counter =0 ;
bool read=false;

void setup() {
  rzeroMin = 10000;
  rzeroMax = 0;
  Serial.begin(9600);
  Serial.setTimeout(1000);
  while(!Serial);
  dht.begin();
  display.begin(LCD_COLUMNS, LCD_ROWS);
  display.setBacklight(BACKLIGHT);
}

void loop() {
  delay(2000);
 if(Serial.available() > 0 && read){
  String received = readFromRasp();
  setLed(received);
    Serial.println(received);
    read=false;
  }
  else{
  
  
  String sensorData = writeTempAndHumidandPpmData();
  //String readInput="\n";
  /*if(Serial.available() > 0){
    String readInput = Serial.readStringUntil('\n');
    if (readInput !="") {
      writeOnDisplay(readInput);
    }
    delay(500);
    
  }*/

  writeOnDisplay(sensorData);
  
  //ledColor();
  read=true;
  }
}

String writeTempAndHumidandPpmData(){
  float ppm = gasSensor.getPPM();
  float humidity = dht.readHumidity();
  float tempInCelsius = dht.readTemperature();
  if (isnan(humidity) || isnan(tempInCelsius)){
    Serial.println(F("Failed to read from THC"));
    return;
  }
  
  Serial.print(tempInCelsius);  
  Serial.print(",");
  Serial.print(humidity);
  Serial.print(",");
  Serial.println(ppm);
  return String(tempInCelsius)+","+String(humidity)+","+String(ppm);
}

String readFromRasp(){
    if(Serial.available() > 0){
      return Serial.readStringUntil('\n');
    }
}

void writeOnDisplay(String message){
  int sep1 = message.indexOf(',');
  int sep2 = message.indexOf(',', sep1+1);
  String temp = message.substring(0, sep1);
  String humid = message.substring(sep1 +1, sep2);
  String ppm = message.substring(sep2+1);

  resetDisplay();
  outputData("Temp:", temp, ("\xDF""C"));
  display.setCursor(0,1);
  outputData("Humid:", humid, "%");
  delay(2000);
  resetDisplay();
  outputData("Luftq.:", ppm, "ppm");
}
void ledColor(){
  led.setRGB(255, 0, 0);
  delay(500);
  led.setRGB(100,0,0);
  delay(500);
  led.setRGB(0, 255, 0);
  delay(500);
  led.setRGB(0,100,0);
  delay(500);
  led.setRGB(0, 0, 255);
  delay(500);
  led.setRGB(0,0,100);
  delay(500);
  led.setRGB(255, 255, 255);
  delay(500);
  led.setRGB(100, 100, 100);
}

void outputData(String prefix, String data, String suffix){
  display.print(prefix);
  display.print(data);
  display.print(suffix);
}

void resetDisplay(){
  display.clear();
  display.setCursor(0,0);
}

void setLed(String command){
  if(command == "LichtAn"){
    r = 255;
    g = 255;
    b = 255;
    showColor(r,g,b);
  }
  if(command == "Blue"){
    r = 0;
    g = 0;
    b = 255;
    showColor(r,g,b);
  }
    
   if(command == "Darker"){
    r=substractRGB(r);
    g=substractRGB(g);
    b=substractRGB(b);
    showColor(r,g,b);
    }
  }
  
void showColor(int r, int g, int b){
  led.setRGB(r, g, b);
  }
int substractRGB(int col){
  int newCol = col+1 - 32;
  if( newCol< 0)
    return 0;
  return newCol;
  }
