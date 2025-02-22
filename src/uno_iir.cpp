/**
 * @file uno_iir.cpp
 * @brief Exemplo de utilização do filtro IIR implementado em C puro.
 *
 * Este sketch demonstra como utilizar a biblioteca de filtro IIR para processar um sinal de entrada
 * (por exemplo, de um sensor analógico) e obter a saída filtrada.
 */

 #include <Arduino.h>
 #include "iir_filter.h"
 
 // Definição dos números de coeficientes para os filtros feedforward (b) e feedback (a)
 #define NB_COEFFS 3  ///< Número de coeficientes feedforward (numerador)
 #define NA_COEFFS 3  ///< Número de coeficientes feedback (denominador)
 // Ordem do filtro = max(NB_COEFFS, NA_COEFFS) - 1.
 #define IIR_ORDER ((NB_COEFFS > NA_COEFFS ? NB_COEFFS : NA_COEFFS) - 1)
 
 // Exemplo de coeficientes para um filtro IIR (a[0] deve ser 1)
 // Estes coeficientes podem representar, por exemplo, um filtro passa-baixas
 static float bCoeffs[NB_COEFFS] = {0.2929f, 0.5858f, 0.2929f};
 static float aCoeffs[NA_COEFFS] = {1.0f, -0.0f, 0.1716f};
 
 // Vetor de estado para o filtro (tamanho = IIR_ORDER)
 static float iirState[IIR_ORDER];
 
 // Estrutura que representa o filtro IIR
 static IIRFilter myIIRFilter;
 
 void setup() {
     Serial.begin(9600);
     // Inicializa o filtro IIR com os coeficientes e o vetor de estado
     IIRFilter_init(&myIIRFilter, iirState, bCoeffs, aCoeffs, NB_COEFFS, NA_COEFFS);
 }
 
 void loop() {
     // Leitura de uma amostra do sensor (exemplo: sensor analógico) e normalização do valor
     float inputSample = analogRead(A0) / 1023.0f;
 
     // Processa a amostra através do filtro IIR
     float filteredOutput = IIRFilter_process(&myIIRFilter, inputSample);
 
     // Exibe o valor filtrado no Monitor Serial
     Serial.println(filteredOutput);
 
     // Pequeno delay para estabilizar a leitura
     delay(10);
 }