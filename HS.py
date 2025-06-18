import streamlit as st
from collections import deque

# Configuração inicial
st.set_page_config(page_title="Football Studio HS", layout="wide")
st.markdown("<h2 style='text-align: center; color: white;'>⚽ Futebol - Análise Inteligente</h2>", unsafe_allow_html=True)

# Cores e rótulos
COLORS = {"C": "🔴", "V": "🔵", "E": "🟡"}
LABELS = {"C": "Casa", "V": "Visitante", "E": "Empate"}

# Histórico dos resultados (até 200)
if "historico" not in st.session_state:
    st.session_state.historico = deque(maxlen=200)

# Mostrar histórico: da esquerda p/ direita, linhas de 9, mais novo acima
def mostrar_historico(historico):
    h = list(historico)
    blocos = [h[i:i + 9] for i in range(0, len(h), 9)]
    blocos.reverse()  # Mostrar do mais novo para o mais antigo
    for linha in blocos:
        colunas = st.columns(9)
        for i, r in enumerate(linha):
            if i < len(colunas):
                colunas[i].markdown(f"<h3 style='text-align: center; font-size: 28px'>{COLORS[r]}</h3>", unsafe_allow_html=True)

# Detectar padrões e calcular confiança
def analisar_padroes(h):
    h = list(h)
    padroes = []

    if len(h) < 9:
        return []

    ultimos_27 = h[:27] if len(h) >= 27 else h

    # Surf de Cor
    for i in range(len(h) - 3):
        if h[i] == h[i+1] == h[i+2] == h[i+3]:
            padroes.append(("Surf de Cor", f"Entrar em {LABELS[h[i]]}", 85))

    # Quebra de Surf
    for i in range(len(h) - 4):
        if h[i] == h[i+1] == h[i+2] == h[i+3] and h[i+4] != h[i]:
            padroes.append(("Quebra de Surf", f"Entrar em {LABELS[h[i+4]]}", 70))

    # Zig-Zag
    for i in range(len(h) - 3):
        if h[i] != h[i+1] and h[i+1] != h[i+2] and h[i+2] != h[i+3]:
            padroes.append(("Zig-Zag", f"Entrar em {LABELS[h[i+3]]}", 75))

    # Padrão espelhado com cor diferente
    for i in range(len(h) - 9):
        bloco1 = h[i:i+3]
        for j in range(i+3, len(h)-2):
            bloco2 = h[j:j+3]
            if bloco1 != bloco2 and all(x == bloco1[0] for x in bloco1) and all(x == bloco2[0] for x in bloco2) and bloco1[0] != bloco2[0]:
                padroes.append(("Padrão Reescrito com Cor Diferente", f"Nova sequência com {LABELS[bloco2[0]]}", 74))

    # Empate recorrente (85% fixo)
    for i in range(len(h) - 4):
        empates = [1 for x in h[i:i+5] if x == "E"]
        if sum(empates) >= 2:
            padroes.append(("Empates recorrentes", "Entrar no Empate", 85))

    # Últimos 9 - frequência
    if len(h) >= 9:
        ultimos9 = h[:9]
        mais_freq = max(set(ultimos9), key=ultimos9.count)
        freq = ultimos9.count(mais_freq)
        if freq >= 4:
            padroes.append(("Frequência recente", f"{LABELS[mais_freq]} aparece {freq}x nos últimos 9", 70 + freq))

    # Padrão 3x1
    for i in range(len(h) - 3):
        if h[i] == h[i+1] == h[i+2] and h[i+3] != h[i]:
            padroes.append(("Padrão 3x1", f"Inversão — entrar em {LABELS[h[i+3]]}", 71))

    # Padrão 3x3
    for i in range(len(h) - 5):
        if h[i] == h[i+1] == h[i+2] and h[i+3] == h[i+4] == h[i+5] and h[i] != h[i+3]:
            padroes.append(("Padrão 3x3", f"Alternância forte — considerar {LABELS[h[i+5]]}", 77))

    return padroes

# Sugestão de Entrada
st.subheader("📈 Sugestão de Entrada Inteligente")
padroes = analisar_padroes(st.session_state.historico)
if padroes:
    melhor = max(padroes, key=lambda x: x[2])
    nome, acao, conf = melhor
    st.success(f"📌 {nome} — 💡 {acao} — 🎯 Confiança: {conf}%")
else:
    st.info("🔎 Aguardando mais resultados para análise...")

# Entrada de resultados
st.subheader("🎮 Inserir Resultado")
c1, c2, c3 = st.columns(3)
if c1.button("🔴 Casa"):
    st.session_state.historico.appendleft("C")
if c2.button("🔵 Visitante"):
    st.session_state.historico.appendleft("V")
if c3.button("🟡 Empate"):
    st.session_state.historico.appendleft("E")

# Exibição do Histórico
st.subheader("📜 Histórico (mais recente acima, esquerda → direita)")
mostrar_historico(st.session_state.historico)

# Controles
col1, col2 = st.columns(2)
if col1.button("↩️ Desfazer Último"):
    if st.session_state.historico:
        st.session_state.historico.popleft()
if col2.button("🧹 Limpar Tudo"):
    st.session_state.historico.clear()

# Rodapé
st.markdown("<br><hr><p style='text-align: center;'>Desenvolvido com ❤️ por IA — Football Studio HS</p>", unsafe_allow_html=True)
