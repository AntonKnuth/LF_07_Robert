//#include "Arduino.h"
#include "LiquidCrystal_PCF8574.h"

//#define LCD_ADDRESS 0x3F
#define LCD_ADDRESS 0x27

int counter =0 ;



#define LCD_ROWS 2
#define LCD_COLUMNS 16
#define SCROLL_DELAY 150
#define BACKLIGHT 255

LiquidCrystal_PCF8574 display(LCD_ADDRESS);

void setup() {
  Serial.begin(9600);
  while(!Serial);

  display.begin(LCD_COLUMNS, LCD_ROWS);
  display.setBacklight(BACKLIGHT);

}

void loop() {
  display.clear();
  if(counter%2==0){
    //Setze den Cursor auf die obere Reihe
    display.setCursor(0,0);
    display.print("Moin!");
   
  }
  else{
    //Setze den Cursor auf die untere Reihe
    display.setCursor(0,1);
    display.print("Hallo!");
  } 
    counter++;
  delay(4000);

}
