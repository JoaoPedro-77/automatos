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
      if (q, symbol) in self.delta:
        # Se houver transição definida, o autômato transita para o estado seguinte
        q = self.delta[(q, symbol)]  

      else:
        # Se não houver transição definida, o autômato rejeita a cadeia
        return False
        
    return q in self.F
