def add_data():
    st.header('Adicionar obra')
    st.write('Aqui você pode adicionar novas obras à base de dados de Direito.')

    # Usamos um form para manter os inputs até o usuário clicar em "Adicionar"
    with st.form("form_adicionar_obra"):
        nome = st.text_input('Nome da obra', key="add_nome")
        autor = st.text_input('Autor', key="add_autor")
        periodo = st.selectbox('Período', ['1º Período', '2º Período', '3º Período', '4º Período', '5º Período'], key="add_periodo")

        # Escolhe matérias conforme o período (cada widget tem chave distinta)
        if periodo == '1º Período':
            materia = st.selectbox('Matéria', ['Teoria do Direito', 'Teoria do Estado Democrático',
                                              'Pensamento Jurídico Brasileiro', 'Economia',
                                              'Teoria do Direito Constitucional', 'Crime e Sociedade'],
                                   key="add_materia_p1")
        elif periodo == '2º Período':
            materia = st.selectbox('Matéria', ['Sociologia Jurídica', 'Programação para Advogados',
                                              'Teoria Geral do Direito Civil', 'Análise Econômica do Direito',
                                              'Penas e Medidas Alternativas', 'Design Institucional',
                                              'Organização do Estado e Direitos Fundamentais'],
                                   key="add_materia_p2")
        else:
            # Para períodos 3/4/5 deixo como input livre (cada chave distinta)
            materia = st.text_input('Matéria (digite o nome da matéria)', key="add_materia_other")

        # Botão de submit do form: só quando clicado o bloco abaixo executa
        submitted = st.form_submit_button('Adicionar')

        if submitted:
            nome_val = st.session_state.get("add_nome", "").strip()
            autor_val = st.session_state.get("add_autor", "").strip()
            # pega matéria a partir da variável local 'materia' (string) — já funciona independentemente da key
            materia_val = materia.strip() if isinstance(materia, str) else materia

            if not nome_val or not autor_val or not materia_val:
                st.warning("Preencha 'Nome', 'Autor' e 'Matéria' antes de adicionar.")
            else:
                # Agora, somente aqui, fazemos o append à lista correta
                if periodo == '1º Período':
                    if materia_val == 'Teoria do Direito':
                        st.session_state.teoria_do_direito.append({'nome': nome_val, 'autor': autor_val})
                    elif materia_val == 'Teoria do Estado Democrático':
                        st.session_state.teoria_do_estado_democratico.append({'nome': nome_val, 'autor': autor_val})
                    elif materia_val == 'Pensamento Jurídico Brasileiro':
                        st.session_state.pensamento_juridico_brasileiro.append({'nome': nome_val, 'autor': autor_val})
                    elif materia_val == 'Economia':
                        st.session_state.economia.append({'nome': nome_val, 'autor': autor_val})
                    elif materia_val == 'Teoria do Direito Constitucional':
                        st.session_state.teoria_constitucional.append({'nome': nome_val, 'autor': autor_val})
                    elif materia_val == 'Crime e Sociedade':
                        st.session_state.crime_sociedade.append({'nome': nome_val, 'autor': autor_val})
                    else:
                        # caso usuário digite algo diferente (segurança)
                        st.session_state.teoria_do_direito.append({'nome': nome_val, 'autor': autor_val})
                elif periodo == '2º Período':
                    if materia_val == 'Sociologia Jurídica':
                        st.session_state.sociologia_juridica.append({'nome': nome_val, 'autor': autor_val})
                    elif materia_val == 'Programação para Advogados':
                        st.session_state.programacao_para_advogados.append({'nome': nome_val, 'autor': autor_val})
                    elif materia_val == 'Teoria Geral do Direito Civil':
                        st.session_state.teoria_geral_direito_civil.append({'nome': nome_val, 'autor': autor_val})
                    elif materia_val == 'Análise Econômica do Direito':
                        st.session_state.analise_economica_direito.append({'nome': nome_val, 'autor': autor_val})
                    elif materia_val == 'Penas e Medidas Alternativas':
                        st.session_state.penas_medidas_alternativas.append({'nome': nome_val, 'autor': autor_val})
                    elif materia_val == 'Design Institucional':
                        st.session_state.design_institucional.append({'nome': nome_val, 'autor': autor_val})
                    elif materia_val == 'Organização do Estado e Direitos Fundamentais':
                        st.session_state.organizacao_estado_direitos_fundamentais.append({'nome': nome_val, 'autor': autor_val})
                    else:
                        st.session_state.programacao_para_advogados.append({'nome': nome_val, 'autor': autor_val})
                else:
                    # Para períodos 3/4/5: cria uma lista nova na sessão dinamicamente
                    key_map = {
                        '3º Período': 'periodo_3',
                        '4º Período': 'periodo_4',
                        '5º Período': 'periodo_5'
                    }
                    key = key_map.get(periodo, 'periodo_outros')
                    if key not in st.session_state:
                        st.session_state[key] = {}
                    if materia_val not in st.session_state[key]:
                        st.session_state[key][materia_val] = []
                    st.session_state[key][materia_val].append({'nome': nome_val, 'autor': autor_val})

                st.success(f'Obra {nome_val}, de {autor_val}, adicionada com sucesso!')
