#ifndef IIR_FILTER_H
#define IIR_FILTER_H

#include <stdint.h>

/**
 * @file iir_filter.h
 * @brief Biblioteca de filtro digital IIR em C puro.
 *
 * Este arquivo contém a declaração das funções e da estrutura utilizada para implementar
 * um filtro digital do tipo IIR (Infinite Impulse Response) utilizando arrays de tamanho fixo,
 * sem o uso de alocação dinâmica de memória.
 */

/**
 * @brief Estrutura que representa um filtro IIR.
 *
 * A estrutura IIRFilter armazena os coeficientes do filtro (feedforward e feedback) e o vetor de
 * estado interno, utilizado para armazenar as amostras intermediárias. O vetor de estado deve ser
 * alocado estaticamente com tamanho igual a max(nb, na)-1, onde nb e na são os números de coeficientes
 * dos filtros feedforward (numerador) e feedback (denominador), respectivamente.
 *
 * Nota: O coeficiente a[0] deve ser 1.
 */
typedef struct {
    float *state;   ///< Ponteiro para o array que armazena o vetor de estado.
    float *b;       ///< Ponteiro para o array de coeficientes feedforward (numerador).
    float *a;       ///< Ponteiro para o array de coeficientes feedback (denominador). a[0] deve ser 1.
    uint8_t nb;     ///< Número de coeficientes feedforward (numerador).
    uint8_t na;     ///< Número de coeficientes feedback (denominador).
} IIRFilter;

/**
 * @brief Inicializa o filtro IIR.
 *
 * Esta função inicializa a estrutura IIRFilter, definindo os coeficientes, zerando o vetor de estado
 * e configurando os números de coeficientes. Os arrays para os coeficientes e o vetor de estado devem ser
 * alocados estaticamente.
 *
 * @param filter Ponteiro para a estrutura IIRFilter a ser inicializada.
 * @param state Array para armazenar o vetor de estado. Deve ter tamanho igual a max(nb, na)-1 elementos.
 * @param b Array com os coeficientes feedforward (numerador). Deve ter nb elementos.
 * @param a Array com os coeficientes feedback (denominador). Deve ter na elementos. a[0] deve ser 1.
 * @param nb Número de coeficientes feedforward.
 * @param na Número de coeficientes feedback.
 */
void IIRFilter_init(IIRFilter *filter, float *state, float *b, float *a, uint8_t nb, uint8_t na){
    filter->state = state;
    filter->b = b;
    filter->a = a;
    filter->nb = nb;
    filter->na = na;
    
    // Calcula a ordem do filtro: número de estados = max(nb, na) - 1.
    uint8_t order = (nb > na ? nb : na) - 1;
    
    // Inicializa o vetor de estado com zeros.
    for (uint8_t i = 0; i < order; i++) {
        filter->state[i] = 0.0f;
    }
}

/**
 * @brief Processa uma nova amostra de entrada pelo filtro IIR.
 *
 * Utiliza o algoritmo Direct Form II transposto para calcular a saída filtrada.
 *
 * @param filter Ponteiro para a estrutura IIRFilter.
 * @param input Nova amostra de entrada.
 * @return float Valor filtrado resultante da operação.
 */
float IIRFilter_process(IIRFilter *filter, float input) {
    // Calcula a ordem do filtro (número de estados) = max(nb, na) - 1.
    uint8_t order = (filter->nb > filter->na ? filter->nb : filter->na) - 1;
    
    float output;
    // Se não há estados (filtro de ordem 0), a saída é simplesmente b[0]*input.
    if (order == 0) {
        output = filter->b[0] * input;
    } else {
        // Calcula a saída do filtro: y = b[0]*input + state[0]
        output = filter->b[0] * input + filter->state[0];
    
        // Atualiza o vetor de estado.
        // Para i de 0 até order-2, atualiza:
        //   state[i] = state[i+1] + (b[i+1]*input) - (a[i+1]*output)
        for (uint8_t i = 0; i < order - 1; i++) {
            float b_val = (i + 1 < filter->nb) ? filter->b[i + 1] : 0.0f;
            float a_val = (i + 1 < filter->na) ? filter->a[i + 1] : 0.0f;
            filter->state[i] = filter->state[i + 1] + b_val * input - a_val * output;
        }
        // Atualiza o último elemento do vetor de estado.
        float b_last = (order < filter->nb) ? filter->b[order] : 0.0f;
        float a_last = (order < filter->na) ? filter->a[order] : 0.0f;
        filter->state[order - 1] = b_last * input - a_last * output;
    }
    
    return output;
}

#endif // IIR_FILTER_H
