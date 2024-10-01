#include <Arduino.h>
#include <math.h>
#include "util\filtroFir.h"

#define pinANALOG A5 // Configura o pino das ondas

#define FILTER_ORDER1 50
DigitalFilter filter1;
const double filter_taps1[FILTER_ORDER1] = {
    4.516054525870999e-05,
    0.0009142054619561833,
    0.0012953896783814676,
    0.0006701264020523413,
    -0.0010061328936756483,
    -0.0027415736303675366,
    -0.0027383246973091066,
    0.00014295225857527812,
    0.004643501894501436,
    0.007022781895771855,
    0.003679867564362992,
    -0.0050001376771318575,
    -0.013077950202782325,
    -0.012409139597132307,
    0.0003627099644714731,
    0.018516051147453732,
    0.027332581877827434,
    0.014351815698230666,
    -0.018440950386355185,
    -0.05024494998675938,
    -0.05075861114965704,
    0.0005389579398013344,
    0.09736941733570999,
    0.20461223885506052,
    0.27492001170175484,
    0.27492001170175484,
    0.20461223885506055,
    0.09736941733571,
    0.0005389579398013344,
    -0.05075861114965705,
    -0.050244949986759394,
    -0.01844095038635519,
    0.014351815698230668,
    0.027332581877827434,
    0.01851605114745374,
    0.0003627099644714731,
    -0.012409139597132314,
    -0.013077950202782327,
    -0.005000137677131861,
    0.003679867564362994,
    0.007022781895771863,
    0.0046435018945014395,
    0.00014295225857527812,
    -0.002738324697309108,
    -0.0027415736303675366,
    -0.0010061328936756498,
    0.0006701264020523413,
    0.0012953896783814691,
    0.0009142054619561833,
    4.516054525870999e-05};

template <typename T>
void plot(const char *varName, T y, const char *unit = NULL)
{
  Serial.print(">");
  Serial.print(varName);
  Serial.print(":");
  Serial.print(millis());
  Serial.print(":");
  Serial.print(y);
  Serial.print(unit != NULL ? "§" : "");
  Serial.print(unit != NULL ? unit : "");
  Serial.println("|g");
}

void setup()
{ // Codigo de configuração
  Serial.begin(9600);
  pinMode(pinANALOG, INPUT);
  DigitalFilter_init(&filter1,FILTER_ORDER1,filter_taps1);  
}

#define TIME_DELAY_SPEED_MS 1
uint32_t previousTimePrintMS = 0;

void loop()
{
  uint32_t currentMilis = millis();
  if ((currentMilis - previousTimePrintMS) >= TIME_DELAY_SPEED_MS)
  {
    previousTimePrintMS = currentMilis;
    int16_t analog_Value = analogRead(pinANALOG);
    plot<int16_t>("normal", analog_Value);      
    DigitalFilter_put(&filter1, analog_Value);
    plot<double>("filtrado", DigitalFilter_get(&filter1));
  }
}
