
#include "DHT.h"

#define DHT_PIN 2
#define DHTTYPE DHT11

DHT dht(DHT_PIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  while(!Serial);
  dht.begin();
}

void loop() {
  delay(5000);
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
