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
