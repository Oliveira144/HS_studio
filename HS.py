import streamlit as st
from collections import Counter

# st.set_page_config deve vir antes de qualquer comando Streamlit
st.set_page_config(page_title="Analisador de Padrões e Sugestões", layout="wide", initial_sidebar_state="expanded")

# --- Injeção de CSS para Estilização Geral (Não foca nos botões de entrada) ---
st.markdown("""
<style>
/* Estilo para o título de resultados e sugestões */
h3 {
    color: #FFD700; /* Dourado para títulos */
    margin-top: 20px;
    margin-bottom: 15px;
}

/* Estilo para os alertas/caixas de informação (sugestões, possibilidades de empate) */
div[data-testid="stAlert"] {
    background-color: #282828 !important; /* Fundo mais escuro */
    color: white !important; /* Texto branco */
    border-left: 5px solid #FFD700 !important; /* Borda dourada */
    padding: 10px !important;
    margin-bottom: 10px !important;
    border-radius: 5px !important;
}
div[data-testid="stAlert"] svg {
    color: #FFD700 !important; /* Ícone dourado */
}
div[data-testid="stAlert"] div[role="alert"] p {
    color: white !important;
}

/* Estilo para o bloco de código (sequência atual e histórico) */
div.stCodeBlock {
    background-color: #202020 !important;
    color: #00FF00 !important; /* Pode ser branco ou outra cor de texto se preferir */
    border-radius: 5px !important;
    padding: 10px !important;
    font-family: 'monospace' !important;
    overflow-x: auto !important; /* Permite scroll horizontal se a sequência for muito longa */
    white-space: pre !important; /* Mantém formatação de espaços e quebras de linha */
}

/* Ajustes gerais de espaçamento, se necessário */
/* Este seletor pode mudar entre versões do Streamlit, é para colunas - mantido apenas como exemplo */
.st-emotion-cache-k3g099 { 
    gap: 1rem !important; /* Garante espaçamento entre as colunas */
}

</style>
""", unsafe_allow_html=True)


# --- Inicialização do Session State ---
# Variáveis para armazenar o estado da aplicação
if 'current_sequence' not in st.session_state:
    st.session_state.current_sequence = []
if 'history' not in st.session_state:
    st.session_state.history = []
if 'last_analysis_results' not in st.session_state:
    st.session_state.last_analysis_results = {}
if 'last_suggestions' not in st.session_state:
    st.session_state.last_suggestions = []
if 'last_empate_possibilities' not in st.session_state:
    st.session_state.last_empate_possibilities = []


# --- Funções de Detecção de Padrões (COMPLETAS e REVISADAS) ---

def detectar_sequencia_surf(seq):
    """1. Sequência (Surf de Cor) – 3+ vezes a mesma cor seguida"""
    padroes_encontrados = []
    if len(seq) < 3:
        return padroes_encontrados
    i = 0
    while i < len(seq) - 2:
        if seq[i] == seq[i+1] == seq[i+2]:
            j = i + 3
            while j < len(seq) and seq[j] == seq[i]:
                j += 1
            padroes_encontrados.append(f"Sequência de '{seq[i]}' por {j-i} vezes, iniciando na posição {i+1}.")
            i = j
        else:
            i += 1
    return padroes_encontrados

def detectar_zig_zag(seq):
    """2. Zig-Zag – alternância de cores (ex: Casa, Visitante, Casa, Visitante...)"""
    padroes_encontrados = []
    if len(seq) < 2:
        return padroes_encontrados
    i = 0
    while i < len(seq) - 1:
        if seq[i] != seq[i+1]:
            j = i + 2
            while j < len(seq) - 1 and seq[j] == seq[i] and seq[j+1] == seq[i+1]:
                j += 2
            if j - i >= 4: # Pelo menos 2 pares para ser um zig-zag reconhecível
                padroes_encontrados.append(f"Padrão Zig-Zag detectado: {''.join(seq[i:j])} iniciando na posição {i+1}.")
            i = j
        else:
            i += 1
    return padroes_encontrados

