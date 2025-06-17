import streamlit as st
from collections import Counter
import re

st.set_page_config(page_title="Football Studio HS", layout="wide")

# ---------------------- Funções de Detecção ----------------------

def detectar_surf(seq):
    return len(seq) >= 3 and seq[-1] == seq[-2] == seq[-3]

def detectar_zigzag(seq):
    return len(seq) >= 4 and all(seq[i] != seq[i+1] for i in range(-4, -1))

def detectar_quebra_surf(seq):
    return len(seq) >= 4 and seq[-4] == seq[-3] == seq[-2] and seq[-1] != seq[-2]

def detectar_quebra_zigzag(seq):
    return len(seq) >= 5 and seq[-5] != seq[-4] and seq[-4] != seq[-3] and seq[-3] != seq[-2] and seq[-1] == seq[-2]

def detectar_duplas_repetidas(seq):
    return len(seq) >= 4 and seq[-4] == seq[-3] and seq[-2] == seq[-1] and seq[-3] != seq[-2]

def detectar_empate_recorrente(seq):
    empates = [i for i in seq if i == 'E']
    return len(empates) >= 3 and ''.join(seq[-10:]).count('E') >= 3

def detectar_escada(seq):
    if len(seq) < 6:
        return False
    s = ''.join(seq[-9:])
    grupos = [len(g) for g in re.findall(r'(C+|V+|E+)', s)]
    return grupos == sorted(grupos)

def detectar_espelho(seq):
    return len(seq) >= 4 and seq[-4] == seq[-1] and seq[-3] == seq[-2]

def detectar_alternancia_com_empate(seq):
    return len(seq) >= 3 and seq[-3] != seq[-1] and seq[-2] == 'E'

def detectar_onda(seq):
    if len(seq) < 6:
        return False
    s = ''.join(seq[-6:])
    grupos = [len(g) for g in re.findall(r'(C+|V+|E+)', s)]
    return grupos in ([1,2,1,2], [2,1,2,1])

def detectar_base_recente(seq):
    return f"Últimos 5: {seq[-5:]}, 7: {seq[-7:]}, 10: {seq[-10:]}"

def detectar_3x1(seq):
    return len(seq) >= 4 and seq[-4] == seq[-3] == seq[-2] and seq[-1] != seq[-2]

def detectar_3x3(seq):
    return len(seq) >= 6 and seq[-6] == seq[-5] == seq[-4] and seq[-3] == seq[-2] == seq[-1] and seq[-6] != seq[-3]
    # ---------------------- Interface ----------------------

st.title("🎲 Football Studio HS - Detector de Padrões Avançados")

cores_input = st.text_input("Digite os últimos resultados (C = Casa, V = Visitante, E = Empate):", "CCCVVVECCVVCCCEVVVCCVVVCEV")
cores = list(cores_input.upper().strip())[-50:]

st.subheader("📊 Histórico de Resultados")
for i in range(0, len(cores), 9):
    linha = cores[i:i+9]
    st.markdown(" ".join([
        f"<span style='color:{'red' if c=='C' else 'blue' if c=='V' else 'orange'}; font-size:22px'>⬤</span>"
        for c in linha
    ]), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔴 Casa"):
        cores.append("C")
with col2:
    if st.button("🔵 Visitante"):
        cores.append("V")
with col3:
    if st.button("🟡 Empate"):
        cores.append("E")
        # ---------------------- Análise ----------------------

st.subheader("🔍 Padrões Detectados")

alertas = []

if detectar_surf(cores): alertas.append("🔴 SURF DE COR DETECTADO – entre nas próximas 3 rodadas")
if detectar_zigzag(cores): alertas.append("🔄 ZIG-ZAG DETECTADO")
if detectar_quebra_surf(cores): alertas.append("⚠️ QUEBRA DE SURF DETECTADA")
if detectar_quebra_zigzag(cores): alertas.append("⚠️ QUEBRA DE ZIG-ZAG DETECTADA")
if detectar_duplas_repetidas(cores): alertas.append("📈 DUPLAS REPETIDAS DETECTADAS")
if detectar_empate_recorrente(cores): alertas.append("🟡 EMPATE RECORRENTE DETECTADO")
if detectar_escada(cores): alertas.append("📊 PADRÃO ESCADA DETECTADO")
if detectar_espelho(cores): alertas.append("🔁 PADRÃO ESPELHO DETECTADO")
if detectar_alternancia_com_empate(cores): alertas.append("⚡ ALTERNÂNCIA COM EMPATE NO MEIO")
if detectar_onda(cores): alertas.append("🌊 PADRÃO ONDA DETECTADO")
if detectar_3x1(cores): alertas.append("🔥 PADRÃO 3x1 DETECTADO")
if detectar_3x3(cores): alertas.append("🔥 PADRÃO 3x3 DETECTADO")

st.info(detectar_base_recente(cores))

if alertas:
    for msg in alertas:
        st.success(msg)
else:
    st.warning("Nenhum padrão relevante detectado no momento.")
