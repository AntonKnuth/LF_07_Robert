
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
  while(!Serial);
  dht.begin();
  display.begin(LCD_COLUMNS, LCD_ROWS);
  display.setBacklight(BACKLIGHT);
}

void loop() {
  delay(5000);
  
  writeTempAndHumidData();
  
  counter = writeOnDisplay("XD", counter);

  readFromRasp();
  
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

void readFromRasp(){
  if(Serial.available() > 0){
    String received = Serial.readStringUntil('\\n');
    Serial.println(received);
  }
}

int writeOnDisplay(String message, int counter){
    display.clear();
  if(counter%2==0){
    //Setze den Cursor auf die obere Reihe
    display.setCursor(0,0);
    display.print("Moin!");
   
  }
  else{
    //Setze den Cursor auf die untere Reihe
    display.setCursor(0,1);
    display.print(message);
  }
  counter++;
  if(counter>1)
    return 0;
  return counter;
}

void ledColor(){
  led.setRGB(255, 0, 0);
  delay(1000);
  led.setRGB(0, 255, 0);
  delay(1000);
  led.setRGB(0, 0, 255);
  delay(1000);
  led.setRGB(255, 255, 255);
}
