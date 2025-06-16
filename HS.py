import streamlit as st
from collections import Counter

st.set_page_config(page_title="Analisador de Padrões e Sugestões", layout="wide", initial_sidebar_state="expanded")

# --- Inicialização do Session State ---
if 'current_sequence' not in st.session_state:
    st.session_state.current_sequence = []
if 'history' not in st.session_state:
    st.session_state.history = []

# --- Funções de Detecção de Padrões (Mesmas do código anterior) ---
# Copie e cole todas as funções de detecção de padrões aqui:
# detectar_sequencia_surf, detectar_zig_zag, detectar_quebra_surf,
# detectar_quebra_zig_zag, detectar_duplas_repetidas, detectar_empate_recorrente,
# detectar_padrao_escada, detectar_espelho, detectar_alternancia_empate_meio,
# detectar_padrao_onda, analisar_previsao_tatica, detectar_padrao_3x1, detectar_padrao_3x3

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
            i = j # Move o índice para depois do surf detectado
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
            if j - i >= 4:
                padroes_encontrados.append(f"Padrão Zig-Zag detectado: {seq[i:j]} iniciando na posição {i+1}.")
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
        if seq[i] != seq[i+1] and seq[i+1] != seq[i+2] and seq[i] == seq[i+2] and seq[i+3] != seq[i] and seq[i+3] != seq[i+1]:
             padroes_encontrados.append(f"Quebra de Zig-Zag detectada: {seq[i:i+3]} interrompido por '{seq[i+3]}' na posição {i+4}.")
    return padroes_encontrados

def detectar_duplas_repetidas(seq):
    """5. Duplas repetidas – Casa, Casa, Visitante, Visitante..."""
    padroes_encontrados = []
    if len(seq) < 4:
        return padroes_encontrados

    for i in range(len(seq) - 3):
        if seq[i] == seq[i+1] and seq[i+2] == seq[i+3] and seq[i] != seq[i+2]:
            padroes_encontrados.append(f"Duplas Repetidas detectadas: '{seq[i]}', '{seq[i+2]}' iniciando na posição {i+1}.")
    return padroes_encontrados

def detectar_empate_recorrente(seq, empate_char='E'):
    """6. Empate recorrente – Empates aparecendo em intervalos curtos"""
    padroes_encontrados = []
    indices_empate = [i for i, x in enumerate(seq) if x == empate_char]

    if len(indices_empate) < 2:
        return padroes_encontrados

    for i in range(len(indices_empate) - 1):
        diff = indices_empate[i+1] - indices_empate[i]
        if diff >= 2 and diff <= 3:
            padroes_encontrados.append(f"Empate Recorrente detectado entre posições {indices_empate[i]+1} e {indices_empate[i+1]+1} (intervalo de {diff-1} não-empates).")
    return padroes_encontrados

def detectar_padrao_escada(seq):
    """7. Padrão Escada – 1 Casa, 2 Visitantes, 3 Casas... (Adaptar para cores/resultados)"""
    padroes_encontrados = []
    if len(seq) < 6:
        return padroes_encontrados

    for i in range(len(seq) - 5):
        if (seq[i] != seq[i+1] and
            seq[i+1] == seq[i+2] and seq[i+1] != seq[i] and
            seq[i+3] == seq[i+4] == seq[i+5] and seq[i+3] == seq[i]
        ):
            padroes_encontrados.append(f"Padrão Escada (1-{seq[i]}, 2-{seq[i+1]}, 3-{seq[i]}) detectado iniciando na posição {i+1}.")
    return padroes_encontrado

def detectar_espelho(seq):
    """8. Espelho – Ex: Casa, Visitante, Visitante, Casa"""
    padroes_encontrados = []
    if len(seq) < 4:
        return padroes_encontrados

    for i in range(len(seq) - 3):
        if seq[i] == seq[i+3] and seq[i+1] == seq[i+2] and seq[i] != seq[i+1]:
            padroes_encontrados.append(f"Padrão Espelho detectado: {seq[i:i+4]} iniciando na posição {i+1}.")
    return padroes_encontrados

