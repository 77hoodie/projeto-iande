#include "Ultrasonic.h"
#include "HX711.h"

#define TRIG_PIN 9
#define ECHO_PIN 8
#define RELAY_PIN 7
#define DOUT  A1
#define CLK   A0

HX711 balanca;

long duration;
int distance;
int nivelMax = 10;
int nivelMin = 100;

float peso;
float pesoMax = 10.0;

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);

  Serial.begin(9600);

  balanca.begin(DOUT, CLK);
  balanca.set_scale(2280.f);
  balanca.tare();
}

void loop() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  duration = pulseIn(ECHO_PIN, HIGH);
  distance = duration * 0.034 / 2;

  Serial.print("Nivel da agua (cm): ");
  Serial.println(distance);

  if (distance <= nivelMax) {
    digitalWrite(RELAY_PIN, LOW);
  } else if (distance >= nivelMin) {
    digitalWrite(RELAY_PIN, HIGH);
  }

  peso = balanca.get_units(5);

  Serial.print("Peso atual (kg): ");
  Serial.println(peso);

  if (peso >= pesoMax) {
    Serial.println("Peso máximo atingido");
  }

  delay(1000);
}