def detectar_quebra_surf(seq):
    """3. Quebra de Surf – sequência que é interrompida"""
    padroes_encontrados = []
    if len(seq) < 4:
        return padroes_encontrados
    for i in range(len(seq) - 3):
        if seq[i] == seq[i+1] == seq[i+2] and seq[i+3] != seq[i]:
            padroes_encontrados.append(f"Quebra de Surf detectada: '{seq[i]}' interrompido por '{seq[i+3]}' na posição {i+4}.")
    return padroes_encontrados

def detectar_quebra_zig_zag(seq):
    """4. Quebra de Zig-Zag – padrão alternado que quebra"""
    padroes_encontrados = []
    if len(seq) < 4:
        return padroes_encontrados
    for i in range(len(seq) - 3):
        # Verifica se é um zig-zag de 3 elementos (A, B, A) e o 4º elemento (C) quebra (C != A e C != B)
        if seq[i] != seq[i+1] and seq[i+1] != seq[i+2] and seq[i] == seq[i+2] and \
           seq[i+3] != seq[i] and seq[i+3] != seq[i+1]:
             padroes_encontrados.append(f"Quebra de Zig-Zag detectada: {''.join(seq[i:i+3])} interrompido por '{seq[i+3]}' na posição {i+4}.")
    return padroes_encontrados

def detectar_duplas_repetidas(seq):
    """5. Duplas repetidas – Casa, Casa, Visitante, Visitante... (AABB)"""
    padroes_encontrados = []
    if len(seq) < 4:
        return padroes_encontrados
    for i in range(len(seq) - 3):
        if seq[i] == seq[i+1] and seq[i+2] == seq[i+3] and seq[i] != seq[i+2]:
            padroes_encontrados.append(f"Duplas Repetidas detectadas: '{seq[i]}', '{seq[i+2]}' iniciando na posição {i+1}.")
    return padroes_encontrados

def detectar_empate_recorrente(seq, empate_char='E'):
    """6. Empate recorrente – Empates aparecendo em intervalos curtos (2 ou 3 resultados entre empates)"""
    padroes_encontrados = []
    indices_empate = [i for i, x in enumerate(seq) if x == empate_char]
    if len(indices_empate) < 2:
        return padroes_encontrados
    for i in range(len(indices_empate) - 1):
        diff = indices_empate[i+1] - indices_empate[i]
        # Se a diferença for 2 (E X E) ou 3 (E X Y E)
        if diff >= 2 and diff <= 3:
            padroes_encontrados.append(f"Empate Recorrente detectado entre posições {indices_empate[i]+1} e {indices_empate[i+1]+1} (intervalo de {diff-1} não-empates).")
    return padroes_encontrados

def detectar_padrao_escada(seq):
    """7. Padrão Escada – Ex: 1 Casa, 2 Visitantes, 3 Casas (ABABBB ou similar, adaptado)"""
    padroes_encontrados = []
    if len(seq) < 6:
        return padroes_encontrados
    for i in range(len(seq) - 5): # <<< AQUI ESTAVA O ERRO DE INDENTAÇÃO NA IMAGEM
        # Exemplo de escada: A, BB, AAA (1 do tipo A, 2 do tipo B, 3 do tipo A)
        if (seq[i] != seq[i+1] and # 1 elemento do primeiro tipo
            seq[i+1] == seq[i+2] and seq[i+1] != seq[i] and # 2 elementos do segundo tipo
            seq[i+3] == seq[i+4] == seq[i+5] and seq[i+3] == seq[i] # 3 elementos do primeiro tipo (o mesmo do primeiro)
        ):
            padroes_encontrados.append(f"Padrão Escada (1-{seq[i]}, 2-{seq[i+1]}, 3-{seq[i]}) detectado iniciando na posição {i+1}.")
    return padroes_encontrados

def detectar_espelho(seq):
    """8. Espelho – Ex: Casa, Visitante, Visitante, Casa (ABBA)"""
    padroes_encontrados = []
    if len(seq) < 4:
        return padroes_encontrados
    for i in range(len(seq) - 3):
        if seq[i] == seq[i+3] and seq[i+1] == seq[i+2] and seq[i] != seq[i+1]:
            padroes_encontrados.append(f"Padrão Espelho detectado: {''.join(seq[i:i+4])} iniciando na posição {i+1}.")
    return padroes_encontrados

