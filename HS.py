@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background-color: #111;
    color: #f1f1f1;
}

h1.titulo {
    font-size: 2.5rem;
    text-align: center;
    color: #39FF14;
    margin-bottom: 2rem;
}

.stButton>button {
    font-weight: bold;
    border-radius: 6px;
    transition: 0.3s ease;
}

.stButton>button:hover {
    transform: scale(1.02);
    background-color: #222;
    border: 1px solid #39FF14;
}
from collections import Counter

def detectar_sequencia_surf(seq):
    resultados = []
    i = 0
    while i < len(seq) - 2:
        if seq[i] == seq[i+1] == seq[i+2]:
            j = i + 3
            while j < len(seq) and seq[j] == seq[i]:
                j += 1
            resultados.append(f"Sequência de '{seq[i]}' por {j-i} vezes na posição {i+1}.")
            i = j
        else:
            i += 1
    return resultados

def detectar_zig_zag(seq):
    resultados = []
    i = 0
    while i < len(seq) - 3:
        if seq[i] != seq[i+1] and seq[i] == seq[i+2] and seq[i+1] == seq[i+3]:
            resultados.append(f"Padrão Zig-Zag detectado iniciando na posição {i+1}: {seq[i:i+4]}")
        i += 1
    return resultados

def detectar_empate_recorrente(seq, empate_char='E'):
    resultados = []
    indices = [i for i, x in enumerate(seq) if x == empate_char]
    for i in range(len(indices) - 1):
        diff = indices[i+1] - indices[i]
        if diff in [2, 3]:
            resultados.append(f"Empates nas posições {indices[i]+1} e {indices[i+1]+1} (distância: {diff-1}).")
    return resultados

def detectar_espelho(seq):
    resultados = []
    for i in range(len(seq) - 3):
        if seq[i] == seq[i+3] and seq[i+1] == seq[i+2] and seq[i] != seq[i+1]:
            resultados.append(f"Padrão Espelho detectado: {''.join(seq[i:i+4])} na posição {i+1}.")
    return resultados

def detectar_padrao_escada(seq):
    resultados = []
    for i in range(len(seq) - 5):
        if (seq[i] != seq[i+1] and
            seq[i+1] == seq[i+2] and seq[i+1] != seq[i] and
            seq[i+3] == seq[i+4] == seq[i+5] and seq[i+3] == seq[i]):
            resultados.append(f"Escada detectada: 1-{seq[i]}, 2-{seq[i+1]}, 3-{seq[i]}. Início: posição {i+1}")
    return resultados
def gerar_sugestoes(sequencia, resultados):
    sugestoes = []
    empates = []

    ultima = sequencia[-1] if sequencia else None
    penultima = sequencia[-2] if len(sequencia) >= 2 else None

    if resultados.get("Surf"):
        if ultima and f"'{ultima}'" in "".join(resultados["Surf"][-1]):
            sugestoes.append(f"🌀 Continua tendência de '{ultima}'? Pode ser um Surf prolongado.")

    if resultados.get("Zig-Zag"):
        if ultima and penultima and ultima != penultima:
            sugestoes.append(f"↔️ Alternância detectada. Próximo pode ser '{penultima}'.")

    if resultados.get("Empate"):
        empates.append("⚖️ Empates frequentes em intervalo curto — fique atento!")
        sugestoes.append("Considerar possibilidade de novo empate na sequência.")

    if resultados.get("Espelho"):
        sugestoes.append("🔁 Padrão Espelho pode estar se formando. Próximo resultado pode repetir lógica.")

    if resultados.get("Escada"):
        sugestoes.append("📶 Escada em construção? Pode se repetir o degrau da sequência.")

    return sugestoes, empates
import streamlit as st
from padroes import *
from sugestoes import gerar_sugestoes

# Configuração da página
st.set_page_config(page_title="Analisador de Padrões", layout="wide")

# Carrega o CSS externo
with open("estilos.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Título
st.markdown("<h1 class='titulo'>🔍 Analisador de Padrões Futebolísticos</h1>", unsafe_allow_html=True)

# Estado global
if 'current_sequence' not in st.session_state:
    st.session_state.current_sequence = []
if 'history' not in st.session_state:
    st.session_state.history = []

# Tabs principais
tab1, tab2, tab3 = st.tabs(["📥 Entrada", "📈 Análise", "📚 Histórico"])

# TAB 1 – Entrada de dados
with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏠 Casa (C)", use_container_width=True):
            st.session_state.current_sequence.append('C')
            st.rerun()
    with col2:
        if st.button("🚗 Visitante (V)", use_container_width=True):
            st.session_state.current_sequence.append('V')
            st.rerun()
    with col3:
        if st.button("⚖️ Empate (E)", use_container_width=True):
            st.session_state.current_sequence.append('E')
            st.rerun()

    st.markdown("---")
    st.subheader("🧾 Sequência Atual")
    if st.session_state.current_sequence:
        st.code(" ".join(st.session_state.current_sequence))
        if st.button("↩️ Desfazer Último"):
            st.session_state.current_sequence.pop()
            st.rerun()
        if st.button("🧼 Limpar Sequência"):
            st.session_state.current_sequence = []
            st.rerun()
    else:
        st.info("Nenhum resultado adicionado ainda.")

# TAB 2 – Análise
with tab2:
    st.subheader("📊 Resultados da Análise")

    if st.session_state.current_sequence:
        seq = st.session_state.current_sequence

        resultados = {
            "Surf": detectar_sequencia_surf(seq),
            "Zig-Zag": detectar_zig_zag(seq),
            "Empate": detectar_empate_recorrente(seq),
            "Espelho": detectar_espelho(seq),
            "Escada": detectar_padrao_escada(seq)
        }

        sugestoes, empates = gerar_sugestoes(seq, resultados)

        with st.expander("🧠 Padrões Detectados", expanded=True):
            algum_padrao = False
            for nome, lista in resultados.items():
                if lista:
                    algum_padrao = True
                    st.success(f"🔹 {nome}")
                    for r in lista:
                        st.markdown(f"- {r}")
            if not algum_padrao:
                st.warning("Nenhum padrão detectado nesta sequência.")

        with st.expander("📌 Sugestões Estratégicas", expanded=True):
            if sugestoes:
                for s in sugestoes:
                    st.info(s)
            else:
                st.info("Nenhuma sugestão clara gerada.")

        with st.expander("⚠️ Empates Potenciais"):
            if empates:
                for e in empates:
                    st.warning(e)
            else:
                st.info("Sem indícios fortes de empate neste momento.")
    else:
        st.info("Adicione resultados para realizar a análise.")

# TAB 3 – Histórico
with tab3:
    st.subheader("🕓 Histórico de Análises")

    if st.session_state.current_sequence:
        atual = "".join(st.session_state.current_sequence)
        if not st.session_state.history or st.session_state.history[-1] != atual:
            st.session_state.history.append(atual)

    if st.session_state.history:
        for i, h in enumerate(reversed(st.session_state.history[-10:]), 1):
            st.code(f"{len(st.session_state.history) - i + 1}: {h}")
        if st.button("🗑️ Limpar Histórico"):
            st.session_state.history = []
            st.success("Histórico removido com sucesso!")
            st.rerun()
    else:
        st.info("Nenhum histórico disponível ainda.")
