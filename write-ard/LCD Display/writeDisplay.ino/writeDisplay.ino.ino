//#include "Arduino.h"
#include "LiquidCrystal_PCF8574.h"

//#define LCD_ADDRESS 0x3F
#define LCD_ADDRESS 0x27

int counter =0 ;

LiquidCrystal_PCF8574 display(LCD_ADDRESS);

#define LCD_ROWS 2
#define LCD_COLUMNS 16
#define SCOLL_DELAY 150
#define BACKLIGHT 255

void setup() {
  Serial.begin(9600);
  while(!Serial);

  display.begin(LCD_COLUMNS, LCD_ROWS);

}

void loop() {
  display.clear();
  if(counter%2==0)
    display.print("Moin!");
  else
    display.print("Hallo!"); 
    counter++;
  delay(4000);

}
