#include <Arduino.h>
#include <math.h>
#include "util\filtroFir.h"

#define pinANALOG A5 // Configura o pino das ondas

#define FILTER_ORDER1 58
DigitalFilter filter1;
const double filter_taps1[FILTER_ORDER1] = {
    -0.0007229,
    -0.0009583,
    -0.0008856,
    -0.0004047,
    0.0004978,
    0.0016231,
    0.002504,
    0.0025186,
    0.0011879,
    -0.0014548,
    -0.0046255,
    -0.0068883,
    -0.0066655,
    -0.0030259,
    0.0035772,
    0.0110253,
    0.0159966,
    0.0151671,
    0.0067897,
    -0.0079726,
    -0.0246135,
    -0.0361409,
    -0.0351369,
    -0.016418,
    0.0206466,
    0.0710888,
    0.125114,
    0.1706017,
    0.1965889,
    0.1965889,
    0.1706017,
    0.125114,
    0.0710888,
    0.0206466,
    -0.016418,
    -0.0351369,
    -0.0361409,
    -0.0246135,
    -0.0079726,
    0.0067897,
    0.0151671,
    0.0159966,
    0.0110253,
    0.0035772,
    -0.0030259,
    -0.0066655,
    -0.0068883,
    -0.0046255,
    -0.0014548,
    0.0011879,
    0.0025186,
    0.002504,
    0.0016231,
    0.0004978,
    -0.0004047,
    -0.0008856,
    -0.0009583,
    -0.0007229};

#define FILTER_ORDER2 59
DigitalFilter filter2;
const double filter_taps2[FILTER_ORDER2] = {
    -0.0007150316378057743,
    -0.001075338917897092,
    -0.0013329812662954755,
    -0.00136109127576512,
    -0.0009564382146871027,
    6.976431785384702e-05,
    0.0017549824384968887,
    0.003857426474285196,
    0.005802952841707283,
    0.006758402094187532,
    0.005845030543329834,
    0.0024546500785393465,
    -0.0034163711559911866,
    -0.010926425518366829,
    -0.01834529199253539,
    -0.02326891168469186,
    -0.0230833297923932,
    -0.015591388949480874,
    0.00034580367667801326,
    0.02432558659803921,
    0.054228782856824864,
    0.08643516573654678,
    0.11641446450623477,
    0.13957803749344821,
    0.15220155074973812,
    0.15220155074973812,
    0.13957803749344824,
    0.11641446450623479,
    0.08643516573654678,
    0.05422878285682488,
    0.02432558659803922,
    0.0003458036766780133,
    -0.015591388949480875,
    -0.0230833297923932,
    -0.023268911684691865,
    -0.01834529199253539,
    -0.010926425518366834,
    -0.0034163711559911875,
    0.002454650078539348,
    0.005845030543329836,
    0.006758402094187539,
    0.005802952841707287,
    0.003857426474285196,
    0.0017549824384968896,
    6.976431785384702e-05,
    -0.0009564382146871042,
    -0.00136109127576512,
    -0.001332981266295477,
    -0.001075338917897092,
    -0.0007150316378057743,
};

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
  DigitalFilter_init(&filter1, FILTER_ORDER1, filter_taps1);
  DigitalFilter_init(&filter2, FILTER_ORDER2, filter_taps2);
}

#define TIME_DELAY_SPEED_MS 10
uint32_t previousTimePrintMS = 0;

void loop()
{
  uint32_t currentMilis = millis();
  if ((currentMilis - previousTimePrintMS) >= TIME_DELAY_SPEED_MS)
  {
    previousTimePrintMS = currentMilis;
    int16_t analog_Value = analogRead(pinANALOG);
    // DigitalFilter_put(&filter1, analog_Value);
    DigitalFilter_put(&filter2, analog_Value);

    plot<int16_t>("normal", analog_Value);
    // plot<double>("filtrado1", DigitalFilter_get(&filter1));
    plot<double>("filtrado2", DigitalFilter_get(&filter2));
  }
}
