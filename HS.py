import streamlit as st
from collections import deque

# Configuração inicial
st.set_page_config(page_title="Football Studio HS", layout="wide")
st.markdown("<h2 style='text-align: center; color: white;'>⚽ Futebol - Análise Inteligente</h2>", unsafe_allow_html=True)

# Cores e rótulos
COLORS = {"C": "🔴", "V": "🔵", "E": "🟡"}
LABELS = {"C": "Casa", "V": "Visitante", "E": "Empate"}

# Histórico (até 200 resultados)
if "historico" not in st.session_state:
    st.session_state.historico = deque(maxlen=200)

# Mostrar histórico: da esquerda p/ direita, linhas de 9, mais recente em cima
def mostrar_historico(historico):
    blocos = [list(historico)[i:i + 9] for i in range(0, len(historico), 9)]
    blocos.reverse()  # mais recente em cima
    for linha in blocos:
        colunas = st.columns(9)
        for i, r in enumerate(linha):
            colunas[i].markdown(f"<h3 style='text-align: center; font-size: 28px'>{COLORS[r]}</h3>", unsafe_allow_html=True)

# Detectar padrões
def analisar_padroes(h):
    h = list(h)
    padroes = []

    if len(h) < 9:
        return padroes  # só começa a sugerir após 9 inserções

    # Surf de Cor (mínimo 4 iguais)
    for i in range(len(h) - 3):
        if h[i] == h[i+1] == h[i+2] == h[i+3]:
            padroes.append(("Surf de Cor", f"Entrar em {LABELS[h[i]]}", 85))

    # Quebra de Surf
    for i in range(len(h) - 4):
        if h[i] == h[i+1] == h[i+2] == h[i+3] and h[i+4] != h[i]:
            padroes.append(("Quebra de Surf", f"Possível inversão para {LABELS[h[i+4]]}", 70))

    # Zig-Zag (alternância)
    for i in range(len(h) - 3):
        if h[i] != h[i+1] and h[i+1] != h[i+2] and h[i+2] != h[i+3]:
            padroes.append(("Zig-Zag", f"Entrar em {LABELS[h[i+3]]}", 75))

    # Padrões Reescritos com Cor Diferente
    for i in range(len(h) - 9):
        bloco1 = h[i:i+3]
        for j in range(i+3, len(h) - 2):
            bloco2 = h[j:j+3]
            if bloco1[0] == bloco1[1] == bloco1[2] and bloco2[0] == bloco2[1] == bloco2[2] and bloco1 != bloco2:
                padroes.append(("Repetição com Cor Diferente", f"Padrão reescrito com {LABELS[bloco2[0]]}", 74))

    # Padrão últimos 5 mais frequente
    if len(h) >= 5:
        ultimos5 = h[:5]
        freq = {x: ultimos5.count(x) for x in set(ultimos5)}
        mais_freq = max(freq, key=freq.get)
        if freq[mais_freq] >= 3:
            padroes.append(("Frequência Alta", f"Alta ocorrência de {LABELS[mais_freq]} ({freq[mais_freq]}x)", 70))

    # Padrão 3x1
    for i in range(len(h) - 3):
        if h[i] == h[i+1] == h[i+2] and h[i+3] != h[i]:
            padroes.append(("Padrão 3x1", f"Inversão esperada para {LABELS[h[i+3]]}", 71))

    # Padrão 3x3
    for i in range(len(h) - 5):
        if h[i] == h[i+1] == h[i+2] and h[i+3] == h[i+4] == h[i+5] and h[i] != h[i+3]:
            padroes.append(("Padrão 3x3", f"Alternância para {LABELS[h[i+5]]}", 77))

    # Empates Recorrentes (mínimo 2 em 5)
    for i in range(len(h) - 4):
        bloco = h[i:i+5]
        if bloco.count("E") >= 2:
            padroes.append(("Empates Frequentes", "Entrar em Empate", 85))

    return padroes

# Sugestão principal (após 9 resultados)
st.subheader("📈 Sugestão de Entrada Inteligente")
padroes = analisar_padroes(st.session_state.historico)
if padroes:
    melhor = max(padroes, key=lambda x: x[2])
    nome, acao, conf = melhor
    st.success(f"📌 {nome} — 💡 {acao} — 🎯 Confiança: {conf}%")
else:
    st.info("🔍 Aguardando mais resultados para análise...")

# Inserção manual de resultados
st.subheader("🎮 Inserir Resultado")
b1, b2, b3 = st.columns(3)
if b1.button("🔴 Casa"):
    st.session_state.historico.appendleft("C")
if b2.button("🔵 Visitante"):
    st.session_state.historico.appendleft("V")
if b3.button("🟡 Empate"):
    st.session_state.historico.appendleft("E")

# Exibir histórico formatado
st.subheader("📜 Histórico (mais recente acima, esquerda → direita)")
mostrar_historico(st.session_state.historico)

# Controles
c1, c2 = st.columns(2)
if c1.button("↩️ Desfazer Último"):
    if st.session_state.historico:
        st.session_state.historico.popleft()
if c2.button("🧹 Limpar Tudo"):
    st.session_state.historico.clear()

# Rodapé
st.markdown("<br><hr><p style='text-align: center;'>Desenvolvido com ❤️ por IA — Football Studio HS</p>", unsafe_allow_html=True)
