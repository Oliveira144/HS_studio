import streamlit as st
import numpy as np # Ainda útil para algumas operações, mas não para o modelo de ML
from collections import Counter
import pandas as pd # Ainda útil para manipulação de dados e visualização

# --- Funções de Ajuda ---
def resultado_para_numerico(resultado):
    """Converte 'C', 'V', 'E' para valores numéricos.
       Mantido para compatibilidade, mas pode ser removido se não for mais necessário."""
    if resultado == 'C': return 1 # Casa
    if resultado == 'V': return 2 # Visitante
    if resultado == 'E': return 0 # Empate
    return -1 # Caso de erro

def numerico_para_resultado(numero):
    """Converte números para 'C', 'V', 'E'."""
    if numero == 1: return 'C'
    if numero == 2: return 'V'
    if numero == 0: return 'E'
    return '?'

# --- Funções de Análise ---

def detectar_padroes_inteligente(hist, janela_min=2, janela_max=4):
    """
    Detecta padrões de sequências de resultados em diferentes tamanhos de janela
    e oferece uma recomendação mais ponderada.
    """
    if len(hist) < janela_max:
        return [], None, None

    todos_padroes = {} # Dicionário para armazenar padrões por tamanho de janela
    # Ajuste para a última sequência para cobrir todas as janelas analisadas
    ultima_sequencia_maior = tuple(hist[-(janela_max-1):]) if janela_max > 1 else ()

    for janela in range(janela_min, janela_max + 1):
        if len(hist) < janela:
            continue
        sequencias = [tuple(hist[i:i+janela]) for i in range(len(hist) - janela + 1)]
        contagem = Counter(sequencias)
        # Filtra padrões que ocorrem mais de uma vez ou que são muito frequentes
        # Padrões que ocorrem mais de 2 vezes OU são mais de 25% das ocorrências
        padroes_encontrados = {seq: freq for seq, freq in contagem.items() if freq > 1 or (len(sequencias) > 0 and freq >= len(sequencias) * 0.25)}
        if padroes_encontrados:
            todos_padroes[janela] = padroes_encontrados

    recomendacao_candidatos = Counter()
    for janela, padroes_na_janela in todos_padroes.items():
        # A parte da sequência final precisa ser ajustada para cada janela
        ult = tuple(hist[-(janela-1):]) if janela > 1 else ()

        for seq, freq in padroes_na_janela.items():
            if seq[:-1] == ult:
                # Pesa a recomendação pela frequência e pelo tamanho da janela (maior janela, maior peso)
                recomendacao_candidatos[seq[-1]] += freq * janela

    sugestao = None
    confianca = 0.0

    if recomendacao_candidatos:
        sugestao, total_votos = recomendacao_candidatos.most_common(1)[0]
        # Calcular confiança baseada na proporção de votos do mais comum
        confianca = total_votos / sum(recomendacao_candidatos.values())

    # Formatar os padrões para exibição
    padroes_exibicao = []
    for janela in sorted(todos_padroes.keys()): # Ordenar para exibição consistente
        for p in todos_padroes[janela]:
            padroes_exibicao.append(f"{''.join(p)} (tam {janela})")

    return padroes_exibicao, sugestao, confianca

def prever_empate_estatistico(dados, janela_analise=10, tendencia_peso=0.5):
    """
    Prevê a chance de empate com base em estatísticas simples:
    - Frequência geral de empates nos últimos N jogos.
    - Análise de tendências (e.g., se houver muitos "CECE" ou "VEVE").
    """
    if len(dados) < 10: # Mínimo de dados para análise estatística
        return 0.0, "Histórico muito curto para análise estatística de empates."

    # Frequência de empates nos últimos 'janela_analise' jogos
    ultimos_dados = dados[-janela_analise:]
    contagem_ultimos = Counter(ultimos_dados)
    frequencia_empate = (contagem_ultimos['E'] / len(ultimos_dados)) * 100 if ultimos_dados else 0.0

    # Análise de tendência (ex: "CE", "VE", "EC", "EV" nos últimos N jogos)
    # Procurar por padrões que possam indicar alternância para empate
    tendencia_score = 0
    # Pontos para sequências que terminam em E ou que são de alternância
    if len(dados) >= 2:
        if dados[-1] == 'E': # Se o último já foi empate, talvez menos provável (ou mais, dependendo do jogo)
            tendencia_score -= 10
        if dados[-1] == 'C' and dados[-2] == 'E': # Ex: EC
            tendencia_score += 5
        if dados[-1] == 'V' and dados[-2] == 'E': # Ex: EV
            tendencia_score += 5
        if dados[-1] == 'E' and dados[-2] == 'C': # Ex: CE
            tendencia_score += 10 # Forte indício de alternância
        if dados[-1] == 'E' and dados[-2] == 'V': # Ex: VE
            tendencia_score += 10 # Forte indício de alternância
    
    if len(dados) >= 3:
        if dados[-1] == 'C' and dados[-2] == 'E' and dados[-3] == 'C': # CEC
            tendencia_score += 15 # Padrão que "chama" um empate
        if dados[-1] == 'V' and dados[-2] == 'E' and dados[-3] == 'V': # VEV
            tendencia_score += 15 # Padrão que "chama" um empate

    # Ajustar a frequência de empate com base na tendência
    # Limitar o score da tendência para não distorcer muito
    tendencia_score_ajustado = max(-20, min(tendencia_score, 20)) # Limita a -20 a +20

    chance_final = frequencia_empate + tendencia_score_ajustado
    chance_final = max(0, min(chance_final, 100)) # Garante que fique entre 0 e 100

    return round(chance_final, 2), "Análise estatística e de tendência concluída."


