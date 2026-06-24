import string

from dfa import DFA
from nfa import NFA

if __name__ == "__main__":
  
  letras = set(string.ascii_lowercase)
  digitos = set(string.digits)
  sigma_url = letras | digitos | {':', '/', '.', '-', '_', '=', '?', '#', '%'}

  dfa_url_transicoes = {
    (0, 'h'): 1,
    (1, 't'): 2,
    (2, 't'): 3,
    (3, 'p'): 4,
    (4, ':'): 5,
    (5, '/'): 6,
    (6, '/'): 7
  }

    # Do estado 7 em diante: qualquer char válido de domínio/path
  chars_dominio = letras | digitos | {'.', '-', '_', '/', '=', '?', '#', '%'} # Domínio não possui ':'
  
  # A string é aceita se ler o prefixo 'http://' seguido de pelo menos um char do domínio

  for c in chars_dominio:
    dfa_url_transicoes[(7, c)] = 8
    dfa_url_transicoes[(8, c)] = 8

  dfa_url = DFA(  
    Q={0, 1, 2, 3, 4, 5, 6, 7, 8},
    sigma=sigma_url,
    delta=dfa_url_transicoes,
    q0=0,
    F={8}  # aceita após ler pelo menos 1 char do domínio
  )


  print("=== Testando DFA com o prefixo 'http://' ===")
  
  testes_dfa = ["http://google.com", "http://localhost:8080/teste", "http://google.com/search?q=python", "http://", "https://google.com", "ftp://google.com", "http://google.com/search?q=python"]

  for teste in testes_dfa:
    resultado = dfa_url.run(teste)
    print(f"DFA.run('{teste}') -> {resultado}\n")

  print("\n" + "=" * 40 + "\n")


  # --- 2. Exemplo de NFA ---

  # Alfabeto: letras, dígitos e símbolos comuns de URL
  letras = set(string.ascii_lowercase)
  digitos = set(string.digits)

  sigma_url = letras | digitos | {':', '/', '.', '-', '_', '=', '?', '#', '%'}
  # Transições fixas do prefixo "http://"
  nfa_url_transicoes = {
    (0, 'h'): {1},
    (1, 't'): {2},
    (2, 't'): {3},
    (3, 'p'): {4},
    (4, ':'): {5},
    (5, '/'): {6},
    (6, '/'): {7},
  }

  # Do estado 7 em diante: qualquer char válido de domínio/path
  chars_dominio = letras | digitos | {'.', '-', '_', '/', '=', '?', '#', '%'} # Domínio não possui ':'
  
  # A string é aceita se ler o prefixo 'http://' seguido de pelo menos um char do domínio

  for c in chars_dominio:
    nfa_url_transicoes[(7, c)] = {8}
    nfa_url_transicoes[(8, c)] = {8}

  nfa_url = NFA(
    Q={0, 1, 2, 3, 4, 5, 6, 7, 8},
    sigma=sigma_url,
    delta=nfa_url_transicoes,
    q0=0,
    F={8}  # aceita após ler pelo menos 1 char do domínio
  )

  print("=== Testando NFA (URLs com prefixo 'http://') ===")
  testes_nfa = ["http://", "http://google", "http://google.com", "https://google.com", "ftp://google.com", "http://google.com/", "http://google.com/search?q=python"]

  for teste in testes_nfa:
    resultado = nfa_url.run(teste)
    print(f"NFA.run('{teste}') -> {resultado}\n")
  

  print("Deseja testar sua própria URL?")
  resposta = input("S/N: ").upper()
  if resposta == "S":
    while True:
      palavra = input("Digite a palavra: ")
      resultado_nfa = nfa_url.run(palavra)
      resultado_dfa = dfa_url.run(palavra)
      print(f"DFA.run('{palavra}') -> {resultado_dfa}")
      print(f"NFA.run('{palavra}') -> {resultado_nfa}")

      resposta = input("Deseja fazer mais algum teste? S/N: ").upper()
      if resposta == "N":
        print("Obrigado por usar o simulador!")
        break
    
  else: 
    print("Obrigado por usar o simulador!")