def detectar_alternancia_empate_meio(seq, empate_char='E'):
    """9. Alternância com empate no meio – Ex: Casa, Empate, Visitante (A E B)"""
    padroes_encontrados = []
    if len(seq) < 3:
        return padroes_encontrados
    for i in range(len(seq) - 2):
        if seq[i+1] == empate_char and seq[i] != empate_char and seq[i+2] != empate_char and seq[i] != seq[i+2]:
            padroes_encontrados.append(f"Alternância com Empate no Meio detectada: {''.join(seq[i:i+3])} iniciando na posição {i+1}.")
    return padroes_encontrados

def detectar_padrao_onda(seq):
    """10. Padrão "onda" – Ex: C, V, C, V (1-2-1-2 de cores) - Similar ao Zig-Zag, mas focado na repetição exata de 4 elementos"""
    padroes_encontrados = []
    if len(seq) < 4:
        return padroes_encontrados
    for i in range(len(seq) - 3):
        if seq[i] == seq[i+2] and seq[i+1] == seq[i+3] and seq[i] != seq[i+1]:
            padroes_encontrados.append(f"Padrão Onda (1-2-1-2) detectado: {''.join(seq[i:i+4])} iniciando na posição {i+1}.")
    return padroes_encontrados

def analisar_previsao_tatica(seq):
    """11. Padrões com base nos últimos 5/7/10 jogos – para previsão tática (mais frequente)"""
    padroes_encontrados = []
    if len(seq) >= 5:
        ultimos_5 = seq[-5:]
        contagem = Counter(ultimos_5)
        mais_frequente = contagem.most_common(1)
        if mais_frequente:
            padroes_encontrados.append(f"Nos últimos 5 resultados, '{mais_frequente[0][0]}' apareceu {mais_frequente[0][1]} vezes.")
    if len(seq) >= 7:
        ultimos_7 = seq[-7:]
        contagem = Counter(ultimos_7)
        mais_frequente = contagem.most_common(1)
        if mais_frequente:
            padroes_encontrados.append(f"Nos últimos 7 resultados, '{mais_frequente[0][0]}' apareceu {mais_frequente[0][1]} vezes.")
    if len(seq) >= 10:
        ultimos_10 = seq[-10:]
        contagem = Counter(ultimos_10)
        mais_frequente = contagem.most_common(1)
        if mais_frequente:
            padroes_encontrados.append(f"Nos últimos 10 resultados, '{mais_frequente[0][0]}' apareceu {mais_frequente[0][1]} vezes.")
    return padroes_encontrados

def detectar_padrao_3x1(seq):
    """12. Padrão 3x1 – Três ocorrências de um tipo, seguida por uma de outro (AAAB)"""
    padroes_encontrados = []
    if len(seq) < 4:
        return padroes_encontrados
    for i in range(len(seq) - 3):
        if seq[i] == seq[i+1] == seq[i+2] and seq[i+3] != seq[i]:
            padroes_encontrados.append(f"Padrão 3x1 detectado: '{seq[i]}' (3x) seguido por '{seq[i+3]}' (1x) na posição {i+1}.")
    return padroes_encontrados

def detectar_padrao_3x3(seq):
    """13. Padrão 3x3 – Três ocorrências de um tipo, seguida por três de outro (AAABBB)"""
    padroes_encontrados = []
    if len(seq) < 6:
        return padroes_encontrados
    for i in range(len(seq) - 5):
        if seq[i] == seq[i+1] == seq[i+2] and seq[i+3] == seq[i+4] == seq[i+5] and seq[i] != seq[i+3]:
            padroes_encontrados.append(f"Padrão 3x3 detectado: '{seq[i]}' (3x) seguido por '{seq[i+3]}' (3x) na posição {i+1}.")
    return padroes_encontrados


