import streamlit as st
import pandas as pd
import collections

# --- Constantes e Funções Auxiliares ---
NUM_RECENT_RESULTS_FOR_ANALYSIS = 27
MAX_HISTORY_TO_STORE = 1000
NUM_HISTORY_TO_DISPLAY = 100 # Número de resultados do histórico a serem exibidos
EMOJIS_PER_ROW = 9 # Quantos emojis por linha no histórico horizontal
MIN_RESULTS_FOR_SUGGESTION = 9

def get_color(result):
    """Retorna a cor associada ao resultado."""
    if result == 'home':
        return 'red'
    elif result == 'away':
        return 'blue'
    else: # 'draw'
        return 'yellow'

def get_color_emoji(color):
    """Retorna o emoji correspondente à cor."""
    if color == 'red':
        return '🔴'
    elif color == 'blue':
        return '🔵'
    elif color == 'yellow':
        return '🟡'
    return ''

def get_result_emoji(result_type):
    """Retorna o emoji correspondente ao tipo de resultado. Agora retorna uma string vazia para remover os ícones."""
    return ''

# --- Funções de Análise ---

def analyze_surf(results):
    """
    Analisa os padrões de "surf" (sequências de Home/Away/Draw)
    nos últimos N resultados para 'current' e no histórico completo para 'max'.
    """
    relevant_results = results[:NUM_RECENT_RESULTS_FOR_ANALYSIS]
    
    current_home_sequence = 0
    current_away_sequence = 0
    current_draw_sequence = 0
    
    if relevant_results:
        # A sequência atual é sempre do resultado mais recente (results[0])
        first_result_current_analysis = relevant_results[0]
        for r in relevant_results:
            if r == first_result_current_analysis:
                if first_result_current_analysis == 'home': 
                    current_home_sequence += 1
                elif first_result_current_analysis == 'away': 
                    current_away_sequence += 1
                else: # draw
                    current_draw_sequence += 1
            else:
                break
    
    # Calcular sequências máximas em todo o histórico disponível para maior precisão
    max_home_sequence = 0
    max_away_sequence = 0
    max_draw_sequence = 0
    
    temp_home_seq = 0
    temp_away_seq = 0
    temp_draw_seq = 0

    for res in results: # Percorre TODOS os resultados (histórico completo) para o máximo
        if res == 'home':
            temp_home_seq += 1
            temp_away_seq = 0
            temp_draw_seq = 0
        elif res == 'away':
            temp_away_seq += 1
            temp_home_seq = 0
            temp_draw_seq = 0
        else: # draw
            temp_draw_seq += 1
            temp_home_seq = 0
            temp_away_seq = 0
            
        max_home_sequence = max(max_home_sequence, temp_home_seq)
        max_away_sequence = max(max_away_sequence, temp_away_seq)
        max_draw_sequence = max(max_draw_sequence, temp_draw_seq)

    return {
        'home_sequence': current_home_sequence,
        'away_sequence': current_away_sequence,
        'draw_sequence': current_draw_sequence,
        'max_home_sequence': max_home_sequence,
        'max_away_sequence': max_away_sequence,
        'max_draw_sequence': max_draw_sequence
    }

def analyze_colors(results):
    """Analisa a contagem e as sequências de cores nos últimos N resultados."""
    relevant_results = results[:NUM_RECENT_RESULTS_FOR_ANALYSIS]
    if not relevant_results:
        return {'red': 0, 'blue': 0, 'yellow': 0, 'current_color': '', 'streak': 0, 'color_pattern_27': ''}

    color_counts = {'red': 0, 'blue': 0, 'yellow': 0}

    for result in relevant_results:
        color = get_color(result)
        color_counts[color] += 1

    current_color = get_color(results[0]) if results else ''
    streak = 0
    for result in results: # Streak é sempre do resultado mais recente no histórico completo
        if get_color(result) == current_color:
            streak += 1
        else:
            break
            
    color_pattern_27 = ''.join([get_color(r)[0].upper() for r in relevant_results])

    return {
        'red': color_counts['red'],
        'blue': color_counts['blue'],
        'yellow': color_counts['yellow'],
        'current_color': current_color,
        'streak': streak,
        'color_pattern_27': color_pattern_27
    }

