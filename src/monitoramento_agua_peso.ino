#include "HX711.h"

#define DOUT 3
#define CLK 2
#define SENSOR_AGUA_PIN A0

HX711 balanca;

const int AGUA_THRESHOLD = 300;
const int INTERVALO_LEITURA = 1500;
const int MEDIAS_PESO = 5;
const float CALIBRATION_FACTOR = -298.12; // Ajustar conforme necessário, esse foi o mais correto encontrado

bool ultimoEstadoAgua = false;

void setup() {
  Serial.begin(115200);
  
  balanca.begin(DOUT, CLK);
  balanca.set_scale(CALIBRATION_FACTOR);
  balanca.tare();
  
  pinMode(SENSOR_AGUA_PIN, INPUT);
  
  delay(2000);
  
  Serial.println("Timestamp_ms,Peso_kg,AguaPresente,LeituraSensorAgua,EstadoMudou");
}

void loop() {
  unsigned long timestamp = millis();
  
  float peso_kg = balanca.get_units(MEDIAS_PESO);
  
  int valorSensorAgua = analogRead(SENSOR_AGUA_PIN);
  bool estadoAtualAgua = (valorSensorAgua > AGUA_THRESHOLD);
  bool estadoMudou = (estadoAtualAgua != ultimoEstadoAgua);
  ultimoEstadoAgua = estadoAtualAgua;
  
  Serial.print(timestamp);
  Serial.print(",");
  Serial.print(peso_kg, 5);
  Serial.print(",");
  Serial.print(estadoAtualAgua ? "1" : "0");
  Serial.print(",");
  Serial.print(valorSensorAgua);
  Serial.print(",");
  Serial.println(estadoMudou ? "1" : "0");
  
  delay(INTERVALO_LEITURA);
}