# --- Funções de Sugestão ---
def gerar_sugestoes(sequence_list, resultados_encontrados):
    sugestoes = []
    possibilidades_empate = []
    ultima_ocorrencia = sequence_list[-1] if sequence_list else None
    penultima_ocorrencia = sequence_list[-2] if len(sequence_list) >= 2 else None

    # Sugestões baseadas nos padrões detectados
    # Acessa os resultados usando .get() para evitar KeyError se a chave não existir
    # Acessa os resultados usando .get() para evitar KeyError se a chave não existir
    if resultados_encontrados.get("1. Sequência (Surf de Cor)"):
        for res in resultados_encontrados["1. Sequência (Surf de Cor)"]:
            if ultima_ocorrencia and f"Sequência de '{ultima_ocorrencia}'" in res:
                try:
                    # Extração mais robusta de start_pos e pattern_length
                    parts = res.split("iniciando na posição ")
                    if len(parts) > 1:
                        start_pos_str = parts[-1].replace(".", "")
                        start_pos = int(start_pos_str)
                    else:
                        continue # Pula se o formato da string for inesperado

                    parts_length = res.split("por ")
                    if len(parts_length) > 1:
                        pattern_length_str = parts_length[-1].split(" vezes")[0]
                        pattern_length = int(pattern_length_str)
                    else:
                        continue # Pula se o formato da string for inesperado

                    if (start_pos + pattern_length - 1) == len(sequence_list):
                         sugestoes.append(f"**Sugestão:** Continuar o 'Surf de Cor' de **'{ultima_ocorrencia}'**.")
                except ValueError:
                    pass

    if resultados_encontrados.get("2. Zig-Zag"):
        if ultima_ocorrencia and penultima_ocorrencia and len(sequence_list) >= 2:
            if (penultima_ocorrencia != ultima_ocorrencia): # É uma alternância
                if len(sequence_list) >= 4 and sequence_list[-4] == penultima_ocorrencia and sequence_list[-3] == ultima_ocorrencia:
                    sugestoes.append(f"**Sugestão:** Continuar o 'Zig-Zag' com **'{penultima_ocorrencia}'**.")

    if resultados_encontrados.get("3. Quebra de Surf"):
        if ultima_ocorrencia and len(sequence_list) >= 4 and \
           sequence_list[-4] == sequence_list[-3] == sequence_list[-2] and \
           ultima_ocorrencia != sequence_list[-4]:
            sugestoes.append(f"**Atenção:** 'Quebra de Surf' recente. O último foi '{ultima_ocorrencia}'.")

    if resultados_encontrados.get("4. Quebra de Zig-Zag"):
        # A, B, A (quebra) C -> C não é A nem B
        if ultima_ocorrencia and len(sequence_list) >= 4:
            if (sequence_list[-4] == sequence_list[-2] and sequence_list[-3] != sequence_list[-4] and \
                ultima_ocorrencia != sequence_list[-4] and ultima_ocorrencia != sequence_list[-3]):
                sugestoes.append(f"**Atenção:** 'Quebra de Zig-Zag' recente. Próximo pode não seguir a alternância original.")

    if resultados_encontrados.get("5. Duplas repetidas"):
        if ultima_ocorrencia and penultima_ocorrencia and \
           len(sequence_list) >= 4 and \
           sequence_list[-4] == sequence_list[-3] and \
           penultima_ocorrencia == ultima_ocorrencia and \
           sequence_list[-4] != ultima_ocorrencia:
            sugestoes.append(f"**Considerar:** Padrão de 'Duplas Repetidas' (Ex: AABB). Pode haver uma nova dupla ou quebra de padrão.")

    if resultados_encontrados.get("6. Empate recorrente"):
        if resultados_encontrados["6. Empate recorrente"]:
            possibilidades_empate.append("**Alta Possibilidade:** 'Empate' devido à recorrência.")
            sugestoes.append("Considerar 'Empate' devido à recorrência.") # Adicionado aqui para aparecer nas sugestões também

    if resultados_encontrados.get("8. Espelho"):
        if ultima_ocorrencia and len(sequence_list) >= 4 and \
           sequence_list[-4] == ultima_ocorrencia and \
           sequence_list[-3] == penultima_ocorrencia:
            sugestoes.append(f"**Sugestão:** Padrão 'Espelho' detectado. Próximo pode inverter ou ser similar ao início ('{penultima_ocorrencia}').")

    if resultados_encontrados.get("9. Alternância com empate no meio"):
        if ultima_ocorrencia and penultima_ocorrencia and len(sequence_list) >= 3 and \
           sequence_list[-2] == 'E' and ultima_ocorrencia != 'E' and sequence_list[-3] != 'E' and \
           sequence_list[-3] != ultima_ocorrencia:
            possibilidades_empate.append(f"**Possibilidade:** 'Empate' como meio de alternância. (Ex: {sequence_list[-3]}, E, {ultima_ocorrencia})")
            sugestoes.append("Considerar 'Empate' devido à alternância com empate no meio.")

    if resultados_encontrados.get("10. Padrão 'onda'"):
        if ultima_ocorrencia and penultima_ocorrencia and \
           len(sequence_list) >= 4 and \
           sequence_list[-4] == penultima_ocorrencia and \
           sequence_list[-3] == ultima_ocorrencia:
            sugestoes.append(f"**Sugestão:** Continuar o 'Padrão Onda' com **'{penultima_ocorrencia}'**.")

    if resultados_encontrados.get("12. Padrão 3x1"):
        if ultima_ocorrencia and len(sequence_list) >= 4 and \
           sequence_list[-4] == sequence_list[-3] == sequence_list[-2] and \
           sequence_list[-1] != sequence_list[-4]:
            sugestoes.append(f"**Atenção:** Padrão 3x1 detectado ('{sequence_list[-4]}' 3x, '{ultima_ocorrencia}' 1x). Pode indicar mudança ou continuação da última.")

    if resultados_encontrados.get("13. Padrão 3x3"):
        if ultima_ocorrencia and len(sequence_list) >= 6 and \
           sequence_list[-6] == sequence_list[-5] == sequence_list[-4] and \
           sequence_list[-3] == sequence_list[-2] == sequence_list[-1] and \
           sequence_list[-6] != sequence_list[-3]:
            sugestoes.append(f"**Atenção:** Padrão 3x3 detectado. Fim de um ciclo (3x '{sequence_list[-6]}', 3x '{sequence_list[-3]}'). Pode iniciar nova tendência.")

    # Sugestões gerais sobre Empate (frequência, ausência)
    empate_count = sequence_list.count('E')
    total_results = len(sequence_list)
    if total_results > 0:
        freq_empate = empate_count / total_results
        if freq_empate > 0.33 and total_results > 3:
            possibilidades_empate.append("A alta frequência de empates na sequência atual sugere maior probabilidade de novo 'Empate'.")
        elif empate_count == 0 and total_results > 5:
            possibilidades_empate.append("Ausência prolongada de empates pode indicar um 'Empate' em breve (lei das médias/compensação).")
        # Análise pós-empate para o que veio depois
        if total_results >= 2 and ultima_ocorrencia != 'E' and penultima_ocorrencia == 'E':
            sugestoes.append(f"**Análise Pós-Empate:** O último resultado foi '{ultima_ocorrencia}' após um empate.")


    return sugestoes, possibilidades_empate


