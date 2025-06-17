import streamlit as st import datetime

Configurações iniciais

st.set_page_config(page_title="Football Inteligente HS", layout="centered") st.title("⚽ Football Inteligente HS")

st.markdown("""

<style>
button {
    border-radius: 8px !important;
}
.stButton>button {
    height: 3em;
    width: 100%;
    font-size: 1.2em;
}
.result-box {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}
.result {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    font-weight: bold;
    color: white;
}
.result.C { background-color: red; }
.result.V { background-color: blue; }
.result.E { background-color: green; }
</style>""", unsafe_allow_html=True)

Entrada manual dos resultados

st.subheader("🔢 Inserir Resultados (C = Casa, V = Visitante, E = Empate)") entrada = st.text_input("Digite os resultados separados por vírgula (Ex: C,V,V,C,E...)")

Funções para detectar padrões

def detectar_padroes(resultados): alertas = [] n = len(resultados)

# 1. Surf de Cor
for i in range(n - 2):
    if resultados[i] == resultados[i+1] == resultados[i+2]:
        alertas.append(f"Surf de cor detectado: 3+ vezes '{resultados[i]}' a partir da posição {i+1}")
        break

# 2. Zig-Zag
if n >= 5:
    padrao = True
    for i in range(2, 6):
        if resultados[i % n] == resultados[(i-2) % n]:
            padrao = False
            break
    if padrao:
        alertas.append("Zig-Zag detectado nos últimos resultados")

# 3. Quebra de Surf
for i in range(3, n):
    if resultados[i] != resultados[i-1] and resultados[i-1] == resultados[i-2] == resultados[i-3]:
        alertas.append(f"Quebra de surf na posição {i+1}: '{resultados[i]}' quebrou sequência de '{resultados[i-1]}'")

# 4. Quebra de Zig-Zag
for i in range(4, n):
    if resultados[i-4] != resultados[i-3] and resultados[i-3] == resultados[i-1] and resultados[i] == resultados[i-2]:
        alertas.append("Quebra de Zig-Zag detectada")

# 5. Duplas Repetidas
for i in range(n - 3):
    if resultados[i] == resultados[i+1] and resultados[i+2] == resultados[i+3]:
        alertas.append("Duplas repetidas detectadas")
        break

# 6. Empate Recorrente
empates = [i for i, x in enumerate(resultados) if x == 'E']
if len(empates) >= 2:
    intervalos = [j - i for i, j in zip(empates[:-1], empates[1:])]
    if any(x <= 3 for x in intervalos):
        alertas.append("Empates recorrentes em intervalos curtos")

# 7. Padrão Escada
grupos = {}
for i in resultados:
    grupos[i] = grupos.get(i, 0) + 1
if sorted(grupos.values()) == list(range(1, len(grupos)+1)):
    alertas.append("Padrão Escada detectado")

# 8. Espelho
if n >= 4:
    for i in range(n - 3):
        if resultados[i] == resultados[i+3] and resultados[i+1] == resultados[i+2]:
            alertas.append("Padrão Espelho detectado")

# 9. Alternância com empate no meio
for i in range(n - 2):
    if resultados[i] == resultados[i+2] and resultados[i+1] == 'E':
        alertas.append("Alternância com empate no meio detectado")

# 10. Padrão Onda (1-2-1-2)
if n >= 4:
    if resultados[-4] != resultados[-3] and resultados[-2] != resultados[-1] and resultados[-4] == resultados[-2] and resultados[-3] == resultados[-1]:
        alertas.append("Padrão Onda (1-2-1-2) detectado")

# 11. Análise Tática (últimos 5/7/10)
for k in [5, 7, 10]:
    if n >= k:
        sub = resultados[-k:]
        count = {x: sub.count(x) for x in ['C','V','E']}
        maior = max(count, key=count.get)
        alertas.append(f"Nos últimos {k}, maior frequência foi: {maior} ({count[maior]})")

return alertas

Processamento dos dados

if entrada: resultados = [x.strip().upper() for x in entrada.split(',') if x.strip().upper() in ['C', 'V', 'E']] if len(resultados) < 5: st.warning("Digite ao menos 5 resultados para análise.") else: st.markdown("### 🧠 Histórico") for i in range(0, len(resultados), 9): linha = resultados[i:i+9] linha_html = '<div class="result-box">' + ''.join([f'<div class="result {r}">{r}</div>' for r in linha]) + '</div>' st.markdown(linha_html, unsafe_allow_html=True)

st.markdown("### 📊 Padrões Detectados")
    alertas = detectar_padroes(resultados)

    if alertas:
        for alerta in alertas:
            st.success(f"✅ {alerta}")
            if 'Surf' in alerta:
                st.markdown("**Sugestão:** Aproveite o surf! Entrada recomendada na mesma cor.")
            elif 'Quebra' in alerta:
                st.markdown("**Sugestão:** Aguardar estabilização antes de nova entrada.")
            elif 'Empate' in alerta:
                st.markdown("**Sugestão:** Fique atento ao empate nas próximas jogadas.")
            else:
                st.markdown("**Sugestão:** Analisar continuidade do padrão.")
    else:
        st.info("Nenhum padrão forte detectado.")

Rodapé

st.markdown("""

Desenvolvido por IA • ⚙️ Evolução Contínua """)