def detectar_alternancia_empate_meio(seq, empate_char='E'):
    """9. Alternância com empate no meio – Casa, Empate, Visitante"""
    padroes_encontrados = []
    if len(seq) < 3:
        return padroes_encontrados

    for i in range(len(seq) - 2):
        if seq[i+1] == empate_char and seq[i] != empate_char and seq[i+2] != empate_char and seq[i] != seq[i+2]:
            padroes_encontrados.append(f"Alternância com Empate no Meio detectada: {seq[i:i+3]} iniciando na posição {i+1}.")
    return padroes_encontrados

def detectar_padrao_onda(seq):
    """10. Padrão "onda" – Ex: 1-2-1-2 de cores"""
    padroes_encontrados = []
    if len(seq) < 4:
        return padroes_encontrados

    for i in range(len(seq) - 3):
        if seq[i] == seq[i+2] and seq[i+1] == seq[i+3] and seq[i] != seq[i+1]:
            padroes_encontrados.append(f"Padrão Onda (1-2-1-2) detectado: {seq[i:i+4]} iniciando na posição {i+1}.")
    return padroes_encontrados

def analisar_previsao_tatica(seq):
    """11. Padrões com base nos últimos 5/7/10 jogos – para previsão tática"""
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
    """12. Padrão 3x1 – Três ocorrências de um tipo, seguida por uma de outro."""
    padroes_encontrados = []
    if len(seq) < 4:
        return padroes_encontrados

    for i in range(len(seq) - 3):
        if seq[i] == seq[i+1] == seq[i+2] and seq[i+3] != seq[i]:
            padroes_encontrados.append(f"Padrão 3x1 detectado: '{seq[i]}' (3x) seguido por '{seq[i+3]}' (1x) na posição {i+1}.")
    return padroes_encontrados

def detectar_padrao_3x3(seq):
    """13. Padrão 3x3 – Três ocorrências de um tipo, seguida por três de outro."""
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
    if resultados_encontrados.get("1. Sequência (Surf de Cor)"):
        for res in resultados_encontrados["1. Sequência (Surf de Cor)"]:
            if f"'{ultima_ocorrencia}'" in res:
                sugestoes.append(f"**Sugestão:** Continuar o 'Surf de Cor' de **'{ultima_ocorrencia}'**.")

    if resultados_encontrados.get("2. Zig-Zag"):
        for res in resultados_encontrados["2. Zig-Zag"]:
            if ultima_ocorrencia and penultima_ocorrencia and f"{penultima_ocorrencia},{ultima_ocorrencia}" in res:
                sugestoes.append(f"**Sugestão:** Continuar o 'Zig-Zag' com **'{penultima_ocorrencia}'**.")

    if resultados_encontrados.get("3. Quebra de Surf"):
        if ultima_ocorrencia and penultima_ocorrencia and st.session_state.current_sequence.count(penultima_ocorrencia) >= 3 and ultima_ocorrencia != penultima_ocorrencia:
            sugestoes.append(f"**Atenção:** 'Quebra de Surf' recente. Próximo pode **não** ser '{ultima_ocorrencia}'.")

    if resultados_encontrados.get("4. Quebra de Zig-Zag"):
        sugestoes.append(f"**Atenção:** 'Quebra de Zig-Zag' recente. Próximo pode não seguir a alternância original.")

    if resultados_encontrados.get("5. Duplas repetidas"):
        sugestoes.append(f"**Considerar:** Padrão de 'Duplas Repetidas'. Pode haver uma nova dupla ou quebra de padrão.")

    if resultados_encontrados.get("6. Empate recorrente"):
        possibilidades_empate.append("**Alta Possibilidade:** 'Empate' devido à recorrência.")
        sugestoes.append("Considerar 'Empate' devido à recorrência.")

    if resultados_encontrados.get("8. Espelho"):
        sugestoes.append(f"**Sugestão:** Padrão 'Espelho' detectado. Próximo pode seguir o inverso ou repetir o início.")

    if resultados_encontrados.get("9. Alternância com empate no meio"):
        possibilidades_empate.append(f"**Possibilidade:** 'Empate' como meio de alternância. (Ex: C, E, V)")
        sugestoes.append("Considerar 'Empate' devido à alternância com empate no meio.")

    if resultados_encontrados.get("10. Padrão 'onda'"):
        if ultima_ocorrencia and penultima_ocorrencia and ultima_ocorrencia != penultima_ocorrencia:
            sugestoes.append(f"**Sugestão:** Continuar o 'Padrão Onda' com **'{penultima_ocorrencia}'**.")

    if resultados_encontrados.get("12. Padrão 3x1"):
        if ultima_ocorrencia and len(sequence_list) >= 4 and sequence_list[-4] == sequence_list[-3] == sequence_list[-2] and sequence_list[-1] != sequence_list[-4]:
            sugestoes.append(f"**Atenção:** Padrão 3x1 detectado. Próximo pode continuar o '{ultima_ocorrencia}' ou iniciar nova sequência.")

    if resultados_encontrados.get("13. Padrão 3x3"):
        if ultima_ocorrencia and len(sequence_list) >= 6 and sequence_list[-6] == sequence_list[-5] == sequence_list[-4] and sequence_list[-3] == sequence_list[-2] == sequence_list[-1] and sequence_list[-6] != sequence_list[-3]:
            sugestoes.append(f"**Atenção:** Padrão 3x3 detectado. Fim de um ciclo, pode iniciar nova sequência.")


    # Sugestões gerais sobre Empate (mesma lógica anterior, mas agora como sugestão explícita)
    empate_count = sequence_list.count('E')
    if sequence_list:
        if empate_count > len(sequence_list) / 3 and len(sequence_list) > 3: # Mais de 33% de empates e sequência razoável
            possibilidades_empate.append("A alta frequência de empates sugere maior probabilidade de novo 'Empate'.")
        elif empate_count == 0 and len(sequence_list) > 5:
            possibilidades_empate.append("Ausência prolongada de empates pode indicar um 'Empate' em breve (lei das médias).")
        # Analisar se o último foi não-empate e o penúltimo foi empate (ex: V,E) pode sugerir não-empate
        if len(sequence_list) >= 2 and ultima_ocorrencia != 'E' and penultima_ocorrencia == 'E':
            sugestoes.append(f"Pós-Empate: O último resultado foi '{ultima_ocorrencia}'.")


    return sugestoes, possibilidades_empate

