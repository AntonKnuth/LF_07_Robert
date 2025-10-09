
#include "DHT.h"

#define DHT_PIN 2
#define DHTTYPE DHT11

DHT dht(DHT_PIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  while(!Serial);
  Serial.println("start"); //For debugging

  dht.begin();
}

void loop() {
  delay(2000);
  float humidity = dht.readHumidity();
  float tempInCelsius = dht.readTemperature();
  if (isnan(humidity) || isnan(tempInCelsius)){
    Serial.println(F("Failed to read from DHT"));
    return;
    }
  Serial.print(F("Luftfeuchtigkeit: ")); Serial.print(humidity); Serial.println("%");
  Serial.print(F("Temperatur: ")); Serial.print(tempInCelsius); Serial.println("°C");
  
}
