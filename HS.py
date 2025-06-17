import streamlit as st
from collections import deque

# Configuração inicial
st.set_page_config(page_title="Football Studio HS", layout="wide")
st.title("🎯 Futebol - Análise Inteligente")

# Cores e rótulos
COLORS = {"C": "🔴", "V": "🔵", "E": "🟡"}
LABELS = {"C": "Casa", "V": "Visitante", "E": "Empate"}

# Histórico de resultados
if "historico" not in st.session_state:
    st.session_state.historico = deque(maxlen=50)

# Função para mostrar o histórico em linhas de 9
def mostrar_historico(historico):
    linhas = [list(historico)[i:i+9] for i in range(0, len(historico), 9)]
    for linha in linhas:
        st.markdown("".join(f"<span style='font-size:30px'>{COLORS[r]}</span>" for r in linha), unsafe_allow_html=True)

# Detectar padrões
def analisar_padroes(h):
    h = list(h)
    padroes = []

    if len(h) >= 3 and h[0] == h[1] == h[2]:
        padroes.append(("Surf de Cor", f"Entrar em {LABELS[h[0]]}", 85))
    if len(h) >= 4 and h[0] != h[1] and h[1] != h[2] and h[2] != h[3]:
        padroes.append(("Zig-Zag", f"Entrar em {LABELS[h[3]]}", 75))
    if len(h) >= 4 and h[0] == h[1] == h[2] and h[2] != h[3]:
        padroes.append(("Quebra de Surf", f"Entrar em {LABELS[h[3]]}", 70))
    if len(h) >= 4 and h[0] != h[1] and h[1] == h[2] and h[2] == h[3]:
        padroes.append(("Quebra de Zig-Zag", f"Entrar em {LABELS[h[3]]}", 68))
    if len(h) >= 4 and h[0] == h[1] and h[2] == h[3] and h[0] != h[2]:
        padroes.append(("Duplas Repetidas", f"Entrar em {LABELS[h[3]]}", 72))
    if h.count("E") >= 3:
        padroes.append(("Empate Recorrente", "Empates frequentes, considerar evitar entrada", 65))
    if len(h) >= 6 and h[0] != h[1] and h[1] == h[2] and h[3] == h[4] and h[5] != h[4]:
        padroes.append(("Padrão Escada", f"Tendência crescente em {LABELS[h[4]]}", 64))
    if len(h) >= 4 and h[0] == h[3] and h[1] == h[2]:
        padroes.append(("Espelho", f"Padrão reflexivo — considerar {LABELS[h[0]]}", 68))
    if len(h) >= 3 and h[0] != h[1] and h[1] == "E" and h[2] != h[1]:
        padroes.append(("Alternância com Empate no meio", f"Possível inversão — entrar em {LABELS[h[2]]}", 66))
    if len(h) >= 4 and h[0] != h[1] and h[1] == h[2] and h[2] != h[3]:
        padroes.append(("Padrão Onda", f"Entrada em {LABELS[h[3]]} por onda reversa", 63))
    if len(h) >= 5:
        ultimos5 = h[:5]
        mais_freq = max(set(ultimos5), key=ultimos5.count)
        freq = ultimos5.count(mais_freq)
        if freq >= 3:
            padroes.append(("Padrão últimos 5", f"Alta frequência de {LABELS[mais_freq]} nos últimos 5 ({freq}x)", 70))
    if len(h) >= 4 and h[0] == h[1] == h[2] and h[3] != h[2]:
        padroes.append(("Padrão 3x1", f"Possível inversão — entrar em {LABELS[h[3]]}", 71))
    if len(h) >= 6 and h[0] == h[1] == h[2] and h[3] == h[4] == h[5] and h[0] != h[3]:
        padroes.append(("Padrão 3x3", f"Alternância forte — considerar entrada em {LABELS[h[5]]}", 77))

    return padroes

# Sugestão principal
st.subheader("📈 Sugestão de Entrada")

padroes = analisar_padroes(st.session_state.historico)

if padroes:
    melhor_padrao = max(padroes, key=lambda x: x[2])
    nome, acao, confianca = melhor_padrao
    st.success(f"📌 **{nome}**\n\n💡 {acao}\n\n🎯 **Confiança: {confianca}%**")
else:
    st.info("Nenhum padrão forte detectado no momento.")

# Interface de entrada
st.subheader("🎮 Inserir Resultado")
c1, c2, c3 = st.columns(3)
if c1.button("🔴 Casa"):
    st.session_state.historico.appendleft("C")
if c2.button("🔵 Visitante"):
    st.session_state.historico.appendleft("V")
if c3.button("🟡 Empate"):
    st.session_state.historico.appendleft("E")

# Histórico de resultados
st.subheader("📜 Histórico de Resultados (linhas de 9, ordem real)")
mostrar_historico(st.session_state.historico)

# Botões auxiliares
cl1, cl2 = st.columns(2)
if cl1.button("↩️ Desfazer último"):
    if st.session_state.historico:
        st.session_state.historico.popleft()
if cl2.button("🧹 Limpar tudo"):
    st.session_state.historico.clear()

# Rodapé
st.markdown("""
Desenvolvido com ❤️ por IA — Football Studio HS
""", unsafe_allow_html=True)
