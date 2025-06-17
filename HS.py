import streamlit as st
from collections import deque

# Configuração da página
st.set_page_config(page_title="Football Studio HS", layout="wide")
st.markdown("<h2 style='text-align: center; color: white;'>⚽ Football Studio HS – Análise Inteligente</h2>", unsafe_allow_html=True)

# Dicionários de ícones e nomes
CORES = {"C": "🔴", "V": "🔵", "E": "🟡"}
NOMES = {"C": "Casa", "V": "Visitante", "E": "Empate"}

# Histórico
if "historico" not in st.session_state:
    st.session_state.historico = deque(maxlen=50)

# Inserção de resultado
st.subheader("🎮 Inserir resultado:")
col1, col2, col3 = st.columns(3)
if col1.button("🔴 Casa"):
    st.session_state.historico.append("C")
if col2.button("🔵 Visitante"):
    st.session_state.historico.append("V")
if col3.button("🟡 Empate"):
    st.session_state.historico.append("E")

# Exibir histórico em linhas de 9 (esquerda para direita)
st.subheader("📜 Histórico (9 por linha)")
def exibir_historico():
    lista = list(st.session_state.historico)
    linhas = [lista[i:i+9] for i in range(0, len(lista), 9)]
    for linha in linhas:
        cols = st.columns(9)
        for i, valor in enumerate(linha):
            cols[i].markdown(f"<h3 style='text-align: center'>{CORES[valor]}</h3>", unsafe_allow_html=True)

exibir_historico()

# Análise de padrões
def analisar_padroes(h):
    h = list(h)
    padroes = []
    if len(h) >= 3 and h[-1] == h[-2] == h[-3]:
        padroes.append(("Surf de Cor", f"Entrar em {NOMES[h[-1]]}", 85))
    if len(h) >= 4 and h[-1] != h[-2] and h[-2] != h[-3] and h[-3] != h[-4]:
        padroes.append(("Zig-Zag", f"Entrar em {NOMES[h[-1]]}", 75))
    if len(h) >= 4 and h[-1] != h[-2] and h[-2] == h[-3] == h[-4]:
        padroes.append(("Quebra de Surf", f"Entrar em {NOMES[h[-1]]}", 70))
    if len(h) >= 4 and h[-1] == h[-2] == h[-3] and h[-4] != h[-3]:
        padroes.append(("Quebra de Zig-Zag", f"Entrar em {NOMES[h[-1]]}", 68))
    if len(h) >= 4 and h[-4] == h[-3] and h[-2] == h[-1] and h[-4] != h[-2]:
        padroes.append(("Duplas Repetidas", f"Entrar em {NOMES[h[-1]]}", 72))
    if h.count("E") >= 3:
        padroes.append(("Empate Recorrente", "Empates frequentes, considerar evitar entrada", 65))
    if len(h) >= 6 and h[-6] != h[-5] and h[-5] == h[-4] and h[-3] == h[-2] and h[-1] != h[-2]:
        padroes.append(("Padrão Escada", f"Tendência crescente em {NOMES[h[-2]]}", 64))
    if len(h) >= 4 and h[-4] == h[-1] and h[-3] == h[-2]:
        padroes.append(("Espelho", f"Padrão reflexivo — considerar {NOMES[h[-1]]}", 68))
    if len(h) >= 3 and h[-3] != h[-2] and h[-2] == "E" and h[-1] != "E":
        padroes.append(("Alternância com Empate no meio", f"Possível inversão — entrar em {NOMES[h[-1]]}", 66))
    if len(h) >= 4 and h[-4] != h[-3] and h[-3] == h[-2] and h[-2] != h[-1]:
        padroes.append(("Padrão Onda", f"Entrada em {NOMES[h[-1]]} por onda reversa", 63))
    if len(h) >= 5:
        ultimos5 = h[-5:]
        freq = {v: ultimos5.count(v) for v in set(ultimos5)}
        mais_freq = max(freq, key=freq.get)
        if freq[mais_freq] >= 3:
            padroes.append(("Padrão últimos 5", f"Alta frequência de {NOMES[mais_freq]} nos últimos 5 ({freq[mais_freq]}x)", 70))
    if len(h) >= 4 and h[-4] == h[-3] == h[-2] and h[-1] != h[-2]:
        padroes.append(("Padrão 3x1", f"Possível inversão — entrar em {NOMES[h[-1]]}", 71))
    if len(h) >= 6 and h[-6] == h[-5] == h[-4] and h[-3] == h[-2] == h[-1] and h[-6] != h[-3]:
        padroes.append(("Padrão 3x3", f"Alternância forte — considerar entrada em {NOMES[h[-1]]}", 77))
    return padroes

# Exibir sugestões
st.subheader("📈 Sugestões de entrada")
padroes = analisar_padroes(st.session_state.historico)
if padroes:
    for nome, acao, conf in padroes:
        st.success(f"📌 {nome} — 💡 {acao} — 🎯 Confiança: {conf}%")
else:
    st.info("Nenhum padrão forte detectado no momento.")

# Ações extras
colA, colB = st.columns(2)
if colA.button("↩️ Desfazer último"):
    if st.session_state.historico:
        st.session_state.historico.pop()
if colB.button("🧹 Limpar histórico"):
    st.session_state.historico.clear()

# Rodapé
st.markdown("<hr><center>Desenvolvido com ❤️ por IA — Football Studio HS</center>", unsafe_allow_html=True)
