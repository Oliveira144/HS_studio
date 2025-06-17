import streamlit as st
from itertools import groupby

st.set_page_config(page_title="Football Studio HS", layout="centered")
st.markdown("<h2 style='text-align: center; color: white;'>⚽ Football Studio HS – Análise Inteligente</h2>", unsafe_allow_html=True)

st.markdown("### 🎮 Inserir resultado:")
col1, col2, col3 = st.columns(3)

# Armazenar os resultados
if "resultados" not in st.session_state:
    st.session_state.resultados = []

# Função para adicionar resultado
def adicionar_resultado(resultado):
    st.session_state.resultados.append(resultado)

# Botões
with col1:
    if st.button("🔴 Casa"):
        adicionar_resultado("C")
with col2:
    if st.button("🔵 Visitante"):
        adicionar_resultado("V")
with col3:
    if st.button("🟡 Empate"):
        adicionar_resultado("E")
        st.markdown("### 🧾 Histórico (últimos resultados em blocos de 9)")

# Função para exibir o histórico formatado
def exibir_historico(cores):
    if not cores:
        st.info("Nenhum resultado inserido ainda.")
        return

    blocos = [cores[i:i + 9] for i in range(0, len(cores), 9)]
    for bloco in blocos:
        linha = ""
        for cor in bloco:
            if cor == "C":
                linha += "🔴 "
            elif cor == "V":
                linha += "🔵 "
            elif cor == "E":
                linha += "🟡 "
        st.markdown(f"<div style='font-size:30px;'>{linha.strip()}</div>", unsafe_allow_html=True)

exibir_historico(st.session_state.resultados)
# Função para detectar padrões no histórico
def detectar_padroes(cores):
    sugestoes = []
    if len(cores) < 4:
        return sugestoes

    ultimos = cores[-10:]

    # Surf de cor
    if len(set(ultimos[-3:])) == 1:
        sugestoes.append(("🌊 Surf detectado", f"Entrar seguindo a cor '{ultimos[-1]}'", 85))

    # Quebra de surf
    if len(ultimos) >= 4 and ultimos[-4] == ultimos[-3] == ultimos[-2] and ultimos[-1] != ultimos[-2]:
        sugestoes.append(("💥 Quebra de Surf", "Sequência quebrada, mudança de padrão", 75))

    # Zig-Zag
    if len(ultimos) >= 4 and ultimos[-1] != ultimos[-2] and ultimos[-2] != ultimos[-3] and ultimos[-3] != ultimos[-4]:
        sugestoes.append(("🔁 Zig-Zag", "Alternância detectada", 70))

    # Duplas repetidas
    if len(ultimos) >= 4 and ultimos[-4] == ultimos[-3] and ultimos[-2] == ultimos[-1]:
        sugestoes.append(("♻️ Duplas repetidas", "Padrão duplo", 75))

    # Empate frequente
    empates = ultimos.count("E")
    if empates >= 3:
        sugestoes.append(("⚠️ Empate frequente", f"{empates} empates recentes", 65))

    # Padrão 3x1
    if len(ultimos) >= 4 and ultimos[-4] == ultimos[-3] == ultimos[-2] and ultimos[-1] != ultimos[-2]:
        sugestoes.append(("🧱 Padrão 3x1", "3 de uma cor e 1 diferente", 60))

    # Padrão 3x3
    if len(ultimos) >= 6 and ultimos[-6] == ultimos[-5] == ultimos[-4] and ultimos[-3] == ultimos[-2] == ultimos[-1] and ultimos[-4] != ultimos[-3]:
        sugestoes.append(("🔳 Padrão 3x3", "Três de uma cor seguidos por três de outra", 80))

    # Padrão Espelho
    if len(ultimos) >= 4 and ultimos[-4:] == ultimos[-4:][::-1]:
        sugestoes.append(("🔄 Espelho", "Reflexo detectado", 68))

    # Alternância com empate no meio (ex: C, E, V)
    if len(ultimos) >= 3 and ultimos[-3] != ultimos[-1] and ultimos[-2] == "E":
        sugestoes.append(("⚖️ Alternância com empate", "Empate entre duas cores diferentes", 60))

    # Padrão Escada
    if len(ultimos) >= 6:
        grupos = [list(g) for k, g in groupby(ultimos)]
        tamanhos = [len(g) for g in grupos]
        if tamanhos == sorted(tamanhos) or tamanhos == sorted(tamanhos, reverse=True):
            sugestoes.append(("📶 Padrão Escada", "Sequência em escadinha", 65))

    # Padrão Onda (1-2-1-2 alternando)
    if len(ultimos) >= 6:
        ondas = [len(list(g)) for k, g in groupby(ultimos)]
        if ondas[-4:] == [1,2,1,2] or ondas[-4:] == [2,1,2,1]:
            sugestoes.append(("🌊 Onda", "Alternância tipo 1-2-1-2 detectada", 72))

    # Análise últimos 5, 7, 10 jogos
    for janela in [5, 7, 10]:
        if len(cores) >= janela:
            bloco = cores[-janela:]
            mais_freq = max(set(bloco), key=bloco.count)
            porcentagem = bloco.count(mais_freq) / janela * 100
            if porcentagem >= 70:
                cor_str = "Casa" if mais_freq == "C" else "Visitante" if mais_freq == "V" else "Empate"
                sugestoes.append((f"📊 Tendência nos últimos {janela}", f"{cor_str} aparece {porcentagem:.0f}% das vezes", int(porcentagem)))

    return sugestoes
    st.markdown("### 🔍 Sugestões de Entrada Inteligente")

# Executa a análise e mostra as sugestões
sugestoes = detectar_padroes(st.session_state.resultados)

if sugestoes:
    for titulo, descricao, confianca in sugestoes:
        st.success(f"**{titulo}**\n\n📌 {descricao} — 🎯 Confiança: {confianca}%")
else:
    st.info("Nenhum padrão relevante detectado no momento.")
    st.markdown("---")
col4, col5 = st.columns(2)

# Botão para desfazer a última jogada
with col4:
    if st.button("↩️ Desfazer última"):
        if st.session_state.resultados:
            st.session_state.resultados.pop()

# Botão para reiniciar tudo
with col5:
    if st.button("🗑️ Limpar tudo"):
        st.session_state.resultados = []

st.markdown("<br><center><small>📊 Desenvolvido com Streamlit – Football Studio HS</small></center>", unsafe_allow_html=True)
