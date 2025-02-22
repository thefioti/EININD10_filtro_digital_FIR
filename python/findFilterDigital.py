import numpy as np
from matplotlib.pyplot import subplots, show
from scipy.signal import firwin, freqz

def findFilterDigitalFir(fDesejada, ordem, fs, filterType="lowpass", desvio=0.05, isBP=True):
    """
    Calcula os coeficientes de um filtro FIR digital utilizando a janela Hamming, 
    ajustando iterativamente a frequência de corte (fc) para atender a um critério de desvio 
    na resposta em frequência. Em seguida, plota a resposta em frequência com marcações das frequências de interesse.
    
    Parâmetros:
      fDesejada   : Frequência desejada para a banda (Hz).
      ordem       : Ordem do filtro (número de coeficientes).
      fs          : Frequência de amostragem (Hz).
      filterType  : Tipo do filtro - 'lowpass' para passa-baixa ou 'highpass' para passa-alta.
      desvio      : Desvio máximo permitido na amplitude (por exemplo, 0.05 para 5%).
      isBP        : Booleano. Se True, fDesejada é da banda de passagem; se False, da banda de rejeição.
    
    Retorna:
      taps : Array com os coeficientes do filtro FIR.
    """
    # Converte a frequência desejada de Hz para radianos por amostra
    f_radians = fDesejada * (2 * np.pi) / fs

    # Define a condição de busca para o cutoff 'fc'
    # Para passa-baixa, a condição é isBP; para passa-alta, inverte o valor de isBP
    condition = isBP if filterType == "lowpass" else not isBP

    # Define o intervalo de variação para 'fc' com base na condição
    if condition:
        fc_max = min(10 * fDesejada, fs / 2)
    else:
        fc_max = fDesejada // 20

    # Gera os valores de fc para testar
    fc_values = np.linspace(fDesejada, fc_max, 10000, endpoint=False)
    fc_escolhido = None

    # Itera sobre os possíveis valores de fc para encontrar o que atende ao critério de desvio
    for fc in fc_values:
        # Calcula os coeficientes do filtro com a janela Hamming
        taps = firwin(numtaps=ordem, cutoff=fc, fs=fs, window="hamming", pass_zero=filterType)
        # Calcula a resposta em frequência do filtro com 1024 pontos
        w, h = freqz(taps, worN=1024)
        
        # Ajusta os arrays dependendo do tipo de filtro
        if condition:
            h_magnitude = np.abs(h)
            w_magnitude = np.abs(w)
        else:
            h_magnitude = np.abs(h)[::-1]
            w_magnitude = np.abs(w)[::-1]
        
        # Define a condição de busca para o índice desejado
        if isBP:
            indices = np.where(h_magnitude <= (1 - desvio))[0]
        else:
            indices = np.where(h_magnitude >= desvio)[0]
        
        # Se nenhum índice satisfizer a condição, passa para o próximo valor de fc
        if indices.size == 0:
            continue
        idx = indices[0]

        # Verifica se a frequência associada ao índice atende ao critério comparado com f_radians
        if condition:
            if w_magnitude[idx] >= f_radians:
                fc_escolhido = fc
                break
        else:
            if w_magnitude[idx] <= f_radians:
                fc_escolhido = fc
                break

    # Se nenhum fc adequado foi encontrado, usa o último valor testado e emite um aviso
    if fc_escolhido is None:
        fc_escolhido = fc_values[-1]
        print("Aviso: Nenhum fc que atenda o critério foi encontrado. Usando fc =", fc_escolhido)

    # Recalcula os coeficientes e a resposta em frequência com o fc escolhido
    taps = firwin(numtaps=ordem, cutoff=fc_escolhido, fs=fs, window="hamming", pass_zero=filterType)
    w, h = freqz(taps, worN=1024)

    # Determina os índices para as frequências limite
    if condition:
        indices_inicial = np.where(np.abs(h) <= (1 - desvio))[0]
        indices_final   = np.where(np.abs(h) <= desvio)[0]
    else:
        indices_inicial = np.where(np.abs(h) >= desvio)[0]
        indices_final   = np.where(np.abs(h) >= (1 - desvio))[0]
    
    # Caso não encontre os índices, utiliza os extremos do array
    idx_inicial = indices_inicial[0] if indices_inicial.size > 0 else 0
    idx_final   = indices_final[0] if indices_final.size > 0 else len(w) - 1

    # Converte os índices em frequências (Hz)
    f_limite_inicial = w[idx_inicial] * fs / (2 * np.pi)
    f_limite_final   = w[idx_final] * fs / (2 * np.pi)
    freqs_hz = w * fs / (2 * np.pi)

    # Configura o gráfico da resposta em frequência
    fig, ax = subplots(figsize=(20, 6))
    ax.plot(freqs_hz, np.abs(h), 'b', label='Resposta em Frequência')
    ax.set_xlabel('Frequência (Hz)')
    ax.set_ylabel('Magnitude')

    # Define as frequências de interesse para o plot, dependendo do tipo de filtro
    if isBP:
        banda_passagem = f_limite_inicial
        banda_bloqueio = f_limite_final
    else:
        banda_passagem = f_limite_final
        banda_bloqueio = f_limite_inicial

    # Plota as linhas verticais e imprime as informações
    print("Frequência limite da Banda de Passagem [Vermelho]:", banda_passagem)
    ax.axvline(banda_passagem, color='r', label='Banda de Passagem')
    print("Frequência de Corte [Verde]:", fc_escolhido)
    ax.axvline(fc_escolhido, color='g', label='Frequência de Corte')
    print("Frequência limite da Banda de Bloqueio [Amarelo]:", banda_bloqueio)
    ax.axvline(banda_bloqueio, color='y', label='Banda de Bloqueio')

    ax.grid()
    ax.legend()
    show()

    return taps

# Exemplo de uso:
# Parâmetros:
# - Frequência desejada: 10 Hz
# - Ordem do filtro: 50
# - Frequência de amostragem: 100 Hz
# - Filtro passa-baixa com a frequência desejada na banda de passagem
taps = findFilterDigitalFir(10, 50, 100, isBP=True)

print("Coeficientes do filtro:")
print(", ".join(str(coef) for coef in taps))
