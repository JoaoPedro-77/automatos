class DFA:
  def __init__(self, Q, sigma, delta, q0, F):
    self.Q = Q          # Conjunto de estados (ex: {0, 1, 2})
    self.sigma = sigma  # Alfabeto (ex: {"a", "b"})
    self.delta = delta  # Transições: dicionário mapeando (estado, símbolo) -> estado
    self.q0 = q0        # Estado inicial
    self.F = F          # Conjunto de estados finais (aceitação)
  
  def __repr__(self):
    return f"DFA(Q={self.Q}, sigma={self.sigma}, q0={self.q0}, F={self.F})"

  def run(self, w):
    q = self.q0
    for symbol in w:
      if symbol not in self.sigma:
        raise ValueError(f"Símbolo '{symbol}' não pertence ao alfabeto {self.sigma}")

      if (q, symbol) in self.delta:
        # Se houver transição definida, o autômato transita para o estado seguinte
        q = self.delta[(q, symbol)]  

      else:
        # Se não houver transição definida, o autômato rejeita a cadeia
        return False
        
        # A variável 'in' verifica se o elemento está presente no conjunto
    return q in self.F


class NFA:
  def __init__(self, Q, sigma, delta, q0, F):
    self.Q = Q          # Conjunto de estados
    self.sigma = sigma  # Alfabeto
    self.delta = delta  # Transições: dicionário mapeando (estado, símbolo) -> conjunto de estados
    self.q0 = q0        # Estado inicial
    self.F = F          # Conjunto de estados finais (aceitação)

  def __repr__(self):
    return f"NFA(Q={self.Q}, sigma={self.sigma}, q0={self.q0}, F={self.F})"

  def epsilon_closure(self, states):
    """Calcula o fecho-épsilon para um conjunto de estados."""
    closure = set(states)
    stack = list(states)

    while stack:
      state = stack.pop()
      # Usamos a string vazia "" para representar transições épsilon (ε)
      if (state, "") in self.delta:
        for next_state in self.delta[(state, "")]:
          if next_state not in closure:
            closure.add(next_state)
            stack.append(next_state)
    return closure

  def run(self, w):
    # O conjunto de estados atuais começa com o fecho-épsilon do estado inicial
    current_states = self.epsilon_closure({self.q0})
    
    for symbol in w:
      if symbol not in self.sigma:
        raise ValueError(f"Símbolo '{symbol}' não pertence ao alfabeto {self.sigma}")
      
      next_states = set()
      for state in current_states:
        if (state, symbol) in self.delta:
          next_states.update(self.delta[(state, symbol)])
      
      current_states = self.epsilon_closure(next_states)
      
    # Aceita se pelo menos um dos estados alcançados for final
    return len(current_states.intersection(self.F)) > 0


# ==========================================
# Exemplos de uso e testes
# ==========================================

if __name__ == "__main__":
  # --- 1. Exemplo de DFA ---
  # Linguagem: Cadeias sobre {a, b} que não contêm a subsequência "ba"
  # Estados:
  #   0: estado inicial, aceita qualquer sequência de "a"s
  #   1: leu um "b", aceita contanto que não venha um "a" depois
  #   2: leu "ba", estado de erro (rejeição permanente)
  dfa_transicoes = {
    (0, "a"): 0, (0, "b"): 1,
    (1, "a"): 2, (1, "b"): 1,
    (2, "a"): 2, (2, "b"): 2
  }
  
  dfa_exemplo = DFA(Q={0, 1, 2}, sigma={"a", "b"}, delta=dfa_transicoes, q0=0, F={0, 1}) 

  print("=== Testando DFA (Cadeias sem 'ba') ===")
  testes_dfa = ["a", "aa", "ab", "b", "bb", "aba", "ba", "aab", "abbb", "bbba"]
  for teste in testes_dfa:
    resultado = dfa_exemplo.run(teste)
    print(f"DFA.run('{teste}') -> {resultado}")

  print("\n" + "="* 40 + "\n")

  # --- 2. Exemplo de NFA ---
  # Linguagem: Cadeias sobre {a, b} que terminam com "ab"
  # Estados:
  #   0: estado inicial (pode ler 'a' ou 'b' e continuar em 0, ou ler 'a' e ir para 1)
  #   1: leu um 'a' que possivelmente é o início de "ab"
  #   2: leu o 'b' final (estado de aceitação)
  nfa_transicoes = {
    (0, "a"): {0, 1},
    (0, "b"): {0},
    (1, "b"): {2}
  }
  nfa_exemplo = NFA(Q={0, 1, 2}, sigma={"a", "b"}, delta=nfa_transicoes, q0=0, F={2})

  print("=== Testando NFA (Cadeias terminando com 'ab') ===")
  testes_nfa = ["ab", "aab", "bab", "abbab", "a", "b", "ba", "aba", "abab"]
  for teste in testes_nfa:
    resultado = nfa_exemplo.run(teste)
    print(f"NFA.run('{teste}') -> {resultado}")