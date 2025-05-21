#include "HX711.h"

#define DOUT     A1
#define CLK      A0

HX711 balanca;

float peso;

void setup() {
  Serial.begin(9600);

  balanca.begin(DOUT, CLK);
  balanca.set_scale(2280.f); // Calibrar peso, esse valor é genérico
  balanca.tare();
}

void loop() {

  peso = balanca.get_units(5);
  Serial.print("Peso atual (kg): ");
  Serial.println(peso, 2);

  delay(1000);
}
