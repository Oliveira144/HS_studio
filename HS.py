@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background-color: #111;
    color: #f1f1f1;
}

h1.titulo {
    font-size: 2.5rem;
    text-align: center;
    color: #39FF14;
    margin-bottom: 2rem;
}

.stButton>button {
    font-weight: bold;
    border-radius: 6px;
    transition: 0.3s ease;
}

.stButton>button:hover {
    transform: scale(1.02);
    background-color: #222;
    border: 1px solid #39FF14;
}
from collections import Counter

def detectar_sequencia_surf(seq):
    resultados = []
    i = 0
    while i < len(seq) - 2:
        if seq[i] == seq[i+1] == seq[i+2]:
            j = i + 3
            while j < len(seq) and seq[j] == seq[i]:
                j += 1
            resultados.append(f"Sequência de '{seq[i]}' por {j-i} vezes na posição {i+1}.")
            i = j
        else:
            i += 1
    return resultados

def detectar_zig_zag(seq):
    resultados = []
    i = 0
    while i < len(seq) - 3:
        if seq[i] != seq[i+1] and seq[i] == seq[i+2] and seq[i+1] == seq[i+3]:
            resultados.append(f"Padrão Zig-Zag detectado iniciando na posição {i+1}: {seq[i:i+4]}")
        i += 1
    return resultados

def detectar_empate_recorrente(seq, empate_char='E'):
    resultados = []
    indices = [i for i, x in enumerate(seq) if x == empate_char]
    for i in range(len(indices) - 1):
        diff = indices[i+1] - indices[i]
        if diff in [2, 3]:
            resultados.append(f"Empates nas posições {indices[i]+1} e {indices[i+1]+1} (distância: {diff-1}).")
    return resultados

def detectar_espelho(seq):
    resultados = []
    for i in range(len(seq) - 3):
        if seq[i] == seq[i+3] and seq[i+1] == seq[i+2] and seq[i] != seq[i+1]:
            resultados.append(f"Padrão Espelho detectado: {''.join(seq[i:i+4])} na posição {i+1}.")
    return resultados

def detectar_padrao_escada(seq):
    resultados = []
    for i in range(len(seq) - 5):
        if (seq[i] != seq[i+1] and
            seq[i+1] == seq[i+2] and seq[i+1] != seq[i] and
            seq[i+3] == seq[i+4] == seq[i+5] and seq[i+3] == seq[i]):
            resultados.append(f"Escada detectada: 1-{seq[i]}, 2-{seq[i+1]}, 3-{seq[i]}. Início: posição {i+1}")
    return resultados
def gerar_sugestoes(sequencia, resultados):
    sugestoes = []
    empates = []

    ultima = sequencia[-1] if sequencia else None
    penultima = sequencia[-2] if len(sequencia) >= 2 else None

    if resultados.get("Surf"):
        if ultima and f"'{ultima}'" in "".join(resultados["Surf"][-1]):
            sugestoes.append(f"🌀 Continua tendência de '{ultima}'? Pode ser um Surf prolongado.")

    if resultados.get("Zig-Zag"):
        if ultima and penultima and ultima != penultima:
            sugestoes.append(f"↔️ Alternância detectada. Próximo pode ser '{penultima}'.")

    if resultados.get("Empate"):
        empates.append("⚖️ Empates frequentes em intervalo curto — fique atento!")
        sugestoes.append("Considerar possibilidade de novo empate na sequência.")

    if resultados.get("Espelho"):
        sugestoes.append("🔁 Padrão Espelho pode estar se formando. Próximo resultado pode repetir lógica.")

    if resultados.get("Escada"):
        sugestoes.append("📶 Escada em construção? Pode se repetir o degrau da sequência.")

    return sugestoes, empates
