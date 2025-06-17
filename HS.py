import streamlit as st
from collections import Counter
from dataclasses import dataclass
from typing import List, Dict, Tuple
import plotly.express as px
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Analisador de Padrões Avançado", 
    layout="wide", 
    initial_sidebar_state="expanded",
    page_icon="🎯"
)

@dataclass
class PatternResult:
    """Classe para estruturar resultados de padrões"""
    pattern_type: str
    description: str
    position: int
    confidence: float = 0.0
    
@dataclass
class AnalysisResult:
    """Classe para estruturar resultados da análise"""
    patterns: List[PatternResult]
    suggestions: List[str]
    empate_possibilities: List[str]
    statistics: Dict[str, float]

class PatternAnalyzer:
    """Classe principal para análise de padrões"""
    
    def __init__(self):
        self.empate_char = 'E'
        self.pattern_functions = {
            "Sequência (Surf)": self._detect_surf_sequence,
            "Zig-Zag": self._detect_zig_zag,
            "Quebra de Surf": self._detect_surf_break,
            "Quebra de Zig-Zag": self._detect_zigzag_break,
            "Duplas Repetidas": self._detect_repeated_pairs,
            "Empate Recorrente": self._detect_recurring_draw,
            "Padrão Escada": self._detect_ladder_pattern,
            "Espelho": self._detect_mirror_pattern,
            "Alternância com Empate": self._detect_alternation_with_draw,
            "Padrão Onda": self._detect_wave_pattern,
            "Padrão 3x1": self._detect_3x1_pattern,
            "Padrão 3x3": self._detect_3x3_pattern
        }
    
    def analyze_sequence(self, sequence: List[str]) -> AnalysisResult:
        """Análise completa da sequência"""
        if not sequence:
            return AnalysisResult([], [], [], {})
        
        patterns = []
        
        # Executa todas as análises de padrões
        for pattern_name, pattern_func in self.pattern_functions.items():
            try:
                pattern_results = pattern_func(sequence)
                for result in pattern_results:
                    patterns.append(PatternResult(
                        pattern_type=pattern_name,
                        description=result,
                        position=0,  # Será ajustado em cada função se necessário
                        confidence=self._calculate_confidence(pattern_name, sequence)
                    ))
            except Exception as e:
                st.error(f"Erro ao analisar padrão {pattern_name}: {str(e)}")
        
        # Análise tática (últimos jogos)
        tactical_patterns = self._analyze_tactical_prediction(sequence)
        for result in tactical_patterns:
            patterns.append(PatternResult(
                pattern_type="Análise Tática",
                description=result,
                position=0,
                confidence=0.7
            ))
        
        # Gera sugestões e possibilidades de empate
        suggestions = self._generate_suggestions(sequence, patterns)
        empate_possibilities = self._analyze_draw_possibilities(sequence, patterns)
        
        # Calcula estatísticas
        statistics = self._calculate_statistics(sequence)
        
        return AnalysisResult(patterns, suggestions, empate_possibilities, statistics)
    
    def _calculate_confidence(self, pattern_name: str, sequence: List[str]) -> float:
        """Calcula confiança baseada no tamanho da sequência e tipo do padrão"""
        confidence_map = {
            "Sequência (Surf)": 0.8,
            "Zig-Zag": 0.7,
            "Empate Recorrente": 0.9,
            "Espelho": 0.6,
            "Padrão 3x3": 0.85
        }
        
        base_confidence = confidence_map.get(pattern_name, 0.5)
        length_factor = min(len(sequence) / 10, 1.0)  # Máximo 1.0
        
        return min(base_confidence * (0.5 + length_factor * 0.5), 1.0)
    
    def _detect_surf_sequence(self, seq: List[str]) -> List[str]:
        """Detecta sequências de 3+ mesma cor"""
        patterns = []
        if len(seq) < 3:
            return patterns
            
        i = 0
        while i < len(seq) - 2:
            if seq[i] == seq[i+1] == seq[i+2]:
                j = i + 3
                while j < len(seq) and seq[j] == seq[i]:
                    j += 1
                patterns.append(
                    f"Surf de '{seq[i]}' por {j-i} posições (pos. {i+1}-{j})"
                )
                i = j
            else:
                i += 1
        return patterns
    
    def _detect_zig_zag(self, seq: List[str]) -> List[str]:
        """Detecta padrões de alternância"""
        patterns = []
        if len(seq) < 4:
            return patterns
            
        i = 0
        while i < len(seq) - 3:
            if (seq[i] != seq[i+1] and seq[i+1] != seq[i+2] and 
                seq[i] == seq[i+2] and seq[i+1] == seq[i+3]):
                
                # Encontra o fim do padrão
                j = i + 4
                while (j < len(seq) - 1 and 
                       seq[j] == seq[i] and seq[j+1] == seq[i+1]):
                    j += 2
                
                if j - i >= 4:
                    patterns.append(
                        f"Zig-Zag {seq[i]}-{seq[i+1]} detectado (pos. {i+1}-{j})"
                    )
                i = j
            else:
                i += 1
        return patterns
    
    def _detect_surf_break(self, seq: List[str]) -> List[str]:
        """Detecta quebras de sequência"""
        patterns = []
        if len(seq) < 4:
            return patterns
            
        for i in range(len(seq) - 3):
            if (seq[i] == seq[i+1] == seq[i+2] and 
                seq[i+3] != seq[i]):
                patterns.append(
                    f"Quebra de Surf: '{seq[i]}' (3x) → '{seq[i+3]}' (pos. {i+4})"
                )
        return patterns
    
    def _detect_zigzag_break(self, seq: List[str]) -> List[str]:
        """Detecta quebras de zig-zag"""
        patterns = []
        if len(seq) < 4:
            return patterns
            
        for i in range(len(seq) - 3):
            if (seq[i] != seq[i+1] and seq[i+1] != seq[i+2] and 
                seq[i] == seq[i+2] and seq[i+3] != seq[i] and 
                seq[i+3] != seq[i+1]):
                patterns.append(
                    f"Quebra Zig-Zag: {seq[i]}-{seq[i+1]}-{seq[i]} → '{seq[i+3]}' (pos. {i+4})"
                )
        return patterns
    
    def _detect_repeated_pairs(self, seq: List[str]) -> List[str]:
        """Detecta duplas repetidas (AABB)"""
        patterns = []
        if len(seq) < 4:
            return patterns
            
        for i in range(len(seq) - 3):
            if (seq[i] == seq[i+1] and seq[i+2] == seq[i+3] and 
                seq[i] != seq[i+2]):
                patterns.append(
                    f"Duplas: {seq[i]}{seq[i]} → {seq[i+2]}{seq[i+2]} (pos. {i+1}-{i+4})"
                )
        return patterns
    
    def _detect_recurring_draw(self, seq: List[str]) -> List[str]:
        """Detecta empates recorrentes"""
        patterns = []
        draw_indices = [i for i, x in enumerate(seq) if x == self.empate_char]
        
        if len(draw_indices) < 2:
            return patterns
            
        for i in range(len(draw_indices) - 1):
            diff = draw_indices[i+1] - draw_indices[i]
            if 2 <= diff <= 4:  # Intervalo ampliado
                patterns.append(
                    f"Empates próximos: pos. {draw_indices[i]+1} e {draw_indices[i+1]+1} "
                    f"(intervalo: {diff-1})"
                )
        return patterns
    
    def _detect_ladder_pattern(self, seq: List[str]) -> List[str]:
        """Detecta padrão escada (1-2-3)"""
        patterns = []
        if len(seq) < 6:
            return patterns
            
        for i in range(len(seq) - 5):
            if (seq[i] != seq[i+1] and
                seq[i+1] == seq[i+2] and seq[i+1] != seq[i] and
                seq[i+3] == seq[i+4] == seq[i+5] and seq[i+3] == seq[i]):
                patterns.append(
                    f"Escada: 1×{seq[i]} → 2×{seq[i+1]} → 3×{seq[i]} (pos. {i+1})"
                )
        return patterns
    
    def _detect_mirror_pattern(self, seq: List[str]) -> List[str]:
        """Detecta padrão espelho (ABBA)"""
        patterns = []
        if len(seq) < 4:
            return patterns
            
        for i in range(len(seq) - 3):
            if (seq[i] == seq[i+3] and seq[i+1] == seq[i+2] and 
                seq[i] != seq[i+1]):
                patterns.append(
                    f"Espelho: {seq[i]}{seq[i+1]}{seq[i+2]}{seq[i+3]} (pos. {i+1})"
                )
        return patterns
    
    def _detect_alternation_with_draw(self, seq: List[str]) -> List[str]:
        """Detecta alternância com empate no meio"""
        patterns = []
        if len(seq) < 3:
            return patterns
            
        for i in range(len(seq) - 2):
            if (seq[i+1] == self.empate_char and 
                seq[i] != self.empate_char and 
                seq[i+2] != self.empate_char and 
                seq[i] != seq[i+2]):
                patterns.append(
                    f"Alternância c/ Empate: {seq[i]}-E-{seq[i+2]} (pos. {i+1})"
                )
        return patterns
    
    def _detect_wave_pattern(self, seq: List[str]) -> List[str]:
        """Detecta padrão onda (ABAB)"""
        patterns = []
        if len(seq) < 4:
            return patterns
            
        for i in range(len(seq) - 3):
            if (seq[i] == seq[i+2] and seq[i+1] == seq[i+3] and 
                seq[i] != seq[i+1]):
                patterns.append(
                    f"Onda: {seq[i]}-{seq[i+1]}-{seq[i]}-{seq[i+1]} (pos. {i+1})"
                )
        return patterns
    
    def _detect_3x1_pattern(self, seq: List[str]) -> List[str]:
        """Detecta padrão 3x1"""
        patterns = []
        if len(seq) < 4:
            return patterns
            
        for i in range(len(seq) - 3):
            if (seq[i] == seq[i+1] == seq[i+2] and 
                seq[i+3] != seq[i]):
                patterns.append(
                    f"3×1: {seq[i]}×3 → {seq[i+3]} (pos. {i+1})"
                )
        return patterns
    
    def _detect_3x3_pattern(self, seq: List[str]) -> List[str]:
        """Detecta padrão 3x3"""
        patterns = []
        if len(seq) < 6:
            return patterns
            
        for i in range(len(seq) - 5):
            if (seq[i] == seq[i+1] == seq[i+2] and 
                seq[i+3] == seq[i+4] == seq[i+5] and 
                seq[i] != seq[i+3]):
                patterns.append(
                    f"3×3: {seq[i]}×3 → {seq[i+3]}×3 (pos. {i+1})"
                )
        return patterns
    
    def _analyze_tactical_prediction(self, seq: List[str]) -> List[str]:
        """Análise tática dos últimos jogos"""
        results = []
        
        for window in [5, 7, 10]:
            if len(seq) >= window:
                recent = seq[-window:]
                counter = Counter(recent)
                most_common = counter.most_common(1)[0]
                percentage = (most_common[1] / window) * 100
                
                results.append(
                    f"Últimos {window}: '{most_common[0]}' apareceu "
                    f"{most_common[1]}×({percentage:.1f}%)"
                )
        
        return results
    
    def _generate_suggestions(self, seq: List[str], patterns: List[PatternResult]) -> List[str]:
        """Gera sugestões baseadas nos padrões"""
        if not seq:
            return []
            
        suggestions = []
        last = seq[-1] if seq else None
        
        # Análise por tipo de padrão
        surf_patterns = [p for p in patterns if "Surf" in p.pattern_type and "Quebra" not in p.pattern_type]
        if surf_patterns and last:
            suggestions.append(f"🔥 Continuar Surf com '{last}'")
        
        zigzag_patterns = [p for p in patterns if "Zig-Zag" in p.pattern_type and "Quebra" not in p.pattern_type]
        if zigzag_patterns and len(seq) >= 2:
            next_expected = seq[-2] if seq[-1] != seq[-2] else seq[-1]
            suggestions.append(f"⚡ Continuar Zig-Zag com '{next_expected}'")
        
        # Sugestão baseada em frequência recente
        if len(seq) >= 5:
            recent_counter = Counter(seq[-5:])
            least_common = recent_counter.most_common()[-1]
            suggestions.append(f"📊 Considerar '{least_common[0]}' (menos frequente recentemente)")
        
        return suggestions
    
    def _analyze_draw_possibilities(self, seq: List[str], patterns: List[PatternResult]) -> List[str]:
        """Analisa possibilidades de empate"""
        possibilities = []
        
        draw_count = seq.count(self.empate_char)
        total = len(seq)
        
        if total > 0:
            draw_freq = draw_count / total
            
            if draw_freq > 0.25:
                possibilities.append(f"🎯 Alta frequência de empates ({draw_freq:.1%})")
            elif draw_count == 0 and total > 5:
                possibilities.append("⚠️ Ausência de empates pode indicar compensação")
        
        # Análise de padrões com empate
        empate_patterns = [p for p in patterns if "Empate" in p.pattern_type]
        if empate_patterns:
            possibilities.append("🔄 Padrões com empate detectados")
        
        return possibilities
    
    def _calculate_statistics(self, seq: List[str]) -> Dict[str, float]:
        """Calcula estatísticas da sequência"""
        if not seq:
            return {}
            
        counter = Counter(seq)
        total = len(seq)
        
        stats = {
            'total_jogos': total,
            'casa_freq': counter.get('C', 0) / total,
            'visitante_freq': counter.get('V', 0) / total,
            'empate_freq': counter.get('E', 0) / total,
        }
        
        # Streak atual
        if seq:
            current_streak = 1
            for i in range(len(seq) - 1, 0, -1):
                if seq[i] == seq[i-1]:
                    current_streak += 1
                else:
                    break
            stats['streak_atual'] = current_streak
            stats['ultimo_resultado'] = seq[-1]
        
        return stats

