import streamlit as st import datetime

Configurações iniciais

st.set_page_config(page_title="Football Inteligente HS", layout="centered") st.title("⚽ Football Inteligente HS")

Estilo customizado

st.markdown("""

<style>
.stButton>button {
    border-radius: 8px !important;
    height: 3em;
    font-size: 1.2em;
}
.result-box {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 1em;
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
    font-size: 0.9em;
}
.result.C { background-color: #d32f2f; }
.result.V { background-color: #1976d2; }
.result.E { background-color: #388e3c; }
</style>""", unsafe_allow_html=True)

Input manual dos resultados

st.subheader("🔢 Inserir Resultados (C = Casa, V = Visitante, E = Empate)") entrada = st.text_input("Digite os resultados separados por vírgula (Ex: C,V,V,C,E,...)")

Funções de detecção de padrões

def detectar_padroes(res): n = len(res) alertas = []

# 1. Surf de Cor
for i in range(n - 2):
    if res[i] == res[i+1] == res[i+2]:
        alertas.append(f"Surf de cor: 3x '{res[i]}' seguidas a partir da posição {i+1}")
        break

# 2. Zig-Zag (5 alternâncias)
if n >= 5:
    zig = all(res[i] != res[i-1] for i in range(1,5))
    if zig:
        alertas.append("Zig-Zag detectado nas últimas 5 posições")

# 3. Quebra de Surf
for i in range(3, n):
    if res[i] != res[i-1] and res[i-1] == res[i-2] == res[i-3]:
        alertas.append(f"Quebra de Surf: '{res[i]}' na posição {i+1} interrompeu sequência {res[i-1]}")

# 4. Quebra de Zig-Zag
if n >= 4:
    seq = res[-4:]
    if seq[0] != seq[1] and seq[1] != seq[2] and seq[2] != seq[3] and not all(seq[i] != seq[i-1] for i in range(1,4)):
        alertas.append("Quebra de Zig-Zag detectada")

# 5. Duplas Repetidas
for i in range(n - 3):
    if res[i] == res[i+1] and res[i+2] == res[i+3]:
        alertas.append("Duplas repetidas detectadas")
        break

# 6. Empate Recorrente
idxE = [i for i, x in enumerate(res) if x == 'E']
for a, b in zip(idxE, idxE[1:]):
    if b - a <= 3:
        alertas.append("Empates recorrentes em intervalo curto")
        break

# 7. Padrão Escada
cont = {x: res.count(x) for x in ['C','V','E']}
vals = sorted([v for v in cont.values() if v>0])
if vals == list(range(1, len(vals)+1)):
    alertas.append("Padrão Escada detectado")

# 8. Espelho
for i in range(n - 3):
    if res[i] == res[i+3] and res[i+1] == res[i+2]:
        alertas.append("Padrão Espelho detectado")
        break

# 9. Alternância com Empate no Meio
for i in range(n - 2):
    if res[i] == res[i+2] and res[i+1] == 'E':
        alertas.append("Alternância com Empate no Meio detectada")
        break

# 10. Onda (1-2-1-2)
if n >= 4:
    seq = res[-4:]
    if seq[0] == seq[2] and seq[1] == seq[3] and seq[0] != seq[1]:
        alertas.append("Padrão Onda (1-2-1-2) detectado")

# 11. Frequência tática (últimos 5,7,10)
for k in [5,7,10]:
    if n >= k:
        sub = res[-k:]
        cnt = {x: sub.count(x) for x in ['C','V','E']}
        maior = max(cnt, key=cnt.get)
        alertas.append(f"Últimos {k}: maior frequência = {maior} ({cnt[maior]})")

return alertas

Processamento da entrada

if entrada: resultados = [x.strip().upper() for x in entrada.split(',') if x.strip().upper() in ['C','V','E']] if len(resultados) < 5: st.warning("Insira ao menos 5 resultados para análise.") else: # Exibir histórico em linhas de 9 st.markdown("### 🧠 Histórico (blocos de 9)") for i in range(0, len(resultados), 9): bloco = resultados[i:i+9] row = '<div class="result-box">' + ''.join([f'<div class="result {r}">{r}</div>' for r in bloco]) + '</div>' st.markdown(row, unsafe_allow_html=True)

# Detectar padrões
    st.markdown("### 📊 Padrões Detectados e Sugestões")
    padroes = detectar_padroes(resultados)
    if padroes:
        for p in padroes:
            st.success(f"✅ {p}")
            # Sugestões básicas
            if 'Surf' in p:
                st.markdown("**Sugestão:** Aproveite a sequência, aposte na mesma cor.")
            elif 'Quebra' in p:
                st.markdown("**Sugestão:** Aguarde estabilização antes de nova entrada.")
            elif 'Empates recorrentes' in p or 'Empate' in p:
                st.markdown("**Sugestão:** Fique atento ao próximo empate.")
            else:
                st.markdown("**Sugestão:** Monitore continuidade do padrão.")
    else:
        st.info("Nenhum padrão forte detectado.")

Rodapé

st.markdown("---") st.write("Desenvolvido por IA • Aprendizado Contínuo 🚀")

