import streamlit as st
from collections import Counter

st.set_page_config(page_title="Analisador de Padrões e Sugestões", layout="wide", initial_sidebar_state="expanded")

# --- Injeção de CSS para Estilização ---
st.markdown("""
<style>
/* Estilo geral para todos os botões para forçar cor de texto e fontes */
div.stButton > button {
    font-size: 1.2em;
    font-weight: bold;
    color: white !important; /* Garante que o texto seja branco */
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    margin-bottom: 10px; /* Espaçamento entre os botões */
    display: flex; /* Para centralizar o texto se o botão for wide */
    justify-content: center; /* Centraliza horizontalmente */
    align-items: center; /* Centraliza verticalmente */
}

/* Cor específica para o botão 'Casa (C)' - usando data-testid do Streamlit */
button[data-testid="stButton-btn_casa"] {
    background-color: #DC3545 !important; /* Vermelho forte */
}

/* Cor específica para o botão 'Visitante (V)' */
button[data-testid="stButton-btn_visitante"] {
    background-color: #007BFF !important; /* Azul forte */
}

/* Cor específica para o botão 'Empate (E)' */
button[data-testid="stButton-btn_empate"] {
    background-color: #6C757D !important; /* Cinza escuro */
}

/* Estilo para os botões de ação (Desfazer, Limpar, Zerar) */
button[data-testid*="stButton-btn_"] { /* Seletor mais genérico para todos os botões com key que começa com 'btn_' */
    background-color: #343A40 !important; /* Quase preto */
    font-size: 1em !important;
    padding: 8px 15px !important;
}

/* Sobrescreve as cores para os botões Casa, Visitante, Empate que são mais específicos */
button[data-testid="stButton-btn_casa"],
button[data-testid="stButton-btn_visitante"],
button[data-testid="stButton-btn_empate"] {
    font-size: 1.2em !important; /* Mantém o tamanho maior para estes */
    padding: 10px 20px !important; /* Mantém o padding maior */
}


/* Estilo para o título de resultados e sugestões */
h3 {
    color: #FFD700; /* Dourado para títulos de seções importantes */
    margin-top: 20px; /* Espaçamento acima do título */
    margin-bottom: 15px; /* Espaçamento abaixo do título */
}

/* Cor de fundo para as caixas de informação/sugestão */
div[data-testid="stAlert"] {
    background-color: #282828 !important; /* Fundo mais escuro para alerts */
    color: white !important;
    border-left: 5px solid #FFD700 !important; /* Borda dourada */
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 5px;
}
div[data-testid="stAlert"] svg { /* Ícone dentro do alert */
    color: #FFD700 !important; /* Ícone dourado */
}
div[data-testid="stAlert"] div[role="alert"] p { /* Texto dentro do alert */
    color: white !important;
}

/* Estilo para o código da sequência atual e histórico */
div.stCodeBlock {
    background-color: #202020 !important; /* Fundo mais escuro para o bloco de código */
    color: #00FF00 !important; /* Texto verde neon (opcional, pode ser branco) */
    border-radius: 5px;
    padding: 10px;
    font-family: 'monospace';
    overflow-x: auto; /* Permite scroll horizontal se a sequência for muito longa */
}
</style>
""", unsafe_allow_html=True)


# --- Inicialização do Session State ---
if 'current_sequence' not in st.session_state:
    st.session_state.current_sequence = []
if 'history' not in st.session_state:
    st.session_state.history = []
if 'last_analysis_results' not in st.session_state:
    st.session_state.last_analysis_results = {}
if 'last_suggestions' not in st.session_state:
    st.session_state.last_suggestions = []
if 'last_empate_possibilities' not in st.session_state:
    st.session_state.last_empate_possibilities = []


# --- Funções de Detecção de Padrões ---
# As 13 funções devem estar COMPLETAS aqui.
# Certifique-se de que cada função está definida corretamente com 'def nome_da_funcao(seq):' e um 'return' válido.

