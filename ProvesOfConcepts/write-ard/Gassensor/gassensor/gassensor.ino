#include "MQ135.h"

MQ135 gasSensor = MQ135(0);
float rzeroMin;
float rzeroMax;

void setup() {
  rzeroMin = 10000;
  rzeroMax = 0;
  Serial.begin(9600);
  while(!Serial);

}

void loop() {
  float ppm = gasSensor.getPPM();
  Serial.print("ppm: ");
  Serial.println(ppm);
  delay(5000);
}
