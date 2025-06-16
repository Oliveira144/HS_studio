# Football Studio HS - Análise completa de padrões avançados
import streamlit as st

# Configuração da página
st.set_page_config(page_title="Football Studio HS", layout="centered")
MAX_HISTORY = 50
RESULTADOS_POR_LINHA = 9

# Sessão
if "history" not in st.session_state:
    st.session_state.history = []

# Mapas
color_map = {"Casa": "red", "Visitante": "blue", "Empate": "orange"}
emoji_map = {"Casa": "🔴", "Visitante": "🔵", "Empate": "🟡"}

# Padrões avançados
def detectar_sequencia(hist):
    if len(hist) < 3: return None
    ultima = hist[-1]
    count = 1
    for i in range(len(hist) - 2, -1, -1):
        if hist[i] == ultima:
            count += 1
        else:
            break
    if count >= 3:
        return f"🔁 Sequência de {count}x {ultima}. Sugestão: manter entrada em **{ultima}**."
    return None

def detectar_zigzag(hist):
    if len(hist) < 4: return None
    ultimos = hist[-4:]
    if ultimos[0] != ultimos[1] and ultimos[0] == ultimos[2] and ultimos[1] == ultimos[3]:
        return f"⚡ Zig-Zag identificado. Sugestão: apostar em **{ultimos[2]}**."
    return None

def detectar_quebra_de_surf(hist):
    if len(hist) < 4: return None
    cor = hist[-2]
    if hist[-1] != cor and hist[-3] == cor and hist[-4] == cor:
        return f"⛔ Quebra de Surf: {cor} foi interrompido. Sugestão: evitar entrada até novo padrão claro."
    return None

def detectar_dupla_repetida(hist):
    if len(hist) < 6: return None
    ultimos = hist[-6:]
    padrao = [ultimos[i] == ultimos[i+1] for i in range(0,5,2)]
    if all(padrao):
        sugestao = hist[-1]
        return f"🔁 Padrão de Duplas detectado. Sugestão: seguir com **{sugestao}**."
    return None

def detectar_espelho(hist):
    if len(hist) < 4: return None
    if hist[-4] == hist[-1] and hist[-3] == hist[-2] and hist[-2] != hist[-1]:
        return f"🔄 Padrão Espelho identificado. Sugestão: repetir início do espelho com **{hist[-4]}**."
    return None

def detectar_empate_repetido(hist):
    if len(hist) < 5: return None
    empates = [i for i in range(len(hist)) if hist[i] == "Empate"]
    if len(empates) >= 2 and (empates[-1] - empates[-2]) <= 3:
        return "🟡 Empates frequentes detectados. Sugestão: considerar entrada para **Empate**."
    return None

def detectar_escada(hist):
    if len(hist) < 6: return None
    grupos = []
    count = 1
    for i in range(len(hist)-2, -1, -1):
        if hist[i] == hist[i+1]:
            count += 1
        else:
            grupos.append(count)
            count = 1
    grupos.append(count)
    if grupos[:3] == [1,2,3] or grupos[:3] == [3,2,1]:
        return "📶 Padrão Escada detectado. Sugestão: repetir escada ou inverter."
    return None

def detectar_alternancia_com_empate(hist):
    if len(hist) < 3: return None
    if hist[-2] == "Empate" and hist[-1] != hist[-3]:
        return f"⚠️ Alternância com Empate detectada. Sugestão: possível entrada para **{hist[-1]}**."
    return None

def detectar_surf(hist):
    if len(hist) < 4: return None
    ultima = hist[-1]
    count = 1
    for i in range(len(hist)-2, -1, -1):
        if hist[i] == ultima:
            count += 1
        else:
            break
    if count >= 4:
        return f"🌊 Surf longo de {count}x {ultima}. Sugeridas 3 entradas na mesma cor: **{ultima}**."
    return None

# Junta tudo
def analisar_todos_os_padroes(hist):
    padroes = [
        detectar_sequencia,
        detectar_zigzag,
        detectar_quebra_de_surf,
        detectar_dupla_repetida,
        detectar_espelho,
        detectar_empate_repetido,
        detectar_escada,
        detectar_alternancia_com_empate,
        detectar_surf
    ]
    analises = []
    for func in padroes:
        r = func(hist)
        if r:
            analises.append(r)
    return analises

# Inserção
st.markdown("### 🎯 Inserir novo resultado")
col1, col2, col3 = st.columns(3)
if col1.button("🔴 Casa"): st.session_state.history.append("Casa")
if col2.button("🔵 Visitante"): st.session_state.history.append("Visitante")
if col3.button("🟡 Empate"): st.session_state.history.append("Empate")

# Limita histórico
if len(st.session_state.history) > MAX_HISTORY:
    st.session_state.history = st.session_state.history[-MAX_HISTORY:]

# Análise
st.markdown("### 🔍 Padrões Detectados")
resultados = analisar_todos_os_padroes(st.session_state.history)
if resultados:
    for r in resultados:
        st.success(r)
else:
    st.info("Nenhum padrão forte detectado no momento.")

# Botão reset
if st.button("🧹 Zerar histórico"):
    st.session_state.history.clear()
    st.experimental_rerun()

# Exibe histórico no final, em linha de 9
st.markdown("### 📜 Histórico de Resultados")
if st.session_state.history:
    linhas = [st.session_state.history[i:i + RESULTADOS_POR_LINHA]
              for i in range(0, len(st.session_state.history), RESULTADOS_POR_LINHA)]
    for linha in linhas:
        cols = st.columns(len(linha))
        for i, res in enumerate(linha):
            with cols[i]:
                st.markdown(
                    f"<div style='text-align:center; font-size:26px; color:{color_map[res]}'>{emoji_map[res]}</div>",
                    unsafe_allow_html=True
                )
else:
    st.info("Nenhum resultado inserido.")