def detectar_sequencia_surf(seq):
    """1. Sequência (Surf de Cor) – 3+ vezes a mesma cor seguida"""
    padroes_encontrados = []
    if len(seq) < 3: return padroes_encontrados
    i = 0
    while i < len(seq) - 2:
        if seq[i] == seq[i+1] == seq[i+2]:
            j = i + 3
            while j < len(seq) and seq[j] == seq[i]: j += 1
            padroes_encontrados.append(f"Sequência de '{seq[i]}' por {j-i} vezes, iniciando na posição {i+1}.")
            i = j
        else: i += 1
    return padroes_encontrados

def detectar_zig_zag(seq):
    """2. Zig-Zag – alternância de cores (ex: Casa, Visitante, Casa, Visitante...)"""
    padroes_encontrados = []
    if len(seq) < 2: return padroes_encontrados
    i = 0
    while i < len(seq) - 1:
        if seq[i] != seq[i+1]:
            j = i + 2
            while j < len(seq) - 1 and seq[j] == seq[i] and seq[j+1] == seq[i+1]: j += 2
            if j - i >= 4: padroes_encontrados.append(f"Padrão Zig-Zag detectado: {seq[i:j]} iniciando na posição {i+1}.")
            i = j
        else: i += 1
    return padroes_encontrados

def detectar_quebra_surf(seq):
    """3. Quebra de Surf – sequência que é interrompida"""
    padroes_encontrados = []
    if len(seq) < 4: return padroes_encontrados
    for i in range(len(seq) - 3):
        if seq[i] == seq[i+1] == seq[i+2] and seq[i+3] != seq[i]:
            padroes_encontrados.append(f"Quebra de Surf detectada: '{seq[i]}' interrompido por '{seq[i+3]}' na posição {i+4}.")
    return padroes_encontrados

def detectar_quebra_zig_zag(seq):
    """4. Quebra de Zig-Zag – padrão alternado que quebra"""
    padroes_encontrados = []
    if len(seq) < 4: return padroes_encontrados
    for i in range(len(seq) - 3):
        if seq[i] != seq[i+1] and seq[i+1] != seq[i+2] and seq[i] == seq[i+2] and seq[i+3] != seq[i] and seq[i+3] != seq[i+1]:
             padroes_encontrados.append(f"Quebra de Zig-Zag detectada: {seq[i:i+3]} interrompido por '{seq[i+3]}' na posição {i+4}.")
    return padroes_encontrados

def detectar_duplas_repetidas(seq):
    """5. Duplas repetidas – Casa, Casa, Visitante, Visitante..."""
    padroes_encontrados = []
    if len(seq) < 4: return padroes_encontrados
    for i in range(len(seq) - 3):
        if seq[i] == seq[i+1] and seq[i+2] == seq[i+3] and seq[i] != seq[i+2]:
            padroes_encontrados.append(f"Duplas Repetidas detectadas: '{seq[i]}', '{seq[i+2]}' iniciando na posição {i+1}.")
    return padroes_encontrados

def detectar_empate_recorrente(seq, empate_char='E'):
    """6. Empate recorrente – Empates aparecendo em intervalos curtos"""
    padroes_encontrados = []
    indices_empate = [i for i, x in enumerate(seq) if x == empate_char]
    if len(indices_empate) < 2: return padroes_encontrados
    for i in range(len(indices_empate) - 1):
        diff = indices_empate[i+1] - indices_empate[i]
        if diff >= 2 and diff <= 3:
            padroes_encontrados.append(f"Empate Recorrente detectado entre posições {indices_empate[i]+1} e {indices_empate[i+1]+1} (intervalo de {diff-1} não-empates).")
    return padroes_encontrados

