#include <Ultrasonic.h>
#include "HX711.h"

#define TRIGGER 9
#define ECHO 8
#define DOUT     A1
#define CLK      A0

Ultrasonic ultrasonic(TRIGGER, ECHO);
HX711 balanca;

float peso;

void setup() {
  Serial.begin(9600);

  balanca.begin(DOUT, CLK);
  balanca.set_scale(2280.f); // Calibrar peso, esse valor é genérico
  balanca.tare();
}

void loop() {
  
  long microsec = ultrasonic.timing();
  float distancia_cm = ultrasonic.convert(microsec, Ultrasonic::CM);

  Serial.print("Nível da agua (cm): ");
  Serial.println(distancia_cm);

  peso = balanca.get_units(5);
  Serial.print("Peso atual (kg): ");
  Serial.println(peso, 2);

  delay(1000);
}
