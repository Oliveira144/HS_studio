import streamlit as st
import numpy as np
from collections import Counter
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pandas as pd # Importar pandas para facilitar manipulação de dados

# --- Funções de Ajuda ---
def resultado_para_numerico(resultado):
    """Converte 'C', 'V', 'E' para valores numéricos."""
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
    ultima_sequencia = tuple(hist[-(janela_max-1):]) # Últimos N-1 resultados para a recomendação

    for janela in range(janela_min, janela_max + 1):
        if len(hist) < janela:
            continue
        sequencias = [tuple(hist[i:i+janela]) for i in range(len(hist) - janela + 1)]
        contagem = Counter(sequencias)
        # Filtra padrões que ocorrem mais de uma vez ou que são muito frequentes
        padroes_encontrados = {seq: freq for seq, freq in contagem.items() if freq > 1 or freq >= len(sequencias) * 0.3}
        if padroes_encontrados:
            todos_padroes[janela] = padroes_encontrados

    recomendacao_candidatos = Counter()
    for janela, padroes_na_janela in todos_padroes.items():
        # Ajusta o slice para a última sequência de acordo com a janela
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
    for janela, pats in todos_padroes.items():
        for p in pats:
            padroes_exibicao.append(f"{''.join(p)} (tam {janela})")

    return padroes_exibicao, sugestao, confianca


def prever_empate_inteligente(dados):
    """
    Função de previsão com Random Forest, usando mais features e avaliações.
    """
    if len(dados) < 30: # Aumentar o mínimo de dados para melhor treinamento
        return 0.0, "Poucos dados para análise robusta."

    X = [] # Features
    y = [] # Labels (0 para não empate, 1 para empate)

    # Geração de Features Aprimorada:
    # Vamos considerar os últimos 5 resultados, além de contagens de resultados recentes.
    for i in range(len(dados) - 6): # Necessita 5 resultados anteriores + 1 para o label
        janela_base = dados[i:i+5] # Janela de 5 resultados
        label = 1 if dados[i+5] == 'E' else 0 # O resultado que estamos tentando prever

        # Converte a janela para numérico
        janela_numerica = [resultado_para_numerico(x) for x in janela_base]

        # Features básicas da janela
        features = janela_numerica[:]

        # Contagem de C, V, E na janela
        contagem_janela = Counter(janela_base)
        features.extend([contagem_janela['C'], contagem_janela['V'], contagem_janela['E']])

        # Adiciona features ao conjunto X e label ao conjunto y
        X.append(features)
        y.append(label)

    if not any(y): # Se não houver nenhum empate nos dados, o modelo não pode aprender a prever empates
        return 0.0, "Não há empates suficientes no histórico para treinamento do modelo."
    if len(np.unique(y)) < 2: # Garante que há pelo menos 2 classes (empate e não empate)
        return 0.0, "Dados insuficientes de ambas as classes (empate/não empate) para treinamento."

    # Usar DataFrame para X para melhor visualização e manipulação se necessário
    feature_names = [f'res_{i+1}' for i in range(5)] + ['count_C', 'count_V', 'count_E']
    X_df = pd.DataFrame(X, columns=feature_names)

    # Dividir dados em treino e teste
    # Garantir que X e y têm o mesmo número de amostras
    min_samples = min(len(X_df), len(y))
    X_train, X_test, y_train, y_test = train_test_split(
        X_df.iloc[:min_samples], y[:min_samples], test_size=0.25, random_state=42, stratify=y
    )
    # Usar stratify=y ajuda a manter a proporção de classes (empate/não empate) no treino/teste

    modelo = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    # n_estimators: mais árvores, melhor performance (mas mais lento)
    # class_weight='balanced': Ajuda a lidar com o desbalanceamento de classes (geralmente poucos empates)

    modelo.fit(X_train, y_train)

    # Previsão para o último conjunto de dados disponível
    # Usar os 5 últimos resultados para a previsão mais recente
    if len(dados) < 5:
        return 0.0, "Histórico muito curto para previsão inteligente."

    ultimos_resultados = dados[-5:]
    ultimos_features_numericos = [resultado_para_numerico(x) for x in ultimos_resultados]
    contagem_ultimos = Counter(ultimos_resultados)
    ultimos_features_complementares = [contagem_ultimos['C'], contagem_ultimos['V'], contagem_ultimos['E']]

    pred_input = np.array(ultimos_features_numericos + ultimos_features_complementares).reshape(1, -1)
    
    chance_predita = 0.0
    if hasattr(modelo, 'predict_proba'):
        chance_predita = modelo.predict_proba(pred_input)[0][1] * 100
    else: # Fallback para modelos que não tem predict_proba
         chance_predita = modelo.predict(pred_input)[0] * 100 # Isso seria 0 ou 100

    # Avaliação do Modelo (para debug/informação)
    y_pred = modelo.predict(X_test)
    y_pred_proba = modelo.predict_proba(X_test)[:, 1] # Probabilidade de ser empate

    acuracia = accuracy_score(y_test, y_pred)
    # st.write(f"Acurácia do Modelo: {acuracia:.2f}")
    # st.text("Relatório de Classificação:")
    # st.text(classification_report(y_test, y_pred))

    # st.text("Matriz de Confusão:")
    # st.dataframe(pd.DataFrame(confusion_matrix(y_test, y_pred)))

    return round(chance_predita, 2), "Análise de IA concluída."

# --- Interface com o usuário ---
st.set_page_config(page_title="Football Studio HS (Inteligente)", layout="centered", page_icon="⚽") # Ícone mais relevante
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

st.subheader("📊 Análise Inteligente:")

padroes, sugestao, confianca = detectar_padroes_inteligente(st.session_state.historico)
if padroes:
    st.success(f"🔍 **Padrões encontrados:** {', '.join(padroes)}")
else:
    st.info("Nenhum padrão repetitivo significativo identificado até agora.")

st.markdown("### 🤖 Previsão de Empate com IA")
chance_empate, msg_ia = prever_empate_inteligente(st.session_state.historico)

if chance_empate > 0.0:
    st.write(f"📈 Chance de empate na próxima rodada: **{chance_empate:.2f}%**")
    if chance_empate >= 60:
        st.success("Chance alta de empate!")
    elif chance_empate >= 40:
        st.info("Chance moderada de empate.")
    else:
        st.warning("Chance baixa de empate.")
else:
    st.warning(f"Não foi possível gerar uma previsão de empate: {msg_ia}")


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
