import numpy as np
from scipy.signal import butter, freqz
from matplotlib.pyplot import subplots, show
from findAnalogFilterByTargetFreq import findAnalogFilterByTargetFreq

def findDigitalFilterIIRByTargetFreq(fDesejada, ordem, fs, filterType, desvio, isBP):
    """
    Calcula os coeficientes de um filtro IIR digital utilizando a frequência de corte 
    de um filtro analógico Butterworth, plota a resposta em frequência com:
    - Frequência desejada
    - Frequência de corte
    - Borda da banda de interesse
    - Borda da banda oposta (frequência complementar)

    Retorna:
      b, a : Coeficientes do filtro IIR.
    """
    # Obtém frequência de corte + frequência limite + complementar
    fc_analog, freq_limite, f_complementar_hz = findAnalogFilterByTargetFreq(
        fDesejada, ordem, filterType, desvio, isBP
    )

    # Frequência de corte normalizada
    nyq = 0.5 * fs
    normal_fc = fc_analog / nyq

    # Coeficientes do filtro digital IIR Butterworth
    b, a = butter(ordem, normal_fc, btype=filterType)

    # Resposta em frequência
    w, h = freqz(b, a, whole=True)
    freqs_hz = w * fs / (2 * np.pi)

    # Plot
    fig, ax = subplots(figsize=(14, 5))
    ax.plot(freqs_hz, np.abs(h), label='Resposta do Filtro IIR', color='b')
    ax.set_xlabel('Frequência (Hz)')
    ax.set_ylabel('Magnitude')
    ax.set_title('Filtro IIR - Resposta em Frequência')

    # Plot das linhas
    print("Frequência Desejada [Amarelo]:", fDesejada)
    ax.axvline(fDesejada, color='y', linestyle='--', label='Frequência Desejada')

    print("Frequência de Corte [Verde]:", fc_analog)
    ax.axvline(fc_analog, color='g', linestyle='--', label='Frequência de Corte')

    if isBP:
        print("Frequência limite da Banda de Passagem [Vermelho]:", freq_limite)
        ax.axvline(freq_limite, color='r', linestyle='--', label='Banda de Passagem')
        print("Frequência Complementar (Rejeição) [Roxa]:", f_complementar_hz)
        ax.axvline(f_complementar_hz, color='purple', linestyle='--', label='Banda de Rejeição')
    else:
        print("Frequência limite da Banda de Rejeição [Vermelho]:", freq_limite)
        ax.axvline(freq_limite, color='r', linestyle='--', label='Banda de Rejeição')
        print("Frequência Complementar (Passagem) [Roxa]:", f_complementar_hz)
        ax.axvline(f_complementar_hz, color='purple', linestyle='--', label='Banda de Passagem')

    ax.grid(True)
    ax.legend()
    show()

    return b, a

# Exemplo de uso:
if __name__ == '__main__':
    b, a = findDigitalFilterIIRByTargetFreq(
            fDesejada = 1000,        # Hz
            ordem = 2,
            fs = 20000,              # Frequência de amostragem
            filterType = 'lowpass',  # 'lowpass' ou 'highpass'
            desvio = 0.05,
            isBP = True              # True para banda de passagem; False para rejeição
    )
    print("Coeficientes do numerador (b):")
    print(", ".join(str(coef) for coef in b))
    print("Coeficientes do denominador (a):")
    print(", ".join(str(coef) for coef in a))
