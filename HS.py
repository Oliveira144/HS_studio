import streamlit as st
from collections import Counter

st.set_page_config(page_title="Analisador de Padrões e Sugestões", layout="wide")

st.title("🔎 Analisador de Padrões e Sugestões")
st.markdown("---")

st.header("📋 Lista de padrões que o sistema vai analisar e notificar:")

st.markdown("""
1.  **Sequência (Surf de Cor)** – 3+ vezes a mesma cor seguida
2.  **Zig-Zag** – alternância de cores (ex: Casa, Visitante, Casa, Visitante...)
3.  **Quebra de Surf** – sequência que é interrompida
4.  **Quebra de Zig-Zag** – padrão alternado que quebra
5.  **Duplas repetidas** – Casa, Casa, Visitante, Visitante...
6.  **Empate recorrente** – Empates aparecendo em intervalos curtos
7.  **Padrão Escada** – 1 Casa, 2 Visitantes, 3 Casas... (Adaptar para cores/resultados)
8.  **Espelho** – Ex: Casa, Visitante, Visitante, Casa
9.  **Alternância com empate no meio** – Casa, Empate, Visitante (Adaptar para cores/resultados)
10. **Padrão "onda"** – Ex: 1-2-1-2 de cores (Adaptar para 1 ou 2 sequências de resultados)
11. **Padrões com base nos últimos 5/7/10 jogos** – para previsão tática
12. **Padrão 3x1** – Três ocorrências de um tipo, seguida por uma de outro.
13. **Padrão 3x3** – Três ocorrências de um tipo, seguida por três de outro.
""")

st.markdown("---")

# Inicializa o histórico na sessão se ainda não existir
if 'history' not in st.session_state:
    st.session_state.history = []

# --- Entrada de Dados ---
st.subheader("Dados para Análise")
st.info("Insira a sequência de resultados/cores separados por vírgula. Ex: Casa,Visitante,Empate,Casa,Casa")
st.warning("Para o propósito deste exemplo, usaremos 'C', 'V', 'E' para Casa, Visitante, Empate ou 'A', 'B', 'C' para cores.")

# Campo de texto para entrada da sequência
input_sequence_str = st.text_area("Digite a sequência de resultados/cores:", height=100,
                                  placeholder="Ex: C,V,C,V,E,C,C")

# Processar a entrada
sequence_list = [item.strip().upper() for item in input_sequence_str.split(',') if item.strip()]

st.markdown("---")

# --- Funções de Detecção de Padrões (mantidas as mesmas do código anterior) ---
# (As funções de detecção de padrões são as mesmas para evitar repetição massiva de código.
#  Você pode copiar e colar as funções 'detectar_sequencia_surf', 'detectar_zig_zag',
#  'detectar_quebra_surf', 'detectar_quebra_zig_zag', 'detectar_duplas_repetidas',
#  'detectar_empate_recorrente', 'detectar_padrao_escada', 'detectar_espelho',
#  'detectar_alternancia_empate_meio', 'detectar_padrao_onda',
#  'analisar_previsao_tatica', 'detectar_padrao_3x1', 'detectar_padrao_3x3' aqui)

# --- Funções de Detecção de Padrões (copie e cole as mesmas aqui) ---
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
            # Procura por A,B,A,B...
            while j < len(seq) - 1 and seq[j] == seq[i] and seq[j+1] == seq[i+1]:
                j += 2
            if j - i >= 4: # Pelo menos 2 alternâncias completas (A,B,A,B)
                padroes_encontrados.append(f"Padrão Zig-Zag detectado: {seq[i:j]} iniciando na posição {i+1}.")
            i = j # Move o índice para depois do zig-zag detectado ou um passo à frente
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
    return padroes_encontrados

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
        # Se houve um surf, a sugestão é continuar o surf
        for res in resultados_encontrados["1. Sequência (Surf de Cor)"]:
            if f"'{ultima_ocorrencia}'" in res: # Se o último elemento faz parte de um surf
                sugestoes.append(f"Continuar o 'Surf de Cor' de '{ultima_ocorrencia}'.")

    if resultados_encontrados.get("2. Zig-Zag"):
        # Se houve um Zig-Zag, a sugestão é continuar a alternância
        for res in resultados_encontrados["2. Zig-Zag"]:
            if ultima_ocorrencia and penultima_ocorrencia and f"{penultima_ocorrencia},{ultima_ocorrencia}" in res:
                sugestoes.append(f"Continuar o 'Zig-Zag' com '{penultima_ocorrencia}'.")

    if resultados_encontrados.get("3. Quebra de Surf"):
        for res in resultados_encontrados["3. Quebra de Surf"]:
            # Se um surf foi quebrado, sugere a continuidade da quebra ou o retorno ao surf
            # Isso é mais ambíguo e pode depender de estratégias.
            sugestoes.append(f"Padrão 'Quebra de Surf' recente. Atenção à mudança de tendência.")

    if resultados_encontrados.get("4. Quebra de Zig-Zag"):
        for res in resultados_encontrados["4. Quebra de Zig-Zag"]:
            sugestoes.append(f"Padrão 'Quebra de Zig-Zag' recente. Atenção à mudança de alternância.")

    if resultados_encontrados.get("5. Duplas repetidas"):
        for res in resultados_encontrados["5. Duplas repetidas"]:
            if ultima_ocorrencia and penultima_ocorrencia and ultima_ocorrencia == penultima_ocorrencia:
                 sugestoes.append(f"Considerar quebras após 'Duplas Repetidas' de '{ultima_ocorrencia}'.")

    if resultados_encontrados.get("6. Empate recorrente"):
        for res in resultados_encontrados["6. Empate recorrente"]:
            # Se há empate recorrente, aumenta a possibilidade de novo empate
            possibilidades_empate.append(f"Alta possibilidade de 'Empate' devido à recorrência.")
            sugestoes.append("Possibilidade de Empate (Recorrência).")

    if resultados_encontrados.get("8. Espelho"):
        for res in resultados_encontrados["8. Espelho"]:
            # Se um espelho foi detectado, pode sugerir a continuidade ou inversão
            sugestoes.append(f"Padrão 'Espelho' detectado. Próximo pode inverter ou ser similar ao início.")

    if resultados_encontrados.get("9. Alternância com empate no meio"):
        for res in resultados_encontrados["9. Alternância com empate no meio"]:
            possibilidades_empate.append(f"Possibilidade de 'Empate' como meio de alternância.")
            sugestoes.append("Possibilidade de Empate (Alternância).")

    if resultados_encontrados.get("10. Padrão 'onda'"):
        for res in resultados_encontrados["10. Padrão 'onda'"]:
            if ultima_ocorrencia and penultima_ocorrencia and ultima_ocorrencia != penultima_ocorrencia:
                sugestoes.append(f"Continuar o 'Padrão Onda' com '{penultima_ocorrencia}'.")


    # Sugestões gerais sobre Empate
    empate_count = sequence_list.count('E') # Considerando 'E' como empate
    if sequence_list:
        if empate_count > len(sequence_list) / 3: # Mais de 33% de empates
            possibilidades_empate.append("A alta frequência de empates sugere maior probabilidade de novo 'Empate'.")
        elif empate_count == 0 and len(sequence_list) > 5:
            possibilidades_empate.append("Ausência prolongada de empates pode indicar um 'Empate' em breve (lei das médias).")


    return sugestoes, possibilidades_empate