def find_complex_patterns(results):
    """
    Identifica padrões de quebra e padrões específicos (2x2, 3x3, 3x1, 2x1, etc.)
    nos últimos N resultados, incluindo os novos padrões.
    Os nomes dos padrões agora são concisos, sem exemplos ou emojis.
    """
    patterns = collections.defaultdict(int)
    relevant_results = results[:NUM_RECENT_RESULTS_FOR_ANALYSIS]

    # Converte resultados para cores para facilitar a análise de padrões
    colors = [get_color(r) for r in relevant_results]

    for i in range(len(colors) - 1):
        color1 = colors[i]
        color2 = colors[i+1]

        # 1. Quebra Simples
        if color1 != color2:
            patterns[f"Quebra Simples ({color1.capitalize()} para {color2.capitalize()})"] += 1

        # Verificar padrões que envolvem 3 ou mais resultados
        if i < len(colors) - 2:
            color3 = colors[i+2]
            
            # 2. Padrões 2x1 (Ex: R R B)
            if color1 == color2 and color1 != color3:
                patterns[f"2x1 ({color1.capitalize()} para {color3.capitalize()})"] += 1
            
            # 3. Zig-Zag / Padrão Alternado (Ex: R B R)
            if color1 != color2 and color2 != color3 and color1 == color3:
                patterns[f"Zig-Zag / Alternado ({color1.capitalize()}-{color2.capitalize()}-{color3.capitalize()})"] += 1

            # 4. Alternância com Empate no Meio (X Draw Y - Ex: R Y B)
            if color2 == 'yellow' and color1 != 'yellow' and color3 != 'yellow' and color1 != color3:
                patterns[f"Alternância c/ Empate no Meio ({color1.capitalize()}-Empate-{color3.capitalize()})"] += 1

            # 5. Padrão Onda 1-2-1 (Ex: R B B R) - variação de espelho ou zig-zag
            if i < len(colors) - 3:
                color4 = colors[i+3]
                if color1 != color2 and color2 == color3 and color3 != color4 and color1 == color4:
                    patterns[f"Padrão Onda 1-2-1 ({color1.capitalize()}-{color2.capitalize()}-{color3.capitalize()}-{color4.capitalize()})"] += 1

        if i < len(colors) - 3:
            color3 = colors[i+2]
            color4 = colors[i+3]

            # 6. Padrões 3x1 (Ex: R R R B)
            if color1 == color2 and color2 == color3 and color1 != color4:
                patterns[f"3x1 ({color1.capitalize()} para {color4.capitalize()})"] += 1
            
            # 7. Padrões 2x2 (Ex: R R B B)
            if color1 == color2 and color3 == color4 and color1 != color3:
                patterns[f"2x2 ({color1.capitalize()} para {color3.capitalize()})"] += 1
            
            # 8. Padrão de Espelho (Ex: R B B R)
            if color1 != color2 and color2 == color3 and color1 == color4:
                patterns[f"Padrão Espelho ({color1.capitalize()}-{color2.capitalize()}-{color3.capitalize()}-{color4.capitalize()})"] += 1

        if i < len(colors) - 5:
            color3 = colors[i+2]
            color4 = colors[i+3]
            color5 = colors[i+4]
            color6 = colors[i+5]

            # 9. Padrões 3x3 (Ex: R R R B B B)
            if color1 == color2 and color2 == color3 and color4 == color5 and color5 == color6 and color1 != color4:
                patterns[f"3x3 ({color1.capitalize()} para {color4.capitalize()})"] += 1

    # 10. Duplas Repetidas (Ex: R R, B B, Y Y) - Contagem de ocorrências de duplas
    for i in range(len(colors) - 1):
        if colors[i] == colors[i+1]:
            patterns[f"Dupla Repetida ({colors[i].capitalize()})"] += 1
            
    # Padrão de Reversão / Alternância de Blocos (Ex: RR BB RR BB)
    block_pattern_keys = []
    if len(colors) >= 4:
        for block_size in [2, 3]: # Tamanhos de bloco comuns
            if len(colors) >= 2 * block_size:
                block1_colors = colors[:block_size]
                block2_colors = colors[block_size : 2 * block_size]
                
                if all(c == block1_colors[0] for c in block1_colors) and \
                   all(c == block2_colors[0] for c in block2_colors) and \
                   block1_colors[0] != block2_colors[0]:
                    
                    if len(colors) >= 4 * block_size:
                        block3_colors = colors[2 * block_size : 3 * block_size]
                        block4_colors = colors[3 * block_size : 4 * block_size]
                        if all(c == block3_colors[0] for c in block3_colors) and \
                           all(c == block4_colors[0] for c in block4_colors) and \
                           block1_colors[0] == block3_colors[0] and \
                           block2_colors[0] == block4_colors[0]:
                                block_pattern_keys.append(f"Padrão Reversão/Bloco Alternado {block_size}x{block_size} ({block1_colors[0].capitalize()} {block2_colors[0].capitalize()})")
                    else:
                            block_pattern_keys.append(f"Padrão Reversão/Bloco {block_size}x{block_size} ({block1_colors[0].capitalize()} {block2_colors[0].capitalize()})")
    
    for key in block_pattern_keys:
        patterns[key] += 1


    return dict(patterns)

