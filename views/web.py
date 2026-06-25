import streamlit as st

def render_interface(dfa_url, nfa_url, run_dfa_step_by_step, run_nfa_step_by_step, generate_graphviz_dot, get_transition_table):
    st.title("Simulador e Visualizador de Autômatos")
    st.markdown("Insira suas próprias URLs para testar as transições de estados passo a passo.")

    # Barra lateral para configurações e input da URL
    st.sidebar.header("Parâmetros")
    tipo_automato = st.sidebar.radio(
        "Escolha o Autômato:", 
        ["DFA (Determinístico)", "NFA (Não-Determinístico)"]
    )

    # Permitir testar URLs personalizadas
    palavra_input = st.sidebar.text_input(
        "Digite sua própria URL para testar:", 
        "http://localhost:8080/teste"
    )

    # Seleção da lógica do autômato
    is_nfa = (tipo_automato == "NFA (Não-Determinístico)")
    automata = nfa_url if is_nfa else dfa_url

    # Rodar simulação
    if is_nfa:
        historico = run_nfa_step_by_step(nfa_url, palavra_input)
    else:
        historico = run_dfa_step_by_step(dfa_url, palavra_input)

    max_steps = len(historico) - 1

    # Inicializar ou resetar o estado do passo atual no session_state
    if "passo" not in st.session_state:
        st.session_state.passo = 0
    if "prev_url" not in st.session_state:
        st.session_state.prev_url = palavra_input
    if "prev_tipo" not in st.session_state:
        st.session_state.prev_tipo = tipo_automato

    # Resetar o passo se a entrada mudar
    if st.session_state.prev_url != palavra_input or st.session_state.prev_tipo != tipo_automato:
        st.session_state.passo = 0
        st.session_state.prev_url = palavra_input
        st.session_state.prev_tipo = tipo_automato

    passo = min(max(0, st.session_state.passo), max_steps)
    st.session_state.passo = passo

    # Controles Passo a Passo (Botões)
    st.subheader("Execução Passo a Passo")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
    with col_btn1:
        if st.button("◀ Anterior", disabled=(passo == 0)):
            st.session_state.passo -= 1
            st.rerun()
    with col_btn2:
        if st.button("Avançar", disabled=(passo == max_steps)):
            st.session_state.passo += 1
            st.rerun()
    with col_btn3:
        if st.button("Resetar"):
            st.session_state.passo = 0
            st.rerun()

    # Resumo do passo atual
    step_idx, char_lido, active_states = historico[passo]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Caractere Lido no Passo", value=f"'{char_lido}'" if step_idx > 0 else "Início")
    with col2:
        st.metric(label="Estado(s) Ativo(s)", value=str(sorted(list(active_states))) if active_states else "Ø (Erro)")
    with col3:
        if passo == max_steps:
            aceitou = any(s in automata.F for s in active_states)
            if aceitou:
                st.success("URL ACEITA!")
            else:
                st.error("URL REJEITADA!")
        else:
            st.info("Simulação em andamento...")

    # Renderizar o grafo dinamicamente (Natividade Graphviz)
    st.markdown("### Grafo de Transições (Passo Atual em Amarelo)")
    dot_graph = generate_graphviz_dot(automata, is_nfa, active_states)
    st.graphviz_chart(dot_graph)

    # Tabela de Transição Delta
    st.markdown(r"### Tabela de Transição ($\delta$)")
    st.markdown(r"A matriz abaixo descreve a função de transição $\delta(q, \sigma)$ para cada categoria de símbolo:")
    df_transition = get_transition_table(automata, is_nfa)
    st.dataframe(df_transition, use_container_width=True, hide_index=True)