# --- Título e Descrição da Aplicação ---
st.header("Análise de Padrões em Sequências de Resultados")
st.markdown("Utilize os botões abaixo para inserir os resultados (Casa, Visitante, Empate) e a análise será **automática**.")

# --- Layout Principal: Colunas para Entrada/Sequência e Sugestões/Resultados ---
col_input_seq, col_suggestions_results = st.columns([1, 2])

with col_input_seq:
    st.subheader("➕ Inserir Resultado")
    st.markdown("Clique para adicionar à sequência atual:")

    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        # Usando os botões padrão do Streamlit. As cores serão as do tema default ou do config.toml
        if st.button("Casa (C)", use_container_width=True, key="btn_casa"):
            st.session_state.current_sequence.append('C')
            st.rerun()
    with btn_col2:
        if st.button("Visitante (V)", use_container_width=True, key="btn_visitante"):
            st.session_state.current_sequence.append('V')
            st.rerun()
    with btn_col3:
        if st.button("Empate (E)", use_container_width=True, key="btn_empate"):
            st.session_state.current_sequence.append('E')
            st.rerun()

    st.markdown("---")
    st.subheader("Ações da Sequência")
    # Botões de ação também com estilo padrão do Streamlit
    if st.button("↩️ Desfazer Último", use_container_width=True, key="btn_undo"):
        if st.session_state.current_sequence:
            st.session_state.current_sequence.pop()
            st.success("Último resultado desfeito!")
            st.rerun()
        else:
            st.warning("Sequência vazia. Nada para desfazer.")
    if st.button("🔄 Limpar Sequência Atual", use_container_width=True, key="btn_clear_current"):
        st.session_state.current_sequence = []
        st.success("Sequência atual limpa!")
        st.rerun()

    st.markdown("---")
    st.subheader("📊 Sequência Atual")
    if st.session_state.current_sequence:
        current_seq_str = "".join(st.session_state.current_sequence)

        formatted_indices_line = ""
        formatted_results_line = ""
        
        # Determina a largura máxima necessária para o índice + espaço
        max_idx_len = len(str(len(current_seq_str))) 
        if max_idx_len < 2: max_idx_len = 2 # Garante pelo menos 2 para alinhamento inicial

        for i, char in enumerate(current_seq_str):
            idx_str = str(i + 1)
            # Adiciona espaços para que o índice ocupe a `max_idx_len` + 1 espaço de padding
            formatted_indices_line += idx_str.rjust(max_idx_len) + " " 
            formatted_results_line += char.rjust(max_idx_len) + " " # Alinha o caractere com a mesma largura
        
        st.code(f"Posições:  {formatted_indices_line.strip()}\nResultados: {formatted_results_line.strip()}")
        
        st.info(f"**DEBUG:** A sequência completa sendo analisada (do mais antigo ao mais recente) é: `{current_seq_str}`")

    else:
        st.info("Nenhum resultado adicionado ainda.")