def analyze_break_probability(results):
    """Analisa a probabilidade de quebra com base no histórico dos últimos N resultados."""
    relevant_results = results[:NUM_RECENT_RESULTS_FOR_ANALYSIS]
    if not relevant_results or len(relevant_results) < 2:
        return {'break_chance': 0, 'last_break_type': ''}
    
    breaks = 0
    total_sequences_considered = 0
    
    for i in range(len(relevant_results) - 1):
        if get_color(relevant_results[i]) != get_color(relevant_results[i+1]):
            breaks += 1
        total_sequences_considered += 1
            
    break_chance = (breaks / total_sequences_considered) * 100 if total_sequences_considered > 0 else 0

    last_break_type = ""
    if len(results) >= 2 and get_color(results[0]) != get_color(results[1]):
        last_break_type = f"Quebrou de {get_color(results[1]).capitalize()} para {get_color(results[0]).capitalize()}"
    
    return {
        'break_chance': round(break_chance, 2),
        'last_break_type': last_break_type
    }

def analyze_draw_specifics(results):
    """Análise específica para empates nos últimos N resultados e padrões de recorrência."""
    relevant_results = results[:NUM_RECENT_RESULTS_FOR_ANALYSIS]
    if not relevant_results:
        return {'draw_frequency_27': 0, 'time_since_last_draw': -1, 'draw_patterns': {}, 'recurrent_draw': False}

    draw_count_27 = relevant_results.count('draw')
    draw_frequency_27 = (draw_count_27 / len(relevant_results)) * 100 if len(relevant_results) > 0 else 0

    time_since_last_draw = -1
    for i, result in enumerate(results): # Tempo desde o último empate no histórico COMPLETO
        if result == 'draw':
            time_since_last_draw = i
            break
    
    draw_patterns_found = collections.defaultdict(int)
    for i in range(len(relevant_results) - 1):
        color1 = get_color(relevant_results[i])
        color2 = get_color(relevant_results[i+1])

        if color2 == 'yellow' and color1 != 'yellow':
            draw_patterns_found[f"Quebra para Empate ({color1.capitalize()} para Empate)"] += 1
        
        if i < len(relevant_results) - 2:
            color3 = get_color(relevant_results[i+2])
            if color3 == 'yellow':
                if color1 == 'red' and color2 == 'blue':
                    draw_patterns_found["Red-Blue-Draw"] += 1
                elif color1 == 'blue' and color2 == 'red':
                    draw_patterns_found["Blue-Red-Draw"] += 1

    # Detecção de Empate Recorrente (intervalos curtos)
    draw_indices = [i for i, r in enumerate(relevant_results) if r == 'draw']
    recurrent_draw = False
    if len(draw_indices) >= 2:
        for i in range(len(draw_indices) - 1):
            interval = draw_indices[i] - draw_indices[i+1] -1
            if 0 <= interval <= 3: # Empates em até 3 rodadas de distância
                recurrent_draw = True
                break

    return {
        'draw_frequency_27': round(draw_frequency_27, 2),
        'time_since_last_draw': time_since_last_draw,
        'draw_patterns': dict(draw_patterns_found),
        'recurrent_draw': recurrent_draw
    }

