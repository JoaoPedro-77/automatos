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

  # Definindo partes de uma URL para suporte a portas
  chars_host = letras | digitos | {'.', '-', '_'}
  chars_path = letras | digitos | {'.', '-', '_', '/', '=', '?', '#', '%', ':'}
  non_host_path_chars = {'/', '?', '#', '=', '%'}

  # Do estado 7 em diante:
  # Estado 7: leu 'http://'. Precisa de pelo menos um caractere de host para ir ao estado 8.
  for c in chars_host:
    dfa_url_transicoes[(7, c)] = 8
    dfa_url_transicoes[(8, c)] = 8

  # Do estado 8 (Host/Domínio):
  # - Se ler ':', vai para o estado 9 (início da porta)
  dfa_url_transicoes[(8, ':')] = 9
  # - Se ler caracteres não-host do path, vai para o estado 11 (caminho/query)
  for c in non_host_path_chars:
    dfa_url_transicoes[(8, c)] = 11

  # Do estado 9 (Lendo porta):
  # - Precisa de um dígito para ir ao estado 10 (porta válida)
  for d in digitos:
    dfa_url_transicoes[(9, d)] = 10
    dfa_url_transicoes[(10, d)] = 10

  # Do estado 10 (Porta válida):
  # - Se ler caracteres de path, vai para o estado 11
  for c in non_host_path_chars:
    dfa_url_transicoes[(10, c)] = 11

  # Do estado 11 (Caminho/Query):
  # - Aceita qualquer caractere válido de path
  for c in chars_path:
    dfa_url_transicoes[(11, c)] = 11

  dfa_url = DFA(  
    Q={0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11},
    sigma=sigma_url,
    delta=dfa_url_transicoes,
    q0=0,
    F={8, 10, 11}  # aceita se terminar no domínio, na porta ou no caminho
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

  # Definindo partes de uma URL para suporte a portas no NFA
  chars_host = letras | digitos | {'.', '-', '_'}
  chars_path = letras | digitos | {'.', '-', '_', '/', '=', '?', '#', '%', ':'}
  non_host_path_chars = {'/', '?', '#', '=', '%'}

  # Do estado 7 em diante:
  for c in chars_host:
    nfa_url_transicoes[(7, c)] = {8}
    nfa_url_transicoes[(8, c)] = {8}

  # Transições do estado 8 (Host):
  nfa_url_transicoes[(8, ':')] = {9}
  for c in non_host_path_chars:
    nfa_url_transicoes[(8, c)] = {11}

  # Transições do estado 9 (Porta):
  for d in digitos:
    nfa_url_transicoes[(9, d)] = {10}
    nfa_url_transicoes[(10, d)] = {10}

  # Transições do estado 10 (Porta válida):
  for c in non_host_path_chars:
    nfa_url_transicoes[(10, c)] = {11}

  # Transições do estado 11 (Caminho/Query):
  for c in chars_path:
    nfa_url_transicoes[(11, c)] = {11}

  nfa_url = NFA(
    Q={0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11},
    sigma=sigma_url,
    delta=nfa_url_transicoes,
    q0=0,
    F={8, 10, 11}  # aceita se terminar no domínio, na porta ou no caminho
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