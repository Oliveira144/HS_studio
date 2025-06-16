# Football Studio HS - Analisador com TODOS os padrões avançados do jogo

import streamlit as st
from collections import deque

# Configuração inicial
st.set_page_config(page_title="Football Studio HS", layout="centered")
MAX_HISTORY = 50
history = deque([], maxlen=MAX_HISTORY)

# Mapas de cor e ícones
color_map = {"Casa": "red", "Visitante": "blue", "Empate": "orange"}
emoji_map = {"Casa": "🔴", "Visitante": "🔵", "Empate": "🟡"}

# Funções de detecção de padrões
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

def detectar_zigzag(hist):
    if len(hist) < 6: return None
    padrao = list(hist)[-6:]
    if all(padrao[i] != padrao[i+1] for i in range(5)):
        return "Zig-zag detectado. Sugestão: seguir alternância."
    return None

def detectar_surf(hist):
    if len(hist) < 6: return None
    cor = hist[-1]
    seguidos = 1
    quebras = 0
    for i in range(len(hist) - 2, -1, -1):
        if hist[i] == cor:
            seguidos += 1
        elif i >= 1 and hist[i-1] == cor:
            seguidos += 1
            quebras += 1
            i -= 1
        else:
            break
    if seguidos >= 4 and quebras <= 2:
        return f"Surf detectado: {seguidos}x {cor} com {quebras} quebra(s). Sugestão: apostar {cor} nas próximas 3."
    return None

def detectar_dupla_alternada(hist):
    if len(hist) < 8: return None
    padrao = list(hist)[-8:]
    pares = [padrao[i:i+2] for i in range(0, 8, 2)]
    if all(par[0] == par[1] for par in pares) and all(pares[i][0] != pares[i+1][0] for i in range(3)):
        return "Padrão de dupla alternada (ex: HH-AA-HH). Sugestão: siga alternância dupla."
    return None

def detectar_empate_ciclico(hist):
    if len(hist) < 10: return None
    indices = [i for i, x in enumerate(hist) if x == "Empate"]
    if len(indices) >= 3:
        diffs = [indices[i+1] - indices[i] for i in range(len(indices)-1)]
        if all(d == diffs[0] for d in diffs):
            return f"Empate cíclico a cada {diffs[0]} jogadas. Sugestão: esperar empate na próxima {diffs[0]} rodada."
    return None

def detectar_quebra_sequencia_com_recuperacao(hist):
    if len(hist) < 7: return None
    ultima = hist[-1]
    anterior = hist[-2]
    if ultima == hist[-3] == hist[-4] and anterior != ultima:
        return f"Sequência com quebra recuperada: {ultima}. Sugestão: seguir o fluxo {ultima}."
    return None

def detectar_cascata_empate(hist):
    if len(hist) < 6: return None
    padrao = list(hist)[-6:]
    if padrao.count("Empate") >= 3:
        return "Cascata de empates detectada. Sugestão: evitar apostas até estabilizar."
    return None

def detectar_sequencia_com_empate_no_meio(hist):
    if len(hist) < 5: return None
    if hist[-1] == hist[-3] and hist[-2] == "Empate":
        return f"Sequência com empate no meio detectada. Sugestão: seguir cor {hist[-1]}."
    return None

def analisar_todos_os_padroes(hist):
    funcoes = [
        detectar_surf,
        detectar_sequencia,
        detectar_zigzag,
        detectar_dupla_alternada,
        detectar_empate_ciclico,
        detectar_quebra_sequencia_com_recuperacao,
        detectar_cascata_empate,
        detectar_sequencia_com_empate_no_meio,
    ]
    analises = []
    for func in funcoes:
        r = func(hist)
        if r:
            analises.append(r)
    return analises

# Interface do app
st.title("🎲 Football Studio HS - Padrões Avançados")

st.markdown("### Histórico de resultados")
cols = st.columns(len(history) if history else 1)
for i, cor in enumerate(history):
    with cols[i]:
        st.markdown(
            f"<div style='text-align:center; font-size:22px; color:{color_map[cor]}'>{emoji_map[cor]}</div>",
            unsafe_allow_html=True
        )

st.markdown("---")

st.markdown("### Inserir novo resultado")
col1, col2, col3 = st.columns(3)
if col1.button("🔴 Casa"): history.append("Casa")
if col2.button("🔵 Visitante"): history.append("Visitante")
if col3.button("🟡 Empate"): history.append("Empate")

st.markdown("---")

st.markdown("### Análise de padrões detectados")
padroes = analisar_todos_os_padroes(history)
if padroes:
    for padrao in padroes:
        st.info(f"{padrao}")
else:
    st.warning("Nenhum padrão forte identificado no momento.")

st.markdown("---")
if st.button("🔁 Zerar histórico"):
    history.clear()
    st.experimental_rerun()
