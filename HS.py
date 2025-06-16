import streamlit as st

# Configurações iniciais
st.set_page_config(page_title="Football Studio HS", layout="centered")
MAX_HISTORY = 50

# Inicializa histórico na sessão
if "history" not in st.session_state:
    st.session_state.history = []

# Mapas de cor e emoji
color_map = {"Casa": "red", "Visitante": "blue", "Empate": "orange"}
emoji_map = {"Casa": "🔴", "Visitante": "🔵", "Empate": "🟡"}

# Funções de padrão (mesmas do código anterior — posso colar de novo se quiser)
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
        return f"Sequência de {count}x {ultima}. Sugestão: seguir a mesma cor."
    return None

# (Adicione aqui todas as outras funções de padrão, como detectar_surf, zigzag, etc.)

def analisar_todos_os_padroes(hist):
    funcoes = [
        detectar_sequencia,
        # Adicione aqui: detectar_surf, detectar_zigzag, etc.
    ]
    analises = []
    for func in funcoes:
        r = func(hist)
        if r:
            analises.append(r)
    return analises

# Exibe histórico
st.title("🎲 Football Studio HS")
st.subheader("Histórico de resultados")

if st.session_state.history:
    cols = st.columns(len(st.session_state.history))
    for i, cor in enumerate(st.session_state.history):
        with cols[i]:
            st.markdown(
                f"<div style='text-align:center; font-size:22px; color:{color_map[cor]}'>{emoji_map[cor]}</div>",
                unsafe_allow_html=True
            )
else:
    st.info("Nenhum resultado inserido ainda.")

# Inserção de resultado
st.markdown("### Inserir novo resultado")
col1, col2, col3 = st.columns(3)
if col1.button("🔴 Casa"): st.session_state.history.append("Casa")
if col2.button("🔵 Visitante"): st.session_state.history.append("Visitante")
if col3.button("🟡 Empate"): st.session_state.history.append("Empate")

# Limitar tamanho do histórico
if len(st.session_state.history) > MAX_HISTORY:
    st.session_state.history = st.session_state.history[-MAX_HISTORY:]

# Análise
st.markdown("### Análise de padrões detectados")
padroes = analisar_todos_os_padroes(st.session_state.history)
if padroes:
    for padrao in padroes:
        st.success(padrao)
else:
    st.warning("Nenhum padrão forte identificado no momento.")

# Reset
if st.button("🔁 Zerar histórico"):
    st.session_state.history.clear()
    st.experimental_rerun()
