import streamlit as st
from collections import Counter

# st.set_page_config deve vir antes de qualquer comando Streamlit
st.set_page_config(page_title="Analisador de Padrões e Sugestões", layout="wide", initial_sidebar_state="expanded")

# --- Injeção de CSS para Estilização Geral (Não foca nos botões de entrada) ---
st.markdown("""
<style>
/* Estilo para o título de resultados e sugestões */
h3 {
    color: #FFD700; /* Dourado para títulos */
    margin-top: 20px;
    margin-bottom: 15px;
}

/* Estilo para os alertas/caixas de informação (sugestões, possibilidades de empate) */
div[data-testid="stAlert"] {
    background-color: #282828 !important; /* Fundo mais escuro */
    color: white !important; /* Texto branco */
    border-left: 5px solid #FFD700 !important; /* Borda dourada */
    padding: 10px !important;
    margin-bottom: 10px !important;
    border-radius: 5px !important;
}
div[data-testid="stAlert"] svg {
    color: #FFD700 !important; /* Ícone dourado */
}
div[data-testid="stAlert"] div[role="alert"] p {
    color: white !important;
}

/* Estilo para o bloco de código (sequência atual e histórico) */
div.stCodeBlock {
    background-color: #202020 !important;
    color: #00FF00 !important; /* Pode ser branco ou outra cor de texto se preferir */
    border-radius: 5px !important;
    padding: 10px !important;
    font-family: 'monospace' !important;
    overflow-x: auto !important; /* Permite scroll horizontal se a sequência for muito longa */
    white-space: pre !important; /* Mantém formatação de espaços e quebras de linha */
}

/* Ajustes gerais de espaçamento, se necessário */
.st-emotion-cache-k3g099 { /* Este seletor pode mudar entre versões do Streamlit, é para colunas */
    gap: 1rem !important; /* Garante espaçamento entre as colunas */
}

</style>
""", unsafe_allow_html=True)


# --- Inicialização do Session State ---
# Variáveis para armazenar o estado da aplicação
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


# --- Funções de Detecção de Padrões (COMPLETAS) ---

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
            if j - i >= 4: # Pelo menos 2 pares para ser um zig-zag reconhecível
                padroes_encontrados.append(f"Padrão Zig-Zag detectado: {seq[i:j]} iniciando na posição {i+1}.")
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
        # Verifica se é um zig-zag de 3 elementos (A, B, A) e o 4º elemento (C) quebra (C != A e C != B)
        if seq[i] != seq[i+1] and seq[i+1] != seq[i+2] and seq[i] == seq[i+2] and \
           seq[i+3] != seq[i] and seq[i+3] != seq[i+1]:
             padroes_encontrados.append(f"Quebra de Zig-Zag detectada: {seq[i:i+3]} interrompido por '{seq[i+3]}' na posição {i+4}.")
    return padroes_encontrados

def detectar_duplas_repetidas(seq):
    """5. Duplas repetidas – Casa, Casa, Visitante, Visitante... (AABB)"""
    padroes_encontrados = []
    if len(seq) < 4: return padroes_encontrados
    for i in range(len(seq) - 3):
        if seq[i] == seq[i+1] and seq[i+2] == seq[i+3] and seq[i] != seq[i+2]:
            padroes_encontrados.append(f"Duplas Repetidas detectadas: '{seq[i]}', '{seq[i+2]}' iniciando na posição {i+1}.")
    return padroes_encontrados

def detectar_empate_recorrente(seq, empate_char='E'):
    """6. Empate recorrente – Empates aparecendo em intervalos curtos (2 ou 3 resultados entre empates)"""
    padroes_encontrados = []
    indices_empate = [i for i, x in enumerate(seq) if x == empate_char]
    if len(indices_empate) < 2: return padroes_encontrados
    for i in range(len(indices_empate) - 1):
        diff = indices_empate[i+1] - indices_empate[i]
        # Se a diferença for 2 (E X E) ou 3 (E X Y E)
        if diff >= 2 and diff <= 3:
            padroes_encontrados.append(f"Empate Recorrente detectado entre posições {indices_empate[i]+1} e {indices_empate[i+1]+1} (intervalo de {diff-1} não-empates).")
    return padroes_encontrados

def detectar_padrao_escada(seq):
    """7. Padrão Escada – Ex: 1 Casa, 2 Visitantes, 3 Casas (ABABBB ou similar, adaptado)"""
    padroes_encontrados = []
    if len(seq) < 6: return padroes_encontrados
    for i in range(len(seq) - 5):
        # Exemplo de escada: A
