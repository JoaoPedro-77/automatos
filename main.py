from dfa import DFA
from nfa import NFA

if __name__ == "__main__":
  # --- 1. Exemplo de DFA ---
  # Linguagem: Strings definidas sobre o alfabeto Sigma = {a, b} que não contêm a subpalavra "ba"
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

  print("\n" + "=" * 40 + "\n")


  # --- 2. Exemplo de NFA ---
  # Linguagem: Strings sobre {a, b} que terminam com "ab"
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