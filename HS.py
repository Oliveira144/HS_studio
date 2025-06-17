# football_studio_app.py - PARTE 1

import streamlit as st

# ---------------------- Configuração Inicial ----------------------
st.set_page_config(page_title="Football Studio HS", layout="centered")

st.title("🎮 Football Studio HS")
st.caption("Análise automatizada de padrões com sugestões inteligentes de entrada")

# ---------------------- Sessão de Histórico ----------------------
if "cores" not in st.session_state:
    st.session_state.cores = []

cores = st.session_state.cores

# ---------------------- Botões de Entrada ----------------------
st.subheader("🎯 Inserir Resultado Manual")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏠 Casa", use_container_width=True):
        cores.append("C")
with col2:
    if st.button("🛫 Visitante", use_container_width=True):
        cores.append("V")
with col3:
    if st.button("⚖️ Empate", use_container_width=True):
        cores.append("E")
with col4:
    if st.button("🔁 Reiniciar", use_container_width=True):
        cores.clear()
        # ---------------------- PARTE 2 (LINHAS de 9 bolinhas) ----------------------

st.subheader("📊 Histórico visual (linhas de 9 bolinhas por linha)")

if cores:
    linhas = [cores[i:i+9] for i in range(0, len(cores), 9)]

    for linha in linhas:
        linha_html = ""
        for cor in linha:
            if cor == "C":
                linha_html += f"<span style='color:red; font-size:22px'>⬤</span> "
            elif cor == "V":
                linha_html += f"<span style='color:blue; font-size:22px'>⬤</span> "
            elif cor == "E":
                linha_html += f"<span style='color:orange; font-size:22px'>⬤</span> "
        st.markdown(linha_html, unsafe_allow_html=True)
else:
    st.info("Nenhum resultado ainda. Clique nos botões acima.")
    # ---------------------- PARTE 3 - Funções de Detecção de Padrões ----------------------

def detectar_surf(cores):
    if len(cores) < 3:
        return False
    ult = cores[-1]
    count = 1
    for i in range(len(cores) - 2, -1, -1):
        if cores[i] == ult:
            count += 1
        else:
            break
    return count >= 3  # 3 ou mais da mesma cor seguidos


def detectar_zigzag(cores):
    if len(cores) < 4:
        return False
    ultimos = cores[-4:]
    for i in range(1, len(ultimos)):
        if ultimos[i] == ultimos[i-1] or ultimos[i] == "E":
            return False
    return True


def detectar_quebra_surf(cores):
    if len(cores) < 4:
        return False
    ultimos = cores[-4:]
    return ultimos[0] == ultimos[1] == ultimos[2] and ultimos[3] != ultimos[2]


def detectar_empate_recorrente(cores):
    if len(cores) < 5:
        return False
    empates = cores[-5:].count("E")
    return empates >= 2
    # ---------------------- PARTE 3 - Sugestões Inteligentes ----------------------

st.subheader("🤖 Sugestões de Entrada e Confiança")

sugestoes = []

if detectar_surf(cores): sugestoes.append(("🔥 SURF DE COR DETECTADO", 90))
if detectar_zigzag(cores): sugestoes.append(("🔄 ZIG-ZAG DETECTADO", 75))
if detectar_quebra_surf(cores): sugestoes.append(("⚠️ QUEBRA DE SURF", 60))
if detectar_empate_recorrente(cores): sugestoes.append(("🟡 EMPATE RECORRENTE", 70))

# Exibe os padrões detectados com a porcentagem de confiança
if sugestoes:
    for texto, confianca in sugestoes:
        st.success(f"{texto} — Confiança estimada: {confianca}%")
else:
    st.info("Nenhum padrão forte detectado ainda.")
    # ---------------------- PARTE 4 - Funções de Detecção Avançadas ----------------------

def detectar_3x1(cores):
    if len(cores) < 4:
        return False
    return cores[-4] == cores[-3] == cores[-2] and cores[-1] != cores[-2]

def detectar_3x3(cores):
    if len(cores) < 6:
        return False
    return cores[-6] == cores[-5] == cores[-4] and cores[-3] == cores[-2] == cores[-1]

def detectar_escada(cores):
    if len(cores) < 6:
        return False
    for i in range(len(cores) - 5):
        if cores[i] == cores[i+1] == cores[i+2] and cores[i+3] == cores[i+4] == cores[i+5]:
            return True
    return False

def detectar_espelho(cores):
    if len(cores) < 4:
        return False
    return cores[-4] == cores[-1] and cores[-3] == cores[-2]
    # ---------------------- PARTE 4 - Sugestões Avançadas ----------------------

st.subheader("🔮 Padrões Avançados Detectados")

sugestoes_avancadas = []

if detectar_3x1(cores): sugestoes_avancadas.append(("⚡ Padrão 3x1 detectado", 80))
if detectar_3x3(cores): sugestoes_avancadas.append(("⚡ Padrão 3x3 detectado", 85))
if detectar_escada(cores): sugestoes_avancadas.append(("⛓️ Padrão Escada detectado", 70))
if detectar_espelho(cores): sugestoes_avancadas.append(("🔄 Padrão Espelho detectado", 75))

if sugestoes_avancadas:
    for texto, confianca in sugestoes_avancadas:
        st.success(f"{texto} — Confiança estimada: {confianca}%")
else:
    st.info("Nenhum padrão avançado detectado.")
    # ---------------------- PARTE 5 - Botão de Reset ----------------------

st.markdown("---")
if st.button("🧹 Reiniciar Histórico"):
    cores.clear()
    st.experimental_rerun()
    # ---------------------- PARTE 5 - Ajustes Visuais Finais ----------------------

st.markdown("""
<style>
    .css-1d391kg, .css-ffhzg2 { padding-top: 10px !important; }
    .stButton button {
        border-radius: 10px;
        padding: 8px 16px;
        font-size: 16px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)
    
