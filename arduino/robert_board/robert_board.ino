
#include "DHT.h"
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

LiquidCrystal_PCF8574 display(LCD_ADDRESS);

RGBLED led(LED_PIN_RED, LED_PIN_GREEN, LED_PIN_BLUE);

DHT dht(DHT_PIN, DHTTYPE);

int counter =0 ;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(1000);
  while(!Serial);
  dht.begin();
  display.begin(LCD_COLUMNS, LCD_ROWS);
  display.setBacklight(BACKLIGHT);
}

void loop() {
  delay(2000);
  
  writeTempAndHumidData();
  String readInput="\n";
  if(Serial.available() > 0){
    String readInput = Serial.readStringUntil('\n');
    if (readInput !="") {
      writeOnDisplay(readInput);
    }
    delay(500);
    
  }
  
  ledColor();
}

void writeTempAndHumidData(){
  float humidity = dht.readHumidity();
  float tempInCelsius = dht.readTemperature();
  if (isnan(humidity) || isnan(tempInCelsius)){
    Serial.println(F("Failed to read from THC"));
    return;
  }
  
  Serial.print(tempInCelsius);  
  Serial.print(",");
  Serial.println(humidity);
}

String readFromRasp(){
    if(Serial.available() > 0){
      return Serial.readString();
    }
}

void writeOnDisplay(String message){
    display.clear();
    display.setCursor(0,0);
    if(message.length() > 16 && message.length() < 33){
      String mPart1 = message.substring(0,15);
      String mPart2 = message.substring(16);
     
      display.print(mPart1);
      display.setCursor(0,1);
      display.print(mPart2);
    }
    else if(message.length() < 16){
      display.print(message);
    }
    else {
      display.print("Message too big!");
    }
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
