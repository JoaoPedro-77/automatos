class NFA:
  def __init__(self, Q, sigma, delta, q0, F):
    self.Q = Q          # Conjunto de estados
    self.sigma = sigma  # Alfabeto
    self.delta = delta  # Transições: dicionário mapeando (estado, símbolo) -> conjunto de estados
    self.q0 = q0        # Estado inicial
    self.F = F          # Conjunto de estados finais (aceitação)

  def __repr__(self):
    return f"NFA(Q={self.Q}, sigma={self.sigma}, q0={self.q0}, F={self.F})"

  def run(self, w):
    current_states = {self.q0}
    
    for symbol in w:
      if symbol not in self.sigma:
        raise ValueError(f"Símbolo '{symbol}' não pertence ao alfabeto {self.sigma}")
      
      next_states = set()
      for state in current_states:
        if (state, symbol) in self.delta:
          next_states.update(self.delta[(state, symbol)])
      
      current_states = next_states
      
    # Aceita se pelo menos um dos estados alcançados for final
    return len(current_states.intersection(self.F)) > 0
