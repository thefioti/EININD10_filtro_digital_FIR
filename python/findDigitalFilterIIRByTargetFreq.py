import numpy as np
from scipy.signal import butter, freqz
from matplotlib.pyplot import subplots, show
from findAnalogFilterByTargetFreq import findAnalogFilterByTargetFreq

def findDigitalFilterIIRByTargetFreq(fDesejada, ordem, fs, filterType, desvio, isBP):
    """
    Calcula os coeficientes de um filtro IIR digital utilizando a frequência de corte 
    de um filtro analógico Butterworth, plota a resposta em frequência com as linhas 
    que indicam as frequências de interesse e retorna os coeficientes do filtro IIR.
    
    Parâmetros:
      fDesejada   : Frequência desejada para a banda (Hz).
      ordem       : Ordem do filtro (número de polos).
      fs          : Frequência de amostragem (Hz).
      filterType  : Tipo do filtro - 'lowpass' para passa-baixa ou 'highpass' para passa-alta.
      desvio      : Desvio máximo permitido na magnitude (ex.: 0.05 para 5%).
      isBP        : Booleano. Se True, fDesejada está na banda de passagem; se False, na banda de rejeição.
    
    Retorna:
      b, a : Arrays com os coeficientes do numerador e denominador do filtro IIR.
    """
    # Calcula a frequência de corte do filtro analógico
    fc_analog = findAnalogFilterByTargetFreq(fDesejada, ordem, filterType, desvio, isBP)

    # Converte a frequência de corte para a normalizada para a frequência de Nyquist
    nyq = 0.5 * fs
    normal_fc = fc_analog / nyq

    # Calcula os coeficientes do filtro IIR Butterworth
    b, a = butter(ordem, normal_fc, btype=filterType)

    # Calcula a resposta em frequência do filtro IIR
    w, h = freqz(b, a, whole=True)

    # Converte as frequências para Hz
    freqs_hz = w * fs / (2 * np.pi)

    # Configura o gráfico da resposta em frequência
    fig, ax = subplots(figsize=(20, 6))
    ax.plot(freqs_hz, np.abs(h), label='Resposta do Filtro IIR', color='b')
    ax.set_xlabel('Frequência (Hz)')
    ax.set_ylabel('Magnitude')

    # Plota a linha vertical da frequência de corte escolhida
    print("Frequência de Corte [Verde]:", fc_analog)
    ax.axvline(fc_analog, color='g', linestyle='--', label='Frequência de Corte')

    # Plota a linha vertical da frequência desejada
    print("Frequência Desejada [Amarelo]:", fDesejada)
    ax.axvline(fDesejada, color='y', linestyle='--', label='Frequência Desejada')

    ax.grid(True)
    ax.legend()
    show()

    return b, a

# Exemplo de uso:
if __name__ == '__main__':
    fDesejada = 1000   # Frequência desejada em Hz
    ordem = 2
    fs = 20000          # Frequência de amostragem em Hz
    filterType = 'lowpass'  # 'lowpass' ou 'highpass'
    desvio = 0.05      # 5% de desvio
    isBP = True        # True para banda de passagem; False para rejeição

    b, a = findDigitalFilterIIRByTargetFreq(fDesejada, ordem, fs, filterType, desvio, isBP)
    print("Coeficientes do numerador (b):")
    print(", ".join(str(coef) for coef in b))
    print("Coeficientes do denominador (a):")
    print(", ".join(str(coef) for coef in a))
