import streamlit as st
from collections import deque

st.set_page_config(page_title="Football Studio HS", layout="centered")

# ----------------------
# VARIÁVEIS GLOBAIS
# ----------------------
MAX_HISTORY = 50
history = deque([], maxlen=MAX_HISTORY)

# ----------------------
# FUNÇÕES DE PADRÕES
# ----------------------
def detectar_sequencia(hist):
    if len(hist) < 3:
        return None
    ultima = hist[-1]
    count = 1
    for i in range(len(hist) - 2, -1, -1):
        if hist[i] == ultima:
            count += 1
        else:
            break
    if count >= 3:
        return f"Sequência de {count}x {ultima}"
    return None

def detectar_zigzag(hist):
    if len(hist) < 5:
        return None
    padrao = list(hist)[-5:]
    if all(padrao[i] != padrao[i+1] for i in range(4)):
        return "Padrão de Zig-Zag detectado"
    return None

def detectar_surf(hist):
    if len(hist) < 6:
        return None
    surf_color = hist[-1]
    sequencia = 1
    for i in range(len(hist)-2, -1, -1):
        if hist[i] == surf_color:
            sequencia += 1
        elif i > 0 and hist[i-1] == surf_color:
            sequencia += 1
            i -= 1
        else:
            break
    if sequencia >= 4:
        return f"Surf detectado em '{surf_color}' com {sequencia} acertos"
    return None

def sugestao_de_entrada(hist):
    surf = detectar_surf(hist)
    if surf:
        cor = hist[-1]
        return {
            "sugestao": f"Surf em andamento: aposte em {cor} nas próximas 3 rodadas!",
            "cor": cor,
            "entradas": [cor, cor, cor]
        }
    seq = detectar_sequencia(hist)
    if seq:
        return {
            "sugestao": f"{seq}. Possível quebra de sequência. Considere aposta oposta.",
            "cor": "Contrária"
        }
    zig = detectar_zigzag(hist)
    if zig:
        return {
            "sugestao": "Zig-Zag detectado. Siga alternância ou espere quebra.",
            "cor": "Alternada"
        }
    return {"sugestao": "Nenhum padrão forte no momento."}

# ----------------------
# INTERFACE STREAMLIT
# ----------------------
st.title("🎲 Football Studio HS - Analisador de Padrões")

st.markdown("Últimos resultados:")
cols = st.columns(len(history) if history else 1)
for i, cor in enumerate(history):
    with cols[i]:
        color_map = {
            "Casa": "red",
            "Visitante": "blue",
            "Empate": "orange"
        }
        if st.button("⬤", key=f"{i}", help=f"{cor}", args=(i,), 
                     use_container_width=True):
            nova_cor = st.selectbox(f"Corrigir resultado {i+1}:", ["Casa", "Visitante", "Empate"], index=["Casa", "Visitante", "Empate"].index(cor), key=f"edit_{i}")
            history[i] = nova_cor
        st.markdown(f"<div style='text-align:center; color:{color_map[cor]}; font-weight:bold'>{cor}</div>", unsafe_allow_html=True)

st.divider()

# Entrada manual
st.subheader("Inserir novo resultado")
col1, col2, col3 = st.columns(3)
if col1.button("🔴 Casa"):
    history.append("Casa")
if col2.button("🔵 Visitante"):
    history.append("Visitante")
if col3.button("🟡 Empate"):
    history.append("Empate")

st.divider()

# Sugestões e Padrões
st.subheader("🧠 Análise de Padrões")
analises = [
    detectar_sequencia(history),
    detectar_zigzag(history),
    detectar_surf(history)
]
for analise in analises:
    if analise:
        st.info(f"🔍 {analise}")

sugestao = sugestao_de_entrada(history)
st.success(f"💡 Sugestão: {sugestao['sugestao']}")

# Botão de reset
st.divider()
if st.button("🔁 Zerar histórico e recomeçar"):
    history.clear()
    st.experimental_rerun()
