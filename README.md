# Filtros Digitais: FIR e IIR & Direct Form II Transposed Filter Implementation

Este repositório apresenta uma visão geral sobre filtros digitais, com foco em implementações de filtros FIR e IIR para sistemas embarcados (como o Arduino). Além disso, inclui uma explicação detalhada sobre o algoritmo **Direct Form II Transposto** para filtros IIR, ressaltando sua eficiência no uso de memória e robustez numérica. Aqui você encontrará explicações conceituais, diagramas ilustrativos e exemplos de código em C puro, sem uso de alocação dinâmica de memória.

---

## Sumário

- [Introdução aos Filtros Digitais](#introdução-aos-filtros-digitais)
- [Filtro FIR](#filtro-fir)
  - [Conceito e Implementação do Filtro FIR](#conceito-e-implementação-do-filtro-fir)
  - [Diagrama do Filtro FIR](#diagrama-do-filtro-fir)
- [Filtro IIR](#filtro-iir)
  - [Conceito e Implementação do Filtro IIR](#conceito-e-implementação-do-filtro-iir)
  - [Direct Form II Transposto](#direct-form-ii-transposto)
  - [Diagrama do Filtro IIR](#diagrama-do-filtro-iir)
- [Direct Form II Transposed Filter Implementation](#direct-form-ii-transposed-filter-implementation)
  - [Visão Geral](#visão-geral-1)
  - [Conceitos Básicos do Filtro IIR](#conceitos-básicos-do-filtro-iir)
  - [Direct Form II vs. Direct Form II Transposto](#direct-form-ii-vs-direct-form-ii-transposto)
  - [Funcionamento do Direct Form II Transposto](#funcionamento-do-direct-form-ii-transposto)
  - [Exemplo Passo a Passo](#exemplo-passo-a-passo)
  - [Diagrama Ilustrativo](#diagrama-ilustrativo)
  - [Vantagens](#vantagens)
  - [Conclusão](#conclusão-1)
- [Exemplos Práticos](#exemplos-práticos)
- [Conclusão Geral](#conclusão-geral)

---

## Introdução aos Filtros Digitais

Filtros digitais são algoritmos utilizados para processar sinais, removendo ou atenuando frequências e ruídos indesejados. Eles são essenciais em diversas áreas, como áudio, comunicações e instrumentação. Os dois tipos principais apresentados aqui são:

- **FIR (Finite Impulse Response):** Possui resposta ao impulso finita, utilizando apenas as entradas passadas.
- **IIR (Infinite Impulse Response):** Utiliza tanto as entradas quanto as saídas passadas, podendo ter uma resposta ao impulso infinita.

---

## Filtro FIR

### Conceito e Implementação do Filtro FIR

O filtro FIR é definido pela equação de convolução:


$$
y[n] = \sum_{i=0}^{N-1} b[i] \cdot x[n-i]
$$


- **x[n]:** Amostra de entrada.
- **y[n]:** Amostra de saída.
- **b[i]:** Coeficientes do filtro.
- **N:** Número de taps (coeficientes).

Este filtro é naturalmente estável e ideal quando se deseja uma resposta de fase linear.

### Diagrama do Filtro FIR

Insira o seguinte diagrama dentro de um bloco de código usando os delimitadores >>>:

```
         x[n]
           │
           ▼
       +---------+
       |  * b0   |
       +---------+
           │
           ▼
       +---------+  <-- Delay (z⁻¹)
       |  * b1   |
       +---------+
           │
           ▼
       +---------+  <-- Delay (z⁻¹)
       |  * b2   |
       +---------+
           │
           ▼
       +---------+  <-- Delay (z⁻¹)
       |  * b3   |
       +---------+
           │
           ▼
         [Soma] ----► y[n]
```

---

## Filtro IIR

### Conceito e Implementação do Filtro IIR

O filtro IIR é definido pela equação de diferença:

$$
y[n] = \sum_{i=0}^{M} b[i] \cdot x[n-i] - \sum_{j=1}^{N} a[j] \cdot y[n-j]
$$

- **x[n]:** Amostra de entrada.
- **y[n]:** Amostra de saída.
- **b[i]:** Coeficientes feedforward (numerador).
- **a[j]:** Coeficientes feedback (denominador), com $ a_0 = 1 $ por convenção.

Embora possam alcançar desempenho similar aos filtros FIR com menos recursos, os filtros IIR requerem cuidados para evitar instabilidade.

### Direct Form II Transposto

Uma implementação eficiente para filtros IIR é o **Direct Form II Transposto**, que reorganiza os cálculos para utilizar um único vetor de estado, otimizando o uso de memória e melhorando a robustez numérica.

#### Funcionamento do Direct Form II Transposto

Considere um filtro de segunda ordem com coeficientes:

- **Coeficientes Feedforward (b):** $b_0,\, b_1,\, b_2 $
- **Coeficientes Feedback (a):** $a_0 = 1,\, a_1,\, a_2$

O processamento de uma nova amostra $x[n]$ ocorre em duas etapas:

1. **Cálculo da Saída:**  
   $$
   y[n] = b_0 \cdot x[n] + d_0
   $$
   onde $d_0$ é o primeiro elemento do vetor de estado.

2. **Atualização do Vetor de Estado:**  
   $$
   d_0 \leftarrow d_1 + b_1 \cdot x[n] - a_1 \cdot y[n]
   $$
   $$
   d_1 \leftarrow b_2 \cdot x[n] - a_2 \cdot y[n]
   $$

Esta estrutura usa apenas um vetor de estado de tamanho 2, otimizando a memória e distribuindo melhor os erros de arredondamento.

### Diagrama do Filtro IIR (Direct Form II Transposto)

Insira o seguinte diagrama dentro de um bloco de código usando os delimitadores >>>:

```
         x[n]
           │
           ▼
       +---------+       (Multiplica por b0)
       |  * b0   |─────────► y[n]
       +---------+            │
           │                  │
           │                  ▼
           │             +---------+
           ├────────────►|  d0     |  <-- Estado 0
           │             +---------+
           │                  │
           │                  ▼
           │             +---------+      (Multiplica por b1)
           │             |  * b1   |─────────► [Adição/Subtração com a1*y[n]]
           │             +---------+
           │                  │
           │                  ▼
           │             +---------+
           └────────────►|  d1     |  <-- Estado 1
                         +---------+
                                │
                                ▼
                           +---------+      (Multiplica por b2)
                           |  * b2   |─────────► [Subtração com a2*y[n]]
                           +---------+
```

---

## Direct Form II Transposed Filter Implementation

### Visão Geral

O **Direct Form II Transposto** é uma técnica para implementar filtros IIR que minimiza o uso de memória e melhora a estabilidade numérica. Utilizando um único vetor de estado para armazenar os cálculos anteriores, essa abordagem é ideal para microcontroladores e ambientes com recursos limitados.

### Conceitos Básicos do Filtro IIR

Um filtro IIR é definido pela seguinte equação de diferença:

$$
y[n] = b_0 \cdot x[n] + b_1 \cdot x[n-1] + \dots + b_{M} \cdot x[n-M] - a_1 \cdot y[n-1] - \dots - a_{N} \cdot y[n-N]
$$

Onde:
- **x[n]:** Amostra de entrada atual.
- **y[n]:** Amostra de saída.
- **b[i]:** Coeficientes do numerador (feedforward).
- **a[i]:** Coeficientes do denominador (feedback), com $a_0 = 1$ por convenção.

### Direct Form II vs. Direct Form II Transposto

- **Direct Form II:**  
  Combina as seções de feedforward e feedback utilizando um único vetor de estado, reduzindo o uso de memória. Porém, pode ser mais suscetível a erros de arredondamento em implementações com precisão limitada.

- **Direct Form II Transposto:**  
  Reorganiza o fluxo dos sinais para calcular primeiro a saída e, em seguida, atualizar o vetor de estado. Isso melhora a distribuição dos erros de arredondamento e a estabilidade numérica.

### Funcionamento do Direct Form II Transposto

Considere um filtro de segunda ordem com os seguintes coeficientes:

- **Coeficientes Feedforward (b):** $[b_0,\, b_1,\, b_2]$
- **Coeficientes Feedback (a):** $[1,\, a_1,\, a_2]$

#### Etapas de Processamento

1. **Cálculo da Saída:**  
   $$
   y[n] = b_0 \cdot x[n] + d_0
   $$
   onde \(d_0\) é o primeiro elemento do vetor de estado.

2. **Atualização do Vetor de Estado:**  
   $$
   d_0 \leftarrow d_1 + b_1 \cdot x[n] - a_1 \cdot y[n]
   $$
   $$
   d_1 \leftarrow b_2 \cdot x[n] - a_2 \cdot y[n]
   $$

Dessa forma, utilizando um vetor de estado de tamanho 2, o filtro processa a nova amostra e atualiza os estados para os próximos cálculos.

### Exemplo Passo a Passo

Imagine um filtro com os coeficientes:

- **Feedforward (b):**  
  $ b_0 = 0.2929,\quad b_1 = 0.5858,\quad b_2 = 0.2929 $
- **Feedback (a):**  
  $ a_0 = 1,\quad a_1 = 0,\quad a_2 = 0.1716 $

#### Cenário Inicial
- Estados $d_0$ e $d_1$ iniciam com valor 0.

#### Processamento de uma Nova Amostra
- **Entrada:** $x[n] = 1.0$

##### Cálculo da Saída
$$
y[n] = 0.2929 \times 1.0 + 0 \quad (\text{pois } d_0 = 0)
$$
$$
y[n] = 0.2929
$$

##### Atualização dos Estados
- **Atualização de $d_0$:**
$$
d_0 \leftarrow 0 + 0.5858 \times 1.0 - 0 \times 0.2929 = 0.5858
$$
- **Atualização de $d_1$:**
$$
d_1 \leftarrow 0.2929 \times 1.0 - 0.1716 \times 0.2929 \approx 0.2929 - 0.0501 = 0.2428
$$

Esses novos valores de $d_0$ e $d_1$ serão utilizados para processar a próxima amostra.

### Diagrama Ilustrativo

Insira o seguinte diagrama dentro de um bloco de código usando os delimitadores >>>:

```
     x[n]
       │
       ▼
   +---------+       (Multiplica por b0)
   |  * b0   |─────────► y[n]
   +---------+            │
       │                  │
       │                  ▼
       │             +---------+
       ├────────────►|  d0     |  <-- Estado 0
       │             +---------+
       │                  │
       │                  ▼
       │             +---------+      (Multiplica por b1)
       │             |  * b1   |─────────► [Adição/Subtração com a1*y[n]]
       │             +---------+
       │                  │
       │                  ▼
       │             +---------+
       └────────────►|  d1     |  <-- Estado 1
                     +---------+
                            │
                            ▼
                       +---------+      (Multiplica por b2)
                       |  * b2   |─────────► [Subtração com a2*y[n]]
                       +---------+
```

### Vantagens

- **Eficiência de Memória:**  
  Utiliza um único vetor de estado com tamanho $\max(nb, na) - 1$ em vez de buffers separados para entradas e saídas.
- **Estabilidade Numérica:**  
  A estrutura transposta distribui melhor os erros de arredondamento, o que é especialmente útil em implementações com precisão limitada.
- **Implementação Simplificada:**  
  O fluxo de dados linear facilita tanto a implementação quanto o debug, tornando o algoritmo ideal para sistemas embarcados.

### Conclusão

O **Direct Form II Transposto** é uma abordagem poderosa para implementar filtros IIR em microcontroladores e ambientes com recursos limitados. Com uso otimizado de memória e maior robustez contra erros numéricos, essa estrutura é amplamente utilizada em aplicações embarcadas. Adapte este exemplo conforme as necessidades do seu projeto e contribua com melhorias!

---

## Exemplos Práticos

O repositório contém implementações em C puro para sistemas embarcados:

- **Filtro FIR:**  
  - Arquivo como `fir_filter.h` demonstra a implementação do filtro FIR.  
  - Um exemplo prático está disponível no arquivo `uno_fir.cpp` para uso com Arduino.
  
- **Filtro IIR (Direct Form II Transposto):**  
  - Arquivo como `iir_filter.h` mostra a implementação do filtro IIR utilizando a estrutura Direct Form II Transposto.  
  - O arquivo `uno_iiR.cpp` apresenta um exemplo prático com Arduino.

---

## Conclusão Geral

Filtros digitais são ferramentas essenciais no processamento de sinais, permitindo a remoção ou atenuação de ruídos e frequências indesejadas.  
- **Filtro FIR:** Oferece uma resposta ao impulso finita e é ideal quando se deseja uma resposta de fase linear.  
- **Filtro IIR:** Com a implementação em **Direct Form II Transposto**, é possível reduzir o uso de memória e melhorar a robustez numérica, sendo ideal para aplicações em microcontroladores com recursos limitados.

Explore os exemplos e adapte o código conforme as necessidades do seu projeto!

---

*Este projeto tem fins educacionais e demonstra práticas eficientes para a implementação de filtros digitais em ambientes com restrição de recursos.*