# --- Executar Análise ---
st.subheader("Padrões Detectados")

if st.button("Analisar Sequência e Gerar Sugestões"):
    if not sequence_list:
        st.warning("Por favor, digite uma sequência para analisar.")
    else:
        # Adiciona a sequência atual ao histórico
        st.session_state.history.append("".join(sequence_list))

        st.write(f"Sequência para análise: **{', '.join(sequence_list)}**")
        st.markdown("---")

        resultados_encontrados = {}
        resultados_encontrados["1. Sequência (Surf de Cor)"] = detectar_sequencia_surf(sequence_list)
        resultados_encontrados["2. Zig-Zag"] = detectar_zig_zag(sequence_list)
        resultados_encontrados["3. Quebra de Surf"] = detectar_quebra_surf(sequence_list)
        resultados_encontrados["4. Quebra de Zig-Zag"] = detectar_quebra_zig_zag(sequence_list)
        resultados_encontrados["5. Duplas repetidas"] = detectar_duplas_repetidas(sequence_list)
        resultados_encontrados["6. Empate recorrente"] = detectar_empate_recorrente(sequence_list)
        resultados_encontrados["7. Padrão Escada"] = detectar_padrao_escada(sequence_list)
        resultados_encontrados["8. Espelho"] = detectar_espelho(sequence_list)
        resultados_encontrados["9. Alternância com empate no meio"] = detectar_alternancia_empate_meio(sequence_list)
        resultados_encontrados["10. Padrão 'onda'"] = detectar_padrao_onda(sequence_list)
        resultados_encontrados["11. Padrões de Previsão Tática"] = analisar_previsao_tatica(sequence_list)
        resultados_encontrados["12. Padrão 3x1"] = detectar_padrao_3x1(sequence_list)
        resultados_encontrados["13. Padrão 3x3"] = detectar_padrao_3x3(sequence_list)

        algum_padrao_detectado = False
        for padrao, resultados in resultados_encontrados.items():
            if resultados:
                st.success(f"✔️ **{padrao}:**")
                for res in resultados:
                    st.write(f"- {res}")
                algum_padrao_detectado = True

        if not algum_padrao_detectado:
            st.info("Nenhum dos padrões definidos foi detectado na sequência fornecida.")

        st.markdown("---")
        st.subheader("🎯 Sugestões de Entradas e Possibilidade de Empate")
        sugestoes, possibilidades_empate = gerar_sugestoes(sequence_list, resultados_encontrados)

        if sugestoes:
            st.write("Baseado nos padrões e tendências:")
            for s in sugestoes:
                st.info(f"- {s}")
        else:
            st.info("Não há sugestões claras de entradas com base nos padrões detectados nesta sequência.")

        if possibilidades_empate:
            st.write("Considerações sobre a possibilidade de Empate:")
            for pe in possibilidades_empate:
                st.warning(f"- {pe}")
        else:
            st.info("Nenhuma tendência forte para 'Empate' detectada nesta sequência.")


st.markdown("---")
st.subheader("📚 Histórico de Resultados")

# Botão para zerar o histórico
if st.button("🧹 Zerar Histórico"):
    st.session_state.history = []
    st.success("Histórico zerado!")

if st.session_state.history:
    for i, entry in enumerate(st.session_state.history):
        formatted_entry = ""
        # Formata a entrada em linhas de 9
        for j in range(0, len(entry), 9):
            formatted_entry += entry[j:j+9] + "\n"
        st.code(f"Análise {i+1}:\n{formatted_entry.strip()}")
else:
    st.info("Nenhum histórico de análises ainda.")


st.markdown("---")
st.markdown("Desenvolvido para análise de padrões. Lembre-se: sugestões são baseadas em heurísticas e não garantem resultados.")