def detectar_padrao_escada(seq):
    """7. Padrão Escada – 1 Casa, 2 Visitantes, 3 Casas... (Adaptar para cores/resultados)"""
    padroes_encontrados = []
    if len(seq) < 6: return padroes_encontrados
    for i in range(len(seq) - 5):
        if (seq[i] != seq[i+1] and # 1 elemento do primeiro tipo
            seq[i+1] == seq[i+2] and seq[i+1] != seq[i] and # 2 elementos do segundo tipo
            seq[i+3] == seq[i+4] == seq[i+5] and seq[i+3] == seq[i] # 3 elementos do primeiro tipo
        ): padroes_encontrados.append(f"Padrão Escada (1-{seq[i]}, 2-{seq[i+1]}, 3-{seq[i]}) detectado iniciando na posição {i+1}.")
    return padroes_encontrados

def detectar_espelho(seq):
    """8. Espelho – Ex: Casa, Visitante, Visitante, Casa"""
    padroes_encontrados = []
    if len(seq) < 4: return padroes_encontrados
    for i in range(len(seq) - 3):
        if seq[i] == seq[i+3] and seq[i+1] == seq[i+2] and seq[i] != seq[i+1]:
            padroes_encontrados.append(f"Padrão Espelho detectado: {seq[i:i+4]} iniciando na posição {i+1}.")
    return padroes_encontrados

def detectar_alternancia_empate_meio(seq, empate_char='E'):
    """9. Alternância com empate no meio – Casa, Empate, Visitante"""
    padroes_encontrados = []
    if len(seq) < 3: return padroes_encontrados
    for i in range(len(seq) - 2):
        if seq[i+1] == empate_char and seq[i] != empate_char and seq[i+2] != empate_char and seq[i] != seq[i+2]:
            padroes_encontrados.append(f"Alternância com Empate no Meio detectada: {seq[i:i+3]} iniciando na posição {i+1}.")
    return padroes_encontrados

def detectar_padrao_onda(seq):
    """10. Padrão "onda" – Ex: 1-2-1-2 de cores"""
    padroes_encontrados = []
    if len(seq) < 4: return padroes_encontrados
    for i in range(len(seq) - 3):
        if seq[i] == seq[i+2] and seq[i+1] == seq[i+3] and seq[i] != seq[i+1]:
            padroes_encontrados.append(f"Padrão Onda (1-2-1-2) detectado: {seq[i:i+4]} iniciando na posição {i+1}.")
    return padroes_encontrados

def analisar_previsao_tatica(seq):
    """11. Padrões com base nos últimos 5/7/10 jogos – para previsão tática"""
    padroes_encontrados = []
    if len(seq) >= 5:
        ultimos_5 = seq[-5:]
        contagem = Counter(ultimos_5)
        mais_frequente = contagem.most_common(1)
        if mais_frequente:
            padroes_encontrados.append(f"Nos últimos 5 resultados, '{mais_frequente[0][0]}' apareceu {mais_frequente[0][1]} vezes.")
    if len(seq) >= 7:
        ultimos_7 = seq[-7:]
        contagem = Counter(ultimos_7)
        mais_frequente = contagem.most_common(1)
        if mais_frequente:
            padroes_encontrados.append(f"Nos últimos 7 resultados, '{mais_frequente[0][0]}' apareceu {mais_frequente[0][1]} vezes.")
    if len(seq) >= 10:
        ultimos_10 = seq[-10:]
        contagem = Counter(ultimos_10)
        mais_frequente = contagem.most_common(1)
        if mais_frequente:
            padroes_encontrados.append(f"Nos últimos 10 resultados, '{mais_frequente[0][0]}' apareceu {mais_frequente[0][1]} vezes.")
    return padroes_encontrados

def detectar_padrao_3x1(seq):
    """12. Padrão 3x1 – Três ocorrências de um tipo, seguida por uma de outro."""
    padroes_encontrados = []
    if len(seq) < 4: return padroes_encontrados
    for i in range(len(seq) - 3):
        if seq[i] == seq[i+1] == seq[i+2] and seq[i+3] != seq[i]:
            padroes_encontrados.append(f"Padrão 3x1 detectado: '{seq[i]}' (3x) seguido por '{seq[i+3]}' (1x) na posição {i+1}.")
    return padroes_encontrados