# --- Título e Descrição da Aplicação ---
st.header("Análise de Padrões em Sequências de Resultados")
st.markdown("Utilize os botões abaixo para inserir os resultados (Casa, Visitante, Empate) e analisar os padrões.")

# --- Layout Dinâmico ---
# Colunas para entrada de dados e visualização da sequência
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("➕ Inserir Resultado")
    st.markdown("Clique para adicionar à sequência atual:")

    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        if st.button("Casa (C)", use_container_width=True):
            st.session_state.current_sequence.append('C')
    with btn_col2:
        if st.button("Visitante (V)", use_container_width=True):
            st.session_state.current_sequence.append('V')
    with btn_col3:
        if st.button("Empate (E)", use_container_width=True):
            st.session_state.current_sequence.append('E')

    st.markdown("---")
    st.subheader("Ações")
    if st.button("🔄 Limpar Sequência Atual", use_container_width=True):
        st.session_state.current_sequence = []
        st.success("Sequência atual limpa!")
    if st.button("✅ Analisar Sequência", type="primary", use_container_width=True):
        pass # A lógica de análise será executada após este bloco


with col2:
    st.subheader("📊 Sequência Atual")
    if st.session_state.current_sequence:
        # Exibe a sequência atual em blocos de 9
        current_seq_str = "".join(st.session_state.current_sequence)
        formatted_current_seq = ""
        for j in range(0, len(current_seq_str), 9):
            formatted_current_seq += current_seq_str[j:j+9] + " " # Adiciona espaço entre blocos
        st.code(f"{formatted_current_seq.strip()}")
    else:
        st.info("Nenhum resultado adicionado ainda.")