with col_suggestions_results:
    # --- Executar Análise Automaticamente (e armazenar no session_state) ---
    if st.session_state.current_sequence:
        current_seq_for_analysis = list(st.session_state.current_sequence)

        # Dicionário para armazenar os resultados de cada padrão
        resultados_encontrados = {
            "1. Sequência (Surf de Cor)": [], "2. Zig-Zag": [], "3. Quebra de Surf": [],
            "4. Quebra de Zig-Zag": [], "5. Duplas repetidas": [], "6. Empate recorrente": [],
            "7. Padrão Escada": [], "8. Espelho": [], "9. Alternância com empate no meio": [],
            "10. Padrão 'onda'": [], "11. Padrões de Previsão Tática": [],
            "12. Padrão 3x1": [], "13. Padrão 3x3": []
        }

        # Executa cada função de detecção de padrão
        resultados_encontrados["1. Sequência (Surf de Cor)"] = detectar_sequencia_surf(current_seq_for_analysis)
        resultados_encontrados["2. Zig-Zag"] = detectar_zig_zag(current_seq_for_analysis)
        resultados_encontrados["3. Quebra de Surf"] = detectar_quebra_surf(current_seq_for_analysis)
        resultados_encontrados["4. Quebra de Zig-Zag"] = detectar_quebra_zig_zag(current_seq_for_analysis)
        resultados_encontrados["5. Duplas repetidas"] = detectar_duplas_repetidas(current_seq_for_analysis)
        resultados_encontrados["6. Empate recorrente"] = detectar_empate_recorrente(current_seq_for_analysis)
        resultados_encontrados["7. Padrão Escada"] = detectar_padrao_escada(current_seq_for_analysis)
        resultados_encontrados["8. Espelho"] = detectar_espelho(current_seq_for_analysis)
        resultados_encontrados["9. Alternância com empate no meio"] = detectar_alternancia_empate_meio(current_seq_for_analysis)
        resultados_encontrados["10. Padrão 'onda'"] = detectar_padrao_onda(current_seq_for_analysis)
        resultados_encontrados["11. Padrões de Previsão Tática"] = analisar_previsao_tatica(current_seq_for_analysis)
        resultados_encontrados["12. Padrão 3x1"] = detectar_padrao_3x1(current_seq_for_analysis)
        resultados_encontrados["13. Padrão 3x3"] = detectar_padrao_3x3(current_seq_for_analysis)

        # Gera as sugestões e possibilidades de empate
        sugestoes, possibilidades_empate = gerar_sugestoes(current_seq_for_analysis, resultados_encontrados)

        # Salva os resultados no session_state para persistência
        st.session_state.last_analysis_results = resultados_encontrados
        st.session_state.last_suggestions = sugestoes
        st.session_state.last_empate_possibilities = possibilidades_empate

        # Adiciona a sequência atual ao histórico (se for diferente da última entrada)
        current_seq_as_string = "".join(st.session_state.current_sequence)
        if not st.session_state.history or current_seq_as_string != st.session_state.history[-1]:
            st.session_state.history.append(current_seq_as_string)
    else:
        # Limpa os resultados se a sequência estiver vazia
        st.session_state.last_analysis_results = {}
        st.session_state.last_suggestions = []
        st.session_state.last_empate_possibilities = []

    st.subheader("🎯 Sugestões de Entradas")
    if st.session_state.last_suggestions: 
        st.markdown("**Considerando os padrões e tendências da sequência atual:**")
        for s in st.session_state.last_suggestions:
            st.info(f"- {s}")
    else:
        st.info("Não há sugestões claras de entradas com base nos padrões detectados nesta sequência.")

    st.markdown("---")
    st.subheader("🤝 Possibilidade de Empate")
    if st.session_state.last_empate_possibilities:
        st.markdown("**Fatores que indicam possibilidade de empate:**")
        for pe in st.session_state.last_empate_possibilities:
            st.warning(f"- {pe}")
    else:
        st.info("Nenhuma tendência forte para 'Empate' detectada nesta sequência.")

    st.markdown("---")
    st.subheader("📈 Padrões Detectados")
    if st.session_state.last_analysis_results:
        algum_padrao_detectado_display = False
        for padrao, resultados in st.session_state.last_analysis_results.items():
            if resultados:
                st.success(f"✔️ **{padrao}:**")
                for res in resultados:
                    st.write(f"- {res}")
                algum_padrao_detectado_display = True
        if not algum_padrao_detectado_display:
            st.info("Nenhum dos padrões definidos foi detectado na sequência fornecida.")
    else:
        st.info("Adicione resultados para ver a análise de padrões.")

st.markdown("---")
st.subheader("📚 Histórico de Análises")

# Botão para zerar o histórico
if st.button("🧹 Zerar Histórico", use_container_width=True, key="btn_clear_history"):
    st.session_state.history = []
    st.success("Histórico zerado!")
    st.rerun() # Recarrega a página para refletir a mudança imediatamente

if st.session_state.history:
    for i, entry in enumerate(st.session_state.history):
        formatted_indices_line_hist = ""
        formatted_results_line_hist = ""
        
        max_idx_len_hist = len(str(len(entry)))
        if max_idx_len_hist < 2: max_idx_len_hist = 2

        for j, char_hist in enumerate(entry):
            idx_str_hist = str(j + 1)
            formatted_indices_line_hist += idx_str_hist.rjust(max_idx_len_hist) + " "
            formatted_results_line_hist += char_hist.rjust(max_idx_len_hist) + " "

        st.code(f"Análise {i+1}:\nPosições:  {formatted_indices_line_hist.strip()}\nResultados: {formatted_results_line_hist.strip()}")
else:
    st.info("Nenhum histórico de análises ainda.")


st.markdown("---")
st.markdown("Desenvolvido para análise de padrões. Lembre-se: sugestões são baseadas em heurísticas e não garantem resultados.")
