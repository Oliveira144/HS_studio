import streamlit as st

st.set_page_config(page_title="Football Studio HS", layout="wide")

st.title("🎲 Football Studio HS — Analisador de Padrões")
st.markdown("Analisa os últimos 50 resultados do jogo Football Studio e detecta padrões avançados com sugestões inteligentes.")

# ---------------------- HISTÓRICO GLOBAL ----------------------
if 'cores' not in st.session_state:
    st.session_state.cores = []

cores = st.session_state.cores

# ---------------------- BOTÕES DE ENTRADA ----------------------
st.subheader("🎯 Inserir Resultado")

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

# ---------------------- HISTÓRICO EM LINHAS DE 9 (HORIZONTAL) ----------------------
st.subheader("🧾 Histórico (últimos resultados em blocos de 9)")

def exibir_historico(cores):
    if not cores:
        st.info("Nenhum resultado inserido ainda.")
        return

    blocos = [cores[i:i + 9] for i in range(0, len(cores), 9)]

    for bloco in blocos:
        colunas = st.columns(len(bloco))
        for i, cor in enumerate(bloco):
            with colunas[i]:
                if cor == "C":
                    st.markdown("<div style='font-size:30px;'>🔴</div>", unsafe_allow_html=True)
                elif cor == "V":
                    st.markdown("<div style='font-size:30px;'>🔵</div>", unsafe_allow_html=True)
                elif cor == "E":
                    st.markdown("<div style='font-size:30px;'>🟡</div>", unsafe_allow_html=True)

exibir_historico(cores)

# ---------------------- FUNÇÕES DE PADRÕES ----------------------
def detectar_surf(cores):
    return len(cores) >= 3 and cores[-1] == cores[-2] == cores[-3]

def detectar_quebra_surf(cores):
    return len(cores) >= 4 and cores[-4] == cores[-3] == cores[-2] and cores[-1] != cores[-2]

def detectar_zigzag(cores):
    if len(cores) < 4:
        return False
    return all(cores[i] != cores[i+1] for i in range(-4, -1))

def detectar_quebra_zigzag(cores):
    if len(cores) < 5:
        return False
    zz = all(cores[i] != cores[i+1] for i in range(-5, -2))
    return zz and cores[-2] == cores[-1]

def detectar_empates_frequentes(cores):
    return cores.count("E") >= 4 and cores[-1] == "E"

def detectar_duplas_repetidas(cores):
    return len(cores) >= 4 and cores[-4] == cores[-3] and cores[-2] == cores[-1] and cores[-4] != cores[-2]

def detectar_3x1(cores):
    return len(cores) >= 4 and cores[-4] == cores[-3] == cores[-2] and cores[-1] != cores[-2]

def detectar_3x3(cores):
    return len(cores) >= 6 and cores[-6] == cores[-5] == cores[-4] and cores[-3] == cores[-2] == cores[-1]

def detectar_escada(cores):
    if len(cores) < 6:
        return False
    for i in range(len(cores) - 5):
        if cores[i] == cores[i+1] == cores[i+2] and cores[i+3] == cores[i+4] == cores[i+5]:
            return True
    return False

def detectar_espelho(cores):
    return len(cores) >= 4 and cores[-4] == cores[-1] and cores[-3] == cores[-2]

# ---------------------- ANÁLISE E SUGESTÕES ----------------------
st.subheader("📈 Sugestões Inteligentes")

sugestoes = []

if detectar_surf(cores): sugestoes.append(("🔥 Surf de cor detectado — aposte nas próximas 3 rodadas", 90))
if detectar_quebra_surf(cores): sugestoes.append(("⚠️ Quebra de Surf — Evite entrada imediata", 60))
if detectar_zigzag(cores): sugestoes.append(("↔️ Zig-Zag detectado — boa chance de alternância", 80))
if detectar_quebra_zigzag(cores): sugestoes.append(("❌ Quebra de Zig-Zag — padrão instável", 65))
if detectar_empates_frequentes(cores): sugestoes.append(("⚠️ Empates frequentes — fique atento", 70))
if detectar_duplas_repetidas(cores): sugestoes.append(("♻️ Duplas repetidas — possível sequência", 75))
if detectar_3x1(cores): sugestoes.append(("⚡ Padrão 3x1 detectado", 80))
if detectar_3x3(cores): sugestoes.append(("⚡ Padrão 3x3 detectado", 85))
if detectar_escada(cores): sugestoes.append(("⛓️ Padrão Escada detectado", 70))
if detectar_espelho(cores): sugestoes.append(("🔄 Padrão Espelho detectado", 75))

if sugestoes:
    for texto, confianca in sugestoes:
        st.success(f"{texto} — Confiança: {confianca}%")
else:
    st.info("Nenhum padrão claro detectado.")

# ---------------------- BOTÃO DE RESET ----------------------
st.markdown("---")
if st.button("🧹 Reiniciar Histórico"):
    cores.clear()
    st.experimental_rerun()

# ---------------------- ESTILO VISUAL ----------------------
st.markdown("""
<style>
    .stButton button {
        border-radius: 12px;
        font-size: 16px;
        height: 3em;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)
