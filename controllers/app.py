import sys
import os

# Adiciona o diretório pai (raiz do projeto) ao sys.path para permitir importações do módulo 'models'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import string
import pandas as pd
import graphviz

from models.dfa import DFA
from models.nfa import NFA
from models.builder import get_automata
from views.web import render_interface

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Simulador de Autômatos (URL)",
    layout="wide"
)

# Estilos CSS adicionais para melhorar o visual 
st.markdown("""
<style>
    .stAlert {
        border-radius: 8px;
    }
    h1, h2, h3 {
        font-family: 'Outfit', 'Inter', sans-serif;
    }
    .dataframe {
        font-size: 14px !important;
    }
</style>
""", unsafe_allow_html=True)

# Funções auxiliares de execução passo a passo
def run_dfa_step_by_step(dfa, w):
    history = []
    q = dfa.q0
    history.append((0, "(início)", {q}))
    
    for i, symbol in enumerate(w):
        if symbol not in dfa.sigma:
            history.append((i + 1, f"Erro: '{symbol}' fora do alfabeto", set()))
            break
        if (q, symbol) in dfa.delta:
            next_q = dfa.delta[(q, symbol)]
            history.append((i + 1, symbol, {next_q}))
            q = next_q
        else:
            history.append((i + 1, symbol, set()))
            break
    return history

def run_nfa_step_by_step(nfa, w):
    history = []
    current_states = {nfa.q0}
    history.append((0, "(início)", current_states))
    
    for i, symbol in enumerate(w):
        if symbol not in nfa.sigma:
            history.append((i + 1, f"Erro: '{symbol}' fora do alfabeto", set()))
            break
        next_states = set()
        for state in current_states:
            if (state, symbol) in nfa.delta:
                next_states.update(nfa.delta[(state, symbol)])
        current_states = next_states
        history.append((i + 1, symbol, current_states))
        if not current_states:
            break
    return history

# Função para gerar a tabela de transição 
def get_transition_table(automata, is_nfa):
    letras = set(string.ascii_lowercase)
    digitos = set(string.digits)
    
    # Categorias de símbolos para as colunas
    categories = {
        "'h'": 'h',
        "'t'": 't',
        "'p'": 'p',
        "':'": ':',
        "'/'": '/',
        "[0-9] (Dígitos)": '0',
        "[a-z exc. h,t,p]": 'x',
        "[.-_] (Símbolos Host)": '.',
        "[=?#%] (Símbolos Path)": '?'
    }
    
    rows = []
    for state in sorted(list(automata.Q)):
        row_data = {
            "Estado": f"q{state}",
            "Tipo": "Final (Aceito)" if state in automata.F else "Normal"
        }
        
        for col_name, rep_char in categories.items():
            if is_nfa:
                dest = automata.delta.get((state, rep_char), set())
                row_data[col_name] = f"{{{', '.join(f'q{d}' for d in sorted(list(dest)))}}}" if dest else "-"
            else:
                dest = automata.delta.get((state, rep_char), None)
                row_data[col_name] = f"q{dest}" if dest is not None else "-"
                
        rows.append(row_data)
        
    df = pd.DataFrame(rows)
    return df

# Geração do diagrama de estados usando Graphviz
def generate_graphviz_dot(automata, is_nfa, active_states):
    dot = graphviz.Digraph(comment="Automata Graph")
    dot.attr(rankdir="LR", size="15,4", bgcolor="#161b22")
    
    # Estilos de nós e fontes padrão do gráfico
    dot.attr('node', fontname="Inter, Arial, sans-serif", fontsize="12", fontcolor="white")
    dot.attr('edge', fontname="Inter, Arial, sans-serif", fontsize="10", fontcolor="#8b949e")

    # Adicionar os nós (estados)
    for state in sorted(list(automata.Q)):
        is_active = (state in active_states)
        is_final = (state in automata.F)
        
        shape = "doublecircle" if is_final else "circle"
        
        # Destaque de cor
        if is_active:
            dot.node(
                str(state), 
                label=f"q{state}", 
                shape=shape, 
                style="filled", 
                fillcolor="#f59e0b",  # Dourado ativo
                color="#fbbf24", 
                fontcolor="black"
            )
        elif is_final:
            dot.node(
                str(state), 
                label=f"q{state}", 
                shape=shape, 
                style="filled", 
                fillcolor="#047857",  # Verde aceitação
                color="#10b981",
                fontcolor="white"
            )
        else:
            dot.node(
                str(state), 
                label=f"q{state}", 
                shape=shape, 
                style="filled", 
                fillcolor="#21262d",  # Cinza padrão
                color="#30363d",
                fontcolor="white"
            )
            
    # Agrupar transições com mesma origem e destino
    edges = {}
    if is_nfa:
        for (src, symbol), dests in automata.delta.items():
            for dst in dests:
                key = (src, dst)
                if key not in edges:
                    edges[key] = []
                edges[key].append(symbol)
    else:
        for (src, symbol), dst in automata.delta.items():
            key = (src, dst)
            if key not in edges:
                edges[key] = []
            edges[key].append(symbol)
            
    # Adicionar arestas ao gráfico
    for (src, dst), symbols in edges.items():
        symbol_label = ", ".join(sorted(symbols))
        
        # Simplificação visual para conjuntos grandes
        if len(symbols) > 10:
            letras = set(string.ascii_lowercase)
            digitos = set(string.digits)
            chars_host = letras | digitos | {'.', '-', '_'}
            chars_path = letras | digitos | {'.', '-', '_', '/', '=', '?', '#', '%', ':'}
            symbol_set = set(symbols)
            
            if symbol_set == chars_host:
                symbol_label = "[a-z0-9.-_]"
            elif symbol_set == chars_path:
                symbol_label = "path_chars"
            elif symbol_set == (chars_path - chars_host - {':'}):
                symbol_label = "symbols"
            elif symbol_set == digitos:
                symbol_label = "[0-9]"

        dot.edge(
            str(src), 
            str(dst), 
            label=symbol_label, 
            color="#8b949e"
        )
        
    return dot

# --- Interface Streamlit ---

dfa_url, nfa_url = get_automata()

render_interface(
    dfa_url=dfa_url,
    nfa_url=nfa_url,
    run_dfa_step_by_step=run_dfa_step_by_step,
    run_nfa_step_by_step=run_nfa_step_by_step,
    generate_graphviz_dot=generate_graphviz_dot,
    get_transition_table=get_transition_table
)
