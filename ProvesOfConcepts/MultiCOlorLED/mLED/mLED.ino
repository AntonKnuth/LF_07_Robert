#include <Transition.h>
#include <RGB.h>
#include <RGBLED.h>
#include "RGBLED.h"

#define LED_PIN_BLUE 5
#define LED_PIN_GREEN 6
#define LED_PIN_RED 9

RGBLED led(LED_PIN_RED, LED_PIN_GREEN, LED_PIN_BLUE);

void setup() {
  Serial.begin(9600);
  while(!Serial);

}

void loop() {
  led.setRGB(255, 0, 0);
  delay(1000);
  led.setRGB(0, 255, 0);
  delay(1000);
  led.setRGB(0, 0, 255);
  delay(1000);
  led.setRGB(255, 255, 255);
  delay(5000);

}
