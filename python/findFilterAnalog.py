import numpy as np
from matplotlib.pyplot import subplots, show
from scipy.signal import butter, freqs

def findAnalogButterFilter(fDesejada, ordem, filterType="lowpass", desvio=0.05, isBP=True):
    """
    Calcula os coeficientes de um filtro analógico Butterworth e ajusta iterativamente a
    frequência de corte (fc) para que a resposta em frequência atenda a um critério de desvio.
    Em seguida, plota a resposta em frequência com marcações das frequências de interesse.
    
    Parâmetros:
      fDesejada   : Frequência desejada para a banda de interesse (Hz). Para filtros analógicos,
                    as frequências são convertidas para rad/s.
      ordem       : Ordem do filtro (número de polos).
      filterType  : Tipo do filtro - 'lowpass' para passa-baixa ou 'highpass' para passa-alta.
      desvio      : Desvio máximo permitido na magnitude da resposta (ex.: 0.05 para 5%).
      isBP        : Booleano. Se True, fDesejada deve estar na banda de passagem; se False, na banda de rejeição.
    
    Retorna:
      b, a : Vetores com os coeficientes do numerador e denominador do filtro Butterworth.
    """
    # Converte a frequência desejada de Hz para rad/s
    f_radians = 2 * np.pi * fDesejada

    # Define o intervalo de busca para a frequência de corte (fc) em rad/s,
    # de acordo com o tipo de filtro e se fDesejada deve estar na banda de passagem ou rejeição.
    if filterType == "lowpass":
        if isBP:
            fc_start = f_radians       # se a frequência desejada deve estar na banda de passagem,
            fc_end   = 10 * f_radians    # fc deve ser alta para que o ganho seja próximo de 1 em fDesejada.
        else:
            fc_start = f_radians / 10   # se fDesejada estiver na rejeição, fc deve ser menor.
            fc_end   = f_radians
    elif filterType == "highpass":
        if isBP:
            fc_start = f_radians / 10   # para passagem, fc deve ser bem menor que fDesejada
            fc_end   = f_radians
        else:
            fc_start = f_radians        # para rejeição, fc deve ser maior que fDesejada
            fc_end   = 10 * f_radians
    else:
        raise ValueError("Tipo de filtro inválido. Use 'lowpass' ou 'highpass'.")

    # Gera os valores candidatos para fc (em rad/s)
    fc_values = np.linspace(fc_start, fc_end, 10000, endpoint=False)
    fc_escolhido = None

    # Itera sobre os possíveis valores de fc para encontrar o que atende ao critério
    # Avaliamos a resposta em frequência no ponto f_radians (fDesejada convertido para rad/s)
    for fc in fc_values:
        # Projeta o filtro Butterworth analógico
        if filterType == "lowpass":
            b, a = butter(ordem, fc, btype="lowpass", analog=True)
        else:  # highpass
            b, a = butter(ordem, fc, btype="highpass", analog=True)
        
        # Calcula a resposta em frequência somente no ponto f_radians
        w_eval, h_eval = freqs(b, a, worN=[f_radians])
        mag = np.abs(h_eval[0])
        
        # Se fDesejada deve estar na banda de passagem, o ganho deve ser próximo de 1;
        # caso contrário, se estiver na rejeição, o ganho deve ser baixo.
        if isBP:
            if mag >= (1 - desvio):
                fc_escolhido = fc
                break
        else:
            if mag <= desvio:
                fc_escolhido = fc
                break

    # Se nenhum fc adequado foi encontrado, usa o último valor testado
    if fc_escolhido is None:
        fc_escolhido = fc_values[-1]
        print("Aviso: Nenhum fc adequado encontrado. Usando fc =", fc_escolhido)

    # Reprojeta o filtro com o fc escolhido
    if filterType == "lowpass":
        b, a = butter(ordem, fc_escolhido, btype="lowpass", analog=True)
    else:
        b, a = butter(ordem, fc_escolhido, btype="highpass", analog=True)
    
    # Para visualização, gera a resposta em frequência em um grid de frequências
    w = np.linspace(0, 10 * f_radians, 1024)
    w, h = freqs(b, a, worN=w)
    freqs_hz = w / (2 * np.pi)  # converte de rad/s para Hz

    # Para definir uma "frequência limite", procuramos onde a resposta atinge (1 - desvio) ou desvio
    if isBP:
        indices = np.where(np.abs(h) <= (1 - desvio))[0]
    else:
        indices = np.where(np.abs(h) <= desvio)[0]
    
    idx_limite = indices[0] if indices.size > 0 else (len(w) - 1)
    freq_limite = w[idx_limite] / (2 * np.pi)

    # Plot da resposta em frequência
    fig, ax = subplots(figsize=(20, 6))
    ax.plot(freqs_hz, np.abs(h), 'b', label='Resposta em Frequência')
    ax.set_xlabel('Frequência (Hz)')
    ax.set_ylabel('Magnitude')
    ax.grid()

    # Plota a frequência limite conforme o critério
    if isBP:
        print("Frequência limite da Banda de Passagem [Vermelho]:", freq_limite)
        ax.axvline(freq_limite, color='r', label='Banda de Passagem')
    else:
        print("Frequência limite da Banda de Rejeição [Vermelho]:", freq_limite)
        ax.axvline(freq_limite, color='r', label='Banda de Rejeição')

    # Plota a frequência de corte (fc escolhido) convertida para Hz
    fc_escolhido_hz = fc_escolhido / (2 * np.pi)
    print("Frequência de Corte [Verde]:", fc_escolhido_hz)
    ax.axvline(fc_escolhido_hz, color='g', label='Frequência de Corte')

    # Marca a frequência desejada (fDesejada)
    print("Frequência Desejada [Amarelo]:", fDesejada)
    ax.axvline(fDesejada, color='y', label='Frequência Desejada')

    ax.legend()
    show()

    return fc_escolhido_hz

# Exemplo de uso:
# Parâmetros:
# - Frequência desejada: 10 Hz
# - Ordem do filtro: 4
# - Filtro passa-baixa com a frequência desejada na banda de passagem
fc_corte  = findAnalogButterFilter(10, 2, filterType="lowpass", desvio=0.05, isBP=True)
print("Frequência de Corte (Hz):", fc_corte)
