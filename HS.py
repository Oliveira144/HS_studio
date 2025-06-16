
importar streamlit como st
de coleções importar deque, Contador
de itertools importar groupby
importar matemática
tempo de importação

# CONFIGURAÇÕES INICIAIS
st.set_page_config(page_title="Estúdio de Futebol HS", layout="centralizado")
st.title("âš½ Football Studio HS – Analisador Avançado de PadrÃµes")
st.markdown("""
<estilo>
    .element-container botão {
        altura: 60px !importante;
        tamanho da fonte: 22px !importante;
    }
</style>""", unsafe_allow_html=True)

# HISTÓRICO
histórico = st.session_state.get("histórico", deque(maxlen=300))

# INPUT OTIMIZADO
st.subheader("ðŸŽ® Inserir resultado ao vivo:")
col1, col2, col3 = st.columns(3)
if col1.button("ðŸ Casa", key="btn_casa"):
    histórico.append("C")
if col2.button("ðŸ¤ Empate", key="btn_empate"):
    historico.append("E")
if col3.button("ðŸš© Visitante", key="btn_visitante"):
    histórico.append("V")

# HISTÓRICO VISUAL
st.subheader("ðŸ“Š Histórico Visual (linhas de 9)")
linhas = [lista(histórico)[i:i+9] para i em intervalo(0, len(histórico), 9)]
para linha em linhas:
    st.markdown(" ".join(f"[{x}]" para x na linha))

# FUNÃ‡Ã•ES DE ANÃ LISE
def traduz(símbolo):
    return {"C": "Casa", "V": "Visitante", "E": "Empate"}.get(simbolo, simbolo)

def detectar_padroes_complexos(hist):
    padroes = []
    se len(hist) < 4:
        retorno padroes
    texto = "".join(hist)
    verificações = {
        "2x2": "CCVV" em texto ou "VVCC" em texto,
        "3x3": "CCCVVV" no texto ou "VVVCCC" no texto,
        "3x1x3": qualquer(texto[i:i+7] == a*3 + b + a*3 para i no intervalo(len(texto)-6) para a em "CV" para b em "VE" se b != a),
        "2x1x2": qualquer(texto[i:i+5] == a*2 + b + a*2 para i no intervalo(len(texto)-4) para a em "CV" para b em "VE" se b != a),
        "4x4": "CCCCVVVV" no texto ou "VVVVCCCC" no texto,
        "3x1x1x2": qualquer(texto[i:i+7] == a*3 + b + b + a*2 para i no intervalo(len(texto)-6) para a em "CV" para b em "VE" se b != a),
    }
    para nome, cond em checks.items():
        se condição:
            padroes.append(nome)
    retorno padroes

def detectar_padroes_repetidos(hist, janela=5):
    se len(hist) < janela * 2:
        retornar Nenhum, 0
    sequências = [tupla(hist[i:i+janela]) for i in range(len(hist) - janela + 1)]
    contagem = Contador(sequências)
    padrões_repetidos = [seq para seq, contar em contagem.items() se contagem > 1]
    sugestões = []
    para padrao em padroes_repetidos:
        para i em intervalo(len(hist) - janela):
            se tupla(hist[i:i+janela]) == padrao e i+janela < len(hist):
                sugestões.append(hist[i+janela])
    se sugere:
        mais_comum, freq = Contador(sugestões).most_common(1)[0]
        return f"ðŸ” Padrão recorrente: {''.join(padroes_repetidos[0])} â†' Entrada: {traduz(mais_comum)} (Confiabilidade: {freq})", freq
    retornar Nenhum, 0

def chance_empate(hist):
    total = len(hist)
    empates = hist.count("E")
    retornar f"{round((empates/total)*100, 1)}%" se total > 0 senão "0%"

def detectar_tendencia_surf(hist):
    se len(hist) < 2:
        retornar "-"
    atual = hist[-1]
    contagem = 1
    para i no intervalo(len(hist)-2, -1, -1):
        se hist[i] == atual:
            contagem += 1
        outro:
            quebrar
    se contagem >= 3:
        quebra = round((1 - (contagem/10)) * 100)
        return f"âš ï¸ {traduz(atual)} em sequência ({count}x) ➾ Chance de quebra: {quebra}%"
    retornar "-"

def recomendacao(hist):
    se len(hist) == 0:
        return "Aguardando os primeiros resultados..."
    se len(hist) < 3:
        return f"Primeiros dados: Último resultado foi {traduz(hist[-1])}."
    ultimos = lista(hist)[-3:]
    se ultimos.count("C") == 3:
        return "ðŸ“‰ Casa em sequência. Sugestão: Visitante ou Empate."
    se ultimos.count("V") == 3:
        return "ðŸ“‰ Visitante em sequência. Sugestão: Casa ou Empate."
    if últimos[-1] != últimos[-2]:
        return "†”ï¸ Zig-zag ativo. Seguir alternância."
    return "ðŸ” Aguardar padrão mais claro."

# ANÃ LISE COMPLETA
st.subheader("ðŸ“ˆ Análise Inteligente")

padroes = detectar_padroes_complexos(histórico)
se padroes:
    st.success("ðŸ”Ž Padrões detectados: " + ", ".join(padroes))
outro:
    st.info("Nenhum padrão complexo identificado.")

sugestao_pelo_retorno, confianca = detectar_padroes_repetidos(histórico)
se sugestao_pelo_retorno:
    se confianca >= 3:
        st.warning(sugestao_pelo_retorno)
    outro:
        st.info(sugestao_pelo_retorno)

surf_status = detectar_tendencia_surf(histórico)
se surf_status != "-":
    st.warning(status_de_surf)

st.markdown(f"ðŸ”„ Chance de empate: {chance_empate(historico)}")
st.markdown(f"ðŸ§ Recomendação com base nos últimos resultados: {recomendacao(historico)}")

# SALVAR HISTÓRICO
st.session_state["histórico"] = histórico