# --- Interface com o usuário ---
st.set_page_config(page_title="Football Studio HS (Estatístico)", layout="centered", page_icon="⚽")
st.title("⚽ Inserir Resultado ao Vivo (Football Studio HS)")

# Inicialização do histórico
if "historico" not in st.session_state:
    st.session_state.historico = []

st.markdown("---") # Separador visual

col1, col2 = st.columns([0.6, 0.4])

with col1:
    st.subheader("Registrar Novo Resultado:")
    opcao = st.radio("Resultado da rodada:", ["🏠 Casa", "🤝 Empate", "✈️ Visitante"], horizontal=True, key="radio_opcao")

with col2:
    st.markdown("<br>", unsafe_allow_html=True) # Espaçamento para alinhar o botão
    resultado_map = {"🏠 Casa": "C", "✈️ Visitante": "V", "🤝 Empate": "E"}
    resultado = resultado_map[opcao]
    if st.button("➕ Inserir Resultado", key="btn_inserir"):
        st.session_state.historico.append(resultado)
        st.success(f"Resultado '{opcao}' inserido!")


st.markdown("---") # Separador visual

st.subheader("📜 Histórico Recente:")
# Visualização do histórico melhorada
hist_recente = st.session_state.historico[-30:] # Últimos 30 resultados
if hist_recente:
    # Dividir em linhas de 10
    num_cols = 10
    for i in range(0, len(hist_recente), num_cols):
        colunas_display = st.columns(num_cols)
        for j, res in enumerate(hist_recente[i:i+num_cols]):
            cor_fundo = ""
            if res == 'C':
                cor_fundo = "background-color:#E6FFE6; border-radius:5px; padding:2px;" # Verde claro
            elif res == 'V':
                cor_fundo = "background-color:#E0F2F7; border-radius:5px; padding:2px;" # Azul claro
            elif res == 'E':
                cor_fundo = "background-color:#FFFACD; border-radius:5px; padding:2px;" # Amarelo claro

            with colunas_display[j]:
                st.markdown(f"<div style='{cor_fundo}; text-align:center;'><b>{res}</b></div>", unsafe_allow_html=True)
else:
    st.info("Nenhum resultado inserido ainda. Comece a adicionar resultados para ver o histórico.")

st.markdown("---") # Separador visual

st.subheader("📊 Análise Inteligente (Estatística):")

padroes, sugestao, confianca = detectar_padroes_inteligente(st.session_state.historico)
if padroes:
    st.success(f"🔍 **Padrões encontrados:** {', '.join(padroes)}")
else:
    st.info("Nenhum padrão repetitivo significativo identificado até agora.")

st.markdown("### 🎲 Previsão de Empate (Estatística)")
chance_empate, msg_prev = prever_empate_estatistico(st.session_state.historico)

if chance_empate > 0.0 or "muito curto" not in msg_prev: # Mostra a chance mesmo que seja 0% se houver dados
    st.write(f"📈 Chance de empate na próxima rodada: **{chance_empate:.2f}%**")
    if chance_empate >= 65: # Limiares ajustados para a nova lógica
        st.success("Chance alta de empate!")
    elif chance_empate >= 40:
        st.info("Chance moderada de empate.")
    else:
        st.warning("Chance baixa de empate.")
else:
    st.warning(f"Não foi possível gerar uma previsão de empate: {msg_prev}")


if sugestao:
    cor_map = {"C": "Casa", "V": "Visitante", "E": "Empate"}
    sugestao_nome = cor_map.get(sugestao, "Desconhecido")
    st.markdown(f"🔮 **Recomendação de Padrão:** O próximo resultado mais provável, com base em padrões, é **{sugestao_nome}** (Confiabilidade: {round(confianca*100, 1)}%)")
    if confianca * 100 > 60:
        st.success("Padrão forte detectado para esta recomendação.")
    elif confianca * 100 > 40:
        st.info("Padrão moderado para esta recomendação.")
    else:
        st.warning("Padrão fraco para esta recomendação.")
else:
    st.warning("Poucos dados ou nenhum padrão claro para uma recomendação baseada em padrões.")

st.markdown("---")
if st.button("🔄 Limpar Histórico", key="btn_limpar"):
    st.session_state.historico = []
    st.experimental_rerun() # Reinicia o app para refletir a limpeza
