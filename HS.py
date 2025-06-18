import streamlit as st
from collections import deque

# Configuração inicial
st.set_page_config(page_title="Football Studio HS", layout="wide")
st.markdown("<h2 style='text-align: center; color: white;'>⚽ Futebol - Análise Inteligente</h2>", unsafe_allow_html=True)

# Cores e rótulos
COLORS = {"C": "🔴", "V": "🔵", "E": "🟡"}
LABELS = {"C": "Casa", "V": "Visitante", "E": "Empate"}

# Histórico dos resultados
if "historico" not in st.session_state:
    st.session_state.historico = deque(maxlen=200)  # Agora armazena até 200 resultados

# Função para mostrar o histórico em blocos de 9 (em linha horizontal, mais recentes acima)
def mostrar_historico(historico):
    blocos = [list(historico)[i:i + 9] for i in range(0, len(historico), 9)]
    blocos = blocos[::-1]  # Mostra blocos mais recentes acima
    for linha in blocos:
        st.markdown("<div style='display: flex; gap: 10px;'>", unsafe_allow_html=True)
        for r in linha:
            st.markdown(f"<div style='font-size: 30px'>{COLORS[r]}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Função de análise de padrões
def analisar_padroes(h):
    h = list(h)
    padroes = []

    # Surf de Cor (mínimo 4 repetições para ser considerado surf)
    for i in range(len(h) - 3):
        if h[i] == h[i + 1] == h[i + 2] == h[i + 3]:
            padroes.append(("Surf de Cor", f"Entrar em {LABELS[h[i]]}", 88))

    # Quebra de Surf
    for i in range(len(h) - 4):
        if h[i] == h[i + 1] == h[i + 2] == h[i + 3] and h[i + 4] != h[i]:
            padroes.append(("Quebra de Surf", f"Entrar em {LABELS[h[i + 4]]}", 72))

    # Zig-Zag
    for i in range(len(h) - 3):
        if h[i] != h[i + 1] and h[i + 1] != h[i + 2] and h[i + 2] != h[i + 3]:
            padroes.append(("Zig-Zag", f"Entrar em {LABELS[h[i + 3]]}", 75))

    # Quebra de Zig-Zag
    for i in range(len(h) - 4):
        if h[i] != h[i + 1] and h[i + 1] != h[i + 2] and h[i + 2] == h[i + 3] == h[i + 4]:
            padroes.append(("Quebra de Zig-Zag", f"Entrar em {LABELS[h[i + 4]]}", 74))

    # Duplas repetidas
    for i in range(len(h) - 3):
        if h[i] == h[i + 1] and h[i + 2] == h[i + 3] and h[i] != h[i + 2]:
            padroes.append(("Duplas Repetidas", f"Repetição alternada — entrar em {LABELS[h[i + 3]]}", 70))

    # Empate recorrente
    empates = [i for i, val in enumerate(h) if val == "E"]
    if len(empates) >= 2:
        for i in range(len(empates) - 1):
            if empates[i+1] - empates[i] <= 5:
                padroes.append(("Empate recorrente", "Atenção para novo empate", 78))
                break

    # Padrão Espelhado
    for i in range(len(h) - 5):
        bloco1 = h[i:i+3]
        for j in range(i+3, len(h) - 2):
            bloco2 = h[j:j+3]
            if bloco1 == bloco2[::-1] and bloco1[0] != bloco2[0]:
                padroes.append(("Padrão Espelho", f"Possível repetição invertida: {LABELS[bloco2[0]]}", 70))

    # Alternância com empate no meio
    for i in range(len(h) - 2):
        if h[i] != "E" and h[i+1] == "E" and h[i+2] != "E" and h[i] == h[i+2]:
            padroes.append(("Alternância com empate", f"Pode repetir {LABELS[h[i]]}", 73))

    # Padrão últimos 5
    if len(h) >= 5:
        ultimos5 = h[:5]
        mais_freq = max(set(ultimos5), key=ultimos5.count)
        freq = ultimos5.count(mais_freq)
        if freq >= 3:
            padroes.append(("Alta frequência nos últimos 5", f"{LABELS[mais_freq]} apareceu {freq} vezes", 70))

    # Padrão 3x1
    for i in range(len(h) - 3):
        if h[i] == h[i + 1] == h[i + 2] and h[i + 3] != h[i]:
            padroes.append(("Padrão 3x1", f"Inversão esperada: {LABELS[h[i + 3]]}", 71))

    # Padrão 3x3
    for i in range(len(h) - 5):
        if h[i] == h[i + 1] == h[i + 2] and h[i + 3] == h[i + 4] == h[i + 5] and h[i] != h[i + 3]:
            padroes.append(("Padrão 3x3", f"Alternância detectada: {LABELS[h[i + 5]]}", 77))

    return padroes

# Interface: Sugestões de Entrada
if len(st.session_state.historico) >= 9:
    st.subheader("📈 Sugestões de Entrada")
    padroes = analisar_padroes(st.session_state.historico)
    if padroes:
        padrao_mais_forte = max(padroes, key=lambda x: x[2])
        nome, acao, confianca = padrao_mais_forte
        st.success(f"📌 {nome} — 💡 {acao} — 🎯 Confiança: {confianca}%")
    else:
        st.info("Nenhum padrão forte detectado no momento.")
else:
    st.warning("⚠️ Insira ao menos 9 resultados para iniciar a análise.")

# Interface: Inserir Resultado
st.subheader("🎮 Inserir Resultado")
c1, c2, c3 = st.columns(3)
if c1.button("🔴 Casa"):
    st.session_state.historico.appendleft("C")
if c2.button("🔵 Visitante"):
    st.session_state.historico.appendleft("V")
if c3.button("🟡 Empate"):
    st.session_state.historico.appendleft("E")

# Exibição do histórico
st.subheader("📜 Histórico de Resultados (linhas de 9)")
mostrar_historico(st.session_state.historico)

# Controles
cl1, cl2 = st.columns(2)
if cl1.button("↩️ Desfazer último"):
    if st.session_state.historico:
        st.session_state.historico.popleft()
if cl2.button("🧹 Limpar tudo"):
    st.session_state.historico.clear()

# Rodapé
st.markdown("<br><hr><p style='text-align: center;'>Desenvolvido com ❤️ por IA — Football Studio HS</p>", unsafe_allow_html=True)
