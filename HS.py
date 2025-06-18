import streamlit as st
from collections import deque

# Configuração inicial
st.set_page_config(page_title="Football Studio HS", layout="wide")
st.markdown("<h2 style='text-align: center; color: white;'>⚽ Futebol - Análise Inteligente</h2>", unsafe_allow_html=True)

# Cores e rótulos
COLORS = {"C": "🔴", "V": "🔵", "E": "🟡"}
LABELS = {"C": "Casa", "V": "Visitante", "E": "Empate"}

# Histórico dos resultados (máximo de 200)
if "historico" not in st.session_state:
    st.session_state.historico = deque(maxlen=200)

# Função para mostrar o histórico em blocos de 9 (em linha, mais recentes acima)
def mostrar_historico(historico):
    blocos = [list(historico)[i:i + 9] for i in range(0, len(historico), 9)]
    blocos = blocos[::-1]  # Mostrar os mais recentes no topo
    for linha in blocos:
        colunas = st.columns(len(linha))
        for i, r in enumerate(linha):
            colunas[i].markdown(f"<h3 style='text-align: center'>{COLORS[r]}</h3>", unsafe_allow_html=True)

# Detecta padrões em qualquer parte do histórico
def analisar_padroes(h):
    h = list(h)
    padroes = []

    # Surf de Cor (4 ou mais)
    for i in range(len(h) - 3):
        if h[i] == h[i + 1] == h[i + 2] == h[i + 3]:
            padroes.append(("Surf de Cor", f"Entrar em {LABELS[h[i]]}", 85))

    # Quebra de Surf
    for i in range(len(h) - 4):
        if h[i] == h[i + 1] == h[i + 2] == h[i + 3] and h[i + 4] != h[i]:
            padroes.append(("Quebra de Surf", f"Entrar em {LABELS[h[i + 4]]}", 70))

    # Zig-Zag
    for i in range(len(h) - 3):
        if h[i] != h[i + 1] and h[i + 1] != h[i + 2] and h[i + 2] != h[i + 3]:
            padroes.append(("Zig-Zag", f"Entrar em {LABELS[h[i + 3]]}", 75))

    # Padrões Reversos por cor
    for i in range(len(h) - 5):
        bloco1 = h[i:i+3]
        for j in range(i+3, len(h) - 2):
            bloco2 = h[j:j+3]
            if bloco1[0] == bloco1[1] == bloco1[2] and bloco2[0] == bloco2[1] == bloco2[2] and bloco1[0] != bloco2[0]:
                padroes.append(("Padrão Espelhado com Cores", f"Nova sequência em {LABELS[bloco2[0]]}", 72))

    # Padrão últimos 5
    if len(h) >= 5:
        ultimos5 = h[:5]
        mais_freq = max(set(ultimos5), key=ultimos5.count)
        freq = ultimos5.count(mais_freq)
        if freq >= 3:
            padroes.append(("Padrão últimos 5", f"Alta frequência de {LABELS[mais_freq]} nos últimos 5 ({freq}x)", 70))

    # Padrão 3x1
    for i in range(len(h) - 3):
        if h[i] == h[i + 1] == h[i + 2] and h[i + 3] != h[i]:
            padroes.append(("Padrão 3x1", f"Possível inversão — entrar em {LABELS[h[i + 3]]}", 71))

    # Padrão 3x3
    for i in range(len(h) - 5):
        if h[i] == h[i + 1] == h[i + 2] and h[i + 3] == h[i + 4] == h[i + 5] and h[i] != h[i + 3]:
            padroes.append(("Padrão 3x3", f"Alternância forte — considerar entrada em {LABELS[h[i + 5]]}", 77))

    return padroes

# Sugestões de entrada (somente se houver pelo menos 9 resultados)
st.subheader("📈 Sugestões de Entrada")
if len(st.session_state.historico) >= 9:
    padroes = analisar_padroes(st.session_state.historico)
    if padroes:
        padrao_mais_forte = max(padroes, key=lambda x: x[2])
        nome, acao, confianca = padrao_mais_forte
        st.success(f"📌 {nome} — 💡 {acao} — 🎯 Confiança: {confianca}%")
    else:
        st.info("Nenhum padrão forte detectado no momento.")
else:
    st.warning("⚠️ Aguarde pelo menos 9 resultados para iniciar a análise.")

# Interface de entrada
st.subheader("🎮 Inserir Resultado")
c1, c2, c3 = st.columns(3)
if c1.button("🔴 Casa"):
    st.session_state.historico.appendleft("C")
if c2.button("🔵 Visitante"):
    st.session_state.historico.appendleft("V")
if c3.button("🟡 Empate"):
    st.session_state.historico.appendleft("E")

# Exibe histórico de forma organizada
st.subheader("📜 Histórico de Resultados (linhas de 9)")
mostrar_historico(st.session_state.historico)

# Botões de controle
cl1, cl2 = st.columns(2)
if cl1.button("↩️ Desfazer último"):
    if st.session_state.historico:
        st.session_state.historico.popleft()
if cl2.button("🧹 Limpar tudo"):
    st.session_state.historico.clear()

# Rodapé
st.markdown("<br><hr><p style='text-align: center;'>Desenvolvido com ❤️ por IA — Football Studio HS</p>", unsafe_allow_html=True)