def generate_advanced_suggestion(results, surf_analysis, color_analysis, break_patterns, break_probability, draw_specifics):
    """
    Gera uma sugestão de aposta baseada em múltiplas análises usando um sistema de pontuação,
    com foco em segurança e incorporando os novos padrões.
    Prioriza sugestões mais fortes e evita conflitos.
    """
    if not results or len(results) < MIN_RESULTS_FOR_SUGGESTION: 
        return {'suggestion': f'Aguardando no mínimo {MIN_RESULTS_FOR_SUGGESTION} resultados para análise detalhada.', 'confidence': 0, 'reason': '', 'guarantee_pattern': 'N/A', 'bet_type': 'none'}

    last_result = results[0]
    last_result_color = get_color(last_result)
    current_streak = color_analysis['streak']
    
    bet_scores = {'home': 0, 'away': 0, 'draw': 0}
    reasons = collections.defaultdict(list)
    guarantees = collections.defaultdict(list)

    # --- Nível 1: Sugestões de Alta Confiança (Pontuação 100+) ---

    # 1. Quebra de Sequência Longa (Surf Max)
    # Se a sequência atual já atingiu ou superou o máximo histórico, há grande chance de quebra.
    if last_result_color == 'red' and surf_analysis['max_home_sequence'] > 0 and current_streak >= surf_analysis['max_home_sequence'] and current_streak >= 3:
        bet_scores['away'] += 150 # Pontuação mais alta
        reasons['away'].append(f"Sequência atual de Vermelho ({current_streak}x) atingiu ou superou o máximo histórico de surf ({surf_analysis['max_home_sequence']}x). Alta probabilidade de quebra para Azul.")
        guarantees['away'].append(f"Surf Max Quebra: {last_result_color.capitalize()}")
    elif last_result_color == 'blue' and surf_analysis['max_away_sequence'] > 0 and current_streak >= surf_analysis['max_away_sequence'] and current_streak >= 3:
        bet_scores['home'] += 150
        reasons['home'].append(f"Sequência atual de Azul ({current_streak}x) atingiu ou superou o máximo histórico de surf ({surf_analysis['max_away_sequence']}x). Alta probabilidade de quebra para Vermelho.")
        guarantees['home'].append(f"Surf Max Quebra: {last_result_color.capitalize()}")
    elif last_result_color == 'yellow' and surf_analysis['max_draw_sequence'] > 0 and current_streak >= surf_analysis['max_draw_sequence'] and current_streak >= 2:
        # Se empate atingiu o máximo, pode quebrar para qualquer lado.
        bet_scores['home'] += 100 
        bet_scores['away'] += 100
        reasons['home'].append(f"Sequência atual de Empate ({current_streak}x) atingiu ou superou o máximo histórico.")
        reasons['away'].append(f"Sequência atual de Empate ({current_streak}x) atingiu ou superou o máximo histórico.")
        guarantees['home'].append(f"Surf Max Quebra: Empate")
        guarantees['away'].append(f"Surf Max Quebra: Empate")

    # --- Nível 2: Padrões Recorrentes e Fortes (Pontuação 70-110) ---

    # 2. Padrões 2x1 e 3x1 altamente recorrentes (Indica quebra)
    for pattern, count in break_patterns.items():
        if count >= 3: # Múltiplas ocorrências do padrão
            # 2x1 patterns
            if "2x1 (Red para Blue)" in pattern and last_result_color == 'red' and current_streak == 2:
                bet_scores['away'] += 110
                reasons['away'].append(f"Padrão '{pattern.split('(')[0].strip()}' altamente recorrente ({count}x).")
                guarantees['away'].append(pattern)
            elif "2x1 (Blue para Red)" in pattern and last_result_color == 'blue' and current_streak == 2:
                bet_scores['home'] += 110
                reasons['home'].append(f"Padrão '{pattern.split('(')[0].strip()}' altamente recorrente ({count}x).")
                guarantees['home'].append(pattern)
            
            # 3x1 patterns
            elif "3x1 (Red para Blue)" in pattern and last_result_color == 'red' and current_streak == 3:
                bet_scores['away'] += 120
                reasons['away'].append(f"Padrão '{pattern.split('(')[0].strip()}' altamente recorrente ({count}x).")
                guarantees['away'].append(pattern)
            elif "3x1 (Blue para Red)" in pattern and last_result_color == 'blue' and current_streak == 3:
                bet_scores['home'] += 120
                reasons['home'].append(f"Padrão '{pattern.split('(')[0].strip()}' altamente recorrente ({count}x).")
                guarantees['home'].append(pattern)
            
            # 2x2 patterns
            elif "2x2 (Red para Blue)" in pattern and len(results) >= 2 and get_color(results[0]) == 'red' and get_color(results[1]) == 'red':
                bet_scores['away'] += 100 
                reasons['away'].append(f"Padrão '{pattern.split('(')[0].strip()}' recorrente ({count}x).")
                guarantees['away'].append(pattern)
            elif "2x2 (Blue para Red)" in pattern and len(results) >= 2 and get_color(results[0]) == 'blue' and get_color(results[1]) == 'blue':
                bet_scores['home'] += 100
                reasons['home'].append(f"Padrão '{pattern.split('(')[0].strip()}' recorrente ({count}x).")
                guarantees['home'].append(pattern)

            # 3x3 patterns (similar to 2x2, but stronger due to length)
            elif "3x3 (Red para Blue)" in pattern and len(results) >= 3 and get_color(results[0]) == 'red' and get_color(results[1]) == 'red' and get_color(results[2]) == 'red':
                bet_scores['away'] += 130 
                reasons['away'].append(f"Padrão '{pattern.split('(')[0].strip()}' altamente recorrente ({count}x).")
                guarantees['away'].append(pattern)
            elif "3x3 (Blue para Red)" in pattern and len(results) >= 3 and get_color(results[0]) == 'blue' and get_color(results[1]) == 'blue' and get_color(results[2]) == 'blue':
                bet_scores['home'] += 130
                reasons['home'].append(f"Padrão '{pattern.split('(')[0].strip()}' altamente recorrente ({count}x).")
                guarantees['home'].append(pattern)

            # Padrão Reversão/Bloco Alternado
            if "Padrão Reversão/Bloco Alternado" in pattern:
                # Extrai as cores envolvidas no padrão
                pattern_info_str = pattern.split('(')[1].replace(')', '').strip()
                # Ex: "Red Blue" -> ['Red', 'Blue']
                # Ajuste para garantir que estamos pegando as cores corretamente, ignorando emojis se houver
                pattern_colors_raw = pattern_info_str.split(' ')
                first_block_color = pattern_colors_raw[0].lower() # Ex: 'Red' -> 'red'
                second_block_color = pattern_colors_raw[1].lower() # Ex: 'Blue' -> 'blue'
                
                if len(results) >= 2:
                    current_block_color = get_color(results[0])
                    prev_block_color = get_color(results[1])
                    
                    if current_block_color == prev_block_color: # Se a sequência atual ainda é do mesmo bloco
                        if current_block_color == first_block_color and second_block_color != 'yellow':
                            if second_block_color == 'blue': # CORREÇÃO AQUI
                                bet_scores['away'] += 115 
                                reasons['away'].append(f"Padrão '{pattern.split('(')[0].strip()}' altamente recorrente ({count}x). Espera-se a reversão para {second_block_color.capitalize()}.")
                                guarantees['away'].append(pattern)
                            elif second_block_color == 'red': # CORREÇÃO AQUI
                                bet_scores['home'] += 115 
                                reasons['home'].append(f"Padrão '{pattern.split('(')[0].strip()}' altamente recorrente ({count}x). Espera-se a reversão para {second_block_color.capitalize()}.")
                                guarantees['home'].append(pattern)
                        elif current_block_color == second_block_color and first_block_color != 'yellow':
                            if first_block_color == 'blue': # CORREÇÃO AQUI
                                bet_scores['away'] += 115 
                                reasons['away'].append(f"Padrão '{pattern.split('(')[0].strip()}' altamente recorrente ({count}x). Espera-se a reversão para {first_block_color.capitalize()}.")
                                guarantees['away'].append(pattern)
                            elif first_block_color == 'red': # CORREÇÃO AQUI
                                bet_scores['home'] += 115 
                                reasons['home'].append(f"Padrão '{pattern.split('(')[0].strip()}' altamente recorrente ({count}x). Espera-se a reversão para {first_block_color.capitalize()}.")
                                guarantees['home'].append(pattern)

    # 3. Sugestão de Empate (se atrasado OU recorrente)
    # Empate Atrasado: Mais de 7 rodadas sem empate E baixa frequência
    if draw_specifics['time_since_last_draw'] >= 7 and draw_specifics['draw_frequency_27'] < 15: # Frequência ajustada para 15%
        bet_scores['draw'] += 80
        reasons['draw'].append(f"Empate não ocorre há {draw_specifics['time_since_last_draw']} rodadas e frequência baixa ({draw_specifics['draw_frequency_27']}% nos últimos 27).")
        guarantees['draw'].append("Empate Atrasado/Baixa Frequência")
    
    # Padrões específicos de empate (Ex: R B Y ou B R Y)
    if len(results) >= 2:
        if get_color(results[0]) == 'away' and get_color(results[1]) == 'home': # Situação atual é Home (R) -> Away (B)
            if "Red-Blue-Draw" in draw_specifics['draw_patterns']:
                bet_scores['draw'] += 95
                reasons['draw'].append(f"Padrão 'Red-Blue-Draw' detectado e recorrente ({draw_specifics['draw_patterns']['Red-Blue-Draw']}x).")
                guarantees['draw'].append("Padrão Red-Blue-Draw")
        elif get_color(results[0]) == 'home' and get_color(results[1]) == 'away': # Situação atual é Away (B) -> Home (R)
            if "Blue-Red-Draw" in draw_specifics['draw_patterns']:
                bet_scores['draw'] += 95
                reasons['draw'].append(f"Padrão 'Blue-Red-Draw' detectado e recorrente ({draw_specifics['draw_patterns']['Blue-Red-Draw']}x).")
                guarantees['draw'].append("Padrão Blue-Red-Draw")

    # 4. Empate Recorrente (intervalos curtos)
    if draw_specifics['recurrent_draw'] and draw_specifics['time_since_last_draw'] >= 0 and draw_specifics['time_since_last_draw'] <= 3: 
        bet_scores['draw'] += 85 # Um pouco mais de confiança
        reasons['draw'].append(f"Empate é recorrente, ocorrendo em intervalos curtos (último há {draw_specifics['time_since_last_draw']} rodadas).")
        guarantees['draw'].append("Empate Recorrente")

    # 5. Zig-Zag / Padrões Alternados
    for pattern, count in break_patterns.items():
        if count >=
