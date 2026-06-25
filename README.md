# Simulador de Autômatos (DFA e NFA)

Simulador didático com interface gráfica e de terminal para validação de Autômatos Finitos Determinísticos (DFA) e Não Determinísticos (NFA), desenvolvido como um projeto de estudo. Atualmente, o autômato está configurado para simular e validar a estrutura de URLs (ex: `http://localhost:8080/teste`).

## 🚀 Funcionalidades

- **DFA e NFA**: Suporte nativo para processamento tanto determinístico quanto não determinístico.
- **Validação de URLs**: Regras integradas para testar formatos comuns de links de internet (protocolos, host, porta, path).
- **Interface Gráfica (Web)**: Painel interativo construído em Streamlit, permitindo:
  - Navegação visual da simulação **passo a passo** (botões Próximo e Anterior).
  - Tabela de transição de estados ($\delta$) em tempo real.
  - Gravação dinâmica de grafos (usando Graphviz), destacando em amarelo os estados ativos.
- **Interface de Terminal (CLI)**: Uma suíte de testes rápida direto pelo terminal, ideal para testar URLs em massa e checar comportamentos.

## 🏗️ Arquitetura do Projeto

O projeto segue um padrão arquitetural limpo (MVC), garantindo a separação entre a interface e as regras matemáticas do autômato:
- **`models/`**: Lógica central (DFA, NFA) e o construtor das regras de validação (`builder.py`).
- **`views/`**: Componentes de interface visual (ex: layout do Streamlit em `web.py`).
- **`controllers/`**: Ponto de junção das lógicas e pontos de entrada da aplicação (`app.py` para Web e `main.py` para Terminal).

## 💻 Pré-requisitos e Instalação

Certifique-se de ter o Python instalado em sua máquina.

1. Clone o repositório e acesse a pasta:
   ```bash
   git clone https://github.com/JoaoPedro-77/automatos.git
   cd automatos
   ```

2. Crie e ative um ambiente virtual (recomendado):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # No Windows use: .venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
   *(Principais bibliotecas: `streamlit`, `pandas`, `graphviz`)*

> **Atenção:** Para que os grafos sejam renderizados corretamente pela biblioteca, é necessário que o motor do [Graphviz](https://graphviz.org/download/) esteja instalado no seu sistema operacional (ex: `sudo apt install graphviz` no Ubuntu, ou via instalador oficial no Windows).

## 🕹️ Como Executar

Você pode interagir com o simulador de duas formas:

### 1. Interface Web (Streamlit)
Oferece a melhor experiência visual interativa. Na raiz do projeto, execute:
```bash
streamlit run controllers/app.py
```
Uma aba será aberta no seu navegador. Insira a URL na barra lateral, escolha o autômato e acompanhe as transições em tempo real!

### 2. Interface de Terminal (CLI)
Para executar uma bateria de testes rápidos via terminal:
```bash
python controllers/main.py
```

## 👨‍💻 Desenvolvedor
Projeto criado com o objetivo de fixar os conceitos da disciplina de linguagens formais e autômatos. Fique à vontade para estudar o código e utilizá-lo como base!
