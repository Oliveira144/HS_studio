import streamlit as st
from collections import deque, Counter
from itertools import groupby
import math

# --- CONFIGURAÇÕES INICIAIS ---
st.set_page_config(page_title="Football Studio HS", layout="centered")
st.title("⚽ Football Studio HS – Analisador Avançado de Padrões")

st.markdown("""
<style>
    .element-container button {
        height: 60px !important;
        font-size: 22px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- HISTÓRICO ---
historico = st.session_state.get("historico", deque(maxlen=300))

# --- INPUT OTIMIZADO ---
st.subheader("🎮 Inserir resultado ao vivo:")
col1, col2, col3 = st.columns(3)
if col1.button("🏠 Casa", use_container_width=True):
    historico.append("C")
elif col2.button("🤝 Empate", use_container_width=True):
    historico.append("E")
elif col3.button("🚩 Visitante", use_container_width=True):
    historico.append("V")

# --- HISTÓRICO VISUAL ---
st.subheader("📊 Histórico Visual (linhas de 9)")
linhas = [list(historico)[i:i+9] for i in range(0, len(historico), 9)]
for linha in linhas:
    st.markdown(" ".join(f"[{x}]" for x in linha))

# --- FUNÇÕES ---
def traduz(simbolo):
    return {"C": "Casa", "V": "Visitante", "E": "Empate"}.get(simbolo, simbolo)

def detectar_padroes_complexos(hist):
    if isinstance(hist, str):
        hist = list(hist)
    padroes = []
    if len(hist) < 4:
        return padroes
    texto = "".join(hist)
    checks = {
        "2x2": "CCVV" in texto or "VVCC" in texto,
        "3x3": "CCCVVV" in texto or "VVVCCC" in texto,
        "3x1x3": any(texto[i:i+7] == a*3 + b + a*3 for i in range(len(texto)-6) for a in "CV" for b in "VE" if b != a),
        "2x1x2": any(texto[i:i+5] == a*2 + b + a*2 for i in range(len(texto)-4) for a in "CV" for b in "VE" if b != a),
        "4x4": "CCCCVVVV" in texto or "VVVVCCCC" in texto,
        "3x1x1x2": any(texto[i:i+7] == a*3 + b + b + a*2 for i in range(len(texto)-6) for a in "CV" for b in "VE" if b != a),
    }
    for nome, cond in checks.items():
        if cond:
            padroes.append(nome)
    return padroes

def detectar_padroes_repetidos(hist, janela=5):
    if isinstance(hist, str):
        hist = list(hist)
    if len(hist) < janela * 2:
        return None, 0
    sequencias = [tuple(hist[i:i+janela]) for i in range(len(hist) - janela + 1)]
    contagem = Counter(sequencias)
    padroes_repetidos = [seq for seq, count in contagem.items() if count > 1]
    sugestoes = []
    for padrao in padroes_repetidos:
        for i in range(len(hist) - janela):
            if tuple(hist[i:i+janela]) == padrao and i+janela < len(hist):
                sugestoes.append(hist[i+janela])
    if sugestoes:
        mais_comum, freq = Counter(sugestoes).most_common(1)[0]
        return f"🔁 Padrão: {''.join(padroes_repetidos[0])} → Entrar: {traduz(mais_comum)} (Confiança: {freq})", freq
    return None, 0

def chance_empate(hist):
    total = len(hist)
    empates = hist.count("E")
    return f"{round((empates / total) * 100, 1)}%" if total > 0 else "0%"

def detectar_tendencia_surf(hist):
    if len(hist) < 5:
        return "-"
    atual = hist[-1]
    count = 1
    for i in range(len(hist) - 2, -1, -1):
        if hist[i] == atual:
            count += 1
        else:
            break
    if count >= 4:
        quebra = round((1 - (count / 10)) * 100)
        return f"⚠️ {traduz(atual)} em sequência ({count}x) ➤ Alta chance de quebra ({quebra}%)"
    return "-"

def recomendacao(hist):
    if len(hist) < 3:
        return "Poucos dados para análise."
    ultimos = list(hist)[-3:]
    if ultimos.count("C") == 3:
        return "📉 Casa em sequência. Sugestão: Visitante ou Empate."
    if ultimos.count("V") == 3:
        return "📉 Visitante em sequência. Sugestão: Casa ou Empate."
    if ultimos[-1] != ultimos[-2]:
        return "↔️ Zig-zag ativo. Seguir alternância."
    return "🔍 Aguardar padrão mais claro."

# --- ANÁLISE INTELIGENTE ---
st.subheader("📈 Análise Inteligente")

padroes = detectar_padroes_complexos(historico)
if padroes:
    st.success("🔎 Padrões encontrados: " + ", ".join(padroes))
else:
    st.info("Nenhum padrão complexo identificado até agora.")

sugestao, confianca = detectar_padroes_repetidos(historico)
if sugestao:
    if confianca >= 3:
        st.warning(sugestao)
    else:
        st.info(sugestao)

surf = detectar_tendencia_surf(historico)
if surf != "-":
    st.warning(surf)

st.markdown(f"🔄 **Chance de empate**: {chance_empate(historico)}")
st.markdown(f"🧠 **Recomendação baseada no histórico**: {recomendacao(historico)}")

# --- SALVAR HISTÓRICO ---
st.session_state["historico"] = historico
