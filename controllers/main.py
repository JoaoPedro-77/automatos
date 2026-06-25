from src.builder import get_automata

if __name__ == "__main__":
  dfa_url, nfa_url = get_automata()

  print("=== Testando DFA com o prefixo 'http://' ===")
  
  testes_dfa = ["http://google.com", "http://localhost:8080/teste", "http://google.com/search?q=python", "http://", "https://google.com", "ftp://google.com", "http://google.com/search?q=python"]

  for teste in testes_dfa:
    resultado = dfa_url.run(teste)
    print(f"DFA.run('{teste}') -> {resultado}\n")

  print("\n" + "=" * 40 + "\n")

  print("=== Testando NFA (URLs com prefixo 'http://') ===")
  testes_nfa = ["http://", "http://google", "http://google.com", "https://google.com", "ftp://google.com", "http://google.com/", "http://google.com/search?q=python"]

  for teste in testes_nfa:
    try:
      resultado = nfa_url.run(teste)
      print(f"NFA.run('{teste}') -> {resultado}\n")
    except ValueError as e:
      print(f"NFA.run('{teste}') -> Erro: {e}\n")
  

  print("Deseja testar sua própria URL?")
  resposta = input("S/N: ").upper()
  if resposta == "S":
    while True:
      palavra = input("Digite a palavra: ")
      try:
        resultado_nfa = nfa_url.run(palavra)
      except ValueError as e:
        resultado_nfa = f"Erro ({e})"
      resultado_dfa = dfa_url.run(palavra)
      print(f"DFA.run('{palavra}') -> {resultado_dfa}")
      print(f"NFA.run('{palavra}') -> {resultado_nfa}")

      resposta = input("Deseja fazer mais algum teste? S/N: ").upper()
      if resposta == "N":
        print("Obrigado por usar o simulador!")
        break
    
  else: 
    print("Obrigado por usar o simulador!")