def detectar_padrao_3x3(seq):
    """13. Padrão 3x3 – Três ocorrências de um tipo, seguida por três de outro."""
    padroes_encontrados = []
    if len(seq) < 6: return padroes_encontrados
    for i in range(len(seq) - 5):
        if seq[i] == seq[i+1] == seq[i+2] and seq[i+3] == seq[i+4] == seq[i+5] and seq[i] != seq[i+3]:
            padroes_encontrados.append(f"Padrão 3x3 detectado: '{seq[i]}' (3x) seguido por '{seq[i+3]}' (3x) na posição {i+1}.")
    return padroes_encontrados


# --- Funções de Sugestão ---
def gerar_sugestoes(sequence_list, resultados_encontrados):
    sugestoes = []
    possibilidades_empate = []
    ultima_ocorrencia = sequence_list[-1] if sequence_list else None
    penultima_ocorrencia = sequence_list[-2] if len(sequence_list) >= 2 else None

    # Sugestões baseadas nos padrões detectados
    if resultados_encontrados.get("1. Sequência (Surf de Cor)"):
        for res in resultados_encontrados["1. Sequência (Surf de Cor)"]:
            # Se a última ocorrência faz parte de uma sequência de surf, sugere continuar
            if ultima_ocorrencia and f"Sequência de '{ultima_ocorrencia}'" in res and res.endswith(f"posição {len(sequence_list)-2}."):
                sugestoes.append(f"**Sugestão:** Continuar o 'Surf de Cor' de **'{ultima_ocorrencia}'**.")

    if resultados_encontrados.get("2. Zig-Zag"):
        # Verifica se o padrão Zig-Zag está nos últimos 2-4 elementos
        if ultima_ocorrencia and penultima_ocorrencia and len(sequence_list) >= 2:
            # Check for CV or VC ending
            if (penultima_ocorrencia == 'C' and ultima_ocorrencia == 'V') or \
               (penultima_ocorrencia == 'V' and ultima_ocorrencia == 'C'):
                # Check for longer zigzag before the last two, e.g., CVCVC
                if len(sequence_list) >= 4 and sequence_list[-4] == penultima_ocorrencia and sequence_list[-3] == ultima_ocorrencia:
                    sugestoes.append(f"**Sugestão:** Continuar o 'Zig-Zag' com **'{penultima_ocorrencia}'**.")


    if resultados_encontrados.get("3. Quebra de Surf"):
        if ultima_ocorrencia and len(sequence_list) >= 4 and \
           sequence_list[-4] == sequence_list[-3] == sequence_list[-2] and \
           ultima_ocorrencia != sequence_list[-4]:
            sugestoes.append(f"**Atenção:** 'Quebra de Surf' recente. O último foi '{ultima_ocorrencia}'.")

    if resultados_encontrados.get("4. Quebra de Zig-Zag"):
        if ultima_ocorrencia and len(sequence_list) >= 4 and \
           ( (sequence_list[-4] == sequence_list[-2] and sequence_list[-3] != sequence_list[-4] and sequence_list[-3] == ultima_ocorrencia and sequence_list[-1] != sequence_list[-3]) or \
             (sequence_list[-4] != sequence_list[-3] and sequence_list[-3] == sequence_list[-1] and sequence_list[-2] != sequence_list[-3] and ultima_ocorrencia != sequence_list[-2]) ):
            sugestoes.append(f"**Atenção:** 'Quebra de Zig-Zag' recente. Próximo pode não seguir a alternância original.")

    if resultados_encontrados.get("5. Duplas repetidas"):
        if ultima_ocorrencia and penultima_ocorrencia and \
           len(sequence_list) >= 4 and \
           sequence_list[-4] == sequence_list[-3] and \
           penultima_ocorrencia == ultima_ocorrencia and \
           sequence_list[-4] != ultima_ocorrencia:
            sugestoes.append(f"**Considerar:** Padrão de 'Duplas Repetidas' (Ex: AABB). Pode haver uma nova dupla ou quebra de padrão.")

    if resultados_encontrados.get("6. Empate recorrente"):
        if resultados_en
