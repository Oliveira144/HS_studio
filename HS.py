import streamlit as st
from collections import deque

# Configuração da página
st.set_page_config(page_title="Football Studio HS", layout="wide")
st.markdown("<h2 style='text-align: center; color: white;'>⚽ Football Studio HS — Análise Inteligente</h2>", unsafe_allow_html=True)

# Cores e rótulos
COLORS = {"C": "🔴", "V": "🔵", "E": "🟡"}
LABELS = {"C": "Casa", "V": "Visitante", "E": "Empate"}

# Histórico até 200
if "historico" not in st.session_state:
    st.session_state.historico = deque(maxlen=200)

# Exibir histórico em blocos de 9 (mais recentes em cima, esquerda para direita)
def mostrar_historico(historico):
    h = list(historico)
    blocos = [h[i:i+9] for i in range(0, len(h), 9)]
    blocos = blocos[::-1]  # Mais recentes primeiro

    for idx, linha in enumerate(blocos):
        st.markdown(
            f"<div style='text-align: center; margin-bottom: 4px;'>"
            f"<span style='color: gray; font-size: 13px;'>Bloco {len(blocos)-idx}</span></div>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<div style='display: flex; justify-content: center; gap: 6px; margin-bottom: 6px;'>"
            + "".join(
                f"<div style='font-size: 22px; width: 30px; height: 30px; text-align: center;'>{COLORS.get(c, '')}</div>"
                for c in linha
            )
            + "</div>",
            unsafe_allow_html=True
        )

# Detectar padrões
def analisar_padroes(h):
    h = list(h)
    padroes = []

    # 1. Surf de Cor
    for i in range(len(h) - 2):
        if h[i] == h[i + 1] == h[i + 2]:
            padroes.append(("Surf de Cor", f"Entrar em {LABELS[h[i]]}", 85))

    # 2. Quebra de Surf
    for i in range(len(h) - 3):
        if h[i] == h[i + 1] == h[i + 2] and h[i + 3] != h[i]:
            padroes.append(("Quebra de Surf", f"Entrar em {LABELS[h[i + 3]]}", 70))

    # 3. Zig-Zag
    for i in range(len(h) - 3):
        if h[i] != h[i + 1] and h[i + 1] != h[i + 2] and h[i + 2] != h[i + 3]:
            padroes.append(("Zig-Zag", f"Entrar em {LABELS[h[i + 3]]}", 75))

    # 4. Padrão 3x1
    for i in range(len(h) - 3):
        if h[i] == h[i+1] == h[i+2] and h[i+3] != h[i]:
            padroes.append(("Padrão 3x1", f"Inversão — entrar em {LABELS[h[i+3]]}", 71))

    # 5. Padrão 3x3
    for i in range(len(h) - 5):
        if h[i] == h[i+1] == h[i+2] and h[i+3] == h[i+4] == h[i+5] and h[i] != h[i+3]:
            padroes.append(("Padrão 3x3", f"Alternância — possível entrada em {LABELS[h[i+5]]}", 77))

    # 6. Padrão Espelhado (cores diferentes)
    for i in range(len(h) - 5):
        bloco1 = h[i:i+3]
        for j in range(i+3, len(h) - 2):
            bloco2 = h[j:j+3]
            if bloco1[0] == bloco1[1] == bloco1[2] and bloco2[0] == bloco2[1] == bloco2[2] and bloco1[0] != bloco2[0]:
                padroes.append(("Padrão Espelhado", f"Nova sequência em {LABELS[bloco2[0]]}", 72))

    # 7. Últimos 5 Frequentes
    if len(h) >= 5:
        ultimos5 = h[-5:]
        mais_freq = max(set(ultimos5), key=ultimos5.count)
        freq = ultimos5.count(mais_freq)
        if freq >= 3:
            padroes.append(("Últimos 5", f"Alta frequência de {LABELS[mais_freq]} ({freq}x)", 70))

    # 8. Surf parcial (2x)
    for i in range(len(h) - 1):
        if h[i] == h[i + 1]:
            padroes.append(("Surf Parcial", f"Possível continuação em {LABELS[h[i]]}", 68))

    # 9. Loop + Quebra
    for i in range(len(h) - 4):
        if h[i] == h[i+2] and h[i+1] == h[i+3] and h[i] != h[i+1] and h[i+4] != h[i]:
            padroes.append(("Loop com Quebra", f"Entrada em {LABELS[h[i+4]]}", 69))

    # 10. Surf com empate no meio
    for i in range(len(h) - 3):
        if h[i] == h[i+2] and h[i+1] == "E" and h[i] != "E":
            padroes.append(("Surf com Empate no meio", f"Provável retorno {LABELS[h[i]]}", 67))

    # 11. 2x2 Invertido
    for i in range(len(h) - 3):
        if h[i] == h[i+1] and h[i+2] == h[i+3] and h[i] != h[i+2]:
            padroes.append(("2x2 Invertido", f"Inversão — próxima pode ser {LABELS[h[i]]}", 73))

    # 12. Espelho com inversão
    for i in range(len(h) - 5):
        if h[i] == h[i+1] == h[i+2] and h[i+3] != h[i] and h[i+4] != h[i] and h[i+5] == h[i]:
            padroes.append(("Espelho com Inversão", f"Entrada oposta a {LABELS[h[i]]}", 74))

    # 13. Sequência alternada com empate no fim
    for i in range(len(h) - 3):
        if h[i] != h[i+1] and h[i+1] != h[i+2] and h[i+2] == "E":
            padroes.append(("Zig-Zag com empate", f"Cuidado: possível empate repetido", 66))

    return padroes

# 📈 Sugestão com base no padrão mais forte
st.subheader("📈 Sugestão Inteligente de Entrada")
if len(st.session_state.historico) >= 9:
    padroes = analisar_padroes(list(st.session_state.historico))
    if padroes:
        padrao_mais_forte = max(padroes, key=lambda x: x[2])
        nome, acao, confianca = padrao_mais_forte
        st.success(f"📌 {nome} — 💡 {acao} — 🎯 Confiança: {confianca}%")
    else:
        st.info("Nenhum padrão forte detectado no momento.")
else:
    st.warning("Insira ao menos 9 resultados para iniciar a análise.")

# 🎮 Inserção de resultados
st.subheader("🎮 Inserir Resultado")
c1, c2, c3 = st.columns(3)
if c1.button("🔴 Casa"):
    st.session_state.historico.append("C")
if c2.button("🔵 Visitante"):
    st.session_state.historico.append("V")
if c3.button("🟡 Empate"):
    st.session_state.historico.append("E")

# 📜 Exibir histórico
st.subheader("📜 Histórico (blocos de 9, recentes em cima)")
mostrar_historico(st.session_state.historico)

# Botões de controle
cl1, cl2 = st.columns(2)
if cl1.button("↩️ Desfazer último"):
    if st.session_state.historico:
        st.session_state.historico.pop()
if cl2.button("🧹 Limpar tudo"):
    st.session_state.historico.clear()

# Rodapé
st.markdown("<hr><p style='text-align: center; font-size: 14px;'>Desenvolvido com ❤️ por IA — Football Studio HS</p>", unsafe_allow_html=True)
