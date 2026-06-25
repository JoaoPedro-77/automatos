import string
from src.dfa import DFA
from src.nfa import NFA

def get_automata():
    letras = set(string.ascii_lowercase)
    digitos = set(string.digits)
    sigma_url = letras | digitos | {':', '/', '.', '-', '_', '=', '?', '#', '%'}

    # 1. Definição do DFA
    dfa_url_transicoes = {
        (0, 'h'): 1,
        (1, 't'): 2,
        (2, 't'): 3,
        (3, 'p'): 4,
        (4, ':'): 5,
        (5, '/'): 6,
        (6, '/'): 7
    }
    chars_host = letras | digitos | {'.', '-', '_'}
    chars_path = letras | digitos | {'.', '-', '_', '/', '=', '?', '#', '%', ':'}
    non_host_path_chars = {'/', '?', '#', '=', '%'}

    for c in chars_host:
        dfa_url_transicoes[(7, c)] = 8
        dfa_url_transicoes[(8, c)] = 8

    dfa_url_transicoes[(8, ':')] = 9
    for c in non_host_path_chars:
        dfa_url_transicoes[(8, c)] = 11

    for d in digitos:
        dfa_url_transicoes[(9, d)] = 10
        dfa_url_transicoes[(10, d)] = 10

    for c in non_host_path_chars:
        dfa_url_transicoes[(10, c)] = 11

    for c in chars_path:
        dfa_url_transicoes[(11, c)] = 11

    dfa_url = DFA(  
        Q={0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11},
        sigma=sigma_url,
        delta=dfa_url_transicoes,
        q0=0,
        F={8, 10, 11}
    )

    # 2. Definição do NFA
    nfa_url_transicoes = {
        (0, 'h'): {1},
        (1, 't'): {2},
        (2, 't'): {3},
        (3, 'p'): {4},
        (4, ':'): {5},
        (5, '/'): {6},
        (6, '/'): {7},
    }

    for c in chars_host:
        nfa_url_transicoes[(7, c)] = {8}
        nfa_url_transicoes[(8, c)] = {8}

    nfa_url_transicoes[(8, ':')] = {9}
    for c in non_host_path_chars:
        nfa_url_transicoes[(8, c)] = {11}

    for d in digitos:
        nfa_url_transicoes[(9, d)] = {10}
        nfa_url_transicoes[(10, d)] = {10}

    for c in non_host_path_chars:
        nfa_url_transicoes[(10, c)] = {11}

    for c in chars_path:
        nfa_url_transicoes[(11, c)] = {11}

    nfa_url = NFA(
        Q={0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11},
        sigma=sigma_url,
        delta=nfa_url_transicoes,
        q0=0,
        F={8, 10, 11}
    )
    
    return dfa_url, nfa_url