# CSS melhorado
def load_css():
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #1f4037, #99f2c8);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .pattern-card {
        background: #f8f9fa;
        padding: 1rem;
        border-left: 4px solid #28a745;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    
    .suggestion-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .stats-container {
        background: #f1f3f4;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .confidence-high { border-left-color: #28a745; }
    .confidence-medium { border-left-color: #ffc107; }
    .confidence-low { border-left-color: #dc3545; }
    </style>
    """, unsafe_allow_html=True)

# Inicialização da sessão
def init_session_state():
    defaults = {
        'current_sequence': [],
        'history': [],
        'analyzer': PatternAnalyzer(),
        'show_advanced': False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Interface principal
def main():
    load_css()
    init_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Analisador de Padrões Avançado</h1>
        <p>Análise inteligente de sequências com IA e estatísticas avançadas</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Layout principal
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("⚡ Entrada Rápida")
        
        # Botões de entrada
        col_c, col_v, col_e = st.columns(3)
        with col_c:
            if st.button("🏠 Casa", use_container_width=True, type="primary"):
                st.session_state.current_sequence.append('C')
                st.rerun()
        with col_v:
            if st.button("✈️ Visitante", use_container_width=True, type="secondary"):
                st.session_state.current_sequence.append('V')
                st.rerun()
        with col_e:
            if st.button("🤝 Empate", use_container_width=True, type="secondary"):
                st.session_state.current_sequence.append('E')
                st.rerun()
        
        st.divider()
        
        # Controles
        col_undo, col_clear = st.columns(2)
        with col_undo:
            if st.button("↶ Desfazer", use_container_width=True):
                if st.session_state.current_sequence:
                    st.session_state.current_sequence.pop()
                    st.success("Desfeito!")
                    st.rerun()
        
        with col_clear:
            if st.button("🗑️ Limpar", use_container_width=True):
                st.session_state.current_sequence = []
                st.success("Limpo!")
                st.rerun()
        
        # Sequência atual
        if st.session_state.current_sequence:
            st.subheader("📊 Sequência Atual")
            seq_str = "".join(st.session_state.current_sequence)
            
            # Formatação melhorada
            formatted = " ".join([f"{i+1:2d}" for i in range(len(seq_str))])
            st.code(f"Pos: {formatted}\nRes: {' '.join(seq_str)}")
            
            st.info(f"**Total:** {len(seq_str)} jogos | **Sequência:** `{seq_str}`")
    
    with col2:
        if st.session_state.current_sequence:
            # Análise
            analyzer = st.session_state.analyzer
            result = analyzer.analyze_sequence(st.session_state.current_sequence)
            
            # Sugestões
            if result.suggestions:
                st.subheader("🎯 Sugestões Inteligentes")
                for suggestion in result.suggestions:
                    st.markdown(f"""
                    <div class="suggestion-card">
                        {suggestion}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Possibilidades de empate
            if result.empate_possibilities:
                st.subheader("🤝 Análise de Empates")
                for possibility in result.empate_possibilities:
                    st.warning(possibility)
            
            # Padrões detectados
            st.subheader("🔍 Padrões Detectados")
            if result.patterns:
                for pattern in result.patterns:
                    confidence_class = (
                        "confidence-high" if pattern.confidence > 0.7 
                        else "confidence-medium" if pattern.confidence > 0.5 
                        else "confidence-low"
                    )
                    
                    st.markdown(f"""
                    <div class="pattern-card {confidence_class}">
                        <strong>{pattern.pattern_type}</strong><br>
                        {pattern.description}<br>
                        <small>Confiança: {pattern.confidence:.1%}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Nenhum padrão detectado ainda. Continue adicionando resultados.")
            
            # Estatísticas
            if result.statistics:
                st.subheader("📈 Estatísticas")
                stats = result.statistics
                
                # Gráfico de distribuição
                df = pd.DataFrame({
                    'Resultado': ['Casa', 'Visitante', 'Empate'],
                    'Frequência': [
                        stats.get('casa_freq', 0),
                        stats.get('visitante_freq', 0),
                        stats.get('empate_freq', 0)
                    ]
                })
                
                fig = px.pie(df, values='Frequência', names='Resultado', 
                            title="Distribuição dos Resultados")
                st.plotly_chart(fig, use_container_width=True)
                
                # Métricas
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric("Total de Jogos", int(stats.get('total_jogos', 0)))
                with col_m2:
                    st.metric("Streak Atual", int(stats.get('streak_atual', 0)))
                with col_m3:
                    st.metric("Último", stats.get('ultimo_resultado', '-'))
        
        else:
            st.info("👆 Adicione alguns resultados para começar a análise!")
    
    # Configurações avançadas
    with st.expander("⚙️ Configurações Avançadas"):
        st.checkbox("Mostrar análise detalhada", key="show_advanced")
        
        if st.session_state.show_advanced and st.session_state.current_sequence:
            st.subheader("🔬 Análise Detalhada")
            
            # Análise de transições
            if len(st.session_state.current_sequence) > 1:
                transitions = {}
                seq = st.session_state.current_sequence
                
                for i in range(len(seq) - 1):
                    transition = f"{seq[i]} → {seq[i+1]}"
                    transitions[transition] = transitions.get(transition, 0) + 1
                
                st.write("**Transições mais frequentes:**")
                for trans, count in sorted(transitions.items(), key=lambda x: x[1], reverse=True):
                    st.write(f"- {trans}: {count}×")
    
    # Histórico
    st.divider()
    st.subheader("📚 Histórico")
    
    col_hist1, col_hist2 = st.columns([3, 1])
    with col_hist2:
        if st.button("🗑️ Limpar Histórico", use_container_width=True):
            st.session_state.history = []
            st.success("Histórico limpo!")
            st.rerun()
    
    if st.session_state.history:
        for i, entry in enumerate(st.session_state.history[-5:], 1):  # Últimas 5
            st.code(f"Análise {len(st.session_state.history)-5+i}: {entry}")
    else:
        st.info("Nenhum histórico ainda.")

if __name__ == "__main__":
    main()
