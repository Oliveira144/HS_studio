import streamlit as st
from collections import deque

st.set_page_config(page_title="Football Studio HS", layout="wide")
st.markdown("<h2 style='text-align: center; color: white;'>⚽ Football Studio HS - Análise Inteligente</h2>", unsafe_allow_html=True)

# Cores e rótulos
CORES = {"C": "🔴", "V": "🔵", "E": "🟡"}
NOMES = {"C": "Casa", "V": "Visitante", "E": "Empate"}

# Histórico de resultados (até 200)
if "historico" not in st.session_state:
    st.session_state.historico = deque(maxlen=200)

# Função para mostrar histórico em blocos de 9 (esquerda → direita, mais novo em cima)
def mostrar_historico(hist):
    blocos = [hist[i:i+9] for i in range(0, len(hist), 9)]
    blocos = blocos[::-1]  # Mais recente em cima
    for linha in blocos:
        colunas = st.columns(9)
        for i, resultado in enumerate(linha):
            with colunas[i]:
                st.markdown(f"<div style='font-size:36px; text-align:center'>{CORES[resultado]}</div>", unsafe_allow_html=True)

# Função de análise de padrões
def analisar_padroes(hist):
    padroes = []
    if len(hist) < 9:
        return []

    h = list(hist)

    # Padrão Surf de Cor
    for i in range(len(h) - 3):
        if h[i] == h[i+1] == h[i+2] == h[i+3]:
            padroes.append(("Surf de Cor", f"Entrar em {NOMES[h[i]]}", 85))

    # Quebra de Surf
    for i in range(len(h) - 4):
        if h[i] == h[i+1] == h[i+2] == h[i+3] and h[i+4] != h[i]:
            padroes.append(("Quebra de Surf", f"Entrar em {NOMES[h[i+4]]}", 70))

    # Zig-Zag
    for i in range(len(h) - 3):
        if len(set(h[i:i+4])) == 4:
            padroes.append(("Zig-Zag", f"Entrar em {NOMES[h[i+3]]}", 75))

    # Repetição com cor diferente
    for i in range(len(h) - 6):
        bloco1 = h[i:i+3]
        for j in range(i+3, len(h)-2):
            bloco2 = h[j:j+3]
            if bloco1 != bloco2 and all(x == bloco1[0] for x in bloco1) and all(x == bloco2[0] for x in bloco2) and bloco1[0] != bloco2[0]:
                padroes.append(("Padrão Reescrito com outra cor", f"Nova sequência de {NOMES[bloco2[0]]}", 74))

    # Frequência nos últimos 9
    ultimos9 = h[:9]
    mais_frequente = max(set(ultimos9), key=ultimos9.count)
    contagem = ultimos9.count(mais_frequente)
    if contagem >= 4:
        padroes.append(("Alta Frequência", f"{NOMES[mais_frequente]} aparece {contagem}x", 70 + contagem))

    # Detecção de empates
    if h.count("E") >= 2:
        padroes.append(("Empate recorrente", "Entrar no Empate", 85))

    return padroes

# Sugestão de entrada
st.subheader("📈 Sugestão de Entrada Inteligente")
padroes_detectados = analisar_padroes(st.session_state.historico)
if padroes_detectados:
    melhor = max(padroes_detectados, key=lambda x: x[2])
    st.success(f"🔍 {melhor[0]} — 💡 {melhor[1]} — 🎯 Confiança: {melhor[2]}%")
else:
    st.info("🔎 Aguardando pelo menos 9 resultados para iniciar análise...")

# Inserção de resultados
st.subheader("🎮 Inserir Resultado")
c1, c2, c3 = st.columns(3)
if c1.button("🔴 Casa"):
    st.session_state.historico.appendleft("C")
if c2.button("🔵 Visitante"):
    st.session_state.historico.appendleft("V")
if c3.button("🟡 Empate"):
    st.session_state.historico.appendleft("E")

# Mostrar histórico
st.subheader("📜 Histórico (mais recente acima, esquerda → direita)")
mostrar_historico(list(st.session_state.historico))

# Ações extras
col1, col2 = st.columns(2)
if col1.button("↩️ Desfazer Último"):
    if st.session_state.historico:
        st.session_state.historico.popleft()
if col2.button("🧹 Limpar Tudo"):
    st.session_state.historico.clear()

# Rodapé
st.markdown("<hr><p style='text-align: center;'>🧠 Desenvolvido por IA | Football Studio HS</p>", unsafe_allow_html=True)