# --- Executar Análise e Exibir Resultados (Após os botões de ação) ---
if st.button("✅ Analisar Sequência", type="primary", key="analyze_button_bottom", use_container_width=True):
    if not st.session_state.current_sequence:
        st.warning("Por favor, adicione resultados à sequência para analisar.")
    else:
        # Adiciona a sequência atual ao histórico
        st.session_state.history.append("".join(st.session_state.current_sequence))

        st.subheader("🔍 Resultados da Análise")
        st.write(f"Sequência analisada: **{', '.join(st.session_state.current_sequence)}**")
        st.markdown("---")

        resultados_encontrados = {}
        resultados_encontrados["1. Sequência (Surf de Cor)"] = detectar_sequencia_surf(st.session_state.current_sequence)
        resultados_encontrados["2. Zig-Zag"] = detectar_zig_zag(st.session_state.current_sequence)
        resultados_encontrados["3. Quebra de Surf"] = detectar_quebra_surf(st.session_state.current_sequence)
        resultados_encontrados["4. Quebra de Zig-Zag"] = detectar_quebra_zig_zag(st.session_state.current_sequence)
        resultados_encontrados["5. Duplas repetidas"] = detectar_duplas_repetidas(st.session_state.current_sequence)
        resultados_encontrados["6. Empate recorrente"] = detectar_empate_recorrente(st.session_state.current_sequence)
        resultados_encontrados["7. Padrão Escada"] = detectar_padrao_escada(st.session_state.current_sequence)
        resultados_encontrados["8. Espelho"] = detectar_espelho(st.session_state.current_sequence)
        resultados_encontrados["9. Alternância com empate no meio"] = detectar_alternancia_empate_meio(st.session_state.current_sequence)
        resultados_encontrados["10. Padrão 'onda'"] = detectar_padrao_onda(st.session_state.current_sequence)
        resultados_encontrados["11. Padrões de Previsão Tática"] = analisar_previsao_tatica(st.session_state.current_sequence)
        resultados_encontrados["12. Padrão 3x1"] = detectar_padrao_3x1(st.session_state.current_sequence)
        resultados_encontrados["13. Padrão 3x3"] = detectar_padrao_3x3(st.session_state.current_sequence)

        col_patterns, col_suggestions = st.columns(2)

        with col_patterns:
            st.subheader("📈 Padrões Detectados")
            algum_padrao_detectado = False
            for padrao, resultados in resultados_encontrados.items():
                if resultados:
                    st.success(f"✔️ **{padrao}:**")
                    for res in resultados:
                        st.write(f"- {res}")
                    algum_padrao_detectado = True
            if not algum_padrao_detectado:
                st.info("Nenhum dos padrões definidos foi detectado na sequência fornecida.")

        with col_suggestions:
            st.subheader("🎯 Sugestões de Entradas")
            sugestoes, possibilidades_empate = gerar_sugestoes(st.session_state.current_sequence, resultados_encontrados)

            if sugestoes:
                st.markdown("**Considerando os padrões e tendências:**")
                for s in sugestoes:
                    st.info(f"- {s}")
            else:
                st.info("Não há sugestões claras de entradas com base nos padrões detectados nesta sequência.")

            st.markdown("---")
            st.subheader("🤝 Possibilidade de Empate")
            if possibilidades_empate:
                st.markdown("**Fatores que indicam possibilidade de empate:**")
                for pe in possibilidades_empate:
                    st.warning(f"- {pe}")
            else:
                st.info("Nenhuma tendência forte para 'Empate' detectada nesta sequência.")
        
        st.markdown("---")


st.markdown("---")
st.subheader("📚 Histórico de Análises")

# Botão para zerar o histórico
if st.button("🧹 Zerar Histórico", use_container_width=True):
    st.session_state.history = []
    st.success("Histórico zerado!")
    st.rerun() # Recarrega a página para refletir a limpeza imediatamente

if st.session_state.history:
    for i, entry in enumerate(st.session_state.history):
        formatted_entry = ""
        # Formata a entrada em linhas de 9
        for j in range(0, len(entry), 9):
            formatted_entry += entry[j:j+9] + " "
        st.code(f"Análise {i+1}: {formatted_entry.strip()}")
else:
    st.info("Nenhum histórico de análises ainda.")


st.markdown("---")
st.markdown("Desenvolvido para análise de padrões. Lembre-se: sugestões são baseadas em heurísticas e não garantem resultados.")

